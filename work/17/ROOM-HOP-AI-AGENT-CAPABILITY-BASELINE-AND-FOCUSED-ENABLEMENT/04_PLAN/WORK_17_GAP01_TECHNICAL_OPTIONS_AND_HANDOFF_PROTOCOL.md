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
- W70 D70-023 (Decision Log blob `53c5a7cfdb02bc38e4213010004e1f0ad137d87f`) and W112 Related Work Integration Index blob `7043e61807d4e46399fca0f5faf532ea2ae317c9` explicitly assign target ownership: W70 Work lifecycle/control plane; W52 Agent-to-Agent task/event orchestration and provider adapters; W37 investigates/evidences the single Core, which remains the source of truth; W33 Evidence Hub; W112 cross-Work contracts/mapping; W14 execution boundary. D70-023 says independent review is pending and implementation/migration/release are not authorized.
- DOC-071 current blob `12f11320dc9da89b27de21313b698224d74519ce` continues to find Work/WP/Assignment persistence and Work Evidence Registry NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED, and accountable Core maintainer NOT IDENTIFIED. Logical ownership is therefore known at governance level; accountable runtime maintainer, APIs and deployed persistence are not.
- Entry 017: exposed 8030 tools do not include private-session dispatch or provider receipt/ACK retrieval.
- Entry 018: Browser Agent Adapter Meeting marker/read-back proves artifact recording in Meeting, not provider delivery or AI ACK.
- Entry 019: inspected Core HTTP composition exposes Meeting/identity routes, not Assignment/Evidence routes; roster/principal registries are not authorization services; W112 DOC-001 is draft, not runtime enforcement.
- GAP-01 remains OPEN / P0; E2 receipt and E3 trace NOT PROVEN.

These are bounded source/tool-surface findings, not proof that no external, separately deployed or user-operated path exists. No provider account, private session, runtime, credential, endpoint or deployed configuration was tested.

## 3. Ownership map — target boundary, not runtime proof

| Concern | Target owner/boundary | Current evidence | Required decision/evidence |
|---|---|---|---|
| Work lifecycle, assignment policy and gates | W70 owns lifecycle/control plane (D70-023) | Ownership explicitly decided; runtime implementation/persistence not proven | Map W70 authority to an existing approved Core service; no parallel control plane |
| Core authoritative data/persistence | W37 investigates/evidences the single Core; D70-023 names Core as source of truth | DOC-071 finds Work/Assignment persistence NOT VERIFIED; accountable Core maintainer NOT IDENTIFIED | Identify live Core maintainer, API/router, store and audit semantics; W37 workspace is not itself Core |
| Agent-to-Agent dispatch/orchestration | W52 owns task/event orchestration and provider adapters (D70-023) | Target ownership decided; actual dispatch path/provider adapters not verified | W52 owner confirms current adapter/transport implementation and non-overlap |
| Identity/authentication | W0000 governance registry + enforced Core authorization boundary | Roster/principal registries are not authenticated authorization | Trusted principal source, scope, expiry, revocation and audit proof |
| Evidence storage/provenance | W33 owns Evidence Hub (D70-023) | Target ownership decided; Work Evidence Registry API/persistence NOT VERIFIED | W33 owner confirms existing store, immutable refs, retention/privacy and Core linkage |
| Cross-Work correlation | W112 owns cross-Work contracts/mapping | DOC-001 draft, not runtime-approved | Approve/adopt contract through governance; no parallel ID scheme |
| Execution boundary | W14 owns execution host (D70-023) | Host security/runtime evidence remains a separate open gap | Keep ACK separate from execution grants; no execution permission implied |

If an existing Core service/API does not implement the approved W70/W52/W33 boundaries, stop and request an owner-authored architecture decision through Work 70. W17 must not silently take component ownership or create replacement services.

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


## 13. Addendum — Core ownership correction and W52 adapter evidence (2026-11-19)

**Correction from Vinh:** Core is jointly built by Vinh and Xu. Do not search for an external Core maintainer or interpret missing CODEOWNERS/PR metadata as unknown Core ownership. Vinh remains the decision authority; Xu is the delegated co-architect/coordinator. W37 is the Core investigation/evidence boundary, not a substitute owner of Core's creation. This supersedes the earlier wording in Entries 020–021 and §3/§10/§11/§12 that suggested an unidentified accountable human Core maintainer. The unresolved questions are implementation facts: exact live Core API/router composition, Work/Assignment persistence, authorization binding and evidence-store runtime—not who built Core.

**W52 read-only trace:** W52 Sandbox contains a candidate room_a2a package and tests/evidence. The inspected adapter registry contains only CodexAdapter (Codex App Server) and QwenAdapter (ACP v1). Both advertise only task.stream_events; the documented profile is no-tool/read-only. This is not a universal provider adapter and does not prove access to private ChatGPT/Gemini/Claude/Grok/Mistral sessions or cloud provider APIs. Live Codex/Qwen are recorded BLOCKED in the capability matrix (CLI absent in the recorded probe environment); native invocation and stream/cancel remain unverified.

CorePort, AuthorityPort, and HostPort are injected interfaces, not production bindings. W52 requires the existing Core for task/event persistence and authorization, and W14 for Host-owned process/transport lifecycle. W52's 2026-10-29 static review records CorePort/AuthorityPort/W14 HostPort and native Codex/Qwen invocation BLOCKED; full E2E NOT RUN. Historical 42/42 coder tests are not independent PASS. W52 remains ACTIVE / DESIGN-FIRST / NOT RELEASED.

**Disposition:** W52 is a reusable candidate component, not a proven active dispatch route. No provider delivery receipt, authenticated recipient ACK or E3 assignment trace was established. Sandbox/GitHub parity and canonical W52 promotion were not tested. No code, test, runtime, provider, branch or release action was performed. GAP-01 remains OPEN / P0; E2/E3 NOT PROVEN; Work 17 READ/TRACE ONLY; protected execution DENY / NOT RELEASED; BUILD/live dispatch/pilot NOT AUTHORIZED.

**Next read-only step:** trace whether the existing W14 Host and Core composition can bind the two W52 adapters without creating parallel services; verify exact route/contract and deployed runtime evidence before any integration proposal. Ka/Cla reviews remain NOT SENT.
