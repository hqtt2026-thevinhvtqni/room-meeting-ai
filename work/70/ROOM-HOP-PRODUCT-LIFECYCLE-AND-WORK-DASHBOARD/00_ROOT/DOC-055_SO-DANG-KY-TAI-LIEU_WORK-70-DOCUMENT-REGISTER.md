# SỔ ĐĂNG KÝ TÀI LIỆU WORK 70 / WORK 70 DOCUMENT REGISTER
- **STT / Document ID:** DOC-055
- **Priority:** P0
- **Read order:** 55
- **Depends on:** DOC-001; DOC-038; DOC-039; DOC-040; DOC-056
- **Status:** ACTIVE — SINGLE SOURCE OF TRUTH
- **Version / Updated:** 3.3 / 2026-11-07
- **Owner:** Xu / AI-01
- **Authority:** Vinh
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
| DOC-039 | P0 | 9 | Quy chuẩn mã loại văn bản / Document Type Code Standard | 00_ROOT/DOC-039_QUY-CHUAN-MA-LOAI-VAN-BAN_DOCUMENT-TYPE-CODE-STANDARD.md | DOC-001; DOC-006; DOC-033; DOC-034; DOC-038 | ACTIVE | Controlled prefixes include BB, BC, QD, QDY, NQ, TTR, PL, HD, HDONG, QT, TC, CT, PA, PH, LENH, KH, YC, TK, BM, HS, TB and CV; QD/QDY, HD/HDONG and QT/TC are distinct. Canonical validator reads DOC-055 directly; legacy DOCUMENT_REGISTER.md is pointer only |
| DOC-040 | P0 | 10 | Sổ đăng ký mã văn bản / Official Document Code Register | 00_ROOT/DOC-040_SO-DANG-KY-MA-VAN-BAN_OFFICIAL-DOCUMENT-CODE-REGISTER.md | DOC-001; DOC-006; DOC-039 | ACTIVE | Single issuance ledger for all operational document codes; no code issued without evidence |
| DOC-007 | P1 | 11 | Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DOC-001 | ACTIVE — G0/G1 NOT_READY; DISCOVERY OUTPUT PREPARED | Problem, users, evidence and assumptions |
| DOC-008 | P1 | 12 | Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DOC-007 | ACTIVE | Scope, requirements and acceptance criteria |
| DOC-009 | P1 | 13 | Work Lifecycle Architecture | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | DOC-008 | ACTIVE | Product lifecycle and system architecture |
| DOC-010 | P1 | 14 | Dashboard Core Read Contract | 03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md | DOC-009 | ACTIVE | Core/Dashboard boundary and read-only contract |
| DOC-011 | P1 | 15 | Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DOC-008; DOC-009 | ACTIVE | Delivery sequence and milestones |
| DOC-012 | P1 | 16 | Work Instantiation & Migration | 04_PLAN/WORK_INSTANTIATION_AND_MIGRATION.md | DOC-003; DOC-009 | ACTIVE | How to create/migrate a Work safely |
| DOC-013 | P1 | 17 | Sổ gói công việc Build / Build Register (WP candidate) | branch work/70/05-build: 05_BUILD/00_ROOT/BUILD_REGISTER.json | DOC-033; DOC-011 | MIGRATION PENDING | JSON is the single machine-readable canonical source for this branch-scoped candidate; BUILD_REGISTER.md is a read-only projection and schemas are technical validators; reconcile WP records into Work-level plan before promotion |
| DOC-036 | P1 | 18 | Build Mapping Register | branch work/70/05-build: 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md | DOC-001; DOC-003; DOC-033 | ACTIVE / MIGRATION IN PROGRESS | Maps engineering artifacts to canonical Work/source paths and classifies legacy build files |
| DOC-014 | P1 | 19 | Sổ bằng chứng / Evidence Register | EVIDENCE/EVIDENCE_REGISTER.json | DOC-004; DOC-033 | ACTIVE — SINGLE CANONICAL JSON SOURCE | Canonical machine-readable source; EVIDENCE_REGISTER.md is a read-only projection and EVIDENCE_REGISTER.schema.json is its technical schema |
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
| DOC-029 | P3 | 36 | Thông báo cấu trúc cũ / Legacy Scaffold Notice | 00_ROOT/DOC-029_THONG-BAO-CAU-TRUC-CU_LEGACY-SCAFFOLD-NOTICE.md | DOC-001 | ACTIVE / HISTORICAL STRUCTURE NOTICE | Historical scaffold rules and 2026-11-07 evidence-path correction; canonical DOC-prefixed file |
| DOC-030 | P3 | 37 | Work 70 Session Log | branch work/70/05-build: 05_BUILD/10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | DOC-002; DOC-033 | LEGACY / HISTORICAL | Preserve detail; Work-wide chronological record is 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md |
| DOC-031 | P3 | 38 | Báo cáo kiểm tra hợp nhất Work 70 / Work 70 Consolidation Checkpoint | EVIDENCE/DOC-031_BAO-CAO-KIEM-TRA-HOP-NHAT_WORK70-CONSOLIDATION-CHECKPOINT.md | DOC-014 | ACTIVE / HISTORICAL EVIDENCE | Historical consolidation checkpoint; one canonical DOC-ID and path |
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
| DOC-054 | P0 | 54 | Lệnh phân công song song Work 70 / Work 70 Parallel Assignment Order | 05_BUILD/00_ROOT/DOC-054_LENH-PHAN-CONG-SONG-SONG-WORK-70.md (main + branch: work/70/05-build) | DOC-001; DOC-042; DOC-043; DOC-044 | ACTIVE / DELIVERABLES RECEIVED — ACK STATUS MIXED / NO BUILD AUTHORIZATION | Phân công Ka, Co, Vi, Qw; Qw ACK được ghi trong DOC-067; Ka/Vi/An ACK vẫn phải xác minh riêng; không cấp quyền BUILD |
| DOC-055 | P0 | 55 | Sổ đăng ký tài liệu Work 70 / Work 70 Document Register | 00_ROOT/DOC-055_SO-DANG-KY-TAI-LIEU_WORK-70-DOCUMENT-REGISTER.md | DOC-001; DOC-038; DOC-039; DOC-040; DOC-056 | ACTIVE / SINGLE SOURCE OF TRUTH | Sổ duy nhất cho DOC-ID, metadata, canonical paths, branch/ref và trạng thái |
| DOC-056 | P0 | 56 | Quyết định chuẩn hóa hệ thống tài liệu Work 70 / Work 70 Document Standardization Policy | 00_ROOT/DOC-056_QUYET-DINH-CHUAN-HOA-HE-THONG-TAI-LIEU_WORK-70-DOCUMENT-STANDARDIZATION-POLICY.md | DOC-001; DOC-033; DOC-038; DOC-039; DOC-040; DOC-055 | ACTIVE / MIGRATION IN PROGRESS | Quy tắc thống nhất và batch migration toàn Work 70 |

