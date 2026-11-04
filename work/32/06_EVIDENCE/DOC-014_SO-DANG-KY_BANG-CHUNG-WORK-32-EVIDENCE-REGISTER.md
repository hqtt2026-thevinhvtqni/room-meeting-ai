# SỔ ĐĂNG KÝ BẰNG CHỨNG WORK 32 / WORK 32 EVIDENCE REGISTER
- **STT / Document ID:** DOC-014
- **Priority:** P1
- **Read order:** 19
- **Depends on:** DOC-004; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.6 / 2026-11-04

| Evidence ID | Claim / scope | Source path | Exact source/version | Result / status |
|---|---|---|---|---|
| W32-EVIDENCE-001 | CI pilot historical results | Legacy 06_EVIDENCE/W32-EVIDENCE-001-CI-PILOT-RESULTS-20261103.md | Historical failed gate evidence retained | HISTORICAL |
| W32-EVIDENCE-002 | Auto E2E pipeline review | Legacy 06_EVIDENCE/W32-EVIDENCE-002-AUTO-E2E-PIPELINE-REVIEW-20261104.md | See source document | RECORDED |
| W32-EVIDENCE-003 | Auto E2E run evidence | Legacy 06_EVIDENCE/W32-EVIDENCE-003-AUTO-E2E-RUN-20261104.md | See source document | RECORDED |
| W32-EVIDENCE-004 | MCP public contract + stdio E2E | Legacy 06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md | See source document | PASS — scoped |
| W32-EVIDENCE-005 | Core product lifecycle Auto E2E | Legacy 06_EVIDENCE/W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104.md | See source document | PASS — Core scope |
| W32-EVIDENCE-006 | Immutable product artifact | Legacy 06_EVIDENCE/W32-EVIDENCE-006-PRODUCT-ARTIFACT-20261104.md | See source document | PASS — artifact scope |
| W32-EVIDENCE-007 | Final exact-SHA validation | Legacy 06_EVIDENCE/W32-EVIDENCE-007-FINAL-EXACT-SHA-20261104.md | Run #70 record; later exact SHA 021c8b842baf937e0ca06f8dcb44050f2741cc7e, Actions 41724493715 | PASS — Core CI/Product E2E/artifact |
| W32-EVIDENCE-008 | Dashboard integration gap audit | Legacy 06_EVIDENCE/W32-EVIDENCE-008-DASHBOARD-INTEGRATION-GAP-20261104.md | Dashboard source HEAD recorded in evidence | BLOCKED / NOT RUN |
| W32-EVIDENCE-009 | Workspace :8010 bounded source audit | Legacy 06_EVIDENCE/W32-EVIDENCE-009-WORKSPACE-8010-SOURCE-AUDIT-20261104.md | Bounded repository/source searches only | NOT PROVEN / BLOCKED |
| W32-EVIDENCE-010 | CTO classifier review and isolated tests | Legacy 06_EVIDENCE/W32-EVIDENCE-010-CTO-REVIEW-CLASSIFIER-RUN-20261104.md | Cla reports 15/15 classifier tests in isolated Python 3.12.3 unittest harness | PASS — classifier scope only; not CI evidence |
| W32-EVIDENCE-011 | CTO CI hardening source review | Legacy 06_EVIDENCE/W32-EVIDENCE-011-CTO-CI-HARDENING-SOURCE-20261104.md | See source document; readback not performed in this normalization pass | RECORDED — review findings only |
| W32-EVIDENCE-012 | CI hardening exact-SHA verification | 06_EVIDENCE/W32-EVIDENCE-012-CI-HARDENING-EXACT-SHA-20261104.md | Commit 2a406dabed6fc2ef7c19aa28c2469cf45ccc45bf; run 41758999218 | PASS — CI hardening scoped; five unaccounted tests remain report-only |
| W32-EVIDENCE-013 | CI dependency constraints + repeat exact-SHA validation | 06_EVIDENCE/W32-EVIDENCE-013-CI-DEPENDENCY-CONSTRAINTS-20261104.md | Commit c7dbe1ade37db4c787099a54560ee79868b8a380; run 41760926463 | PASS — 44-package constraints match observed freeze; all jobs pass |
| W32-EVIDENCE-014 | Coverage disposition and deterministic meeting suite promotion | 06_EVIDENCE/W32-EVIDENCE-014-COVERAGE-DISPOSITION-20261104.md | Commit 3cc8e6e945528c4acda631e9dd3e2f4e50bc983f; run 41762690300 | PASS — 167 unit tests; four remaining test files stay report-only |

