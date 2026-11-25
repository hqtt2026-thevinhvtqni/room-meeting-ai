# KẾ HOẠCH TRIỂN KHAI W122 — ROOM-HOP EMAIL INTELLIGENCE
## DOC-001 / Canonical delivery plan — revision 1
- Work ID: 122
- Product owner: Vinh
- Intended end user / beneficiary: Anh Đức
- Coordinator: Xu (ROOM-HOP identity: xu)
- Date: 2026-11-25 (UTC+07:00)
- Lifecycle standard: Work 70
- Status: PROPOSED — DISCOVER / ARCHITECTURE INTAKE; G3 BUILD NOT AUTHORIZED
- Scope boundary: W120 and W121 remain separate and untouched; W122 does not depend on CUA.

## 1. Product outcome
Deliver a secure, practical Mail Center for Anh Đức to manage multiple mailboxes from one place. It should reduce time spent checking and sorting email, surface important messages and required actions, prepare reliable replies, and automate only low-risk responses explicitly permitted by mailbox-specific policy.

Success is not merely an AI summary. The product must reliably show which mailbox received the message, who sent it, what it concerns, why it matters, whether action is needed, what the next action is, and whether a reply is a draft, awaiting approval, queued, accepted by provider, or sent. Every decision must be traceable.

## 2. Confirmed initial requirements
1. Connect multiple primary mailboxes.
2. Monitor incoming mail and classify important messages.
3. Identify messages requiring action and alert the user.
4. Summarize threads and prepare suggested replies.
5. Notify through Dashboard and email alerts.
6. Automatically send to partners only when the exact action is within a policy approved by the Owner for that mailbox.
7. Sensitive, ambiguous, high-impact, or out-of-authority matters must stop for human approval.
8. Do not invent facts, deadlines, prices, promises, or commitments.
9. W120/W121 are out of scope and must not be changed or made dependencies.

## 3. Product operating model
### 3.1 Inbox workflow
RECEIVE → SYNC → NORMALIZE → SECURITY SCREEN → CLASSIFY → ACTION QUEUE → SUMMARIZE → DRAFT (when useful) → APPROVAL OR POLICY CHECK → SEND (only if authorized) → AUDIT.

### 3.2 Priority labels
- P0 Urgent: time-critical or material operational interruption.
- P1 Important: material business/partner/customer matter.
- P2 Requires response: explicit question, request, or task.
- P3 Informational: useful but no immediate action identified.
- P4 Low relevance / likely spam: priority is not a security verdict.

Security is a separate axis: TRUSTED / UNKNOWN / SUSPICIOUS / MALICIOUS / QUARANTINED. A high-priority email may still be malicious. Suspicious or malicious content is never eligible for automatic reply.

### 3.3 Initial automation levels
- Level 0 — Read-only: connect, sync, classify, summarize, alert.
- Level 1 — Draft-only: prepare replies; user edits and sends manually.
- Level 2 — Narrow approved auto-send: only pre-authorized low-risk categories, known recipients/partner allow-list, approved templates/rules, per-mailbox opt-in, and fresh policy check at send time.
- Level 3 — Expanded automation: not part of initial release; requires separate evidence and Owner approval.

Default state is Level 0/1. Autonomous sending is DENY until explicitly enabled.

## 4. Work packages and deliverables
| WP | Work package | Main outputs | Exit criteria |
|---|---|---|---|
| WP-01 | Product discovery & user workflow | Anh Đức user journey, mailbox inventory template, user stories, priority/action taxonomy, acceptance criteria | Scope and workflow baselined; unknowns explicit |
| WP-02 | Provider selection & feasibility | Gmail/Google, Outlook/M365, IMAP capability matrix; OAuth/scope, quota, push/delta, limitations | First provider selected from evidence; no credential or consent change |
| WP-03 | ROOM-HOP integration contracts | Verified Core authority, Gateway, Event Listener, Agent Runtime, Dashboard and dispatch contracts | Each integration mapped to approved readable contract; no guessed endpoints |
| WP-04 | Security, privacy & threat model | Data-flow, threat model, mailbox isolation, token lifecycle, retention/deletion, attachment and prompt-injection controls | Ka independent review closed or risks accepted by Owner |
| WP-05 | Architecture & ADR | Provider-neutral architecture, event/message schemas, sync state machine, send-policy state machine, notification model | One official architecture minutes/ADR approved by Owner |
| WP-06 | Build authorization & implementation design | Build backlog, module boundaries, cost budget, test strategy, rollout/rollback plan | G3 explicitly authorized; no implementation before this gate |
| WP-07 | Mailbox connection & sync | Provider adapter, OAuth lifecycle, cursor/watch/delta, dedupe, retry, reconnect/revoke | Test mailbox sync repeatable; mailbox isolation proven |
| WP-08 | Email intelligence | Classification, security signals, thread summary, action/deadline extraction, evidence-linked draft | Safety and accuracy test set passes agreed thresholds; low confidence escalates |
| WP-09 | Mail Center Dashboard & alerts | Inbox overview, Priority, Action Required, Drafts, Pending Approval, AI Sent, Mailbox Settings, Audit/Errors | UI reads canonical live state; no mock data represented as live |
| WP-10 | Approval & controlled send | Per-mailbox policy, partner allow-list, approval binding, send-time recheck, outbox/idempotency, provider receipt | Deny/allow/approval matrix passes; no send on stale/changed approval |
| WP-11 | Independent verification | Unit/contract/integration/security/E2E tests, fault injection, QE report | Independent reviewer evidence and journal read-back complete |
| WP-12 | Pilot, handoff & operations | Anh Đức onboarding, user guide, runbook, monitoring, revoke, backup/recovery, support process | Owner accepts pilot; rollback/revoke tested; release decision recorded |

