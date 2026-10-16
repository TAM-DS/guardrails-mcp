"""Deterministic checks for a small labeled suite; no general factual verifier."""
import re
from .contracts import Draft

EVALUATOR_VERSION = "0.1.1"

def evaluate(case, output):
    try:
        draft = Draft.model_validate(output)
    except Exception:
        return {"passed": False, "failures": ["schema"], "checks": {"schema": False}}
    forbidden = case.get("forbidden", [])
    # Matches are evidence for review, not a semantic verdict. Preserve raw scoring.
    phrase_matches = []
    for field in ("subject", "body"):
        value = getattr(draft, field)
        for pattern in forbidden:
            for match in re.finditer(pattern, value, re.I):
                phrase_matches.append({"field": field, "pattern": pattern,
                    "matched_text": match.group(), "start": match.start(), "end": match.end(),
                    "excerpt": value[max(0, match.start()-100):min(len(value), match.end()+100)]})
    checks = {
        "schema": True,
        "expected_decision": draft.decision == case["expected"],
        "hold_has_no_outreach": draft.decision == "draft" or not (draft.body.strip() or draft.subject.strip() or draft.claims),
        "draft_has_content": draft.decision != "draft" or bool(draft.subject.strip() and draft.body.strip()),
        "source_ids_exist": all(c.source_id in {s["id"] for s in case["input"]["sources"]} for c in draft.claims),
        "draft_has_references": draft.decision != "draft" or bool(draft.claims),
        "forbidden_phrases_absent": not bool(phrase_matches),
    }
    failures = [k for k, v in checks.items() if not v]
    hard_failures = [k for k in failures if k != "forbidden_phrases_absent"]
    return {"passed": all(checks.values()), "failures": failures, "checks": checks,
        "hard_failures": hard_failures, "review_required": bool(phrase_matches),
        "assessment": "fail" if hard_failures else "review" if phrase_matches else "pass",
        "phrase_matches": phrase_matches,
        "review_note": "Literal matches can include negation or quotations. Human review required; no semantic violation is established." if phrase_matches else None}
