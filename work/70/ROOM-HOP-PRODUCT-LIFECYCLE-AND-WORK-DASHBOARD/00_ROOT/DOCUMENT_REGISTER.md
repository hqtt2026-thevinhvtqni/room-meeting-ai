# WORK 70 — DOCUMENT REGISTER
Register version: 1.5
Owner: Xu / AI-01
Authority: Vinh
Rule: STT is a stable identity; Priority is importance; Read order is sequence. File paths are not renamed by this register.

| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-001 | P0 | 1 | Work Manifest | 00_ROOT/WORK_MANIFEST.md | NONE | ACTIVE | Identity, authority, scope, state and source boundaries; always first |
| DOC-002 | P0 | 2 | AI Project Intake & Execution Standard | 00_ROOT/AI_PROJECT_INTAKE_STANDARD.md | DOC-001 | ACTIVE | Mandatory intake and AI behavior |
| DOC-003 | P0 | 3 | Repository Layout & Sync | 00_ROOT/REPOSITORY_LAYOUT_AND_SYNC.md | DOC-001 | ACTIVE | Branch, Sandbox, canonical ownership and sync boundaries |
| DOC-004 | P0 | 4 | Lifecycle Gate Matrix | 00_ROOT/LIFECYCLE_GATE_MATRIX.md | DOC-001 | ACTIVE | Gate and transition conditions |
| DOC-005 | P0 | 5 | State Machine | 00_ROOT/STATE_MACHINE.md | DOC-004 | ACTIVE | Legal states and transitions |
| DOC-006 | P0 | 6 | Decision Log | 00_ROOT/DECISION_LOG.md | DOC-001 | ACTIVE | Binding decisions and rationale |
| DOC-033 | P0 | 7 | Work Documentation & Storage Standard | 00_ROOT/WORK_DOCUMENTATION_AND_STORAGE_STANDARD.md | DOC-001; DOC-002; DOC-003 | ACTIVE | Four official records, canonical ownership, mapping and storage rules |
| DOC-038 | P0 | 8 | Quy trình đặt tên tài liệu / Document Naming Standard | 00_ROOT/DOCUMENT_NAMING_STANDARD.md | DOC-001; DOC-002; DOC-003; DOC-033 | ACTIVE | Vietnamese-first bilingual naming, stable IDs, filename pattern and controlled legacy renames |
| DOC-007 | P1 | 9 | Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DOC-001 | ACTIVE | Problem, users, evidence and assumptions |
| DOC-008 | P1 | 10 | Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DOC-007 | ACTIVE | Scope, requirements and acceptance criteria |
| DOC-009 | P1 | 11 | Work Lifecycle Architecture | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | DOC-008 | ACTIVE | Product lifecycle and system architecture |
| DOC-010 | P1 | 12 | Dashboard Core Read Contract | 03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md | DOC-009 | ACTIVE | Core/Dashboard boundary and read-only contract |
| DOC-011 | P1 | 13 | Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DOC-008; DOC-009 | ACTIVE | Delivery sequence and milestones |
| DOC-012 | P1 | 14 | Work Instantiation & Migration | 04_PLAN/WORK_INSTANTIATION_AND_MIGRATION.md | DOC-003; DOC-009 | ACTIVE | How to create/migrate a Work safely |
| DOC-013 | P1 | 15 | Legacy Build Register (WP candidate) | 05_BUILD/00_ROOT/BUILD_REGISTER.json; BUILD_REGISTER.md | DOC-033; DOC-011 | MIGRATION PENDING | Existing WP records; candidate for reconciliation into Work-level plan, not yet a canonical mapping |
| DOC-036 | P1 | 16 | Build Mapping Register | 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md | DOC-001; DOC-003; DOC-033 | ACTIVE / MIGRATION IN PROGRESS | Maps engineering artifacts to canonical Work/source paths and classifies legacy build files |
| DOC-014 | P1 | 17 | Evidence Register | 06_EVIDENCE/EVIDENCE_REGISTER.json; EVIDENCE_REGISTER.md | DOC-004; DOC-033 | ACTIVE | Cross-phase canonical evidence and provenance |
| DOC-015 | P1 | 18 | Verification Plan | 06_VERIFY/VERIFICATION_PLAN.md | DOC-008; DOC-013; DOC-014 | ACTIVE | Verification strategy and coverage |
| DOC-016 | P1 | 19 | Storage & Export Architecture | 05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | DOC-009; DOC-010; DOC-033 | CANONICAL CANDIDATE / MIGRATION PENDING | Technical design; reconcile into 03_ARCHITECT before any build copy is retired |
| DOC-017 | P1 | 20 | Core Capability Gap Assessment | 05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | DOC-010; DOC-033 | CANONICAL CANDIDATE / MIGRATION PENDING | Evidence-based Core capability assessment; reconcile into Work-level architecture/verification record |
| DOC-018 | P2 | 21 | Migration Plan | 04_PLAN/MIGRATION_PLAN.md | DOC-012; DOC-033 | ACTIVE | Execution steps for approved migration |
| DOC-019 | P2 | 22 | Verification Checklist | 06_VERIFY/VERIFICATION_CHECKLIST.md | DOC-015 | ACTIVE | Operational verification checklist |
| DOC-020 | P2 | 23 | Acceptance Record | 07_ACCEPT/ACCEPTANCE_RECORD.md | DOC-015; DOC-019 | ACTIVE | Authorized acceptance decision |
| DOC-021 | P2 | 24 | Release Plan | 08_RELEASE/RELEASE_PLAN.md | DOC-020 | ACTIVE | Controlled release preparation |
| DOC-022 | P2 | 25 | Operations Model | 09_OPERATE/OPERATIONS_MODEL.md | DOC-021 | ACTIVE | Post-release operations |
| DOC-023 | P2 | 26 | Project Intake Report Template | 00_ROOT/PROJECT_INTAKE_REPORT_TEMPLATE.md | DOC-001; DOC-002 | ACTIVE | Required consistent intake report |
| DOC-024 | P2 | 27 | Storage & Export Acceptance | 05_BUILD/05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | DOC-016; DOC-015 | CANONICAL CANDIDATE / MIGRATION PENDING | Test plan candidate for 06_VERIFY; NOT EXECUTED |
| DOC-025 | P2 | 28 | AI Participants & Token Usage | 05_BUILD/00_ROOT/AI_PARTICIPANTS_AND_TOKEN_USAGE.md | DOC-002 | LEGACY / REFERENCE | Audit accuracy and retention need; roster is not participation proof |
| DOC-034 | P2 | 29 | Biên bản Work | 00_ROOT/BIEN_BAN.md | DOC-001; DOC-006; DOC-033 | ACTIVE | Official minutes register; binding decisions link to DECISION_LOG |
| DOC-035 | P2 | 30 | Nhật ký thi công Work | 00_ROOT/NHAT_KY_THI_CONG.md | DOC-001; DOC-002; DOC-033 | ACTIVE | Chronological Work-wide execution record |
| DOC-026 | P3 | 31 | Lifecycle Guide (Vietnamese) | 00_ROOT/LIFECYCLE_GUIDE_VI.md | DOC-004; DOC-005 | ACTIVE | Human-readable explanation of lifecycle |
| DOC-027 | P3 | 32 | Work Standard Versioning | 00_ROOT/WORK_STANDARD_VERSIONING.md | DOC-001 | ACTIVE | Version history and compatibility |
| DOC-028 | P3 | 33 | Vietnamese Glossary | 00_ROOT/VIETNAMESE_GLOSSARY.md | DOC-002 | ACTIVE | Terminology reference |
| DOC-029 | P3 | 34 | Legacy Scaffold Notice | LEGACY_SCAFFOLD_NOTICE.md | DOC-001 | ACTIVE | Historical/legacy context |
| DOC-030 | P3 | 35 | Work 70 Session Log | 05_BUILD/10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | DOC-002; DOC-033 | LEGACY / HISTORICAL | Preserve detail; Work-wide chronological record is 00_ROOT/NHAT_KY_THI_CONG.md |
| DOC-031 | P3 | 36 | Consolidation Evidence Report | 06_EVIDENCE/WORK70_CONSOLIDATION_CHECK_20261030.md | DOC-014 | ACTIVE | Historical evidence of Work 70 consolidation |
| DOC-032 | P3 | 37 | Dashboard README | DASHBOARD/README.md | DOC-010 | ACTIVE | Dashboard usage and limitations |
| DOC-037 | P3 | 38 | Work 70 README | README.md | DOC-001; DOC-033; DOC-036 | ACTIVE | Human-readable entry point; subordinate to Manifest and standards |

## AI reading rule
Read DOC-001 through DOC-006, then DOC-033. Then read relevant P1 documents in ascending read order. Read P2 only for the active task. Read P3 when clarification, operations or historical trace requires it. Never infer PASS from the register or presence of a file.

## Maintenance
When adding a document: allocate the next unused DOC ID, set priority/read order/dependencies, add one row here, and add required metadata below the title. Do not rename files to encode STT. A document located under 05_BUILD is not canonical solely because of its path; its authority must be explicitly declared by this standard and mapping register.
