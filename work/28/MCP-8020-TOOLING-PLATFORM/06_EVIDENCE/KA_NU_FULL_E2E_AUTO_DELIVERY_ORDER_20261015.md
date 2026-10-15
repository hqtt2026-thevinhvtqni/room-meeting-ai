# KA → NU — FULL E2E-AUTOMATIC DELIVERY ORDER — WORK 28
Date: 2026-10-15
Work: 28 — MCP-8020-TOOLING-PLATFORM
Authority: Vinh
Coordinator / independent reviewer: Ka (CSA)
Implementation owner: Nu
Delivery support: Go
Independent security veto/review: Cla

## Mission
Nu owns the end-to-end completion of Work 28, not merely a contract, plan, or isolated unit tests. Drive READ → TRACE → DESIGN → BUILD → TEST → E2E → EVIDENCE → READBACK → HANDOFF. Work in the Work 28 Sandbox and any explicitly approved isolated runner only. Report blockers as evidence, not as speculative PASS.

## Source-of-truth rules
1. Read the current Work 28 manifest, requirements, architecture blueprint, test plan, latest Go v1.3.0 checkpoint, Ka source/security audits, and Cla historical review.
2. Reconcile current artifacts before editing. Preserve history and do not overwrite evidence; version new artifacts.
3. Separate these claims: SOURCE REVIEW, UNIT/CONTRACT TEST, ISOLATED ADAPTER TEST, CONNECTOR E2E, LIVE PC MCP :8020 E2E. Never promote one level to another.
4. Current Go checkpoint says tests run = 0. Treat tests as NOT RUN until a valid runner log proves otherwise.
5. Do not treat the 18-tool live list as proof of source/runtime binding. Do not infer live code from public GitHub or Sandbox files.

## Required delivery phases
### P0 — Inventory and deterministic validation
- Read the full 04_CODE/tool_contracts.py and 05_TEST/test_tool_contracts.py; if connector read limits prevent review, split test source into bounded evidence segments without changing test semantics.
- Inspect and map all v1.3.0 contracts and historic Cla findings against current source. Confirm/fix only with source-backed evidence.
- Provide exact test command, interpreter/version, working directory, discovered and executed test counts, stdout/stderr, exit code, and SHA-256 of source/test files when an approved route exists. Never invent hash or test results.
- No PASS with zero discovered/executed tests.

### P1 — Resource enforcement
- Implement and test adapter-level bounded reads and bounded directory listing; configuration fields alone are not enforcement.
- Count UTF-8 payload by bytes. Test exactly-at-limit and one-byte/entry-over-limit, multibyte UTF-8, huge file and huge directory cases.
- Choose explicit overflow semantics (deny or explicit truncation metadata); never silently truncate. Avoid reading entire untrusted files or materializing entire directories before applying limits.

### P2 — Real authorization boundary
- Keep TrustedPrincipal and WorkContext as data contracts, not proof of authentication.
- Trace and implement authorization at the actual adapter/Core enforcement boundary only where the canonical source and approved isolated environment are available.
- Derive principal from trusted transport/server-side context; never trust caller-supplied identity_id, authorized, role, or allowed_operations.
- Enforce all six operations (LIST/READ/CREATE/WRITE/APPEND/DELETE), scoped to the requested Work, fail closed. Add forged-principal, missing-context, operation-mismatch and cross-Work negative tests.
- Treat lexical path validation separately from filesystem containment. Test traversal, absolute/drive/UNC/ADS, symlink/reparse/junction escape and race/TOCTOU where the actual filesystem adapter is available.

### P3 — Execution/evidence trust model
- Keep python_run NO-GO. No arbitrary shell, command strings, caller-selected interpreter/cwd/environment, or fallback execution host.
- Define a server-owned run lifecycle and acceptance logic. A test run cannot PASS on printed JSON, self-reported counters, exit code alone, or forged in-process test summaries.
- Require immutable source snapshot/hash binding, trusted runtime identity, server-created request/run IDs, bounded outputs/resources, timeout/process-tree cleanup evidence, protected evidence write/readback and integrity verification before PASS.
- If canonical runtime, trusted Core route, OS isolation or protected evidence writer is absent, implement only safe contracts/adapters/tests in the isolated Sandbox and mark runtime E2E BLOCKED. Do not fabricate a runner or second host.

### P4 — Automatic regression / red-green E2E
- Build one deterministic entry point for the tests that are genuinely executable in the approved isolated environment.
- Exercise baseline → deliberate disposable TEST-WORK mutation → expected FAIL with nonzero exit and evidence → revert/patch → new PASS with new run ID/hash/evidence; never mutate MAIN SOURCE or production Work for the red test.
- Test malformed responses, zero tests, test failure despite process exit 0, nonzero exit, hash mismatch, missing/forged principal, cross-Work access, limits, evidence overwrite/delete and cleanup failures.
- If an end-to-end stage depends on PC/runtime credentials or a route unavailable here, mark that stage BLOCKED and write the exact evidence request. Do not claim full E2E PASS.

### P5 — Evidence and handoff
- Produce 06_EVIDENCE/NU_WORK28_FULL_E2E_DELIVERY_<timestamp>.md.
- Include file list/change rationale, architecture/source trace, test matrix, tests added vs actually executed, exact environment/command/log/counters/exit code, SHA-256 or explicit hash BLOCKED, E2E layer reached, negative-test outcomes, known risks, and reproducible next command.
- Append a concise status to 06_EVIDENCE/NHAT_KY_THI_CONG.md.
- Ask Ka for independent source/evidence review; ask Cla for security veto/review after current artifacts are readable. Nu must not self-certify final PASS.

## Safety and scope boundaries
- Authorized: read, trace, design, edit and test Work 28 Sandbox artifacts and approved isolated copies; add tests and evidence.
- Not authorized by this order: edit the live PC repository, restart/replace MCP :8020 or Core services, change live tool registration, enable python_run, deploy/release, or change production/MAIN SOURCE. These remain blocked pending source/runtime evidence and explicit Vinh approval.
- Do not overwrite/clean unrelated working-tree changes. Do not create duplicate runners/bridges or duplicate capabilities.
- Final release remains NO-GO until live source/runtime binding, real authorization, filesystem containment, OS isolation, protected evidence, full approved E2E and Cla review are proven.

## Required immediate response from Nu
Read the order, inspect current Work 28 artifacts, then publish a short checkpoint naming: (1) first concrete build slice, (2) files to change, (3) tests to execute and the actual runner available, (4) blockers requiring Go/Cla/PC evidence. Proceed with the isolated work without waiting for another planning cycle.
