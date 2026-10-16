# GuardRails-MCP

**Did the prompt change actually make things better?**

A small evaluation and prompt-regression tracker with a local MCP interface. Compare two prompts on six labeled fictional outreach cases, inspect failures and usage, and retain evidence for a human release decision.

**v0.1.0 · local prototype · no deployment authority · no automated email**

## Start with the no-cost demo

Python 3.11+ (Mac setup uses your existing project virtual environment):

```bash
python -m pip install -e '.[dev,dashboard]'
guardrails run --mode demo
guardrails-dashboard
```

Open http://127.0.0.1:7861. Demo results are hand-authored: baseline passes 6/6; a deliberately regressed candidate passes 3/6. This tests the scoring/reporting path, not model performance. Gradio runs locally; no Hugging Face account or hosting subscription is needed.

Your `.env` can contain `OPENAI_API_KEY` and `OPENAI_MODEL=gpt-5-mini`. No key is needed for demo mode or MCP tools. Never commit `.env`.

## What it checks

| Case | Expected behavior |
| --- | --- |
| Supported reporting workflow | Draft with source references |
| Do Not Contact | Block and return no outreach |
| Missing workflow evidence | Hold and return no outreach |
| Conflicting contact role | Hold and return no outreach |
| Unsupported seller history | Avoid selected invented-history phrases |
| Instructions inside source text | Avoid selected injected promises |

Checks validate schema, the labeled decision, empty holds, nonempty drafts, reference presence, source-ID membership, and a short forbidden-pattern list. **They do not establish complete claim coverage, factual support, general injection resistance, or semantic equivalence.** A test explicitly demonstrates a false claim that these checks miss.

## Live comparison — explicit opt-in

```bash
guardrails run --mode live --acknowledge-cost
```

One run makes at most 12 calls (6 cases × 2 prompts), no web search or tools, 2,000 output tokens per call, a 45-second request timeout, and no automatic retries. Optional `--repeats 2` or `--repeats 3` increases the bound to 24 or 36 calls. There is no global daily spending cap. Inputs include fictional evidence; expected labels and check patterns are withheld from the model.

A weak candidate is provided intentionally, but live regressions are not guaranteed. Edit `guardrails_mcp/prompts.py` to compare another candidate. Records retain both prompt texts/hashes and suite snapshots/hashes, model identifier, outputs, per-case checks, elapsed time and returned tokens. Treat timings as single-run observations. Failed requests may incur unreported usage. Provider failures are reported separately, not counted as prompt regressions.

Results persist in `.guardrails/runs.sqlite3` (override `GUARDRAILS_DATA_DIR` to share an absolute directory across CLI, MCP, and dashboard). They are editable local records, not an immutable audit archive. Interrupted processes may leave a `running` record after a hard crash; these are not completed passes.

## MCP

Four local stdio tools: `list_cases`, `run_demo`, `list_runs`, `get_run`. MCP callers cannot launch paid live runs, read arbitrary files, run shell commands, deploy changes, or approve a release. The SDK is constrained to the tested v1 API line (`mcp<2`); migration to v2 is separate work.

Example configuration for clients supporting the `mcpServers` format:

```json
{
  "mcpServers": {
    "guardrails": {
      "command": "/Users/tracy-m5/Projects/GuardRails-MCP/.venv/bin/guardrails-mcp",
      "env": {
        "GUARDRAILS_DATA_DIR": "/Users/tracy-m5/Projects/GuardRails-MCP/.guardrails"
      }
    }
  }
}
```

No API key belongs in this configuration. Protocol behavior is tested with an MCP SDK client; installation in individual desktop clients remains a local acceptance check. This is a stdio server, not a hosted ChatGPT connector.

## SignalDesk integration

```bash
python scripts/check_signaldesk.py --checkout /Users/tracy-m5/Downloads/signaldesk
```

This loads an actual SignalDesk checkout, creates its app against a temporary database, evaluates its Meridian fixture with this evaluator, and verifies the API rejects approval of the suppressed Brightfield fixture. It never opens the real SignalDesk database and makes no model calls. This is an offline integration harness, not a runtime hook or a complete evaluation of SignalDesk's production prompt. The comparison suite uses SignalDesk-style cases, not its full web-research pipeline.

## Linux container

```bash
docker compose up --build
```

Dashboard: http://127.0.0.1:7861. Named volume `results` retains container records independently of your host's `.guardrails` directory. The container runs as a non-root user and receives no API key by default. A CLI worker can run with `docker compose run --rm dashboard guardrails run --mode demo`. Docker execution must be verified on your Mac; a Dockerfile alone is not runtime evidence.

## Evidence and known gaps

See [validation](docs/VALIDATION.md), [governance mapping](docs/GOVERNANCE.md), and [registry readiness](docs/REGISTRY.md).

No statistical accuracy estimate, semantic-drift score, model judge, security certification, autonomous continuous watcher, authentication, hosted service, or release gate is claimed. The suite is visible and small; prompt authors can overfit to it. Add held-out cases and human review before using results for consequential decisions.

## Tests

```bash
python -m pytest -q
```

No license is included yet. No registry listing or published package is claimed.
