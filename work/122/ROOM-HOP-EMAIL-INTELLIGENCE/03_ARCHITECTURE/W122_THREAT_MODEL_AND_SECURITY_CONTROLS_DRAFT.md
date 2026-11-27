# W122 — THREAT MODEL & SECURITY CONTROLS (DRAFT)
**Document code:** SEC-W122-001  
**Version:** 0.1-DRAFT  
**Date:** 2026-11-27  
**Owner:** Vinh (Product Owner)  
**Prepared by:** Xu / AI-01  
**Review status:** PENDING — independent security review by Ka (AI-02) not received  
**Gate status:** G2 NOT APPROVED · G3 BUILD NOT AUTHORIZED

> This is a working threat model for review, not an approved security baseline. Controls below are proposed requirements. No production implementation or security test has been performed.

## 1. Purpose and scope
Identify threats to the W122 email-intelligence product across mailbox connection, synchronization, message interpretation, classification, summarization, draft creation, approval, notification, and any future sending. The first demonstration is intended to use one Owner-designated Gmail mailbox, initially read-only and draft-only. The product must later support multiple independently isolated mailboxes for Anh Đức and other authorized users.

In scope:
- OAuth identity and mailbox ownership binding; token/credential lifecycle.
- Gmail/provider API ingestion, push notifications, history cursors, retries and reconciliation.
- Untrusted message bodies, headers, attachments, links and embedded instructions.
- AI classification, extraction, summarization and reply drafting.
- Dashboard, notifications, approval workflow, audit and future send boundary.
- Tenant isolation, retention, deletion, revocation, operational and supply-chain risks.

Out of scope for this draft:
- Penetration testing, production configuration review, formal privacy/legal assessment, cloud IAM verification, and certification.
- Any claim that ROOM-HOP Core, W52 dispatch, provider adapter, credential vault, queue/outbox or production routes are already deployed and compliant.

## 2. Security objectives
1. **Mailbox sovereignty:** only the verified owner/tenant may access a mailbox; no cross-tenant reads or writes.
2. **Least privilege:** request only the narrowest provider scopes needed for the currently enabled feature.
3. **No authority from content:** email text, sender display name, links, attachments, quoted text and AI output cannot grant permissions or approve side effects.
4. **Human control:** initial release is read-only + draft-only; sending and destructive mailbox actions remain disabled.
5. **Integrity:** approvals bind to the exact mailbox, sender identity, recipient set, content hash, policy version, approver and expiry.
6. **Confidentiality:** minimize collection, display, retention and logging of message bodies, attachments, tokens and personal data.
7. **Recoverability:** duplicate, delayed, reordered or missing provider events must not cause duplicate actions or silent data loss.
8. **Accountability:** security-relevant events are attributable, tamper-evident and reviewable without logging secrets or unnecessary message content.

## 3. Assets and security impact
| Asset | Examples | Primary impact if compromised |
|---|---|---|
| Mailbox identity | provider subject, verified address, tenant/user binding | cross-account access, impersonation |
| OAuth credentials | refresh/access tokens, client secret, state/PKCE material | unauthorized mailbox access |
| Message data | headers, body, labels, thread metadata | privacy breach, manipulation |
| Attachments and links | PDFs, office files, URLs, archives | malware, data exfiltration |
| AI outputs | priority, extracted tasks, summaries, drafts | false actions, missed obligations |
| Approval records | approver, exact content hash, expiry | unauthorized send |
| Send state | outbox item, idempotency key, provider receipt | duplicate or ambiguous send |
| Audit evidence | actor, action, policy decision, correlation ID | repudiation, weak incident response |
| Tenant configuration | rules, allowlists, notification targets | cross-tenant policy changes |
| Runtime and integrations | Core, provider adapter, queue, dashboard | systemic compromise |