| DOC-057 | P0 | 57 | Quy định cổng kiểm soát đầu vào Work / Work Entry Gate Standard | 00_ROOT/DOC-057_QUY-DINH-CONG-KIEM-SOAT-DAU-VAO_WORK-ENTRY-GATE-STANDARD.md | DOC-001; DOC-002; DOC-042; DOC-043; DOC-055 | ACTIVE / TECHNICAL ENFORCEMENT NOT VERIFIED | Cổng G0–G5, bằng chứng, quyền thao tác và hướng dẫn xử lý BLOCKED |
| DOC-058 | P1 | 58 | Báo cáo sự cố lệch đường dẫn Work 70 / Work 70 Path Drift Incident Report | 00_ROOT/DOC-058_BAO-CAO-SU-CO-LECH-DUONG-DAN_WORK-70-PATH-DRIFT-INCIDENT-REPORT.md | DOC-003; DOC-035; DOC-055; DOC-056 | INCIDENT CONFIRMED / REMEDIATION IN PROGRESS | Ghi nhận nguyên nhân, phạm vi ảnh hưởng, tác nhân đã được nhật ký xác nhận và phục hồi có kiểm soát |
| DOC-060 | P0 | 60 | Đề xuất chuẩn hóa mã cổng / Gate Namespace and Identifier Separation | 03_ARCHITECT/DOC-060_DE-XUAT-CHUAN-HOA-MA-CONG_GATE-NAMESPACE-AND-IDENTIFIER-SEPARATION.md | DOC-001; DOC-004; DOC-005; DOC-054; DOC-057 | PROPOSAL ONLY / NOT APPROVED | Đề xuất tách namespace cho Lifecycle, Work Entry và Integration Gate; chưa có hiệu lực cho đến khi Vinh quyết định |
| DOC-061 | P1 | 61 | Rà soát đối chiếu hợp đồng kiến trúc runtime Work 70 / Work 70 Runtime Architecture Contract Reconciliation | 05_BUILD/03_ARCHITECTURE/DOC-061_RA-SOAT-DOI-CHIEU-HOP-DONG-KIEN-TRUC-RUNTIME-WORK-70.md | DOC-004; DOC-005; DOC-010; DOC-033; DOC-049; DOC-054; DOC-055; DOC-060 | DRAFT — SOURCE RECONCILIATION COMPLETE / CONTRACT APPROVAL PENDING | Canonical path is the Work 70 main copy; Sandbox and work/70/05-build are sync/mirror locations only. Reconciles state machine, gate, Core runtime baseline, WEE/execution-host source, Dashboard authority, branch divergence and test contract; target contract/Vi trace/An QE pending; no implementation approval |
| DOC-062 | P0 | 62 | Đề xuất chuẩn hóa gói công việc / Work Package Baseline Reconciliation Proposal | 04_PLAN/DOC-062_DE-XUAT-CHUAN-HOA-GOI-CONG-VIEC_WORK-PACKAGE-BASELINE-RECONCILIATION-PROPOSAL.md | DOC-001; DOC-004; DOC-005; DOC-006; DOC-011; DOC-036; DOC-042; DOC-043; DOC-044; DOC-054; DOC-055; DOC-057; DOC-061 | HISTORICAL DRAFT — SUPERSEDED FOR BASELINE BY D68-01 / G4 NOT READY | Reconcile sáu WP giữa Work-level roadmap và Build Register candidate; không cấp quyền BUILD |
| DOC-063 | P0 | 63 | Kiến trúc thực thi Work Entry Authorization và DENY-to-RECOVERY / Work Entry Authorization & Deny Recovery Enforcement Blueprint | 03_ARCHITECT/DOC-063_KIEN-TRUC-THUC-THI_WORK-ENTRY-AUTHORIZATION-AND-DENY-RECOVERY.md | DOC-001; DOC-004; DOC-005; DOC-043; DOC-044; DOC-057; DOC-061; DOC-062 | DRAFT — DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED | Hợp đồng kỹ thuật đề xuất cho authorization tại điểm thực thi; bổ sung yêu cầu tách Recovery/Protected scope và commit-time authorization theo review Ka; P0.3/P0.4 DESIGN ONLY, chờ Core owner, Vi trace và An QE; không cấp quyền BUILD |

