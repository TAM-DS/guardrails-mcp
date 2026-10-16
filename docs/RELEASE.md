# Release — v0.1.1

Status: published to PyPI and the official MCP Registry on October 16, 2026. MIT licensed. Copyright © 2026 Tracy Anne Griffin Manning.

## Build

From a clean checkout, with a virtual environment activated:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

The wheel includes the fictional suite and all three entry points. The source distribution includes the registry manifest and documentation. `.env`, local databases and IDE settings must never be packaged. Rebuild after any license or metadata changes. Publish only the specific reviewed wheel and source archive, not unrelated old versions.

## Release notes

- Explicit phrase-match review evidence: matched text, field, pattern, offsets and context.
- Review-only assessment separated from other deterministic failures; raw conservative scores preserved.
- Evaluator version recorded in new runs; old records remain unchanged.
- 19 tests passed in Linux and on the maintainer's Mac.
- Mac MCP v0.1.1 verified through run_demo/get_run after reconnecting the server.
- Docker v0.1.1 rebuilt; updated guidance and retained legacy run visually confirmed.
- One live v0.1.0 comparison is documented with its apparent evaluator false positive, not silently rescored. See LIVE_REVIEW.md.

## Published package installation

```bash
uvx --from guardrails-mcp==0.1.1 guardrails-mcp
```

This launches a stdio MCP process and waits for a client. It does not start the dashboard. The MCP client launches this command itself. Configure an absolute GUARDRAILS_DATA_DIR to persist records consistently. No API key is required for MCP demo/read tools. Dashboard installation requires the dashboard extra.

## Publication evidence

- GitHub Actions build and publish jobs succeeded: [run 38944535947](https://github.com/TAM-DS/guardrails-mcp/actions/runs/38944535947).
- PyPI returned the 0.1.1 wheel and source distribution.
- A fresh Mac virtual environment installed from PyPI; demo run `dbf50e8080f1422a9a87e646705826de` completed with evaluator package 0.1.1, baseline 6/6, candidate 3/6, zero errors, and one phrase-only review case. These are seeded fixtures, not live model measurements.
- The maintainer published server.json with mcp-publisher; independent registry retrieval confirmed active version 0.1.1.
- Registry-driven client installation remains untested. A later local Docker exit-137 restart report remains under investigation; the container was stopped while preserving its named volume. Neither issue is hidden by the publication result.

## GitHub Actions Trusted Publisher setup

Workflow: `.github/workflows/publish-pypi.yml`. It runs manually from main, defaults to build-only, runs tests and distribution checks, and passes only those artifacts to a separate publishing job. Publishing uses the `pypi` GitHub environment and short-lived OIDC credentials, not a stored API token.

In PyPI account Publishing, add a pending GitHub publisher:

| Field | Value |
| --- | --- |
| PyPI project name | guardrails-mcp |
| Owner | TAM-DS |
| Repository | guardrails-mcp |
| Workflow filename | publish-pypi.yml |
| Environment | pypi |

After configuring PyPI, open the repository Actions tab, select Build and publish PyPI release, Run workflow on main, and select publish only when ready for the public upload. Build-only runs do not need PyPI authentication. Successful workflow execution and PyPI retrieval must be verified before claiming publication. Registry submission is separate.
