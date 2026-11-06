# Work 32 — CI/CD for ROOM-HOP (Python, no Docker)

- Document Number: W32-README-001
- Priority order: P1 — Work overview and current acceptance state
- Owner / final authority: Vinh
- Coordinator: Xu (AI-01)
- Execution owner: Ka — CSA / Architecture & Backend Owner (delegated)
- Sandbox Work ID: 32
- GitHub repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Canonical implementation branch: `work/32-ci-cd-python-ci-v2`
- Work documents: `work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/`

## Current status — 2026-11-04

- **CI:** PASS — GitHub Actions push / pull-request / manual-dispatch workflow operational.
- **Unit gate:** PASS — 157 deterministic Python 3.12 tests.
- **Core product Auto E2E:** PASS — 39 tests, including full live HTTP → MCP stdio → persistent transcript → close → final artifact → readback journey; 1 warning. **Immutable artifact E2E:** PASS — exact-SHA archive extracted and product E2E passed against the artifact. **Dashboard→Core browser E2E:** BLOCKED / NOT RUN because the separately maintained Dashboard still uses a mock bridge.
- **CD:** BLOCKED / NOT RUN — no attested staging/VPS target, protected deployment environment, deployment credentials, health-check target or tested rollback.
- **Release:** NOT RELEASED.
- **Overall:** ACTIVE — NOT RELEASED pending CD target evidence, branch governance and independent review.

## Exact validated evidence

- Final validated SHA: `e451764d4bc900a98f4d0b2d00a1e863ea86b22c`.
- Successful GitHub Actions run #68: `41723597131`.
- CI architecture/security hardening run #58: `41719864578` (SUCCESS, SHA-pinned workflow), SHA `4d70e2fce18982cfdd8c3487dee1d15c2ca51fd3`, SUCCESS; 157 unit passed and 38 E2E passed (1 warning).
- The workflow fetches the exact triggering SHA without submodule recursion, uses Python 3.12, read-only `contents: read`, bounded job timeouts, `pip check`, `compileall`, independent unit/E2E jobs, immutable source archive build + checksum verification, extracted-artifact product E2E, and 14-day evidence artifacts.
- GitHub Actions dependencies are pinned to audited commit SHAs; see `03_ARCHITECTURE/CICD_TARGET_ARCHITECTURE.md`.
- Full artifact digests and MCP contract evidence: `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.

## Scope / guardrails

No Docker requirement. No Core or live-service architecture change. No two-way Sandbox↔GitHub sync. No automatic merge, secrets mutation or production deploy. Vinh authorized Ka to implement and push Work 32 changes only to the dedicated feature branch and activate branch-scoped CI; that authorization does not authorize main merge or production release.

The Work branch is currently diverged from main (68 ahead / 32 behind at the latest comparison); no merge, rebase or cherry-pick has been performed. Independent Vibe review and safe branch reconciliation remain required before integration.


## Product-level evidence and boundary

- Full Core product journey evidence: `06_EVIDENCE/W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104.md`.
- Unit: 157 passed. Product Auto E2E: 39 passed, 1 warning.
- Dashboard source audit: `hqtt2026-thevinhvtqni/hqtt-Dashboard-note`, branch `hqtt-ai-project-structure-082c9`, HEAD `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`; `App.tsx` still selects `createMockBridge()`. UI-to-Core product integration is not claimed.
- Overall Work 32 remains ACTIVE — NOT RELEASED until Dashboard integration scope is resolved, independent review is complete, branch governance is reconciled, and CD gates are evidenced.


## Immutable product artifact

- Run #67 / `41723138912`: SUCCESS.
- Exact artifact source SHA: `0069157d24d6748cff69f162147b892242d9726f`.
- Source archive built from that SHA, checksum verified, extracted into a clean directory, dependencies checked, packages compiled and product E2E run against extracted artifact (1 passed).
- Artifact ID `13272918198`, uploaded artifact ZIP digest `fa059d00b74fe7e884c98ca95dc9ec283dcb940ffaa0b3b6eec4c25761a299f6`.
- This is a retained release-candidate artifact, not a staging/production deployment.


## Exact-SHA immutable artifact verification — PASS

- Final tested source SHA: `e451764d4bc900a98f4d0b2d00a1e863ea86b22c`; Actions run #68 `41723597131` SUCCESS.
- Unit: 157 passed; Product Auto E2E: 39 passed, 1 warning; extracted artifact E2E: 1 passed in 2.15s.
- Source archive SHA-256: `76d77939c43b33727a534cbccd06e4240eb106458659b9186f9fb125ca59f0ae`.
- Artifact ID `13271449355`; uploaded ZIP digest `9a688cc80b97e428a2d1b9c39a3c4bc97aa854e7b0715b64e8a7d39aa98c6062`.
- Retention: 14 days. Artifact is a release candidate, not deployed.


## Current checkpoint — 2026-11-06 (supersedes earlier status snapshots)

- Canonical implementation branch: `work/32-ci-cd-python-ci-v2`.
- Branch HEAD at checkpoint: `3dc65a4603823f58543f5216af2b0885df3a1627` (W32-LOG-78 audit commit).
- Latest completed full branch-head CI at this checkpoint: run #108 / `41953241351`, exact SHA `442ef9eb0623a610378433705d4baf5663e6ca2b`, SUCCESS 4/4 jobs. Run #109 / `42118931381` for the W32-LOG-78 documentation commit is IN PROGRESS; do not count it as PASS until it completes on its exact SHA.
- Main HEAD: `d7266eb9bfedfc534fc87d56548e47841bb583b9`; branch comparison: DIVERGED, 184 ahead / 35 behind, merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`, 74 changed files.
- Earlier snapshot (68 ahead / 32 behind; 157 unit / 39 E2E) is historical and must not be used as current status.
- PR #40 is an earlier pilot PR from `work/32-ci-cd-room-hop-python-no-docker`; it remains OPEN / DRAFT with no submitted review. It is not the current v2 implementation PR.
- Integration decision: no direct merge to main, no rebase/force-push and no merge of PR #40. Prepare a separately reviewed integration branch from current main and transplant only the approved Work 32 change set; run exact-SHA CI and open a fresh PR after independent review.
- Work 32 remains ACTIVE — NOT RELEASED. PC Windows runtime provenance, Dashboard→Core E2E, CD/staging and release remain separate unresolved gates.


