# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.
- CI gates before CD; CD/deployment deferred; no auto-merge/auto-deploy.
- Status semantics: PASS = executed with evidence; FAIL = executed and failed; BLOCKED = prerequisite unavailable; NOT RUN = not executed.
- Repair loop: max 3 attempts, then BLOCKED for human review.

## Current (2026-11-05)
- Phase A (survey): COMPLETE.
- Phase B (CI pilot): G7 APPROVED by Vinh ("triển khai tiếp w32", 2026-11-05). mcp pinned to `>=1.14,<2.0`; run #7 verifying.
- Run history #1–#6 and both G4 findings recorded in the Evidence Log; evidence auto-published to issue #39.
- Latest measured suite state (run #6): 178 passed / 10 failed — all 10 failures the single mcp 2.x API cause.
- Main head moved since branch base (`d7266eb…` vs `cc3100c…`); main's requirements.txt also lacks the new deps — include on integration.

## Next steps
1. Record run #7 G2 verdict in the Evidence Log.
2. If G2 PASS: reviewer checks diff/risks, then decide Phase C scope (integration/E2E gates) with Vinh.
3. Reconcile Work branch with new main head before any merge discussion.
