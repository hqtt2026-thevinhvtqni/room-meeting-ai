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
