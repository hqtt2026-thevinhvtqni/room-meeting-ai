# KIẾN TRÚC SẢN PHẨM WORK 115 / PRODUCT ARCHITECTURE
- **STT / Document ID:** DOC-008
- **Priority:** P1
- **Read order:** 8
- **Depends on:** DOC-006; DOC-007
- **Status:** DRAFT — HYPOTHESES ONLY / NOT APPROVED
- **Version / Updated:** 0.1 / 2026-11-12

## 1. Product shape
A web application with two responsive experiences:
- Manager web dashboard for project/site oversight and report review.
- Mobile-friendly field reporting interface for workers.

Whether the worker interface is a responsive web app, Progressive Web App (PWA — ứng dụng web có thể cài đặt) or native app is OPEN. Prefer the simplest option that satisfies validated field conditions.

## 2. Logical components — candidate only
1. Web UI: manager dashboard and worker report screens.
2. Application/API layer: project, work item, assignment, report, review and attachment workflows.
3. Identity and access control: manager, supervisor and worker roles with project-scoped authorization.
4. Data persistence: structured records for projects, work items, users, assignments and reports.
5. File/object storage: site photos and uploaded attachments.
6. Notification mechanism: optional alerts for new reports, overdue submissions and issues.
7. Audit/evidence layer: who submitted, changed, reviewed and when.

## 3. Candidate data entities
Project/Site; WorkItem; User; Team; Assignment; DailyReport; ReportLine; PhotoAttachment; Issue; ReviewComment; AuditEvent.
These are conceptual names, not a finalized schema.

## 4. Key workflow
Manager creates project → defines work items → assigns worker → worker submits field report → system stores report and photos → manager reviews → manager requests correction or confirms → project progress view updates.

## 5. Design constraints to resolve
- Authentication and role/resource authorization.
- Data isolation across projects and customers.
- Upload limits, image compression, retry and duplicate submission.
- Offline/poor-network behavior.
- Time-zone and timestamp integrity.
- Data backup, export, retention and deletion policy.
- Hosting region, budget and operational ownership.

## 6. Source-of-truth boundaries
- Backend database is expected to own product business state, subject to approved architecture.
- Uploaded photos must be stored durably with metadata and access control.
- Dashboard is a projection; it must not be a separate state authority.
- GitHub stores source and versioned documentation, not production secrets or private site photos.
- No architecture decision or technology choice is approved by this draft.

## 7. Security baseline
Deny by default. Workers may access only assigned projects/work items and their permitted reports. Managers may access only projects they own/manage. Every read/write and report review must be authorized server-side. Do not place credentials or private field data in Git.


## 8. Conditional architecture decision — Rule-first, AI-assisted
**Status: DESIGN PRINCIPLE ADOPTED FOR EVALUATION; NOT A FINAL PRODUCT OR TECHNOLOGY APPROVAL.**

The preferred direction is to keep deterministic business rules and authoritative product state outside language models. AI is an optional assistant around the workflow, not the owner of construction records, calculations, permissions or approvals.

### 8.1 Logical decision flow
1. **Application Core / Router:** authenticates the actor, checks project-scoped permissions, validates inputs and routes each task to the appropriate deterministic or AI capability.
2. **Rule Engine (first choice):** handles calculations, totals, unit conversions, required-field checks, workflow states, threshold alerts and other deterministic operations. The exact rules and formulas must be sourced, versioned and approved; calculations must be reproducible and testable.
3. **Student Model (optional):** a locally hosted or otherwise controlled model may assist with report classification, summarization, OCR/extraction review, FAQ drafts or converting free text into a proposed structured report. It must return uncertainty and source references where applicable. It cannot commit authoritative business state without normal validation and user confirmation.
4. **Teacher Model (exception path):** a stronger external or separately governed model may be considered for difficult cases, evaluation, drafting synthetic examples or model-quality review. It is not a default dependency and must not receive private site/customer data until data protection, contractual, security and cost approvals exist.
5. **Human review:** a designated manager/supervisor remains responsible for confirming reports, resolving material discrepancies and approving business decisions.
6. **Data and evidence stores:** the application database remains the source of truth for structured business state; controlled object storage holds photos/files; audit records capture submissions, edits, AI suggestions, approvals and provenance.

