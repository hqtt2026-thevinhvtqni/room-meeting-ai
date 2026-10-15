# Work 28 — MCP Tool Contract Registry v1

Status: DRAFT / NOT REGISTERED IN LIVE MCP
Contract version: 1.0.0
Authority: Vinh | Build lead: Xu

## Existing tools observed in the current connector session

The current connected ROOM-HOP tool surface exposes 18 operations. This is not proof
that it equals the live PC MCP :8020 registry.

- Meetings: list_meetings, get_meeting, get_transcript, join_meeting, start_meeting, add_paste_to_meeting
- Sandbox: sandbox_create_work, sandbox_list_works, sandbox_list, sandbox_read, sandbox_create, sandbox_write, sandbox_append, sandbox_delete
- Orientation: get_room_structure, get_room_context
- Agent flow: get_pending_tasks, submit_proposal

## Proposed additions (design only; do not advertise as live tools)

| Priority | Proposed capability | Contract intent | Canonical dependency |
|---|---|---|---|
| P0 | sandbox_search | Search authorized Work artifacts with bounded results | Sandbox/Core |
| P0 | sandbox_stat | Metadata for one authorized relative path | Sandbox/Core |
| P0 | sandbox_read_range | Bounded line/byte range reads | Sandbox/Core |
| P0 | capability_discover | Return registered tool names, versions and JSON schemas | Actual MCP registry |
| P1 | sandbox_diff | Compare current artifact to supplied/readback revision | Sandbox/Core |
| P1 | sandbox_patch | Guarded patch with expected-before content/hash | Sandbox/Core; write policy |
| P1 | artifact_validate | Run registered, bounded validators only | Approved validator registry |
| P1 | artifact_verify | Readback/hash verification | Sandbox/Core |
| P2 | execution_submit | Submit typed WorkContext-bound request | Core -> W12/W13 |
| P2 | execution_status | Read authoritative run state | Core -> W12/W13 |
| P2 | execution_output_read | Read bounded, redacted logs | Core -> W12/W13 |
| P2 | evidence_collect | Correlate request/task/run IDs and evidence refs | Core + canonical execution |
| P3 | pc_source_list/read/search | Source access through authenticated PC bridge | W24 only |
| P3 | runtime_health | Report dependency readiness with explicit unknowns | MCP/Core/W12/W13/W24 |

## Shared response envelope

All new tools should return:
- request_id: non-empty correlation ID
- status: PASS | FAIL | BLOCKED | DENIED | TIMEOUT | NOT_FOUND | INVALID_REQUEST
- message: safe, concise explanation
- result: optional typed payload
- evidence_ref: optional authoritative evidence pointer
- contract_version: semantic version

## Security rules

1. Core :8000 remains the authorization and routing authority.
2. MCP validates shape and propagates identity; it must not invent authorization.
3. All file operations are relative to an authorized Work root.
4. Reject absolute paths, traversal, drive-qualified paths, UNC paths and alternate data streams.
5. No general-purpose shell/command-string tool.
6. Execution uses approved command IDs and the canonical W12/W13 contract.
7. PC source operations must use W24; do not create a second PC bridge.
8. Mutations require authorization, audit trail and readback verification.
9. Cap output sizes/timeouts and redact secrets.
10. An unavailable dependency is BLOCKED, never PASS.

## Integration gate

These contracts are not live until source registration, Core authorization routing, negative
security tests, and real MCP -> Core -> capability -> readback E2E are evidenced.
