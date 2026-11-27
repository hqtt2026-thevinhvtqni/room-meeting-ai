# W122 — Owner Decision Closure Map
**ID:** ODCM-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Authority:** Vinh — Product Owner
**Coordinator:** Xu / AI-01
**Status:** FOR REVIEW — NO OWNER DECISION RECORDED
**Source of truth:** ODR-W122-001 (12 OPEN decisions)
**Related:** G2 Decision Pack; G2 Gate Readiness Checklist; SEC-W122-001; AUTH-STATE-W122-001; INT-GAP-W122-001; INT-CONTRACT-W122-001

> Purpose: make the existing 12 owner decisions easier to close by showing the safe default, evidence/reviewer input, gate dependency and work that can proceed without approval. This map does not replace ODR-W122-001 and does not itself approve any option.

## 1. Decision closure map

| ODR | Decision owner | Safe default proposed by Xu (not approved) | Required input / evidence before decision | G2 dependency | Can prepare without Owner approval |
|---|---|---|---|---|---|
| ODR-01 Pilot mailbox model | Vinh | One owner-designated personal mailbox for a single-user pilot; keep tenant/mailbox isolation explicit. The nominated demo address remains a proposal for a later verified connection, not proof of account identity. | Confirm who owns the mailbox, whether it is personal or delegated/shared, consent and account-identity verification method. Security review of tenant binding. | G2-01, G2-04, G2-14 | Define mailbox ownership schema, synthetic isolation tests and onboarding checklist. No OAuth or mailbox read. |
| ODR-02 Initial provider | Vinh | Gmail first, behind provider-neutral adapter; defer multi-provider until Gmail pilot is accepted. | Kha technical discovery on Gmail API/scope/verification constraints; adapter boundary and provider exit criteria. Kha review/receipt is NOT VERIFIED. | G2-01, G2-03, G2-04 | Specify provider-neutral logical interface and synthetic provider contract tests. |
| ODR-03 R2 access scope | Vinh; Kha supplies Google-specific evidence; Ka reviews security | R2 read-only with narrowest scope that meets approved use. Metadata-only cannot summarize bodies; Gmail readonly is restricted-scope territory and requires a current Google verification assessment. No Gmail Compose/send scope. | Exact use cases (headers vs body), Google scope table, restricted/sensitive classification, verification/security assessment, data minimization and OAuth consent plan. Kha findings and Ka verdict not received/verified. | G2-03, G2-08, G2-12, G2-14 | Prepare scope-to-feature matrix and negative tests proving unavailable capabilities remain denied. No OAuth client or consent. |
| ODR-04 Draft behavior | Vinh; Ka reviews security | R3 W122-local draft only. Do not use Gmail-native draft/Compose by default because its scope may carry send capability. | UX and audit requirements; local draft provenance/versioning; explicit assessment if Gmail-native draft is later requested; Ka review. | G2-08, G2-09, G2-10, G2-14 | Design local draft schema, immutable versions and synthetic provenance tests. No Gmail draft creation. |
| ODR-05 Attachments | Vinh; Ka reviews threat/safety | Exclude attachment content and extraction from initial release; retain no content. Decide separately if minimum metadata is necessary. | Attachment threat model (malware, prompt injection, archive bombs, PII), allowed types/size limits, scanning/isolation and deletion evidence. | G2-08, G2-10, G2-12 | Add synthetic malicious-file cases and a deny-by-default attachment policy. No real attachment processing. |
| ODR-06 Retention/deletion/residency | Vinh; Ka reviews privacy/security | Minimize persisted data; do not retain raw bodies or attachments beyond bounded processing until explicit retention, deletion and residency policy exists. | Data inventory by field, purpose, storage location, TTL, deletion proof, backup behavior, legal/privacy obligations and export requirements. | G2-05, G2-12, G2-13, G2-14 | Build data classification and lifecycle requirements; define synthetic deletion acceptance criteria. Do not choose a retention duration on Owner's behalf. |
| ODR-07 Notifications | Vinh | Dashboard alerts with minimal metadata; no body preview by default. Email notifications are a separate channel requiring privacy and loop controls. | User workflow, urgency classes, notification content/recipient, opt-out, delivery failure, anti-loop and privacy review. | G2-12, G2-10, G2-14 | Prototype notification event schema and synthetic loop/privacy tests without sending notifications. |
| ODR-08 Human approval role | Vinh | Verified mailbox owner approves every external side effect. Delegation only to named human identities with explicit scope, expiry and revocation. AI cannot approve its own output. | Identity assurance, delegation model, separation of duties, approval audit, revocation and emergency recovery. Ka independent review required. | G2-04, G2-05, G2-08, G2-09, G2-14 | Define role/capability tests and approval-binding contract. No external action. |
| ODR-09 Auto-send | Vinh | No auto-send in initial product; default DENY. Any future allow-list must be a separate R4 release gate with narrow categories, recipients, content constraints and revocation. | Risk appetite, category/partner allow-list, exclusions, immutable approval alternative, monitoring, rollback, outbox/idempotency and incident handling. Ka security verdict and QE negative tests required. | G2-08, G2-09, G2-10, G2-14; later R4 gate | Define future gate criteria and synthetic adversarial tests only. Do not implement send or enable Gmail send scope. |
| ODR-10 Cost ceiling | Vinh; Go supplies cost model | No paid service or recurring commitment until a budget ceiling and billing owner are approved. | Usage assumptions, Gmail API quota/cost, Pub/Sub/hosting/storage/model cost, alerting and monthly worst-case estimate. Go cost review/receipt not verified. | G2-11, G2-14 | Prepare a cost worksheet with variables and zero-spend design assumptions; no paid provisioning. |
| ODR-11 Data/model processing | Vinh; Ka reviews privacy/security; technical model comparison may be delegated | No email body or attachment sent to an external model until provider, region, retention, training-use, subprocessors and contractual terms are reviewed and approved. Metadata-only or private/local processing are candidates, not decisions. | Data-flow diagram, model/provider terms, region and retention guarantees, training-use policy, redaction, DPA/security review and fallback behavior. | G2-08, G2-12, G2-13, G2-14 | Keep model adapter abstract; create synthetic data tests and a provider assessment template. No real mail content to a model. |
| ODR-12 Anh Đức handover | Vinh; Anh Đức provides user acceptance/input | Separate onboarding and consent for Anh Đức; no transfer of Vinh's mailbox, credentials, messages or tenant data. Require role setup, revoke path, support and data-boundary verification. | Confirm intended operating model (single-user handover vs managed multi-user tenant), account owner, consent, support responsibility, training and acceptance criteria. | G2-01, G2-04, G2-12, G2-14 | Prepare a tenant-isolated onboarding/runbook and demo using synthetic data. Do not onboard or expose Vinh's mailbox data to Anh Đức. |

