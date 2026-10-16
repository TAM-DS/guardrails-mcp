import hashlib
import json
import os
import time
import uuid
from importlib.resources import files
from .checks import EVALUATOR_VERSION, evaluate
from .contracts import Draft
from .prompts import PROMPTS
from . import store

def suite():
    return json.loads(files("guardrails_mcp").joinpath("data/signaldesk.json").read_text())

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def demo_output(case, variant):
    # Hand-authored fixtures demonstrate scoring; they are not model performance measurements.
    if case["expected"] != "draft":
        result = {"decision": case["expected"], "subject": "", "body": "", "claims": []}
    else:
        result = {"decision": "draft", "subject": "Reporting workflow question", "body": "Your team compiles weekly reports manually. Would a workflow review help?", "claims": [{"text": "Weekly reports are compiled manually.", "source_id": "M1"}]}
    if variant == "candidate" and case["id"] in ("suppressed", "missing-evidence", "seller-history"):
        result = {"decision": "draft", "subject": "A quick pilot", "body": "We already work with commercial-vehicle dealers. Could we discuss a pilot?", "claims": [{"text": "Manual reports", "source_id": "M1"}]}
    return result

def live_output(client, model, prompt, case):
    args = {"model": model, "instructions": prompt,
            "input": json.dumps(case["input"]), "text_format": Draft,
            "max_output_tokens": 2000, "store": False}
    if model == "gpt-5-mini":
        args["reasoning"] = {"effort": "low"}
    response = client.responses.parse(**args)
    usage = response.usage
    tokens = {"input": getattr(usage, "input_tokens", None), "output": getattr(usage, "output_tokens", None)}
    if response.status != "completed" or response.output_parsed is None:
        return None, tokens, "incomplete_or_refused"
    return response.output_parsed.model_dump(), tokens, None

def summarize(rows):
    metrics = {}
    for variant in ("baseline", "candidate"):
        group = [r for r in rows if r["variant"] == variant]
        metrics[variant] = {"passed": sum(r["passed"] for r in group), "total": len(group),
            "errors": sum(bool(r.get("error")) for r in group),
            "review_required": sum(bool(r.get("review_required")) for r in group),
            "review_only": sum(r.get("assessment") == "review" for r in group),
            "input_tokens": sum((r.get("tokens") or {}).get("input") or 0 for r in group),
            "output_tokens": sum((r.get("tokens") or {}).get("output") or 0 for r in group),
            "elapsed_seconds": round(sum(r["seconds"] for r in group), 3)}
    pairs = {}
    for r in rows:
        pairs.setdefault((r["case_id"],r["repeat"]), {})[r["variant"]] = r
    comparable = [v for v in pairs.values() if len(v)==2 and not any(r.get("error") for r in v.values())]
    regressions = [v["candidate"]["case_id"] for v in comparable if v["baseline"]["passed"] and not v["candidate"]["passed"]]
    improvements = [v["candidate"]["case_id"] for v in comparable if not v["baseline"]["passed"] and v["candidate"]["passed"]]
    return {"variants": metrics, "regressions": regressions, "improvements": improvements,
            "comparable_pairs": len(comparable), "not_compared_pairs": len(pairs)-len(comparable)}

def run(mode="demo", repeats=1, acknowledge_cost=False, client=None):
    if mode not in ("demo", "live") or type(repeats) is not int or not 1 <= repeats <= 3:
        raise ValueError("Mode must be demo/live; repeats must be 1–3")
    cases = suite()
    if mode == "live":
        if not acknowledge_cost:
            raise ValueError("Live evaluations require explicit CLI --acknowledge-cost")
        if client is None:
            if not os.getenv("OPENAI_API_KEY", "").strip():
                raise ValueError("OPENAI_API_KEY is not configured")
            from openai import OpenAI
            client = OpenAI(timeout=45, max_retries=0)
    run_id = uuid.uuid4().hex
    record = {"id": run_id, "created": store.now(), "status": "running", "mode": mode,
        "model": os.getenv("OPENAI_MODEL", "gpt-5-mini") if mode=="live" else "hand-authored-fixtures",
        "evaluator_version": EVALUATOR_VERSION, "scoring_policy": "All deterministic checks must pass; phrase matches require human review and are not proof of unsafe claims.",
        "suite_hash": digest(cases), "prompt_hashes": {k:digest(v) for k,v in PROMPTS.items()},
        "prompts": PROMPTS, "suite": cases, "repeats": repeats,
        "max_calls": len(cases)*2*repeats if mode=="live" else 0, "rows": [],
        "scope": "Known deterministic checks only; not semantic truth, security certification, or deployment approval."}
    store.save(record)
    try:
        for repeat in range(repeats):
            for case in cases:
                # Alternate variant order to reduce simple order effects; no statistical claim.
                order = ("baseline","candidate") if repeat % 2 == 0 else ("candidate","baseline")
                for variant in order:
                    start = time.perf_counter(); tokens=None; error=None; output=None
                    try:
                        if mode == "demo":
                            output=demo_output(case,variant)
                        else:
                            output,tokens,error=live_output(client,record["model"],PROMPTS[variant],case)
                    except Exception as exc:
                        # Do not persist exception text: it can contain request data or credentials.
                        error=type(exc).__name__
                    checks=evaluate(case,output) if error is None else {"passed":False,"failures":["provider_error"],"checks":{}}
                    record["rows"].append({"case_id":case["id"], "variant":variant,"repeat":repeat+1,
                        "output":output,"tokens":tokens,"error":error,
                        "seconds":round(time.perf_counter()-start,4),**checks})
                    record["summary"]=summarize(record["rows"]);store.save(record)
        record["status"]="completed_with_errors" if any(r["error"] for r in record["rows"]) else "completed"
    except BaseException:
        record["status"]="interrupted";store.save(record);raise
    store.save(record)
    return record
