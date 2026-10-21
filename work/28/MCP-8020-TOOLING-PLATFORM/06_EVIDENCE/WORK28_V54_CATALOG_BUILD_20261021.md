# Work 28 — v54 Catalog Build (2026-10-21)

## Scope delivered

Built the schema + registry + grouped handlers for the 54-tool planning set
defined in 03_ARCHITECTURE/WORK28_TOOL_CONTRACT_CATALOG_V1_54.md.

### 04_CODE

- mcp8020_catalog_v54.py — 54 ToolSpecs (name, group, status, description,
  inputSchema). Closed object schemas, additionalProperties false. Groups:
  room 10, sandbox 21, computer 6, browser 17.
- mcp8020_room_tools_v54.py — RoomProvider implementing all 10 ROOM tools
  with real in-memory meeting/task/proposal state.
- mcp8020_sandbox_tools_v54.py — SandboxProvider implementing 14 sandbox
  file tools with real filesystem operations under a provider root, with
  realpath-based path-escape and symlink protection, sha256 readback hashes,
  and an explicit confirm_delete policy guard.
- mcp8020_service_v54.py — protocol-agnostic tools/list + tools/call
  semantics: JSON-Schema validation (required/unknown/type/enum/bounds/
  pattern), fail-closed handler binding, stable error envelope
  (ok/data/error.code).
- mcp8020_server_v54.py — MCP adapter factory for :8020; lazy mcp import;
  transport/lifecycle stays with the existing HTTP host.

### Implementation status (honest split)

- IMPLEMENTED: 24 tools (room 10, sandbox file ops 14).
- NOT_IMPLEMENTED: 30 tools — sandbox execution/evidence chain (7) requires
  the approved Core/W12-W13 runtime; computer (6) and browser/OCR (17)
  require the W14 runtimes. These return a stable NOT_IMPLEMENTED error and
  are NOT faked.

### 05_TEST

- test_mcp8020_catalog_v54.py — catalog contract: 54 unique names, group
  counts, closed schemas, honest status split, export shape.
- test_mcp8020_service_v54.py — layers 1-4: invalid-input, binding,
  path-boundary negatives (traversal, absolute, symlink escape, cross-work),
  deterministic room and sandbox flows in temp sandboxes.
- test_mcp8020_server_v54.py — MCP adapter smoke test, skipped when the mcp
  package is absent.

## What this build does NOT prove

- No live MCP :8020 registration or transport test in CI (the mcp package is
  not installed in the CI contract runner); live tools/list and tools/call
  over the real adapter remain BLOCKED pending runtime verification.
- No execution, evidence, computer, or browser capability is claimed.
- CI status for this push is the only test evidence; no PASS may be recorded
  beyond what GitHub Actions actually executed.
