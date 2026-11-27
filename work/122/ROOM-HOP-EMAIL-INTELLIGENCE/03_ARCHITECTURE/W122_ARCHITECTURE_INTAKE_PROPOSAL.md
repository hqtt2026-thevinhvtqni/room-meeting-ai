# W122 — KIẾN TRÚC ĐỀ XUẤT / ARCHITECTURE INTAKE
Status: PROPOSAL — NOT APPROVED; BUILD NOT AUTHORIZED
Date: 2026-11-25

## 1. Logical architecture
1. Mailbox Registry & Identity: mailbox ID, provider, tenant/account reference, granted scopes, owner, state, policy version. Secrets are stored only in approved encrypted vault.
2. Provider Adapter: provider-specific OAuth/API/webhook/IMAP implementation behind a stable contract. No provider-specific token or object leaks into domain logic.
3. Sync & Event Engine: push subscriptions where available, polling fallback, cursor/checkpoint, deduplication, idempotency, bounded retry, dead-letter and reconciliation.
4. Normalization & Thread Context: canonical message/thread/attachment metadata; preserve provider IDs and source provenance.
5. Trust & Security Inspection: sender/authentication signals, suspicious-link/attachment metadata, prompt-injection boundary, sensitive-data detection. Never execute attachments.
6. Intelligence Pipeline: classify priority/action/security separately; summarize; extract explicit facts/deadlines; draft response with confidence and source references.
7. Approval & Send Policy: policy evaluation at send-time, mailbox-specific allow-list, approval requirement, recipient/content checks, rate limits, idempotency key and send receipt.
8. Notification Service: Dashboard + configured email alert, loop prevention and deduplication.
9. Mail Center UI: render-only consumer of canonical state; user approval action goes through authorized backend command, not direct provider credentials.
10. Audit & Observability: append-only event trail for auth, sync, classification, draft, approval, send, failure, retry, revoke and policy changes.

## 2. Canonical lifecycle
RECEIVED → SYNCED → NORMALIZED → SECURITY_SCREENED → CLASSIFIED → ACTION_REQUIRED / INFORMATIONAL / SUSPICIOUS → DRAFTED → PENDING_APPROVAL → APPROVED → SEND_QUEUED → SENT / SEND_FAILED.
Terminal or side states: QUARANTINED, REJECTED_BY_POLICY, DUPLICATE, REVOKED, EXPIRED.
A draft is never represented as sent. A queued request is never represented as delivered. Provider acceptance/receipt and later delivery status must remain distinct.

## 3. Priority and security are orthogonal
Priority:
- P0 Urgent
- P1 Important
- P2 Requires response
- P3 Informational
- P4 Spam / low relevance

Security assessment:
- TRUSTED / UNKNOWN / SUSPICIOUS / MALICIOUS / QUARANTINED.
A P0 email may still be malicious. Security state overrides auto-send eligibility.

## 4. Send policy
Default DENY for autonomous sending until Owner enables a narrowly scoped policy.
Require human approval for quotes, contracts, payments, legal, complaints/disputes, sensitive personal/business data, external commitments, low-confidence or unsupported factual claims.
Eligible low-risk automatic responses must use pre-approved templates/rules, known recipients or allow-listed partner domains, factual verified context, rate limits and per-mailbox opt-in.
Every send re-evaluates policy and authorization immediately before provider call.
Exactly-once delivery cannot be assumed across network failures; use idempotency/outbox/reconciliation and surface UNKNOWN when provider outcome is ambiguous.

## 5. ROOM-HOP mapping — hypotheses to verify
- Core :8000: canonical authority, mailbox grants, policy decisions, audit.
- Gateway :8040: provider adapter ingress/egress.
- Event Listener :8050: provider events/webhooks.
- Agent Runtime :8051: classification and drafting orchestration.
- Dashboard :3000: Mail Center rendering only.
- Workspace :8010: possible document/context surface only if authorized.
These are candidate mappings, not verified runtime facts. W122 must inspect actual source contracts and deployed routes before binding to them. Never use retired/broken routes.

