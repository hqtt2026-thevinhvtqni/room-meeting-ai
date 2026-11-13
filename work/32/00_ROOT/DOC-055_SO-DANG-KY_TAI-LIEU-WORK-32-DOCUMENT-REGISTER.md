# SỔ ĐĂNG KÝ TÀI LIỆU WORK 32 / WORK 32 DOCUMENT REGISTER
- **STT / Document ID:** DOC-055
- **Priority:** P0
- **Read order:** 11
- **Depends on:** DOC-001; DOC-002; DOC-003; DOC-033; DOC-038; DOC-039; DOC-040
- **Status:** ACTIVE — SINGLE SOURCE OF TRUTH
- **Version / Updated:** 1.7 / 2026-11-04
- **Owner:** Xu / AI-01
- **Authority:** Vinh

Rule: DOC-ID is stable identity; Priority is importance; Read order is sequence. Every controlled document has one canonical path. Legacy files remain mapped and preserved until controlled migration.

| DOC-ID | Priority | Read order | Canonical document | Canonical path / reference | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-001 | P0 | 1 | Work Manifest | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | NONE | ACTIVE |
| DOC-002 | P0 | 2 | AI Intake & Execution Standard adoption | 00_ROOT/DOC-002_TIEU-CHUAN-TIEP-NHAN_VA-THUC-THI_AI-PROJECT-INTAKE-AND-EXECUTION.md | DOC-001 | ACTIVE |
| DOC-003 | P0 | 3 | Repository Layout & Sync Contract | 00_ROOT/DOC-003_CAU-TRUC-KHO_VA-HOP-DONG-DONG-BO_REPOSITORY-LAYOUT-AND-SYNC.md | DOC-001 | ACTIVE |
| DOC-004 | P0 | 4 | Lifecycle Gate Matrix | 00_ROOT/DOC-004_MA-TRAN-CONG_VONG-DOI-WORK-LIFECYCLE-GATE-MATRIX.md | DOC-001 | ACTIVE |
| DOC-005 | P0 | 5 | Work State Machine | 00_ROOT/DOC-005_MAY-TRANG-THAI_VONG-DOI-WORK-STATE-MACHINE.md | DOC-004 | ACTIVE |
| DOC-006 | P0 | 6 | Work 32 Decision Log | 00_ROOT/DOC-006_SO-QUYET-DINH_WORK-32-DECISION-LOG.md | DOC-001 | ACTIVE |
| DOC-033 | P0 | 7 | Documentation & Storage Standard adoption | 00_ROOT/DOC-033_TIEU-CHUAN-TAI-LIEU_VA-LUU-TRU_WORK-DOCUMENTATION-AND-STORAGE.md | DOC-001; DOC-002; DOC-003 | ACTIVE |
| DOC-038 | P0 | 8 | Shared Document Naming Standard | Work 70 DOC-038 v1.2 | DOC-001; DOC-033 | ADOPTED BY REFERENCE |
| DOC-039 | P0 | 9 | Shared Document Type Code Standard | Work 70 DOC-039 v1.2 | DOC-006; DOC-033; DOC-038 | ADOPTED BY REFERENCE |
| DOC-040 | P0 | 10 | Shared Official Document Code Register | Work 70 DOC-040 v1.4; no W32 operational codes issued | DOC-039 | ADOPTED BY REFERENCE |
| DOC-055 | P0 | 11 | Work 32 Document Register | 00_ROOT/DOC-055_SO-DANG-KY_TAI-LIEU-WORK-32-DOCUMENT-REGISTER.md | DOC-001; DOC-033 | ACTIVE |
| DOC-034 | P1 | 12 | Work 32 Minutes | 00_ROOT/DOC-034_BIEN-BAN_BIEN-BAN-WORK-32-MINUTES.md | DOC-001; DOC-006; DOC-033 | ACTIVE |
| DOC-035 | P1 | 13 | Work 32 Execution Log | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_NHAT-KY-WORK-32-EXECUTION-LOG.md | DOC-001; DOC-002; DOC-033 | ACTIVE |
| DOC-007 | P1 | 14 | Discover Brief | 01_DISCOVER/DOC-007_TOM-TAT_KHAM-PHA-WORK-32-DISCOVER-BRIEF.md | DOC-001 | ACTIVE |
| DOC-008 | P1 | 15 | Product Requirements | 02_DEFINE/DOC-008_YEU-CAU_SAN-PHAM_WORK-32-PRODUCT-REQUIREMENTS.md | DOC-007 | ACTIVE |
| DOC-009 | P1 | 16 | Architecture | 03_ARCHITECT/DOC-009_KIEN-TRUC_CI-CD-AND-PRODUCT-AUTO-E2E-ARCHITECTURE.md | DOC-004; DOC-006 | ACTIVE |
| DOC-011 | P1 | 17 | Implementation Roadmap | 04_PLAN/DOC-011_KE-HOACH-TRIEN-KHAI_WORK-32-IMPLEMENTATION-ROADMAP.md | DOC-004; DOC-009 | ACTIVE |
| DOC-036 | P1 | 18 | Build Mapping Register | 05_BUILD/DOC-036_DANG-KY-ANH-XA_BUILD-MAPPING-REGISTER.md | DOC-001; DOC-003; DOC-033; DOC-011 | ACTIVE / MIGRATION IN PROGRESS |
| DOC-014 | P1 | 19 | Evidence Register | 06_EVIDENCE/DOC-014_SO-DANG-KY_BANG-CHUNG-WORK-32-EVIDENCE-REGISTER.md | DOC-004; DOC-033 | ACTIVE |
| DOC-015 | P1 | 20 | Verification Plan | 06_VERIFY/DOC-015_KE-HOACH_KIEM-CHUNG-WORK-32-VERIFICATION-PLAN.md | DOC-009; DOC-011; DOC-014 | ACTIVE |
| DOC-020 | P2 | 21 | Acceptance Record | 07_ACCEPT/DOC-020_BIEN-BAN_NGHIEM-THU-WORK-32-ACCEPTANCE-RECORD.md | DOC-015 | NOT READY |
| DOC-021 | P2 | 22 | Release Plan | 08_RELEASE/DOC-021_KE-HOACH_PHAT-HANH-WORK-32-RELEASE-PLAN.md | DOC-020 | BLOCKED |
| DOC-032 | P2 | 23 | Dashboard Status Projection | DASHBOARD/DOC-032_BANG-TRANG-THAI_DASHBOARD-STATUS-PROJECTION.md | DOC-001; DOC-004; DOC-005; DOC-014 | ACTIVE |
| DOC-037 | P2 | 24 | Work 32 Overview | 00_ROOT/DOC-037_GIOI-THIEU_WORK-32-README.md | DOC-001; DOC-033; DOC-055 | ACTIVE |

