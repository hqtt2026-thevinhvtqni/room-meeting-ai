# W32-ADR-002 — MCP Public Boundary Contract Reconciliation

- Document Number: W32-ADR-002
- Priority: P1
- Author: Ka — CSA / Architecture & Backend Owner (delegated)
- Date-Time: 2026-11-04 (hour/minute not captured; not inferred)
- Status: DECIDED FOR WORK 32 CI SCOPE; runtime validation pending

## Context and evidence

The CI pilot failed at `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression`: T8 expected six MCP tools, including `join_meeting` and `start_meeting`, while the Public V1 adapter registered four.

Repository history and current contracts resolve the intended boundary:

1. Commit `73a454b4a806a47a738ab323b50ce4154a65d6b6` introduced `docs/MCP_PUBLIC_BOUNDARY_V1.md` and the original MCP V1 boundary with three read tools: `list_meetings`, `get_meeting`, `get_transcript`.
2. Commit `d9b0a1a5baea1498a940e8d4652c9e875915c05a` added `add_paste_to_meeting` as a fourth public tool.
3. Commit `a799106199976334ef740c80f566f801fb00c667` added Message v1.0 identity metadata and T8. T8's six-tool assertion conflicts with the earlier locked MCP public boundary. The same commit's integration client prose still describes four locked tools, while its implementation incorrectly adds a `join_meeting` requirement/method.
4. `API_CONTRACT.md` defines lifecycle operations, including `POST /meetings/{id}/join` and `POST /meetings/{id}/start`, as Core HTTP routes. They are not MCP Public V1 tools.

## Decision

- Work 32 CI treats the MCP Public V1 inventory as exactly four tools: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`.
- Meeting lifecycle join/start remains on the approved Core HTTP boundary. Do not expose duplicate MCP lifecycle tools.
- T8 is corrected to assert the four-tool contract, not deleted or skipped.
- MCP adapter must forward optional `identity_id` to `MeetingService.add_paste`; absence preserves the legacy unidentified paste path.
- Integration MCP client must require only the four locked tools; remove its unsupported `join_meeting` call.
- A dedicated CI test must launch the actual MCP stdio subprocess, assert exact tool inventory, and verify list/get/transcript plus both legacy and identified paste paths.

## Change scope

Only the MCP adapter, Integration client, T8 contract test, and CI E2E test/workflow are changed. No Core lifecycle or business logic is modified.

## Validation

- Source reconciliation: PASS (repository history and contracts inspected).
- Updated T8 and stdio E2E: COMMITTED; GitHub Actions run `41718470071` at SHA `5309f89984e5ab61d85c22e404babec88ace5995` is queued/pending at report creation.
- Runtime PASS is not claimed until that exact SHA completes successfully.

## Release boundary

No merge/rebase/cherry-pick to main, no secrets, no deployment, and no production mutation. Work 32 remains ACTIVE — NOT RELEASED.


---

## Addendum — Decision A: Browser Adapter reuses canonical MCP stdio (2026-11-05)

- Decision owner: Xu / AI-01, under Vinh's delegated Work32 execution authority.
- Decision: SELECT OPTION A. Work32 Public V1 remains stdio-only. Browser Adapter uses the existing integration.RoomHopIntegration client/session boundary. No Streamable HTTP MCP listener is added.
- Reason: Work32 already has a tested stdio subprocess/session client and CI E2E. This avoids creating a second network transport and preserves the existing server factory and ADR-002 public boundary.

### Implementation contract
1. Each Browser Adapter workflow submission opens one RoomHopIntegration.session(); context exit closes the session and child process.
2. Browser Adapter remains a synchronous FastAPI/Playwright boundary. Its sync submission function uses local asyncio.run to execute one async stdio session per workflow. No shared event loop, MCP session, or subprocess is stored globally. Concurrent workflows own separate child processes/sessions.
3. Child CWD and PYTHONPATH are pinned to the repository root derived from the Browser Adapter source location. The child environment explicitly overrides ROOM_HOP_MEETINGS_DIR with ROOMHOP_TEST_MEETINGS_DIR.
4. Submission is blocked unless ROOMHOP_TEST_MODE=1, explicit ROOMHOP_TEST_MEETING_ID, ROOMHOP_TEST_IDENTITY_ID, and absolute ROOMHOP_TEST_MEETINGS_DIR are present.
5. The selected store must already exist and contain .roomhop-disposable-test-store with exact content ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE. Missing/invalid marker blocks before subprocess creation. No automatic store creation or meeting provisioning is performed.
6. Before any tool call, actual MCP tool names must equal exactly the four ADR-002 names. The exact configured meeting must be present and active. No fallback meeting or identity is permitted.
7. Handoff calls only add_paste_to_meeting with the configured identity, then reads transcript and verifies the exact marker plus execution/evidence/work IDs and evidence filename.
8. No Core REST shortcut, HTTP MCP endpoint, :8020, or Browser Adapter's own /mcp route is used.

### Verification and limits
- Deterministic contract tests cover test-mode guard, required explicit store/identity, missing store, sentinel guard, exact tool inventory, no meeting fallback, inactive meeting rejection, exact target/identity, readback, and session cleanup.
- PC/live Browser Adapter E2E remains opt-in and requires the disposable-store marker plus explicit test target.
- This decision and code implementation do not prove the currently running PC PID 20468 is Work32. No PC process/service is started, stopped, restarted, or reconfigured here.
- No MCP live call, transcript mutation, merge to main, CD/deploy, production release, or strict coverage enablement is authorized by this addendum.

Status: Architecture decision RECORDED; implementation committed to Work32 branch; CI validation pending. Work32 remains ACTIVE — NOT RELEASED.
