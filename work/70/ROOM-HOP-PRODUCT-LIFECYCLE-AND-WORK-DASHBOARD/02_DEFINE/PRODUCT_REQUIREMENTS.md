# YÊU CẦU SẢN PHẨM / PRODUCT REQUIREMENTS
- **STT / Document ID:** DOC-008
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 12
- **Depends on / Phụ thuộc:** DOC-007; DOC-042; DOC-043
- **Status / Trạng thái:** ACTIVE — MASTER REQUIREMENTS TEMPLATE
- **Version / Updated:** 1.1 / 2026-10-30
- **Process / Quy trình áp dụng:** DOC-043 — Quy trình Xác định Yêu cầu / Define Process
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

> DOC-008 là baseline requirements của từng Work. Bản mẫu này không tự động có nghĩa các yêu cầu dưới đây đã được phê duyệt hoặc triển khai. Chỉ nội dung được điền, truy xuất và phê duyệt theo G2 mới trở thành baseline có hiệu lực.

## 1. Work & baseline overview — Tổng quan
- Work ID / Name:
- Product / service:
- Product Owner:
- Define Coordinator:
- Discover Brief (DOC-007) version:
- G1 decision reference:
- Requirements baseline version:
- Date / Status: DRAFT / IN REVIEW / READY FOR G2 / APPROVED / SUPERSEDED
- Research depth inherited from Discover:
- Applicable standards / contracts:

## 2. Product outcome — Kết quả sản phẩm
- Problem to solve (link to DOC-007):
- Target users / beneficiaries:
- Product outcome:
- Value hypothesis:
- Success metric(s):

| Metric ID | Metric / definition | Baseline | Target | Unit / window | Data source | Owner | Status / caveat |
|---|---|---|---|---|---|---|---|
| MET-001 | | TBD | TBD | | | | |

Không tự đặt baseline/target khi chưa có dữ liệu hoặc Product Owner approval. TBD phải có owner và kế hoạch đo.

## 3. Actors & stakeholder needs — Vai trò và nhu cầu

| Actor ID | Actor / stakeholder | Goal / responsibility | Need / pain point | Permission / authority | Source |
|---|---|---|---|---|---|
| ACT-001 | | | | | |

## 4. Use cases & workflows — Trường hợp sử dụng

| Use Case ID | Name / goal | Primary actor | Trigger | Preconditions | Main outcome | Alternate / exception flows | Related needs |
|---|---|---|---|---|---|---|---|
| UC-001 | | | | | | | |

Mô tả chi tiết luồng chính, luồng thay thế, lỗi, retry, timeout, từ chối quyền, dữ liệu thiếu và postcondition khi liên quan.

## 5. Scope & boundaries — Phạm vi và ranh giới
### In Scope
- 

### Out of Scope
- 

### Deferred / Later
- 

### System boundary and external parties
- External actors/systems:
- Inputs / outputs at business level:
- Ownership boundary:
- Explicit exclusions:

## 6. Constraints & dependencies — Ràng buộc và phụ thuộc

| ID | Constraint / dependency | Type | Source / authority | Impact | Owner | Resolution / condition |
|---|---|---|---|---|---|---|
| CON-001 | | TECH / DATA / SEC / PRIV / LEGAL / OPS / COST / TIME / EXTERNAL | | | | |

## 7. Requirements catalogue — Danh mục yêu cầu

ID convention: stable IDs by category, e.g. BUS-001, USR-001, FR-001, NFR-001, DATA-001, SEC-001, PRIV-001, INT-001, OPS-001, REG-001. Do not reuse retired IDs.

| Requirement ID | Category | Requirement statement (one meaning) | Rationale / source trace | Priority | Owner | Dependencies | Verification method | Acceptance criteria reference | Status |
|---|---|---|---|---|---|---|---|---|---|
| FR-001 | FR | | | MUST / SHOULD / COULD / WON'T FOR NOW | | | | AC-001 | DRAFT |

### Requirement writing rules
- State observable behavior/condition; keep WHAT separate from HOW.
- Avoid ambiguous adjectives unless measurable thresholds are defined.
- Split requirements that have independent acceptance outcomes.
- Record assumptions and unresolved questions instead of embedding guesses.
- Requirements may be DRAFT, PROPOSED, APPROVED, DEFERRED, REJECTED or SUPERSEDED.
- APPROVED requires the approved baseline/G2 decision reference.

## 8. Acceptance criteria — Tiêu chí nghiệm thu

| AC ID | Requirement ID(s) | Given / precondition | When / action | Then / observable result | Negative / edge cases | Verification evidence |
|---|---|---|---|---|---|---|
| AC-001 | FR-001 | | | | | |

Acceptance criteria must be deterministic enough for independent verification. State test data, environment, threshold and measurement window when relevant.

## 9. Quality attributes & NFR — Thuộc tính chất lượng

