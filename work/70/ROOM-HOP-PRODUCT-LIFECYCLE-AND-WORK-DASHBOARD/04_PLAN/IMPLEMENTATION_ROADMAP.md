# IMPLEMENTATION ROADMAP — WORK 70 / VERSION 1.1

## Delivery packages
| WP | Objective | Owner | Reviewer | Current state |
|---|---|---|---|---|
| WP-70-01 | Canonical Work structure, lifecycle, gates and state machine | Xu | Qw | IN_PROGRESS |
| WP-70-02 | Work Package registry, schema and build folder contract | Xu | Qw | IN_PROGRESS |
| WP-70-03 | Per-Work Dashboard, data schema and read-only source contract | Xu | Qw | IN_PROGRESS |
| WP-70-04 | Core read integration discovery and verification | Xu / Core owner TBD | Qw | BLOCKED / NOT VERIFIED |
| WP-70-05 | Evidence registry, storage and file export architecture | Xu | Qw | DESIGN ONLY |
| WP-70-06 | Independent verification, acceptance preparation and release readiness | Xu | Qw | PLANNED |

## End-to-end sequence
1. Reconcile canonical structure and document contracts.
2. Complete WP register/schema and evidence index/schema.
3. Validate PRODUCT_STATUS.json against schema; correct Dashboard rendering and source truth.
4. Inspect actual Core implementation and identify verified APIs/permissions; do not invent endpoints.
5. Implement storage/export only after actual Core and storage contracts are approved.
6. Run automated schema, static, browser, security, failure and regression tests.
7. Independent QE review; publish evidence and defect disposition.
8. Prepare acceptance record; Vinh retains final acceptance authority.
9. Release only after explicit acceptance, deployment/rollback evidence and operational readiness.

## Dependencies and blockers
- Core lifecycle/read APIs and authorization contract not yet verified in Work 70 evidence.
- Storage provider, retention policy and real artifact registry contract not yet approved/verified.
- Dashboard browser E2E and independent QE evidence not yet recorded.
- Existing Work migration is out of scope until Work 70 reference is accepted.

## Scope protection
Do not modify Work 10/15/28 or bulk-migrate any existing Work. Do not claim Core live, persistent storage, export availability or release without evidence.
