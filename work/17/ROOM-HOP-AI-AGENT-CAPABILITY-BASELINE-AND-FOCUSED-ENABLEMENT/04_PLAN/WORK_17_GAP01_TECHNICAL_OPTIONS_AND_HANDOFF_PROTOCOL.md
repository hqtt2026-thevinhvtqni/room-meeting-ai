# WORK 17 — GAP-01 Technical Options & Session Handoff Protocol Proposal

- Date: 2026-11-19 (UTC+7) · Owner/authority: Vinh · Coordinator: Xu / AI-01
- Status: PROPOSAL ONLY — READ / TRACE; NOT APPROVED FOR BUILD OR LIVE DISPATCH
- Scope: GAP-01 Assignment authority, delivery path, receipt, identity binding and ACK correlation.
- Inputs: DOC-044; W70 DOC-064/065/066; W17 GAP-01 reconciliation; Journal Entries 016–019.

## 1. Recommendation

Do not implement a new dispatcher, API, database, queue or parallel Assignment Registry.

1. Resolve the existing authoritative owner and persistence boundary first. W70 is the target Work/WP/Gate governance authority; that does not prove W70 documents or MeetingService own runtime Assignment state.
2. Keep the existing AI conversation by evaluating SESSION_HANDOFF first. It is user-mediated, not automatic dispatch. Reuse DOC-044 as the assignment source/template and DOC-065 as the logical event contract; do not fork them.
3. Separate transport state from assignment state. Packet creation is not delivery; paste is not provider receipt; a reply is not cryptographic identity proof.
4. Do not store operational truth in Sandbox or Meeting transcript. Until an existing Core-owned persistence service is identified and approved, remain document-only.
5. Require independent security and technical review before any BUILD proposal. This document is not a dispatch request or live-trial authorization.

## 2. Evidence baseline and limits

- DOC-064 blob `0cd5cc7108310a93c98a289cc9a27f89b951b5dc`: target hybrid architecture; implementation not authorized.
- DOC-065 blob `a18db833f7286400ca702b850f072df6d834c4f1`: provider-neutral contract proposal; route names deferred until Core owner mapping.
- DOC-066 blob `8278b5199b5802ac915d412df499a181dd37342a`: implementation unauthorized, tests NOT RUN; Session Handoff MVP is future work, not an existing capability.
- Entry 017: exposed 8030 tools do not include private-session dispatch or provider receipt/ACK retrieval.
- Entry 018: Browser Agent Adapter Meeting marker/read-back proves artifact recording in Meeting, not provider delivery or AI ACK.
- Entry 019: inspected Core HTTP composition exposes Meeting/identity routes, not Assignment/Evidence routes; roster/principal registries are not authorization services; W112 DOC-001 is draft, not runtime enforcement.
- GAP-01 remains OPEN / P0; E2 receipt and E3 trace NOT PROVEN.

These are bounded source/tool-surface findings, not proof that no external, separately deployed or user-operated path exists. No provider account, private session, runtime, credential, endpoint or deployed configuration was tested.

## 3. Ownership map — target boundary, not runtime proof

| Concern | Target boundary | Current evidence | Required decision |
|---|---|---|---|
| Work/WP/Gate | W70 governance / approved Core projection | Documents exist; live store not proven | Name canonical service and owner |
| Assignment record | Existing approved Core/Work service, if present | Owner/API/store not identified | Named accountable owner; persistence/schema proof |
| Identity/auth | W0000 identity governance + enforced Core auth | Registries are not authenticated authorization | Trusted principal, scope, expiry, revoke, audit |
| AI orchestration | W52 target responsibility | Runtime authority not proven here | W52 owner confirms interface/non-overlap |
| Cross-Work correlation | W112 target contract | DOC-001 draft, not runtime-approved | Governance approval; no parallel ID scheme |
| Evidence provenance | Existing approved W33/Core service | Evidence owner/API not identified | Owner, immutable refs, retention/privacy |
| Adapter/build boundary | Existing approved Core/Gateway/Build | No private-session dispatch exposed | Verify existing capability; no assumed gateway |

If no existing Core service owns Assignment state, stop and request an owner-authored architecture decision through Work 70. W17/W52 must not silently assume ownership.

## 4. Transport option assessment

