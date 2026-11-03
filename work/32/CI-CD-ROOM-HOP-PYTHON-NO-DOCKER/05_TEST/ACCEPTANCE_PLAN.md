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
- [x] Verify push-triggered execution against exact triggering SHA.
- [ ] Verify required-check enforcement on main — NOT APPLIED; main branch protection is not enabled and no admin settings change was authorized.
- Exit: PASS on exact SHA `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`, Actions run `41719444619`; 157 unit tests passed.

## Phase C — Integration / Auto E2E

- [x] Use isolated temporary fixtures and cleanup.
- [x] Prove live HTTP lifecycle/recording roundtrip in the CI runner.
- [x] Prove actual MCP stdio subprocess boundary without bypassing Core.
- [x] Verify exact four-tool MCP Public V1 inventory.
- [x] Verify legacy paste compatibility and optional identity metadata propagation/readback.
- [x] Retain JUnit artifacts for both unit and E2E jobs.
- Exit: PASS on exact SHA `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`; 38 E2E tests passed, 1 warning. See `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.

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
- Actions run: `41719444619` (run #50, SUCCESS)
- Unit: 157 passed.
- Auto E2E: 38 passed, 1 warning.
- Unit artifact: `13271935444`; SHA-256 `f65f5ded755fc64c51baa876e604e5f8d0cde2b67d748a6f6db46792a35bf9c5`.
- E2E artifact: `13271058785`; SHA-256 `6e2a5149466a56b938d0e59ef5be93b533117c98d5d0b35477cf341481c938c9`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch compare: 52 ahead / 31 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No main merge, rebase, cherry-pick, production deployment or secrets mutation.

## Overall

- CI: PASS.
- Auto E2E: PASS.
- CD: BLOCKED / NOT RUN.
- Release: NOT RELEASED.
- Work 32: ACTIVE — NOT RELEASED pending CD target evidence, branch governance, and independent review.
