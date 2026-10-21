# Work 28 — MCP 8020: Inventory and Reconstruction Baseline

- Date: 2026-10-21
- Scope: Recreate the 18 tools exposed by the existing MCP 8020 server in Work 28.
- Sandbox status: unavailable during this session (Sandbox MCP calls failed internally).
- GitHub repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Target branch: work/28-mcp-tooling-platform
- Status: BLOCKED for implementation verification; this file records the source-of-truth inventory, not a claim that the tools have been rebuilt or registered.

## Exact 18-tool inventory reported for MCP 8020

1. list_meetings
2. get_meeting
3. get_transcript
4. join_meeting
5. start_meeting
6. add_paste_to_meeting
7. sandbox_create_work
8. sandbox_list_works
9. sandbox_list
10. get_room_structure
11. get_room_context
12. sandbox_read
13. sandbox_create
14. sandbox_write
15. sandbox_append
16. sandbox_delete
17. get_pending_tasks
18. submit_proposal

## Required reconstruction sequence

1. Inspect the current branch tree and recover the existing server registration, schemas, handlers, and service dependencies before writing replacement code.
2. Preserve these 18 public tool names and argument/result contracts; do not replace working tools with mock implementations.
3. Recreate code and contract tests under Work 28, documenting dependencies and errors.
4. Run unit/contract tests and record command output and hashes as evidence.
5. Verify live `tools/list` on MCP 8020 returns exactly the expected 18 names, then call representative tools end-to-end through MCP → Core/Workspace.
6. Report DONE only when implementation, tests, and live registration are evidenced. Otherwise retain BLOCKED with the exact blocker.

## Safety and scope constraints

- Do not edit the production MCP 8020 server or replace its current tools as part of this reconstruction task.
- Do not report PASS based on source inspection alone.
- Do not invent behavior where the original implementation/contracts cannot be recovered.
