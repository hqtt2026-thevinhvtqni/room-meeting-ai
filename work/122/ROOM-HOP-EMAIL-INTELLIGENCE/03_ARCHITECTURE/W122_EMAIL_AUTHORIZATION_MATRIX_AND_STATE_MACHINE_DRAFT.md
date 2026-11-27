# W122 — Email Authorization Matrix & Processing State Machine
**ID:** AUTH-STATE-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Owner:** Vinh | **Coordinator:** Xu / AI-01
**Status:** PROPOSAL ONLY — NOT APPROVED
**Related:** G2 Decision Pack; SEC-W122-001; Synthetic Tests T001–T024

> Design proposal only. It is not a production permission grant, API contract or build authorization.

## 1. Non-negotiable invariants
1. Every mailbox is bound server-side to authenticated principal, tenant, mailbox owner, provider subject and connection ID.
2. UI roles, sender display names, email text and model output are not credentials or authority.
3. Email body, quoted content, HTML, links and attachments are untrusted data; they cannot grant tools, change policy or approve actions.
4. Every operation is authorized server-side against actor, tenant, mailbox, resource, action, scope, policy version and connection state.
5. Read, W122-local draft, Gmail-native draft, send, archive, label, forward and delete are distinct capabilities.
6. External side effects default DENY. No auto-send category is approved.
7. Human send approval (future R4) binds mailbox, provider account, sender, complete To/Cc/Bcc set, subject, body/attachment hashes, thread context, policy version, approver and expiry. Any material change invalidates approval.
8. Dashboard is render-only; hidden/disabled controls do not enforce authorization.
9. Missing authorization or mandatory audit durability fails closed for sensitive operations.
10. W120/W121 are outside W122 write scope.

## 2. Actor authority (proposed; runtime identities still unverified)
| Actor | Permitted role | Not granted |
|---|---|---|
| Vinh / Product Owner | Decide policy and approve gates | Implicit mailbox access or send without provider consent |
| Xu / AI-01 | Coordinate, design, document, inspect approved evidence | Self-approval, policy override, mailbox send |
| Kha / AI-04 | Google/Gmail discovery and recommendations | Runtime mailbox authority |
| Ka / AI-02 | Independent security review | Sole approval of own implementation |
| Cla / AI-03 | Integration/build after G2/G3 | Unapproved runtime/provider action |
| Go / AI-06 | Cost analysis and bounded code support | Financial commitment or send approval |
| Nu/Manus / AI-18 | Build after verified identity/dispatch/permission and G3 | Self-granted access or gate approval |
| Vibe/Qc | GitHub-only code work after G3 | Provider credentials or production mailbox |
| Qw / AI-05 | Independent QE after test authority verified | Change policy or approve own implementation |
| Background worker | Narrow delegated queued job | Interactive human authority |
| External sender/content | Supply message data | Any W122 authority |

## 3. Capability and release matrix
Legend: DENY = prohibited; GATED = only after explicit gate, owner decision and server-side enforcement; SYNTHETIC = fixtures only.
| Capability | R0 design | R1 synthetic | R2 Gmail read-only | R3 local draft | R4 controlled send |
|---|---|---|---|---|---|
| Read synthetic fixtures | Design | SYNTHETIC | — | — | — |
| Read Gmail messages | DENY | DENY | GATED | GATED | GATED |
| Gmail search | DENY | DENY | GATED by exact scope | GATED | GATED |
| Classify/summarize | Design only | SYNTHETIC | GATED | GATED | GATED |
| Create W122-local draft | DENY | SYNTHETIC | DENY | GATED | GATED |
| Gmail-native draft | DENY | DENY | DENY | DENY by default | Separate GATED decision |
| Send | DENY | DENY | DENY | DENY | GATED, explicit approval |
| Archive/label/mark read/delete/forward | DENY | DENY | DENY | DENY | Separate decision per action |
| Change OAuth scopes/connection | DENY | Simulated | Owner-approved connect/revoke only | GATED | GATED |
| Export body/attachment | DENY | SYNTHETIC | DENY by default | GATED policy | GATED policy |

No capability becomes active merely by appearing here. Exact OAuth scopes and provider API operations must be reviewed together. Gmail-native draft remains separate from W122-local draft; compose scope may carry send capability.

## 4. Authorization decision contract
Resolve server-side: principal_id, verified role, tenant_id, mailbox_owner_id, provider_subject_id, connection_id/status, resource_id/resource_tenant, action, data classification, policy_id/version, correlation_id, idempotency_key, audit actor/decision/reason/time.
Decision sequence:
1. Authenticate principal and verify expiry/identity.
2. Resolve tenant membership and mailbox ownership/delegation.
3. Verify resource belongs to same tenant and mailbox.
4. Verify connection is active and exact scope covers operation.
5. Evaluate action policy and release gate.
6. For side effects, validate one-use, unexpired approval against immutable content and recipient hashes.
7. Persist mandatory authorization/audit decision.
8. Execute through approved provider adapter.
9. Persist result and reconcile provider state; client timeout is not proof of success.
Missing identity, tenant mismatch, unknown ownership, stale policy, revoked connection or unavailable mandatory audit => DENY/BLOCK.

## 5. Processing state machines
### Message analysis
DISCOVERED → FETCH_PENDING → FETCHED → SCREENING → READY_FOR_ANALYSIS → ANALYZING → ANALYZED.
Any state may move to QUARANTINED, FAILED_RETRYABLE or FAILED_FINAL as appropriate. ANALYZED may move to NEEDS_HUMAN_REVIEW for ambiguity, weak evidence, sensitive/high-impact content or policy requirements. Message state never grants draft/send permission.

