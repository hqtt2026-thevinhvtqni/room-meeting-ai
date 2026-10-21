# Work 28 — Unified Tool Reconstruction Journal — 2026-10-21

## Vinh's directive
Vinh has no PC access now. Continue preparing implementation/documentation; do not run PC-dependent tests or invent results. Test when PC access returns.

## Scope
Reconstruct the 18 existing ROOM-HOP tools and include three existing read-only GitHub tools:
- github_repository
- github_read_file
- github_search_files

Expected unified registry: 21 tools. Existing GitHub write-capable adapter methods remain separate and are not added to this 21-tool surface.

## Files added / updated
- 04_CODE/mcp8020_unified_registry_v1.py — ordered registry, JSON schemas, boundary labels and exact-count validation. Argument schemas were aligned to the observed tool signatures for join/start meeting, add paste, sandbox create-work/list, pending tasks and proposal submission.
- 04_CODE/mcp8020_unified_server_v1.py — fail-closed server factory, injected providers, required/unknown argument checks and UTF-8 JSON output.
- 05_TEST/test_mcp8020_unified_registry_v1.py — static contract tests authored; NOT RUN per Vinh's instruction.
- 05_TEST/WORK28_PC_VALIDATION_PLAN_21_TOOLS.md — deferred PC validation plan.
- This journal records the work and remaining acceptance gates.

## Boundaries and honest status
- Factory does not start a second HTTP listener or modify MAIN SOURCE.
- Existing approved HTTP host must mount the factory only after PC validation.
- Core remains authorization authority; injected providers must enforce authorization.
- Caller-supplied identity fields are not authorization evidence.
- Missing provider handlers cause startup to fail closed.
- The new factory still requires real provider objects to be wired and must be validated against the installed MCP SDK; source preparation does not prove live MCP registration.
- Unit tests: NOT RUN.
- Live MCP tools/list: NOT RUN.
- Core authorization/security tests: NOT RUN.
- MCP -> Core -> provider -> readback E2E: BLOCKED until PC is available.
- Work 28 overall: ACTIVE, not accepted/released.