## 5. Detailed phase gates
### G0 — Intake baseline
Required: product outcome, owner, intended user, scope boundary, related Works, risk level, initial requirements.
Current evidence: Work 122 exists in Sandbox and GitHub main mirror was previously recorded in J002/J003; intended end user Anh Đức is now explicitly recorded in this plan.
Remaining: original source email/content must be preserved in 01_ORIGINAL and reconciled verbatim; user-specific workflow and mailbox/provider inventory are not yet confirmed.
Exit: requirements baseline and source provenance complete.

### G1 — Discovery
Required: provider capability/scope matrix; actual ROOM-HOP service/adapter contracts and verified deployment boundary; data classification/privacy/retention/deletion; cost/quota assumptions with sources; Kha discovery and Ka security review findings or explicit BLOCKED status.
Current: Gmail official API discovery and W05 reuse boundary are documented; W05 is not a Gmail connector. Core/Gateway/Event/Agent production contracts and agent dispatch are not verified. Kha/Ka briefs are prepared but NOT DISPATCHED.
Exit: evidence sufficient for architecture; unresolved risks and assumptions visible.

### G2 — Architecture decision
Required: provider-neutral adapter; mailbox identity/token lifecycle; sync/event/cursor/recovery; message/thread/attachment metadata and provenance; AI classification/confidence; approval/send state machine; audit/retention/deletion/incident response; Dashboard/notification contract; cost model; deployment topology; independent security review; one canonical official minutes/ADR.
Exit: Owner approves architecture. AI consensus alone is not approval.

### G3 — Build authorization
Required: approved G2 minutes/ADR, scoped backlog, named execution owner, verified runtime permissions, test environment, cost ceiling, security controls and rollback plan.
Exit: explicit Owner authorization. Until then, no production code implementation, OAuth consent, secret creation, mailbox connection or paid commitment.

### G4 — Verification
Test in synthetic data and provider test tenant first:
- Mailbox A/B isolation and wrong-mailbox prevention.
- Duplicate, delayed, out-of-order and dropped event handling.
- Cursor expiry and full-resync recovery.
- OAuth expiry, revoke and reconnect.
- Malicious sender, phishing, prompt injection, malicious links/attachments.
- Hallucinated facts/deadlines/commitments and low-confidence escalation.
- Wrong recipient, changed draft, changed recipients, stale approval.
- Duplicate send, retry, timeout ambiguity and provider rejection.
- Notification loops, rate limits, quota exhaustion and service outage.
No real external send during initial verification. A controlled test sink requires separate explicit authorization.

### G5 — Acceptance
Required: functional acceptance against user stories; security/privacy review closure; independent QE report with reproducible evidence; Dashboard provenance and audit completeness; operational runbook, recovery/revoke drill and known limitations; Anh Đức pilot feedback and Owner acceptance.
Exit: PASS only when evidence exists; otherwise FAIL/BLOCKED with remediation.

### G6 — Release & operate
Staged rollout: (1) read-only pilot; (2) draft-only pilot; (3) narrow auto-send for one approved mailbox/category/partner set; (4) expand only after review of operating evidence and explicit approval.
Controls: feature flags, per-mailbox kill switch, global send kill switch, token revoke, audit export, rollback and incident response.

## 6. Initial acceptance criteria
- Every email is associated with exactly one authorized mailbox identity and provider reference.
- No cross-mailbox message, draft, token or recipient leakage.
- Priority and security are separate and visible.
- Every AI summary/draft traces to source message/thread evidence.
- Deadline fields remain unknown unless a source explicitly states them.
- Draft is never shown as sent; queued is never shown as delivered.
- Suspicious/malicious/unknown-risk content cannot trigger auto-send.
- Sensitive/high-impact categories require human approval.
- Auto-send is DENY by default and requires mailbox-specific allow policy.
- Approval is bound to exact draft content/hash, recipients, mailbox, policy version and expiry; any change invalidates it.
- Send-time policy is re-evaluated; retries do not create duplicate sends.
- Ambiguous provider outcome is surfaced as UNKNOWN_PENDING_RECONCILIATION, not falsely reported as success/failure.
- Every connection, sync, classification, draft, approval, send, error, retry and revoke action is audited.
- User can disable sending and revoke mailbox access without deleting unrelated mailbox data.
- Dashboard reflects canonical live state and exposes source/time/status.