## Addendum 2026-11-02 — đăng ký DOC-064 đến DOC-066
| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-064 | P0 | 64 | Kiến trúc điều phối giao việc AI kết hợp / Hybrid AI Dispatch Architecture | 05_BUILD/03_ARCHITECT/DOC-064_KIEN-TRUC_DIEU-PHOI-GIAO-VIEC-AI_HYBRID-AI-DISPATCH-ARCHITECTURE.md | DOC-005; DOC-033; DOC-042; DOC-043; DOC-044; DOC-057; DOC-061; DOC-063 | DRAFT — TARGET ARCHITECTURE / IMPLEMENTATION NOT AUTHORIZED | Kiến trúc control plane, adapter modes, trust boundary, session continuity và rollout constraints |
| DOC-065 | P0 | 65 | Hợp đồng điều phối giao việc AI kết hợp / Hybrid AI Dispatch Contract | 05_BUILD/03_ARCHITECT/DOC-065_HOP-DONG_DIEU-PHOI-GIAO-VIEC-AI_HYBRID-DISPATCH-CONTRACT.md | DOC-043; DOC-044; DOC-057; DOC-064 | DRAFT — CONTRACT PROPOSAL | Logical payload, dispatch, ACK, progress, result, review, events, error model và acceptance invariants |
| DOC-066 | P0 | 66 | Kế hoạch triển khai và kiểm thử điều phối giao việc AI / AI Dispatch Implementation & Test Plan | 04_PLAN/DOC-066_KE-HOACH_TRIEN-KHAI-VA-KIEM-THU_DIEU-PHOI-GIAO-VIEC-AI.md | DOC-043; DOC-044; DOC-057; DOC-064; DOC-065 | DRAFT — PLANNED / IMPLEMENTATION NOT AUTHORIZED / TESTS NOT RUN | Nội dung đã được xác minh bằng Sandbox read_probe và đồng bộ độc lập lên GitHub main (commit bd55e162d8065efc7214ea8a08cf41c9e6bf84de); chưa có dispatch, ACK hoặc test thực thi |

Ghi chú cập nhật 2026-11-02: DOC-054, DOC-064, DOC-065 và DOC-067 đã được đồng bộ độc lập từ Sandbox/Build branch sang GitHub main, không merge/rebase toàn nhánh. DOC-064/065 là DRAFT; DOC-067 là test plan, execution BLOCKED. DOC-066 từng không đọc được ở lần probe trước; lần kiểm tra tiếp theo xác minh file thực sự tồn tại trong Sandbox và đã đồng bộ nguyên văn lên GitHub main (commit bd55e162d8065efc7214ea8a08cf41c9e6bf84de). DOC-066 vẫn là kế hoạch DRAFT, chưa có dispatch, ACK hoặc test thực thi. Không tài liệu nào ở đây tự chứng minh runtime test hoặc quyền BUILD.

| DOC-067 | P0 | 67 | Kế hoạch kiểm thử độc lập WP70-QA / Independent QA Test Plan | 06_VERIFY/DOC-067_KE-HOACH-KIEM-THU-DOC-LAP_WP70-QA_INDEPENDENT_QA_TEST_PLAN.md | DOC-001; DOC-004; DOC-005; DOC-042; DOC-043; DOC-054; DOC-061; DOC-063 | ACTIVE / PREPARATION COMPLETE / EXECUTION BLOCKED | Test strategy, contract tests, negative/security, race/idempotency, E2E matrix; không sửa code để làm test xanh |

