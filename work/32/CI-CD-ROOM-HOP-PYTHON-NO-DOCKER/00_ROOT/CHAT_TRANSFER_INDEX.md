# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.
- CI gates before CD; CD/deployment deferred; no auto-merge/auto-deploy.
- Status semantics: PASS = executed with evidence and passed; FAIL = executed and failed; BLOCKED = prerequisite/evidence unavailable; NOT RUN = not executed.
- Repair loop: max 3 attempts, then BLOCKED for human review.

## Current (2026-11-04)
- Phase A (survey): COMPLETE.
- Phase B (minimal CI pilot): IN PROGRESS — 3 repair attempts used; run #4 verdict pending after requirements.txt fix.
- CI workflow: `.github/workflows/work32-ci-pilot.yml` (branch-scoped, evidence to issue #39).
- G4 finding: requirements.txt was missing requests, mcp, fastapi, uvicorn — fixed on the Work branch.
- Main head moved since branch base (`d7266eb…` vs base `cc3100c…`) — revisit before integration.

## Known blockers
- `sandbox_read` MCP endpoint returns empty content (worked around via GitHub read-back).
- G3/G5 BLOCKED by design until Phase C approval.
- CI job-log download via API requires repo admin; evidence flows through issue #39 instead.
