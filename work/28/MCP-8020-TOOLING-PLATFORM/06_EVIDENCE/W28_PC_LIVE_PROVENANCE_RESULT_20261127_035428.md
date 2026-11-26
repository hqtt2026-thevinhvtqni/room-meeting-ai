# W28 PC Live Provenance Result — 2026-11-27 03:54:28

**Collector:** `PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.ps1`  
**Evidence folder:** `C:\Users\Admin\AppData\Local\Temp\W28_LIVE_PROVENANCE_20261127_035428`  
**Source:** Operator-provided PowerShell output in the W28 conversation.  
**Scope:** Read-only local Git/listener/source-hash inspection and MCP initialize/tools/list. No tools/call and no 8020 probe.

## 1. Local checkout state

- Repository: `D:\ROOM-HOP-CLEAN\room-meeting-ai`
- Branch: `main`
- HEAD: `13c18dd9954f5c01d4c42990cd261fb6c68c5795`
- Working tree: **DIRTY**.
- Collector output includes numerous modified, deleted and untracked paths, including a large number of unrelated files and W28 evidence paths.
- Do not clean, reset, checkout, stash, overwrite or otherwise mutate this working tree as part of W28. It is not the canonical Work28 branch.

## 2. Listener observations

| Port | PID | Process | Module | Module candidate SHA-256 |
|---|---:|---|---|---|
| 8000 | 8548 | python.exe | `room_hop_mcp.http_main` | `8cebcf77f4e13655a5769e2269f64f698f7ac40f79f74def88784025c1d816d2` |
| 8030 | 7664 | python.exe | `room_hop_mcp.mcp_build_http_main` | `15342b4159a8cd4daf01f9d03482b92d9657083cafaabc073b51d5b80ba3b1d1` |
| 8031 | 14428 | python.exe | `execution_host.server` | `976631b2b32f19d6149e6f827844733b465e6c21743aeff63bf9064f9994ea80` |

- No listener on port 8001 was present in the collector output.
- These are process/listener and candidate module-file observations. They do not prove that the running process loaded the current on-disk bytes or establish a secure mapping from MCP endpoint to a specific upload service.

## 3. MCP endpoint observation

- Endpoint: `https://admin-pc.tail7d6101.ts.net/build/mcp`
- Result: `PASS_READONLY_PROTOCOL_RESPONSE`
- Protocol version: `2025-03-26`
- Tool count: 17
- Tools included Sandbox file operations (`sandbox_read`, `sandbox_read_probe`, `sandbox_list`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`, `sandbox_create_work`, `sandbox_list_works`) and meeting/context tools.
- No host process inspection, shell/command execution, ACL inspection, mount inspection or arbitrary runtime diagnostic tool was listed.
- The collector did not invoke `tools/call`; this result is initialize/tools/list protocol evidence only.

## 4. Selected local source hashes

- `room_hop_mcp/adapter/server.py`: `b45bd5f3fd626813d1a00d5c11aa0f64fc087ba4fc277871495e45bbb7862149`
- `room_hop_mcp/adapter/http_server.py`: `498b95f9da162e5833d433476464ec13e2cd2f455737642c4dc56b3a1fea8c49`
- `room_hop_mcp/__main__.py`: `473cc7c64aa7b5342e357d8089466d0dad385c29ecc6ff8ac924830c3abe6350`
- `execution_host/server.py`: `976631b2b32f19d6149e6f827844733b465e6c21743aeff63bf9064f9994ea80`
- `core/execution_authority/http_server.py`, `core/execution_authority/authority.py`, `work/28/.../mcp8020_unified_registry_v1.py`, and `mcp8020_unified_server_v1.py`: NOT_FOUND in the collector's selected local paths.

These hashes describe the selected local worktree files only. They are not proof of deployed or in-memory source identity.

## 5. Security and acceptance interpretation

- Current listener provenance was captured successfully.
- The observed MCP 8030 interface still provides no approved host runtime inspection path.
- The collector did not identify an upload-service process or inspect the actual upload Sandbox/staging ACLs, Windows token privileges, handle identity, reparse-point behavior or no-replace publication.
- No upload, readback, recovery, cleanup or runtime E2E test was performed.
- The result does not remediate or close the F01 parent-swap vulnerability and does not prove F02/F03/F04.

## 6. Disposition

**Evidence status:** CURRENT PC LISTENER / MCP PROTOCOL PROVENANCE CAPTURED; HOST FILESYSTEM SECURITY NOT OBSERVED.  
**F01:** BLOCKED.  
**F02:** PARTIAL / NOT VERIFIED.  
**F03–F04:** BLOCKED.  
**PR #85:** DRAFT / UNMERGED.  
**Execution Gate:** CLOSED.  
**Work28:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

No local PC repository mutation was requested or performed by this evidence collection.
