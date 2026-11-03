# W32-EVIDENCE-002 — Auto E2E Pipeline Review

- Document Number: W32-EVIDENCE-002
- Priority: P1
- Author: Ka — CSA / Architecture & Backend Owner (delegated)
- Date-Time: 2026-11-04 (hour/minute not captured; not inferred)
- Status: REVIEW RECORDED; EXECUTION PENDING

## Scope
Review the current GitHub CI workflow, MCP public boundary implementation, and tests before extending automatic E2E. No Core or MCP application source was changed in this evidence step.

## Verified source observations
1. Branch: `work/32-ci-cd-python-ci-v2`.
2. Workflow `.github/workflows/ci.yml` has separate `unit` and `e2e` jobs. Previously `e2e` declared `needs: unit`, so a unit failure prevented collection of E2E evidence.
3. Commit `c45e16362b63e5e10c2915aa7cad7465b7635a78` removes only that dependency. The two jobs now run independently; any failed job still makes the overall workflow fail.
4. E2E job runs existing in-process suites plus `tests/test_ci_live_e2e.py`, which starts a real Uvicorn listener on an ephemeral loopback port and uses HTTP requests for a local roundtrip. It does not require external services.
5. `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression` expects six public tools, including `join_meeting` and `start_meeting`; current `room_hop_mcp/adapter/server.py` registers four tools only: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`.
6. The same T8 test sends optional `identity_id` to `add_paste_to_meeting`. Current adapter schema declares it optional, but the handler currently calls `service.add_paste(meeting_id, text)` without forwarding it. This is a separate implementation/test-contract mismatch.
7. Existing `tests/test_mcp_server.py` asserts legacy schema requirements and delegation. It does not establish that `join_meeting` / `start_meeting` are intended public MCP tools.

## Decision / guardrail
- Do not change Core or expand MCP public API merely to make CI green.
- Do not weaken, skip, or delete T8.
- Keep the two T8 discrepancies separate: (A) expected tool inventory versus current public boundary; (B) optional identity_id declared but not propagated.
- Resolve intended public API against authoritative API_CONTRACT / approved MCP boundary decision and source history before any application patch.
- Continue E2E execution independently from unit gate so failures are visible, not hidden behind job dependency.
- No main merge, secrets, deployment, or production mutation.

## Current evidence status
- Workflow source update: COMMITTED on Work branch.
- New workflow execution for commit: NOT YET VERIFIED at report creation.
- Unit/E2E result on updated workflow: NOT RUN / PENDING.
- Overall Work 32: ACTIVE — NOT RELEASED.