| Option | Existing conversation | Automation | Cost | Assurance | Disposition |
|---|---|---|---|---|---|
| Native connector | Only if provider explicitly supports target session continuity | Potentially automated | Existing entitlement; verify | Strongest with trusted session binding + provider receipt | Long-term candidate; NOT VERIFIED |
| SESSION_HANDOFF | Yes, human pastes into exact conversation | User-mediated | No API call required for handoff | Manual-attested, lower assurance | First candidate for review |
| ROOM Meeting relay | Does not prove private-session continuity | Meeting-only | Existing service | Meeting message only | Not a substitute |
| Provider API adapter | May create new session; continuity varies | Automated | May cost | Depends on provider auth/receipt | Defer; explicit cost approval |
| UNSUPPORTED | N/A | None | Zero | No delivery claim | Fail closed |

No silent fallback may change target session or incur API cost. A mode change is a separately recorded decision.

## 5. SESSION_HANDOFF logical protocol (not implemented)

### 5.1 HANDOFF_READY

Use the DOC-044-based assignment snapshot and stable assignment ID/version. Generate an immutable, deterministic packet containing Work/WP, assignment/version, issuer, intended AI roster ID/role, objective, bounded scope, source baseline, allowed/prohibited actions, inputs, deliverables, acceptance criteria, due/expiry and response schema.

Bind `dispatch_id`, `attempt_id`, `correlation_id`, `idempotency_key`, `payload_digest`, `issued_at`, `expires_at` and one-time random nonce/challenge. Exclude passwords, API keys, cookies, provider tokens, private chat history and unrelated personal data.

Packet creation means only HANDOFF_READY — never DELIVERED or ACKNOWLEDGED.

### 5.2 HANDOFF_SUBMITTED

A human copies the immutable packet into the exact existing conversation they select. Record packet ID/digest, selected AI/provider label, operator principal, timestamp and a permitted conversation reference. Do not scrape/store cookies or private identifiers.

This is operator attestation only. It is not provider receipt and does not prove the AI processed the packet. Wrong target, stale version, expired packet or digest mismatch => INVALID/EXPIRED; never silently retarget.

### 5.3 MANUAL_ATTESTED response

The response should echo assignment_id/version, dispatch_id, attempt_id, correlation_id, payload_digest, nonce, decision (ACCEPT/REJECT/NEED_CLARIFICATION), accepted_scope_digest, response time, next-update estimate and reason for rejection/clarification.

A human records the response and evidence reference as MANUAL_ATTESTED. Nonce echo correlates a response to a packet but does not authenticate provider/session identity. A typed AI ID is not proof.

### 5.4 State separation

- HANDOFF_READY: packet prepared only.
- HANDOFF_SUBMITTED: operator attests packet was pasted; no provider receipt claim.
- MANUAL_ATTESTED: response manually recorded; assurance remains manual.
- ACKNOWLEDGED_MANUAL: only if the approved business owner accepts this assurance for a specific pilot; never map to verified ACK.
- ACKNOWLEDGED_VERIFIED: reserved for trusted connector/provider identity + receipt bound to the same assignment/dispatch/attempt.
- DELIVERY_UNKNOWN: submission but no attributable receipt/response; reconcile before retry.
- REJECTED / NEED_CLARIFICATION / EXPIRED / CANCELLED: explicit reason and authorized actor.
- No response means no ACK. A human must not type acceptance on an AI's behalf.

These labels are proposals for DOC-065 reconciliation, not approved live state transitions.

## 6. Correlation and security invariants

1. One correlation_id follows assignment → dispatch → attempt → receipt → ACK → progress/result.
2. Stable assignment_id/version; each attempt has unique dispatch_id/attempt_id.
3. Same idempotency key + same digest = same logical retry; same key + changed digest = IDEMPOTENCY_CONFLICT.
4. Nonce is random, single-use, assignment/attempt-bound, time-limited and invalidated on cancel/expiry. Echo is not identity proof.
5. Preserve response evidence, digest, operator attestation, timestamps, provenance and source assignment version; redact unrelated conversation content.
6. Use event sequence/causation ID for ordering; retain occurred_at and received_at separately.
7. ACK does not grant execution permission and cannot mutate Work/WP/Gate.
8. Unknown, stale, conflicting, expired, unbound or replayed evidence fails closed.
9. Retention, encryption, access and deletion must be approved by the existing evidence/data owner.
10. Meeting transcript, Git commit, Sandbox write, browser marker, roster membership or Xu's note can never be substituted for provider receipt/AI ACK.

## 7. Assurance levels

| Level | Meaning | Allowed claim |
|---|---|---|
| P0 PACKET_ONLY | Packet generated | HANDOFF_READY |
| P1 OPERATOR_ATTESTED | Human says it was submitted | HANDOFF_SUBMITTED, not provider DELIVERED |
| P2 RESPONSE_MANUAL_ATTESTED | Human records matching response/digest/challenge | MANUAL_ATTESTED; optional ACKNOWLEDGED_MANUAL only if approved |
| P3 CONNECTOR_VERIFIED | Trusted provider receipt + authenticated session/AI binding + matching ACK | DELIVERED + ACKNOWLEDGED_VERIFIED |
| P4 E2E_TRACE | P3 plus execution/artifact/verification/independent trace | E3 candidate |