## 6. Key contracts to define
- MailboxConnectionContract: provider, mailbox_ref, scopes, token_ref, status, expiry, revoke.
- MessageEnvelope: provider_message_id, mailbox_id, thread_id, sender, recipients, subject, received_at, body_ref, attachment_refs, auth_signals, source_provenance.
- SyncCheckpoint: cursor, history_id/delta_token, last_success, subscription_expiry, idempotency namespace.
- ClassificationResult: priority, security_state, action_required, extracted_facts, confidence, evidence_refs, model_version.
- DraftRecord: source_message_refs, proposed_recipients, subject/body, factual_claim_refs, confidence, policy_tags, state.
- ApprovalDecision: actor, decision, scope, policy_version, timestamp, reason.
- SendCommand/Receipt: idempotency_key, approved_draft_hash, recipient_set, provider_request_id, outcome, timestamps.
- AuditEvent: actor, mailbox, action, policy version, correlation ID, outcome, evidence reference.

## 7. Threats / abuse cases
- Prompt injection in body, quoted thread, signature, calendar invite or attachment.
- Spoofed sender / compromised mailbox / malicious OAuth consent.
- Token leakage through logs, prompts, GitHub or exception traces.
- Duplicate sends from webhook retries, polling overlap or agent retries.
- Cross-mailbox data leakage or wrong sender identity.
- Model hallucination / fabricated promise / wrong recipient.
- Malicious attachment, macro, URL or HTML tracking content.
- Auto-send policy bypass through stale approval, changed draft or changed recipient.
- Notification loop and event storms.
- Provider quota, subscription expiry and cursor gaps.

## 8. Open architecture decisions
ADR required for provider order, data retention, content storage, attachment policy, event transport, approval UX, auto-send eligibility, model selection, cost budgets, notification mailbox, audit retention and disaster recovery.
No decision is final until source evidence, reviewer feedback and one official decision record exist.

## 9. Verification strategy
- Unit tests for normalization, classification schema, policy evaluator, idempotency and state machine.
- Contract tests against provider mocks and official test tenants.
- Synthetic malicious/prompt-injection corpus; prove deny/quarantine behavior.
- Multi-mailbox isolation and token-revocation tests.
- Webhook duplicate/out-of-order/replay and polling reconciliation tests.
- Send-policy matrix: allow/deny/approval-required, stale approval, changed body/recipient, timeout ambiguity.
- Independent QE report and evidence read-back.
- No real external send during initial verification; use provider test tenant or controlled sink after explicit approval.


## 10. Detailed logical data model — proposal only
The following are domain contracts, not deployed database tables or approved ROOM-HOP API routes.

### 10.1 MailboxAccount
- mailbox_id: opaque internal ID; never use email address as the authorization key.
- owner_user_id / tenant_id: immutable owner and tenant boundary.
- provider / provider_account_ref: provider identity and opaque account reference.
- granted_scopes: exact consented scopes; store grant metadata, not raw tokens.
- credential_ref: pointer to an approved secret vault only.
- connection_state: PENDING, CONNECTED, DEGRADED, REAUTH_REQUIRED, REVOKED, ERROR.
- policy_id / policy_version; connected_at, last_verified_at, revoked_at.
- Every read, sync, draft, approval and send operation must resolve mailbox ownership before execution.

### 10.2 Message and Thread
- MessageRecord: internal message_id, mailbox_id, provider_message_id, thread_id, sender/recipient headers, subject, received_at, normalized_body_ref, attachment_refs, provider_labels, authentication_signals, content_hash, source_provenance, sync_version.
- ThreadRecord: internal thread_id, mailbox_id, provider_thread_id, ordered message references, latest_message_at.
- Body and attachment bytes are separated from metadata and stored only under an explicit retention/encryption policy. Do not place raw message bodies, access tokens or attachment bytes in logs, agent task payloads, or GitHub.
- Preserve original provider IDs and timestamps. Do not silently rewrite quoted content or collapse distinct messages.

