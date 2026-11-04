# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.
- CI gates before CD; CD/deployment deferred; no auto-merge/auto-deploy.
- Status semantics: PASS = executed with evidence; FAIL = executed and failed; BLOCKED = prerequisite unavailable; NOT RUN = not executed.
- Repair loop: max 3 attempts, then BLOCKED for human review.

## Current (2026-11-04, end of session)
- Phase A (survey): COMPLETE.
- Phase B (CI pilot): workflow live and evidence-first; G0/G1/G6 PASS; G2 BLOCKED at repair-loop exhaustion (3/3).
- G4 finding 2 (OPEN): `mcp` SDK 2.x incompatible with `room_hop_mcp/adapter/server.py` (1.x API). Candidate fix: pin `mcp>=1.0,<2.0` — awaiting Vinh.
- Evidence issue: #39 (auto-maintained). #38 closed as duplicate.
- Main head moved since branch base (`d7266eb…` vs `cc3100c…`); main's requirements.txt also lacks the deps — fix applies there too on integration.

## Next steps (pending Vinh)
1. Decide on mcp pin `>=1.0,<2.0` (G7 approval → apply → run #5 → record G2 verdict).
2. If PASS: reviewer checks diff/risks, then decide Phase C scope (integration/E2E gates).
3. Reconcile Work branch with new main head before any merge discussion.
