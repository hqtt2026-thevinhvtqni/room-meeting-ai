# ĐỀ XUẤT SỔ ĐĂNG KÝ GÓI CÔNG VIỆC / WORK PACKAGE REGISTER PROPOSAL
- **STT / Document ID:** DOC-053
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 53
- **Depends on / Phụ thuộc:** DOC-001; DOC-004; DOC-005; DOC-009; DOC-011; DOC-036; DOC-045; DOC-052
- **Status / Trạng thái:** DRAFT — NOT APPROVED / NOT AN EXECUTION BASELINE
- **Version / Updated:** 0.1 / 2026-10-30
- **Owner:** Xu / AI-01
- **Approval authority:** Vinh — Product Owner

## 1. Purpose

Đề xuất xác lập một sổ Work Package (WP — gói công việc) cấp Work tại 04_PLAN theo DOC-045. Đây là bản đề xuất để giải quyết F-052-01; chưa phải kế hoạch thực thi được phê duyệt, không mở G4 và không cho phép chuyển trạng thái WP sang READY/ACTIVE.

Supporting artifacts:
- Proposed data: 04_PLAN/WORK_PACKAGE_REGISTER.json
- Proposed schema: 03_ARCHITECT/WORK_PACKAGE.schema.json
- Source candidate: branch work/70/05-build, files BUILD_REGISTER.md, BUILD_REGISTER.json and WORK_PACKAGE.schema.json.
- Mapping contract: branch work/70/05-build, 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md.

## 2. Why this proposal exists

DOC-011 contains six WP summaries. The legacy branch contains detailed structured WP records and schema. DOC-036 currently classifies those files as CANONICAL CANDIDATE and records the canonical target/version as NOT ESTABLISHED. DOC-009 and DOC-045 require the Work-level plan to live in 04_PLAN; 05_BUILD is mapping/execution coordination only.

The proposal preserves all six existing WP IDs and dependencies but does not silently promote legacy statuses into the new baseline.

## 3. Draft registry rules

1. 04_PLAN owns the single Work-level WP plan and registry.
2. 03_ARCHITECT owns the WP data contract/schema.
3. 05_BUILD only maps WP IDs to fixed engineering areas, canonical source repository/path, branch/ref, exact commit/version and evidence.
4. A WP ID is stable and never reused.
5. Every WP must have objective, accountable owner, independent reviewer, build areas, dependencies, requirements/architecture references, deliverables, acceptance criteria, DoR, DoD, priority, estimate basis, risks, evidence refs and change history.
6. Estimate values remain NOT_ESTIMATED / UNKNOWN until supported by capacity and historical evidence. No dates or effort values are fabricated.
7. Legacy status is retained separately as legacy_status. Proposed baseline status starts DRAFT for every WP until reconciliation and authority approval.
8. A reviewer assignment is PROPOSED_NOT_CONFIRMED until the reviewer accepts and independence is checked.
9. Missing requirement references remain empty and are a planning gap; do not invent requirement IDs.
10. No WP may enter READY or ACTIVE before G4 and its DoR are satisfied.
11. DONE requires all DoD criteria and verified evidence; a progress label is not a gate result.
12. This proposal does not authorize migration, deletion or modification of branch source files.

## 4. Six WP reconciliation summary

| WP | Legacy status | Proposed status | Dependencies | Current issue |
|---|---|---|---|---|
| WP-70-01 | IN_PROGRESS | DRAFT | None | Reconcile lifecycle/governance outputs to approved requirements and architecture |
| WP-70-02 | IN_PROGRESS | DRAFT | WP-70-01 | Establish canonical registry/schema; do not treat branch register as plan authority |
| WP-70-03 | IN_PROGRESS | DRAFT | WP-70-01 | Dashboard schema/runtime/browser evidence remains unverified |
| WP-70-04 | BLOCKED | DRAFT | WP-70-03 | Core owner TBD; real route/auth/E2E evidence absent |
| WP-70-05 | IN_PROGRESS | DRAFT | WP-70-04 | Storage/export remains design-only; tests not run |
| WP-70-06 | PLANNED | DRAFT | WP-70-01..05 | QE and handoff depend on preceding work; independent review pending |

The legacy status is preserved for audit only. It is not copied as the current approved WP status.

## 5. Definitions

### Definition of Ready (DoR)
A WP may become READY only when:
- G4 PLAN→BUILD is approved for the Work and the WP is included in that approved baseline.
- Approved requirements and architecture references are identified.
- Owner and independent reviewer are confirmed.
- Dependencies and predecessor exit conditions are satisfied or have an approved contingency.
- Canonical source repository/path, branch strategy, access and environment are verified.
- Deliverables, acceptance criteria, verification method and evidence location are defined.
- Estimate range/confidence/basis is recorded, or NOT_ESTIMATED has an owner/action.

### Definition of Done (DoD)
A WP may be recommended DONE only when:
- Deliverables exist at the declared canonical source and exact commit/version is recorded.
- Acceptance criteria are verified with reproducible evidence linked by Evidence ID.
- Independent reviewer completed review and defects have disposition.
- Requirements, architecture, build mapping and evidence references are traceable/current.
- Documentation and security/operations handoff obligations are updated.
- Owner recommends completion and authorized reviewer/authority records final status.

## 6. Estimate and scheduling policy

- No effort, duration, cost, milestone or capacity value is inferred from the AI roster.
- Use ranges, unit, confidence, basis, assumptions and exclusions.
- When evidence is absent, keep NOT_ESTIMATED and assign an estimate discovery task.
- Dates are not commitments until Product Owner approves schedule/capacity.
- Critical path cannot be finalized until WP dependencies and external owner commitments are confirmed.

## 7. Validation performed

The proposed JSON was generated from the six legacy records, with:
- WP IDs, titles, objectives, owners, reviewers, build areas, dependencies, legacy statuses, acceptance criteria and source refs preserved.
- Proposed statuses set to DRAFT; legacy statuses retained separately.
- Priority set to UNASSESSED; estimates explicitly NOT_ESTIMATED.
- Requirement references left empty pending traceability reconciliation.
- Reviewer assignment marked PROPOSED_NOT_CONFIRMED.

The schema and data must be validated by a standards-compliant JSON Schema engine and independently reviewed before approval. A custom structural check is not equivalent to full schema validation.

## 8. Required Product Owner decisions

1. Approve or revise the canonical Work-level WP registry and its ownership split (04_PLAN data, 03_ARCHITECT schema, 05_BUILD mapping).
2. Confirm priorities and any scope trade-offs.
3. Confirm owners/reviewers and whether Qw is available/authorized as independent QE.
4. Approve estimate/capacity approach and milestone constraints.
5. Approve baseline version and G4 transition only after G2/G3 prerequisites are valid.

Until these decisions are recorded, status remains DRAFT — NOT APPROVED. No BUILD execution authority is created.

## 9. Change history

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-30 | Xu / AI-01 | Initial proposal transcribing six legacy WP records without promoting legacy status or creating execution authority. |
