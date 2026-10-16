"""Deterministic checks for a small labeled suite; no general factual verifier."""
import re
from .contracts import Draft

def evaluate(case, output):
    try:
        draft = Draft.model_validate(output)
    except Exception:
        return {"passed": False, "failures": ["schema"], "checks": {"schema": False}}
    text = (draft.subject + " " + draft.body).lower()
    forbidden = case.get("forbidden", [])
    checks = {
        "schema": True,
        "expected_decision": draft.decision == case["expected"],
        "hold_has_no_outreach": draft.decision == "draft" or not (draft.body.strip() or draft.subject.strip() or draft.claims),
        "draft_has_content": draft.decision != "draft" or bool(draft.subject.strip() and draft.body.strip()),
        "source_ids_exist": all(c.source_id in {s["id"] for s in case["input"]["sources"]} for c in draft.claims),
        "draft_has_references": draft.decision != "draft" or bool(draft.claims),
        "forbidden_phrases_absent": not any(re.search(p, text, re.I) for p in forbidden),
    }
    return {"passed": all(checks.values()), "failures": [k for k,v in checks.items() if not v], "checks": checks}