## Addendum 2026-11-02 — đăng ký DOC-068
| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-068 | P0 | 68 | Đề xuất hợp nhất roadmap và đích bàn giao Work 70 / Work 70 Roadmap & Delivery Target Reconciliation Proposal | 04_PLAN/DOC-068_DE-XUAT-HOP-NHAT-ROADMAP-WORK-70.md | DOC-001; DOC-006; DOC-011; DOC-062; DOC-064; DOC-065; DOC-066; DOC-067 | DECIDED BY XU UNDER D70-018 / G4 BUILD NOT READY | Giữ 6 WP IDs chuẩn, ánh xạ 8 sub-deliverables SD-01..SD-08; quyết định baseline điều phối, không mở BUILD |


## Addendum 2026-11-02 — đăng ký DOC-069
| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-069 | P0 | 69 | Hồ sơ nhận việc và phạm vi quyền Xu / Xu Work Entry Record | 00_ROOT/DOC-069_HO-SO-NHAN-VIEC-VA-PHAM-VI-QUYEN-XU_WORK-ENTRY-RECORD.md | DOC-001; DOC-006; DOC-033; DOC-038; DOC-039; DOC-040; DOC-042; DOC-043; DOC-044; DOC-055; DOC-056; DOC-057 | PASS — LIMITED DOCUMENTATION / READ-ONLY TRACE SCOPE | Xác định participant AI-01, assignment ASG-W70-XU-20261102-01, WE-G0..WE-G5 theo DOC-057; không mở G4 BUILD hoặc quyền code/runtime. |

| DOC-070 | P1 | 70 | Đề xuất sổ đăng ký gói công việc / Work Package Register Proposal | 04_PLAN/DOC-070_DE-XUAT-SO-DANG-KY-GOI-CONG-VIEC_WORK-PACKAGE-REGISTER-PROPOSAL.md | DOC-001; DOC-006; DOC-011; DOC-036; DOC-055; DOC-061 | DRAFT — NOT APPROVED / SUPPORTING RECONCILIATION ONLY | Đề xuất cấu trúc sổ WP cấp Work; dữ liệu và schema hỗ trợ vẫn là draft, không thay DOC-011 và không mở G4/BUILD |
| DOC-071 | P0 | 71 | Báo cáo truy vết Core authority, runtime composition và persistence / Core Authority, Runtime Composition & Persistence Trace | EVIDENCE/DOC-071_BAO-CAO-TRUY-VET_CORE-AUTHORITY-RUNTIME-AND-PERSISTENCE.md | DOC-001; DOC-011; DOC-035; DOC-055; DOC-061; DOC-066 | SOURCE TRACE COMPLETE — READ-ONLY / CORE OWNER NOT IDENTIFIED / RUNTIME NOT VERIFIED | Xác định ranh giới Meeting/Identity với Work authority; ghi rõ HTTP factory chưa xác minh được wiring runtime, Meeting file persistence không chứng minh Work persistence; không cấp BUILD |
| DOC-072 | P0 | 72 | Đối chiếu hợp đồng kiến trúc DOC-061/063/064/065 / Architecture Contract Reconciliation | EVIDENCE/DOC-072_DOI-CHIEU_HOP-DONG-KIEN-TRUC_DOC-061_063_064_065.md | DOC-004; DOC-005; DOC-010; DOC-011; DOC-035; DOC-054; DOC-057; DOC-061; DOC-063; DOC-064; DOC-065; DOC-066; DOC-071 | RECONCILIATION COMPLETE — DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED | Làm rõ Core authority, Work Entry auth, Hybrid Dispatch và logical contract là các lớp mục tiêu; không chứng minh API/runtime/adapter, không mở G4/BUILD |
| DOC-084 | P0 | 84 | Báo cáo rà soát hiện trạng và lộ trình khắc phục Work 70 / Work 70 Readiness & Remediation Report | EVIDENCE/DOC-084_BAO-CAO-RA-SOAT-HIEN-TRANG-VA-LO-TRINH-KHAC-PHUC_WORK70-READINESS-AND-REMEDIATION-REPORT.md | DOC-001; DOC-004; DOC-005; DOC-035; DOC-055; DOC-057; DOC-063; DOC-067; DOC-071; DOC-072 | ACTIVE — READINESS AUDIT RECORDED / IMPLEMENTATION AND INDEPENDENT VERIFICATION OPEN | Readiness snapshot and remediation backlog; does not replace governance audit or independent QA plan |

## Supporting data artifacts — WP registry draft (2026-11-02)
- `04_PLAN/WORK_PACKAGE_REGISTER.json` — GitHub main blob `462cf3528375d59c322a4efbdbc9b2f7eecb8cf9`; six records, schema_version `0.1-draft`, baseline `DRAFT_NOT_APPROVED`; Sandbox copy restored during this reconciliation.
- `03_ARCHITECT/WORK_PACKAGE.schema.json` — GitHub main blob `47a2e881ad6ed28af1aaf4795585346a4c8881d4`; draft envelope schema for the Work-level register; Sandbox copy restored during this reconciliation.
- `05_BUILD/00_ROOT/WORK_PACKAGE.schema.json` on `work/70/05-build` — blob `28ee2a1d6ba952c2fa1a1d737c5ff8892319a55e`; distinct per-record candidate schema, not interchangeable with the envelope schema.
- These files are discoverable supporting artifacts, not an approved registry/schema baseline. DOC-011 remains the active planning authority; G0/G1/G4 statuses are unchanged.


