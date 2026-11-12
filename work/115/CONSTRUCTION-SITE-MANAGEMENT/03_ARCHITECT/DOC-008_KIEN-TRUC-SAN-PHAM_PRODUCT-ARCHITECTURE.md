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
