# Work 32 — Manifest

- Name: CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Owner/final authority: Vinh
- Coordinator: Xu (AI-01)
- Date: 2026-10-24, Asia/Ho_Chi_Minh
- Status: CORE PRODUCT AUTO E2E + IMMUTABLE ARTIFACT E2E PASS; DASHBOARD→CORE INTEGRATION AND CD BLOCKED; NOT RELEASED
- Sandbox ID: 32
- GitHub branch: work/32-ci-cd-room-hop-python-no-docker

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