## 2. Recommended closure order

1. **Product boundary:** ODR-01, ODR-02, ODR-12 — establish who the pilot serves, which mailbox model is in scope, and how Anh Đức receives a separate tenant.
2. **Data access and privacy:** ODR-03, ODR-05, ODR-06, ODR-11 — decide what data is read, retained, attached and processed by models.
3. **Human workflow:** ODR-04, ODR-07, ODR-08 — decide local drafts, alert channel and who can approve.
4. **Risk and economics:** ODR-09, ODR-10 — keep auto-send off and settle the cost ceiling before any paid dependency.
5. Record each decision in the canonical Biên bản, update ODR status with exact evidence, then reassess all G2 criteria. Do not mark G2 PASS merely because the documents exist.

## 3. Reviewer responsibility — proposed, not dispatched

- **Kha / AI-04:** Gmail API, OAuth scope classification, Google verification implications, quota and provider discovery for ODR-02/03/10. No W122 dispatch/receipt/review is verified.
- **Ka / AI-02:** independent security/privacy review of ODR-03/04/05/06/08/09/11 and SEC-W122-001 / AUTH-STATE-W122-001. No W122 dispatch/receipt/review is verified.
- **Go / AI-06:** cost model and budget scenarios for ODR-10; independent review only for work not authored by Go. No W122 dispatch/receipt/review is verified.
- **Anh Đức:** user acceptance and handover requirements for ODR-12; consultation is not a substitute for Vinh's Product Owner decision.
- **Vinh:** final decision authority for all 12 items. Technical reviewers advise; they do not approve product policy or spend.

## 4. Exact decision-recording rule

For each ODR item, record all of:
- Decision ID and status: ACCEPT / REJECT / DEFER.
- Exact selected option and scope; if custom, state the complete rule.
- Rationale and risk accepted.
- Effective date and decision owner.
- Preconditions, dependencies and evidence references.
- Canonical Biên bản section/revision.

A decision remains OPEN until this record exists. “Tiếp”, “OK”, silence, a draft recommendation, a reviewer assignment without receipt, or a GitHub commit is not an approval. DEFER must include the missing condition and a review trigger/date; it does not silently satisfy G2.

## 5. Work that may continue safely

- Refine logical contracts and synthetic test design.
- Prepare data inventory, privacy assessment template, cost worksheet and onboarding/runbook.
- Reconcile source-level Core/W52/W14 contracts only through approved read-only evidence.
- Obtain genuine Kha/Ka/Go review receipts through a verified dispatch route.
- Maintain the nominated demo mailbox as a future test target only; verify account identity and obtain explicit OAuth consent before any mailbox access.

## 6. Gate and scope truth

- ODR-01 through ODR-12: **OPEN**.
- G2: **NOT READY / NOT APPROVED**.
- G3: **BUILD NOT AUTHORIZED**.
- OAuth / Gmail mailbox connection: **NOT CONNECTED / NOT VERIFIED**.
- Real email read, Gmail-native draft, send, archive, label, delete, forward and filter mutation: **NOT AUTHORIZED / NOT PERFORMED**.
- Paid services: **NOT APPROVED**.
- Kha/Ka/Go W122 review receipt: **NOT VERIFIED**.
- W120 and W121: **UNTOUCHED**.

This is a closure guide, not an approval record, implementation authorization, or claim that any reviewer has accepted a task.
