# DANG KY ANH XA BUILD / BUILD MAPPING REGISTER
- Document ID: DOC-036
- Priority: P1
- Read order: 18
- Depends on: DOC-001, DOC-003, DOC-033, DOC-011
- Status: ACTIVE — LEGACY CLASSIFICATION IN PROGRESS
- Version: 1.5 / 2026-11-04

05_BUILD is a mapping and engineering coordination layer, not a canonical source-code or original-document store.

| Mapping | Artifact | Canonical source | Version | Sandbox location | Classification |
|---|---|---|---|---|---|
| MAP-32-001 | Core source | GitHub hqtt2026-thevinhvtqni/room-meeting-ai, branch work/32-ci-cd-python-ci-v2 | Verified HEAD c3079bbb73edc84b2e05c2767cf9bb135a754e42 | No canonical copy in Sandbox | GITHUB SOURCE / HEAD RECHECK |
| MAP-32-002 | Active CI hardening workflow | Same repository, .github/workflows/ci-validation.yml | Blob SHA 48c3a649e31f97285530fdedf730718ace5622a9 at commit c3079bbb73edc84b2e05c2767cf9bb135a754e42 | Sandbox .github/workflows/ci-validation.yml; Work mirror CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/ci-validation.yml | VERIFIED — exact blob match |
| MAP-32-003 | Product E2E working copy | Same repository, tests/test_ci_product_e2e.py | Blob SHA not refreshed | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/tests/test_ci_product_e2e.py | TEMPORARY |
| MAP-32-004 | Legacy mixed Work tree | Sandbox Work 32 | Historical mixed tree | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/ | LEGACY / CLASSIFICATION IN PROGRESS |
| MAP-32-005 | Governance records | Sandbox Work 32 root | DOC-ID and version in DOC-055 | 00_ROOT and lifecycle folders | CANONICAL IN SANDBOX |
| MAP-32-006 | CI helper package | Same repository, work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/ci_tools/__init__.py | Blob SHA 561fb264f439513a72ebc37902544981e1c548d0 | Sandbox CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/ci_tools/__init__.py | VERIFIED — exact branch path |
| MAP-32-007 | Coverage checker | Same repository, work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/ci_tools/check_test_coverage.py | Blob SHA 80c750e42cdc93635c8632a1fae228278166ac19 | Sandbox CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/ci_tools/check_test_coverage.py | VERIFIED — exact branch path |
| MAP-32-008 | Coverage checker tests | Same repository, work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/05_TEST/test_check_test_coverage.py | Blob SHA ea7f6794ad0e906f70c3a4ff34eede8d76c72408 | Sandbox CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/05_TEST/test_check_test_coverage.py | VERIFIED — exact branch path |
| MAP-32-009 | Classifier source/test | Same repository, work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/python_test_runtime/result_classifier.py and 05_TEST/test_result_classifier.py | Blob SHAs 6e79ac7eda83a3f48fc744c02fecf862cc11e341 / 94d4e2a4eb34ddd8b3ba09fd26c394f57078225f | Existing Sandbox classifier source/test | VERIFIED — present on same branch and exercised by tooling gate |
| MAP-32-010 | CI dependency constraints | Same repository, constraints-ci.txt | Blob SHA 8f30ded0ff6a6e4ffdc8d690c494de161e7e2ab8 at commit c7dbe1ade37db4c787099a54560ee79868b8a380 | Sandbox constraints-ci.txt | VERIFIED — 44 pins from observed pip freeze; exact readback PASS |
| MAP-32-011 | Deterministic meeting lifecycle unit suite | Same repository, tests/test_meeting.py | Blob SHA 9054233f0f1589de0089bbdeb9aeea7184ab2ee0 | GitHub canonical test source; no separate Sandbox mirror | VERIFIED — 10 tests pass in exact-SHA CI run #4 |
| MAP-32-012 | Isolated MCP integration E2E | Same repository, tests/test_integration.py | Blob SHA e76cc63002f4b45008f5115a325eb7481b7611b0 | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/tests/test_integration.py | SOURCE UPDATED — exact-SHA CI run pending |
| MAP-32-013 | Portable Work13 WEE E2E | Same repository, tests/test_work13_wee_integration.py | Blob SHA 302895a8f78711b5b052724d004c7876783fe617 | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/04_CODE/tests/test_work13_wee_integration.py | SOURCE UPDATED — exact-SHA CI run pending |
| MAP-32-014 | Duplicate CI Pilot workflow | `.github/workflows/ci.yml` | Deleted on authorized branch after trigger audit; commit includes deletion | No Sandbox mirror retained | RETIRED — replaced by ci-validation.yml |

Byte-for-byte Sandbox↔GitHub readback is PASS for active workflow MAP-32-002 at commit 3cc8e6e945528c4acda631e9dd3e2f4e50bc983f, and for MAP-32-006 through MAP-32-008 plus MAP-32-010 (unchanged blobs from commit c7dbe1ade37db4c787099a54560ee79868b8a380). Other mappings remain subject to their own exact-file verification. Preserve all legacy files. Physical moves or deletes require a separate approved migration plan.

