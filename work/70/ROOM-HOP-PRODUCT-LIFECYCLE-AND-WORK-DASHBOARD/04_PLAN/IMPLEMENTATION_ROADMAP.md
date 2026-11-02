# IMPLEMENTATION ROADMAP — WORK 70 / VERSION 1.5
- **STT / Document ID:** DOC-011
- **Priority:** P1
- **Read order:** 15
- **Depends on:** DOC-008; DOC-009; DOC-033; DOC-036
- **Status:** ACTIVE
- **Version / Updated:** 1.5 / 2026-11-02

## Delivery packages
| WP | Objective | Owner | Reviewer | Current state |
|---|---|---|---|---|
| WP-70-01 | Canonical Work structure, lifecycle, gates, shared records and state machine | Xu | Qw | IN_PROGRESS |
| WP-70-02 | Work-level planning model, mapping register and build folder contract | Xu | Qw | IN_PROGRESS |
| WP-70-03 | Per-Work Dashboard, data schema and read-only source contract | Xu | Qw | IN_PROGRESS |
| WP-70-04 | Core read integration discovery and verification | Xu / Core owner TBD | Qw | BLOCKED / NOT VERIFIED |
| WP-70-05 | Evidence registry, storage and file export architecture | Xu | Qw | DESIGN ONLY |
| WP-70-06 | Independent verification, acceptance preparation and release readiness | Xu | Qw | PLANNED |


## Work Package registry authority — reconciled 2026-11-02
- **Canonical Work-level plan:** this DOC-011 roadmap is the active planning source for the six WP-70-01..WP-70-06 IDs, objectives, owners, reviewers and current states.
- **Baseline decision:** D-068-01 was decided by Xu under Vinh's explicit delegation D70-018. DOC-011 retains the six WP IDs and maps the eight sub-deliverables SD-01..SD-08. This is an internal planning/coordination baseline; it does not pass G0/G1/G4 or authorize BUILD.
- **No separate approved WP registry exists:** the earlier proposed path `04_PLAN/WORK_PACKAGE_REGISTER.json` was not found in the Work 70 Sandbox listing or GitHub main. Do not refer to it as an existing canonical registry.
- **Schema location correction:** `WORK_PACKAGE.schema.json` is present only as a Build-branch candidate under `05_BUILD/00_ROOT/`; the previously stated `03_ARCHITECT/WORK_PACKAGE.schema.json` path is not the verified location. It is not an approved Work-level schema.
- **DOC-053 correction:** the earlier reference to `04_PLAN/DOC-053_DE-XUAT-SO-DANG-KY-GOI-CONG-VIEC_WORK-PACKAGE-REGISTER-PROPOSAL.md` is invalid. The observed DOC-053 is `09_OPERATE/PHASE_EXECUTION_PLAYBOOK.md`, not a WP-register proposal.
- **Build mapping authority:** DOC-036 and the Build Register/schema files remain Build-layer mapping/candidate artifacts; they do not replace DOC-011 or create a second Work-level plan.
- **Historical proposal:** DOC-062 is retained as a reconciliation proposal record and is superseded for baseline decisions by D-068-01; see its dated addendum. No separate registry migration is implied.
- **Gate boundary:** G0/G1 remain NOT_READY and G4 remains NOT READY / NOT PASS. No implementation or release authorization is granted by this section.

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


## Sub-deliverable mapping — D-068-01 (2026-11-02)
Giữ nguyên sáu WP ID chuẩn của DOC-011; phân rã đích bàn giao tám package thành SD-01..SD-08 như sau:

| Sub-deliverable | Nội dung | WP cha | Trạng thái / điều kiện |
|---|---|---|---|
| SD-01 | Governance baseline: Manifest, lifecycle, gates, state, registers, canonical ownership | WP-70-01 | IN_PROGRESS; đối chiếu tài liệu và bằng chứng |
| SD-02 | Lifecycle Engine: resolve/bind/validate/prepare/execute/test/evidence/finalize; fail-closed, idempotency | WP-70-01 | SPIKE ONLY; tích hợp cần contract + Work Entry |
| SD-03 | Planning/mapping: Work plan, WP registry, canonical mapping | WP-70-02 | IN_PROGRESS; không tạo nguồn WP thứ hai |
| SD-04 | Hybrid AI Dispatch: assignment, handoff, delivery, ACK, progress, result, review | WP-70-02 | DESIGN; adapter/private-session dispatch chưa xác minh |
| SD-05 | Core authority/contracts: registry, routes, auth, audit, Work scope | WP-70-04 | BLOCKED; Core owner/API/persistence chưa xác minh |
| SD-06 | Dashboard: Core-backed read-only UI, freshness/error states, browser E2E | WP-70-03 | LOCAL SNAPSHOT ONLY; Core-live BLOCKED |
| SD-07 | Evidence/export: durable evidence, integrity, provenance, export | WP-70-05 | DESIGN ONLY; storage contract chưa được xác minh |
| SD-08 | Independent QE, acceptance, release, operations | WP-70-06 | PREPARATION ONLY; runtime QE NOT RUN; final acceptance/release reserved |

**Quyết định của Xu theo ủy quyền D70-018:** thông qua mapping này làm baseline điều phối nội bộ Work 70; không đổi sáu WP ID và không biến Build Register candidate thành nguồn chuẩn. Mapping không mở G4/BUILD, không xác nhận bất kỳ package nào DONE/PASS.

**Dependencies:** SD-05 Core authority phải được xác minh trước tích hợp SD-02/04/06/07 vào authoritative state. SD-08 chỉ chạy QE sau khi có implementation và môi trường hợp lệ. No local snapshot/WEE file is Core authority.
