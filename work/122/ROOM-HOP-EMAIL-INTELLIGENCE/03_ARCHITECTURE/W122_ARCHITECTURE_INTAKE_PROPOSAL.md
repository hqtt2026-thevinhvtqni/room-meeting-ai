# W122 — KIẾN TRÚC ĐỀ XUẤT / ARCHITECTURE INTAKE
Status: PROPOSAL — NOT APPROVED; BUILD NOT AUTHORIZED
Date: 2026-11-25

## Logical architecture
1. Mailbox Registry & Identity: mailbox ID, provider, tenant/account reference, scopes, owner, state, policy version; secrets only in approved encrypted vault.
2. Provider Adapter: provider-specific OAuth/API/webhook/IMAP behind stable provider-neutral contracts.
3. Sync & Event Engine: push where available, polling fallback, cursor/checkpoint, dedupe, idempotency, bounded retry, dead-letter, reconciliation.
4. Normalization & Thread Context: canonical message/thread/attachment metadata with provider provenance.
5. Trust & Security Inspection: sender/authentication signals, suspicious links/attachments, prompt-injection boundary, sensitive-data detection. Never execute attachments.
6. Intelligence Pipeline: classify priority/security/action separately; summarize; extract explicit facts/deadlines; draft with confidence and source references.
7. Approval & Send Policy: send-time policy, allow-list, approval, recipient/content checks, rate limits, idempotency and provider receipt.
8. Notification Service: Dashboard + configured email alert; dedupe and loop prevention.
9. Mail Center UI: render canonical state; approvals route through authorized backend.
10. Audit & Observability: auth, sync, classification, draft, approval, send, failure, retry, revoke and policy changes.

## Canonical lifecycle
RECEIVED → SYNCED → NORMALIZED → SECURITY_SCREENED → CLASSIFIED → ACTION_REQUIRED / INFORMATIONAL / SUSPICIOUS → DRAFTED → PENDING_APPROVAL → APPROVED → SEND_QUEUED → SENT / SEND_FAILED.
Side states: QUARANTINED, REJECTED_BY_POLICY, DUPLICATE, REVOKED, EXPIRED. Draft ≠ sent; queued ≠ delivered; provider acceptance and delivery remain distinct.

## Priority and security are orthogonal
Priority: P0 Urgent; P1 Important; P2 Requires response; P3 Informational; P4 Spam/low relevance.
Security: TRUSTED / UNKNOWN / SUSPICIOUS / MALICIOUS / QUARANTINED. A P0 email may be malicious; security state overrides auto-send eligibility.

## Send policy
Default DENY until Owner enables narrowly scoped policy. Human approval required for quotes, contracts, payments, legal, complaints/disputes, sensitive data, external commitments, low-confidence or unsupported claims. Low-risk auto-send requires pre-approved rules/templates, known or allow-listed recipients, verified facts, rate limits and per-mailbox opt-in. Re-evaluate authorization at send-time. Do not assume exactly-once delivery; use idempotency/outbox/reconciliation and report UNKNOWN on ambiguous outcomes.

## ROOM-HOP mapping — hypotheses only
Core :8000 authority/policy/audit; Gateway :8040 provider ingress/egress; Event Listener :8050 events; Agent Runtime :8051 analysis/drafting; Dashboard :3000 rendering; Workspace :8010 optional authorized context. All mappings require source/runtime verification. No assumed API/endpoint; never use retired/broken routes.

## Contracts to define
MailboxConnectionContract; MessageEnvelope; SyncCheckpoint; ClassificationResult; DraftRecord; ApprovalDecision; SendCommand/Receipt; AuditEvent. Each must preserve mailbox identity, source provenance, policy version, correlation ID and idempotency scope.

## Threats
Prompt injection in body/thread/signature/invite/attachment; spoofing/compromised mailbox; OAuth consent abuse; token leakage; duplicate sends; cross-mailbox leakage; hallucinated promises/wrong recipients; malicious attachments/URLs; stale approval or changed draft; notification loops; quota/subscription expiry/cursor gaps.

## Open decisions
Provider order, retention, content storage, attachment handling, event transport, approval UX, auto-send eligibility, model choice, cost budgets, notification mailbox, audit retention, disaster recovery.

## Verification
Unit tests for normalization, classification schema, policy, idempotency and state machine. Provider contract tests; synthetic prompt-injection corpus; mailbox isolation/revoke tests; webhook replay/out-of-order and polling reconciliation; send-policy matrix including stale approval, changed body/recipient and timeout ambiguity. Independent QE and evidence read-back. No real external send in initial verification; controlled test sink only after explicit authorization.
