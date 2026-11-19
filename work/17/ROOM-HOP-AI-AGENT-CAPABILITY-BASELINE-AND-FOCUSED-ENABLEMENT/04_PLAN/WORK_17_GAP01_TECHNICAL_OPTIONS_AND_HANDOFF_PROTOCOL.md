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


## 14. Addendum — W52 HostPort / W14 boundary compatibility (2026-11-19)

W52's HostPort contract requires an adapter-specific, long-lived RpcPort with request/notify/receive/respond and a confirmed stop operation. The inspected W14 HTTP surface exposes only GET /health and POST /execute. W14 W12ExecutionAdapter accepts a one-shot command and returns an ExecutionResult; W14's declared adapters are BrowserAdapter, GitHubGateway and CIAdapter. No direct W52 HostPort binding or bidirectional provider transport is present in the inspected source.

Therefore W14's ability to execute a command must not be confused with delivery to an AI provider or recipient ACK. W14 RuntimeIdentity identifies the host process, not the AI recipient. In addition, the inspected W14 WorkContext authorization is a caller-supplied boolean and does not itself prove online Core grant validation; see W17 GAP-11 for that separate security gap.

**Disposition:** W52→W14 HostPort direct binding NOT PROVEN / contract mismatch in inspected interfaces. No endpoint was called and no runtime was started. Any reuse must remain inside the existing W14 execution boundary and require Core-authorized WorkContext/agent identity, Host-owned stdio/RPC lifecycle, bounded framing/output, cancel/stop confirmation and evidence correlation. This is a design question for W14/W70/Core governance, not authorization to add a parallel endpoint or executor. GAP-01 remains OPEN / P0; E2/E3 NOT PROVEN; READ/TRACE ONLY.

## 15. Addendum — Core / W70 / W33 end-to-end responsibility trace (2026-11-19)

The intended ownership chain is:
- W70 Control Plane: Work/WP/Task lifecycle, Assignment policy, permissions/gates/decisions and dashboard projection (DOC-095).
- Core (Vinh + Xu): authoritative shared service/state and identity boundary; the inspected Core HTTP app currently composes Meeting and identity routes, not Work Assignment/Dispatch/Evidence routes.
- W52: provider-neutral Agent-to-Agent orchestration, provider adapters and task/event delivery semantics.
- W14: execution-host and process/transport boundary.
- W33: durable shared file/evidence storage.
- W112: cross-Work integration contracts, dependency/evidence correlation and integration coordination.

Core evidence: core_http_main.py composes create_http_app; inspected http_server.py mounts /identities and Meeting routes only. identity_resolution.py resolves Principal/Agent Registry entries. agent_registry.py explicitly defers permissions/authority; identity existence is not dispatch authorization. Meeting membership policy is not Work Assignment authority. This is bounded source inspection, not a claim about all deployments.

W70 evidence: DOC-095 is DESIGN BASELINE / IMPLEMENTATION NOT AUTHORIZED and explicitly lists runtime dispatch/event delivery/evidence parity/concurrency/recovery as not fully verified. DOC-044 is ACTIVE/TEMPLATE, not a runtime Assignment API. DOC-005 requires server-side authorization, version/CAS, gate/evidence checks, audit correlation and idempotency, but the inspected Core routes do not establish that implementation.

W33 evidence: Work 33 is an offline CLI-first content-addressed store (SHA-256 blobs + SQLite + audit). v1 has no HTTP server. put accepts caller-supplied --agent attribution string; this is not authenticated provider identity. A10 integration remains BLOCKED pending Core/MCP write path and credentials. Thus W33 is a reusable storage component, not a proven live Work Evidence Registry ingress.

Combined verdict: no live integrated chain is proven. W70's Assignment design, Core identity registry, W52 adapter candidates, W14 execution host and W33 store are distinct pieces with unclosed runtime contracts. Do not bypass W70/Core authorization, do not call a W14 command result provider ACK, and do not let W33's agent metadata authenticate a sender. W112 should coordinate the cross-Work contract without taking ownership away from component Works. No new dispatcher/API/database/queue is proposed.

GAP-01 remains OPEN / P0; E2/E3 NOT PROVEN; Work 17 READ/TRACE ONLY; protected execution DENY / NOT RELEASED; BUILD/live dispatch/pilot NOT AUTHORIZED.

