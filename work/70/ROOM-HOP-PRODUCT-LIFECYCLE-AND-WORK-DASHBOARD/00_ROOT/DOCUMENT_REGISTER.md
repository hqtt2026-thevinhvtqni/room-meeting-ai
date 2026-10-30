# WORK 70 — DOCUMENT REGISTER
Register version: 1.0
Owner: Xu / AI-01
Authority: Vinh
Rule: STT is a stable identity; Priority is importance; Read order is sequence. File paths are not renamed by this register.

| STT | Priority | Read order | Document | Path | Depends on | Status | Purpose / reading instruction |
|---|---|---:|---|---|---|---|---|
| DOC-001 | P0 | 1 | Work Manifest | 00_ROOT/WORK_MANIFEST.md | NONE | ACTIVE | Identity, authority, scope, state and repository rules; always first |
| DOC-002 | P0 | 2 | AI Project Intake & Execution Standard | 00_ROOT/AI_PROJECT_INTAKE_STANDARD.md | DOC-001 | ACTIVE | Mandatory process and AI behavior |
| DOC-003 | P0 | 3 | Repository Layout & Sync | 00_ROOT/REPOSITORY_LAYOUT_AND_SYNC.md | DOC-001 | ACTIVE | Branch, Sandbox and sync boundaries |
| DOC-004 | P0 | 4 | Lifecycle Gate Matrix | 00_ROOT/LIFECYCLE_GATE_MATRIX.md | DOC-001 | ACTIVE | Gate and transition conditions |
| DOC-005 | P0 | 5 | State Machine | 00_ROOT/STATE_MACHINE.md | DOC-004 | ACTIVE | Legal states and transitions |
| DOC-006 | P0 | 6 | Decision Log | 00_ROOT/DECISION_LOG.md | DOC-001 | Binding decisions and rationale |
| DOC-007 | P1 | 7 | Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DOC-001 | Problem, users, evidence and assumptions |
| DOC-008 | P1 | 8 | Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DOC-007 | Scope, requirements and acceptance criteria |
| DOC-009 | P1 | 9 | Work Lifecycle Architecture | 03_ARCHITECT/WORK_LIFECYCLE_ARCHITECTURE.md | DOC-008 | Product lifecycle and system architecture |
| DOC-010 | P1 | 10 | Dashboard Core Read Contract | 03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md | DOC-009 | Core/Dashboard boundary and read-only contract |
| DOC-011 | P1 | 11 | Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DOC-008; DOC-009 | Delivery sequence and milestones |
| DOC-012 | P1 | 12 | Work Instantiation & Migration | 04_PLAN/WORK_INSTANTIATION_AND_MIGRATION.md | DOC-003; DOC-009 | How to create/migrate a Work safely |
| DOC-013 | P1 | 13 | Build Register | 05_BUILD/00_ROOT/BUILD_REGISTER.json; BUILD_REGISTER.md | DOC-001; DOC-011 | Canonical WP records; JSON authoritative within WP registry |
| DOC-014 | P1 | 14 | Evidence Register | 06_EVIDENCE/EVIDENCE_REGISTER.json; EVIDENCE_REGISTER.md | DOC-004 | Cross-phase evidence and provenance |
| DOC-015 | P1 | 15 | Verification Plan | 06_VERIFY/VERIFICATION_PLAN.md | DOC-008; DOC-013; DOC-014 | Verification strategy and coverage |
| DOC-016 | P1 | 16 | Storage & Export Architecture | 05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | DOC-009; DOC-010 | Storage/export design; currently design-only |
| DOC-017 | P1 | 17 | Core Capability Gap Assessment | 05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | DOC-010 | Evidence-based Core capability gaps |
| DOC-018 | P2 | 18 | Migration Plan | 04_PLAN/MIGRATION_PLAN.md | DOC-012 | Execution steps for approved migration |
| DOC-019 | P2 | 19 | Verification Checklist | 06_VERIFY/VERIFICATION_CHECKLIST.md | DOC-015 | Operational verification checklist |
| DOC-020 | P2 | 20 | Acceptance Record | 07_ACCEPT/ACCEPTANCE_RECORD.md | DOC-015; DOC-019 | Authorized acceptance decision |
| DOC-021 | P2 | 21 | Release Plan | 08_RELEASE/RELEASE_PLAN.md | DOC-020 | Controlled release preparation |
| DOC-022 | P2 | 22 | Operations Model | 09_OPERATE/OPERATIONS_MODEL.md | DOC-021 | Post-release operations |
| DOC-023 | P2 | 23 | Project Intake Report Template | 00_ROOT/PROJECT_INTAKE_REPORT_TEMPLATE.md | DOC-001; DOC-002 | Required consistent intake report |
| DOC-024 | P2 | 24 | Storage & Export Acceptance | 05_BUILD/05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | DOC-016; DOC-015 | Acceptance tests for future implementation |
| DOC-025 | P2 | 25 | AI Participants & Token Usage | 05_BUILD/00_ROOT/AI_PARTICIPANTS_AND_TOKEN_USAGE.md | DOC-002 | AI role roster; participation/token values require evidence |
| DOC-026 | P3 | 26 | Lifecycle Guide (Vietnamese) | 00_ROOT/LIFECYCLE_GUIDE_VI.md | DOC-004; DOC-005 | Human-readable explanation of lifecycle |
| DOC-027 | P3 | 27 | Work Standard Versioning | 00_ROOT/WORK_STANDARD_VERSIONING.md | DOC-001 | Version history and compatibility |
| DOC-028 | P3 | 28 | Vietnamese Glossary | 00_ROOT/VIETNAMESE_GLOSSARY.md | DOC-002 | Terminology reference |
| DOC-029 | P3 | 29 | Legacy Scaffold Notice | LEGACY_SCAFFOLD_NOTICE.md | DOC-001 | Historical/legacy context |
| DOC-030 | P3 | 30 | Work 70 Session Log | 05_BUILD/10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | DOC-002 | Session-level implementation history |
| DOC-031 | P3 | 31 | Consolidation Evidence Report | 06_EVIDENCE/WORK70_CONSOLIDATION_CHECK_20261030.md | DOC-014 | Historical evidence of Work 70 consolidation |
| DOC-032 | P3 | 32 | Dashboard README | DASHBOARD/README.md | DOC-010 | Dashboard usage and limitations |

## AI reading rule
Read DOC-001 through DOC-006 first. Then read P1 documents in ascending read order that are relevant to the assigned scope. Read P2 only for the active task. Read P3 when clarification, operations or historical trace requires it. Never infer PASS from the register or the presence of a file.

## Maintenance
When adding a document: allocate the next unused DOC ID, set priority/read order/dependencies, add one row here, and add the required metadata header to the new Markdown document. When materially revising a legacy Markdown file, add its assigned DOC ID, priority, read order and dependencies below the title. Do not rename files to encode STT.
