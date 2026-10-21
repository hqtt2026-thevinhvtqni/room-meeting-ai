# Work 28 — PC Validation Plan for Unified 31-Tool MCP Surface

Status: NOT RUN — PC unavailable. Do not report PASS until the PC checks below are executed.
Scope: 18 existing ROOM-HOP operations + 3 read-only GitHub operations + 10 bounded runtime/Sandbox/GitHub extensions.

## Expected inventory
- Legacy tools: 18 (meetings, sandbox, room orientation, tasks/proposal).
- Existing GitHub tools: github_repository, github_read_file, github_search_files.
- Runtime tools: execution_submit, execution_status, execution_output_read.
- Additional Sandbox tools: sandbox_search, sandbox_stat, sandbox_read_range, sandbox_write_verified. Existing sandbox_write remains in the legacy set to avoid a duplicate name; inject its new read/search adapter separately as `sandbox_extensions`.
- GitHub write tools: github_create_branch, github_create_file, github_update_file.
- Expected unified registry: 31 unique names (18 + 3 + 10).

## PC checks when available
1. Run unit tests for registry/provider contracts.
2. Verify installed MCP SDK compatibility with Server, Tool and TextContent usage.
3. Inject distinct `sandbox` (legacy) and `sandbox_extensions` (new bounded search/stat/range) providers, plus `runtime`, `core`, `proposals`, and `github`; verify all mapped methods exist and missing handlers fail startup closed.
4. Mount through the existing approved MCP HTTP entrypoint; do not start a parallel listener.
5. Query tools/list and compare exact 31 names/count/schemas, including the ten extensions.
6. Exercise GitHub read/write calls on a disposable non-default test branch; verify expected-blob-SHA protection for updates.
7. Exercise legacy operations through Core/Sandbox/Proposal providers and all new runtime/Sandbox/GitHub providers.
8. Run negative security tests: unknown tool, missing/extra fields, missing provider, path traversal, spoofed identity and unauthenticated calls.
9. Verify Core remains the authorization authority and caller identity_id is never trusted as proof.
10. Verify runtime operations route only through authenticated Core to Execution Host; no arbitrary shell input and no Core inside Sandbox.
11. Record request/run IDs, inventory, test output, commit SHA, bounded stdout/stderr/exit code, and readback evidence.

## Acceptance gates
- G0: source/contract prepared.
- G1: PC unit tests PASS.
- G2: live tools/list exact 31-name match.
- G3: Core authorization and negative security tests PASS.
- G4: MCP -> Core -> provider -> readback E2E PASS.

Current honest status: G0 prepared; G1-G4 NOT RUN/BLOCKED until PC is available.
