# SỔ ĐĂNG KÝ TÀI LIỆU WORK 70 / WORK 70 DOCUMENT REGISTER
- **STT / Document ID:** DOC-055
- **Priority:** P0
- **Read order:** 55
- **Depends on:** DOC-001; DOC-038; DOC-039; DOC-040; DOC-056
- **Status:** ACTIVE — SINGLE SOURCE OF TRUTH
- **Version / Updated:** 2.0 / 2026-10-31
- **Owner:** Xu / AI-01
- **Authority:** Vinh
Register version: 2.0
Owner: Xu / AI-01
Authority: Vinh
Rule: DOC-ID is stable identity; Priority is importance; Read order is sequence. Every controlled document has one canonical path. Legacy paths are aliases only.

| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-001 | P0 | 1 | Work Manifest | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | NONE | ACTIVE | Identity, authority, scope, state and source boundaries; always first |
| DOC-002 | P0 | 2 | AI Project Intake & Execution Standard | 00_ROOT/DOC-002_TIEU-CHUAN-TIEP-NHAN-DU-AN_AI-PROJECT-INTAKE-STANDARD.md | DOC-001 | ACTIVE | Mandatory intake and AI behavior |
| DOC-003 | P0 | 3 | Repository Layout & Sync | 00_ROOT/DOC-003_CAU-TRUC-KHO-VA-DONG-BO_REPOSITORY-LAYOUT-AND-SYNC.md | DOC-001 | ACTIVE | Branch, Sandbox, canonical ownership and sync boundaries |
| DOC-004 | P0 | 4 | Lifecycle Gate Matrix | 00_ROOT/DOC-004_MA-TRAN-CONG-VONG-DOI_LIFECYCLE-GATE-MATRIX.md | DOC-001 | ACTIVE | Gate and transition conditions |
| DOC-005 | P0 | 5 | State Machine | 00_ROOT/DOC-005_MAY-TRANG-THAI_WORK-STATE-MACHINE.md | DOC-004 | ACTIVE | Legal states and transitions |
| DOC-006 | P0 | 6 | Decision Log | 00_ROOT/DOC-006_SO-QUYET-DINH_DECISION-LOG.md | DOC-001 | ACTIVE | Binding decisions and rationale |
| DOC-033 | P0 | 7 | Work Documentation & Storage Standard | 00_ROOT/DOC-033_TIEU-CHUAN-TAI-LIEU-VA-LUU-TRU_WORK-DOCUMENTATION-AND-STORAGE-STANDARD.md | DOC-001; DOC-002; DOC-003 | ACTIVE | Four official records, canonical ownership, mapping and storage rules |
| DOC-038 | P0 | 8 | Quy trình đặt tên tài liệu / Document Naming Standard | 00_ROOT/DOC-038_QUY-TRINH-DAT-TEN-TAI-LIEU_DOCUMENT-NAMING-STANDARD.md | DOC-001; DOC-002; DOC-003; DOC-033 | ACTIVE | Vietnamese-first bilingual naming, stable IDs, filename pattern and controlled legacy renames |
| DOC-039 | P0 | 9 | Quy chuẩn mã loại văn bản / Document Type Code Standard | 00_ROOT/DOC-039_QUY-CHUAN-MA-LOAI-VAN-BAN_DOCUMENT-TYPE-CODE-STANDARD.md | DOC-001; DOC-006; DOC-033; DOC-034; DOC-038 | ACTIVE | Controlled prefixes for minutes, decisions, directives, appendices and other formal records |
| DOC-040 | P0 | 10 | Sổ đăng ký mã văn bản / Official Document Code Register | 00_ROOT/DOC-040_SO-DANG-KY-MA-VAN-BAN_OFFICIAL-DOCUMENT-CODE-REGISTER.md | DOC-001; DOC-006; DOC-039 | ACTIVE | Single issuance ledger for all operational document codes; no code issued without evidence |
| DOC-007 | P1 | 11 | Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DOC-001 | ACTIVE | Problem, users, evidence and assumptions |
| DOC-008 | P1 | 12 | Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DOC-007 | ACTIVE | Scope, requirements and acceptance criteria |
| DOC-009 | P1 | 13 | Work Lifecycle Architecture | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | DOC-008 | ACTIVE | Product lifecycle and system architecture |
| DOC-010 | P1 | 14 | Dashboard Core Read Contract | 03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md | DOC-009 | ACTIVE | Core/Dashboard boundary and read-only contract |
| DOC-011 | P1 | 15 | Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DOC-008; DOC-009 | ACTIVE | Delivery sequence and milestones |
| DOC-012 | P1 | 16 | Work Instantiation & Migration | 04_PLAN/WORK_INSTANTIATION_AND_MIGRATION.md | DOC-003; DOC-009 | ACTIVE | How to create/migrate a Work safely |
| DOC-013 | P1 | 17 | Legacy Build Register (WP candidate) | branch work/70/05-build: 05_BUILD/00_ROOT/BUILD_REGISTER.json; BUILD_REGISTER.md | DOC-033; DOC-011 | MIGRATION PENDING | Existing WP records; candidate for reconciliation into Work-level plan, not yet a canonical mapping |
| DOC-036 | P1 | 18 | Build Mapping Register | branch work/70/05-build: 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md | DOC-001; DOC-003; DOC-033 | ACTIVE / MIGRATION IN PROGRESS | Maps engineering artifacts to canonical Work/source paths and classifies legacy build files |
| DOC-014 | P1 | 19 | Evidence Register | 06_EVIDENCE/EVIDENCE_REGISTER.json; EVIDENCE_REGISTER.md | DOC-004; DOC-033 | ACTIVE | Cross-phase canonical evidence and provenance |
| DOC-015 | P1 | 20 | Verification Plan | 06_VERIFY/VERIFICATION_PLAN.md | DOC-008; DOC-013; DOC-014 | ACTIVE | Verification strategy and coverage |
| DOC-016 | P1 | 21 | Storage & Export Architecture | branch work/70/05-build: 05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | DOC-009; DOC-010; DOC-033 | CANONICAL CANDIDATE / MIGRATION PENDING | Technical design; reconcile into 03_ARCHITECT before any build copy is retired |
| DOC-017 | P1 | 22 | Core Capability Gap Assessment | branch work/70/05-build: 05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | DOC-010; DOC-033 | CANONICAL CANDIDATE / MIGRATION PENDING | Evidence-based Core capability assessment; reconcile into Work-level architecture/verification record |
| DOC-018 | P2 | 23 | Migration Plan | 04_PLAN/MIGRATION_PLAN.md | DOC-012; DOC-033 | ACTIVE | Execution steps for approved migration |
| DOC-019 | P2 | 24 | Verification Checklist | 06_VERIFY/VERIFICATION_CHECKLIST.md | DOC-015 | ACTIVE | Operational verification checklist |
| DOC-020 | P2 | 25 | Acceptance Record | 07_ACCEPT/ACCEPTANCE_RECORD.md | DOC-015; DOC-019 | ACTIVE | Authorized acceptance decision |
| DOC-021 | P2 | 26 | Release Plan | 08_RELEASE/RELEASE_PLAN.md | DOC-020 | ACTIVE | Controlled release preparation |
| DOC-022 | P2 | 27 | Operations Model | 09_OPERATE/OPERATIONS_MODEL.md | DOC-021 | ACTIVE | Post-release operations |
| DOC-023 | P2 | 28 | Project Intake Report Template | 00_ROOT/DOC-023_BIEU-MAU-BAO-CAO-TIEP-NHAN_DU-AN-PROJECT-INTAKE-REPORT-TEMPLATE.md | DOC-001; DOC-002 | ACTIVE | Required consistent intake report |
| DOC-024 | P2 | 29 | Storage & Export Acceptance | branch work/70/05-build: 05_BUILD/05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | DOC-016; DOC-015 | CANONICAL CANDIDATE / MIGRATION PENDING | Test plan candidate for 06_VERIFY; NOT EXECUTED |
| DOC-025 | P2 | 30 | AI Participants & Token Usage | branch work/70/05-build: 05_BUILD/00_ROOT/AI_PARTICIPANTS_AND_TOKEN_USAGE.md | DOC-002 | LEGACY / REFERENCE | Audit accuracy and retention need; roster is not participation proof |
| DOC-034 | P2 | 31 | Biên bản Work | 00_ROOT/DOC-034_BIEN-BAN_HOP-WORK-70-MINUTES.md | DOC-001; DOC-006; DOC-033 | ACTIVE | Official minutes register; binding decisions link to DECISION_LOG |
| DOC-035 | P2 | 32 | Nhật ký thi công Work | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md | DOC-001; DOC-002; DOC-033 | ACTIVE | Chronological Work-wide execution record |
| DOC-026 | P3 | 33 | Lifecycle Guide (Vietnamese) | 00_ROOT/DOC-026_HUONG-DAN-VONG-DOI_LIFECYCLE-GUIDE-VI.md | DOC-004; DOC-005 | ACTIVE | Human-readable explanation of lifecycle |
| DOC-027 | P3 | 34 | Work Standard Versioning | 00_ROOT/DOC-027_QUAN-LY-PHIEN-BAN_TIEU-CHUAN-WORK-STANDARD-VERSIONING.md | DOC-001 | ACTIVE | Version history and compatibility |
| DOC-028 | P3 | 35 | Vietnamese Glossary | 00_ROOT/DOC-028_BANG-THUAT-NGU_VIETNAMESE-GLOSSARY.md | DOC-002 | ACTIVE | Terminology reference |
| DOC-029 | P3 | 36 | Legacy Scaffold Notice | LEGACY_SCAFFOLD_NOTICE.md | DOC-001 | ACTIVE | Historical/legacy context |
| DOC-030 | P3 | 37 | Work 70 Session Log | branch work/70/05-build: 05_BUILD/10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | DOC-002; DOC-033 | LEGACY / HISTORICAL | Preserve detail; Work-wide chronological record is 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md |
| DOC-031 | P3 | 38 | Consolidation Evidence Report | 06_EVIDENCE/WORK70_CONSOLIDATION_CHECK_20261030.md | DOC-014 | ACTIVE | Historical evidence of Work 70 consolidation |
| DOC-032 | P3 | 39 | Dashboard README | DASHBOARD/README.md | DOC-010 | ACTIVE | Dashboard usage and limitations |
| DOC-037 | P3 | 40 | Work 70 README | README.md | DOC-001; DOC-033; DOC-036 | ACTIVE | Human-readable entry point; subordinate to Manifest and standards |
| DOC-041 | P1 | 41 | Báo cáo rà soát quản trị Work 70 / Work 70 Governance Audit Report | 00_ROOT/DOC-041_BAO-CAO-RA-SOAT-QUAN-TRI_GOVERNANCE-AUDIT-REPORT.md | DOC-001; DOC-003; DOC-004; DOC-005; DOC-006; DOC-033; DOC-038; DOC-039; DOC-040 | ACTIVE — AUDIT OPEN | Confirmed governance findings and remediation backlog; not product acceptance |

