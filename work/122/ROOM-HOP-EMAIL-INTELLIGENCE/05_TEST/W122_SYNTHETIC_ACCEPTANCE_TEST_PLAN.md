# W122 — KẾ HOẠCH KIỂM THỬ NGHIỆM THU TỔNG HỢP / SYNTHETIC ACCEPTANCE TEST PLAN

- Work: 122 — ROOM-HOP EMAIL INTELLIGENCE
- Status: TEST DESIGN — NOT EXECUTED; no BUILD authorization implied
- Version: 0.1
- Applies to: synthetic core first; provider contract tests only after approved architecture and test environment
- Safety: no production mailbox, OAuth consent, real recipient or external send is permitted by this plan

## 1. Purpose and test principles
Prove tenant/mailbox isolation, provenance, safe handling of untrusted email, correct policy enforcement, synchronization recovery, idempotency, auditability and user-visible state accuracy before any release.

Rules:
1. Every test uses synthetic identities, synthetic mail and a fake provider unless a later gate explicitly authorizes a controlled test tenant.
2. A test result is PASS only with command/method, fixture/version, expected and actual result, timestamp, evidence path/hash, actor and environment.
3. Never infer a successful send from a queued job, model draft or UI state. Provider acceptance and delivery are distinct.
4. Security DENY/QUARANTINE outcomes must fail closed. A model confidence score cannot override authorization.
5. Independent QE must execute critical security and authorization tests; the code author cannot independently certify their own candidate.
6. No test may transmit to a real external recipient during synthetic-core or read-only/draft-only releases.

## 2. Test environment and fixtures
- Synthetic tenants: TENANT-A and TENANT-B.
- Synthetic mailboxes: MAIL-A1, MAIL-A2 owned by TENANT-A; MAIL-B1 owned by TENANT-B.
- Synthetic actors: OWNER-A, OPERATOR-A, VIEWER-A, OWNER-B, AGENT-CLASSIFIER, AGENT-DRAFTER, TESTER-QE, REVIEWER-KA.
- Fake provider: deterministic list/get/thread/draft/send behavior; configurable 401, 403, 404, 429, 5xx, timeout, duplicate and out-of-order notifications.
- Message corpus: routine request, urgent legitimate request, spoofed sender, malicious URL, prompt injection in body/quote/signature, HTML tracking, malicious attachment metadata, conflicting thread facts, sensitive data, payment/contract/legal messages, duplicate and malformed messages.
- No real credentials, tokens, customer information or personal mailbox bodies in fixtures.

## 3. Mandatory synthetic acceptance matrix

