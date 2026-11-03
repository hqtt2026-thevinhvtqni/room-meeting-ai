# WORK 28 — TEST PLAN
Revision: 1.2 — 2026-10-12
Status: source/test specification written; no approved-runner execution claimed.

## 1. Canonical local contract command
From Work 28 Sandbox root:
`python -m unittest discover -s 05_TEST -t . -v`
Acceptance requires exact command, exit code 0, test count > 0 and captured output. A green process with zero discovered tests is failure. This command has not yet been run by an approved runner in this session.

## 2. Contract regression scope
- request_id/run_id generation and ASCII validation.
- SHA-256 shape.
- bounded limit including None/default and bool rejection.
- path traversal, absolute/drive/UNC/ADS, NFKC/NFC, bidi/invisible/control, Windows reserved names, trailing dot/space, option-like components, wildcards/expansion and protected metadata.
- status lifecycle, safe exception mapping and serialization.
- execution result must explicitly identify RUN_SCRIPT or RUN_TESTS.
- execution PASS must include run_id, exit_code=0, source_sha256, evidence_ref and non-empty run/test summary.
- RUN_TESTS PASS requires tests_run >= 1 and failures/errors = 0.
- execution with nonzero exit, zero tests, malformed summary, missing evidence or nonzero test failure/error must not PASS.

## 3. Automatic E2E matrix
The canonical operating pipeline is `01_PLAN/WORK28_AUTO_E2E_RUNBOOK_V2.0.md`; A01-A18 acceptance cases remain in `03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`. GitHub Actions `Work 28 Automatic E2E Gate` runs source/contract regression and native Linux/Windows lifecycle suites on every relevant push/PR and emits a machine-readable gate report. The deployed MCP → Core → canonical Runtime → Execution Host → protected evidence/readback path remains BLOCKED until deployed identities and trusted route/isolation evidence are wired. CI PASS is not live E2E PASS.

The gate evaluator `04_CODE/work28_auto_e2e_gate_v1.py` must calculate PASS only from a complete evidence record with deployment-held HMAC-SHA256 attestation and pinned key ID, Work-relative entry path, path containment and symlink-rejection attestations; missing verifier configuration or invalid/tampered signatures must never PASS. Its 16 contract tests are tests of the evaluator only, not evidence that a deployed E2E execution occurred.

## 4. Security/runtime tests — BLOCKED
- Authenticated principal derivation and Core WorkContext resolution.
- Cross-Work access checks on run/status/output/cancel.
- Filesystem containment and no-follow/reparse-point protection at open time.
- Immutable source snapshot/hash binding.
- OS isolation for host files/secrets/network/loopback.
- resource caps, timeout and process-tree cleanup.
- protected evidence write/readback and agent overwrite/delete denial.
- runtime identity and no fallback host.

## 5. Gate status
- G1 source inventory: PARTIAL; inspected source snapshot does not prove deployed PC SHA.
- G2 contract/policy: IN PROGRESS; independent review pending.
- G3 approved-runner contract tests: BLOCKED.
- G4 auth/path/isolation: BLOCKED.
- G5 live MCP -> Core -> canonical runtime -> protected evidence: BLOCKED.
- G6 compatibility and full E2E: BLOCKED.
