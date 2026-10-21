# Work 28 — PC Validation Plan for Unified 21-Tool MCP Surface

Status: NOT RUN — PC unavailable. Do not report PASS until the PC checks below are executed.
Scope: 18 existing ROOM-HOP operations + 3 read-only GitHub operations.

## Expected inventory
- Legacy tools: 18 (meetings, sandbox, room orientation, tasks/proposal).
- GitHub tools: github_repository, github_read_file, github_search_files.
- Expected unified registry: 21 unique names.

## PC checks when available
1. Run unit tests for registry/provider contracts.
2. Verify installed MCP SDK compatibility with Server, Tool and TextContent usage.
3. Verify all injected providers expose mapped methods; missing method must fail startup closed.
4. Mount through the existing approved MCP HTTP entrypoint; do not start a parallel listener.
5. Query tools/list and compare exact names/count/schemas.
6. Exercise GitHub read-only calls against a test repository/branch.
7. Exercise legacy operations through Core/Sandbox/Proposal providers.
8. Run negative security tests: unknown tool, missing/extra fields, missing provider, path traversal, spoofed identity and unauthenticated calls.
9. Verify Core remains the authorization authority and caller identity_id is never trusted as proof.
10. Record request IDs, inventory, test output, commit SHA and readback evidence.

## Acceptance gates
- G0: source/contract prepared.
- G1: PC unit tests PASS.
- G2: live tools/list exact match.
- G3: Core authorization and negative security tests PASS.
- G4: MCP -> Core -> provider -> readback E2E PASS.

Current honest status: G0 prepared; G1-G4 NOT RUN/BLOCKED until PC is available.
