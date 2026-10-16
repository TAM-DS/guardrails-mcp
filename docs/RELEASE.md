# Release preparation — v0.1.1

Status: prepared for review; not published to PyPI or the MCP Registry. MIT licensed. Copyright © 2026 Tracy Anne Griffin Manning.

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

## Installation after PyPI publication only

```bash
uvx --from guardrails-mcp==0.1.1 guardrails-mcp
```

This launches a stdio MCP process and waits for a client. It does not start the dashboard. The MCP client launches this command itself. Configure an absolute GUARDRAILS_DATA_DIR to persist records consistently. No API key is required for MCP demo/read tools. Dashboard installation requires the dashboard extra.

## Remaining publication steps

1. MIT license approved and included in package metadata and archives; review the final artifacts.
2. Authenticate to the maintainer's PyPI account and establish package ownership. A name lookup returning 404 does not reserve the name.
3. Upload the reviewed artifacts using PyPI tooling. Never paste credentials into chat.
4. Test installation from PyPI in a fresh environment.
5. Authenticate the GitHub namespace with the official MCP publisher and submit server.json.
6. Retrieve the registry entry and verify that its install configuration works.

A schema-valid manifest is preparation, not registration, certification, or a verified package listing.
