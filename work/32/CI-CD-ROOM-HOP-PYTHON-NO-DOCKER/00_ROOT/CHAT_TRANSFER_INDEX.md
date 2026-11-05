# Chat Transfer Index — Work 32

## Goal
Design CI/CD for Python-based ROOM-HOP, no Docker, survey first and no PC changes.

## Decisions
- CI engine: GitHub Actions, Python 3.11 hosted runner, no Docker.
- CI gates before CD; CD/deployment deferred; no auto-merge/auto-deploy.
- Status semantics: PASS = executed with evidence; FAIL = executed and failed; BLOCKED = prerequisite unavailable; NOT RUN = not executed.
- Repair loop: max 3 attempts, then BLOCKED for human review.

## Current (2026-11-05, after main-head check)
- Phase A: COMPLETE. Phase B CI pilot: CI-side COMPLETE — run #7 (`95495b9`): G1 PASS; G2 3 failed / 185 passed; evidence auto-published to issue #39.
- Main-head check (per Vinh): main `d7266eb…` does NOT carry a fix for the 3 failures.
- Remaining G2 failures classified:
  - 2× F4 design-marker tests — INTENTIONAL expected-FAIL per the test file header (evidence for a future F4 implementation round).
  - 1× T8 six-tools contract — genuine drift: MCP adapter registers 4 of 6 frozen tools (missing `join_meeting`, `start_meeting`).
- Full analysis: Evidence Log section "Main-head reconciliation check (2026-11-05)".

## Next steps (pending Vinh)
1. Decide: (a) Coder registers the 2 missing MCP tools on the Work branch, and (b) either implement F4 maxLength (1048576) or scope the 2 design-marker tests out of the hard G2 gate.
2. After G2 PASS: reviewer checks diff/risks; decide Phase C scope.
3. Reconcile with main head before merge; main's requirements.txt also needs the same dependency fix.
