# WORK 28 — WP1 TEST SUMMARY HARDENING (SANDBOX-ONLY)
Date: 2026-10-14 (+07)
Authority: Vinh
Coordinator: Xu
Status: SOURCE WRITTEN + READBACK VERIFIED; TESTS NOT EXECUTED

## Scope
A narrow Work 28 contract-hardening slice was applied only to the Work 28 Sandbox copies of:
- 04_CODE/tool_contracts.py
- 05_TEST/test_tool_contracts.py

No PC source, MAIN_SOURCE, GitHub branch, running service, registry registration, or execution endpoint was changed.

## Defect addressed
Before this change, RUN_TESTS execution PASS validation:
- defaulted missing failures/errors counters to zero;
- did not require a skipped counter;
- therefore could accept incomplete test summaries that did not explicitly prove zero skipped tests.

## Change made
For execution results marked PASS with operation RUN_TESTS, the contract now requires each of tests_run, failures, errors, and skipped to be present as an integer, explicitly rejects bool values, requires tests_run >= 1, and requires failures=0, errors=0, skipped=0.

Added regression cases for:
- missing skipped counter;
- boolean skipped counter;
- nonzero skipped counter.

Updated existing positive/failure test summaries to include explicit counters where applicable.

## Verification
- Sandbox writes returned status=ok for both files.
- Both files were read back through MCP.
- Static readback confirmed the required-counter validation and the new regression-test names are present.
- Test method count in the read-back test file: 19.
- No Python/unittest/pytest runner was available through the connected MCP tools; tests were NOT executed.
- This is not a test PASS, runtime PASS, security PASS, or live E2E PASS.

## Remaining review items
- Validate expected/discovered/executed test inventory, not merely tests_run >= 1.
- Independently inspect the diff and run canonical command in an approved runner.
- Add/verify negative cases for forged status, replay, absent evidence, source hash mismatch, and unauthorized/cross-Work access.
- Keep python_run / execution tools unregistered until Core authorization, canonical W12/W13 runtime, OS isolation, protected evidence and independent live E2E pass.