## AI reading rule
Read DOC-001 through DOC-006, then DOC-033, DOC-038, DOC-039 and DOC-040. Then read relevant P1 documents in ascending read order. Read P2 only for the active task. Read P3 when clarification, operations or historical trace requires it. Read DOC-041 when reconciling governance or closing its remediation backlog. Never infer PASS from the register or presence of a file.

## Maintenance
When adding a document: allocate the next unused DOC ID, set priority/read order/dependencies, add one row here, and add required metadata below the title. Canonical filenames must encode DOC-ID under DOC-038. Legacy paths are retained only as controlled aliases during migration; see DOC-056. A document located under 05_BUILD is not canonical solely because of its path; its authority must be explicitly declared by this standard and mapping register.

| DOC-042 | P0 | 42 | Quy trình điều phối thực thi toàn trình / End-to-End Execution Orchestration | 00_ROOT/DOC-042_QUY-TRINH-DIEU-PHOI-THUC-THI_EXECUTION-ORCHESTRATION.md | DOC-001; DOC-002; DOC-004; DOC-005; DOC-033; DOC-041 | ACTIVE / OPERATING STANDARD | Hợp đồng điều phối, assignment, tích hợp, bằng chứng, blocker và handoff |
| DOC-043 | P0 | 43 | Ma trận vai trò và quyền AI / AI Role & Permission Matrix | 00_ROOT/DOC-043_MA-TRAN-VAI-TRO-VA-QUYEN-AI_AI-ROLE-PERMISSION-MATRIX.md | DOC-002; DOC-004; DOC-005; DOC-042 | ACTIVE / CONTROLLED REGISTER | Vai trò, quyền mặc định, capability verification và độc lập QE |
| DOC-044 | P1 | 44 | Mẫu hợp đồng giao việc / Work Assignment Contract Template | 04_PLAN/DOC-044_MAU-HOP-DONG-GIAO-VIEC_WORK-ASSIGNMENT-CONTRACT.md | DOC-002; DOC-011; DOC-033; DOC-042; DOC-043 | ACTIVE / TEMPLATE | Mẫu assignment bắt buộc cho mọi WP/AI |