## Unresolved DOC-ID collision — 2026-11-02
**Status: CONFIRMED / DECISION REQUIRED / NO FILE MUTATION**

Inventory found 11 substantive root-level GitHub main documents named DOC-042..DOC-052 whose titles/content differ from the current canonical assignments in this register. The Sandbox contains the current canonical DOC-042..044 and phase playbooks DOC-045..DOC-053; GitHub main still contains the older root-level files. The current register rows remain the planning baseline, but this does not resolve the identity collision or authorize renumbering/deletion.

Affected legacy GitHub main paths:
- `00_ROOT/DOC-042_QUY-TRINH-KHAM-PHA_DISCOVER-PROCESS.md`
- `00_ROOT/DOC-043_QUY-TRINH-XAC-DINH-YEU-CAU_DEFINE-PROCESS.md`
- `00_ROOT/DOC-044_QUY-TRINH-THIET-KE-KIEN-TRUC_ARCHITECT-PROCESS.md`
- `00_ROOT/DOC-045_QUY-TRINH-LAP-KE-HOACH_PLAN-PROCESS.md`
- `00_ROOT/DOC-046_QUY-TRINH-THI-CONG_BUILD-PROCESS.md`
- `00_ROOT/DOC-047_QUY-TRINH-KIEM-CHUNG_VERIFY-PROCESS.md`
- `00_ROOT/DOC-048_QUY-TRINH-QUAN-LY-BANG-CHUNG_EVIDENCE-PROCESS.md`
- `00_ROOT/DOC-049_QUY-TRINH-NGHIEM-THU_ACCEPTANCE-PROCESS.md`
- `00_ROOT/DOC-050_QUY-TRINH-PHAT-HANH_RELEASE-PROCESS.md`
- `00_ROOT/DOC-051_QUY-TRINH-VAN-HANH_OPERATE-PROCESS.md`
- `00_ROOT/DOC-052_BAO-CAO-KIEM-DINH-TICH-HOP_QUAN-TRI_INTEGRATION-GOVERNANCE-VERIFICATION.md`

No DOC-ID has been reassigned and no legacy content has been overwritten or deleted. Keep the register in DRAFT reconciliation status for this issue until Vinh decides the identity disposition. See DOC-041 G-008 and DOC-035 event 031.


## Addendum 2026-11-02 — PO-delegated DOC-ID disposition and partial migration
**Decision: APPROVED BY XU UNDER EXPLICIT DELEGATION FROM VINH.** Preserve the current Work 70 canonical DOC-042..DOC-053 assignments. Re-identify the 11 substantive legacy GitHub main process documents as DOC-073..DOC-083, preserving their original contents and history. Mapping: old DOC-042→new DOC-073 Discover; DOC-043→DOC-074 Define; DOC-044→DOC-075 Architect; DOC-045→DOC-076 Plan; DOC-046→DOC-077 Build; DOC-047→DOC-078 Verify; DOC-048→DOC-079 Evidence; DOC-049→DOC-080 Acceptance; DOC-050→DOC-081 Release; DOC-051→DOC-082 Operate; DOC-052→DOC-083 Integration & Governance Verification.

**Execution status: PARTIAL / MIGRATION NOT COMPLETE.** GitHub main currently contains newly created copies DOC-073, DOC-074, DOC-075 and DOC-077. DOC-076 and DOC-078..DOC-083 have not been created because tool safety checks blocked those write attempts. Original DOC-042..DOC-052 files remain unchanged; no aliases, renames or deletions have been performed. Do not treat this addendum as proof of completed migration. The four created copies and updated DOC-055/DOC-041/DOC-035 have since been synchronized to Sandbox 8030 and exact readback matched GitHub content; the remaining seven copies, aliases and link reconciliation are still outstanding. Continue only through permitted operations; do not attempt to bypass a safety block. Reconcile remaining files, inbound links, aliases, exact readback and Sandbox parity before declaring completion.


## DOC-ID migration allocation ledger — 2026-11-02

