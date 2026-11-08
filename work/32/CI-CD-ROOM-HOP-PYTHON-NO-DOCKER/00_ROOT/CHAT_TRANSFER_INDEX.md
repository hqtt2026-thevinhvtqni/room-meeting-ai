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
Sandbox Work 32 exists. GitHub branch `work/32-ci-cd-room-hop-python-no-docker` exists. Canonical GitHub path: `work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/`.

## Known blocker
`sandbox_list` lists files, but `sandbox_read` returns an empty object. Content read-back is not verified. Next: confirm mirror contents, fix/read around the read endpoint, complete read-only repository survey, then ask Vinh to approve implementation.