| DOC-045 | P1 | 45 | Hướng dẫn thực thi giai đoạn Khám phá / Discover Execution Playbook | 01_DISCOVER/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 01_DISCOVER |
| DOC-046 | P1 | 46 | Hướng dẫn thực thi giai đoạn Định nghĩa / Define Execution Playbook | 02_DEFINE/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 02_DEFINE |
| DOC-047 | P1 | 47 | Hướng dẫn thực thi giai đoạn Kiến trúc / Architect Execution Playbook | 03_ARCHITECT/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 03_ARCHITECT |
| DOC-048 | P1 | 48 | Hướng dẫn thực thi giai đoạn Kế hoạch / Plan Execution Playbook | 04_PLAN/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 04_PLAN |
| DOC-049 | P1 | 49 | Hướng dẫn thực thi giai đoạn Thi công / Build Execution Playbook | 05_BUILD/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 05_BUILD |
| DOC-050 | P1 | 50 | Hướng dẫn thực thi giai đoạn Kiểm chứng / Verify Execution Playbook | 06_VERIFY/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 06_VERIFY |
| DOC-051 | P1 | 51 | Hướng dẫn thực thi giai đoạn Nghiệm thu / Accept Execution Playbook | 07_ACCEPT/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 07_ACCEPT |
| DOC-052 | P1 | 52 | Hướng dẫn thực thi giai đoạn Phát hành / Release Execution Playbook | 08_RELEASE/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 08_RELEASE |
| DOC-053 | P1 | 53 | Hướng dẫn thực thi giai đoạn Vận hành / Operate Execution Playbook | 09_OPERATE/PHASE_EXECUTION_PLAYBOOK.md | DOC-042; DOC-004; DOC-005 | ACTIVE / EXECUTION PLAYBOOK | Quy trình đầu vào, thực thi, đầu ra, exit checks và điều cấm của phase 09_OPERATE |
| DOC-054 | P0 | 54 | Lệnh phân công song song Work 70 / Work 70 Parallel Assignment Order | 05_BUILD/00_ROOT/DOC-054_LENH-PHAN-CONG-SONG-SONG-WORK-70.md (branch: work/70/05-build) | DOC-001; DOC-042; DOC-043; DOC-044 | ACTIVE / ASSIGNMENT READY | Phân công Ka, Co, Vi, Qw; trạng thái nhận việc phải xác minh riêng |
| DOC-055 | P0 | 55 | Sổ đăng ký tài liệu Work 70 / Work 70 Document Register | 00_ROOT/DOC-055_SO-DANG-KY-TAI-LIEU_WORK-70-DOCUMENT-REGISTER.md | DOC-001; DOC-038; DOC-039; DOC-040; DOC-056 | ACTIVE / SINGLE SOURCE OF TRUTH | Sổ duy nhất cho DOC-ID, metadata, canonical paths, branch/ref và trạng thái |
| DOC-056 | P0 | 56 | Quyết định chuẩn hóa hệ thống tài liệu Work 70 / Work 70 Document Standardization Policy | 00_ROOT/DOC-056_QUYET-DINH-CHUAN-HOA-HE-THONG-TAI-LIEU_WORK-70-DOCUMENT-STANDARDIZATION-POLICY.md | DOC-001; DOC-033; DOC-038; DOC-039; DOC-040; DOC-055 | ACTIVE / MIGRATION IN PROGRESS | Quy tắc thống nhất và batch migration toàn Work 70 |
