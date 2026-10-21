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


## Follow-up source audit — 2026-10-21 (Xu / GPT-6)

### Findings from reading the branch source (not runtime test evidence)

1. The unified registry exports exactly 21 tools (18 legacy + 3 read-only GitHub). It does **not** register the runtime adapter methods `execution_submit`, `execution_status`, or `execution_output_read`. Therefore the 21-tool MCP surface alone cannot yet provide the requested AI-run-test / read-output / repair loop.
2. `runtime_tools_v1.py` explicitly forwards only `RUN_TESTS` and `RUN_SCRIPT` operation labels to an injected authenticated Core transport; it intentionally does not spawn processes. This preserves the architecture boundary, but a trusted Core/Execution Host implementation and a registered MCP-facing contract are still required before execution can work end-to-end.
3. `mcp8020_unified_server_v1.py` imports the MCP SDK at module import time. The current Work 28 GitHub Actions workflow sets up Python 3.12 but does not install a declared dependency set before test discovery. If the workflow's discovered tests import this server module, the run may fail with missing `mcp`; this needs verification and a pinned dependency/lock or explicit install step.
4. The workflow command is `python -m unittest discover -s 05_TEST -v`, while the documented contract runner uses `python -m unittest discover -s 05_TEST -t . -v`. The intended canonical command should be consistent so imports and discovery behave deterministically.

### Required next implementation steps

- Keep the 21 legacy/GitHub registry inventory stable unless Vinh explicitly approves expanding it; add execution capabilities through a separately reviewed, bounded registry change or existing approved runtime tool surface.
- Wire execution only through authenticated Core → Execution Host/runtime; never execute arbitrary caller-provided shell strings and never place Core 8000 inside Sandbox.
- Require bounded approved profiles/operations, source hash binding, request/run IDs, timeout/resource limits, output size limits, and persisted stdout/stderr + exit code + test counters.
- Add contract tests for runtime tool registration, fail-closed provider wiring, async/sync handler behavior, argument type validation, and output status normalization.
- Align CI dependencies and the canonical test command, then capture actual workflow run ID, commit SHA, test count and artifact/readback evidence.

### Honest status

Source review only. No unit test, GitHub Actions run, live MCP `tools/list`, or MCP → Core → Execution Host → Sandbox → output-readback run was executed in this follow-up. No PASS claimed.
