# Work 32 — Manifest

- Name: CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Owner/final authority: Vinh
- Coordinator: Xu (AI-01)
- Date: 2026-10-24, Asia/Ho_Chi_Minh
- Status: Run #430 hosted/source lanes PASS; live Core/Host identity BLOCKED; workflow mirror strict-parity remediation committed at current PR head; exact-head retest PENDING; release acceptance gate FAIL; ACTIVE — NOT RELEASED
- Sandbox ID: 32
- GitHub branch (current implementation): work/32-main-integration-authority-20261112 (PR #52; do not merge without Vinh approval)
- Previous CI pilot branch names in historical records are not the current implementation ref.

## Goal
Survey and design evidence-first CI/CD for existing Python ROOM-HOP without Docker. Supplemental scope: remove the Tester dependency on Vinh's PC by providing repeatable Python/pytest execution through the existing authorized Work 12/13 Execution Host contract, plus fail-closed test-result classification.

## Guardrails
No Docker requirement; no live-service or MAIN SOURCE changes; no auto-merge or production deploy. Vinh explicitly authorized Ka on 2026-11-04 to implement and push Work 32 changes only to the dedicated feature branch and activate branch-scoped CI/Auto E2E. This authorization does not permit main merge, production deployment, secrets changes, or bypass of independent review. CD remains a separate gated phase. Core :8000 remains the single source of truth and must never be installed inside Sandbox. Sandbox is the AI build zone; MAIN SOURCE remains read-only for AI build operations. The full ROOM-HOP source tree is not copied into this Work.

## Integration boundaries
- Work 12 owns the Work Execution Environment contract.
- Work 13 owns the canonical Execution Host service/bridge (POST /execute).
- Work 27 owns the sandbox runtime adapter/contract and must not be duplicated.
- Work 32 owns the Python CI candidate, environment/test evidence classification and acceptance plan.
- Work 51 consumes this capability for the Coder–Tester loop.
- Current evidence: live execution capability is not attested through the current ROOM-HOP route; no pytest result is claimed.


## Current evidence snapshot — 2026-11-04

- Canonical implementation branch: `work/32-ci-cd-python-ci-v2`.
- Final exact-SHA validation: `ecb263a2d53786e71bdca8eed336b303506c06b4` (Actions run #65, `41722744353`, SUCCESS).
- GitHub Actions run #65 / `41722744353`: SUCCESS on final exact SHA; run #64 / `41722337882`: SUCCESS on product-level Auto E2E SHA; run #58 / `41719864578`: SUCCESS after action SHA pinning.
- Python 3.12 bounded unit gate: 157 passed.
- Product Auto E2E gate: 39 passed, 1 warning; includes one complete live HTTP → MCP stdio → persistent transcript → HTTP close → MCP readback journey. Immutable source artifact was extracted and re-tested: 1 product E2E passed.
- Artifact evidence and SHA-256 digests: `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch comparison: 68 ahead / 32 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No merge/rebase/cherry-pick; main unchanged.
- CD / deployment remains BLOCKED until a real staging target, ownership, approved credentials/environment, health check, and tested rollback are evidenced.
- Release status: ACTIVE — NOT RELEASED.


## Product-level boundary

- Core product journey is now verified end-to-end by `tests/test_ci_product_e2e.py`; evidence: `06_EVIDENCE/W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104.md`.
- The separate HQTT Dashboard still uses `createMockBridge()` at inspected source HEAD `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`; Dashboard→Core integrated E2E is BLOCKED / NOT RUN. Do not treat a mock UI build as proof of product integration.
- CD / staging / production remains BLOCKED / NOT RUN. No deploy target or rollback evidence is attested.


## Immutable product artifact gate

- GitHub Actions run #67 / `41723138912`, exact source SHA `0069157d24d6748cff69f162147b892242d9726f`: SUCCESS.
- Job `Build and verify immutable ROOM HOP product artifact`: PASS.
- Built exact-SHA source archive `room-hop-0069157d24d6748cff69f162147b892242d9726f.tar.gz`; checksum generated and verified.
- Extracted archive; installed declared dependencies; `pip check`; `compileall`; product E2E against extracted artifact: 1 passed in 1.76s.
- Release-candidate artifact bundle ID `13272918198`, uploaded ZIP digest `fa059d00b74fe7e884c98ca95dc9ec283dcb940ffaa0b3b6eec4c25761a299f6`, 14-day retention.
- This is a CI release-candidate artifact only, not a deployed release.


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

- Main HEAD: `157e88e2cd821a0b53bdcabd6483956e6bc2074a`; merge base: `9e4002cbd93a6b92684b17623d79a1adda161d37`. No merge/rebase/cherry-pick.


## Final exact branch verification — 2026-11-04

- Final exact SHA: `4a931a351432a1ce6a06b84f05ed6fa3c788a1eb`.
- GitHub Actions run #70: `41724182414` — SUCCESS.
- Unit: 157 passed in 1.90s.
- Product Auto E2E: 39 passed, 1 warning in 2.74s.
- Immutable artifact job: exact-SHA archive created, checksum verified, extracted, dependencies checked, packages compiled; artifact-level product E2E: 1 passed in 2.52s.
- Source archive: `room-hop-4a931a351432a1ce6a06b84f05ed6fa3c788a1eb.tar.gz`.
- Source archive SHA-256: `0b14943b1a85201fa0dc02ba0f823b5fa15440ed0935d7da5a020aa29c3861a2`.
- Product artifact ID `13272004526`; uploaded ZIP digest `24221ef509286698cc73ce3edbe0fd20650cbf5cdd89745e86b3f728996f4d21`.
- Unit artifact ID `13272199414`; ZIP digest `878c286f3e84b392560c917715d5bf5b5e7c7979fac63d7d5c0c7345795b5e87`.
- Product E2E artifact ID `13273940178`; ZIP digest `543b2e0a0641e6de9d205aaa278e5f038132ffdc7fb54e9add6e971b2d52cf0a`.
- All artifacts retained for 14 days.
- Main HEAD `157e88e2cd821a0b53bdcabd6483956e6bc2074a`; Work branch 70 ahead / 32 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`. No merge/rebase/cherry-pick.
- Core product Auto E2E + immutable artifact E2E: PASS. Dashboard→Core browser integration: BLOCKED / NOT RUN. CD/staging/production: BLOCKED / NOT RUN. Release: NOT RELEASED.

 
## Current checkpoint — 2026-11-06 (canonical branch correction)

- **Canonical GitHub implementation branch:** `work/32-ci-cd-python-ci-v2`.
- The previous top-level branch value naming `work/32-ci-cd-room-hop-python-no-docker` referred to the original CI pilot branch and is superseded for current implementation work.
- Current audit HEAD: `3dc65a4603823f58543f5216af2b0885df3a1627`; last completed full CI: run #108 / `41953241351`, SHA `442ef9eb0623a610378433705d4baf5663e6ca2b`, SUCCESS 4/4. Run #109 / `42118931381` validates the subsequent journal-only commit and is still in progress at checkpoint.
- Main comparison: 184 ahead / 35 behind, merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`; 74 changed files. Do not merge directly.
- PR #40 is the old pilot PR, OPEN / DRAFT, and has no review submissions. It is not the current v2 branch review.
- Keep Work 32 ACTIVE — NOT RELEASED. Main integration requires independent review and a clean integration branch based on current main; PC runtime, Dashboard→Core and CD gates remain separate.


## Current verified checkpoint — 2026-11-08 (Run #229)

- Current implementation branch: `work/32-ci-runner-owned-fixture-v2`.
- Exact validated SHA: `4177721a1e557f20127ff124b6c8d64ab63321e7`.
- GitHub Actions run #229: `42456186691` — SUCCESS, 6/6 jobs.
- Unit: 189 passed; Product Auto E2E: 68 passed; Windows Browser Adapter E2E: 10 passed; artifact-level E2E: 1 passed.
- Work32 tooling tests PASS; active workflow and mirror IN_SYNC.
- Windows runner-owned fixture, process/owner/health/listener preflight, MCP stdio handoff/readback and exact-process cleanup PASS. Windows artifact ID `13607457887`, SHA-256 `eaa90c74da57cc17569bbd67d7e884c69c1cab5edfe154a02395790b14bf3e62`.
- Immutable product artifact ID `13606734880`; source archive SHA-256 `e16cbff567681555b9c70b86ac3c8a5a5f4c582e0b83b5db7d9f12aa4749b1c2`; checksum re-computation matched packaged checksum.
- Main HEAD at audit: `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb`. Work branch vs main: diverged, 246 ahead / 273 behind, merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`, 80 changed files. No merge/rebase/cherry-pick performed.
- Source archive hygiene inventory: 44 `desktop.ini` paths and 43 test/test-results-like paths; classification/remediation pending. No mass deletion authorized/performed.
- Dashboard→Core browser integration remains BLOCKED / NOT RUN. CD/deployment remains BLOCKED / NOT RUN: no attested staging/VPS target, protected environment approval, deployment credentials, health target or rollback evidence.
- DOC-050 G7 RELEASE is separate from CI success. No G7 approval, release tag, merge or production deployment has occurred.

## Overall — 2026-11-08

- CI / exact-SHA validation: PASS.
- Product Auto E2E: PASS.
- Windows Browser Adapter + MCP Sub handoff/readback: PASS.
- Immutable source artifact checksum: PASS.
- Main integration: BLOCKED pending independent review of 80-file diff and clean integration strategy.
- Dashboard→Core: BLOCKED / NOT RUN.
- CD / staging / production: BLOCKED / NOT RUN.
- G7 RELEASE: NOT READY / NOT AUTHORIZED.
- Work 32: ACTIVE — NOT RELEASED.


## Latest exact-SHA checkpoint — 2026-11-08 / Run #232

- Current branch HEAD at checkpoint: `4dd07dbf4c30541c70bb91e8b053fe62d8b6290e` (`work/32-ci-runner-owned-fixture-v2`).
- Run #232 / `42459846727`: SUCCESS on exact cleanup SHA; 6/6 jobs PASS.
- Unit: 189 passed; Product Auto E2E: 68 passed; Windows Browser Adapter E2E: 10 passed; immutable artifact-level E2E: 1 passed; tooling mirror IN_SYNC; release acceptance CI gate PASS.
- Windows meeting `MEETING-W32-42459846727-1`; adapter PID 11160; dynamic port 58525; preflight PASS; MCP stdio handoff/readback PASS; cleanup PASS. Windows artifact ID `13609715124`, SHA-256 `3f15f641f1d81dfe3de0c11fb729378cd23c0984e6810d5e12664f4d252e6e30`.
- Product artifact ID `13609242768`; uploaded ZIP digest `5c84a98996c5cd653ad89b8bd0b89d0a841063bbc9cac76983e649f0f6c11aac`; extracted-artifact product test 1 passed.
- Removed 44 tracked Windows Explorer `desktop.ini` metadata files from this feature branch only; resulting tree verified zero remaining. Existing `.gitignore` rule retained. No test source files were deleted.
- Main comparison, Dashboard→Core and CD/G7 blockers remain unchanged; no main merge, release tag or deployment.
- Work32: CI ACCEPTANCE PASS; MAIN INTEGRATION BLOCKED; CD/G7 NOT READY; ACTIVE — NOT RELEASED.


## Latest exact-SHA checkpoint — 2026-11-08 / Run #234

- Branch SHA: `0fd12a94dcf598583e402cdb92352ee2f6596880`; GitHub Actions Run #234 / `42460406640`: SUCCESS, 6/6 jobs.
- Unit 189 passed; Product Auto E2E 68 passed; Windows Browser Adapter E2E 10 passed; immutable artifact E2E 1 passed; tooling workflow mirror IN_SYNC; CI release acceptance gate PASS.
- Windows disposable meeting `MEETING-W32-42460406640-1`; adapter PID 21468; dynamic port 58821; exact-SHA preflight, MCP stdio handoff/readback and cleanup PASS.
- Main compare: current main `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb`; diverged 251 ahead / 273 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`; 124 changed paths. No merge/rebase/cherry-pick.
- Work32 remains ACTIVE — NOT RELEASED; Dashboard→Core and CD remain BLOCKED / NOT RUN; DOC-050 G7 RELEASE NOT READY / NOT AUTHORIZED.


## Current authority acceptance checkpoint — 2026-11-13

- Current implementation branch: `work/32-main-integration-authority-20261112`; PR #52 remains open and unmerged.
- Latest source/workflow head with hosted CI evidence: `17ba50ab2e8736e2636e323741ce735c107fe197`.
- Latest documentation head: `98d58b912b53e70a33c4ec56abf9c8795e1055e4`; documentation-only manifest/journal/evidence updates are followed by a new exact-head run.
- Run #416 / 43357544278: unit 250 passed; Product Auto E2E 122 passed; hosted Windows Browser Adapter 10 passed; Work32 tooling PASS; immutable product artifact checksum/dependency/compile checks PASS and artifact E2E 1 passed.
- Dedicated runner identity ROOM-HOP-W32-PC / Windows X64: PASS.
- Live Core invalid-credential authority route: HTTP 404 instead of required 401/403.
- Live Host health: HTTP 200 but provider_type, authority and grant_cache fields are missing/blank.
- Runner service PATH: Python NOT_FOUND; Git 2.55.0.windows.3.
- Ports 8000/8031 are loopback listeners, but process owner/module remain unresolved and expected entrypoint match is false.
- DOC-124/DOC-125 and W32-LOG-117/118 record the source hardening and live runtime findings. W32-EVIDENCE-024/025 record exact evidence references.
- Main integration, CD, staging, production, G7 release and protected execution remain BLOCKED / NOT AUTHORIZED. No service restart or runtime configuration was performed.
- **Overall: HOSTED CI PASS; LIVE CORE/HOST RUNTIME BLOCKED; RELEASE NOT AUTHORIZED. Work32 ACTIVE — NOT RELEASED.**


## Current checkpoint — 2026-11-13 19:59 Asia/Ho_Chi_Minh

- Current PR #52 branch HEAD after workflow mirror remediation: `a4e62e5e8234a3d1cdf7688a6622752fe6f67148`.
- Run #430 / `43358168481` tested prior documentation head `e6d3ed5662ee93e4106d01066f6cacf1078edb03`: unit 250 PASS; Product Auto E2E 122 PASS; hosted Windows Browser Adapter 10 PASS; immutable artifact E2E 1 PASS; dedicated PC runner identity PASS.
- Run #430 live PC probe FAIL: Core invalid-credential route HTTP 404; Host health HTTP 200 but required identity fields blank; process owner/module unresolved; Python NOT_FOUND in runner service PATH. Release acceptance gate FAIL.
- Active workflow and Work32 mirror are now byte-identical (blob SHA `fd613c2e2ef2f54772133a46e8d5f593dc0c4b36`); strict checker mode `CHECK_STRICT=1` is enabled. Exact-head CI for current HEAD is pending.
- DOC-035 entry: W32-LOG-20261113-119. Evidence register: W32-EVIDENCE-026/027.
- ROOM-HOP Sandbox parity is not verified because MCP :8030 connection was unavailable during this continuation.
- Main, CD, staging, production and release remain untouched. PR #52 remains open/unmerged. Protected execution denied.
- **Overall: HOSTED/SOURCE LANES PASS ON RUN #430; LIVE CORE/HOST BLOCKED; MIRROR PARITY SOURCE PASS; CURRENT HEAD CI PENDING; WORK32 ACTIVE — NOT RELEASED.**


## Security remediation continuation — 2026-11-13

- PR #52 integration candidate remains open/unmerged on `work/32-main-integration-authority-20261112`.
- Ka created isolated remediation branch `work/32-main-integration-remediation-20261113` from candidate SHA `d639199159d2f2c72d0e706e1490d9afd0f20ac3`, per Xu's H0/H1 directive.
- Confirmed residual: granted pytest child process inherited operator HOME/profile/temp paths. Source patch now redirects these to a per-run isolated home and adds a regression test; W32-LOG-20261113-120 / W32-EVIDENCE-028.
- Exact-head tests and CI for the remediation branch have not yet run. Process-tree termination/output caps, Host request-origin protections, independent security review and live PC Core/Host identity remain open.
- Do not merge/rebase/cherry-pick, restart PC services, provision credentials, execute protected commands, deploy or release. Protected execution remains denied.


## H1 process containment continuation — 2026-11-13 20:07 Asia/Ho_Chi_Minh

- Remediation branch: `work/32-main-integration-remediation-20261113`; source base is PR #52 candidate SHA `d639199159d2f2c72d0e706e1490d9afd0f20ac3`.
- Per-run child environment isolation: committed with regression test (W32-LOG-120 / W32-EVIDENCE-028).
- Bounded stdout/stderr capture (1 MiB combined), POSIX process-session termination, Windows process-tree taskkill path, and fail-closed status mapping: committed with repository regressions (W32-LOG-121 / W32-EVIDENCE-029).
- Exact process helper blob `9f5eeddbbcb32152b19321ac59563e2729a3303c` passed isolated Linux smoke: py_compile PASS; output-flood and timeout-descendant tests 2/2 PASS. This does not certify Windows behavior or the full Work32 suite.
- Full repo exact-head CI, Windows runner validation, Host/Origin protections, transport peer authentication, live PC process provenance and independent Cla review remain pending.
- Keep protected execution DENIED. No PC services, main, merge, CD, staging, production or release changed.
