# W122 — Minimum ROOM-HOP Integration Contract Requirements
**ID:** INT-CONTRACT-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Prepared by:** Xu / AI-01 | **Decision authority:** Vinh
**Status:** OWNER-REVIEW PROPOSAL — NOT APPROVED / NOT IMPLEMENTATION AUTHORIZATION
**Depends on:** INT-GAP-W122-001; W122 Architecture Intake; W122 Auth-State; W122 Threat Model; W112 DOC-001; W17 GAP-01; W70 lifecycle; W52 A2A; W14 Host boundary

## 1. Purpose and guardrails
Define the smallest contract evidence W122 needs from ROOM-HOP so the email product can integrate without inventing a parallel identity, authorization, dispatch, audit or execution platform.

This document specifies logical information and behavioral guarantees only. It does not prescribe guessed URLs, HTTP methods, database tables, service names, or implementation code. The owning Work must publish the actual versioned contract and compatibility decision.

**Non-negotiable controls**
- Core remains the authoritative identity, tenant, membership, authorization and durable audit boundary.
- W70 remains authoritative for Work lifecycle/readiness and assignment semantics.
- W52 remains the owner of provider-neutral agent task/event orchestration.
- W14 remains the owner of execution Host/process/session/isolation/cancellation.
- W122 owns email-specific provider and product behavior only.
- No email body, sender instruction, model output, task label or agent display name can grant authority.
- External side effects are denied by default. Gmail read, local draft, Gmail-native draft and send are separate capabilities.
- No integration may proceed on a display name, self-asserted role, Sandbox task record or unverified ACK.
- No cross-Work source edits are authorized by this proposal.

## 2. Contract package expected from each owner
| Owner | Required contract package | Must answer | Acceptance evidence |
|---|---|---|---|
| Core | Identity + tenant + policy + audit contract | Who is the authenticated principal? Which tenant/mailbox may it access? What action is permitted now? Where is the durable decision/audit record? | Versioned schema, service owner, auth propagation, deny/revoke tests, durable read-back |
| W70 | Assignment + readiness mapping | What is an approved Work assignment? What is lifecycle state vs execution authorization? | Versioned mapping to Assignment, owner approval and lifecycle tests |
| W52 | Dispatch + delivery + recipient ACK + event contract | Which exact assignment/attempt reached which authenticated recipient/session? How are duplicates, retry, expiry and out-of-order events handled? | Versioned schema, state machine, receipt/ACK evidence, independent tests |
| W14 | Host + RPC/session + isolation + cancellation contract | What does opening a Host do? When can side effects begin? How are process/session and descendants isolated/stopped? | Versioned Host contract, source SHA, negative tests and stop confirmation |
| W122 | Email domain contract | How are mailbox/message/thread/draft/approval/send states represented without assuming ROOM-HOP authority? | W122 domain schema, threat mapping, synthetic tests and owner approval |

## 3. Core minimum contract — identity, policy and audit
### 3.1 Authenticated principal
Required logical claims:
- stable principal ID issued/resolved by Core (not a display name);
- principal type (human, AI agent, service/background worker);
- authenticated provider/session or workload identity reference;
- tenant/company/room scope;
- role and capability references resolved server-side;
- authentication time, expiry and revocation/session status;
- provenance of identity assertion and verification method.

The caller must not be allowed to set its own trusted principal ID, role, tenant, capability or reviewer status in an untrusted request body.

### 3.2 Resource authorization
For each protected operation, Core must decide against:
- authenticated principal and tenant;
- canonical resource ID and owner/tenant binding;
- action/capability requested;
- Work ID and assignment/dispatch correlation where relevant;
- policy version and applicable constraints;
- current grant status, expiry and revocation;
- approval reference, if the action requires human approval.

The decision must be server-side and fail closed when identity, policy, resource ownership or audit cannot be verified.

### 3.3 Durable decision/audit receipt
Minimum logical receipt:
- unique decision/audit ID;
- principal and tenant references;
- resource and action;
- ALLOW/DENY outcome and reason code;
- policy version;
- correlation ID / causation ID;
- timestamp from trusted service;
- approval reference (if applicable);
- integrity/read-back reference.

