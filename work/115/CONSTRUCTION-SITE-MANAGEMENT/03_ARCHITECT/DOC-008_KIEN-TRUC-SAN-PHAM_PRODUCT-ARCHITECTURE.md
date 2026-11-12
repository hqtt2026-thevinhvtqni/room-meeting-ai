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
