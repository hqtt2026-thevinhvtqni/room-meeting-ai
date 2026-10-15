# Nu — Source transfer status
Date: 2026-10-15 (+07)
Work: 28 / MCP-8020-TOOLING-PLATFORM
Order: `KA_NU_SANDBOX_FIRST_SOURCE_TRANSFER_ORDER_20261015.md`
Status: **BLOCKED_SOURCE_ACCESS**

## Verification performed
- Read the Sandbox-first source intake order through MCP 8020.
- Listed Work 28 after the order was recorded.
- `MCP-8020-TOOLING-PLATFORM/04_CODE/source_snapshot/` is **not present**.
- The only current `04_CODE` implementation artifact is `tool_contracts.py`, which the order explicitly classifies as contract code, not the real MCP/Core/Sandbox implementation.
- No source snapshot manifest, archive, per-file hash manifest, or `SOURCE_TRANSFER_STARTED` / `SOURCE_SNAPSHOT_IMPORTED` evidence exists.

## Exact access gap
The current Nu execution context has ROOM-HOP Sandbox file operations and read-only evidence already stored in Work 28, but no authorized read-only channel that exposes the actual PC working-tree file contents from:
- `D:\ROOM-HOP-CLEAN\room-meeting-ai\room_hop_mcp\mcp_http_main.py`
- `room_hop_mcp\sandbox_service.py`
- `room_hop_mcp\sandbox_identity.py`
- remaining imported `room_hop_mcp` dependencies and relevant Core authorization modules/tests.

The previously reported PC metadata (listener PID, HEAD and selected SHA-256 values) is provenance metadata only; it is not a source snapshot and cannot be used to reconstruct the files. The public GitHub `main` source was already shown not to match the connected 18-operation PC surface, so it is not substituted.

## Smallest required unblock
Provide one authorized read-only source transfer into the Sandbox containing the relevant existing source tree (or a source archive), excluding secrets/runtime state, plus:
1. source origin and collection timestamp;
2. branch/HEAD and dirty/untracked status;
3. included/excluded relative paths;
4. per-file SHA-256 and archive SHA-256.

After that transfer is available, Nu can place the verified snapshot under `04_CODE/source_snapshot/`, read it back, verify hashes and return `SOURCE_SNAPSHOT_IMPORTED` before any implementation work.

## Guardrail decision
No source was fabricated, copied from an unrelated revision, written to the PC, or treated as imported. Work 28 remains `ACTIVE / NOT LOCKED`; implementation, independent review and final bundle remain pending source intake.
