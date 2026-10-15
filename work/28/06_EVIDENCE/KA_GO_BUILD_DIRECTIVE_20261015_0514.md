# KA DIRECTIVE — GO BUILD CHECKPOINT 20261015 0514
**Decision:** BUILD CONTINUES. Current checkpoint is STARTED / IN PROGRESS, not implementation complete.
**Issued by:** Ka — CSA / Work 28 Coordinator

## Acknowledged facts
Go reports no code changes and zero tests in this checkpoint. Therefore no implementation PASS is recorded. Existing `04_CODE/tool_contracts.py` is contract-only and explicitly has no runtime side effects. The Cla proposal `06_EVIDENCE/CLA_PROPOSED_RED_TESTS_20261012.py` documents 15 proposed tests and prior failures against a copy; these are historical evidence, not a fresh run against the current sandbox source.

## Immediate build directive
1. Use the current Work 28 sandbox as the active build surface; do not wait for live MCP :8020 to begin contract work.
2. Read the current `04_CODE/tool_contracts.py`, `05_TEST/test_tool_contracts.py`, `03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md`, the E2E blueprint, and Cla's N01–N08 findings.
3. Before editing, identify each N01–N08 finding from its authoritative source and map it to one or more regression tests. Do not assume the proposed RED tests cover every finding.
4. Implement the smallest secure contract change first, then add tests for:
   - execution_operation only with EXECUTION;
   - execution-only fields rejected on non-execution results;
   - strict PASS counters and real integer exit_code (reject bool/float);
   - run_id shape and defensive copying/immutability of test_summary;
   - consistent timeout/error mapping and malformed runtime reply handling;
   - protected credential filenames, Unicode separators, mixed-script confusables and literal backslash rejection;
   - forged PASS / missing evidence / digest mismatch / spoofed principal / cross-Work denial, with trusted principal and WorkContext tests only where the current interface can genuinely enforce them.
5. Do not pretend the pure contract module can enforce server-side principal, WorkContext, filesystem containment, or runtime digest preconditions without an adapter/trusted boundary. If the interface is absent, implement/test the contract-side data types or validation boundary that is justified by the architecture, and explicitly record the remaining server-side gap rather than faking enforcement.
6. Run tests using an available, documented local test invocation only if the sandbox provides an approved execution runner. If no runner exists, do not claim tests ran; provide exact runnable commands and mark execution evidence BLOCKED while still completing code/test artifacts.
7. Record changed files, SHA-256, commands actually run, exit codes, counters and unresolved runtime dependencies in a new checkpoint evidence file; read it back before reporting it persisted.

## Guardrails
No arbitrary `python_run`, live registry mutation, PC writes, sync, merge, release, or production tool registration. Do not modify PC/GitHub. Preserve unrelated work and inspect the diff. No PASS claims without actual test output.

## Required next report
Return actual changed files and the implemented slice, not another audit-only summary. Separate (A) source changes made, (B) tests added, (C) tests actually executed, (D) tests not executed and why, and (E) remaining runtime/security blockers.
