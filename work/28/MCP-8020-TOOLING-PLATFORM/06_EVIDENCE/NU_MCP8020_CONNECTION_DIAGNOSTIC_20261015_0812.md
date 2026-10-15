# Nu — MCP 8020 connection/source-transfer diagnostic
Date: 2026-10-15 (+07)
Work: 28 / MCP-8020-TOOLING-PLATFORM
Status: **MCP_CONNECTED / SOURCE_TRANSFER_CAPABILITY_MISSING**

## Connection checks
- ROOM-HOP MCP server responded successfully to tool discovery.
- `get_room_context` returned `status=ok`, `service=room-hop`, `version=1.0`.
- `get_room_structure` returned the MAIN_SOURCE tree, including `room_hop_mcp/`, `core/`, `integration/` and other source paths.
- `sandbox_list_works` returned all 37 Works, including Work 28 with `manifest_exists=true`.
- `sandbox_list` returned the complete Work 28 tree.
- Existing `sandbox_read` and previous `sandbox_write`/`sandbox_append` operations succeeded.

Conclusion: MCP 8020 and the Work 28 Sandbox connection are operational.

## Boundary/capability finding
`get_room_context` explicitly reports:
- MAIN SOURCE is read-only for AI build operations.
- Sandbox is the read/write AI BUILD ZONE.
- MCP :8020 is the AI/agent boundary.
- AI cannot merge, commit or push.

The exposed room-hop tool list contains Sandbox file operations (`sandbox_list`, `sandbox_read`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`) and orientation/meeting operations, but no authorized operation for:
- reading arbitrary MAIN_SOURCE file contents into an agent response;
- PC working-tree source export/collection;
- source-tree copy/import into a Work;
- archive upload/import;
- source manifest/hash generation over the PC tree;
- PC-to-Sandbox bridge transfer.

`sandbox_write` accepts a text `content` string for one Work-relative path; it is not a source-tree transfer or archive-import capability. `get_room_structure` exposes paths only and is not source-content readback.

## Root cause
**Root cause is a capability gap at the MCP 8020 boundary, not a connectivity failure:** the current connected server can inspect and write Work Sandbox artifacts, but it does not expose an authorized PC/Main-Source → Work 28 source-transfer operation. The available connection therefore cannot produce the required provenance-traceable `04_CODE/source_snapshot/` from the actual PC working tree.

The MAIN_SOURCE tree visibly contains source paths, but the current API does not provide their contents through a permitted read/copy route. Replacing it with public GitHub `main` would violate the Sandbox-first order because the PC working tree is known to differ.

## Required unblock
Add or authorize one narrowly scoped read-only transfer route, preferably:
1. PC-side collector selects an allowlisted source tree and excludes secrets/runtime state;
2. collector creates a manifest with origin, timestamp, HEAD, dirty/untracked state, included/excluded paths, per-file SHA-256 and archive SHA-256;
3. collector transfers the archive/manifest into Sandbox;
4. Nu verifies readback and returns `SOURCE_SNAPSHOT_IMPORTED`;
5. only then does E2E-Automatic start.

No listener restart, PC write, registry mutation, source fabrication or alternate-revision substitution was performed.
