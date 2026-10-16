# Illustrative governance mapping

These mappings describe a small evaluation prototype, not compliance, certification, or coverage of an entire framework. A human owns test definitions, failure investigation, and the release decision.

| NIST AI RMF 1.0 function | Implemented evidence/control | Known gap |
| --- | --- | --- |
| Govern | Documented evaluation boundary; MCP cannot authorize deployment or spend API credits | No authenticated roles, assigned organizational owner, or policy enforcement |
| Map | Six labeled fictional outreach cases and explicit intended behavior | No stakeholder/impact assessment; only one workflow |
| Measure | Case checks, provenance snapshots, latency and returned token counts, paired regressions | No semantic truth verifier, confidence intervals, comprehensive adversarial set, or live accuracy benchmark |
| Manage | Explicit CLI cost opt-in, request/output limits, error visibility | No daily budget, monitoring/alerting, automatic remediation, or release gate |

Selected OWASP Top 10 for LLM Applications 2025 topics are risk lenses, not a completed security checklist:

| Topic | Narrow check/control | Known gap |
| --- | --- | --- |
| LLM01 Prompt Injection | Seeded source-instruction case with selected forbidden phrases | No general injection detection or defense |
| LLM06 Excessive Agency | MCP exposes no delivery, deployment, or paid-run tool | Host permissions still matter; no production authorization system |
| LLM09 Misinformation | Source-ID checks and selected unsupported seller-history patterns | Valid references can accompany false claims; paraphrases evade patterns |
| LLM10 Unbounded Consumption | Fixed cases, repeats 1–3, output cap and request timeout, retries disabled | Repeated run invocations remain possible; no dollar cap or global quota |

Sources: https://www.nist.gov/itl/ai-risk-management-framework and https://genai.owasp.org/llm-top-10/ (reviewed October 16, 2026).
