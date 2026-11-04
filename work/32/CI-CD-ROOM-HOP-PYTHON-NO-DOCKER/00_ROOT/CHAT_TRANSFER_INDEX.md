# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- Proposed CI engine: GitHub Actions with a Python runner.
- Start with CI gates and evidence; CD/deployment deferred.
- No auto-merge or auto-deployment.
- PASS needs evidence; FAIL means an executed check failed; BLOCKED means a prerequisite/evidence path is unavailable; NOT RUN means not executed.
- Proposed repair loop: maximum 3 attempts, then BLOCKED for human review.

## Current
- Phase A (survey) COMPLETE: mirror verified via GitHub read-back; baseline inventory done (requirements, pytest.ini, no prior workflows).
- Phase B (minimal CI pilot) IN PROGRESS: workflow `work32-ci-pilot.yml` added on the Work branch on 2026-11-04, authorized by Vinh ("triển khai tiếp").
- Main head moved since branch base: `d7266eb9bfedfc534fc87d56548e47841bb583b9` vs base `cc3100c835ad87ac9670a2ba38dc2c2dfae63755` — integration plan must be revisited.
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.

## Known blockers
- `sandbox_read` MCP endpoint still returns empty content (worked around via GitHub read-back; not blocking this Work).
- Gates G3/G5 BLOCKED by design until Phase C approval.