## 7. Staffing and responsibility
- Xu: product/technical coordination, architecture, evidence journal, integration trace, handoff.
- Vinh: Product Owner and final gate authority.
- Anh Đức: intended end user and pilot feedback provider; no account access assumed.
- Kha: initial Gmail/Google discovery only.
- Ka: independent security and architecture review.
- Cla: CTO integration/code/debug after G2/G3.
- Go: cost analysis and code support; QE/review only for work not authored by Go (conflict-of-interest separation).
- Manus (AI-18): candidate autonomous end-to-end builder after identity, task dispatch, permissions and audit are verified; one outcome-based assignment, not fragmented ACKs.
- Vibe: GitHub-only code support after authorization; no direct Sandbox/runtime changes.
- Qw: HQTT review role; not default QE.
- Qc/Vi/Co: only assigned within verified roster and permission boundaries.
No agent may be marked assigned, dispatched or accepted without a verifiable dispatch/receipt record.

## 8. Cost and resource controls
Prefer existing ROOM-HOP infrastructure and narrow provider scopes. No paid cloud/API/hosting commitment, production app registration or billing activation without Owner approval. Estimate per-mailbox sync volume, message-processing/model tokens, notification volume, storage/retention and monitoring before G2. Enforce provider quotas, model budgets, retry caps and per-mailbox rate limits. Record actual usage/costs after implementation is authorized.

## 9. Current blockers and evidence gaps
1. Original source email/body has not been read back from W122/01_ORIGINAL in the current inspection; requirements above are based on prior conversation context, not a verbatim source-mail copy.
2. Approved production contracts for Core/Gateway/Event Listener/Agent Runtime have not been verified in inspected artifacts.
3. W52 task dispatch mechanism is not exposed in the current Build MCP tool inventory; Kha/Ka briefs are NOT DISPATCHED.
4. Provider order, test mailbox/tenant, OAuth app ownership, retention period and Anh Đức workflow inventory are not confirmed.
5. No approved G2 architecture or G3 build authorization.
6. No code, OAuth consent, credential operation, real mailbox connection or external send has been performed.

## 10. Immediate next actions (Xu)
1. Locate and preserve the original source email verbatim in 01_ORIGINAL; if unavailable, record its absence and do not reconstruct it as a quote.
2. Inspect only new/authoritative sources for ROOM-HOP production contracts; avoid repeating prior reads without new evidence.
3. Verify the approved task-dispatch route; dispatch Kha and Ka only when an authorized mechanism is available, and record receipts.
4. Complete provider comparison for Gmail vs Outlook/M365 vs IMAP and recommend a first provider from evidence.
5. Prepare G1 evidence/gap matrix and consolidate real reviewer findings into the one canonical minutes/ADR.
6. Present G2 architecture decision and G3 scope/cost/test plan to Vinh for approval.
7. After G3, execute build, independent verification, Anh Đức pilot and handoff.

## 11. Current status
DISCOVER / ARCHITECTURE INTAKE. G0/G1 are not yet closed. G2 not approved. G3 BUILD NOT AUTHORIZED. REAL SEND NOT AUTHORIZED.


## 12. Demo mailbox — owner-provided account
- Initial demo mailbox requested by Vinh: `thevinhvtqni@gmail.com`.
- Provider for first demo: Gmail / Google.
- Intended use: controlled demonstration of inbox ingestion, classification, prioritization, thread summary, action extraction, draft suggestion and Dashboard workflow.
- Initial permission level: READ-ONLY + DRAFT-ONLY. No send, reply, forward, delete, archive, label mutation, filter creation, or settings change during the first demo.
- Data minimization: start with a small, explicitly selected sample or a narrow date/query window; avoid bulk export and avoid unrelated personal content. Redact sensitive data in reports and test fixtures.
- Account identity verification: Gmail connector `get_profile` was invoked to confirm the authenticated account, but returned an empty result. Therefore the connected identity is NOT VERIFIED to match `thevinhvtqni@gmail.com`; do not read mailbox content until identity is confirmed.
- OAuth/application connection for the W122 product itself remains NOT CONFIGURED. A ChatGPT Gmail connector session, if available, is not evidence that W122's own OAuth integration is implemented.
- Demo success criteria: show real message metadata/content only after mailbox identity is verified; trace each AI classification and summary to source message; create draft suggestions only if explicitly requested; demonstrate that no send action is possible in read-only/demo mode.
