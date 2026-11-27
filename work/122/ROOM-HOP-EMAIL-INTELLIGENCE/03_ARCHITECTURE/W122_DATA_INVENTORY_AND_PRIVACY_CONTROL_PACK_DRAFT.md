# W122 — Data Inventory & Privacy Control Pack
**ID:** DATA-PRIV-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Owner:** Vinh — Product Owner
**Coordinator:** Xu / AI-01
**Status:** DESIGN PROPOSAL — NOT APPROVED
**Related:** ODR-W122-001 (ODR-03, 05, 06, 07, 08, 11, 12); SEC-W122-001; AUTH-STATE-W122-001; INT-CONTRACT-W122-001; T001–T024

> This document defines a proposed data inventory, purpose limitation, privacy controls and evidence requirements. It does not select retention periods, approve a provider/model, grant OAuth scopes, authorize mailbox access, or authorize implementation.

## 1. Privacy design principles

1. **Purpose limitation:** collect and process a field only for a documented product function.
2. **Data minimization:** prefer message IDs, timestamps, labels and limited headers over full message bodies where feasible.
3. **Mailbox isolation:** every record is bound server-side to tenant, verified owner, provider subject and mailbox connection ID. Never trust client-supplied tenant/mailbox identifiers.
4. **No implicit model disclosure:** message bodies, attachments and derived sensitive content must not be sent to an external model unless ODR-11 is decided and the provider/data-processing review is complete.
5. **No implicit retention:** transient processing is preferred. Persistent retention requires a declared purpose, location, access policy, deletion rule and recovery/backup treatment.
6. **Human authority:** AI classification, summaries and draft text are suggestions, not authorization for external actions.
7. **Verifiable deletion:** deletion must cover primary records, indexes, caches, derived artifacts and applicable backups according to an approved policy; record evidence without retaining the deleted content.
8. **No cross-customer learning by default:** do not reuse customer email content, prompts, summaries or attachments across tenants or for model training absent explicit lawful basis and owner approval.
9. **Fail closed:** if tenant ownership, consent, policy, audit or retention state cannot be established, deny processing or side effects.
10. **Separate demo from production:** synthetic demo data is preferred. A real mailbox must not be accessed until account identity, consent, scopes and gate approvals are verified.

## 2. Data inventory and proposed handling

| Data class | Examples | Purpose | Minimum proposed handling | Sensitivity / risk | Decision / dependency |
|---|---|---|---|---|---|
| Account identity | Tenant ID, owner principal, provider subject, mailbox connection ID | Bind mailbox to rightful tenant/owner | Store opaque identifiers and verified binding status; never expose OAuth tokens | High — account takeover/cross-tenant access | ODR-01, ODR-08; Core identity contract |
| OAuth secrets | Access/refresh tokens, client secrets, state/nonce | Provider authentication | Secret manager only; encrypted, least-privilege access, rotation/revocation; never logs, prompts, browser payloads or Git | Critical | ODR-03; approved vault and credential lifecycle contract |
| Message envelope | Provider message/thread IDs, received time, sender/recipient headers, labels, size | Inbox listing, threading, routing | Store only required fields; normalize carefully; avoid unnecessary recipient copies | High — personal contacts and relationship graph | ODR-03, ODR-06 |
| Message body | Plain text, HTML, quoted history, signatures | Summarization, extraction, draft assistance | Prefer transient bounded processing; redact/minimize; do not persist by default; external model blocked pending ODR-11 | Very high — personal, financial, legal, health and confidential content | ODR-03, ODR-06, ODR-11 |
| Attachments | PDFs, office files, images, archives | Potential later extraction | Excluded from initial release; no download, OCR, parsing or model upload unless separately approved | Critical — malware, PII, prompt injection, archive bombs | ODR-05, ODR-06, ODR-11 |
| Classification output | Priority, category, confidence, reason codes | Inbox triage and alerts | Store compact structured result with source IDs and model/policy version; mark as AI-generated | Medium–high — incorrect routing or sensitive inference | ODR-06, ODR-11 |
| Extracted action items | Tasks, due dates, commitments, named people | Task suggestions | Store only if feature approved; cite source message ID/snippet; require human confirmation before task dispatch | High — false commitments and personal data | ODR-06, ODR-08 |
| Summary | Thread summary, key points, next steps | Reduce reading effort | Minimize detail; source-linked; access controlled; same retention as derived personal data | High — may reveal more than source metadata | ODR-06, ODR-11 |
| Draft reply | Subject/body, recipients, attachments references | Human-reviewed response preparation | W122-local draft only as proposed default; immutable versions and provenance; no Gmail-native draft/send by default | Very high — disclosure and unintended commitment | ODR-04, ODR-08, ODR-09 |
| Approval record | Approver identity, approved recipient set, content hash, policy version, expiry | Authorize a future external side effect | Store immutable, tamper-evident metadata; single-use; bind exact content and recipient set | Critical | ODR-08, ODR-09 |
| Audit/security events | Access, policy decision, read/export/delete/approval/send attempts | Accountability and incident response | Append-only/tamper-evident; metadata only; no body/token/attachment content | High — audit leakage and repudiation | ODR-06, ODR-08; Core audit contract |
| Notification payload | Alert type, severity, message/thread reference | Inform user of action needed | Minimal metadata; no body preview by default; authorized recipient only | High — lock-screen/shared-device leakage | ODR-07 |
| Usage/billing telemetry | API calls, token counts, model latency, errors | Cost and reliability | Aggregate by tenant; avoid content; restrict raw identifiers; bounded retention | Medium | ODR-10, ODR-11 |
| Support/debug artifacts | Error traces, support exports, screenshots | Troubleshooting | Redact addresses, body, tokens and attachment names; explicit owner-approved export | High | ODR-06, ODR-11, ODR-12 |
| Deletion tombstones | Opaque record ID, deletion request ID, completion state | Prove deletion without retaining deleted data | Keep minimal non-content evidence; define expiry with approved retention schedule | Medium–high | ODR-06 |

