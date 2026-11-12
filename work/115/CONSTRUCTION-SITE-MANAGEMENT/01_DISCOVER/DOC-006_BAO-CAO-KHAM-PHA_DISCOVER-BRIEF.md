# BÁO CÁO KHÁM PHÁ WORK 115 / DISCOVER BRIEF
- **STT / Document ID:** DOC-006
- **Priority:** P1
- **Read order:** 6
- **Depends on:** DOC-001; DOC-002
- **Status:** DRAFT — DISCOVERY IN PROGRESS
- **Version / Updated:** 0.1 / 2026-11-12
- **Product Owner:** Vinh
- **Orchestrator:** Xu / AI-01

## 1. Problem statement — initial
A construction manager may not have a simple, consistent way to receive structured progress updates from workers at different job sites. Verbal or scattered messages can make it difficult to consolidate daily progress, photos, completed quantities and issues. This is a problem hypothesis to validate with the intended user, not a confirmed finding.

## 2. Intended users
- Uncle / construction business manager — primary product beneficiary and likely manager user.
- Site supervisor / foreman — may assign or review work and consolidate updates.
- Construction worker — submits field updates from a phone.
Exact roles and permission boundaries are UNKNOWN pending interview.

## 3. Confirmed product direction from Vinh
- Create a web application.
- Workers working at construction sites report back through a phone.
- A manager reviews incoming information through a web interface.
- The application is intended as a gift for the user's uncle.

## 4. Discovery questions
- What type of construction does the uncle manage: residential houses, renovations, commercial buildings, or other?
- Does he manage one site at a time or multiple concurrent sites?
- Who creates projects, assigns work and approves daily reports?
- Do workers each have smartphones and reliable mobile data at the sites?
- Are photos, quantity, percentage complete, time, material usage and issues required?
- Is a report daily, per task, per shift, or event-based?
- Does the manager need cost, materials, payroll, quotations or customer reporting in the first release?
- What languages, devices and digital-literacy constraints apply?
- Is offline capture required, and how should delayed synchronization behave?
- What privacy, retention, backup and account recovery expectations apply?

## 5. Initial user journeys to validate
1. Manager creates a project/site and defines work items.
2. Manager assigns a worker or team to an item.
3. Worker opens a simple mobile-friendly report form.
4. Worker submits description, progress/quantity and optional photos.
5. Manager reviews, comments, requests correction or confirms the report.
6. Dashboard summarizes project progress and outstanding issues.

## 6. Risks and unknowns
- Network connectivity and photo upload reliability.
- Identity, role permissions and unauthorized access to site/customer data.
- Data loss, duplicate submissions and audit history.
- Workers' ability to use the interface quickly on low-end phones.
- Scope creep into accounting, payroll, materials and project ERP.
- Hosting cost and long-term maintenance for a gift intended to be useful.

## 7. Discovery conclusion
- Product direction: CONFIRMED at a high level.
- Detailed business workflow: NOT VERIFIED.
- Approved requirements: NOT STARTED.
- Architecture: initial hypotheses only.
- Implementation safe to begin: NO — discovery and requirements first.
- Next action: prepare a short interview/workflow walkthrough with the uncle and derive measurable MVP requirements.