### 10.3 Intelligence and action records
- AnalysisRecord: message/thread refs, priority, security_state, action_required, category, extracted facts/deadlines, confidence, evidence_refs, model/provider/version, created_at.
- DraftRecord: immutable draft revision, source refs, mailbox_id, sender identity, exact recipient set, subject/body hash, factual_claim_refs, template/policy version, status, expires_at.
- ApprovalRecord: approving actor, role, mailbox_id, draft revision/hash, exact recipient-set hash, decision, reason, policy version, created_at, expires_at.
- SendAttempt / SendReceipt: idempotency key, immutable approved draft hash, recipient-set hash, provider request ID, attempt number, outcome SENT/FAILED/UNKNOWN, provider acceptance timestamp and reconciliation state.
- AuditEvent: append-only event ID, actor, mailbox, action, correlation ID, policy version, timestamp, outcome and evidence reference. Do not store secrets or full message bodies in audit records.

## 11. Logical service boundaries and command contracts
These names describe internal capabilities only; they are not claims that endpoints or services currently exist.
1. Mailbox Registry: register connection metadata, inspect state, list owner-authorized mailboxes, revoke.
2. Provider Adapter: verify identity, list changes, fetch message/thread, create draft, send only when explicitly authorized by policy.
3. Sync Coordinator: start bounded initial sync, advance cursor, deduplicate events, reconcile gaps, renew subscriptions.
4. Message Intelligence: normalize, security-screen, classify, extract facts, summarize and draft.
5. Policy & Approval: evaluate action against mailbox policy; create, expire and revoke approvals; re-evaluate at execution time.
6. Outbox Executor: accept only immutable approved commands; enforce idempotency; record provider result; reconcile UNKNOWN outcomes.
7. Notification: publish deduplicated dashboard/email alerts without creating mail loops.
8. Audit & Observability: query provenance and operational outcomes with role-based redaction.

Every command must carry: authenticated actor identity, tenant_id, mailbox_id, correlation_id, idempotency_key where applicable, policy_version and explicit source references. Backend must derive authority from authenticated context; it must not trust a mailbox_id or role supplied by the UI alone.

## 12. End-to-end processing sequence
A. Connect: user explicitly chooses provider and mailbox; OAuth state is single-use, short-lived and bound to owner, tenant, redirect URI and connection attempt. Verify returned account identity before setting CONNECTED. Store tokens only in the approved vault.
B. Initial sync: request the narrowest required scope; page through bounded metadata; fetch bodies only when the selected feature requires them. Save cursor/checkpoint only after durable processing. Enforce mailbox-specific rate limits.
C. Incremental sync: provider push is a wake-up signal, not the source of truth. Validate notification origin, deduplicate/replay-protect, fetch authoritative changes from cursor, persist event and advance cursor transactionally. Periodic reconciliation is mandatory. On stale cursor, mark GAP_DETECTED and perform controlled resync; never silently skip the gap.
D. Normalize and inspect: sanitize HTML for display, retain provenance, inspect sender authentication and URL/attachment metadata, quarantine suspicious content. Attachments are inert data; never execute macros, scripts, links or embedded instructions.
E. Analyze: treat all email content as untrusted data, not system/developer instructions. Separate quoted text, sender claims and verified facts. Every extracted deadline, amount, commitment or requested action must cite its source message span/reference. Low confidence becomes NEEDS_REVIEW.
F. Notify: send a deduplicated alert containing minimum necessary metadata and a secure link to the authorized Mail Center. Do not copy sensitive body content into notification channels by default.
G. Draft: produce a draft linked to exact source messages, mailbox identity and recipients. Draft creation does not imply approval or sending.
H. Approve/execute: approval is bound to exact draft revision/hash, mailbox, sender identity, recipient set and policy version. Any change invalidates approval. Re-evaluate current policy and mailbox connection immediately before send.
I. Reconcile: distinguish provider accepted, delivered (if provider reports it), failed and UNKNOWN. On timeout, query/reconcile before retry; never blindly resend.