## 16. Addendum — Reuse W112 DOC-001; no parallel cross-Work contract (2026-11-19)

W112 already defines the cross-Work contract baseline in DOC-001 v1.0. It is DRAFT / DESIGN BASELINE and NOT APPROVED FOR RUNTIME ENFORCEMENT. Reuse it as the candidate common contract; do not duplicate its assignment/event/evidence schemas inside Work17 or build a parallel dispatcher, event bus, evidence store or lifecycle engine.

| Boundary | Authority / component responsibility | Existing contract/source evidence | Current evidence status | Required closure evidence |
|---|---|---|---|---|
| Work/WP/Task/Assignment lifecycle | W70 policy and lifecycle authority | DOC-095, DOC-044, DOC-005 | Design/template; no live Assignment route proven in inspected Core app | Owner-approved versioned contract, server-side state transition API, CAS/version guard, authorization and journal readback |
| Core identity/authority/state | Core built by Vinh + Xu; Vinh decision authority | Core HTTP app, identity_resolution, Agent/Principal Registry | Meeting/identity routes inspected; Agent Registry defers permission/authority; Work Assignment/Dispatch routes not found in inspected app | Exact deployed source/commit and route map; authenticated principal/agent resolution; server-side grant checks; authoritative persistence |
| Provider dispatch/events | W52 | A2A contract, adapter-interface, room_a2a adapter registry | Sandbox candidate Codex App Server + Qwen ACP only; W52 not mapped to canonical GitHub Work subtree per W112 index (dated 2026-11-09) | Owner-approved canonical repo/branch/commit; native runtime adapter; authenticated provider receipt; correlated ACK |
| Execution/transport | W14 | W14 HostPort/HTTP source | W52 HostPort requires long-lived RPC; inspected W14 exposes one-shot /execute; direct binding not proven | Versioned RPC/stdio contract within W14 boundary; Core-authorized identity; cancel/stop and process evidence; no second executor |
| Evidence storage | W33 | RSFEH architecture/data model/CLI | CLI-only v1; no HTTP server; Core/MCP integration A10 BLOCKED; W33 branch mapping requires refresh | Canonical branch/commit; Core-authorized write path; authenticated actor; immutable content hash and retrievable evidence refs |
| Cross-Work compatibility | W112 | DOC-001 v1.0, Integration Charter | DRAFT, not runtime enforcement; explicit assignment/event/evidence semantics already exist | Owner review, version compatibility, contract fixtures, S0–S5 integration evidence |
| Quality and acceptance | W32 / independent QE / W70 | DOC-001 test levels + W70 gates | No live integrated E2E or independent QE PASS established | Replay/idempotency/concurrency/security/recovery tests, independent QE, Founder acceptance |

### Required event/receipt invariants to preserve
1. DISPATCHED is not ACKNOWLEDGED. Artifact arrival or host command success is not recipient ACK.
2. ACK must be attributable to authenticated receiving identity and the exact assignment_id; include correlation_id, causation_id, idempotency_key, source_revision and delivery_attempt.
3. Provider receipt, recipient ACK, execution permission and acceptance are separate facts and separate state transitions.
4. Unknown identity, missing permission, stale revision, replay or mismatched assignment must fail closed.
5. Evidence states RECORDED, VERIFIED, NOT_RUN, NOT_VERIFIED, REJECTED remain distinct. MOCK/SNAPSHOT/SANDBOX evidence cannot be promoted to LIVE.
6. W70 retains lifecycle authority; Core enforces shared identity/authority/state; W52 owns provider communication; W14 owns execution host; W33 stores evidence; W112 coordinates cross-boundary contracts. No owner is replaced.

### Canonical-source blockers
W112's 2026-11-09 index records W52 NOT SYNCED (branch exists but no W52 Work-document subtree), W33 on a Work branch, W14 PARTIAL SYNC on a release branch, and W37 as investigation workspace rather than proof of Core source ownership. These are dated mapping records, not current branch-state proofs; exact canonical repo/branch/commit must be freshly reconciled before integration. Vinh's direct Core ownership correction (Vinh + Xu) governs Work17's Core-builder boundary.

No implementation, branch promotion, live dispatch or provider test is authorized by this matrix. GAP-01 remains OPEN/P0; E2/E3 NOT PROVEN; Work17 READ/TRACE ONLY.