## 4. Trust boundaries
- **TB-1 User ↔ ChatGPT/ROOM-HOP UI:** user intent and authentication must be distinguished from text displayed by the interface.
- **TB-2 ROOM-HOP Core ↔ W122 services:** Core must own authenticated identity, tenant membership, authorization, canonical state and audit contracts. W122 must not invent or bypass these contracts.
- **TB-3 W122 ↔ Gmail/provider:** provider tokens and API responses cross an external boundary; validate issuer, subject, scopes, account binding, schema and errors.
- **TB-4 Email content ↔ AI analysis:** all inbound content is hostile/untrusted data, even when it appears to come from a known sender.
- **TB-5 AI output ↔ policy/approval engine:** model output is advisory data, never an authorization token or executable command.
- **TB-6 Dashboard/notification ↔ backend:** UI is render-only; all actions require server-side authorization and state revalidation.
- **TB-7 Approval ↔ external side effect:** send execution must revalidate immutable approval, policy, mailbox state and recipient/content binding.
- **TB-8 Runtime ↔ storage/logging/backup:** secrets and message content must be segregated, encrypted and access-controlled.

## 5. Threat actors and abuse cases
- External sender or compromised correspondent crafting malicious messages.
- Phisher/spammer spoofing display names, domains or reply-to addresses.
- Malicious attachment or link author.
- Malicious or compromised OAuth app, provider token thief, or insider with excessive privileges.
- Cross-tenant attacker exploiting object IDs, search filters, cache keys or authorization gaps.
- Prompt-injection author attempting to make an AI reveal data, call tools, or send a message.
- Accidental operator misconfiguration, stale approval, replay, duplicate event or recovery bug.
- Compromised dependency, browser session, webhook endpoint or notification destination.