## 13. Default automation policy matrix
| Action/category | Default behavior | Autonomous send |
|---|---|---|
| Read headers / classify metadata | Allowed only for connected, owner-authorized mailbox and granted scope | Not applicable |
| Read body / summarize | Only when feature requires it and user policy permits | Not applicable |
| Draft routine acknowledgement | Draft only; show source and confidence | DENY by default |
| Routine low-risk reply to pre-approved partner | Draft + approval during initial release | Only after separate Owner opt-in, narrow rule, template, recipient allow-list and negative tests |
| Quotes, pricing, purchase orders, payments, invoices | Human approval | DENY |
| Contracts, legal, regulatory, HR, complaints or disputes | Human approval and elevated review | DENY |
| Credentials, security alerts, account recovery, personal/sensitive data | Quarantine or human review | DENY |
| External promise, delivery date, refund, admission of liability, policy exception | Human approval | DENY |
| Unknown sender, spoofing signals, suspicious URL/attachment, prompt injection | Quarantine / no action | DENY |
| Low confidence, missing source evidence, conflicting thread facts | Human review | DENY |

Autonomous sending is a later, separately approved capability; it is not part of the initial Gmail demo or a consequence of connecting a mailbox.

## 14. Privacy, retention and tenant isolation
- Tenant and mailbox isolation are mandatory at every storage, query, cache, vector/search index, task, log, export and notification boundary.
- Never use a global mailbox search without an owner/tenant-scoped authorization filter enforced server-side.
- Encrypt credentials and message content at rest and in transit; use separate vault references and key/access policies. Do not put secrets in source control, prompts, logs, screenshots or test fixtures.
- Retain the minimum data required. Proposed configurable classes: connection metadata; message metadata; message body; attachment bytes; derived summaries/drafts; audit records. Exact retention periods are an ADR/Owner decision and must not be guessed.
- Provide disconnect/revoke, stop-sync, export and deletion workflows with auditable completion; revocation must stop future provider calls and invalidate pending send commands.
- Redact notification previews and analytics by default. Support user-configurable retention only within legal/provider constraints.
- Cross-mailbox retrieval is forbidden unless the actor has explicit authority for every mailbox in the result set.

## 15. Failure, retry and recovery rules
- Provider 401/invalid_grant: pause sync, mark REAUTH_REQUIRED, alert owner; do not loop refresh attempts.
- Provider 403/scope missing: fail closed and request the narrowest additional consent only when a feature requires it.
- 429/quota: bounded exponential backoff with jitter and per-mailbox fairness; expose retry-after and queue age.
- 5xx/network interruption: retry idempotent reads; use outbox and reconciliation for writes.
- Duplicate/out-of-order push: deduplicate by provider event/message identity and cursor; do not duplicate classification or send.
- Stale cursor/history expiration: GAP_DETECTED, controlled full sync, reconcile counts and provenance before clearing gap.
- Ambiguous send timeout: outcome UNKNOWN; block automatic resend until provider reconciliation or human resolution.
- Revoked connection/policy: cancel pending work and invalidate approvals immediately.
- Poison message/attachment: quarantine that item without blocking unrelated mailbox processing.

## 16. Release slices and exit criteria — proposed
- Slice 0 / Design: close G0–G2; owner-approved architecture, data/privacy ADRs, security review, verified ROOM-HOP contracts. No live mailbox operations.
- Slice 1 / Synthetic core: provider-neutral schema, deterministic state machine, policy evaluator, audit, fake provider and synthetic mail corpus. No OAuth or real mailbox.
- Slice 2 / Read-only Gmail pilot: only after approved OAuth design and explicit account consent; identity verification, bounded read, sync recovery, mailbox isolation, no draft/send mutation.
- Slice 3 / Draft-only: draft generation with source references, confidence and approval UX; no send permission.
- Slice 4 / Controlled send: separate Owner authorization, narrow allow-list/template, immutable approval binding, outbox/reconciliation, negative security tests and independent QE PASS.
- Slice 5 / Anh Đức handover: tenant/mailbox onboarding, documented roles, training, backup/revoke, operational dashboard, incident and support runbook. No release until acceptance evidence is complete.

