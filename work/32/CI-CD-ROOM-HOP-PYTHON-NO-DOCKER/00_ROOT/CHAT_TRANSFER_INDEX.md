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
- G4 finding 2 (OPEN): `mcp` 2.x incompatible with `room_hop_mcp/adapter/server.py` (1.x API).
- Evidence issue: #39 (auto-maintained). #38 closed as duplicate.
- Main head moved since branch base (`d7266eb…` vs `cc3100c…`); main's requirements.txt also lacks the new deps.

## Handoff to Xu (per Vinh, 2026-11-04)
- Vinh's decision: record the proposal in the Work log for Xu to read and execute; NO further implementation from chat.
- Read: `02_EXTENSION/PHASE_B_HANDOFF_XU.md` — full proposal for the mcp fix (pin `mcp>=1.0,<2.0` preferred), run #5, G2 verdict recording, Phase C decision, and main-head reconciliation.
- G7 approval for the mcp pin must still be captured inside the Work process before Xu executes it.
