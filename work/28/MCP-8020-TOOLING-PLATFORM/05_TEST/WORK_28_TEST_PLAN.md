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


---

## Current Work 32 adoption / exact-SHA CI addendum — 2026-11-04

The Work 32 product Auto E2E pattern has been adopted without importing Work 32 meeting-domain endpoints or weakening Work 28 security boundaries.

- Exact-SHA pipeline: `41743292650`, source `e835a13ae0cddd84a077e17055cd9354a874f212`, all five jobs SUCCESS.
- Unit/regression suite: **348 passed / OK**.
- New G3 test: `test_mcp8020_unified_server_stdio_contract_v1.py` launches the Work 28 MCP server factory as a real child process over MCP stdio and checks the exact 31 tool names and all schemas. Inert providers are used only to isolate transport/contract; this is not product execution or deployed E2E.
- Linux suspended-spawn: 13 passed, 4 Windows-only skipped. Windows suspended-spawn: 17 passed.
- Immutable artifact job: exact-SHA tar.gz SHA-256 verified, clean extraction, dependency check, compileall and **348 tests passed** against extracted artifact.
- Source archive SHA-256: `23dc6b188eb381569f476b6e043b5a12290f4ae610183d926e8a1ab7da3348d6`.
- Source artifact ID `13282017725`; report artifact ID `13283075166`.

### Current gate disposition

- G0 provenance / exact SHA: PASS for this CI run.
- G1 dependency / compile: PASS.
- G2 unit and Linux/Windows lifecycle regression: PASS.
- G3 MCP stdio transport + exact tool/schema contract: PASS (contract-only scope).
- G4 trusted Core authorization + approved Runtime + Execution Host deployed product journey: BLOCKED / NOT RUN.
- G5 protected evidence persistence and authorized readback on deployed route: BLOCKED / NOT RUN.
- Artifact extraction and retest: PASS.
- Independent An QA and Ka architecture/security review: pending separate reports; not self-certified by Vi.
- Execution Gate: CLOSED. Release: NOT RELEASED.
