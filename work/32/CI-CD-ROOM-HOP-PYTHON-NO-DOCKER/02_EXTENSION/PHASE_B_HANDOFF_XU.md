# Phase B Handoff Proposal — for Xu (AI-01)

Written: 2026-11-04 (Asia/Ho_Chi_Minh), by the Vibe agent, per Vinh's instruction: record the proposal in the Work log for Xu to read and execute; do not implement from chat.

## Context
Phase B CI pilot is live on branch `work/32-ci-cd-room-hop-python-no-docker` (workflow `.github/workflows/work32-ci-pilot.yml`, evidence auto-published to issue #39). Repair loop exhausted 3/3; current disposition G2 = BLOCKED pending human decision.

## G4 Finding 2 (open) — mcp SDK major-version incompatibility
- Evidence: CI run #4 (`750c08d`), log tail in issue #39.
- Symptom: 12+ unit tests FAIL with `AttributeError: 'Server' object has no attribute 'list_tools'` — e.g. `room_hop_mcp/adapter/server.py:32`, `tests/test_mcp_server.py`, `tests/test_f4_resource_limits.py`, `tests/test_message_v1.py`.
- Root cause: `mcp>=1.0` (added in repair 3/3) resolves to the latest 2.x SDK, whose `Server` API no longer exposes the 1.x decorators the code was written against.
- All remaining G2 failures trace to this single cause; collection/imports are clean.

## Proposed action for Xu (awaiting G7 approval inside the Work process)
1. Confirm the exact mcp major/minor the codebase targets (check ROOM-HOP provenance/baseline docs, e.g. ROOM-2026-001-BASELINE-FROZEN; verify against the MCP SDK changelog).
2. Preferred minimal fix: pin `mcp>=1.0,<2.0` in requirements.txt (Work branch only; record the exact resolved version as evidence).
   - Alternative (only if 2.x is required for other reasons): migrate `room_hop_mcp/adapter/server.py` to the 2.x API — larger diff, needs reviewer attention.
3. Push, let run #5 execute, record the G2 verdict in the Evidence Log and issue #39.
4. If G2 PASS: reviewer checks diff/risks; then decide Phase C scope (integration/E2E gates) with Vinh.
5. Integration note: main (`d7266eb…`) also has an incomplete requirements.txt — the same dependency fix must be included when reconciling the Work branch with the new main head.

## Status semantics reminder
PASS requires executed evidence. Until run #5 exists, G2 remains BLOCKED, not FAIL. No auto-merge, no deployment.
