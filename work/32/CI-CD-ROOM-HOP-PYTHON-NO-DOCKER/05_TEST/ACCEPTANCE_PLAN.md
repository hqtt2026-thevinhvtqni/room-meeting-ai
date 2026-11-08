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

## Phase D — Immutable product artifact

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
- Validated SHA: `e451764d4bc900a98f4d0b2d00a1e863ea86b22c`
- Actions run: `41723597131` (run #68, SUCCESS)
- Unit: 157 passed.
- Product Auto E2E: 39 passed, 1 warning.
- Unit artifact: `13271834116`; SHA-256 `ace199d3ba5a5993933397ab711820a864f18849b7f206bd0fd7544b05cfe520`.
- E2E artifact: `13273572459`; SHA-256 `ef3e55a390d5534c9325cbd88163eb3fb87679528428cf782c900bd46fe2f7fa`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch compare: 68 ahead / 32 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No main merge, rebase, cherry-pick, production deployment or secrets mutation.

## Overall

- CI: PASS.
- Auto E2E: PASS.
- CD: BLOCKED / NOT RUN.
- Release: NOT RELEASED.
- Work 32: ACTIVE — NOT RELEASED pending CD target evidence, branch governance, and independent review.


### Product boundary note

The Core product E2E is PASS for the exact scope in W32-EVIDENCE-005. The separate Dashboard is still mock-backed at inspected HEAD `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`; its end-user browser-to-Core flow is NOT RUN. The dashboard bridge contract and the locked Core/Workspace ownership contract must be reconciled before adding a truthful integrated UI test. Do not bypass Core or create a second source of meeting state.


### Product artifact evidence

- Artifact source SHA: `0069157d24d6748cff69f162147b892242d9726f`.
- Workflow run #67: `41723138912` — SUCCESS (unit 157; Product Auto E2E 39; artifact-level E2E 1 passed).
- Immutable release-candidate artifact: `13272918198`, ZIP digest `fa059d00b74fe7e884c98ca95dc9ec283dcb940ffaa0b3b6eec4c25761a299f6`.
- Full artifact evidence: `06_EVIDENCE/W32-EVIDENCE-006-PRODUCT-ARTIFACT-20261104.md`.


## Final exact-SHA artifact pipeline validation — PASS

- Final branch SHA: `e451764d4bc900a98f4d0b2d00a1e863ea86b22c`.
- GitHub Actions run #68: `41723597131` — SUCCESS on exact SHA.
- Unit: 157 passed in 2.68s.
- Product Auto E2E: 39 passed, 1 warning in 3.94s.
- Immutable artifact job: archive built, SHA-256 generated and verified, extracted to clean directory, dependencies installed, `pip check`, `compileall`, artifact-level product E2E: 1 passed in 2.15s.
- Product source archive SHA-256: `76d77939c43b33727a534cbccd06e4240eb106458659b9186f9fb125ca59f0ae`.
- Archive: `room-hop-e451764d4bc900a98f4d0b2d00a1e863ea86b22c.tar.gz`.
- Product artifact ID: `13271449355`; uploaded ZIP SHA-256: `9a688cc80b97e428a2d1b9c39a3c4bc97aa854e7b0715b64e8a7d39aa98c6062`.
- Unit artifact ID `13271834116`; ZIP digest `ace199d3ba5a5993933397ab711820a864f18849b7f206bd0fd7544b05cfe520`.
- Product E2E artifact ID `13273572459`; ZIP digest `ef3e55a390d5534c9325cbd88163eb3fb87679528428cf782c900bd46fe2f7fa`.
- Retention: 14 days.

- Product artifact ID `13271449355`; archive SHA-256 `76d77939c43b33727a534cbccd06e4240eb106458659b9186f9fb125ca59f0ae`; upload bundle digest `9a688cc80b97e428a2d1b9c39a3c4bc97aa854e7b0715b64e8a7d39aa98c6062`.


## Current exact-SHA checkpoint — 2026-11-08 / Run #229

- Current implementation branch: `work/32-ci-runner-owned-fixture-v2`.
- Exact validated source SHA: `4177721a1e557f20127ff124b6c8d64ab63321e7`.
- GitHub Actions run #229 / `42456186691`: SUCCESS, 6/6 jobs.
- Unit: 189 passed; Product Auto E2E: 68 passed; Windows Browser Adapter E2E: 10 passed; immutable artifact-level E2E: 1 passed.
- Windows Browser Adapter test proves runner-owned disposable Core fixture, process identity/health/listener preflight, Browser workflow, MCP Public V1 stdio handoff and transcript readback, plus exact-process cleanup.
- Product source archive SHA-256: `e16cbff567681555b9c70b86ac3c8a5a5f4c582e0b83b5db7d9f12aa4749b1c2`; independently recomputed digest matched the checksum file in the downloaded artifact.
- Main integration is NOT ACCEPTED: compare against main HEAD `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb` is diverged (246 ahead / 273 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`; 80 changed files). No merge/rebase/cherry-pick; independent review and clean integration strategy required.
- Dashboard browser→Core remains BLOCKED / NOT RUN.
- Phase D (staging/VPS, protected approval environment, credentials, health checks, rollback, independent Vibe review, main integration) remains BLOCKED / NOT RUN. CI artifact is a release candidate, not a deployed release.
- G7 RELEASE: NOT READY / NOT AUTHORIZED under DOC-050. Work32 remains ACTIVE — NOT RELEASED.


## Latest exact-SHA checkpoint — 2026-11-08 / Run #232

- Exact cleanup SHA `4dd07dbf4c30541c70bb91e8b053fe62d8b6290e`; Actions run #232 / `42459846727`: SUCCESS, 6/6 jobs.
- Unit 189 passed; Product Auto E2E 68 passed; Windows Browser Adapter E2E 10 passed; artifact-level product E2E 1 passed; tooling mirror IN_SYNC; release acceptance CI gate PASS.
- Windows disposable meeting `MEETING-W32-42459846727-1`; PID 11160; dynamic port 58525; exact-SHA process/owner/health/listener preflight PASS; MCP handoff/readback PASS; cleanup PASS.
- Removed 44 confirmed Windows Explorer `desktop.ini` metadata files from Work32 feature branch; verified zero remain. No test code or Core/API/DB/runtime behavior changed in this cleanup.
- Main integration remains BLOCKED; Dashboard→Core remains BLOCKED / NOT RUN; Phase D CD/deployment remains BLOCKED / NOT RUN; DOC-050 G7 RELEASE NOT READY / NOT AUTHORIZED. Work32 remains ACTIVE — NOT RELEASED.


## Latest exact-SHA checkpoint — 2026-11-08 / Run #234

- Branch SHA: `0fd12a94dcf598583e402cdb92352ee2f6596880`; GitHub Actions Run #234 / `42460406640`: SUCCESS, 6/6 jobs.
- Unit 189 passed; Product Auto E2E 68 passed; Windows Browser Adapter E2E 10 passed; immutable artifact E2E 1 passed; tooling workflow mirror IN_SYNC; CI release acceptance gate PASS.
- Windows disposable meeting `MEETING-W32-42460406640-1`; adapter PID 21468; dynamic port 58821; exact-SHA preflight, MCP stdio handoff/readback and cleanup PASS.
- Main compare: current main `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb`; diverged 251 ahead / 273 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`; 124 changed paths. No merge/rebase/cherry-pick.
- Work32 remains ACTIVE — NOT RELEASED; Dashboard→Core and CD remain BLOCKED / NOT RUN; DOC-050 G7 RELEASE NOT READY / NOT AUTHORIZED.