| NFR ID | Attribute | Requirement / measurable threshold | Load / environment / percentile | Measurement method | Risk if unmet | Owner |
|---|---|---|---|---|---|---|
| NFR-001 | Performance / Availability / Reliability / Accessibility / Maintainability / Portability / Scalability | TBD until justified | | | | |

Avoid absolute claims such as “zero defects”, “fully secure” or “instant”. Define the scope and measurement.

## 10. Data, security, privacy, integration and operations
### Data
- Data entities / classification:
- Source of truth / ownership:
- Quality / provenance:
- Retention / archival / deletion:
- Export / portability:
- Data access / audit:

### Security & privacy
- Actors / authorization expectations:
- Authentication / trust boundaries:
- Sensitive data and privacy constraints:
- Audit requirements:
- Threat / abuse cases:
- Required security review / evidence:

### Integration
- External systems / parties:
- Business-level interface needs:
- Compatibility / version expectations:
- Failure / retry / timeout behavior:

### Operations
- Logging / monitoring / alerting:
- Backup / restore / recovery:
- Support owner / service expectations:
- Incident / escalation requirements:

Mark N/A only with rationale and reviewer acceptance.

## 11. Prioritization & trade-offs — Ưu tiên và đánh đổi

| Requirement / option | Priority | Why this priority | Value | Cost / complexity | Risk | Deferred alternative |
|---|---|---|---|---|---|---|
| | | | | | | |

Priority guide:
- MUST: essential to product outcome, mandatory obligation or critical risk control.
- SHOULD: high value, but a justified alternative/workaround exists.
- COULD: useful, non-essential.
- WON'T FOR NOW: explicitly excluded from this baseline; may be reconsidered through change control.

## 12. Assumptions, open questions and risks

| ID | Type (ASSUMPTION / QUESTION / RISK / CONFLICT) | Description | Impact if unresolved | Evidence / source | Owner | Resolution condition / due point |
|---|---|---|---|---|---|---|
| AQR-001 | | | | | | |

## 13. Traceability matrix — Ma trận truy xuất

| Discover problem / evidence | User need / outcome | Use case | Requirement ID | Acceptance criteria | Verification / evidence | Decision reference |
|---|---|---|---|---|---|---|
| | | | | | | |

Check traceability both forward and backward. A requirement without a valid source/rationale must be justified or removed from the proposed baseline. A success outcome with no supporting requirement/measurement must be resolved or explicitly accepted as out of scope.

## 14. Decisions & change requests
### Pending decisions
| Decision ID | Question / options | Impact | Decision authority | Due condition | Status |
|---|---|---|---|---|---|
| | | | | | |

### Change requests after baseline approval
| CR ID | Request / reason | Affected requirements / scope | Impact analysis | Reviewer | Product Owner decision | New baseline |
|---|---|---|---|---|---|---|
| | | | | | | |

## 15. G2 assessment — DEFINE → ARCHITECT

| G2 criterion | Evidence / reference | Reviewer finding | Status (PASS / GAP / N/A with reason) |
|---|---|---|---|
| G1 PASS and approved Discover Brief | | | |
| Product outcome and success measures defined | | | |
| Actors, stakeholder needs and use cases identified | | | |
| In-scope, out-of-scope and boundaries explicit | | | |
| Requirements uniquely identified and traceable | | | |
| Acceptance criteria and verification methods testable | | | |
| Applicable NFR/data/security/privacy/integration/ops/compliance covered | | | |
| Constraints, dependencies, risks and open questions recorded | | | |
| Priorities and trade-offs justified | | | |
| Bidirectional traceability reviewed | | | |
| Independent review/findings dispositioned | | | |
| Product Owner approval and G2 decision recorded | | | |

- Overall G2 status: NOT READY / NEEDS RESEARCH / BLOCKED / PASS / WAIVED
- Reviewer(s), role and date:
- Product Owner decision:
- Approved baseline version:
- Decision record reference:
- Authorized next phase: YES / NO
- Waiver authority, rationale, scope, expiry and residual risk (if applicable):

**Rule:** G2 PASS requires the authorized decision and approved baseline. A populated template, number of requirements, AI consensus or Dashboard status is not approval.

## 16. Handoff to ARCHITECT — Bàn giao
- Approved DOC-008 version:
- DOC-007 / G1 reference:
- G2 decision reference:
- Outcomes and metrics:
- Requirements catalogue:
- Scope and boundaries:
- Acceptance / quality attributes:
- Traceability matrix:
- Constraints / dependencies / risks:
- Open decisions / assumptions:
- Known limitations:
- Receiving architecture owner:
- Handoff acknowledgement / date:

## 17. Change history — Lịch sử thay đổi

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-10-30 | Xu / AI-01 | Initial Work 70 product objective, functional/quality requirements and acceptance criteria |
| 1.1 | 2026-10-30 | Xu / AI-01 | Corrected title/metadata version mismatch; converted into governed Define requirements template aligned with DOC-043; added outcomes, actors, use cases, scope, requirement taxonomy, acceptance criteria, NFR, data/security/ops, traceability, G2 and change control |
