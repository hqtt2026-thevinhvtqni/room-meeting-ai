# Acceptance Plan — Work 32

- Document Number: W32-ACCEPTANCE-PLAN-002
- Priority order: P1 — CI validation and release gates
- Owner: Vinh
- Execution owner: Ka — CSA / Architecture & Backend Owner (delegated)
- Last evidence update: 2026-11-04 (Asia/Ho_Chi_Minh)

## Phase A — Baseline survey

- [x] Read governing repository and Work rules.
- [x] Confirm branch/path conventions and exact source SHA.
- [x] Inventory Python, dependencies, tests and existing workflows.
- [x] Identify safe isolated commands and external-service dependencies.
- [x] Capture baseline evidence without PC/live-service changes.
- Exit: survey and source boundary documented; implementation authorized by Vinh for the Work feature branch only.

## Phase B — Minimal CI pilot

- [x] Add a narrowly scoped GitHub Actions workflow on the Work branch.
- [x] Install declared Python dependencies without Docker.
- [x] Run Python 3.12 compile/import validation and bounded deterministic unit tests.
- [x] Run pip dependency consistency check.
- [x] Publish test evidence artifacts without secrets.
- [x] Pin external GitHub Actions to audited immutable commit SHAs.
- [x] Verify push-triggered execution against exact triggering SHA.
- [ ] Verify required-check enforcement on main — NOT APPLIED; main branch protection is not enabled and no admin settings change was authorized.
- Exit: PASS on final exact SHA `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa`, Actions run `41720062142`; 157 unit tests passed.

## Phase C — Integration / Auto E2E

- [x] Use isolated temporary fixtures and cleanup.
- [x] Prove live HTTP lifecycle/recording roundtrip in the CI runner.
- [x] Prove actual MCP stdio subprocess boundary without bypassing Core.
- [x] Verify exact four-tool MCP Public V1 inventory.
- [x] Verify legacy paste compatibility and optional identity metadata propagation/readback.
- [x] Retain JUnit artifacts for both unit and E2E jobs.
- Exit: PASS on final exact SHA `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa`, Actions run `41720062142`; 38 E2E tests passed, 1 warning. See `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.

## Phase D — CD / Release readiness

- [ ] Identify and attest an actual staging/VPS target, owner, OS/runtime and deployment path.
- [ ] Establish protected GitHub Environment with explicit human approval.
- [ ] Configure deployment credentials and host trust only after target ownership and security review.
- [ ] Define immutable artifact/revision promotion and deployment provenance.
- [ ] Implement health checks against the actual application contract.
- [ ] Demonstrate rollback/recovery on staging.
- [ ] Complete independent Vibe review and resolve findings.
- [ ] Reconcile the Work branch with current main using reviewed diffs; do not blindly rebase/merge.
- [ ] Verify required checks and branch protection before any merge.
- [ ] Obtain explicit release approval before production deployment.

Exit: BLOCKED / NOT RUN. No staging host, deployment credentials, protected environment approval, health-check target or rollback evidence is currently attested. Do not create a fake deploy job or claim CD PASS.

## Exact evidence / current status

- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/32-ci-cd-python-ci-v2`
- Validated SHA: `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`
- Actions run: `41720062142` (run #61, SUCCESS)
- Unit: 157 passed.
- Auto E2E: 38 passed, 1 warning.
- Unit artifact: `13271771079`; SHA-256 `b792ec86244662b23a8ced58422500795d5324759ee7ae4dce67d7a7b0d36773`.
- E2E artifact: `13272230927`; SHA-256 `1315a1e2a74f760ed538ccd3e207e8f1ec3f549b3f05f7d2ba3c29420db6936e`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch compare: 61 ahead / 31 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No main merge, rebase, cherry-pick, production deployment or secrets mutation.

## Overall

- CI: PASS.
- Auto E2E: PASS.
- CD: BLOCKED / NOT RUN.
- Release: NOT RELEASED.
- Work 32: ACTIVE — NOT RELEASED pending CD target evidence, branch governance, and independent review.