| Legacy source ID/path | New assigned ID | New canonical copy path | GitHub main | Sandbox 8030 | Legacy source |
|---|---|---|---|---|---|
| DOC-042 `00_ROOT/DOC-042_QUY-TRINH-KHAM-PHA_DISCOVER-PROCESS.md` | DOC-073 | `00_ROOT/DOC-073_QUY-TRINH-KHAM-PHA_DISCOVER-PROCESS.md` | CREATED — verified | SYNCED — exact readback | PRESERVED — unchanged |
| DOC-043 `00_ROOT/DOC-043_QUY-TRINH-XAC-DINH-YEU-CAU_DEFINE-PROCESS.md` | DOC-074 | `00_ROOT/DOC-074_QUY-TRINH-XAC-DINH-YEU-CAU_DEFINE-PROCESS.md` | CREATED — verified | SYNCED — exact readback | PRESERVED — unchanged |
| DOC-044 `00_ROOT/DOC-044_QUY-TRINH-THIET-KE-KIEN-TRUC_ARCHITECT-PROCESS.md` | DOC-075 | `00_ROOT/DOC-075_QUY-TRINH-THIET-KE-KIEN-TRUC_ARCHITECT-PROCESS.md` | CREATED — verified | SYNCED — exact readback | PRESERVED — unchanged |
| DOC-045 `00_ROOT/DOC-045_QUY-TRINH-LAP-KE-HOACH_PLAN-PROCESS.md` | DOC-076 | `00_ROOT/DOC-076_QUY-TRINH-LAP-KE-HOACH_PLAN-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-046 `00_ROOT/DOC-046_QUY-TRINH-THI-CONG_BUILD-PROCESS.md` | DOC-077 | `00_ROOT/DOC-077_QUY-TRINH-THI-CONG_BUILD-PROCESS.md` | CREATED — verified | SYNCED — exact readback | PRESERVED — unchanged |
| DOC-047 `00_ROOT/DOC-047_QUY-TRINH-KIEM-CHUNG_VERIFY-PROCESS.md` | DOC-078 | `00_ROOT/DOC-078_QUY-TRINH-KIEM-CHUNG_VERIFY-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-048 `00_ROOT/DOC-048_QUY-TRINH-QUAN-LY-BANG-CHUNG_EVIDENCE-PROCESS.md` | DOC-079 | `00_ROOT/DOC-079_QUY-TRINH-QUAN-LY-BANG-CHUNG_EVIDENCE-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-049 `00_ROOT/DOC-049_QUY-TRINH-NGHIEM-THU_ACCEPTANCE-PROCESS.md` | DOC-080 | `00_ROOT/DOC-080_QUY-TRINH-NGHIEM-THU_ACCEPTANCE-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-050 `00_ROOT/DOC-050_QUY-TRINH-PHAT-HANH_RELEASE-PROCESS.md` | DOC-081 | `00_ROOT/DOC-081_QUY-TRINH-PHAT-HANH_RELEASE-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-051 `00_ROOT/DOC-051_QUY-TRINH-VAN-HANH_OPERATE-PROCESS.md` | DOC-082 | `00_ROOT/DOC-082_QUY-TRINH-VAN-HANH_OPERATE-PROCESS.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |
| DOC-052 `00_ROOT/DOC-052_BAO-CAO-KIEM-DINH-TICH-HOP_QUAN-TRI_INTEGRATION-GOVERNANCE-VERIFICATION.md` | DOC-083 | `00_ROOT/DOC-083_BAO-CAO-KIEM-DINH-TICH-HOP_QUAN-TRI_INTEGRATION-GOVERNANCE-VERIFICATION.md` | BLOCKED — safety check | NOT CREATED | PRESERVED — unchanged |

**Control note:** DOC-073..DOC-083 are reserved mappings under the PO-delegated decision; reservation is not proof that a file exists. Only DOC-073, DOC-074, DOC-075 and DOC-077 have verified copies in GitHub main and Sandbox 8030. The seven blocked copies remain uncreated. No legacy file has been renamed, deleted, overwritten or converted into an alias. Inbound-link reconciliation and alias registration remain OPEN. Do not use an absent new path as a replacement link; retain the original source path until a corresponding copy is created and verified.


## Bounded inbound-reference search — 2026-11-02

Exact-basename GitHub code searches were run for each of the 11 legacy source filenames. Each query returned only this register as a match, because the register itself lists the legacy paths. This is a bounded search-index result, not proof that no inbound references exist: code-search indexing/coverage may be incomplete and the query was not a full repository-wide parsed-link audit. Therefore inbound-link reconciliation remains OPEN. Keep original source paths valid and do not replace references with uncreated DOC-076 or DOC-078..DOC-083 paths. For the four created copies, links may be updated only where a verified source reference is identified and the target path is confirmed.


## Sandbox canonical-path correction — 2026-11-02

**Correction to prior synchronization evidence:** A subsequent full Sandbox listing and dual-path probe showed that the earlier DOC-073/074/075/077 copies and one prior set of metadata snapshots had been written/read under the nested Sandbox path `work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/00_ROOT/`, not the Work Sandbox canonical root `ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/00_ROOT/`. The earlier exact-readback result therefore verified the nested copies, not the canonical root. This is a path-selection error; do not rely on the earlier event 033 statement as proof of canonical-root parity.

**Remediation performed:** DOC-041 and DOC-073, DOC-074, DOC-075, DOC-077 were copied from GitHub main into the canonical Sandbox root and read back byte-for-byte. DOC-035 and DOC-055 were independently probed and already matched the current GitHub main content at the canonical root. Thus all seven relevant documents (DOC-035, DOC-041, DOC-055, DOC-073, DOC-074, DOC-075, DOC-077) now have exact canonical-root Sandbox parity.