### 8.2 Core product versus optional extensions
- **Core discovery target:** project/site management, work assignments, mobile field reports, photo attachments, review/correction, progress visibility and audit history. Each remains subject to user discovery and approval.
- **Optional AI assistance:** report summarization, classification, extraction suggestions, duplicate/anomaly flags and search/FAQ support. These are candidates only; validate user value and error impact before inclusion.
- **Out of current MVP scope:** QS (quantity surveying / bóc tách khối lượng), estimating/dự toán, bill-of-quantities generation, unit-price recommendations, payroll and cost control. Treat as a separately scoped extension only if the Product Owner approves after discovery.

### 8.3 Non-negotiable controls
- **Authority:** model output is a suggestion, never the source of truth. No model may grant access, approve a report, alter a confirmed quantity or trigger a financial commitment on its own.
- **Rule provenance:** every formula, rate, unit conversion and threshold must have an identifiable source, version, effective date and authorized owner. Unknown or conflicting sources must trigger abstention/escalation, not an invented answer.
- **Data isolation:** enforce tenant/customer and project-level isolation server-side for every read, write, search, attachment and AI retrieval. Never rely on prompt instructions as an access-control boundary.
- **Privacy:** do not use real worker/customer/site data for training or external model calls without explicit purpose, authority, consent/legal basis where applicable, minimization, redaction and approved retention controls.
- **Auditability:** retain actor, timestamp, input/source references, model/provider/version where used, output, confidence/uncertainty, reviewer action and final accepted value according to an approved retention policy.
- **Security:** least privilege, deny-by-default authorization, secrets outside Git, controlled uploads, malware/content checks where appropriate, and no cross-project retrieval.
- **Resilience:** field reporting must remain usable if an AI provider/model is unavailable. Poor-network/offline behavior must be designed from discovery evidence; queue/retry must avoid duplicate submissions and preserve timestamps.
- **Cost and operations:** no paid model API, GPU rental, fine-tuning job or recurring AI cost is authorized by this decision. Measure task volume, latency, error severity, human correction rate and total operating cost before selecting infrastructure.
- **Fallback:** if a model is unavailable, uncertain, out of scope or lacks source evidence, fall back to deterministic workflow or human review. Do not silently fabricate or auto-fill consequential values.

### 8.4 Model and training policy
- No specific model family/version (including Qwen or Llama examples) is selected. Compare currently available candidates only after requirements, privacy and hardware constraints are known.
- RAG (Retrieval-Augmented Generation / sinh câu trả lời có truy xuất nguồn) and fine-tuning solve different problems. Prefer retrieval of current, authorized project documents for changing facts; consider fine-tuning only for a stable, well-defined behavior after a measured baseline.
- AI-generated Q&A or synthetic records are not ground truth. Training/evaluation corpora require lawful access, provenance, deduplication, redaction, expert validation and a held-out test set independent of training data.
- Do not claim fixed accuracy targets (including 95%) or savings percentages before defining task-specific test sets, severity-weighted metrics, abstention criteria and independent evaluation.

### 8.5 Entry conditions before implementation
Before any AI component is built or connected, document: validated user task; data classification and permitted processing; source-of-truth and human approval path; threat model and project isolation tests; benchmark dataset and baseline; fallback behavior; operating-cost ceiling; monitoring and rollback plan. The normal W70 phase gates still apply. This section does not authorize BUILD.


## 9. Business role and reporting architecture — updated from user clarification
**Confirmed relationship:** Quản công (site foreman) reports construction progress to Nhà thầu (contractor). Chủ đầu tư (project investor) may be granted access as an optional extension when required.

### 9.1 Role-oriented application model
- **Foreman workspace:** mobile-first report creation/submission for assigned projects and work items; attachment upload; report history and correction response.
- **Contractor workspace:** project portfolio and project-level dashboard; assignment of foremen; report inbox; review, comment, clarification/correction workflow; progress overview.
- **Investor view (optional capability):** a separately permissioned, project-scoped view that the contractor/project administrator explicitly enables. Default to read-only, with only approved progress and report information.
- **Field workers (optional subordinate source):** may provide updates/photos to the foreman. Direct worker accounts are not assumed until the real site workflow is confirmed.

### 9.2 Reporting flow
Contractor creates project and defines work/reporting structure → appoints foreman → foreman submits progress report and supporting evidence → contractor reviews and may request correction → accepted report is reflected in project progress → authorized investor can view the shared information if the feature is enabled.

The report lifecycle, review authority, report frequency, correction rules and whether an investor can comment/acknowledge remain OPEN for discovery.

