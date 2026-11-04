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