## 17. Addendum — Prepared independent review packets (2026-11-19)

**Preparation state: READY FOR FOUNDER-TRIGGERED REVIEW; NOT SENT.** These briefs are embedded in the existing canonical technical proposal. No separate packet files were created. Ka/Cla have not been contacted. Release requires Vinh's explicit instruction.

### Packet K — Ka (CSA / architecture and security boundary review)

**Objective:** challenge whether GAP-01 can connect W70 Assignment authority, Core identity/permission, W52 provider dispatch, W14 execution/transport, W33 evidence persistence and W70 projection without bypassing ownership or weakening security.

**Read set:** this Work17 proposal (Addenda 14–17), Audit Journal Entries 023–026, GAP-01/GAP-11; W112 DOC-001 v1.0, Integration Charter and Related Work Integration Index; W70 DOC-095, DOC-044 and DOC-005. Use owner-approved source snapshots only after exact repository/branch/commit reconciliation.

**Questions (every answer must cite source/path/line/commit):**
1. Is the authority chain complete and non-circular? Identify who creates, authorizes, dispatches, receives, ACKs, permits execution, accepts output and writes evidence. Preserve Vinh+Xu as Core builders and Vinh as decision authority.
2. Can W70 Assignment transitions be enforced server-side with authenticated actor, permission/grant validation, expected-version/CAS, expiry/revocation, idempotency and audit correlation? Distinguish normative DOCs from live routes/persistence.
3. What cryptographic/authenticated proof binds ACK to the actual receiving AI/provider session and exact assignment_id, correlation_id, causation_id, idempotency_key, source_revision and delivery_attempt? Explain why browser marker, user attestation, host process identity, nonce or artifact arrival is insufficient for VERIFIED ACK.
4. Can W52 long-lived provider communication coexist with W14's inspected one-shot /execute surface without creating a second dispatcher/executor or confusing host identity with recipient identity? State the smallest owner-preserving contract delta.
5. Does W33 CLI-first, caller-attributed write path meet authenticated evidence-ingress needs? If not, identify the authorized owner boundary; do not propose a parallel evidence store.
6. Threat-model replay/spoofed/stale ACK, wrong recipient, assignment substitution, duplicate dispatch, timeout/unknown delivery, retry storms, permission revocation, out-of-order events, concurrent transitions, partial persistence and evidence tampering. Specify fail-closed and recovery behavior.
7. Are MOCK/SNAPSHOT/SANDBOX/LIVE and RECORDED/VERIFIED/NOT_RUN/NOT_VERIFIED/REJECTED sufficiently separated? Identify false-PASS paths.

**Required output:** verdict per question (PASS/GAP/BLOCKED/NOT REVIEWED), evidence references and bounded scope, ranked critical risks, minimum prerequisites before design approval/implementation/live pilot, and confirmation no recommendation creates a parallel dispatcher/bus/store/bypass. Static review only.

### Packet C — Cla (CTO / code and integration feasibility review)

**Objective:** verify technical feasibility against canonical source, distinguish reusable code from deployed runtime behavior, and identify minimum changes within existing component ownership.

**Read set:** same Work17 proposal/journal/GAP and W112/W70 docs as Packet K; Core HTTP composition and identity/registry source; W52 adapter interfaces and candidate Codex/Qwen adapters; W14 HostPort/HTTP server/adapters; W33 CLI/store/integration acceptance criterion. Every source claim must include repository, branch, commit and exact path. Sandbox snapshots are not canonical until reconciled.

**Questions (code-level evidence required):**
1. Reconcile canonical repository/branch/commit and source-of-truth for Core, W52, W14, W33 and W70. Mark missing/stale/partial/unverified mappings; do not infer from branch names or commit authors.
2. Trace Assignment creation → dispatch → provider transport → receipt → recipient ACK → execution authorization → artifact submission → evidence persistence → W70 projection. Name implemented symbol/route/interface and tests at each hop, or mark NOT FOUND / NOT VERIFIED.
3. Compare W52 HostPort/RpcPort with W14 HTTP /execute and adapters. Can an existing transport satisfy bidirectional streaming, cancellation, correlation and lifecycle, or is a versioned adapter contract needed? Keep one execution host.
4. Inspect Codex App Server and Qwen ACP candidates: do they submit to authenticated provider sessions and expose delivery receipts/authenticated ACK, or are they read-only/no-tool candidates? Separate interface declaration from operational proof.
5. Inspect Core route composition/registries: do Assignment/Dispatch/Evidence routes, authenticated actor resolution, server-side permission grants, durable state and concurrency controls exist? Meeting membership and registry identity are not Work authority.
6. Inspect W33 ingress/retrieval: are immutable SHA-256 content, authenticated actor attribution, event/assignment correlation, idempotent writes and durable retrieval available through an authorized Core path? Do not add a second store.
7. Propose smallest ordered implementation slices assigned to existing owners (W70/Core/W52/W14/W33/W112/W32-QE), with dependency gates and acceptance evidence. Include negative tests for spoofing, replay, stale revision, wrong assignment, duplicate delivery, timeout/unknown delivery, revocation and concurrency.