## 6. Threat register (STRIDE-oriented)
| ID | Threat / STRIDE | Risk before controls | Required controls | Residual concern |
|---|---|---|---|---|
| TM-01 | Forged/spoofed sender or OAuth subject (Spoofing) | HIGH | Bind provider immutable subject + verified mailbox + tenant/user + connection ID; never trust display name; validate OAuth state, PKCE, redirect URI, issuer and audience | Provider account compromise remains possible |
| TM-02 | Cross-tenant message/object access (Information disclosure, Elevation) | CRITICAL | Enforce tenant/mailbox authorization server-side on every read/write; tenant-scoped queries, cache keys, storage paths and jobs; negative isolation tests | Misconfigured privileged service |
| TM-03 | Token theft or overbroad scopes (Information disclosure, Elevation) | CRITICAL | Least scope, server-side encrypted vault, no browser/local/log exposure, rotation/revocation, short-lived access token, secret redaction | Vault/IAM compromise |
| TM-04 | Email prompt injection directs AI to reveal data or use tools (Tampering, Elevation) | CRITICAL | Treat content as data; isolate instructions from content; no tools/credentials in analysis context; policy engine outside model; output schema validation; explicit refusal for content-originated actions | Model may still misclassify or leak within permitted context |
| TM-05 | AI summary/classification invents urgency, obligation or facts (Tampering) | HIGH | Evidence-linked extraction with message/thread IDs and quoted spans; confidence/uncertainty; distinguish fact/inference; human correction; no irreversible action from model score alone | Hallucination and omission |
| TM-06 | Malicious attachment or URL executes or exfiltrates (Tampering, DoS) | HIGH | Do not auto-open/execute; MIME sniffing and size limits; quarantine/sandbox scanning before any future extraction; block active content; safe link handling; no server-side URL fetch without SSRF controls | Zero-day parser/scanner risk |
| TM-07 | Dashboard action bypasses backend policy (Elevation) | CRITICAL | UI render-only; backend re-authorizes actor, tenant, state and policy on every command; CSRF/session protections; no client-trusted role flags | Backend authorization defect |
| TM-08 | Approval replay or content/recipient substitution (Repudiation, Tampering) | CRITICAL | One-time approval nonce; immutable approval record binds mailbox, from, exact To/Cc/Bcc set, subject/body hash, attachment hashes, policy version, approver and expiry; invalidate on any edit | Compromised approver session |
| TM-09 | Duplicate send after retry or timeout (DoS / Tampering) | CRITICAL | Durable outbox, idempotency key, unique constraint, state machine; timeout becomes UNKNOWN; reconcile provider state before retry; never blind resend | Provider may not expose definitive lookup |
| TM-10 | Duplicate/out-of-order/missed push event causes state drift (Tampering) | HIGH | Treat push as wake-up only; durable per-mailbox history cursor; deduplicate; process history in order; periodic reconciliation; full resync on stale cursor | Provider retention/availability limits |
| TM-11 | Revoked/disconnected account continues processing (Elevation) | HIGH | Recheck connection state and token validity before each job/action; cancel queued work; revoke tokens; mark REAUTH_REQUIRED; no fallback credential | In-flight race at revocation boundary |
| TM-12 | Sensitive content leaks via logs, alerts or analytics (Information disclosure) | HIGH | Data minimization; redact bodies/tokens; alerts contain minimal metadata; tenant-scoped access; retention and deletion policy; audit access | Screenshots/export and downstream systems |
| TM-13 | Notification loop or spoofed action link (Spoofing, DoS) | MEDIUM | Signed short-lived action references; no authority in email notification; loop suppression; rate limits; safe links; backend revalidation | User can still be phished |
| TM-14 | Malicious header/MIME/parser payload (Tampering, DoS) | HIGH | Strict parser limits; canonicalization; reject malformed/oversized inputs; preserve raw evidence safely; fuzz parser before release | Parser/library vulnerabilities |
| TM-15 | Audit log alteration or missing actor attribution (Repudiation) | HIGH | Append-only/tamper-evident event log; server timestamp; actor/tenant/correlation ID; integrity monitoring; separate audit access; no secrets/content | Privileged infrastructure operator |
| TM-16 | Queue/job replay, stale lease or race (Tampering, DoS) | HIGH | Durable job IDs, idempotent handlers, lease/visibility timeout, bounded retry with jitter, dead-letter review, state transition guards | Operational recovery mistakes |
| TM-17 | Provider quota exhaustion or API abuse (DoS) | MEDIUM | Per-mailbox quotas, backoff with jitter, bounded concurrency, circuit breaker, budget/usage telemetry | Provider-wide outage |
| TM-18 | Cross-mailbox notification or search result mix-up (Information disclosure) | CRITICAL | Tenant/mailbox key on every query and notification; no global unscoped search; access tests with two synthetic tenants; recipient resolution from verified owner settings only | Shared cache/index configuration |
| TM-19 | Model/provider retention or training exposure (Information disclosure) | HIGH | Approved model data-processing terms; no unapproved provider; minimize/redact prompt payload; retention controls; no sensitive attachments until reviewed | Third-party processing risk |
| TM-20 | Supply-chain/dependency compromise (Tampering, Elevation) | HIGH | Pin dependencies; provenance/SBOM; vulnerability scanning; signed/reviewed builds; least-privilege runtime; staged rollout and rollback | Unknown zero-day and maintainer compromise |

Risk labels are preliminary qualitative ratings, not measured likelihoods. Ka must independently challenge severity, missing threats and control sufficiency.

## 7. Non-negotiable policy invariants
1. Initial demo: read-only + draft-only. No send/reply/forward/delete/archive/label/filter/settings mutation.
2. No send permission or send scope is requested in the initial pilot.
3. Email content cannot change policy, add trusted senders, approve a draft, change recipients or invoke tools.
4. Model-generated urgency/priority cannot authorize a side effect.
5. A draft is not an approval. A displayed button is not an authorization.
6. Any edit to approved content or recipients invalidates the approval and requires a new approval.
7. Expired, revoked, replayed, ambiguous or mismatched approval is DENY.
8. On ambiguous send timeout, state is UNKNOWN until reconciled; never retry blindly.
9. Cross-tenant access is always DENY, including search, cache, export, notification and background jobs.
10. If authorization, ownership, audit, or provider state cannot be verified, fail closed and surface BLOCKED.

