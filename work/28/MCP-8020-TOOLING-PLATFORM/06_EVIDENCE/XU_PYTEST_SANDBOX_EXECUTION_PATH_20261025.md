# Work 28 — Pytest on Sandbox: execution-path investigation
**Date:** 2026-10-25 (UTC+7)  
**Owner:** Xu — AI-01 GPT CEO / Quân sư LAB  
**Work:** 28 · MCP-8020-TOOLING-PLATFORM  
**Status:** IN PROGRESS / EXECUTION BLOCKED — NOT PASS

## Goal
Run the real Work 28 pytest suite inside the authorized Sandbox runtime through MCP, capture real exit code/stdout/stderr, repair failures, rerun, and preserve evidence. No PC-only test run may be represented as a Sandbox run.

## Evidence inspected through MCP 8030
- `05_TEST/test_tool_contracts.py` imports `04_CODE.tool_contracts` using `importlib.import_module`.
- The canonical code and test directories are siblings under `MCP-8020-TOOLING-PLATFORM/`.
- Running pytest from the repository root against the nested test path previously failed collection with `ModuleNotFoundError: No module named '04_CODE'`. This is consistent with an incorrect working directory/import root; it does not establish that the test itself is failing.
- The documented command in `02_EXTENSION/DECISION_AI_RUN_PYTHON_VIA_MCP.md` requires governed Python execution through MCP → Core :8000 authorization → approved canonical runtime, with run_id, real exit code, stdout/stderr, bounded resources, and evidence.
- The currently available MCP 8030 tool surface in this session exposes Sandbox file operations but no Python/pytest execution action. Therefore this session cannot honestly claim that pytest has run inside Sandbox.

## Source reconciliation
A targeted comparison found that Sandbox `04_CODE/tool_contracts.py` lacked three enum members present on the GitHub branch:
- `SandboxOperation.READ_RANGE`
- `SandboxOperation.SEARCH`
- `SandboxOperation.STAT`

Sandbox was updated from the exact GitHub branch content and read back. **PASS — exact content equality** for this file after synchronization. GitHub blob SHA: `3dc1a4c3939c4f57ec4b1d7e1391ece1fb68f52e`.

## Canonical working directory and first test command
The runner must set its working directory to:
`MCP-8020-TOOLING-PLATFORM/`

Then run:
```bash
python -m pytest -q 05_TEST
```

Contract-suite alternative:
```bash
python -m unittest discover -s 05_TEST -t . -v
```

Do not run these from repository root with a nested `05_TEST` path and then misclassify the resulting import-path error as a test assertion failure.

## Required implementation task
Expose a governed `python_test` / `python_run` action on the existing canonical execution path (W12/W13/Work 27 only where genuinely integrated). Do not add an unrestricted shell, do not create a parallel execution host, and do not bypass Core :8000. The tool must:
1. Bind identity, Work ID 28, approved relative test target and request/run IDs server-side.
2. Use the canonical Work 28 directory as cwd; reject traversal and out-of-scope paths.
3. Run approved pytest/unittest entry points in an isolated, bounded runtime with timeout and output limits; network/package install/host access denied by default.
4. Return real run_id, terminal status, exit code, stdout/stderr, source revision/hash, and test summary.
5. Prove negative cases: unauthorized Work, path traversal, timeout, output cap, and a deliberately failing test.
6. Permit the AI to edit a Sandbox file, rerun through MCP, inspect output, and write correlated evidence without manual PC intervention.

## Acceptance gates
- **G0 — Import root:** the canonical command imports `04_CODE.tool_contracts` from the Work 28 platform root.
- **G1 — Actual Sandbox execution:** smoke test returns real run_id + exit code + stdout/stderr through MCP and approved runtime.
- **G2 — Test suite:** pytest runs from Sandbox; report pass/fail/error/skip counts and exit code. No silent skips or mocked execution evidence.
- **G3 — Security:** unauthorized requests/path traversal denied; timeout and output limits proven.
- **G4 — Repeatability:** fix a failing test/code path in Sandbox and rerun without PC intervention; read back source hash and evidence.
- **G5 — Release:** only after all required gates have evidence. Until then Work 28 stays ACTIVE / NOT RELEASED.

## Current truthful status
- **PASS:** Sandbox↔GitHub content equality for `04_CODE/tool_contracts.py` after the targeted sync.
- **BLOCKED:** actual pytest execution inside Sandbox because an authorized Python execution tool is not exposed in the current MCP 8030 tool surface.
- **NOT CLAIMED:** pytest suite PASS, runtime isolation PASS, or end-to-end PASS.

## Next action
Continue wiring `python_test` through the existing authorized execution architecture. Once that action is callable, run the canonical command, fix collection/import failures based on real output, and record the full test summary and exit code.

## Follow-up implementation (2026-10-25)
- **DONE — Import-path hardening:** updated `05_TEST/test_tool_contracts.py` to add the canonical platform root (`Path(__file__).resolve().parents[1]`) to `sys.path` before importing `04_CODE.tool_contracts`. This removes dependence on the caller's current working directory for this test's import.
- **PASS — Sync/readback:** exact updated test content was read back from both Sandbox and GitHub. GitHub test blob SHA: `af20321adfd2eace85951b5457911afdb59ab113`.
- **Still BLOCKED:** no authorized Python execution action is exposed by the current MCP 8030 tool surface, so neither the patched test nor the full pytest suite has been executed in Sandbox. The import-path fix is not a test PASS.