## 3. Processing-stage controls

| Stage | Data touched | Required controls | Fail-closed condition |
|---|---|---|---|
| Connect mailbox | Identity, OAuth state/tokens, scopes | Verified owner binding; single-use expiring OAuth state; fixed redirect URI; secret manager; explicit consent | Identity mismatch, invalid state, missing consent, unapproved scope |
| Discover/sync | IDs, history cursor, envelope metadata | Per-mailbox cursor; idempotent sync; bounded fields; provider error handling; audit | Tenant mismatch, revoked token, stale cursor without safe resync plan |
| Fetch content | Body, headers | Just-in-time fetch; minimum scope; bounded size; sanitize HTML; no hidden remote content execution | Scope not approved, content exceeds safe bounds, policy/audit unavailable |
| Analyze | Body or metadata, derived output | Treat email as untrusted input; isolate model; no tool authority from email; redact; record model/policy version | ODR-11 unresolved for external model; prompt injection or provenance cannot be controlled |
| Persist results | Classification, summaries, tasks, drafts | Purpose-specific store; tenant-scoped access; retention tags; encryption; provenance | No approved retention/location/access rule |
| Notify | Minimal alert metadata | User preference, privacy-safe content, recipient validation, anti-loop and rate limits | Recipient not verified, sensitive preview requested without approval |
| Draft | Recipients, subject, body | Local draft namespace; version/hash; no automatic send; clear AI-generated provenance | Draft changed after approval or recipient scope unknown |
| Approve/send (future only) | Exact content and recipients | Human approval bound to mailbox, sender, To/Cc/Bcc, body/attachment hashes, policy version and expiry; durable outbox; reconciliation | Any mismatch, expired/reused approval, audit unavailable, ambiguous send state |
| Delete/export | All stored and derived data | Authenticated request; scope confirmation; dependency graph; deletion receipts; backup lifecycle | Cannot identify all copies or prove authorization |

## 4. Data-flow boundary

**Proposed flow:** Provider Gmail API → W122 provider adapter → Core identity/tenant/policy/audit boundary → minimal processing queue → approved analysis adapter → tenant-scoped result store → Dashboard.

- Gmail is a candidate first provider only; ODR-02 remains OPEN.
- Core is the authority for identity, tenant ownership, policy decisions and durable audit; the exact callable contract remains unverified.
- W52 is a candidate task/event dispatch boundary; do not treat its draft contract as a production runtime.
- W14 is a candidate execution host boundary; no email side effect may bypass approved Core/W52/W14 contracts.
- Dashboard is presentation-only and never grants permissions.
- External model providers are a separate trust boundary; no raw email content crosses it until ODR-11 is approved.
- Attachments are excluded from the initial release proposal.
- No data flow may use W120 or W121 as an implicit shared store or permission boundary.

## 5. Retention and deletion policy — unresolved owner decisions

No numeric retention period is selected in this draft. Before persistence, the Owner must decide retention separately for:
- OAuth connection metadata and token lifecycle records.
- Message envelope and synchronization cursors.
- Raw message bodies and attachment bytes (default proposal: do not persist).
- Summaries, classifications and extracted action items.
- Local drafts and draft versions.
- Approval records and security/audit logs.
- Notifications and delivery records.
- Backups, caches, search indexes and derived embeddings (if any).
- Support exports and deletion tombstones.

