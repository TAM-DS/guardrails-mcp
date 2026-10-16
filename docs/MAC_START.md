# Mac handoff

Existing project: your local checkout of this repository.

The existing `.env` and `.venv` stay local. Before updating, inspect `git status --short`. If only `.gitignore` has local modifications, preserve it with:

```bash
git stash push -m "Local setup before GuardRails v0.1" -- .gitignore
git pull --ff-only https://github.com/TAM-DS/guardrails-mcp.git main
python -m pip install -e '.[dev,dashboard]'
python -m pytest -q
guardrails run --mode demo
guardrails-dashboard
```

If Git reports other local edits, divergent history, or a merge error, stop and share that message rather than resetting files. The new `.gitignore` already excludes `.env`, `.venv`, and `.idea`; keep the stash as a backup rather than applying it automatically.

Open http://127.0.0.1:7861. Expect a completed **demo** record with 6 baseline passes, 3 candidate passes, and 3 seeded regressions. Refresh results to confirm the run persists.

Start with the host dashboard. Docker and an MCP desktop client are separate acceptance steps after this succeeds. No paid API run is required for this milestone.