**Required output:** source-backed call graph; per-hop IMPLEMENTED/PARTIAL/DESIGN ONLY/NOT FOUND/NOT VERIFIED matrix; canonical-source reconciliation; minimal owner-preserving change list; test/evidence matrix; blockers and sequencing. No code changes, branch writes, provider calls, tests or live dispatch during review.

### Common reviewer constraints and decision rule
- Review is advisory only; it cannot approve implementation, release protected execution or authorize a pilot.
- Dispatch, transport success, browser marker, artifact arrival, user-mediated submission or host process completion are not recipient ACK.
- No parallel dispatcher, event bus, Assignment database, evidence store or execution host without explicit Vinh decision and W70 governance.
- If canonical source cannot be proven, mark BLOCKED / NOT VERIFIED; do not fill gaps with assumptions.
- Work17 remains READ/TRACE ONLY; protected execution DENY / NOT RELEASED. Ka/Cla review request remains unsent pending Vinh's instruction.


## 18. Addendum — Review dispatch capability and W52 branch reconciliation (2026-11-19)

### 18.1 Review dispatch capability check
Xu inspected the currently exposed ROOM-HOP Build MCP tool surface and available connected actions for a supported, auditable way to send a task/message to named ROOM agents. The exposed ROOM-HOP tools include Sandbox read/write/list and legacy meeting read/join/start/paste operations; no Assignment/Dispatch/Agent-message send operation was exposed. The legacy Meeting surface is excluded from use because its runtime is a known unsafe/broken boundary for this Work. No verified direct messaging endpoint or authenticated Ka/Cla recipient identity is available in the current tool surface.

**Disposition:** reviewer briefs remain PREPARED / NOT DELIVERED. This is a tooling boundary, not a decision to wait for Vinh. Xu must not claim that Ka/Cla were contacted, fabricate ACKs, or use a known-broken meeting path to simulate delivery. Continue all preparatory, source-trace and evidence work that is independently executable. When an approved, verifiable agent-dispatch route becomes available, Xu may use it within delegated authority and record the actual delivery receipt/recipient ACK separately.

### 18.2 W52 branch read-only reconciliation
GitHub branch search in `hqtt2026-thevinhvtqni/room-meeting-ai` returned exactly `work/52-room-universal-ai-communication-orchestration` for query `work/52`. Fetching its `README.md` succeeded (blob `677ed190bf05735de326064d5e0ac323d38642ba`). That README onboards to the legacy ROOM HOP v0.2 context set (`AGENTS.md`, `context/PROJECT_STATE.md`, `context/XU_CORE.md`, `context/XU_SESSION.md`, `context/XU_MEMORY.md`) and records an Aug-2026 state focused on MockConnector / Real API verification. Branch `AGENTS.md` blob `83d12cf8c29c8b167ef61ac04d10daab2411125d`; `PROJECT_STATE.md` blob `8c2bc37ac39e977ce3af9f1aa894b958f0e5de52`; `XU_CORE.md` blob `3e1ba4f51345100bfce33d98b9137bc05e16ed7b`; `XU_SESSION.md` blob `7d0ffaee0fc2e290c18bf4744af22a91a0e422bf`; `XU_MEMORY.md` blob `af64eff272d353e6eec986aaa846904de687186d`.
 
