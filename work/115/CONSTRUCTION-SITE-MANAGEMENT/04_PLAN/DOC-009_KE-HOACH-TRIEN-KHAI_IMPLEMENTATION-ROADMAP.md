# KẾ HOẠCH TRIỂN KHAI WORK 115 / IMPLEMENTATION ROADMAP
- **STT / Document ID:** DOC-009
- **Priority:** P1
- **Read order:** 9
- **Depends on:** DOC-006; DOC-007; DOC-008
- **Status:** DRAFT — BUILD NOT AUTHORIZED
- **Version / Updated:** 0.1 / 2026-11-12
- **Governing standard:** Work 70 Standard 1.2

| Phase | WP | Objective | Status | Exit evidence |
|---|---|---|---|---|
| 01_DISCOVER | WP115-01 | Interview intended manager; map actual site workflow, users, devices and constraints | IN_PROGRESS | Validated problem, personas and current workflow |
| 02_DEFINE | WP115-02 | Define MVP scope, functional/non-functional requirements and measurable acceptance | PLANNED | Approved DOC-007 and acceptance criteria |
| 03_ARCHITECT | WP115-03 | Select app shape, data model, API, identity, storage, offline and deployment architecture | PLANNED | Reviewed architecture and threat/data-flow review |
| 04_PLAN | WP115-04 | Estimate work, dependencies, delivery milestones, costs and operational ownership | PLANNED | Approved implementation plan and source repository |
| 05_BUILD | WP115-05 | Implement manager web, worker reporting, API, persistence and attachments | NOT AUTHORIZED | Source code, tests and build evidence |
| 06_VERIFY | WP115-06 | Verify functional workflows, security, mobile usability, upload reliability and recovery | PLANNED | Reproducible test evidence and independent review |
| 07_ACCEPT | WP115-07 | Demonstrate real workflows to Product Owner and intended manager | PLANNED | Explicit acceptance record |
| 08_RELEASE | WP115-08 | Deploy controlled release and hand over access/operations | PLANNED | Approved release record |
| 09_OPERATE | WP115-09 | Maintain backups, incidents, updates and user support | PLANNED | Operations guide and ownership |

## Initial sequencing
1. Validate the uncle's real workflow before choosing technology.
2. Keep the MVP focused on project/site, assignment, field report, photo and manager review unless discovery changes it.
3. Decide connectivity/offline needs before choosing the worker interaction model.
4. Decide privacy, authorization, storage and backup before using real data.
5. Declare the canonical product source repository before BUILD.
6. Do not claim implementation progress from scaffold creation.