### 9.3 Multi-party authorization and information boundaries
- Model organizations/contractors, projects, memberships/assignments and project-specific external stakeholders as separate authorization scopes; final schema remains undecided.
- Every request must be checked server-side against actor, organization, project, resource and action.
- Investor access is opt-in per project, least-privilege, revocable and read-only by default; it must not imply access to the contractor's organization-wide portfolio.
- Separate internal contractor notes and commercially/personally sensitive information from investor-visible report fields.
- Do not expose worker personal data, internal cost/commercial details, attachments or comments to an investor unless specifically approved for that project.
- Record who granted/revoked access, which project/report was shared, what scope was granted and when.
- The dashboard must filter by the viewer's authorized projects and visibility class; hiding a UI element is not authorization.

### 9.4 Product boundary clarification
The primary product workflow is foreman-to-contractor progress reporting. Investor access is an optional extension point, not a mandatory MVP user or a reason to build a full investor portal now. Direct worker reporting remains an open option, not a confirmed requirement.


## 10. Construction material and warehouse architecture — discovery extension
**User-confirmed direction:** include construction materials in the foreman's work context and add a **Thủ kho / Storekeeper** actor responsible for recording material receipts. Detailed workflow, approval authority and data schema remain hypotheses pending discovery.

### 10.1 Role workspaces
- **Foreman:** view relevant item catalogue and available balances; submit material requests linked to a project work item/area; see request and issue status.
- **Storekeeper:** assigned-warehouse workspace for receipt entry, stock movement, issue/return recording where authorized, stock count and discrepancy reporting.
- **Contractor:** project/warehouse oversight, assignment of storekeepers, policy and approval configuration, movement review and stock reports.
- **Investor (optional):** separately authorized, project-scoped summary view only when explicitly shared.

### 10.2 Candidate domain entities
Organization; Project; Warehouse; WarehouseMembership; MaterialItem; UnitOfMeasure; MaterialRequest; MaterialRequestLine; MaterialReceipt; MaterialReceiptLine; StockMovement; StockMovementLine; MaterialIssue; MaterialReturn; StockCount; StockAdjustment; SupplierReference; DocumentAttachment; ApprovalEvent; AuditEvent.
These are conceptual candidates, not a finalized schema. A project may have one or multiple warehouses; this remains OPEN.

### 10.3 Candidate transaction flow
Supplier/delivery arrives → storekeeper checks physical delivery and records a draft receipt with item/quantity/unit and evidence → authorized user verifies/posts the receipt → stock ledger and derived balance update → foreman submits a request against a work item → authorized contractor role approves or rejects if approval is required → storekeeper records actual issued quantity and recipient/work area → ledger updates → return/count/adjustment is separately recorded with reason and authority → contractor reviews material usage against progress reports.

### 10.4 State and integrity rules
- Distinguish draft, submitted, approved/rejected, posted, reversed and void states as appropriate; exact state machine is OPEN.
- Draft records do not affect on-hand stock. Only validated, authorized posted movements affect balances.
- Store balances as a projection derived from the movement ledger; do not accept a client-supplied balance as authoritative.
- Enforce positive quantity, valid unit, item/warehouse/project scope and permitted source/destination; support explicit unit conversion only when a governed conversion exists.
- Posted movement corrections require reversal or adjustment entries with actor, time, reason and reference; do not silently mutate history.
- Prevent duplicate receipt posting using stable document/reference identifiers and idempotency controls where available.
- Preserve attachment access controls and project isolation for delivery notes/photos.
- Reconcile physical count with ledger and record variances; never auto-correct discrepancies without an authorized adjustment.
- Keep procurement commitment, supplier invoice/payment and accounting valuation outside this workflow unless separately approved.

### 10.5 Separation of duties and authorization
- The storekeeper may record what was physically received; whether the same person may verify/post receipts, approve requests or authorize adjustments is OPEN.
- Foreman request authority does not imply authority to approve or issue stock.
- Contractor assigns project/warehouse memberships and explicit action permissions; authorization is checked server-side for every transaction.
- Investor access is not inherited from project membership; only explicitly shared summary fields are visible.
- Every transaction captures actor, timestamp, project, warehouse, item, quantity/unit, source/destination, supporting evidence, status and audit history.

### 10.6 Product boundary
The material extension covers operational stock visibility and movement records only. It does not authorize procurement, full ERP, accounting, cost valuation, QS/BOQ, automated purchasing or financial commitments. Material workflows must remain usable without AI; AI may only suggest extraction/classification after the Rule-first and privacy gates are met. W115 remains in 01_DISCOVER; no BUILD authorization.


