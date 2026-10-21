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


## Addendum 2026-10-21 (post-#68): execution gateway layer

- mcp8020_execution_gateway_v54.py — ExecutionGateway binding all seven
  execution/evidence tool handlers to a CoreExecutionClient protocol
  (submit/status/result/cancel/artifact/evidence/handoff). Ships with
  BlockedExecutionClient as the fail-closed default. No concrete client is
  wired: PROPOSED_EXECUTION_TOOL_CONTRACT_V1 section 5 remains NO-GO until
  the authenticated Core route, canonical W12/W13 runtime, and OS isolation
  gate are evidenced. Catalog status for these tools stays NOT_IMPLEMENTED.
- 05_TEST/test_mcp8020_execution_gateway_v54.py — semantics tests against an
  explicit MockCoreExecutionClient (clearly labeled a fixture, not evidence):
  truthful PASS/FAIL, TIMEOUT terminal, zero-tests FAIL, DENIED before run
  creation, indistinguishable cross-work NOT_FOUND, evidence/handoff round
  trip. These prove the gateway cannot weaken statuses; they do NOT prove a
  live Core route exists.

## Remaining gates (unchanged)

1. Live MCP :8020 tools/list + tools/call against the real HTTP host — BLOCKED
   pending PC runtime verification.
2. Core :8000 route + W12/W13 runtime for the seven execution tools — NO-GO
   by design until preconditions in the execution contract are evidenced.
3. W14 runtimes for computer/browser groups — external dependency.