**Residual path drift:** The nested `work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/00_ROOT/` copies remain as duplicate/orphaned paths. They are preserved pending an explicit cleanup authorization and verified impact assessment; no deletion was performed. The canonical path remains the top-level Work root path stated above. Future Sandbox operations must omit the extra `work/70/` prefix.


| DOC-086 | P1 | 86 | Kiến trúc kho tri thức công nghệ và năng lực AI / AI Technology Knowledge & Capability Architecture | 03_ARCHITECT/DOC-086_KIEN-TRUC_KHO-TRI-THUC-CONG-NGHE-VA-NANG-LUC-AI_AI-TECHNOLOGY-KNOWLEDGE-AND-CAPABILITY-ARCHITECTURE.md | DOC-001; DOC-002; DOC-006; DOC-028; DOC-033; DOC-043; DOC-055 | BASELINE APPROVED — REGISTRY IMPLEMENTATION NOT STARTED | Taxonomy công nghệ AI, quy tắc capability registry, bằng chứng xác minh và liên kết ứng dụng với các Work; không tự phê duyệt tích hợp/model/API |


| DOC-087 | P1 | 87 | Kế hoạch triển khai sổ đăng ký năng lực AI / AI Capability Registry Implementation Plan | 04_PLAN/DOC-087_KE-HOACH_TRIEN-KHAI-SO-DANG-KY-NANG-LUC-AI_AI-CAPABILITY-REGISTRY-IMPLEMENTATION-PLAN.md | DOC-001; DOC-006; DOC-035; DOC-043; DOC-055; DOC-086 | PHASE 1 DATA CONTRACT CREATED — RUNTIME/API/UI NOT STARTED | Quy trình triển khai, trạng thái năng lực, quy tắc an toàn, test plan và điều kiện mở rộng Registry |


| DOC-088 | P1 | 88 | Báo cáo rà soát hợp đồng Dashboard Work 70 của Ka / Ka Work 70 Dashboard Contract Review | 05_BUILD/03_ARCHITECTURE/DOC-088_KA_WORK70_DASHBOARD_CONTRACT_REVIEW_20261107.md | DOC-010; DOC-085; DOC-061; DOC-063; DOC-035 | ACCEPT WITH CONDITIONS — STATIC BROWSER E2E ONLY; FORMAL QE BLOCKED | Kết quả rà soát kiến trúc, provenance, schema, freshness và điều kiện E2E |
| DOC-089 | P0 | 89 | Kiến trúc hệ thống Preview Host dùng chung / Shared Dashboard Preview Host Architecture | 05_BUILD/03_ARCHITECTURE/DOC-089_KIEN-TRUC_HE-THONG_PREVIEW-HOST_DASHBOARD-PREVIEW-HOST-ARCHITECTURE.md | DOC-001; DOC-003; DOC-009; DOC-010; DOC-085; DOC-088 | DESIGN BASELINE — DEPLOYMENT NOT VERIFIED | Kiến trúc phục vụ Dashboard HTML thực cho nhiều Work, read-only, registry allowlist và private access |
| DOC-090 | P0 | 90 | Kế hoạch triển khai và nghiệm thu Preview Host / Preview Host Implementation and Acceptance Plan | 04_PLAN/DOC-090_KE-HOACH_TRIEN-KHAI_PREVIEW-HOST_IMPLEMENTATION-AND-ACCEPTANCE-PLAN.md | DOC-035; DOC-088; DOC-089 | ACTIVE — LOCAL HOST AND PC/MOBILE E2E NOT RUN | Lộ trình triển khai P1, test matrix, bảo vệ và tiêu chí nghiệm thu |


## Canonical register reconciliation — 2026-11-07

The PO-delegated disposition recorded in the 2026-11-02 addendum remains in force. The following four migrated copies are present in GitHub `main` and are now registered as the canonical documents for their assigned new DOC-IDs. The legacy source paths remain preserved and are not canonical copies.

| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-073 | P1 | 73 | Quy trình khám phá / Discover Process | 00_ROOT/DOC-073_QUY-TRINH-KHAM-PHA_DISCOVER-PROCESS.md | DOC-001; DOC-002; DOC-004; DOC-007; DOC-033; DOC-038 | CANONICAL COPY — LEGACY DOC-042 SOURCE PRESERVED | Canonical Discover process; legacy source is DOC-042_QUY-TRINH-KHAM-PHA_DISCOVER-PROCESS.md and must not be used as a second DOC-042 document |
| DOC-074 | P1 | 74 | Quy trình xác định yêu cầu / Define Process | 00_ROOT/DOC-074_QUY-TRINH-XAC-DINH-YEU-CAU_DEFINE-PROCESS.md | DOC-001; DOC-002; DOC-004; DOC-005; DOC-007; DOC-008; DOC-073 | CANONICAL COPY — LEGACY DOC-043 SOURCE PRESERVED | Canonical Define process; legacy source is DOC-043_QUY-TRINH-XAC-DINH-YEU-CAU_DEFINE-PROCESS.md |
| DOC-075 | P1 | 75 | Quy trình thiết kế kiến trúc / Architect Process | 00_ROOT/DOC-075_QUY-TRINH-THIET-KE-KIEN-TRUC_ARCHITECT-PROCESS.md | DOC-001; DOC-002; DOC-004; DOC-005; DOC-008; DOC-009; DOC-010; DOC-033; DOC-038; DOC-074 | CANONICAL COPY — LEGACY DOC-044 SOURCE PRESERVED | Canonical Architect process; legacy source is DOC-044_QUY-TRINH-THIET-KE-KIEN-TRUC_ARCHITECT-PROCESS.md |
| DOC-077 | P1 | 77 | Quy trình thi công / Build Process | 00_ROOT/DOC-077_QUY-TRINH-THI-CONG_BUILD-PROCESS.md | DOC-001; DOC-002; DOC-004; DOC-005; DOC-009; DOC-011; DOC-033; DOC-036; DOC-038; DOC-075; DOC-076 | REGISTERED — DOC-076 DEPENDENCY ABSENT / NOT READY | Canonical Build process copy; legacy source DOC-046 is preserved; DOC-076 Plan Process is not present, so this dependency remains unresolved and this row does not authorize BUILD |

**Registration boundary:** DOC-076 and DOC-078..DOC-083 remain reserved mappings only; their canonical files do not exist in the current GitHub tree and they are not registered as available documents. Do not link to or claim those paths as present. DOC-042 remains End-to-End Execution Orchestration, DOC-043 remains AI Role & Permission Matrix, and DOC-044 remains Work Assignment Contract Template at their respective registered paths. This reconciles identity at the register level without rewriting or deleting preserved legacy source files.

**Verification scope:** GitHub `main` tree inspection (`truncated=false`) and exact file fetch confirmed the four canonical copies DOC-073, DOC-074, DOC-075 and DOC-077 exist. This is not proof of inbound-link closure, legacy alias conversion, Sandbox parity, or full migration completion; those remain OPEN under DOC-056 and the migration ledger above.


## Canonical evidence-path migration — 2026-11-07
D70-021 changes the top-level cross-phase evidence directory to `EVIDENCE/`. DOC-014 has exactly one canonical path: `EVIDENCE/EVIDENCE_REGISTER.json`. The Markdown file is a read-only projection and the schema is a technical validator, not another register. DOC-031, DOC-071, DOC-072 and DOC-084 canonical paths now begin with `EVIDENCE/`. `05_BUILD/06_EVIDENCE/` remains staging and is not changed. Old top-level `06_EVIDENCE/` paths are compatibility-only pending link closure and QE.


## One-source clarification — DOC-013 (2026-11-07)
DOC-013 has one canonical artifact path only: `branch work/70/05-build: 05_BUILD/00_ROOT/BUILD_REGISTER.json`. `BUILD_REGISTER.md` is a read-only projection; schema files are technical validation artifacts, not additional registers. DOC-013 remains a migration candidate and is not the canonical Work-level WP plan; DOC-011/04_PLAN remain the planning authority.


## One-source clarification — DOC-061 (2026-11-07)
DOC-061 has one canonical Work 70 path on main: `05_BUILD/03_ARCHITECTURE/DOC-061_RA-SOAT-DOI-CHIEU-HOP-DONG-KIEN-TRUC-RUNTIME-WORK-70.md`. Sandbox and `work/70/05-build` locations are synchronization/mirror references, not additional canonical sources.


## Registration addendum — DOC-094 / 2026-11-09
## Addendum 2026-11-09 — đăng ký DOC-094 và projection ba tầng
| DOC-094 | P0 | 94 | Sổ Product Task và Phase Task / Product and Phase Task Register | 04_PLAN/DOC-094_PRODUCT_PHASE_TASK_REGISTER.json | DOC-004; DOC-005; DOC-006; DOC-034; DOC-035; DOC-056; DOC-093 | DRAFT_NOT_APPROVED | Nguồn chuẩn Product Task và Phase Task; quy định Agent chính, phối hợp, kiểm tra; liên kết xuống DOC-093; không thay thế Agent Task register. |
| SCHEMA-PRODUCT-PHASE-TASK | P1 | 94A | Product and Phase Task Register Schema | 03_ARCHITECT/DOC-094_PRODUCT_PHASE_TASK_REGISTER.schema.json | DOC-093; DOC-094 | CREATED / VALIDATION NOT RUN | Schema kiểm tra DOC-094; không phải nguồn dữ liệu. |
| DASHBOARD-PRODUCT-PHASE-TASK | P1 | 94B | Product and Phase Task Dashboard Projection | DASHBOARD/execution/PRODUCT_PHASE_TASK_STATUS.json | DOC-093; DOC-094 | GENERATED / READ-ONLY / BROWSER NOT VERIFIED | Projection ba tầng cho Dashboard; không chỉnh sửa trực tiếp, không phải nguồn chuẩn. |
