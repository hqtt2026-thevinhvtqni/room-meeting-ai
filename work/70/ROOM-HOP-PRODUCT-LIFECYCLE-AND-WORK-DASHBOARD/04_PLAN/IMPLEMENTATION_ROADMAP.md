# IMPLEMENTATION ROADMAP — WORK 70 / VERSION 1.3
- **STT / Document ID:** DOC-011
- **Priority:** P1
- **Read order:** 15
- **Depends on:** DOC-008; DOC-009; DOC-033; DOC-036
- **Status:** ACTIVE
- **Version / Updated:** 1.3 / 2026-10-30

## Delivery packages
| WP | Objective | Owner | Reviewer | Current state |
|---|---|---|---|---|
| WP-70-01 | Canonical Work structure, lifecycle, gates, shared records and state machine | Xu | Qw | IN_PROGRESS |
| WP-70-02 | Work-level planning model, mapping register and build folder contract | Xu | Qw | IN_PROGRESS |
| WP-70-03 | Per-Work Dashboard, data schema and read-only source contract | Xu | Qw | IN_PROGRESS |
| WP-70-04 | Core read integration discovery and verification | Xu / Core owner TBD | Qw | BLOCKED / NOT VERIFIED |
| WP-70-05 | Evidence registry, storage and file export architecture | Xu | Qw | DESIGN ONLY |
| WP-70-06 | Independent verification, acceptance preparation and release readiness | Xu | Qw | PLANNED |


## Work Package registry authority
- Proposed Work-level data: `04_PLAN/WORK_PACKAGE_REGISTER.json` (schema_version 0.1-draft).
- Proposed contract: `03_ARCHITECT/WORK_PACKAGE.schema.json`.
- Proposal and approval checklist: `04_PLAN/DOC-053_DE-XUAT-SO-DANG-KY-GOI-CONG-VIEC_WORK-PACKAGE-REGISTER-PROPOSAL.md`.
- Status: DRAFT_NOT_APPROVED. The six legacy records and their legacy statuses are preserved for reconciliation only; all proposed WP statuses remain DRAFT, estimates remain NOT_ESTIMATED and reviewer assignments remain unconfirmed.
- The proposal does not supersede this roadmap, does not authorize migration and does not open G4. Until Vinh approves the WP baseline, DOC-011 remains the planning authority and the proposal is non-authoritative.

## End-to-end sequence
1. Reconcile canonical structure, four official records and source ownership contracts.
2. Establish Work-level WP plan and 05_BUILD mapping register; classify legacy build files before any migration.
3. Validate PRODUCT_STATUS.json against schema; correct Dashboard rendering and source truth.
4. Inspect actual Core implementation and identify verified APIs/permissions; do not invent endpoints.
5. Implement storage/export only after actual Core and storage contracts are approved.
6. Run automated schema, static, browser, security, failure and regression tests.
7. Independently review the mapping migration and publish reconciliation evidence.
8. Independent QE review; publish evidence and defect disposition.
9. Prepare acceptance record; Vinh retains final acceptance authority.
10. Release only after explicit acceptance, deployment/rollback evidence and operational readiness.

## Dependencies and blockers
- Core lifecycle/read APIs and authorization contract not yet verified in Work 70 evidence.
- Storage provider, retention policy and real artifact registry contract not yet approved/verified.
- Dashboard browser E2E and independent QE evidence not yet recorded.
- 05_BUILD legacy candidate files have not been migrated; canonical target/version reconciliation and explicit approval remain required.
- Existing Work migration is out of scope until Work 70 reference is accepted.

## Scope protection
Do not modify Work 10/15/28 or bulk-migrate any existing Work. Do not claim Core live, persistent storage, export availability or release without evidence. Do not mark 05_BUILD mapping migration PASS before target hashes and independent review.