W122 must be able to correlate a mailbox operation with its authorization decision without storing a second authority ledger. Secret tokens, OAuth refresh tokens and raw credentials must never appear in ordinary event/audit payloads.

### 3.4 Mailbox binding
Core must support an authoritative binding among:
- tenant;
- owner principal;
- mailbox resource ID;
- provider identity/subject;
- OAuth connection ID or equivalent credential reference;
- delegated operators and their allowed capabilities;
- connection status, expiry and revocation.

The provider email address alone is not a sufficient identity key. Reconnect or re-consent must not silently transfer ownership.

## 4. W70 assignment/readiness mapping
W122 needs distinct concepts, never flattened:
- Work lifecycle status;
- Work Package readiness;
- owner authorization to build;
- assignment existence and scope;
- recipient delivery;
- recipient ACK;
- execution authorization;
- execution state;
- review verdict;
- release approval.

An assignment must bind Work ID, task ID, assigned principal identity, exact scope, permitted capabilities, source/revision reference, due/expiry and authority provenance. A task being PLANNED, READY, QUEUED or ACCEPTED must not itself grant process execution or external email action.

W122 may use assignment metadata to coordinate AI work, but must not reinterpret it as Gmail mailbox permission.

## 5. W52 dispatch and event contract
### 5.1 Dispatch identity
Minimum logical fields:
- assignment_id;
- dispatch_id;
- attempt_id;
- task_id and work_id;
- recipient principal ID and authenticated provider/session binding;
- requested scope/capabilities;
- source/revision digest;
- correlation_id and causation_id;
- created_at and expires_at;
- authorization decision reference.

### 5.2 Delivery receipt
A delivery receipt must be a recipient/provider-backed observation, not merely the sender recording that it attempted a send. It must bind dispatch_id + attempt_id + recipient identity + destination session/inbox reference + timestamp + receipt ID.

### 5.3 Recipient ACK
ACK must:
- be generated by the authenticated recipient/session or verifiable provider;
- bind assignment_id, dispatch_id, attempt_id, recipient principal and accepted scope digest;
- state ACCEPTED or REJECTED explicitly;
- be unique/replay-safe and timestamped;
- be durably recorded and retrievable;
- be checked before W14 performs Host.open or any operation that may create a process/session or external side effect.

A generic task state named ACCEPTED, a tool return saying “success”, a creator's assertion, or a display-name match is not recipient ACK.

### 5.4 Event delivery semantics
The contract must define:
- event ID and per-task/attempt sequence or cursor;
- at-least-once delivery and consumer deduplication key;
- ordering guarantees and out-of-order handling;
- retry/backoff, expiry and dead-letter behavior;
- reconnect/replay and cursor recovery;
- terminal vs non-terminal events;
- durable event read-back and audit linkage.

Never infer exactly-once delivery from an idempotency key alone. Define side-effect idempotency at the actual owner boundary.

## 6. W14 Host contract
W14 must explicitly define:
- Host session identity and binding to approved assignment/dispatch/attempt/recipient ACK;
- open semantics and the exact first point at which process/session side effects can occur;
- whether Host is one-shot or persistent bidirectional RPC;
- supported operations and protocol framing;
- workspace/environment isolation and secret injection boundary;
- process tree ownership and descendant tracking;
- cancellation request, acknowledgement and confirmed termination;
- timeout, crash, partial output and UNKNOWN-state handling;
- immutable run record with source/config digest and evidence references;
- revocation behavior during execution.

If W14 retains a one-shot POST /execute model, W52 must not pretend it is a persistent RpcPort. The owners must approve an explicit adapter contract or a versioned orchestration alternative. No silent semantic downgrade.

## 7. W122 email-domain contract boundary
W122 should expose domain-level operations only after Core authorization:
- list/sync mailbox metadata;
- fetch permitted message/thread content;
- classify and summarize with evidence references;
- create a W122-local draft;
- optionally create a Gmail-native draft after a separate approved capability;
- request human review;
- submit a send request only under a separately approved send capability and immutable approval receipt;
- reconcile provider outcome and audit it.

