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
See `03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md` for A01-A18. Must exercise the deployed MCP entry point through Core to the canonical runtime and protected evidence; unit tests and direct runtime calls do not substitute.

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
