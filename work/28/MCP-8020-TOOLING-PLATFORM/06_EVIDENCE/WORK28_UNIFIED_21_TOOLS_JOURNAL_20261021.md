# Work 28 — Unified MCP Tool Reconstruction Journal — 2026-10-21

## Vinh's directive
Vinh has no PC access now. Continue preparing implementation/documentation; do not run PC-dependent tests or invent results. Test when PC access returns.

## Scope
Reconstruct the 18 existing ROOM-HOP tools, three existing read-only GitHub tools, and nine explicitly requested extensions:
- github_repository
- github_read_file
- github_search_files

Expected unified registry: 30 unique tools (18 legacy + 3 read-only GitHub + 9 extensions). The legacy sandbox_write name is retained exactly once; its old input contract is preserved.

## Files added / updated
- 04_CODE/mcp8020_unified_registry_v1.py — ordered registry, JSON schemas, boundary labels and 30-tool exact-count validation. Argument schemas were aligned to the observed tool signatures for join/start meeting, add paste, sandbox create-work/list, pending tasks and proposal submission.
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

1. At the time of this audit, the unified registry exported 21 tools and did not register the runtime adapter methods. Vinh then explicitly directed Xu to add the requested tools; the registry has now been expanded to 30 names, including `execution_submit`, `execution_status`, and `execution_output_read`.
2. `runtime_tools_v1.py` explicitly forwards only `RUN_TESTS` and `RUN_SCRIPT` operation labels to an injected authenticated Core transport; it intentionally does not spawn processes. This preserves the architecture boundary, but a trusted Core/Execution Host implementation and a registered MCP-facing contract are still required before execution can work end-to-end.
3. `mcp8020_unified_server_v1.py` imports the MCP SDK at module import time. The current Work 28 GitHub Actions workflow sets up Python 3.12 but does not install a declared dependency set before test discovery. If the workflow's discovered tests import this server module, the run may fail with missing `mcp`; this needs verification and a pinned dependency/lock or explicit install step.
4. The workflow command is `python -m unittest discover -s 05_TEST -v`, while the documented contract runner uses `python -m unittest discover -s 05_TEST -t . -v`. The intended canonical command should be consistent so imports and discovery behave deterministically.

### Required next implementation steps

- Preserve the 18 legacy operations and three existing GitHub read tools; add the nine bounded extensions now explicitly requested by Vinh.
- Wire execution only through authenticated Core → Execution Host/runtime; never execute arbitrary caller-provided shell strings and never place Core 8000 inside Sandbox.
- Require bounded approved profiles/operations, source hash binding, request/run IDs, timeout/resource limits, output size limits, and persisted stdout/stderr + exit code + test counters.
- Expand contract tests for the 30-name registry and new runtime/Sandbox/GitHub tool schemas. Still add server/provider integration tests for fail-closed wiring, async/sync handler behavior, argument type validation, and output status normalization.
- Align CI dependencies and the canonical test command, then capture actual workflow run ID, commit SHA, test count and artifact/readback evidence.

### Honest status

Source review only. No unit test, GitHub Actions run, live MCP `tools/list`, or MCP → Core → Execution Host → Sandbox → output-readback run was executed in the source-only implementation phase. No PASS claimed.


## Implementation update — 2026-10-21 (Xu / GPT-6)

### Added to the unified registry

- Preserved all 21 existing names and appended nine unique names: `execution_submit`, `execution_status`, `execution_output_read`, `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, `github_create_branch`, `github_create_file`, and `github_update_file`.
- Unified registry now declares 30 unique tool names, with an exact-count guard and bounded input schemas.
- Updated the unified server factory to require injected `runtime` and `sandbox_extensions` providers. The new Sandbox extension boundary is deliberately separate from the legacy `sandbox` provider, avoiding a requirement that one adapter implement two incompatible contracts. The factory still starts no listener; it must be mounted through the already-approved host only after validation.
- Updated the registry contract test and PC validation plan to expect 30 tools.
- Runtime submission accepts only the declared `RUN_TESTS` / `RUN_SCRIPT` operation labels, a Work ID, source SHA-256, profile ID, and request ID; no arbitrary shell command field is exposed.
- Sandbox range reads are capped at 65,536 bytes; runtime output reads at 16,384 bytes; GitHub updates require an expected 40-character blob SHA and a non-default branch.

### Remaining integration boundary / status

- These are source/contract changes committed to the Work 28 branch, not proof that the live MCP host exposes 30 tools.
- The injected Runtime provider must route through authenticated Core to the Execution Host; Core must remain outside Sandbox. Actual execution, timeout/resource enforcement, persisted output/exit-code/test-counter evidence, and output readback still require trusted backend wiring and PC E2E validation.
- Legacy Sandbox, Sandbox extension, Runtime, and GitHub providers must expose all mapped methods and enforce authorization/path/branch policy. Startup is intended to fail closed when a handler is absent.
- Registry contract tests have been authored/updated but **NOT RUN**. Live `tools/list`, GitHub write tests, Runtime execution, and full E2E remain **NOT RUN / BLOCKED** pending PC validation.
- Work 28 remains ACTIVE; no PASS or release claim.
