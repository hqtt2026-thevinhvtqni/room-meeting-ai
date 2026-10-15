# WORK 28 — TOOL CONTRACT AUDIT / EXECUTION GATE
Date: 2026-10-15 (+07)
Authority: Vinh
Coordinator: Co
Status: SOURCE REVIEW COMPLETE; TEST EXECUTION BLOCKED; TOOL REGISTRATION NO-GO

## READ / TRACE
Read back from Work 28 Sandbox:
- 04_CODE/tool_contracts.py (contract version 1.1.0)
- 05_TEST/test_tool_contracts.py
- 03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md
- 03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md
- 06_EVIDENCE/XU_WP1_TEST_SUMMARY_HARDENING_20261014.md

Existing source is a pure contract library. Its own module docstring says no network, filesystem, subprocess, Core, or runtime side effects; it does not grant authorization or implement an execution adapter. Registry status is DRAFT / NOT REGISTERED IN LIVE MCP.

## CONTRACT TEST INVENTORY
- Test methods present in read-back source: 19.
- Expected/discovered test count: NOT VERIFIED; no approved runner/discovery output was available through the connected tools.
- Executed tests: 0 (not run).
- Failures / errors / skipped: NOT APPLICABLE because no test process ran; do not interpret as zero.
- Exit code: NOT AVAILABLE; no process was launched.
- Canonical command recorded in test source: `python -m unittest discover -s 05_TEST -t . -v`, from Work 28 root.
- Evidence of source write/readback from 2026-10-14 exists in XU summary; that evidence explicitly says tests were not executed.

## COVERAGE REVIEW
Covered by current 19 test methods:
- lexical path traversal, absolute/drive/UNC/ADS and Unicode/control/confusable rejection;
- request/run ID shape, SHA-256 string format, bounded limit;
- unknown status normalization;
- execution operation required;
- execution PASS missing evidence fields, missing/boolean/nonzero skipped, zero tests, failures, nonzero exit;
- safe exception mapping and enum serialization.

Not proved by this pure contract test file; require integration/security tests at trusted adapter boundary:
1. Forged PASS/result payload or caller-supplied status cannot override authoritative runtime status.
2. Evidence reference resolves to protected evidence, readback integrity verifies, and evidence cannot be overwritten/deleted by Sandbox.
3. Expected source hash is compared against the immutable snapshot hash before process creation; mismatch yields BLOCKED and no process.
4. Request/idempotency replay is rejected or returns the original immutable result; payload reuse under the same request/operation key is rejected.
5. Core-derived principal, WorkContext, operation and root are authorized server-side; spoofed principal and cross-Work status/output/cancel are denied/not-found before side effects.
6. OS/process isolation, process-tree cleanup, runtime build/instance attestation and actual tool invocation through MCP -> Core -> W12/W13.
7. Test discovery inventory must reconcile expected, discovered and executed counts, including failures, errors and skipped.

The current ToolResult shape validator cannot itself prove any of the above; adding a syntactically valid SHA or non-empty evidence_ref is not proof that either is true.

## DECISION
NO-GO for registering any execution tool. Do not change live MCP registry. Source contract hardening is a design/source milestone only, not a test or security PASS.

## BLOCKED
No approved Python/unittest/pytest execution tool is exposed by this session. The connected ROOM-HOP tools provide Sandbox file operations but no process launch or local PC access. Therefore tests were not run and no exit code exists. No PC source, MAIN_SOURCE, live service, GitHub branch, or execution endpoint was changed.

## NEXT ACTION
Authorized operator on canonical PC/repository runs the exact command above from Work 28 root in an approved isolated runner; captures command, Python/runtime identity, stdout/stderr, exit code, discovered/executed/failure/error/skipped counts and source SHA-256. Then implement and test the missing adapter-boundary negative cases before a separate security/E2E review. Tool registration remains prohibited until Core authorization, W12/W13 isolation, protected evidence and live MCP-to-Core readback are evidenced.
