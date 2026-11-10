# W1111 — AUTONOMOUS E2E EXECUTION MODE
**Owner:** Co — Coder W1111
**Authority:** User/Chairman; Cla remains CTO / technical work coordinator
**Effective:** 2026-11-10 07:43 UTC+7
**Priority:** P0 — Core → Execution Host → Sandbox → GitHub

## Operating instruction
Co is authorized to execute the W1111 P0 work end-to-end autonomously within currently available connected Sandbox and GitHub capabilities. Do not stop for approval or send progress reports at each stage. Continue through inspect → implement → test → inspect evidence → correct → retest → branch commit/PR → remote readback → journal.

## Work sequence
1. Reconcile canonical W1111 task, journal, baseline, source trace, PR #48 and current branch/commit state before modifying anything.
2. Work only on a dedicated non-main branch / existing authorized PR branch. Preserve unrelated changes and existing records.
3. Resolve Core authority integration and execution-host path, then W13 grant validation and W12 host execution; verify the exact source SHA and Work policy.
4. Build E2E tests for positive authorization and negative boundaries (wrong Work, wrong SHA, expired/replayed grant where applicable, workspace/path boundary, timeout/process cleanup, Core record failure).
5. Verify durable Core result recording and FINAL_RESULT.json; check that failures remain failures and cannot be reported as PASS.
6. Verify Sandbox → GitHub branch/commit/PR remote readback and record exact SHAs, test results, and artifacts.
7. Self-correct implementation/test failures within available permissions; rerun relevant tests and full suite when possible. Do not hide skipped, unavailable, or blocked checks.
8. Keep canonical W1111 journal and revision/evidence records current. Preserve original source records; append corrections/addenda rather than rewriting history.

## Reporting policy
- No routine step-by-step updates to the user.
- Report only when (a) a PC/VS Code action is genuinely required, with one consolidated copy/paste command and exact expected output; (b) an explicit human approval/secret/deployment privilege is required; or (c) work is complete or a hard blocker is proven.
- When requesting PC support, explain why connected Sandbox/GitHub cannot perform that step, list the exact evidence needed, and wait. Do not ask the user to run PC commands for work that can be done through connected tools.

## Hard safety / authority boundaries
- No main-branch writes, PR merge, release, production deployment, service restart, credential creation/rotation, secret disclosure, destructive cleanup, or privilege escalation without the corresponding explicit authority.
- No use of the user's laptop as an execution host. C07 read-only PC attestation may be requested only if exact live process/module/hash evidence cannot be obtained remotely and is essential to diagnose the blocker.
- Do not infer live PASS from CI PASS, file write/readback, or a source-level test. Keep CI, Sandbox, live runtime, and GitHub remote evidence distinct.
- If current tools lack a real process runner for Sandbox execution, continue all code/docs/CI preparation possible, then raise one consolidated PC/VS Code request only for the irreducible live-runtime step.
- Preserve exact blockers and evidence; never manufacture results.

## Definition of done
A traceable E2E run proves: authorized request → Core policy/grant → Execution Host validation → execution in the correct Work Sandbox → result artifact and durable Core record → remote GitHub branch/commit readback. Include negative authorization tests, exact tested SHA, CI run/job evidence, and runtime identity evidence. Until all required layers are evidenced, status remains BLOCKED / NOT VERIFIED, not PASS.