## Legacy artifact mapping — preserve in place
| Legacy path under CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/ | Canonical mapping / role | Migration status |
|---|---|---|
| 00_ROOT/WORK_MANIFEST.md | Historical manifest snapshot; DOC-001 is current canonical | LEGACY — preserve |
| 00_ROOT/STRUCTURE_POLICY.md | Historical structure policy; superseded by DOC-001/DOC-003/DOC-033 | LEGACY — preserve |
| README.md | Legacy entry point; DOC-037 is current canonical | LEGACY — preserve |
| BIEN_BAN.md | Historical decision/minutes source; DOC-006/DOC-034 index it | LEGACY — preserve |
| NHAT_KY_HOP_THI_CONG.md | Historical detailed log; DOC-035 is current canonical Work-wide log | LEGACY — preserve |
| KE_HOACH_THI_CONG_XU.md | Historical plan; reconcile into DOC-011 | LEGACY — preserve |
| 03_ARCHITECTURE/CICD_TARGET_ARCHITECTURE.md | Technical source candidate mapped by DOC-009 | LEGACY / CANONICAL CANDIDATE |
| 05_TEST/ACCEPTANCE_PLAN.md | Verification source candidate mapped by DOC-015 | LEGACY / CANONICAL CANDIDATE |
| 02_EXTENSION/W32-REQ-001-XU-ARCHITECTURE-DECISION-REQUEST.md | Open architecture decision request | ACTIVE — NOT APPROVED |
| 06_EVIDENCE/W32-EVIDENCE-001…011 | Historical evidence artifacts; cross-phase index is DOC-014 | PRESERVE / READBACK STATUS PER REGISTER |
| 04_CODE/* and .github/workflows/* | Working copies until exact GitHub mapping | TEMPORARY / VERSION MAPPING REQUIRED |

## Reading rule
Read DOC-001 through DOC-006; then DOC-033 and shared DOC-038/039/040 references; then this register; then relevant P1 records by read order. Read P2 only for acceptance/release work. File presence is not evidence of implementation or PASS.


## Controlled legacy aliases and duplicate candidates
- `05_BUILD/BUILD_MAPPING_REGISTER.md` — legacy/unprefixed duplicate; canonical register is DOC-036. Preserve until controlled cleanup.
- `05_BUILD/DOC-036_DANG-KY-ANH-XA_DANG-KY-BUILD-MAPPING-BUILD-MAPPING-REGISTER.md` — duplicate DOC-036 candidate created during interrupted write attempt; not canonical. Preserve and classify; do not silently delete.
- `DASHBOARD/README.md` — compatibility overview; canonical status projection is DOC-032.
- `CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/06_EVIDENCE/W32-EVIDENCE-010-CTO-REVIEW-CLASSIFIER-RUN-20261104.md` and `W32-EVIDENCE-011-CTO-CI-HARDENING-SOURCE-20261104.md` are present in the Sandbox inventory and are indexed by DOC-014. Readback of their contents remains separate from inventory confirmation.
- `06_EVIDENCE/W32-EVIDENCE-012-CI-HARDENING-EXACT-SHA-20261104.md` — canonical exact-SHA CI hardening verification, run #2, commit 2a406dabed6fc2ef7c19aa28c2469cf45ccc45bf; indexed by DOC-014.
- `06_EVIDENCE/W32-EVIDENCE-013-CI-DEPENDENCY-CONSTRAINTS-20261104.md` — 44-package constraints provenance and repeat exact-SHA run #3, commit c7dbe1ade37db4c787099a54560ee79868b8a380; indexed by DOC-014.
- `06_EVIDENCE/W32-EVIDENCE-014-COVERAGE-DISPOSITION-20261104.md` — five-file source classification, deterministic meeting suite promotion and exact-SHA run #4, commit 3cc8e6e945528c4acda631e9dd3e2f4e50bc983f; indexed by DOC-014.

## Verification checkpoint
Sandbox root inventory confirms the lifecycle folders and the preserved legacy tree. Readback status OK for DOC-001, DOC-034, DOC-035, DOC-009, DOC-014, DOC-020 and DOC-036. Other newly created records are present in the inventory; full content readback remains pending. No GitHub documentation sync has been performed.


## Additional canonical lifecycle record
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-022 | P3 | 25 | Operations Model | 09_OPERATE/DOC-022_MO-HINH_VAN-HANH-WORK-32-OPERATIONS-MODEL.md | DOC-020; DOC-021 | NOT STARTED |

Compatibility aliases retained with DOC metadata:
- `05_BUILD/BUILD_MAPPING_REGISTER.md` → DOC-036 canonical path.
- `05_BUILD/DOC-036_DANG-KY-ANH-XA_DANG-KY-BUILD-MAPPING-BUILD-MAPPING-REGISTER.md` → preserved duplicate pointer; not canonical.
- `DASHBOARD/README.md` → DOC-032 canonical path.
- `09_OPERATE/README.md` → DOC-022 canonical path.


## Additional canonical execution evidence
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-060 | P0 | 26 | W32 CI Hardening — Isolated Integration + Portable Work13 E2E | 06_EVIDENCE/DOC-060_W32-CI-HARDENING-ISOLATED-INTEGRATION-EXACT-SHA-20261104.md | DOC-014; DOC-035; DOC-036 | PASS — exact-SHA run #16; Work 32 ACTIVE — NOT RELEASED |

| DOC-061 | P0 | 27 | W32 CI Hardening — Draft Cleanup + Exact-SHA Run #17 | 06_EVIDENCE/DOC-061_W32-CI-DRAFT-CLEANUP-EXACT-SHA-RUN17-20261104.md | DOC-014; DOC-035; DOC-036 | PASS — run #17; Work 32 ACTIVE — NOT RELEASED |


| DOC-062 | P0 | 28 | Browser Adapter :8787 recheck + exact-SHA run #18 | 06_EVIDENCE/DOC-062_W32-BROWSER-ADAPTER-8787-AND-RUN18-20261104.md | DOC-014; DOC-035; DOC-036 | Hosted CI PASS; browser adapter E2E NOT VERIFIED; F4 BLOCKED |


| DOC-063 | P0 | 29 | F4 resource limits source audit and implementation disposition | 06_EVIDENCE/DOC-063_W32-F4-RESOURCE-LIMITS-SOURCE-AUDIT-20261104.md | DOC-056; DOC-062 | F4.1 source present; F4.3 schema gap; F4.4 rate enforcement absent; BLOCKED pending policy |


| DOC-064 | P1 | 30 | CI Warning Disposition — Node.js 20 Actions Runtime and Starlette/httpx | 06_EVIDENCE/DOC-064_W32-CI-WARNING-DISPOSITION-20261104.md | DOC-014; DOC-035; DOC-036 | PASS — Node.js warning run #36; Starlette/httpx warning run #39 |


| DOC-065 | P0 | 31 | F4 Rate Limit Decision and Implementation Record | 06_EVIDENCE/DOC-065_W32-F4-RATE-LIMIT-DECISION-AND-IMPLEMENTATION-20261104.md | DOC-063; DOC-035; DOC-014 | PASS — exact-SHA run #34; same-host SQLite; multi-host not certified |


| DOC-066 | P1 | 32 | Node.js 24 GitHub Actions Pin Update | 06_EVIDENCE/DOC-066_W32-NODE24-ACTIONS-PIN-UPDATE-20261104.md | DOC-035; DOC-036; CI workflow | PASS — run #36; zero Node.js 20 warnings |


| DOC-067 | P1 | 33 | Starlette TestClient httpx2 Compatibility Update | 06_EVIDENCE/DOC-067_W32-STARLETTE-HTTPX2-COMPATIBILITY-UPDATE-20261104.md | DOC-064; DOC-035; DOC-036 | PASS — run #39; zero StarletteDeprecationWarning |


| DOC-068 | P1 | W32 Test & System-Structure Evidence Consolidation | 2026-11-05 | 06_EVIDENCE/DOC-068_W32-TEST-AND-SYSTEM-STRUCTURE-EVIDENCE-CONSOLIDATION-20261105.md | Consolidated CI, F4, Browser Adapter, PC runtime evidence; Xu architecture review |

## Additional records — 2026-11-06
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-075 | P1 | 35 | Workflow Mirror Branch-Source Audit | 06_EVIDENCE/DOC-075_WORKFLOW-MIRROR-BRANCH-SOURCE-AUDIT-20261106.md | DOC-014; DOC-035; DOC-036 | ACTIVE — branch integration gap confirmed |
| DOC-076 | P1 | 36 | Auto CI/CD Stages 1–6 Sandbox Implementation | 06_EVIDENCE/DOC-076_WORK-32-AUTO-CICD-STAGES-1-TO-6-SANDBOX-IMPLEMENTATION-20261106.md | DOC-074; DOC-075; DOC-014 | SANDBOX STATIC PREPARATION PASS; runtime/GitHub BLOCKED |
| DOC-077 | P1 | 37 | Browser Adapter Windows-Lane Gap and Fail-Closed Readiness | 06_EVIDENCE/DOC-077_WORK-32-BROWSER-ADAPTER-WINDOWS-LANE-READINESS-20261106.md | DOC-074; DOC-076; An QE audits | DESIGN RECONCILIATION COMPLETE; NOT ACTIVATED |
| DOC-078 | P1 | 38 | Ka Full-Process Continuation and Gate Status | 06_EVIDENCE/DOC-078_WORK-32-KA-FULL-PROCESS-CONTINUATION-AND-GATE-STATUS-20261106.md | DOC-074; DOC-076; DOC-077; DOC-035 | SANDBOX CONTINUATION COMPLETE; GITHUB+RUNTIME+WINDOWS BLOCKED |
| DOC-079 | P1 | 39 | Coverage Checker Windows-Lane Mapping Design | 01_PLAN/DOC-079_COVERAGE-CHECKER-WINDOWS-LANE-MAPPING-DESIGN-20261106.md | DOC-073; DOC-077; An INV-01 | DESIGN ONLY / NOT IMPLEMENTED |

| DOC-080 | P0 | 40 | GitHub Branch Drift and Sandbox Sync Package | 06_EVIDENCE/DOC-080_GITHUB-BRANCH-DRIFT-AND-SANDBOX-SYNC-PACKAGE-20261106.md | DOC-074; DOC-076; An 05:54 audit | SANDBOX PACKAGE READY; GITHUB WRITE BLOCKED |


## Current branch reconciliation — 2026-11-06
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-083 | P0 | 41 | Current Branch / Auto-E2E Reconciliation | 06_EVIDENCE/DOC-083_WORK-32-CURRENT-BRANCH-AUTO-E2E-RECONCILIATION-20261106.md | DOC-014; DOC-035; DOC-075; DOC-077; An 10:11 QE audit | HOSTED LANES PASS; WINDOWS SKIPPED; RELEASE GATE FAIL; NOT RELEASED |

- DOC-079 addendum: Windows coverage mapping is implemented on current GitHub branch; earlier Sandbox-only design status is historical. Windows execution remains blocked.
- DOC-080: retain as historical sync-package record; its branch-state assumptions were superseded by An's later 10:11 audit and DOC-083.
- Current source-of-truth observation: GitHub branch HEAD 554ebe3145e8b13206b50d8722879b0bae3db094; Sandbox source copies are stale. Do not promote Sandbox source without authorized exact-SHA reconciliation.


| DOC-084 | P0 | 42 | Windows Lane Fail-Closed Preflight Source Audit | 06_EVIDENCE/DOC-084_WINDOWS-LANE-FAIL-CLOSED-PREFLIGHT-SOURCE-AUDIT-20261106.md | DOC-083; DOC-081; DOC-082; DOC-014; DOC-035 | SOURCE CONTRACT VERIFIED; RUNNER/PROCESS/STORE READINESS BLOCKED; NOT RELEASED |

| DOC-085 | P2 | 43 | Current Acceptance Gate Reconciliation — Run #133 | 07_ACCEPT/DOC-020_BIEN-BAN_NGHIEM-THU-WORK-32-ACCEPTANCE-RECORD.md (addendum) | DOC-083; DOC-084; DOC-014; DOC-057; W14 restoration evidence | NOT ACCEPTED / NOT READY; Work32 ACTIVE — NOT RELEASED |


## Additional P0 execution design record — 2026-11-07
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-092 | P0 | 33 | Windows Auto E2E Runner-Owned Fixture and Process Design | 06_EVIDENCE/DOC-092_WORK32-WINDOWS-AUTO-E2E-RUNNER-OWNED-FIXTURE-PROCESS-DESIGN-20261107.md | DOC-074; DOC-077; DOC-083; DOC-084; DOC-035 | DESIGN VERIFIED / IMPLEMENTATION NOT INTEGRATED |


## Current review, remediation and exact-SHA evidence — 2026-11-09
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-093 | P0 | 44 | Browser Adapter stdio handoff source review | 06_EVIDENCE/DOC-093_W32-BROWSER-AGENT-ADAPTER-ROOMHOP-MCP-HANDOFF-SOURCE-REVIEW-20261108.md | DOC-069; DOC-035 | SOURCE REVIEW / integration evidence |
| DOC-094 | P0 | 45 | Exact GitHub branch and Adapter source | 06_EVIDENCE/DOC-094_WORK32-EXACT-GITHUB-BRANCH-AND-ADAPTER-SOURCE-20261108.md | DOC-093; DOC-035 | SOURCE SHA provenance |
| DOC-095 | P0 | 46 | PC checkout source mismatch | 06_EVIDENCE/DOC-095_WORK32-PC-CHECKOUT-SOURCE-MISMATCH-20261108.md | DOC-094; DOC-035 | Historical PC/runtime blocker |
| DOC-096 | P0 | 47 | Isolated PC checkout execution handoff | 06_EVIDENCE/DOC-096_WORK32-ISOLATED-PC-CHECKOUT-EXECUTION-HANDOFF-20261108.md | DOC-095 | Handoff recorded |
| DOC-097 | P0 | 48 | Clean PC checkout identity verification | 06_EVIDENCE/DOC-097_WORK32-CLEAN-PC-CHECKOUT-IDENTITY-VERIFICATION-20261108.md | DOC-096 | Source identity evidence |
| DOC-098 | P0 | 49 | Windows lane exact-SHA preflight requirements | 06_EVIDENCE/DOC-098_WORK32-WINDOWS-LANE-EXACT-SHA-PREFLIGHT-REQUIREMENTS-20261108.md | DOC-097; DOC-100 | Preflight contract |
| DOC-099 | P0 | 50 | Windows preflight runner and port 8787 blocker | 06_EVIDENCE/DOC-099_WORK32-WINDOWS-PREFLIGHT-RUNNER-AND-PORT8787-BLOCKER-20261108.md | DOC-098 | Historical blocker; no PC mutation in this remediation |
| DOC-100 | P0 | 51 | Runner-owned Windows E2E implementation | 06_EVIDENCE/DOC-100_WORK32-RUNNER-OWNED-WINDOWS-E2E-IMPLEMENTATION-20261108.md | DOC-098; DOC-099 | Windows E2E now PASS on Run #264 |
| DOC-101 | P0 | 52 | Main integration review package | 06_EVIDENCE/DOC-101_WORK32-MAIN-INTEGRATION-REVIEW-PACKAGE-20261108.md | DOC-035; DOC-094; DOC-100 | PR #49 clean integration package |
| DOC-102 | P0 | 53 | Architecture/security review request | 06_EVIDENCE/DOC-102_W32-ARCHITECTURE-SECURITY-REVIEW-REQUEST-20261109.md | DOC-101; DOC-035 | Xu/Cla review request |
| DOC-103 | P0 | 54 | CEO/CTO review request and execution log | 06_EVIDENCE/DOC-103_WORK32-CEO-CTO-REVIEW-REQUEST-AND-EXECUTION-LOG-20261109.md | DOC-102; PR #49 | Review request posted; response/re-review pending |
| DOC-104 | P0 | 55 | PR49 exact source mirror manifest | 06_EVIDENCE/DOC-104_WORK32-PR49-SOURCE-MIRROR-MANIFEST-20261109.md | DOC-101; DOC-102 | 11/11 source mirror byte-identical PASS |
| DOC-105 | P0 | 56 | Xu/Cla review reconciliation and remediation matrix | 06_EVIDENCE/DOC-105_WORK32-REVIEW-RECONCILIATION-AND-REMEDIATION-MATRIX-20261109.md | DOC-102; DOC-103; DOC-104 | Findings mapped; Qw W32 report traceability pending |
| DOC-106 | P0 | 57 | Security remediation build plan | 06_EVIDENCE/DOC-106_WORK32-SECURITY-REMEDIATION-BUILD-PLAN-20261109.md | DOC-105; Xu-03; Cla-EVIDENCE-017 | Implementation on PR #49; exact-SHA CI PASS |
| DOC-107 | P0 | 58 | Security remediation Run #264 evidence | 06_EVIDENCE/DOC-107_WORK32-SECURITY-REMEDIATION-RUN264-20261109.md | DOC-104; DOC-105; DOC-106 | Run #264 6/6 PASS; re-review/product gates open |

**Current source of truth:** PR #49 code SHA `3b25f2759a5b8daf7477b155d306ddaa7e1032ac` passed Run #264 (`42521404004`) across all six jobs. Latest PR head `a7fe318d14ef06bf3c25bf6005b80dede81a307f` adds DOC-107 only. PR remains DRAFT; main unchanged; ACTIVE — NOT RELEASED.

- **DOC-107 addendum:** Run #265 (`42521596692`) revalidated documentation-only head `a7fe318d14ef06bf3c25bf6005b80dede81a307f`; 6/6 PASS. Code SHA remains Run #264 PASS at `3b25f2759a5b8daf7477b155d306ddaa7e1032ac`.

- **DOC-107 addendum:** Run #266 (`42521781012`) completed SUCCESS on docs-only PR head `6369ce2578492e996390a422b759e40d0585acf5`; all six required jobs PASS. Code SHA remains Run #264 PASS.

- **DOC-105/DOC-107 addendum:** Cla S10 is explicitly OPEN (meeting.yaml atomicity and ID allocation concurrency). Run #267 (`42521925585`) 6/6 PASS on documentation-only head `79dd24cc3451a58646643982af3003cc5712edb9`; code SHA Run #264 remains PASS.

- **DOC-105/DOC-107 addendum:** S10 atomic YAML replacement, same-process per-meeting serialization, and collision-safe ID reservation implemented; Run #276 (`42522590577`) pending exact head `815c6720078eddb03c2219e1cba0b442456e0502`. Cross-process YAML consistency remains open.

- **DOC-105/DOC-107 addendum:** S10 PASS within one-Core-process local boundary on Run #277 (`42522681112`), exact head `d72b68659e9717d8ea33a5c41b2d379fc15064e2`, 6/6 PASS. Cross-process meeting.yaml read-modify-write remains OPEN; multi-process/multi-host BLOCKED.

- **DOC-107 addendum:** Run #289 (`42523529820`) SUCCESS 6/6 on latest documentation-only head `03f9ebe2a70b576900f8284375e3663bd14d69e6`; code SHA `e0e990a2c2a0d92813afd811359b8cf168c0e18b` passed Run #287 with 205 Unit tests.

- **DOC-107 addendum:** Run #290 (`42523723241`) SUCCESS 6/6 on latest PR head `1d9a8f5f172b8075dd8223728ba0c057bb35ea14`; code/test SHA `e0e990a2c2a0d92813afd811359b8cf168c0e18b` passed Run #287 with 205 unit tests.


## Additional P0 governance control — 2026-11-09
| DOC-ID | Priority | Read order | Canonical document | Canonical path / reference | Depends on | Status |
| DOC-108 | P0 | 59 | Quy định cổng đọc hồ sơ và tiếp nhận AI Work 32 / Work 32 AI Full-Read Entry Gate | 00_ROOT/DOC-108_QUY-DINH_CONG-READ-GATE_TIEP-NHAN-AI-WORK-ENTRY-AND-FULL-READ-REQUIREMENT.md | DOC-001; DOC-002; DOC-003; DOC-004; DOC-005; DOC-006; DOC-033; DOC-055; Work70 DOC-057 | ACTIVE — POLICY ADOPTED / TECHNICAL ENFORCEMENT NOT VERIFIED |

Reading rule addendum: DOC-108 is mandatory for every Work32 participant. It requires all canonical controlled documents registered in DOC-055 (P0–P3), the full DOC-035 journal, DOC-034 minutes, DOC-006 decisions, shared Work70 standards and assignment-linked evidence. Per-agent/per-assignment Work Entry records must be created and referenced from DOC-035. DOC-055 remains the sole Work32 document register.


## 2026-11-10 — F1 controlled assignment
| DOC-ID / Assignment | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| W32-ASG-F1-001 | P0 | 60 | DOC-044 Work Assignment Contract — F1 repeated-start and health semantics | 04_PLAN/DOC-044_W32-F1-REPEATED-START-ASSIGNMENT.md | DOC-035 W32-LOG-20261110-132; DOC-115; Work70 DOC-044; Work70 DOC-057; Work70 DOC-093 Task W32-05-BUILD-KA-F1-REPEATED-START-001 | DRAFT / BLOCKED — NO SOURCE WRITE AUTHORIZATION |

- This assignment instance is linked to the Work70 role-based Task Register. It is a controlled DRAFT and does not authorize source/test mutation until Work Entry G0–G5 PASS, source-map reconciliation, READY status and Ka ACK.


## 2026-11-10 — DOC-116 participant-specific Work Entry record designation
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-116 | P0 | 61 | Work Entry Record — Ka / AI-02 / W32-ASG-F1-001 | 00_ROOT/DOC-116_WORK-ENTRY_KA_AI-02_W32-ASG-F1-001.md | DOC-108; DOC-044; Work70 DOC-057; DOC-035 | OPEN — PARTICIPANT COMPLETION REQUIRED; NOT A GATE PASS |

- Xu designates DOC-116 as the single canonical Ka-specific entry record for W32-ASG-F1-001. Ka owns completion of participant reading inventory and G0–G5 evidence; Xu owns independent verification and explicit READY/BLOCKED decision.
- DOC-116 resolves the missing record identity/path only. It does not pass G2, any other gate, grant execution permission, or imply Ka ACK.
- Current status remains G0/G1/G3 participant-reported PASS pending Xu review; G2 PARTIAL; G4/G5 BLOCKED. No source/test write, test execution, CI dispatch, runner/PC action, branch/PR/main mutation, merge, deploy or release.


## 2026-11-10 — DOC-117 scoped execution boundary decision
| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-117 | P0 | 62 | Quyết định đường thực thi có kiểm soát quyền / W32 Scoped Execution Boundary | 00_ROOT/DOC-117_QUYET-DINH_DUONG-THUC-THI-CO-KIEM-SOAT-QUYEN_W32-SCOPED-EXECUTION-BOUNDARY.md | DOC-001; DOC-002; DOC-044; DOC-055; Work70 DOC-057/DOC-063; DOC-108; DOC-116; DOC-035 | TARGET CONTRACT SELECTED / ENFORCEMENT NOT IMPLEMENTED OR VERIFIED |

- DOC-117 selects a fail-closed, server-enforced Authorization Gateway as the target route for protected Work32 writes and execution. Every grant must bind authenticated participant, Work, active assignment/ACK, exact resource/path, action, source SHA/blob, environment, validity/revocation and verified Work Entry decision.
- Generic Work-level Sandbox write tools do not prove or enforce this tuple and are not an acceptable protected execution route.
- DOC-117 is a target architecture/operational hold only. It does not claim gateway implementation, approve Core changes, pass G4/G5 or grant execution permission. Work70 DOC-063 remains DRAFT / DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED.

 
## 2026-11-10 — Xu status correction addendum for DOC-116
- **Purpose:** Reconcile the historical DOC-116 row below with the current participant submission and Xu independent review, without rewriting the register's historical row or DOC-116 history.
- **Canonical document:** DOC-116 — 00_ROOT/DOC-116_WORK-ENTRY_KA_AI-02_W32-ASG-F1-001.md
- **Correction evidence:** DOC-116 addendum W32-DOC-116-CORR-20261110-01 and Xu Independent Review Addendum dated 2026-11-10; W32-LOG-20261110-176 in DOC-035.
- **Current participant status:** PARTICIPANT EVIDENCE SUBMITTED / WAITING XU INDEPENDENT REVIEW — correction addendum verified present.
- **Xu independent gate disposition:** G0 PARTIAL; G1 BLOCKED; G2 PASS LIMITED for registration/storage only; G3 PARTIAL; G4 BLOCKED; G5 BLOCKED.
- **Register interpretation:** The original DOC-116 table row remains historical and is not overwritten. This addendum is the current status authority until a controlled future version updates the row.
- **Execution boundary:** DOC-044 remains DRAFT/BLOCKED. No READY/EXECUTION_AUTHORIZED decision; no source/test write, test execution, CI dispatch, PC/runner action, branch/PR/main mutation, merge, deployment or release.
- **Next:** Ka resolves G1/G3 evidence gaps; Xu re-reviews. G4 requires a real server-enforced Authorization Gateway and Core Owner approval/evidence. Work32 remains ACTIVE — NOT RELEASED.



## 2026-11-14 — DOC-125 Execution Host OS resource quota design review

| DOC-ID | Priority | Read order | Canonical document | Canonical path | Depends on | Status |
|---|---|---:|---|---|---|---|
| DOC-125 | P0 | 63 | W32 Execution Host OS Resource Quota Design Review | 01_PLAN/DOC-125_W32-EXECUTION-HOST-OS-RESOURCE-QUOTA-DESIGN-REVIEW-20261114.md | DOC-117; DOC-123; DOC-124; DOC-035 | PROPOSED — REVIEW REQUEST ONLY — NOT APPROVED |

- DOC-125 records the missing OS-enforced memory, CPU and process-count quotas in the Work32 protected execution path and requests independent review from Ka and Cla.
- Candidate Windows Job Object design is not approved. Race-free process assignment before user code starts, fail-closed behavior, supported-platform policy and deterministic negative tests must be reviewed.
- No code change is authorized until review feedback is reconciled into the canonical Biên bản/decision. Protected execution remains DENIED; Work32 remains ACTIVE — NOT ACCEPTED — NOT RELEASED.


## 2026-11-14 — DOC-125 review and decision status addendum

- **Canonical DOC-125:** 01_PLAN/DOC-125_W32-EXECUTION-HOST-OS-RESOURCE-QUOTA-DESIGN-REVIEW-20261114.md.
- **Reviews received:** Ka / AI-02 CSA review; Cla / AI-03 CTO feasibility review. Both are READ-ONLY and neither authorizes implementation.
- **Xu source trace:** exact-branch blobs independently fetched; see DOC-035 W32-LOG-20261114-134.
- **Decision:** DOC-006 W32-DECISION-20261114-08 and DOC-034 Biên bản W32-20261114-08 approve the Windows Job Object / ResourceBackend design direction WITH CONDITIONS only.
- **Current status:** REVIEW COMPLETE / DESIGN DIRECTION APPROVED WITH CONDITIONS / PRODUCT IMPLEMENTATION NOT AUTHORIZED. D1–D6 remain open; protected execution DENIED; H1 resource isolation BLOCKED.
- **Evidence mirror:** Cla review file is stored at 06_EVIDENCE/W32-EVIDENCE-CLA-06-DOC125-RESOURCE-QUOTA-CTO-REVIEW-20261114.md.
- **No release:** Work32 remains ACTIVE — NOT ACCEPTED — NOT RELEASED.