P0–P2 do not satisfy W17 E2 provider receipt or E3 dispatch/ACK criteria. A P2 usability pilot cannot close GAP-01.

## 8. Failure handling

| Failure | Required handling | Forbidden |
|---|---|---|
| Owner unknown | Stop; ownership decision | Parallel store/API |
| Target session unverified | BLOCKED/UNSUPPORTED | Guess recipient |
| Stale/expired packet | Reject; regenerate from current approved assignment | Reuse stale packet |
| Wrong conversation | INVALID + audit | Silent retarget |
| No response | DELIVERY_UNKNOWN/timeout | Assume delivered/accepted |
| Nonce mismatch/replay | Reject + audit | Trust matching display name |
| Typed AI ID only | Manual assurance only | Claim authenticated identity |
| Duplicate submit/ACK | Idempotent dedupe | Duplicate execution |
| Same key, changed payload | IDEMPOTENCY_CONFLICT | Overwrite |
| Connector fallback changes session | Stop for decision | Silent new session/API spend |
| Grant revoked/expired | Deny next privileged action | Continue on old ACK |
| Secret/private context in evidence | Quarantine/redact per incident policy | Store in journal |
| Evidence service unavailable | Document-only/BLOCKED | Sandbox/Meeting as shadow DB |

## 9. Minimal pilot prerequisites — NOT AUTHORIZED

- Named Core/Assignment owner and approved authoritative record/persistence contract.
- Explicit Vinh Work Entry authorizing one bounded, non-sensitive assignment.
- Ka security review, technical owner review, independent QE plan/reviewer.
- One AI with unambiguous roster identity/provider/model and operator-selected target session.
- Approved privacy/retention for manual response evidence.
- Manual receipt explicitly labeled lower assurance; no claim of E2/E3.
- No code execution, repository write, secret access, privileged action, API usage or paid fallback.

A successful manual pilot proves only P1/P2 usability, not automatic dispatch, provider delivery or cryptographic identity.

## 10. Independent review requests (proposed, NOT SENT)

- Ka / AI-02: threat model wrong-session submission, prompt injection, nonce replay, manual-attestation abuse, privacy/retention, identity assurance and fail-closed behavior. Require severity/evidence/disposition and APPROVE / REQUEST_CHANGES / BLOCKED.
- Core accountable maintainer (not yet identified): name Assignment/Work/Evidence authority, persistence, authenticated principal, current API/router mount and audit contract. If absent, state so and route through governance.
- Cla / AI-03: assess minimal DOC-044/DOC-065-compatible handoff path using existing approved components only; identify hidden dependencies and confirm no new API/DB/dispatcher.
- Independent QE (later): derive negative/positive tests only after owner and contract approval.

No review request was sent to any AI member; no ACK is claimed.

## 11. Gates and next actions

| Gate | Required evidence | State |
|---|---|---|
| D1 Core/Assignment/Evidence owner | Named owner + existing service/API/persistence proof | BLOCKED |
| D2 DOC-064/065 reconciliation | Owner-approved mapping; no assumed routes | NOT STARTED |
| D3 Ka + Cla independent reviews | Written independent findings | NOT REQUESTED / NOT DISPATCHED |
| D4 Manual assurance decision | Explicit Vinh decision and scope | NOT AUTHORIZED |
| D5 Bounded pilot plan | Work Entry, owner, reviewer, target, expiry, privacy | NOT AUTHORIZED |
| D6 Connector verification | Trusted session binding + provider receipt | NOT PROVEN |

Immediate next read-only action: identify accountable Core maintainer from existing governance/source ownership records. Prepare review packets, but do not submit them to AI sessions until an approved assignment/handoff channel exists. Do not create another Work, API, database, dispatcher or Meeting relay.

## 12. Disposition

GAP-01 OPEN / P0; E2 provider delivery receipt NOT PROVEN; E3 assignment→dispatch→delivery→ACK NOT PROVEN; Core Assignment/Evidence owner NOT IDENTIFIED in inspected scope; SESSION_HANDOFF is a review candidate only; Work 17 READ/TRACE ONLY; protected execution DENY / NOT RELEASED; BUILD/live dispatch/pilot NOT AUTHORIZED.

This is an analysis artifact only. It does not close a gap, approve a contract delta, create an assignment, prove delivery or authorize implementation.