## 17. Decisions still reserved for Owner / ADR
Provider order beyond first Gmail demo; mailbox count and tenant ownership model; body/attachment retention periods and storage region; whether attachment content is ever indexed; notification destination; model/provider and data-processing terms; monthly budget and quota limits; approval roles/delegation; auto-send categories and partner allow-list; audit retention; backup/deletion and disaster recovery. No paid service or external commitment without explicit Owner approval.

## 18. Explicit unknowns and build blockers
- Approved Core identity/mailbox authorization and audit contracts are not yet evidenced.
- Approved W52 task dispatch and execution contract is not yet evidenced.
- Production provider adapter, webhook ingress, durable queue/outbox and secret vault are not yet verified.
- Actual deployed routes and service ownership for Core/Gateway/Event Listener/Agent Runtime are not verified.
- Kha and Ka briefs exist, but no verifiable dispatch/receipt or independent findings are present.
- Original source email is absent from the inspected 01_ORIGINAL folder.
- G0/G1 owner requirements/decision and G2 architecture approval remain open; G3 BUILD remains NOT AUTHORIZED.


## 19. Updated ROOM-HOP integration evidence — 2026-11-27
This section records read-only findings from current Sandbox artifacts. It does not approve or implement an integration.

### 19.1 W52 A2A candidate boundary
- W52 `a2a-contract-v0.1.md` is explicitly DRAFT; the schema checks described there are author-run and not independent PASS.
- W52 `adapter-interface.md` defines an injectable library, not an HTTP service or executor. CorePort and AuthorityPort require existing authorized Core implementations; HostPort belongs to the W14 execution-host owner.
- The inspected candidate profile is no-tool/read-only and advertises only `task.stream_events`. Tasks requiring tool access, writes, approvals or resume are explicitly unsupported pending verified W14 integration.
- W52 permission matrix states task roles are assertions to verify, not credentials; PASS requires an independent tester/reviewer with separate Authority grant and evidence. A creator cannot independently accept their own candidate.
- W52 event model is DRAFT; sequence continuity, state-transition validity and at-least-once conformance are explicitly not verified by the described schema checks.
- A W52 evidence file records a Ka review task as ASSIGNED IN SANDBOX but says Ka ACK is not verified. This is W52-specific evidence only; it is not a receipt or review for W122.

### 19.2 W11 and W12 production boundaries
- W11 `PRODUCTION_INTEGRATION_BOUNDARY.md` requires an approved member identity to be resolved by Core, Core to validate identity and policy, and Core to own membership, message identity, correlation, persistence and deduplication. It explicitly declines to guess unreadable identity-registration or Room-join calls.
- W12 `EXECUTION_HOST_BOUNDARY.md` confirms the current task exposes only Sandbox file APIs. Process/service, Git gateway, GitHub gateway, CI and WorkContext-bound browser adapters are NOT_CONFIGURED / not exposed through the inspected ROOM-HOP adapter.
- Therefore W52 is a useful candidate contract reference, not a production dispatch mechanism or email executor. W122 must not call guessed Core/Gateway routes, instantiate its own parallel identity/event store, or treat a Sandbox task record as a verified agent execution.

### 19.3 W122 integration decision pending
Before implementation, obtain: (1) approved Core identity/tenant/mailbox authorization and audit contract; (2) approved W52 task submission/receipt/event contract and verified registry identity for each agent; (3) approved W14 Host interface and actual runtime deployment evidence; (4) approved provider-adapter ingress/egress and secret-vault contracts; and (5) independent security/QE acceptance. Until then, only design and synthetic specifications may proceed. G2 remains NOT APPROVED; G3 BUILD remains NOT AUTHORIZED.