## 8. Proposed control architecture
- **Identity/connection service:** bind immutable provider subject to verified mailbox, tenant, owner and connection ID; OAuth state single-use/expiring; PKCE; exact redirect URI; scopes recorded and checked.
- **Credential boundary:** encrypted server-side vault; service identity with least privilege; tokens never returned to browser, model prompt, logs or analytics; revocation and rotation procedures.
- **Ingestion boundary:** provider adapter validates response shape and account identity; history cursor is durable; push events only wake the synchronizer; deduplicate and reconcile.
- **Content safety boundary:** parse as untrusted bytes/text; separate message content from system/developer instructions; attachments disabled by default; safe rendering and link handling.
- **Analysis boundary:** model receives only authorized, minimized content; no secrets or arbitrary tool access; outputs are schema-validated and evidence-linked; model cannot call send.
- **Policy boundary:** deterministic server-side policy evaluates authenticated actor, tenant, mailbox, operation, recipient, content hash, approval and current connection state.
- **Approval/send boundary (future release only):** immutable approval + one-time nonce + durable outbox + idempotency + provider reconciliation; disabled in initial demo.
- **Audit boundary:** append-only events for connect, sync, read, analysis, draft, approval, deny, revoke and any future send attempt; redact secrets and minimize content.
- **UI boundary:** dashboard displays state and evidence; it cannot be source of truth or bypass server authorization.

## 9. Proposed data classification and retention
| Data class | Examples | Default handling proposal |
|---|---|---|
| Secrets | OAuth tokens, client secrets, signing keys | Vault only; never log or expose; rotate/revoke |
| Highly sensitive | Full body, attachments, personal/financial/legal data | Avoid persistent storage by default; encrypt if approved; short retention decision required |
| Operational metadata | provider IDs, timestamps, cursor, sync state | Tenant-scoped; retain only for product operation and audit |
| AI-derived data | summaries, priorities, task extraction, drafts | Treat as potentially sensitive; retain only with purpose and owner-approved duration |
| Audit data | actor, operation, policy result, correlation ID | Append-only, access restricted; no raw body/token |
| Notifications | subject/snippet/priority/action link | Minimal content; avoid sensitive body excerpts on lock screens |

Exact retention periods, deletion SLAs, data residency, backup expiry and model-provider processing terms are OPEN OWNER/LEGAL decisions. No duration is approved by this draft.

## 10. Security failure behavior
- Identity mismatch, missing tenant binding, missing permission or unknown role → DENY and audit.
- Expired/revoked credentials → stop mailbox jobs; REAUTH_REQUIRED; do not fall back to another account.
- Provider 401/403 → stop and surface auth/permission state; no retry loop.
- Provider 429/5xx → bounded exponential backoff with jitter; preserve cursor and job state.
- Invalid or stale history cursor → mark cursor invalid and perform controlled full reconciliation; do not silently skip.
- Duplicate event/job → idempotent no-op with audit evidence.
- Attachment parser/scanner uncertainty → quarantine or skip; never execute.
- Model timeout/invalid schema/low evidence → mark analysis incomplete; do not fabricate a summary or action.
- Approval mismatch/expiry/replay → DENY; require a new approval.
- Send timeout (future only) → UNKNOWN + reconciliation; never blind retry.
- Audit write unavailable → block security-sensitive side effects; do not proceed without required audit durability.

## 11. Negative security tests mapped to synthetic acceptance plan
The following are proposed test mappings; none has been executed.
| Threat IDs | Existing W122 tests | Expected negative result |
|---|---|---|
| TM-01, TM-03 | T001, T002, T003 | reject unbound identity, excessive scope or token exposure |
| TM-02, TM-18 | T001, T018 | tenant B cannot read/search/receive tenant A data |
| TM-04 | T004, T005 | prompt injection cannot invoke tools, reveal secrets or alter policy |
| TM-05 | T006, T007 | unsupported claims lack evidence and are marked uncertain |
| TM-06, TM-14 | T019 | unsafe attachment/parser input is isolated or rejected |
| TM-07 | T023 | direct UI/API bypass is denied server-side |
| TM-08 | T010, T011 | edited, replayed, expired or mismatched approval is denied |
| TM-09 | T012, T013 | ambiguous send remains UNKNOWN; duplicate send prevented |
| TM-10, TM-16 | T014, T015 | duplicates/reordering/stale cursor reconcile without loss |
| TM-11 | T016 | revoked connection stops work and requires reauthorization |
| TM-12, TM-13, TM-19 | T017, T018, T020 | notifications/logs/models do not leak protected content |
| TM-15 | T021 | audit tampering or missing actor is detected/blocked |
| TM-17 | T022 | quota/provider failure is bounded and recoverable |
| State integrity | T024 | invalid transitions and unsupported states are rejected |