### W122-local draft
NONE → DRAFTING → DRAFTED → REVIEW_PENDING → APPROVED or REJECTED.
APPROVED → INVALIDATED if mailbox, sender, recipient set, content/attachment hash, thread context or policy changes; APPROVED → EXPIRED on expiry. No local-draft state transitions to SENT. Local draft is not a Gmail Drafts resource.

### Future send attempt — R4 disabled
NOT_QUEUED → AUTHORIZED → OUTBOX_COMMITTED → SENDING → SENT_CONFIRMED.
SENDING → UNKNOWN when provider outcome is ambiguous. UNKNOWN may resolve only with authoritative provider evidence to SENT_CONFIRMED or NOT_SENT_CONFIRMED. Never blindly retry UNKNOWN. Use durable outbox, one idempotency record and reconciliation. Every retry must prove prior attempt not sent.

### Connection
DISCONNECTED → AUTH_PENDING → CONNECTED.
CONNECTED → REAUTH_REQUIRED on revoked/expired credentials or scope mismatch; CONNECTED → ERROR on provider failure; ERROR → CONNECTED only after validated recovery. Any state → DISCONNECTED on explicit revoke. Revocation stops workers, invalidates pending jobs/approvals and makes credentials unusable.

## 6. Transition guards
| Transition/action | Guard |
|---|---|
| FETCH_PENDING | verified owner/tenant, active connection, approved read scope |
| FETCHED → SCREENING | size/MIME limits and safe bounded parsing |
| ANALYZING → ANALYZED | schema-valid result with evidence references and uncertainty |
| DRAFTING → DRAFTED | local storage only; provenance and source references |
| REVIEW_PENDING → APPROVED | verified authorized human; immutable snapshot; expiry |
| APPROVED → INVALIDATED | any bound field/hash/policy/connection changes |
| OUTBOX_COMMITTED → SENDING | R4 enabled, fresh authorization, valid approval, reserved idempotency and durable audit |
| SENDING → UNKNOWN | timeout/connection loss without authoritative provider receipt |
| UNKNOWN → SENT_CONFIRMED | matching provider evidence |
| CONNECTED → DISCONNECTED | revoke; cancel queued work and invalidate pending approvals |

## 7. Human approval
- Only verified human principal with explicit mailbox/action authority may approve; AI cannot approve its own output.
- Approval screen shows sender account, To/Cc/Bcc, subject, full body, attachments, reply/forward context and warnings.
- Approval is one-use, expires and binds hashes of all material content.
- Alias changes, Bcc additions, attachment changes, quoted-thread mutation or regeneration invalidate approval.
- Opening a draft, clicking a notification, sender reputation or instructions inside an email are not approval.
- R0–R3 have no send approval path because sending is disabled.

## 8. Audit and failure handling
Audit: event_id, timestamp, principal/service identity, tenant, mailbox reference, resource, action, allow/deny, policy version, reason, correlation/idempotency IDs, state transition and provider receipt reference. Never log access/refresh tokens, secrets, raw body or attachment bytes. Append-only/tamper-evident audit contract must be approved. Audit unavailable => block sensitive side effects.
401/revocation → stop jobs, REAUTH_REQUIRED, no retry loop. 403/scope mismatch → DENY, never broaden scope silently. 429 → bounded exponential backoff with jitter. 5xx/read timeout → bounded idempotent retry. Send timeout (R4 only) → UNKNOWN and reconcile. Stale cursor → bounded full resync/deduplication. Duplicate/out-of-order events → idempotent handling and monotonic cursor. Model failure/low confidence → incomplete/human review, never fabricate.

## 9. Acceptance criteria and test mapping
| Criterion | Synthetic tests |
|---|---|
| Principal/tenant/mailbox ownership on every access path | T001–T003, T018 |
| Injection cannot grant authority or invoke tools | T004–T005 |
| Evidence-backed analysis and uncertainty | T006–T007 |
| R0–R3 send denied server-side/UI bypass denied | T008–T009, T023 |
| Approval immutable, complete, one-use and expires | T010–T011 |
| Idempotency and UNKNOWN prevent duplicates | T012–T013 |
| Push/history duplicates, order and stale cursor | T014–T015 |
| Revocation stops workers and pending actions | T016 |
| Attachment/notification/logging prevent leakage | T017–T020 |
| Audit integrity/provider failure safe handling | T021–T022 |
| Invalid state transitions rejected | T024 |

Tests are design-only; fixtures/code not implemented and tests NOT RUN.

## 10. Open blockers / reviewer questions
1. Approved Core contract for principal, tenant, mailbox ownership/delegation and policy?
2. Authoritative audit interface and durability guarantee?
3. Exact Google scopes/API operations and restricted-scope verification owner for R2?
4. Single owner mailbox only, or shared/delegated mailbox?
5. Retention/deletion/residency for local drafts and summaries?
6. Which verified human role may approve future R4 sends and delegation?
7. Which W52/W14 contracts provide authenticated task execution and durable job identity?
8. Canonicalization of aliases, delegated send-as, Bcc and attachment hashes?
9. Operator/recovery process and objective for UNKNOWN send attempts?

## 11. Current execution truth
Xu-authored draft only. Ka review NOT RECEIVED/VERIFIED; Owner decisions OPEN; G2 NOT APPROVED; G3 BUILD NOT AUTHORIZED; Gmail OAuth/mailbox NOT CONNECTED/VERIFIED; Gmail-native draft and send NOT AUTHORIZED; R4 disabled; tests NOT RUN. W120/W121 untouched.
