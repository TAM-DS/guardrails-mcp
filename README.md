# GuardRails-MCP

**Did the prompt change actually make things better?**

A small evaluation and prompt-regression tracker with a local MCP interface. Compare two prompts on six labeled fictional outreach cases, inspect failures and usage, and retain evidence for a human release decision.

**v0.1.1 · local prototype · no deployment authority · no automated email**

Published October 16, 2026: [PyPI v0.1.1](https://pypi.org/project/guardrails-mcp/0.1.1/) · [Official MCP Registry record](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.TAM-DS%2Fguardrails-mcp/versions/0.1.1). Registration establishes listing and ownership checks, not security certification.

## Why this exists

Prompt changes often ship without evidence. A prompt is edited, a few outputs look fine, and it goes live. GuardRails-MCP gives a team a repeatable, reviewable record of what changed and what broke *before* a human signs off.

**Who it is for:** teams building agentic or LLM workflows that need release evidence, and the AI assurance, risk, and governance reviewers who have to ask for it.

**What it is not:** an approval authority. It produces evidence. A person makes the release decision.

## How it works

```mermaid
flowchart LR
    A[Baseline prompt] --> C[Six labeled cases]
    B[Candidate prompt] --> C
    C --> D[Deterministic checks]
    D --> E[Run record: prompt hashes, suite hash, evaluator version, outputs]
    E --> F{Phrase match only?}
    F -- yes --> G[Flag: review required]
    F -- no --> H[Pass or hard fail]
    G --> I[Human reviews evidence]
    H --> I
    I --> J[Release decision<br/>outside this tool]
```

## Governance at a glance

| Enforced by code | Left to a human |
| --- | --- |
| Schema, labeled decision, empty holds, nonempty drafts, reference presence, source-ID membership, short forbidden-pattern list | The release decision |
| Live runs bounded to at most 12 calls (24 or 36 with repeats), 2,000 output tokens per call, 45-second timeout, no automatic retries | Judging whether a phrase match is a real unsafe claim |
| Paid live runs require `--acknowledge-cost`; MCP callers cannot launch them | Claim coverage and factual support |
| Four local MCP tools only: no arbitrary file reads, shell commands, deployments, or approvals | Adding held-out cases and checking for overfitting |
| Each run records prompt texts and hashes, suite snapshot and hash, evaluator version, model, outputs, and per-case checks | Record retention and immutability (local records are editable) |
| Provider failures are reported separately from prompt regressions | Spending limits across days (there is no global daily cap) |

### NIST AI RMF 1.0 mapping (illustrative)

This describes the design of a small evaluation prototype. It is not compliance, certification, or coverage of an entire framework. The full table, including OWASP LLM Top 10 lenses, is in [docs/GOVERNANCE.md](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/GOVERNANCE.md).

| Function | Implemented evidence or control | Known gap |
| --- | --- | --- |
| Govern | Documented evaluation boundary; MCP cannot authorize deployment or spend API credits | No authenticated roles, assigned organizational owner, or policy enforcement |
| Map | Six labeled fictional outreach cases and explicit intended behavior | No stakeholder or impact assessment; only one workflow |
| Measure | Case checks, provenance snapshots, latency and returned token counts, paired regressions | No semantic truth verifier, confidence intervals, comprehensive adversarial set, or live accuracy benchmark |
| Manage | Explicit CLI cost opt-in, request and output limits, error visibility | No daily budget, monitoring or alerting, automatic remediation, or release gate |

## Dashboard preview

[![GuardRails-MCP dashboard with seeded comparison results and recorded evaluator version](https://github.com/TAM-DS/guardrails-mcp/raw/main/docs/images/dashboard-overview.png)](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/images/dashboard-overview.png)

*Seeded demo using six fictional cases: baseline 6/6, deliberately regressed candidate 3/6. These are hand-authored fixtures, not measured model performance.*

**Recorded-run details, review guidance, and known gaps**

[![Recorded-run metadata with review guidance and known gaps](https://github.com/TAM-DS/guardrails-mcp/raw/main/docs/images/review-guidance.png)](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/images/review-guidance.png)

*The interface keeps evaluator version, prompt provenance, review guidance, and known gaps visible. This screenshot shows the guidance and run metadata; it does not display an individual phrase-match assessment.*

## Start with the no-cost demo

Python 3.11+, in an activated virtual environment:

```
python -m pip install "guardrails-mcp[dashboard]==0.1.1"
guardrails run --mode demo
guardrails-dashboard
```

Open <http://127.0.0.1:7861>. Demo results are hand-authored: baseline passes 6/6; a deliberately regressed candidate passes 3/6. This tests the scoring and reporting path, not model performance. Gradio runs locally; no Hugging Face account or hosting subscription is needed.

Your `.env` can contain `OPENAI_API_KEY` and `OPENAI_MODEL=gpt-5-mini`. No key is needed for demo mode or MCP tools. Never commit `.env`.

For source development, clone this repository and install with `python -m pip install -e '.[dev,dashboard]'`.

## What it checks

| Case                            | Expected behavior                       |
| ------------------------------- | --------------------------------------- |
| Supported reporting workflow    | Draft with source references            |
| Do Not Contact                  | Block and return no outreach            |
| Missing workflow evidence       | Hold and return no outreach             |
| Conflicting contact role        | Hold and return no outreach             |
| Unsupported seller history      | Avoid selected invented-history phrases |
| Instructions inside source text | Avoid selected injected promises        |

Checks validate schema, the labeled decision, empty holds, nonempty drafts, reference presence, source-ID membership, and a short forbidden-pattern list. **They do not establish complete claim coverage, factual support, general injection resistance, or semantic equivalence.** A test explicitly demonstrates a false claim that these checks miss.

### Phrase matches require review

A literal pattern match is **not proof of an unsafe claim**. New records include `phrase_matches` with field, pattern, matched text, offsets and surrounding excerpt; `review_required`; and an `assessment` of `pass`, `review`, or `fail`. A phrase-only failure receives `review`; other deterministic failures remain `fail` even when a phrase also matches. This does not automatically approve negations or quotations.

Raw `passed`, `failures`, and regression counts remain conservative and unchanged in meaning: every check must pass. Summary `review_only` counts identify phrase-only cases within those raw failures. `hard_failures` excludes phrase matches but does not imply semantic verification. New runs record evaluator version `0.1.1`. Existing records are never automatically rescored or rewritten, and old runs lack the new review fields.

See [the first live run review](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/LIVE_REVIEW.md) for an observed false positive and the limits of its interpretation.

## Live comparison — explicit opt-in

```
guardrails run --mode live --acknowledge-cost
```

One run makes at most 12 calls (6 cases × 2 prompts), no web search or tools, 2,000 output tokens per call, a 45-second request timeout, and no automatic retries. Optional `--repeats 2` or `--repeats 3` increases the bound to 24 or 36 calls. There is no global daily spending cap. Inputs include fictional evidence; expected labels and check patterns are withheld from the model.

A weak candidate is provided intentionally, but live regressions are not guaranteed. Edit `guardrails_mcp/prompts.py` to compare another candidate. Records retain both prompt texts and hashes, suite snapshots and hashes, model identifier, outputs, per-case checks, elapsed time and returned tokens. Treat timings as single-run observations. Failed requests may incur unreported usage. Provider failures are reported separately, not counted as prompt regressions.

Results persist in `.guardrails/runs.sqlite3` (override `GUARDRAILS_DATA_DIR` to share an absolute directory across CLI, MCP, and dashboard). They are editable local records, not an immutable audit archive. Interrupted processes may leave a `running` record after a hard crash; these are not completed passes.

## MCP

Four local stdio tools: `list_cases`, `run_demo`, `list_runs`, `get_run`. MCP callers cannot launch paid live runs, read arbitrary files, run shell commands, deploy changes, or approve a release. The SDK is constrained to the tested v1 API line (`mcp<2`); migration to v2 is separate work.

Example configuration for clients supporting the `mcpServers` format. Replace the paths with your own:

```
{
  "mcpServers": {
    "guardrails": {
      "command": "/path/to/your/.venv/bin/guardrails-mcp",
      "env": {
        "GUARDRAILS_DATA_DIR": "/path/to/your/.guardrails"
      }
    }
  }
}
```

No API key belongs in this configuration. Protocol behavior is tested with an MCP SDK client, and the maintainer verified `list_cases`, `run_demo` and `get_run` through the OpenAI desktop app, including at v0.1.1. This is a stdio server, not a hosted ChatGPT connector. Installing through the registry listing has not been tested; see [validation](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/VALIDATION.md).

## SignalDesk integration

```
python scripts/check_signaldesk.py --checkout /path/to/signaldesk
```

This loads an actual SignalDesk checkout, creates its app against a temporary database, evaluates its Meridian fixture with this evaluator, and verifies the API rejects approval of the suppressed Brightfield fixture. It never opens the real SignalDesk database and makes no model calls. This is an offline integration harness, not a runtime hook or a complete evaluation of SignalDesk's production prompt. The comparison suite uses SignalDesk-style cases, not its full web-research pipeline.

## Linux container

```
docker compose up --build
```

Dashboard: <http://127.0.0.1:7861>. Named volume `results` retains container records independently of your host's `.guardrails` directory. The container runs as a non-root user and receives no API key by default. A CLI worker can run with `docker compose run --rm dashboard guardrails run --mode demo`. The maintainer verified the Docker demo and persistence across a container restart. One earlier unexplained container exit (code 137) is documented in [validation](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/VALIDATION.md); its cause is unconfirmed.

## Evidence and known gaps

See [validation](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/VALIDATION.md), [governance mapping](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/GOVERNANCE.md), [release notes](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/RELEASE.md), and [registry listing](https://github.com/TAM-DS/guardrails-mcp/blob/main/docs/REGISTRY.md).

No statistical accuracy estimate, semantic-drift score, model judge, security certification, autonomous continuous watcher, authentication, hosted service, or release gate is claimed. The suite is visible and small; prompt authors can overfit to it. Add held-out cases and human review before using results for consequential decisions.

## Roadmap

Not built yet. These are the gaps described above, listed as candidate next steps:

- **Held-out cases** kept separate from the visible suite, to reduce overfitting.
- **Optional model-judge check**, clearly labeled and kept separate from the deterministic checks.
- **Immutable audit logging**, so run records cannot be edited after the fact.
- **Semantic checks** for claim coverage and factual support beyond phrase matching.
- **A daily spend cap** for live runs.

## Tests

```
python -m pytest -q
```

## License

Licensed under the [MIT License](https://github.com/TAM-DS/guardrails-mcp/blob/main/LICENSE). Copyright © 2026 Tracy Anne Griffin Manning.
