# YÊU CẦU SẢN PHẨM WORK 115 / PRODUCT REQUIREMENTS
- **STT / Document ID:** DOC-007
- **Priority:** P1
- **Read order:** 7
- **Depends on:** DOC-006
- **Status:** NOT STARTED — REQUIREMENTS NOT APPROVED
- **Version / Updated:** 0.1 / 2026-11-12

This document is an empty controlled requirements baseline. The following are candidate requirement areas only; none is approved or assigned a final priority yet.

## Candidate functional areas
- Project/site creation and project overview.
- Work item / task breakdown and worker assignment.
- Mobile-friendly field report submission.
- Report content: date/time, work description, progress, completed quantity/unit, photos and issues.
- Manager review, comments, correction requests and report history.
- Read-only dashboard for project progress, recent reports and unresolved issues.
- User accounts and role-based access.
- Search, filtering and export of reports, subject to privacy and data-retention decisions.

## Candidate non-functional areas
- Mobile-first usability on common Android phones and browsers.
- Reliable photo upload, upload retry and duplicate prevention.
- Clear handling of weak or intermittent network conditions.
- Secure authentication, authorization and project-level data isolation.
- Backups, recovery, audit trail and data export.
- Affordable hosting and low operational complexity.

## Non-goals to evaluate
Accounting, payroll, procurement, inventory/warehouse, full ERP, BIM/3D, GPS tracking and automatic worker surveillance are not part of the initial MVP unless the Product Owner later approves a change.

## Acceptance criteria
NOT DEFINED. Measurable acceptance criteria must be derived from validated user journeys during DEFINE. Do not use this candidate list as build authorization.


## 1.1 Confirmed business direction — reporting to the contractor
**User-confirmed direction (2026-11-12):** the site foreman / construction foreman (quản công) reports construction progress to the contractor (nhà thầu). The system may be extended to provide the project investor (chủ đầu tư) with access when needed.

This clarifies the primary operating relationship. It does not yet approve every detailed workflow, field, role permission or MVP feature.

### Candidate actor model
- **Quản công / Site Foreman — primary reporting actor:** prepares and submits progress reports for the assigned site/project and work items. Whether individual workers also submit directly remains OPEN.
- **Nhà thầu / Contractor — primary recipient and operational manager:** receives reports, monitors project progress, asks for clarification/correction and manages access for the contractor's project team. The exact authority of contractor owner, project manager and site supervisor must be discovered.
- **Chủ đầu tư / Project Investor — optional external stakeholder:** may be granted scoped access when the contractor/project requires it. Default candidate is read-only visibility to explicitly shared project reports and progress, not operational editing or approval authority. Actual permissions require explicit agreement.
- **Thợ / Field Worker — possible supporting actor:** may provide source updates or photos to the foreman, or report directly only if the actual site process requires it. Not confirmed as a mandatory account type.

### Candidate primary workflow
Contractor creates/opens a project and defines reporting expectations → assigns a foreman → foreman submits progress report with supporting details/photos → contractor reviews and requests clarification or correction → accepted report updates the project progress view → if enabled, investor sees the authorized report/progress view.

### Candidate report contents to validate
Reporting period/date; project and work item; work completed; progress/quantity and unit where measurable; planned versus actual progress if tracked; site photos; issues/risks/delays and required decisions; foreman identity and submission time; contractor review status/comments. Do not require every field until discovery validates its usefulness.

### Candidate access boundaries
- Access must be scoped to the specific contractor organization and project.
- A foreman sees and submits only for projects/assignments granted to them.
- Contractor staff see projects they are authorized to manage.
- Investor access is explicitly enabled per project, least-privilege, revocable and preferably read-only by default.
- Investor must not automatically see contractor's other projects, internal notes, worker personal data, costs or commercial information.
- A shared report should have a clear distinction between internal contractor notes and information intentionally visible to the investor.

### Open discovery questions
Confirm who creates projects and appoints the foreman; whether one contractor manages multiple projects; whether one project has multiple contractors; who reviews/accepts reports; report frequency (daily, shift-based, milestone or ad hoc); whether investors need live dashboard access or periodic exported reports; and which report fields are visible externally.


## 1.2 Confirmed business extension — construction materials and storekeeper
**User-confirmed direction (2026-11-12):** the construction foreman (quản công) also needs construction-material information/workflows, and a storekeeper (thủ kho) role is added to record material receipts into the project warehouse.

### Candidate role responsibilities
- **Quản công / Site Foreman:** views material availability relevant to assigned work; raises or records material needs for work items; confirms the intended work area/recipient for material requests. Whether the foreman may directly request, approve or record material issues remains OPEN.
- **Thủ kho / Storekeeper:** records actual received materials into the assigned project warehouse, including item, unit, quantity, receipt date/time, supplier/source and supporting delivery/receipt documents where available; maintains stock movement records; records issues/returns and physical counts only within granted authority.
- **Nhà thầu / Contractor:** manages project and warehouse access; defines who may request, approve, receive and issue materials; reviews material balances and exceptions. Approval hierarchy and purchasing responsibility remain OPEN.
- **Chủ đầu tư / Project Investor:** optional, explicitly scoped visibility only if enabled; no default access to internal warehouse notes, supplier/commercial data or detailed costs.

### Candidate material MVP workflows
1. **Material catalogue:** code/name, specification, unit of measure and active status. Avoid duplicate item identities within the relevant organization/project scope.
2. **Goods receipt / nhập kho:** storekeeper records actual delivered quantity, item, unit, date/time, warehouse/project, supplier/source and delivery note or photo evidence. A receipt is not proof of payment or procurement approval.
3. **Material request:** foreman records needed item, quantity, work item/area, required date and reason. Approval path is not yet confirmed.
4. **Material issue / xuất kho:** record actual issued quantity, recipient/team and destination work item/area, linked to an approved request where that workflow is adopted.
5. **Return/adjustment/count:** record returned material, damaged/lost quantity, stock count and any adjustment with reason and authorized actor. Never silently overwrite stock balances.
6. **Stock ledger and balance:** derive on-hand quantity from opening balance plus posted receipts and returns minus issues and authorized deductions/adjustments. Preserve transaction history and audit actor/time.
7. **Material report:** opening balance, receipts, issues, returns, adjustments and closing balance by project, warehouse, item and period.

### Candidate access boundaries
- Storekeeper access is limited to assigned project warehouse(s); no automatic visibility across the contractor's portfolio.
- Foreman sees material information needed for assigned work and may submit requests; cannot alter warehouse balances by editing a report.
- Only authorized roles may post receipts, issues, returns or adjustments. Keep request, approval and physical execution as distinct events when the workflow requires separation of duties.
- Each stock movement records actor, timestamp, item, unit, quantity, source/destination, project/warehouse, reference document and status.
- Stock balance is a derived view from an immutable/append-only movement ledger; corrections use reversal/adjustment entries, not destructive edits to posted transactions.
- Investor visibility is separately configured per project and should default to summary-level information only if explicitly shared.

### Scope boundary and unresolved discovery
This addition is a candidate material/warehouse workflow, not authorization for full ERP, purchasing, accounts payable, costing, inventory valuation, accounting, or automated procurement. Validate whether a project has one or multiple warehouses; whether storekeeper can also approve; who authorizes issues/adjustments; whether material is tracked by batch/lot or serial; treatment of transfers, returns, wastage and damaged goods; and whether balances are shared across projects. No BUILD authorization is implied.