Each class requires: purpose; system of record; storage region; encryption; access roles; TTL; deletion trigger; backup expiry; legal hold behavior; export path; and deletion verification evidence. A delete request must not be reported complete while known replicas, indexes or backups remain outside the approved deletion schedule.

## 6. External model/provider review checklist

Before sending any real email content to a model/provider, record:
- Legal entity and service/product name.
- Data categories sent (metadata, body, quoted history, summaries, attachments).
- Processing region and subprocessors.
- Retention and deletion commitments, including abuse-monitoring logs.
- Whether data is used for training or service improvement and how to opt out.
- Encryption in transit/at rest and access controls.
- Contract/DPA and applicable cross-border transfer assessment.
- Redaction/minimization and tenant isolation.
- Incident notification, auditability and exit/deletion process.
- Model version, fallback and reproducibility expectations.

No provider is approved by this checklist. ODR-11 remains OPEN.

## 7. Privacy and security acceptance evidence

Minimum evidence before G2 can be reconsidered:
1. Approved data inventory and purpose map, signed by Owner.
2. Approved data-flow and trust-boundary diagram.
3. Per-field storage/location/access/retention/deletion schedule.
4. Verified tenant/mailbox ownership enforcement and negative isolation tests.
5. OAuth scope and credential lifecycle assessment.
6. Independent Ka review of privacy, prompt injection, attachment and audit controls.
7. Model-provider data-processing assessment and explicit Owner decision.
8. Notification privacy and recipient verification tests.
9. Deletion tests covering primary data, derived artifacts, indexes, caches and backup policy.
10. Synthetic acceptance evidence with Qw independent QE verdict.
11. Canonical Biên bản records decisions and dependencies.
12. No unresolved critical/high privacy or cross-tenant risk without explicit Owner acceptance and mitigation.

## 8. Open decisions and responsible input

| Decision | Required owner action | Technical/reviewer input |
|---|---|---|
| ODR-03 Scope | Select metadata-only vs body-read scope and release boundary | Kha Google scope/verification evidence; Ka security review |
| ODR-05 Attachments | Exclude, metadata-only, or defer extraction | Ka threat review; Qw negative tests |
| ODR-06 Retention/deletion/residency | Approve per-data-class schedule and deletion commitments | Ka privacy/security review; storage/backup contract evidence |
| ODR-07 Notifications | Select channels and content exposure | UX/privacy review; synthetic leakage and loop tests |
| ODR-08 Approval role | Owner-only or named human delegates | Core identity and audit contract; Ka review |
| ODR-11 Model processing | Select local/private, approved external, or metadata-only strategy | Provider terms/data-flow review; Ka privacy review |
| ODR-12 Handover | Confirm separate tenant onboarding for Anh Đức | Anh Đức acceptance input; Vinh final decision |

All listed decisions remain OPEN. Review roles are recommendations only; no task dispatch or reviewer acceptance is claimed.

## 9. Demo data policy

- Preferred first demo: synthetic mailbox fixtures with fictional senders, subjects and message bodies.
- The nominated mailbox address is a future demo target only. It does not establish verified account ownership, OAuth consent or permission to read messages.
- Do not copy personal email into fixtures, logs, prompts, screenshots, test snapshots or GitHub.
- If the Owner later authorizes a real mailbox pilot, start with a separate explicit consent and scope confirmation; verify identity; document data categories and deletion; use read-only permissions; and keep send disabled.
- Anh Đức receives a separate onboarding/tenant. Never reuse Vinh's OAuth token, mailbox content or credentials.

## 10. Gate truth

- This pack: **DRAFT / NOT APPROVED**.
- ODR-03, ODR-05, ODR-06, ODR-07, ODR-08, ODR-11, ODR-12: **OPEN**.
- Gmail OAuth/mailbox: **NOT CONNECTED / NOT VERIFIED**.
- External model processing of real email content: **NOT AUTHORIZED**.
- Attachment retrieval/extraction: **NOT AUTHORIZED**.
- Retention periods and data residency: **NOT DECIDED**.
- G2: **NOT READY / NOT APPROVED**.
- G3: **BUILD NOT AUTHORIZED**.
- No real email read/send, paid service, code execution or test execution performed by this document.
- W120/W121 remain untouched.

This document is a design/evidence checklist only. It is not legal advice, a privacy impact assessment approval, a production control certification, or authorization to process real mailbox data.
