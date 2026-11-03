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

## Phase C — Product-level Integration / Auto E2E

- [x] Use isolated temporary fixtures and cleanup.
- [x] Prove live HTTP lifecycle/recording roundtrip in the CI runner.
- [x] Prove actual MCP stdio subprocess boundary without bypassing Core.
- [x] Execute one complete Core product journey: identity discovery, Core ID allocation, create/open/join/start, policy/quorum rejection, MCP recording, transcript byte-integrity, close, final artifact and post-close MCP readback.
- [x] Verify real HTTP server + real MCP stdio child process against one isolated persistent meeting directory.
- [x] Verify raw paste remains separate from the official final artifact.
- [ ] Dashboard browser → Core integrated journey — BLOCKED / NOT RUN; Dashboard bridge source is still mock and its proposed API is not part of the locked Core contract.
- [x] Verify exact four-tool MCP Public V1 inventory.
- [x] Verify legacy paste compatibility and optional identity metadata propagation/readback.
- [x] Retain JUnit artifacts for both unit and E2E jobs.
- Exit: Core product-level Auto E2E PASS on SHA `a39438caa694549a7918d3a86878ee5ff95338de`, Actions run `41722337882`; 39 E2E tests passed, 1 warning. See `06_EVIDENCE/W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104.md`. Dashboard→Core E2E remains BLOCKED / NOT RUN.

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
- Validated SHA: `a39438caa694549a7918d3a86878ee5ff95338de`
- Actions run: `41722337882` (run #64, SUCCESS)
- Unit: 157 passed.
- Product Auto E2E: 39 passed, 1 warning.
- Unit artifact: `13271603230`; SHA-256 `d53fefde32748e5c8bc5cbb44090d041c402b6faeb076fb8bf8533fd274dee18`.
- E2E artifact: `13273077743`; SHA-256 `ff7c5cc0e63d39dedd83031cebe6c1a4aa501f153a98cf32eb137b819ceaa729`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch compare: 64 ahead / 32 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No main merge, rebase, cherry-pick, production deployment or secrets mutation.

## Overall

- CI: PASS.
- Auto E2E: PASS.
- CD: BLOCKED / NOT RUN.
- Release: NOT RELEASED.
- Work 32: ACTIVE — NOT RELEASED pending CD target evidence, branch governance, and independent review.


### Product boundary note

The Core product E2E is PASS for the exact scope in W32-EVIDENCE-005. The separate Dashboard is still mock-backed at inspected HEAD `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`; its end-user browser-to-Core flow is NOT RUN. The dashboard bridge contract and the locked Core/Workspace ownership contract must be reconciled before adding a truthful integrated UI test. Do not bypass Core or create a second source of meeting state.