## 11. Quantity takeoff, BOQ and estimating architecture — candidate extension
**Status: discovery architecture only.** This section extends the earlier Rule-first design. It supersedes the earlier statement that QS/estimating is excluded from all W115 scope; it does not approve implementation, final MVP scope, formulas, rates or AI drawing extraction.

### 11.1 Logical domain modules
- Drawing & Revision Register: controlled source files and immutable revision metadata.
- Measurement Workspace: takeoff sheets and quantity calculation lines.
- BOQ Workspace: structured work items, units, quantities, location and work-package grouping.
- Estimate Workspace: versioned norms, unit rates, cost build-up, assumptions and estimate snapshots.
- Review & Approval Workflow: role-authorized review, comments, approve/reject and revision supersession.
- Actual Progress & Acceptance: field-reported quantities and separately verified/accepted quantities.
- Materials Ledger: operational receipts/issues/returns/counts, linked by references to work items but not merged with takeoff or consumption data.
- Variance & Reporting: estimate/plan/actual/accepted/stock comparisons with provenance.

### 11.2 Core entities (conceptual; not finalized schema)
DrawingDocument, DrawingRevision, TakeoffSheet, TakeoffLine, MeasurementFormula, BOQ, BOQRevision, BOQLine, NormSet, NormItem, RateBook, RateRevision, Estimate, EstimateRevision, EstimateLine, EstimateApproval, WorkPackage, ProgressQuantity, QuantityVerification, AcceptanceRecord, MaterialMovement, VarianceRecord, AuditEvent.
Every revisioned aggregate needs stable identity, revision number, lifecycle state, creator, timestamps and links to its source/parent revision.

### 11.3 Quantity and cost provenance
Every takeoff line should preserve source drawing/revision, page/detail/zone, measurement method, dimensions or count, formula, unit, rounding rule, assumptions, preparer and reviewer. Every estimate line should preserve BOQ revision, norm/rate identifiers and revisions, price source/date, unit conversion basis, cost components and calculation version. Reproducible calculations belong in deterministic application logic, not in an LLM response.

### 11.4 Revision and state integrity
- Never mutate an approved revision in place; create a successor revision and preserve comparison history.
- A drawing revision change flags dependent takeoff lines for impact review; it must not silently recalculate or replace approved quantities.
- Draft/imported quantities are not approved BOQ quantities. Imported rows require schema, unit, duplicate and range validation plus a review state.
- Estimate totals are derived from line-level quantities and versioned rates using explicit, testable rounding rules.
- Approval records identify the approving actor, authority, time, comments and exact revision hash/identity.
- Contract variation/change orders remain a separately governed candidate workflow; no automatic contract amendment.

### 11.5 Separation of quantity, progress, acceptance and stock
- Drawing measurement, BOQ/estimate, contract quantity, planned quantity, reported execution, verified/accepted quantity and paid quantity are distinct ledgers or stateful records.
- Field progress can reference BOQ/work-package lines but cannot edit the approved estimate.
- Store issue is not consumption; consumption is not proof of completed work; completed work is not accepted work; accepted work is not proof of payment.
- Stock balance is derived only from posted material movement records. Estimated material norms create expected demand, not physical stock.
- Variance reports must show numerator, denominator, unit, source revisions and time window; flag incomparable or missing data instead of inventing a ratio.

### 11.6 AI boundary for drawings and estimates
AI may later assist with document classification, OCR, candidate dimension extraction or draft line descriptions. It cannot be the measurement authority, rate source, calculation engine, approval actor or source of truth. Preserve page/detail references, raw extracted text/geometry, model/provider/version, confidence, reviewer edits and final accepted value. Uncertain or unsupported extraction must abstain and route to manual measurement. No external model call with confidential drawings before privacy, contractual, security and cost approval. No model API, GPU, fine-tuning or training dataset is authorized here.

### 11.7 MVP sequencing proposal (not approved)
Stage A discovery prototype: Excel BOQ/estimate import, manual line entry, validation, version history and human review.
Stage B controlled calculation: approved units/norms/rates and deterministic estimate calculations after source standards are selected.
Stage C optional drawing assistance: PDF first, then specific CAD formats only after representative-file tests, measurement benchmark and independent engineering validation.
Stage D integrated controls: connect planned material demand, field actuals, warehouse movement and variance dashboard.
Each stage requires W70 gates and explicit scope approval; no BUILD authorization is implied.