## 2026-11-04 — W32 TRACK A MIRROR UPDATE
- Current authorized branch HEAD: `c3079bbb73edc84b2e05c2767cf9bb135a754e42`.
- Active workflow blob: `48c3a649e31f97285530fdedf730718ace5622a9`; report-only coverage retained; `CHECK_STRICT=1` absent.
- MCP integration tests use test-owned temporary meeting directories and no longer read `meetings[0]` from persistent repository state.
- Work13 E2E uses `sys.executable`, removing the Ubuntu-incompatible `python.exe` literal.
- Both suites are included in `E2E_TESTS`; duplicate `.github/workflows/ci.yml` retired after confirming active workflow retains push, pull_request-to-main and workflow_dispatch triggers.
- Exact-SHA Actions verification is pending; no test PASS is claimed from source edits alone.


## 2026-11-04 — W32-LOG-34/35 reconciliation (Xu)
- Current branch HEAD at journal sync: `450c0b2409c0d19c68931cb0331652bac6f3b5df`; run #18 / `41787301060` SUCCESS, 4/4 jobs.
- Source changes after run #17 are not asserted here; run #18 is the exact-SHA validation reference.
- Browser Adapter :8787 test: DEFERRED — WAITING FOR PC ACCESS; same-host loopback execution is required. Port-open report and active meeting read do not establish adapter health or E2E PASS.
- F4 audit: 1 MiB UTF-8 runtime byte guard exists; MCP schema maxLength is missing; rate-limit constant 100 is declared but not enforced. F4 remains BLOCKED pending explicit policy decision.
- Current CI status: 167 unit PASS; 20 tooling PASS; 45 Product Auto E2E PASS / 1 warning; immutable artifact E2E 1 PASS. Two tests remain report-only; strict coverage unauthorized.
- Branch governance remains DIVERGED (94 ahead / 35 behind main at current read); no merge/rebase/cherry-pick authorized.
- Preserve all historical mappings and files. This addendum supersedes stale HEAD/test status above without rewriting historical evidence.

## 2026-11-04 — W32-LOG-39 mapping addendum (Vibe, per Vinh delegation)
- Branch HEAD at this addendum: `14cb29a5228abe9b9195f2bee44c96b92f5c2a32` (docs-only commits after 450c0b2409c0d19c68931cb0331652bac6f3b5df; commits 64575ef4 / b92e9150 / e279ca91 / 14cb29a5 are journal/evidence/documentation changes only).
- MAP-32-002 remains VALID: `.github/workflows/` contains exactly one file, `ci-validation.yml`; no workflow changes since commit c3079bbb73edc84b2e05c2767cf9bb135a754e42 (blob 48c3a649e31f97285530fdedf730718ace5622a9 per MAP-32-002); retired `ci.yml` is not restored.
- MAP-32-010 remains VALID at HEAD: constraints-ci.txt unchanged (44 pins; starlette==1.10.0, httpx==0.28.1, fastapi==0.162.0 among them), matching pip-freeze evidence of runs #2/#3.
- No physical moves or deletions performed in this addendum. All historical mappings preserved.