Mapping is a design aid only. Existing T001–T024 plan remains NOT RUN; test fixtures and code do not exist yet.

## 12. Release security gates
- **R0 — Design:** threat model reviewed; owner decisions and privacy/retention unresolved items tracked.
- **R1 — Synthetic core:** tenant isolation, identity binding, policy deny, audit, idempotency and failure-state tests pass with synthetic tenants/provider.
- **R2 — Read-only Gmail pilot:** approved OAuth app/scopes, verified account binding, secret storage, consent/verification assessment, revocation and data handling reviewed. No send capability.
- **R3 — Draft-only:** draft provenance, recipient validation, content safety and audit verified. No send.
- **R4 — Controlled send:** separate Owner decision, explicit send scope, approved categories, immutable approvals, outbox/idempotency, reconciliation, incident controls and independent QE/security PASS required.
- **R5 — Anh Đức handover:** tenant onboarding, support, privacy notice, recovery, access review and operational runbook accepted.

No release gate is passed by writing this document.

## 13. Open review questions for Ka (AI-02)
1. Are the threat actors, assets and trust boundaries complete? Which high-impact boundary is missing?
2. Is the CRITICAL/HIGH/MEDIUM ranking defensible? Re-rank with rationale.
3. Can prompt injection cross from analysis to tools or approval through any indirect path?
4. Are tenant isolation and mailbox identity binding enforceable across background jobs, search, cache, notifications, exports and audit?
5. Are OAuth scope separation, token lifecycle, consent/verification and revocation requirements adequate?
6. Is the approval binding complete, including Bcc, attachments, reply threading, aliases, delegated send-as and provider-side changes?
7. Is the UNKNOWN send state/reconciliation strategy safe under provider ambiguity?
8. What controls are required for attachment extraction, URL previews, SSRF, MIME parsing and malware?
9. What privacy, retention, deletion, backup and model-provider risks are missing?
10. Which controls must be independently tested before R1, R2, R3 and R4?

## 14. Owner decisions still required
- Approve the threat model as baseline or request changes.
- Confirm tenant model and account ownership semantics.
- Approve data classification, retention, deletion and residency.
- Approve provider/model processing terms and cost ceiling.
- Decide whether attachments are excluded, metadata-only or scanned/extracted later.
- Decide notification channels and permitted content.
- Define future send categories, approvers and delegation policy (R4 only).
- Approve incident response, audit retention and recovery objectives.

## 15. Current execution truth
- Threat model: DRAFT authored by Xu; independent Ka review NOT RECEIVED.
- Synthetic test plan: 24 cases designed; fixtures NOT CREATED; test code NOT IMPLEMENTED; tests NOT RUN; independent QE NOT RUN.
- Gmail mailbox identity: NOT VERIFIED; mailbox content NOT READ.
- OAuth production path, credential vault, provider adapter, queue/outbox and deployed service contracts: NOT VERIFIED.
- G2 architecture: NOT APPROVED.
- G3 BUILD: NOT AUTHORIZED.
- Real send: NOT AUTHORIZED.
- W120/W121: no write attempted by this task.

## 16. Decision requested from independent reviewer
Ka is requested to return a written review with:
- review artifact/version and exact SHA-256 (if available);
- threat IDs accepted/rejected/modified and reasons;
- newly identified threats and control gaps;
- risk re-ranking and required negative tests;
- explicit verdict: PASS / PASS WITH CONDITIONS / FAIL / BLOCKED;
- evidence and scope limitations.

Until a verifiable review receipt and Owner decision exist, this document remains DRAFT.
