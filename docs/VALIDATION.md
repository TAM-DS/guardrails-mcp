# Validation — v0.1.0

October 16, 2026; Linux, Python 3.12.14.

- 15 automated tests passed. Includes separate-process MCP initialization, tool discovery, demo execution and rejection of invalid run IDs.
- Seeded demo: baseline 6/6, candidate 3/6; three deliberately introduced regressions. These are fixtures, not measured LLM results.
- Actual SignalDesk v0.3.1 checkout was loaded against a temporary database. Meridian's fixture passed the evaluator's narrow checks; Brightfield approval returned HTTP 409. No customer records or live API calls were used. This is an offline integration harness, not an installed runtime hook.
- Gradio dashboard returned HTTP 200 and its real demo callback persisted the expected 6/6 versus 3/6 result. Browser visual layout was not verified here. A build-environment SOCKS proxy required clearing proxy variables for localhost testing; this is not a user setup requirement.
- Live provider contracts, incomplete responses, usage handling and sanitized errors were tested with mocks. No live evaluation was run by the assistant.
- MCP client-specific desktop configuration, Mac installation, and Docker execution require user-side acceptance. Docker is unavailable in this build environment.
- Registry publication is pending distribution packaging and verification. This project is not registered or certified.

Known gaps: phrase-based checks miss paraphrases; source-ID membership is not entailment; six public cases are insufficient for a general quality claim; repeated samples do not establish statistical significance; there is no semantic-drift metric or authenticated multi-user service. Abrupt process termination can leave a running record.

## v0.1.1 — October 16, 2026

- 19 automated tests passed in the build environment, including the negated-guarantee example, a direct guarantee, suppression plus phrase match, evaluator versioning and unchanged legacy records.
- v0.1.0 user-side acceptance completed: Mac installation (15 tests), actual SignalDesk fixture/API integration, Docker demo, persistence across restart, and OpenAI desktop MCP list_cases/run_demo/get_run. The patch still needs the normal Mac update and restart.
- The maintainer ran one live comparison and retrieved it through MCP. See [human review](LIVE_REVIEW.md). Raw results remain 6/6 versus 1/6; one apparent phrase false positive is documented alongside them.
- Phrase evidence and review-only counts are reporting additions; they do not establish semantic truth or automatically clear a flagged output. Existing records are not migrated or rescored.

## Maintainer acceptance completed for v0.1.1

Mac: 19 tests passed in 0.43 seconds. Desktop MCP returned evaluator_version 0.1.1 and seller-history review evidence for run 906378402c254bc9b5565b4be4374ede after toggling the connection off/on. Docker rebuilt successfully; the maintainer's screenshot confirms new Review guidance and the retained v0.1.0 seeded run. These checks do not rerun or alter the original live evaluation.

## Release packaging checks

Wheel and source distribution built successfully with python-build; both passed twine check. The wheel was installed into an isolated target directory and exercised from outside the checkout (using existing dependency versions): six cases loaded, demo completed, evaluator 0.1.1 and review-only evidence confirmed. This is not a clean-machine dependency-resolution test. Archive inspection found no .env, SQLite or IDE files. Registry server.json passed the official 2025-12-11 JSON Schema. PyPI and registry publication remain pending; no license is selected.
