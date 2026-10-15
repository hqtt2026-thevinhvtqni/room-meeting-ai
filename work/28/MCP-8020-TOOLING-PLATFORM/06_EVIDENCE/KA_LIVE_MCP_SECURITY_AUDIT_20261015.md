# Work 28 — Live MCP 8020 Security Audit

Date: 2026-10-15
Reviewer: Ka / CSA
Status: PARTIAL AUDIT — SECURITY BLOCKED; E2E NOT VERIFIED; RELEASE NO-GO

## Evidence supplied from PC
- Existing `integration/mcp_public_tools_probe.py` against `https://admin-pc.tail7d6101.ts.net/meeting/mcp` returned `INITIALIZE: PASS`, `LIST_TOOLS: PASS`, `TOOL_COUNT: 18`.
- Live tool names: `list_meetings`, `get_meeting`, `get_transcript`, `join_meeting`, `start_meeting`, `add_paste_to_meeting`, `sandbox_create_work`, `sandbox_list_works`, `sandbox_list`, `get_room_structure`, `get_room_context`, `sandbox_read`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`, `get_pending_tasks`, `submit_proposal`.
- Source `room_hop_mcp/sandbox_identity.py` explicitly states that identity validity is not authentication and `identity_id` is self-declared until transport authentication is enabled. `check_sandbox_identity` compares the provided ID against `agents/*.yaml`.
- The provided `mcp_http_main.py` excerpts show `sandbox_list` and `sandbox_read` directly invoking `SandboxService`; excerpts for create/write/append/delete show the same pattern. The excerpts do not establish caller authentication or Core-mediated authorization before file operations.
- `sandbox_service.py` `_work_root()` resolves the Work root and checks it is inside `sandbox_root`; `_path()` resolves the target and checks it is inside the Work root. This is positive containment logic, but not a complete proof against symlink/race/path edge cases.
- The supplied excerpts show `list()` using `root.rglob("*")` and `read()` using `target.read_text(encoding="utf-8")`; no output-size bound is visible in these excerpts.

## Findings
1. Live MCP tool inventory: PASS for the 18 tools listed above, based on the actual `tools/list` probe output supplied by Vinh.
2. Identity authentication: BLOCKED. Registry membership is not proof of the requester's identity; caller-supplied `identity_id` is not authentication.
3. Authorization boundary: BLOCKED / NOT PROVEN. Current excerpts do not prove each sandbox operation is authenticated and authorized by Core before accessing files. Do not claim a bypass as fully demonstrated without tracing all middleware/call paths, but do not accept the authorization contract as PASS.
4. Path containment: PARTIAL POSITIVE EVIDENCE. `_work_root()` and `_path()` enforce resolved-path containment. Security test coverage for traversal, symlinks, drive/UNC/ADS paths, and race cases remains unverified.
5. Bounded reads/listing: NOT PROVEN from supplied excerpts.

## Next required evidence
- Trace the full active request path and all decorators/middleware for all six sandbox tools; determine whether any transport authentication exists outside the shown functions and whether Core authorization is invoked.
- Inspect full `SandboxService` bodies for create/write/append/delete, root initialization, symlink behavior, and size limits.
- Add/run safe, isolated regression tests for unknown/self-declared identity, unauthorized read/write/delete, `..` traversal, absolute/drive/UNC paths, symlink escape, transcript append-only, and bounded read/list output.
- Capture test command, exit code, and output. Do not change/restart the live listener or mutate registry without explicit authorization.

## Release decision
Work 28 remains ACTIVE / NOT LOCKED. Live MCP inventory is verified; security contract and E2E are not verified. No overall PASS; release remains NO-GO until source trace, tests, and end-to-end evidence are complete.