The following expected W52 source paths were NOT FOUND on that branch ref: `room_a2a/adapters.py`, `room_a2a/contracts.py`, `room_a2a/transport.py`, `WORK_MANIFEST.md`, `work/52/WORK_MANIFEST.md`. This bounded check does not prove the entire branch lacks W52 source; it proves only that the known candidate paths are not present at those locations and that its root README/context are legacy v0.2 onboarding. The W52 Sandbox candidate source remains the evidence base for the prior adapter trace; canonical source promotion/mapping remains NOT VERIFIED. No merge, migration or branch mutation performed.

### 18.3 Consequences
- Do not treat existence of a branch named for W52 as proof that the W52 Sandbox candidate source is promoted or canonical.
- Do not treat branch-level v0.2 Meeting/MockConnector state as proof of current provider dispatch, authenticated receipt or recipient ACK.
- Keep W52 owner boundary for Agent-to-Agent orchestration; W70 Assignment authority, Core identity/permission/state, W14 Host transport, W33 evidence and W112 compatibility boundaries unchanged.
- GAP-01 remains OPEN/P0; E2 provider receipt and E3 Assignment→Dispatch→Delivery→ACK remain NOT PROVEN. READ/TRACE ONLY; protected execution DENY / NOT RELEASED.


### 19. Core v0.2 provider connector trace — positive source finding, bounded scope

Read-only GitHub main fetch of core/connectors.py, core/discussion.py, core/agent_registry.py, core/identity_resolution.py, run_meeting_v2.py and inspected tests establishes:

- Core contains source implementations for synchronous OpenAI Chat Completions and Anthropic Messages calls behind AgentConnector.send_turn(MeetingContextForAgent) -> AgentResponse. This is a positive provider-call primitive for Meeting turns; do not state Core has no provider connector.
- The inspected return contract reduces provider output to parsed text/status. It does not expose provider delivery receipt/request ID, authenticated recipient identity, Work assignment_id, dispatch_id, attempt/correlation/idempotency binding or attributable ACK proof.
- run_discussion() dispatches by Meeting participant order and writes Meeting messages/events. It is not W70 Work Assignment lifecycle and does not prove Assignment authority, Work dispatch state or W33 evidence ingress.
- Inspected run_meeting_v2.py main path calls build_mock_connectors(); it does not select the real OpenAI/Anthropic connectors. Inspected connector tests cover parsing, mock behavior and missing key/model guards, not a successful provider HTTP round trip. MISSION-2026-001 report dated 2026-08-15 also records real API NOT TESTED; historical evidence only.
- Agent Registry explicitly defers permissions/authority; identity resolution only identifies registry membership and does not authenticate provider-side recipient or authorize a Work Assignment.

Architecture disposition: reuse candidate = Core existing provider-call primitive, only after verifying a live supported caller and preserving Core ownership. Missing proof remains the bridge from W70 Assignment → Core authorization/dispatch → provider delivery receipt → recipient-bound ACK → evidence. Do not build a second connector registry or dispatcher in Work17. Source-level only; no provider call, test, runtime or credential check occurred. GAP-01 remains OPEN/P0, E2/E3 NOT PROVEN, READ/TRACE ONLY.


### 20. Core HTTP composition check — provider connector wiring remains unproven

Read-only fetch of room_hop_mcp/core_http_main.py and room_hop_mcp/adapter/http_server.py on GitHub main:

- build_app() constructs MeetingManager/MeetingService and returns create_http_app(service); this entrypoint does not import or construct AgentConnector, OpenAIConnector, AnthropicConnector, connector factory or run_discussion.
- The inspected HTTP adapter defines only identity and Meeting routes (GET /identities, GET /meetings, GET /meetings/{id}, GET /meetings/{id}/transcript; POST Meeting paste/create/open/join/start/close). No Work Assignment/dispatch/provider invocation/receipt/ACK/evidence-ingress route is defined in this file.
- The entrypoint docstring claims an additive Work execution-authority mount, but inspected composition returns only create_http_app(service); the inspected adapter contains no such route. Record this as a bounded source/documentation discrepancy, not proof about every deployment or branch.

Disposition: Core OpenAI/Anthropic connector source exists (Addendum 19), but connector-to-Core-HTTP runtime wiring and a Work dispatch route are NOT PROVEN in inspected main sources. Do not create a parallel app/dispatcher in Work17. GAP-01 OPEN/P0; E2/E3 NOT PROVEN; READ/TRACE ONLY. No runtime, HTTP, provider or test invocation occurred.