## Exact-SHA run reference
- GitHub Actions run #71: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41724493715
- Source SHA: 021c8b842baf937e0ca06f8dcb44050f2741cc7e.
- Unit: 157 passed; Product Auto E2E: 39 passed, 1 warning; immutable artifact E2E: 1 passed.
- This does not prove Dashboard Browser E2E, independent QE, CD or release.
- Run #76 completed SUCCESS on SHA 519a79f97142b2c55d1b07931159888b6ef8e381 (run ID 41748162994); superseded by hardening run #2/#3.
- Latest CI Hardening run #3: run 41760926463 on exact SHA c7dbe1ade37db4c787099a54560ee79868b8a380; 157 unit, 20 tooling, 39 Product Auto E2E passed/1 warning, 1 immutable artifact E2E passed; 44-package constraints applied.
- Latest CI Hardening run #4: run 41762690300 on exact SHA 3cc8e6e945528c4acda631e9dd3e2f4e50bc983f; 167 unit, 20 tooling, 39 Product Auto E2E passed/1 warning, 1 immutable artifact E2E passed; unaccounted coverage reduced from five to four.

Evidence is immutable by reference. Corrections add a new evidence record; failed or superseded historical results are not overwritten.

| W32-EVIDENCE-016 | Track A hardening: isolated MCP integration + portable Work13 E2E | 06_EVIDENCE/DOC-060_W32-CI-HARDENING-ISOLATED-INTEGRATION-EXACT-SHA-20261104.md | Exact SHA c3079bbb73edc84b2e05c2767cf9bb135a754e42; run 41786170213 | PASS — 4/4 jobs; 45 E2E; coverage report-only with two findings |

| W32-EVIDENCE-017 | Retired draft workflow cleanup + exact-SHA CI run #17 | 06_EVIDENCE/DOC-061_W32-CI-DRAFT-CLEANUP-EXACT-SHA-RUN17-20261104.md | Exact SHA d0906794dfb348565389ca54ad328f0cf67f1ac2; run 41786820432 | PASS — 4/4 jobs; 45 Product Auto E2E; two report-only tests remain |


| W32-EVIDENCE-018 | Browser Adapter :8787 endpoint/test contract + exact-SHA run #18 | 06_EVIDENCE/DOC-062_W32-BROWSER-ADAPTER-8787-AND-RUN18-20261104.md | Exact SHA 450c0b2409c0d19c68931cb0331652bac6f3b5df; run 41787301060 | CI 4/4 PASS; browser test NOT RUN; F4 NOT RUN; strict remains unauthorized |


| W32-EVIDENCE-019 | F4 source audit and PC-access deferral disposition | 06_EVIDENCE/DOC-063_W32-F4-RESOURCE-LIMITS-SOURCE-AUDIT-20261104.md | Exact audited SHA 450c0b2409c0d19c68931cb0331652bac6f3b5df; source blob SHAs recorded in DOC-063 | SOURCE AUDIT COMPLETE; F4 NOT PASS; browser E2E DEFERRED |

