# WORK 70 — DOCUMENT REGISTER
Register version: 1.1
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
| DOC-007 | P1 | 8 | Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DOC-001 | ACTIVE | Problem, users, evidence and assumptions |
| DOC-008 | P1 | 9 | Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DOC-007 | ACTIVE | Scope, requirements and acceptance criteria |
| DOC-009 | P1 | 10 | Work Lifecycle Architecture | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | DOC-008 | ACTIVE | Product lifecycle and system architecture |
| DOC-010 | P1 | 11 | Dashboard Core Read Contract | 03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md | DOC-009 | ACTIVE | Core/Dashboard boundary and read-only contract |
| DOC-011 | P1 | 12 | Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DOC-008; DOC-009 | ACTIVE | Delivery sequence and milestones |
| DOC-012 | P1 | 13 | Work Instantiation & Migration | 04_PLAN/WORK_INSTANTIATION_AND_MIGRATION.md | DOC-003; DOC-009 | ACTIVE | How to create/migrate a Work safely |
| DOC-013 | P1 | 14 | Build Mapping Register | 05_BUILD/00_ROOT/BUILD_REGISTER.json; BUILD_REGISTER.md | DOC-033; DOC-011 | ACTIVE | Engineering WP-to-area mapping; must not become competing canonical plan |
| DOC-014 | P1 | 15 | Evidence Register | 06_EVIDENCE/EVIDENCE_REGISTER.json; EVIDENCE_REGISTER.md | DOC-004; DOC-033 | ACTIVE | Cross-phase canonical evidence and provenance |
| DOC-015 | P1 | 16 | Verification Plan | 06_VERIFY/VERIFICATION_PLAN.md | DOC-008; DOC-013; DOC-014 | ACTIVE | Verification strategy and coverage |
| DOC-016 | P1 | 17 | Storage & Export Architecture | 05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | DOC-009; DOC-010; DOC-033 | ACTIVE | Legacy technical design; canonical-source classification/migration pending |
| DOC-017 | P1 | 18 | Core Capability Gap Assessment | 05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | DOC-010; DOC-033 | ACTIVE | Evidence-based Core capability gaps; classification/migration pending |
| DOC-018 | P2 | 19 | Migration Plan | 04_PLAN/MIGRATION_PLAN.md | DOC-012; DOC-033 | ACTIVE | Execution steps for approved migration |
| DOC-019 | P2 | 20 | Verification Checklist | 06_VERIFY/VERIFICATION_CHECKLIST.md | DOC-015 | ACTIVE | Operational verification checklist |
| DOC-020 | P2 | 21 | Acceptance Record | 07_ACCEPT/ACCEPTANCE_RECORD.md | DOC-015; DOC-019 | ACTIVE | Authorized acceptance decision |
| DOC-021 | P2 | 22 | Release Plan | 08_RELEASE/RELEASE_PLAN.md | DOC-020 | ACTIVE | Controlled release preparation |
| DOC-022 | P2 | 23 | Operations Model | 09_OPERATE/OPERATIONS_MODEL.md | DOC-021 | ACTIVE | Post-release operations |
| DOC-023 | P2 | 24 | Project Intake Report Template | 00_ROOT/PROJECT_INTAKE_REPORT_TEMPLATE.md | DOC-001; DOC-002 | ACTIVE | Required consistent intake report |
| DOC-024 | P2 | 25 | Storage & Export Acceptance | 05_BUILD/05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | DOC-016; DOC-015 | ACTIVE | Legacy test plan; not executed |
| DOC-025 | P2 | 26 | AI Participants & Token Usage | 05_BUILD/00_ROOT/AI_PARTICIPANTS_AND_TOKEN_USAGE.md | DOC-002 | ACTIVE | AI role roster; participation/token values require evidence |
| DOC-026 | P3 | 27 | Lifecycle Guide (Vietnamese) | 00_ROOT/LIFECYCLE_GUIDE_VI.md | DOC-004; DOC-005 | ACTIVE | Human-readable explanation of lifecycle |
| DOC-027 | P3 | 28 | Work Standard Versioning | 00_ROOT/WORK_STANDARD_VERSIONING.md | DOC-001 | ACTIVE | Version history and compatibility |
| DOC-028 | P3 | 29 | Vietnamese Glossary | 00_ROOT/VIETNAMESE_GLOSSARY.md | DOC-002 | ACTIVE | Terminology reference |
| DOC-029 | P3 | 30 | Legacy Scaffold Notice | LEGACY_SCAFFOLD_NOTICE.md | DOC-001 | ACTIVE | Historical/legacy context |
| DOC-030 | P3 | 31 | Work 70 Session Log | 05_BUILD/10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | DOC-002; DOC-033 | ACTIVE | Historical build log; canonical chronological log belongs at Work root |
| DOC-031 | P3 | 32 | Consolidation Evidence Report | 06_EVIDENCE/WORK70_CONSOLIDATION_CHECK_20261030.md | DOC-014 | ACTIVE | Historical evidence of Work 70 consolidation |
| DOC-032 | P3 | 33 | Dashboard README | DASHBOARD/README.md | DOC-010 | ACTIVE | Dashboard usage and limitations |

## AI reading rule
Read DOC-001 through DOC-006, then DOC-033. Then read relevant P1 documents in ascending read order. Read P2 only for the active task. Read P3 when clarification, operations or historical trace requires it. Never infer PASS from the register or presence of a file.

## Maintenance
When adding a document: allocate the next unused DOC ID, set priority/read order/dependencies, add one row here, and add required metadata below the title. Do not rename files to encode STT. A document located under 05_BUILD is not canonical solely because of its path; its authority must be explicitly declared by this standard and mapping register.