### 21. W1111 Core Execution Authority V1.2 branch candidate — reuse boundary and review blockers

Read-only comparison of branch work/w1111-core-execution-authority-v1-2 and PR #48 found an existing Core execution-grant implementation candidate:

- Core source core/execution_authority.py implements enrolled service-credential authentication, Work/purpose-scoped short-lived grants and an append-only hash-chained JSONL journal.
- Branch-specific room_hop_mcp/adapter/http_server.py mounts the five execution-authority routes through mount_execution_authority_routes; main's inspected adapter does not. Branch W13 Host source validates the grant online and binds pytest execution to the Work source snapshot.
- PR #48 is OPEN/DRAFT, unmerged; current head c70eb2b82f54a000a81263dc519078ddf105f075; compare main...branch reports DIVERGED, ahead 157 / behind 648, mergeable=false. Historical CI success on 9bbeed63... is not current-head proof; no PR-triggered run was returned for current head by the available query (push runs not covered).
- W1111 approval record states DR-1..DR-4 approved, Gate 2 implementation authorized, but Gate 3 runtime alignment, Gate 4 live/security E2E and Gate 5 wiring/publishing remain NOT OPEN. No Work17 authority to merge/deploy/restart or access secrets follows from this.

Static integrity blocker: branch ExecutionAuthority.record_run() validates that submitted source hash is 64-hex but does not compare it to the source hash bound to the Work policy/grant. The branch unit test configures a...a, submits b...b, and expects the run record to succeed. This contradicts the stated exact-source binding requirement. Candidate defect to return to W1111/PR #48 owner review; not changed by Work17.

GAP-01 boundary: Execution grants authorize an enrolled service identity to perform a Work/purpose operation. They do not implement AI member private-session dispatch, provider delivery receipt or recipient-bound ACK. Keep execution authority separate from Agent Assignment dispatch. Do not create a duplicate execution authority in Work17 and do not merge the diverged branch.


### 22. Contract compatibility — Execution Authority grant is not Agent Assignment dispatch

Cross-check against W112 DOC-001 v1.0 (DRAFT), W70 DOC-063 (DRAFT / design only) and W70 DOC-065 v1.0 (DRAFT contract proposal) confirms distinct responsibilities:

- DOC-001 Assignment requires assignment/task/assignee/accountable role/scope/permission/capability/dependencies/status/ACK references; ACK must be attributable to receiving identity and assignment ID. Events/evidence require correlation, causation, idempotency, source revision and provenance.
- DOC-063 requires trusted principal + Work/WP/assignment + exact action/resource scope + source revision + Gate/WP snapshot + expiry/revocation + policy version + idempotency/version checks, with assignment and verifiable ACK before protected action and commit-time revalidation.
- DOC-065 requires assignment_id, dispatch_id, attempt_id, ai_id, adapter/session target, delivery receipt/status, identity proof and recipient-bound ACK; dispatch is not ACK.
- W1111 PR #48 Execution Authority candidate grants a service identity a Work/purpose-scoped execution token and records an execution run. The inspected grant schema is not the DOC-001 Assignment lifecycle and has no provider/session delivery or recipient-bound ACK contract.

Disposition: PR #48 is a useful execution-authorization candidate only; it cannot replace W70 Assignment authority, W52 provider dispatch or DOC-065 delivery/ACK. It does not close GAP-01 E2/E3. DOC-001/DOC-063/DOC-065 remain unapproved for runtime enforcement; do not duplicate registries or dispatchers in Work17.


### 24. W52 branch full-tree reconciliation — legacy connector source is Meeting-scoped, not Work dispatch

Branch `work/52-room-universal-ai-communication-orchestration` resolves to commit `afd93ea8960d4cf9b27a57338b75f8d51624c170` (tree `6bd3411c0381c1d8bd595d23b68bf8b583273c10`; 398 entries, not truncated). This corrects the scope of Entry 027: the branch DOES contain `docs/work52/{README,BIEN_BAN,KE_HOACH_THI_CONG_XU,NHAT_KY_HOP_THI_CONG}.md` and legacy `core/connectors.py` / `core/discussion.py`. The earlier missing-path finding applied only to newer `room_a2a/*` candidate adapters/contracts/transport and manifest locations tested, not all W52 files.