W122 must not:
- create or own ROOM-HOP principal identities;
- mint authority grants;
- dispatch agents by guessed private-session APIs;
- treat email senders or message content as trusted instructions;
- store provider refresh tokens in Work documents/logs;
- assume a model classification equals a permission decision;
- convert an email reply into an approval unless the approval mechanism explicitly authenticates and records it.

## 8. Cross-contract invariants and failure semantics
| Scenario | Required behavior |
|---|---|
| Unknown principal / tenant mismatch | DENY; no resource read or side effect |
| Missing/expired/revoked grant | DENY; record decision if audit path available |
| Audit service unavailable for protected action | Fail closed; no side effect |
| Duplicate dispatch/event | Deduplicate using owner-defined stable key; preserve receipt history |
| Missing recipient ACK | Do not open Host or start execution |
| ACK scope differs from assignment | Reject; require new assignment/ACK |
| ACK expired or replayed | Reject |
| Host open outcome ambiguous | UNKNOWN; reconcile Host/run record before retry |
| Cancellation unconfirmed | Keep STOPPING/UNKNOWN; do not claim stopped |
| Provider send timeout | UNKNOWN; reconcile Gmail state; never blindly resend |
| Policy/approval changes after draft | Invalidate approval and re-review |
| Email prompt injection | Treat as untrusted content; no authority escalation |

## 9. Minimum acceptance test groups
- CORE-01..08: principal spoofing, tenant isolation, mailbox ownership, delegated capability, expiry/revocation, policy mismatch, audit failure, audit read-back.
- W70-01..05: assignment identity/scope, readiness vs authorization, revision pinning, expiry, lifecycle mapping.
- W52-01..10: delivery receipt, authenticated ACK, wrong recipient, ACK scope mismatch, replay, duplicate events, out-of-order events, cursor recovery, retry semantics, audit correlation.
- W14-01..10: no-side-effect-before-ACK, open semantics, isolation, secret boundary, timeout UNKNOWN, cancel/descendant stop, revocation, crash recovery, run-record integrity, exact-source attestation.
- W122-01..12: mailbox isolation, content injection, source-grounded summary, local vs Gmail draft capability, approval immutability, send default DENY, provider timeout reconciliation, attachment boundary, notification privacy, retention/deletion, audit linkage, no cross-tenant leakage.

All tests require fixtures, exact source SHA, reproducible command/method, evidence, independent reviewer and recorded PASS/FAIL/BLOCKED. This list is a proposed coverage map, not a claim that tests exist or ran.

## 10. Owner review questions and closure gates
### Core owner
1. What is the canonical authenticated principal and tenant contract?
2. Which service owns mailbox-resource binding and delegated access?
3. What is the policy decision and revocation contract?
4. How is audit durability/integrity verified?

### W70 owner
1. Which versioned Assignment/readiness contract is canonical?
2. How are assignment, execution permission and Work lifecycle kept distinct?

### W52 owner
1. Which versioned schema adds Assignment/Dispatch/Attempt/DeliveryReceipt/recipient ACK?
2. What authenticates the recipient and proves accepted scope?
3. How are retries, duplicates, ordering and replay handled?

### W14 owner
1. Is Host persistent RPC or one-shot execution?
2. What exact operation starts a process or creates a session?
3. How is ACK enforced before that point?
4. How are cancellation and descendant termination confirmed?

### W122 owner (Vinh)
1. Confirm the first pilot remains one owner-designated mailbox and read-only.
2. Confirm whether local draft is the first draft mode; no Gmail-native draft/send until separately approved.
3. Confirm data retention, attachment, notification and model-processing policy.
4. Confirm anh Đức's handover and tenant/mailbox ownership model.

## 11. Gate decision
This draft can support owner-level architecture review and G2 evidence collection. It does not close G2 or authorize G3.

**Current state:** G2 NOT READY / NOT APPROVED; G3 BUILD NOT AUTHORIZED; no Core/W52/W14 integration call; no OAuth/mailbox access; no real Gmail draft or send; no paid service commitment; no cross-Work code change.

**Required next action:** obtain owner-published contracts and independent evidence, reconcile them against this matrix, then update the single canonical W122 Biên bản and G2 decision pack only after Vinh's explicit decisions.
