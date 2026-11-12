# DOC-008 — SỔ ĐĂNG KÝ TÀI LIỆU WORK 76 / WORK 76 DOCUMENT REGISTER

- Document ID: DOC-008 | Priority: P0 | Read order: 8
- Work ID: 76 — AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK
- Status: ACTIVE — SINGLE CANONICAL DOCUMENT REGISTER
- Owner: Xu / AI-01
- Authority: Vinh
- Standard: Work 70 DOC-033, DOC-038, DOC-039, DOC-040 and DOC-056
- Rule: one DOC-ID, one canonical path; technical/runtime files are registered as technical artifacts and do not receive fabricated DOC IDs.

| DOC-ID / Artifact | Canonical path | Purpose | Status |
|---|---|---|---|
| DOC-001 | 00_ROOT/DOC-001_WORK-MANIFEST.md | Work identity, scope, authority and lifecycle baseline | ACTIVE |
| DOC-002 | 01_DISCOVER/DOC-002_DISCOVER-BRIEF.md | Discovery brief and unresolved questions | ACTIVE |
| DOC-003 | 02_DEFINE/DOC-003_PRODUCT-REQUIREMENTS.md | Product requirements baseline | DRAFT |
| DOC-004 | 03_ARCHITECT/DOC-004_TRIGGER-ENGINE-ARCHITECTURE.md | Trigger Engine architecture baseline | DRAFT |
| DOC-005 | 04_PLAN/DOC-005_IMPLEMENTATION-ROADMAP.md | Implementation roadmap | ACTIVE |
| DOC-006 | 06_VERIFY/DOC-006_VERIFICATION-PLAN.md | Verification plan | ACTIVE |
| DOC-007 | 00_ROOT/DOC-007_HO-SO-NHAN-VIEC_CO_WORK-ENTRY-RECORD.md | Co participant-specific Work Entry and assignment scope | BLOCKED FOR BUILD |
| DOC-008 | 00_ROOT/DOC-008_SO-DANG-KY-TAI-LIEU_WORK-76-DOCUMENT-REGISTER.md | Canonical document register for Work 76 | ACTIVE |
| DOC-035 | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_EXECUTION-LOG.md | Canonical Work execution journal | ACTIVE |
| EVIDENCE_REGISTER | 06_EVIDENCE/EVIDENCE_REGISTER.md | Evidence inventory and status | ACTIVE |
| BUILD_REGISTER | 05_BUILD/00_ROOT/BUILD_REGISTER.md | Work Package ownership, reviewer and status mapping | ACTIVE |
| DASHBOARD | DASHBOARD/index.html; DASHBOARD/PRODUCT_STATUS.json; DASHBOARD/PRODUCT_STATUS.schema.json; DASHBOARD/README.md | Read-only Work 76 dashboard projection and its data contract | IN_REVIEW |

## Technical artifacts (no DOC-ID)
- DASHBOARD/index.html — responsive dashboard UI.
- DASHBOARD/PRODUCT_STATUS.json — local snapshot, not Core live.
- DASHBOARD/PRODUCT_STATUS.schema.json — JSON schema.
- DASHBOARD/README.md — run/test instructions.
- Other source, tests, lockfiles and runtime artifacts are registered by path in the Build Register when created.

## Canonical ownership
- 00_ROOT: Manifest, Work Entry, Document Register, execution journal.
- 01_DISCOVER: discovery inputs/findings.
- 02_DEFINE: product requirements.
- 03_ARCHITECT: architecture and design decisions.
- 04_PLAN: roadmap and implementation plan.
- 05_BUILD: build register, implementation mappings, source and tests.
- 06_VERIFY: verification plan and test results.
- 06_EVIDENCE: evidence register and immutable/traceable evidence references.
- DASHBOARD: read-only status projection only.

No duplicate document register or parallel journal is authorized. Update this register when a controlled document is added, moved, renamed or retired.
