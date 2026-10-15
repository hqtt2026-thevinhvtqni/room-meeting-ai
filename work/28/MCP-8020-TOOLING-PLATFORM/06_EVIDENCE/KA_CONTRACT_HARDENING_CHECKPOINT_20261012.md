# KA — WORK 28 CONTRACT HARDENING CHECKPOINT
Date: 2026-10-12 (+07)
State: SOURCE WRITTEN / READBACK VERIFIED / TEST EXECUTION BLOCKED

## Changes made in Work Sandbox
- `04_CODE/tool_contracts.py` upgraded to contract version 1.1.0.
- Added QUEUED, RUNNING and CANCELLED lifecycle statuses.
- Added OperationKind and strict evidence requirements for execution PASS: run_id, exit_code=0, evidence_ref, source SHA-256 and trusted non-empty test summary.
- Added server-boundary ID generators for request_id/run_id and strict ASCII correlation-ID validation.
- Added SHA-256 validation.
- Tightened lexical Work path checks for normalization/confusables, control/format characters, DEL/C1, traversal/absolute/drive/UNC/ADS, option-like paths, Windows reserved names/trailing dot-space, expansion/wildcards and protected metadata components.
- Added safe exception status mapping without exposing exception text.
- Expanded regression tests and added package marker files so the documented unittest discovery command can run without a manually supplied PYTHONPATH.

## Persistence evidence
- MCP Sandbox write returned status=ok for the source and test files.
- Subsequent sandbox_read succeeded for `tool_contracts.py`, `test_tool_contracts.py` and the WP0 source map.
- This proves persistence/readback only.

## Not claimed
- No Python command was run against this Work Sandbox source in the canonical W12/W13 runtime.
- No G3 PASS, no live MCP execution tool, no authorization/isolation test, and no E2E PASS is claimed.
- The path validator is lexical defense in depth; filesystem containment, no-follow/reparse-point handling and OS isolation remain mandatory.
- Contract hardening does not itself make arbitrary Python safe.

## Next independent actions
- Ka: perform static review/readback of contract patch; correct defects found.
- Cla: review the patch against S02/S06/S07/S08/S09/S14 and the full security matrix.
- Go: hold E2E until the approved runtime route and isolation prerequisites are proven.
- Runtime owner: expose the canonical runner through Core only after deployed source/identity and security gates are verified.

## Contract 1.2 follow-up — 2026-10-12
- Added explicit `ExecutionOperation` enum (`RUN_SCRIPT` / `RUN_TESTS`); every EXECUTION result must identify the operation.
- RUN_TESTS PASS now requires tests_run >= 1 and zero failures/errors.
- Serialization emits `execution_operation` as its string value.
- Added regression cases for missing operation, zero-test PASS, failing test summary and enum serialization.
- Source/test writes and readback are verified; the tests have not been executed by an approved runner.
