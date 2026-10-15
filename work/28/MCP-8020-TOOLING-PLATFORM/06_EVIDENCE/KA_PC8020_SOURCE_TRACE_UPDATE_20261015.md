# Work 28 — PC 8020 Source Trace Update
Date: 2026-10-15
Owner: Ka / CSA
Authority: Vinh
Status: SOURCE TRACE PARTIAL / P0 IMPLEMENTATION BLOCKED ON FULL AUTHORIZATION PATH

## PC evidence received
- Listener: 127.0.0.1:8020, PID 6748.
- Process command: Python 3.12 `-m room_hop_mcp.mcp_http_main`.
- Repository: D:/ROOM-HOP-CLEAN/room-meeting-ai
- Git HEAD: d7c90d9d31062d389810808e43dfdd19d7711b75, branch main.
- Working tree is heavily modified/untracked; Git HEAD alone does not identify running source.
- SHA256 room_hop_mcp/mcp_http_main.py: 8A720CE9C3DD9981964D681130BCCB9EB5B1C31A31CB1E3B02121A5EB9644A64
- SHA256 room_hop_mcp/sandbox_service.py: 575AE1EC354DC9B718E12D2A0B6C491437E95742FAA264922174CEF2FA602485
- SHA256 room_hop_mcp/sandbox_identity.py: 70485F86B216A161C13B75610092E0C1FF8635CDBA4DDEE65B39078CF17173B3

## Source-level findings from PC Select-String output
The running entrypoint source imports `SandboxService` and `check_sandbox_identity`, creates `sandbox = SandboxService(SANDBOX_ROOT)`, and uses FastMCP registration via `@mcp.tool`.
Observed registrations in the source excerpt:
- Meetings: list_meetings, get_meeting, get_transcript, join_meeting, start_meeting, add_paste_to_meeting.
- Sandbox: sandbox_create_work, sandbox_list_works, sandbox_list, sandbox_read, sandbox_create, sandbox_write, sandbox_append, sandbox_delete.
- Orientation: get_room_structure, get_room_context.
- Agent flow: get_pending_tasks, submit_proposal.
This yields 18 registrations in the excerpt, but does NOT prove the live endpoint's tools/list response.
The SandboxService excerpt shows create_work, _work_root, _path, list_works, list, read, write, append, create, delete. No search/stat/read_range equivalent appeared in the excerpt.
No capability_discover registration appeared in the MCP entrypoint excerpt.
The source output does not show the complete authorization flow, Core :8000 route, or all method bodies; those remain unverified.

## P0 gap assessment
1. sandbox_search — not observed in the provided SandboxService method inventory; likely missing, pending full-source check.
2. sandbox_stat — not observed; likely missing, pending full-source check.
3. sandbox_read_range — not observed; likely missing, pending full-source check.
4. capability_discover — not observed among the listed @mcp.tool registrations; live tools/list still unverified.

## Security and integration constraints
- Do not modify or restart PID 6748 based only on this inventory.
- Worktree is not clean; no reset/checkout/overwrite.
- Before coding P0, inspect the full path authorization/identity enforcement for sandbox_read/list and Core :8000; the excerpt alone is insufficient to assert Core is authoritative.
- Any new file capability must reuse SandboxService._path/_work_root or prove equivalent confinement, be read-only, output-bounded, deny traversal/absolute/drive/UNC/ADS paths, and have negative tests.
- capability_discover must derive from actual registered MCP tool definitions/schema, not a static list. Need live MCP tools/list response to compare.
- Do not add execution/shell/Python capabilities.

## Tests and status
- Tests run by Ka in this turn: 0 (no local PC test runner available in this execution context).
- Live endpoint tools/list response: NOT PROVIDED.
- MCP -> Core -> authorized capability -> readback E2E: BLOCKED / NOT VERIFIED.
- Work 28: ACTIVE / NOT LOCKED.
- Release: NO-GO until security, registration, and live E2E evidence pass.

## Single actionable next step for PC
Provide full, read-only source for:
- room_hop_mcp/sandbox_service.py
- room_hop_mcp/sandbox_identity.py
- room_hop_mcp/mcp_http_main.py sections for sandbox_read/list and all MCP tool registrations
- the actual Core :8000 authorization route or service those tools are required to call
Also collect the raw successful JSON-RPC response to tools/list from 127.0.0.1:8020 using the same running process. The existing mcp_tools_list.json files are requests only, not responses.