## Verification update — 2026-11-06 (supersedes the earlier 3dc65a / run #109 checkpoint)

- Canonical implementation branch remains `work/32-ci-cd-python-ci-v2`.
- Current canonical branch HEAD verified from GitHub: `f5ea569c918d8ebfc94e52eab631cb514a198101`.
- Latest completed active-branch CI at this verification: run #115 / `42123995682`, exact SHA `f5ea569c918d8ebfc94e52eab631cb514a198101`, conclusion SUCCESS. All four jobs completed successfully: unit, tooling, Product Auto E2E, and immutable product artifact verification.
- Workflow mirror candidate `work/32-sync-workflow-mirror-20261106` was at `74fa891d72639a7d881811d2e17bd27f85a3fe6c` before the append-only journal update. It contained one workflow-mirror commit relative to canonical HEAD; the only implementation-path change was `04_CODE/ci-validation.yml`.
- On the mirror candidate, `04_CODE/ci-validation.yml` and root `.github/workflows/ci-validation.yml` are byte-identical (blob SHA `4787d5899250d9a903402e4c4b8f1247da902e61`). The root workflow blob is also identical on the canonical implementation branch. The canonical branch's older `04_CODE/ci-validation.yml` copy remains distinct; the mirror candidate is the branch carrying the proposed synchronization.
- No run on the mirror candidate is expected under the current push branch filters; CI is executed on the canonical implementation branch. Do not treat zero mirror-branch runs as a trigger failure.
- The append-only journal entry `W32-LOG-20261106-01` records the exact branch, blob and run evidence, including correction of the earlier premature trigger diagnosis.
- **Status:** workflow mirror synchronization PASS; canonical active-branch CI PASS (4/4 jobs); Work 32 remains ACTIVE — NOT RELEASED. No merge/rebase/cherry-pick, CD or production deployment is authorized by this verification.
- **Remaining gates:** independent review and safe integration strategy; Windows PC runtime provenance; Dashboard→Core product integration E2E; attested staging/CD target, health check and rollback.


## Main integration gate — 2026-11-06

- Current main HEAD: `d7266eb9bfedfc534fc87d56548e47841bb583b9`.
- Current canonical Work 32 branch HEAD: `f5ea569c918d8ebfc94e52eab631cb514a198101`.
- Main comparison: DIVERGED, 191 ahead / 35 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- Canonical branch protection is disabled and no required status checks are configured.
- PR #40 is the old pilot branch PR (OPEN / DRAFT), not the canonical v2 branch. No PR for the canonical v2 branch was found.
- **Integration gate: BLOCKED.** Do not merge/rebase the canonical branch directly or merge PR #40. The approved safe path is a separate integration branch from current main, minimal approved change-set transplant, exact-SHA CI and fresh independent-review PR.
- This gate does not invalidate the successful run #115; CI PASS and main-integration readiness are separate decisions.
- Detailed evidence: `W32-LOG-20261106-02` in `NHAT_KY_HOP_THI_CONG.md`.