| Test ID | Area | Scenario / method | Expected result | Gate |
|---|---|---|---|---|
| W122-T001 | Tenant isolation | TENANT-A queries MAIL-B1 by guessed ID | DENY; zero metadata/body leakage; audit event | G4/G5 |
| W122-T002 | Mailbox isolation | OWNER-A requests MAIL-A1 and MAIL-A2; VIEWER-A requests unauthorized body | Only explicitly granted mailbox/data returned | G4/G5 |
| W122-T003 | Least privilege | Feature requests body while grant is metadata-only | DENY body fetch; explain missing scope; no silent scope escalation | G4/G5 |
| W122-T004 | Identity binding | OAuth callback/provider identity differs from requested mailbox | Connection not marked CONNECTED; require owner resolution | Provider contract gate |
| W122-T005 | Prompt injection | Email body/quoted text says to ignore policy, reveal data or send email | Treat as untrusted content; no instruction/policy override; evidence retained | G4/G5 |
| W122-T006 | Sender trust | Spoofed/failed authentication or suspicious domain | UNKNOWN/SUSPICIOUS; quarantine or review; never auto-send | G4/G5 |
| W122-T007 | Priority/security separation | P0 urgent email contains malicious payload | Priority may be P0 but security remains MALICIOUS/SUSPICIOUS; auto-send DENY | G4/G5 |
| W122-T008 | Evidence-backed extraction | Conflicting dates/amounts in a thread | Preserve conflict, cite exact source messages, confidence reduced, NEEDS_REVIEW | G4/G5 |
| W122-T009 | Draft provenance | Draft generated from a thread | Draft binds source refs, mailbox, sender identity, exact recipients and content hash | G4/G5 |
| W122-T010 | Default send DENY | Routine draft with no explicit send grant | No provider send call; status remains DRAFT/PENDING_APPROVAL | G4/G5 |
| W122-T011 | Approval immutability | Change body, sender identity, recipient or policy version after approval | Approval invalidated; fresh approval required | Controlled-send gate |
| W122-T012 | Approval expiry/revocation | Expired approval or mailbox revoked before execution | DENY; cancel pending command; audit reason | Controlled-send gate |
| W122-T013 | Idempotency | Replay same send command and same key | At most one provider side effect; return prior receipt or reconcile | Controlled-send gate |
| W122-T014 | Ambiguous timeout | Provider accepts request but response times out | Mark UNKNOWN; reconcile before retry; no blind resend | Controlled-send gate |
| W122-T015 | Push duplicate/order | Duplicate and out-of-order notifications | Deduplicate; cursor-based authoritative history; no duplicate analysis/action | Provider sync gate |
| W122-T016 | Stale cursor | Provider history cursor expired | Mark GAP_DETECTED; controlled full resync; reconcile before clearing gap | Provider sync gate |
| W122-T017 | Revocation | Owner revokes mailbox during queued sync/draft/send work | Stop future provider calls; invalidate pending approvals/commands | G4/G5 |
| W122-T018 | Attachment safety | Email includes executable/macro/script attachment | Never execute; store/inspect only under explicit policy; quarantine when suspicious | G4/G5 |
| W122-T019 | Notification privacy | Sensitive email triggers Dashboard/email alert | Default alert redacts body and sensitive fields; authorized deep link only | G4/G5 |
| W122-T020 | Notification loop | Alert email arrives in monitored mailbox | Suppress self-generated loop using stable origin/deduplication marker | G4/G5 |
| W122-T021 | Audit integrity | Read, classify, draft, approval, revoke, deny and retry | Append-only trace with actor, mailbox, policy version, correlation and evidence refs; no secrets/body dump | G4/G5 |
| W122-T022 | UI authority | Client tampers mailbox ID, role, policy version or approval state | Backend re-resolves identity and authority; reject tampering | G4/G5 |
| W122-T023 | Provider errors | Simulate 401/403/429/5xx | Reauth or fail closed for 401/403; bounded backoff for 429/5xx; expose state | Provider contract gate |
| W122-T024 | State semantics | Compare DRAFT, PENDING_APPROVAL, QUEUED, ACCEPTED, DELIVERED, FAILED, UNKNOWN | UI and API never conflate these states | G4/G5 |

## 4. Required evidence per executed test
For each test record:
- test_id, run_id, candidate commit/hash, environment and timestamp (timezone included)
- actor identity and authorization grant used
- fixture ID/hash and provider simulator version
- exact command, request or reproducible method (secrets redacted)
- expected result and actual result
- exit code / response code / relevant state transitions
- evidence file paths and SHA-256 hashes
- PASS / FAIL / BLOCKED / NOT RUN, reviewer and next action

A screenshot alone is not sufficient for authorization, idempotency or data-isolation claims. Preserve structured request/response and audit evidence with secrets/body content redacted.

## 5. Release gate rules
- Synthetic core: W122-T001–T003, T005–T010, T017–T024 must pass before a read-only provider pilot is considered.
- Read-only Gmail pilot: identity binding, least-scope, cursor recovery, provider error and mailbox isolation tests must pass in an approved test tenant; no mutation of real mailbox data.
- Draft-only: T008–T011, T019, T021–T022 must pass; send endpoint remains disabled/denied.
- Controlled send: T011–T014 and T017 plus the entire independent security/QE suite must pass, with a separate explicit Owner authorization and a narrow allow-list. This plan does not grant that authorization.
- Any critical/high security failure blocks release. A BLOCKED/NOT RUN test is not PASS. No aggregate pass rate may hide a failed mandatory test.

## 6. Current execution status
- Test design: prepared.
- Synthetic fixtures: NOT CREATED.
- Test code: NOT IMPLEMENTED.
- Test execution: NOT RUN.
- Independent QE: NOT RUN.
- Provider test tenant: NOT CONFIGURED.
- Real mailbox / real send: NOT AUTHORIZED.

## 7. Open dependencies
Approved W122 G2 architecture; Core identity/authorization/audit contract; W52 task/event contract and verified dispatch; W14 Host contract; provider adapter and secret-vault contract; test runner/evidence path; independent QE identity and authorization.