## 2026-11-04 — Xu current-state addendum after Vibe W32-LOG-39
- Current verified branch HEAD before this addendum: `14d0257b90e8a5c886268aa941123e96b455641d`; run #27 / `41802775140` completed SUCCESS, 4/4 jobs on that exact SHA.
- DOC-014 includes W32-EVIDENCE-020 through 024; W32-LOG-40 records raw run #27 log verification and the corrected Starlette warning root cause.
- Workflow mapping remains one canonical `.github/workflows/ci-validation.yml`; 44 dependency pins remain unchanged. No action or Python dependency was upgraded.
- Branch divergence current at this check: 103 ahead / 35 behind main; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`. No reconciliation mutation authorized.
- Historical mappings remain intact; this addendum does not claim full tree sync or whole-product acceptance.


## 2026-11-04 — W32-LOG-41 F4 implementation source mapping
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P0 — Core resource protection
- `core/paste_rate_limiter.py`: new SQLite same-host atomic rolling-window store; source SHA and CI outcome pending exact-SHA verification.
- `core/secretary.py`: central UTF-8 byte validation; existing 1 MiB behavior retained.
- `core/meeting_manager.py`: Core paste admission after active/text/identity validation; commit quota only after successful transcript append; domain rate-limit error carries retry seconds.
- `room_hop_mcp/adapter/server.py`: MCP text schema maxLength=1,048,576; runtime byte guard remains authoritative.
- `room_hop_mcp/adapter/http_server.py`: optional identity propagation; rate rejection maps to HTTP 429 and Retry-After.
- `tests/test_f4_resource_limits.py`: F4 policy, atomic concurrency, scope isolation, rolling expiry, persistence, rollback and HTTP/Core tests.
- `.github/workflows/ci-validation.yml`: dedicated F4 test module included in bounded unit gate; strict coverage remains disabled.
- SQLite scope is same-host local filesystem only; no multi-host claim or deployment authorization.


## 2026-11-04 — W32-LOG-43 exact-SHA F4 mapping and verification
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P0 — F4 resource protection
- Current branch HEAD `c7359d4cb5eae62992129dd1a3615652ce93680e`; Actions run #34 / `41805684024` SUCCESS, 4/4 jobs.
- Source blob SHAs: `core/paste_rate_limiter.py` `db95a2f910bb755bcbca7ea873c022fb1bb30853`; `core/secretary.py` `1e3a2eb2228b4c778429f1e3dad78cacaacf04d9`; `core/meeting_manager.py` `64f075f4c22ed08bb82e97d97878beed45678212`; `room_hop_mcp/adapter/server.py` `b740f72b95ea3a6e0a7e1d19a3ef3275b9899815`; `room_hop_mcp/adapter/http_server.py` `f17d752f6badf2b600f78906e63982d18f70e859`; `tests/test_f4_resource_limits.py` `1a1d85573fadb3f84dae12bb0ae5b5d9d760ef15`; workflow `379e70a397afbd03a74e6c22768a73e9e89e79a6`.
- Unit 189 passed; Product Auto E2E 45 passed; tooling 20 OK; immutable artifact E2E 1 passed. See DOC-014 W32-EVIDENCE-021 and DOC-065.
- Same-host SQLite scope and identity-authentication caveat are explicitly retained. No multi-host or release claim.


## 2026-11-04 — W32-LOG-44 Node 24 action mapping
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P1 — CI runtime compatibility
- `.github/workflows/ci-validation.yml`: setup-python v7.1.0 pinned to `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`; upload-artifact v7.0.1 pinned to `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`. Both exact action.yml files declare node24.
- Workflow blob SHA and exact-SHA Actions result pending validation.
- No dependency, test, trigger, permission, artifact-retention or product source change in this action-only patch.


## 2026-11-04 — W32-LOG-45 Node 24 Actions exact-SHA mapping
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P1 — CI runtime compatibility
- Workflow blob SHA: `5cf513349e953a9991c5856496702597a45a110c`.
- Exact-SHA run #36 / `41806199038` at `7984d167a1eec935f062dd17894d89ff90503619`: 4/4 SUCCESS; 189 unit, 45 Product Auto E2E, 20 tooling, artifact E2E 1 passed.
- Raw logs across all four jobs: zero Node.js 20 Actions deprecation warnings. Node runtime remediation PASS. Starlette/httpx warning remains independent.


## 2026-11-04 — W32-LOG-46 httpx2 dependency mapping
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P1 — Test runtime compatibility
- `requirements.txt`: add `httpx2>=2.16.0`; retain `httpx>=0.27.0`.
- `constraints-ci.txt`: add `httpx2==2.16.0`; retain `httpx==0.28.1`.
- No FastAPI/Starlette upgrade. Exact-SHA validation and transitive pip-freeze inspection pending.


## 2026-11-04 — W32-LOG-47 httpx2 dependency provenance
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P1 — Dependency reproducibility
- Run #38 / `41806667551` at exact SHA `0065dbe54eff7282d6eec8eb56f104927ba1e9c4`: 4/4 SUCCESS; 189 unit, 45 Product Auto E2E, 20 tooling, artifact E2E 1 passed.
- Raw unit/E2E logs: zero StarletteDeprecationWarning and zero Node.js 20 Actions warnings.
- Observed transitive packages: `httpcore2==2.16.0`, `truststore==0.10.5`; pin both in constraints-ci.txt. Exact updated constraints SHA and validation run pending.


## 2026-11-04 — W32-LOG-48 Starlette/httpx2 exact-SHA mapping
- **Name:** Ka
- **Title:** CSA / Backend execution owner delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Priority Order:** P1 — CI dependency compatibility
- `requirements.txt` blob SHA `f82b95fb1e6fe695e3f0409d78e19f4255dba8b1`; `constraints-ci.txt` blob SHA `a43c0404408b4a0d2e5406d3e8d3c25ff7c78593`.
- Direct and transitive pins: httpx2 2.16.0; httpcore2 2.16.0; truststore 0.10.5. Existing httpx 0.28.1 retained.
- Exact-SHA run #39 / `41806906885`, SHA `17d7d87c9e09b08026fd8bdda29578c04bd1aa35`: 4/4 SUCCESS; unit 189, Product Auto E2E 45, tooling 20, artifact E2E 1 passed.
- pip check passed; raw unit/E2E logs show zero StarletteDeprecationWarning and zero Node.js 20 Actions warnings.