- W52 README: ACTIVE / DESIGN-FIRST / NOT RELEASED; provider-neutral A2A design, reuse Core/Gateway/Agent Runtime/MCP 8030/Sandbox; no production changes before gates. Plan says G0 IN PROGRESS and G1-G6 NOT STARTED. Design/plan is not implementation or release proof.
- Legacy `core/connectors.py` (blob `809c4d2fca01e6fcdaf26b91bf34b1af26dfd15a`) contains AgentConnector.send_turn() and synchronous OpenAI/Anthropic provider HTTP calls, plus Mock/Internal connectors. This is a genuine provider-call primitive for Meeting turns.
- `core/discussion.py` (blob `aa722f95235f613c288ba212074527ed2ce01ebc`) selects Meeting participants round-robin and persists Meeting messages/events. It does not bind a W70 Work Assignment, permission_ref, dispatch_id/attempt, provider receipt, recipient-authenticated ACK or W33 evidence reference.
- Identity Resolution / Meeting JOIN policy is not Work authorization or provider-side recipient authentication. AgentResponse is status/content/raw only. Claude/Xu model fields are blank in the inspected branch snapshot; Ka internal configuration does not establish an independent reachable runtime.
- W52 plan/log remain at initialization/G0 inventory stage. The older connector does not prove newer W52 A2A candidate source is canonical or deployed.

Disposition: legacy Meeting provider-call primitive EXISTS IN SOURCE; current W52 Work dispatch/delivery/ACK chain NOT PROVEN. Do not use legacy Meeting surface as workaround; no branch merge/migration, provider call, test or dispatch occurred. GAP-01 OPEN/P0; E2/E3 NOT PROVEN; READ/TRACE ONLY; protected execution DENY / NOT RELEASED.


### 23. Consolidated GAP-01 ownership and closure-evidence map

| Boundary / owner | Reusable evidence found | Missing proof to close GAP-01 |
|---|---|---|
| W70 Assignment/lifecycle | DOC-044 template; DOC-095 design baseline; DOC-005 state-machine requirements | Live Assignment service/persistence, server-side authority, ACK-bound transitions, version/idempotency/audit |
| Core identity/auth | AgentRegistry + identity_resolution membership only; W1111 PR #48 service execution grant candidate | Authenticated AI recipient identity/session, active Assignment binding, scope/expiry/revocation/source/gate checks; distinguish service identity from AI identity |
| Core Meeting connectors | OpenAI/Anthropic provider-call source | Main HTTP runtime wiring, Work Assignment context, provider receipt/request ID and assignment/dispatch correlation; current v2 runner path uses MockConnector |
| W52 orchestration | Sandbox Codex App Server + Qwen ACP read-only/no-tool candidate | Canonical source mapping, live provider invocation, target/session authentication, delivery receipt, cancel/recovery |
| W14 transport | Existing Host/Execution Host source | Compatible bidirectional HostPort/RpcPort binding within W14 boundary; one-shot /execute or pytest grant is not provider delivery |
| W33 evidence | Offline CLI-first hash-addressed store | Authenticated durable ingress/read/version/retention and Assignment/event/source provenance binding |
| W112 compatibility | DOC-001 assignment/event/evidence schema baseline | Independent review + owner approval; mapping into existing APIs, no duplicate bus/store |
| Ka/Cla review delivery | Review packets prepared | Supported authenticated agent-message delivery route and separate reviewer ACK |

Minimum E2 proof: trusted provider/adapter receipt for actual delivery to intended session, bound to assignment_id + dispatch_id + attempt_id + target/session + correlation/idempotency + timestamp + source/payload digest. HTTP acceptance alone is insufficient.

Minimum E3 proof: authenticated receiving AI response or explicitly lower-assurance manual receipt, bound to same assignment/dispatch/attempt, with decision, accepted-scope digest, ack_ref, timestamp and provenance. No response means no ACK. Host execution result, Meeting transcript paste or human-entered AI name is not provider ACK.

Architecture direction: existing ownership boundaries contain reusable fragments, but full-chain proof is missing at trust-boundary bindings. Reuse W70/Core/W52/W14/W33/W112; do not create a parallel dispatcher, identity registry, queue, event bus or evidence store. GAP-01 remains OPEN/P0; E2/E3 NOT PROVEN; READ/TRACE ONLY; protected execution DENY / NOT RELEASED. This matrix is not BUILD approval.
