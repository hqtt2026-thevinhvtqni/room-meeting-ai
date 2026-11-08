# SỔ ĐĂNG KÝ TÀI LIỆU WORK 103 / WORK 103 DOCUMENT REGISTER
- **STT / Document ID:** DOC-055
- **Priority:** P0
- **Read order:** 2
- **Depends on:** DOC-001
- **Status:** ACTIVE — INITIAL INVENTORY
- **Version / Updated:** 1.0 / 2026-11-08
- **Authority:** Vinh
- **Owner:** Xu / AI-01

This is the sole canonical register for Work 103 controlled documents and important technical artifacts. One document has one canonical path. Legacy paths below are not competing sources.

| ID / Artifact | Type | Canonical path or mapping | Current status | Notes |
|---|---|---|---|---|
| DOC-001 | Manifest | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | ACTIVE | Work identity, source authority, structure and gates |
| DOC-034 | Official minutes | 00_ROOT/DOC-034_BIEN-BAN_HOP-WORK-103-MINUTES.md | ACTIVE | Legacy path retained as pointer |
| DOC-035 | Execution journal | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-103-EXECUTION-LOG.md | ACTIVE | Legacy journal history merged and preserved |
| DOC-045 | Work plan / roadmap | 04_PLAN/DOC-045_KE-HOACH-THI-CONG_WORK-103-ROADMAP.md | ACTIVE | Legacy path retained as pointer |
| DOC-055 | Document Register | 00_ROOT/DOC-055_SO-DANG-KY-TAI-LIEU_WORK-103-DOCUMENT-REGISTER.md | ACTIVE | Sole register |
| DOC-056 | Standardization plan | 00_ROOT/DOC-056_KE-HOACH-CHUAN-HOA_WORK-103-STANDARDIZATION-PLAN.md | ACTIVE | Controlled migration batches |
| DOC-057 | Evidence Register | EVIDENCE/DOC-057_SO-DANG-KY-BANG-CHUNG_WORK-103-EVIDENCE-REGISTER.md | ACTIVE | Sole cross-phase evidence index |
| TECH-001 | RAG corpus | 00_CORPUS/ | ACTIVE / SOURCE_MAPPING_PENDING | Corpus manifest and source documents |
| TECH-002 | RAG architecture | 03_ARCHITECTURE/ | ACTIVE / REGISTER_DETAIL_PENDING | Architecture documents and contracts |
| TECH-003 | RAG implementation | 04_CODE/ | ACTIVE / SOURCE_MAPPING_PENDING | Python source and requirements; preserve current CI paths |
| TECH-004 | Test suite and evaluation sets | 05_TEST/ | ACTIVE / SOURCE_MAPPING_PENDING | Includes EVAL_SET.json and blind candidate pool V1 |
| EVD-LEGACY | Historical evidence | 06_EVIDENCE/ | LEGACY_PATH / CONTENT_ACTIVE | Preserve historical files; no silent moves |
| TECH-005 | CI workflow | .github/workflows/work-103-rag-ci.yml | ACTIVE / VERIFY_MAPPING | Register exact branch/ref and commit in next mapping update |
| DASH-001 | Work dashboard | DASHBOARD/ | NOT_CREATED | Read-only projection; no mock values |

## Legacy path mapping
| Existing path | Canonical destination | Migration action |
|---|---|---|
| 00_ROOT/WORK_MANIFEST.md | 00_ROOT/DOC-001... | Compatibility pointer established; inbound-link audit still pending |
| BIEN_BAN.md | 00_ROOT/DOC-034... | Canonical copy established; original path now pointer |
| KE_HOACH_THI_CONG_XU.md | 04_PLAN/DOC-045... | Canonical copy established; WPs to be rebaselined; original path now pointer |
| NHAT_KY_HOP_THI_CONG.md | 00_ROOT/DOC-035... | Historical entries preserved in DOC-035; original path now pointer |
| 00_CORPUS/ | 01_DISCOVER/ + approved corpus location | Classify received originals vs curated test fixtures before moving |
| 02_EXTENSION/ | 01_DISCOVER/ or 03_ARCHITECT/ | Classify reference material before moving |
| 03_ARCHITECTURE/ | 03_ARCHITECT/ | Map architecture documents; no move now |
| 04_CODE/ | 05_BUILD mapping → declared canonical source path | Preserve until CI/import/reference migration is verified |
| 05_TEST/ | 06_VERIFY mapping → declared canonical test path | Preserve until CI/test reference migration is verified |
| 06_EVIDENCE/ | EVIDENCE/ | Keep legacy read path until all links/workflow consumers are audited |

## Register rules
Update this register whenever a controlled document, canonical path, source mapping, status or version changes. Technical artifacts are registered by stable artifact ID and exact path/ref/commit; do not assign DOC IDs to source code. A status is not PASS unless supported by exact evidence. Compatibility pointers are not separate authoritative documents.
