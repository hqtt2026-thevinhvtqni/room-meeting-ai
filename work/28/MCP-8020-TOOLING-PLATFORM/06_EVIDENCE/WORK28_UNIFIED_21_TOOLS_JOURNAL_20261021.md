# Work 28 — Unified Tool Reconstruction Journal — 2026-10-21

## Vinh's directive
Vinh has no PC access now. Continue preparing implementation/documentation; do not run PC-dependent tests or invent results. Test when PC access returns.

## Scope
Reconstruct the 18 existing ROOM-HOP tools and include three existing read-only GitHub tools:
- github_repository
- github_read_file
- github_search_files

Expected unified registry: 21 tools. Existing GitHub write-capable adapter methods remain separate and are not added to this 21-tool surface.

## Files added
- 04_CODE/mcp8020_unified_registry_v1.py — ordered registry, input schemas, boundary labels, uniqueness/count validation.
- 04_CODE/mcp8020_unified_server_v1.py — fail-closed server factory, injected providers, argument checks, UTF-8 JSON output.
- 05_TEST/WORK28_PC_VALIDATION_PLAN_21_TOOLS.md — deferred PC validation plan.

## Boundaries
- Factory does not start a second HTTP listener or modify MAIN SOURCE.
- Existing approved HTTP host must mount the factory only after PC validation.
- Core remains authorization authority; injected providers must enforce authorization.
- Caller-supplied identity fields are not authorization evidence.
- Missing provider handlers cause startup to fail closed.
- Registry/source prepared does not prove live MCP registration.

## Status
- Source prepared: DONE (authoring only).
- Unit tests: NOT RUN.
- Live MCP tools/list: NOT RUN.
- Core authorization/security tests: NOT RUN.
- MCP -> Core -> provider -> readback E2E: BLOCKED until PC is available.
- Work 28 overall: ACTIVE, not accepted/released.
