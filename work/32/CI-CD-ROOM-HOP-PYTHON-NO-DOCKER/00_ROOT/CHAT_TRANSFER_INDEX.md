# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.
- CI gates before CD; CD/deployment deferred; no auto-merge/auto-deploy.
- Status semantics: PASS = executed with evidence; FAIL = executed and failed; BLOCKED = prerequisite unavailable; NOT RUN = not executed.
- Repair loop: max 3 attempts, then BLOCKED for human review.

## Current (2026-11-05, after run #7)
- Phase A: COMPLETE. Phase B CI pilot: **CI-side work COMPLETE** — workflow stable, evidence auto-published to issue #39.
- Run #7 (`95495b9`): G1 PASS; G2 FAIL with 3 failed / 185 passed — mcp pin `>=1.14,<2.0` effective (was 10 failed).
- Remaining G2 failures = product-drift (not CI):
  1. `room_hop_mcp/adapter/server.py` registers 4 tools; frozen contract requires 6 (`join_meeting`, `start_meeting` missing).
  2. `add_paste` schema lacks `maxLength` (contract: 1048576).
- G7: PASS (Vinh approved the mcp pin execution, 2026-11-05).

## Next steps (pending Vinh)
1. Decide product-repair path: Coder fixes server.py (2 tool registrations + maxLength) after approval, OR check whether main head `d7266eb…` already carries the fix (branch cut from older base `cc3100c…`).
2. After G2 PASS: reviewer checks diff/risks; decide Phase C scope (integration/E2E gates).
3. Reconcile Work branch with main head before any merge discussion; main's requirements.txt also needs the same dependency fix.