| W32-EVIDENCE-020 | Vibe independent CI action-SHA audit (false-positive clearance + P1 consolidation proposal) | CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/06_EVIDENCE/W32-EVIDENCE-010-CI-ACTION-SHA-INDEPENDENT-AUDIT-20261104.md (legacy path); legacy journal W32-LOG-14, commit cb7fdb13af94732468c291d6768137db3b4c549b | setup-python@a26af69 (v5.6.0) and upload-artifact@ea165f8d (v4.6.2) verified correct in both workflows | FALSE POSITIVE CLEARED; consolidation proposal later APPROVED in W32-LOG-38. NOTE: legacy filename reuses ID-010; canonical register ID-010 remains the CTO classifier record. New records must not reuse existing IDs |

| W32-EVIDENCE-021 | Vibe independent verification of runs #23/#24 and F4 source audit | 00_ROOT/DOC-035 W32-LOG-20261104-37, commit e279ca918ffbe27d149b8a0f174f1e80f268361a | Runs 41788992658 (64575ef4) and 41789201999 (b92e9150) SUCCESS 4/4; F4 findings reproduced at 450c0b2 | VERIFIED; ACCEPTED by Xu in W32-LOG-38 |

| W32-EVIDENCE-022 | Documentation-only exact-SHA CI runs #25/#26 | GitHub Actions run #25 41789850424 (e279ca918ffbe27d149b8a0f174f1e80f268361a); run #26 on 14cb29a5228abe9b9195f2bee44c96b92f5c2a32 | Docs-only commits on work/32-ci-cd-python-ci-v2; product source unchanged since 450c0b2409c0d19c68931cb0331652bac6f3b5df | PASS — 4/4 jobs each; no source/workflow/test claim |

| W32-EVIDENCE-023 | CI warning disposition: Node.js 20 deprecation + Starlette/httpx warning | 00_ROOT/DOC-035 W32-LOG-20261104-39 | Pinned stack: starlette==1.10.0, httpx==0.28.1, fastapi==0.162.0; actions setup-python@v5.6.0, upload-artifact@v4.6.2 | ANALYSIS RECORDED; no pin/dependency change; Starlette/httpx root cause NOT CONFIRMED pending raw-log review |

- 2026-11-04 addendum (Vibe, per Vinh delegation recorded in W32-LOG-39): registered W32-EVIDENCE-020 through 023; no historical row was edited or removed. Evidence is immutable by reference; corrections add new records only.


| W32-EVIDENCE-024 | Run #27 exact-SHA hosted CI and raw warning trace | GitHub Actions run 41802775140, SHA 14d0257b90e8a5c886268aa941123e96b455641d; raw E2E job 126482333884; W32-LOG-40 | 4/4 jobs PASS; Unit 167; Product E2E 45 passed/1 Starlette warning; tooling PASS; immutable artifact E2E 1 PASS; artifact ID 13307834500 digest sha256:ae916dd53a4edb474aba0aa9b4c2982b0020e3541f64ea6e04d4104ddf3db8ed | VERIFIED; Starlette warning source confirmed at fastapi/testclient.py:1; no dependency/action pin changes |


| W32-EVIDENCE-021 | F4 Option A implementation and exact-SHA CI validation | DOC-065; source files core/paste_rate_limiter.py, core/secretary.py, core/meeting_manager.py, MCP/HTTP adapters; Actions run 41805684024 | Exact SHA c7359d4cb5eae62992129dd1a3615652ce93680e; unit 189 passed; Product Auto E2E 45 passed; tooling 20 OK; immutable artifact E2E 1 passed | PASS — 100 accepted requests / resolved identity / meeting / rolling 60 seconds; same-host SQLite atomic store; multi-host not certified |


| W32-EVIDENCE-022 | Node.js 24 Actions runtime pin update and exact-SHA verification | DOC-066; `.github/workflows/ci-validation.yml` | Exact SHA 7984d167a1eec935f062dd17894d89ff90503619; Actions run 41806199038; 4/4 jobs SUCCESS; raw logs: zero Node.js 20 deprecation warnings | PASS — setup-python v7.1.0 and upload-artifact v7.0.1 pinned by immutable commit SHA; Starlette warning remains separate |
