# W122 — Core / W52 / W14 Integration Gap Matrix
**ID:** INT-GAP-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Prepared by:** Xu / AI-01 | **Decision authority:** Vinh
**Status:** READ-TRACE ASSESSMENT — NO INTEGRATION AUTHORIZED
**Related:** W122 Architecture Intake §§18–19; G2-CHECK-W122-001; W17 GAP-01; W112 DOC-001; W113 Discover Brief

> This is a source-level contract comparison, not a live runtime test. A documented boundary or historical attestation is not proof of a currently deployed, authorized service.

## 1. Executive finding
W122 should not implement its own identity, authorization, event store, task dispatcher or process host to bypass missing ROOM-HOP contracts. The inspected evidence points to a clean ownership split:
- Core owns authenticated identity, tenant/membership, policy/authorization decisions, canonical message/event identity, correlation, persistence and deduplication.
- W52 owns provider-neutral A2A orchestration and task/event mapping, but its v0.1 candidate remains DRAFT/NOT RELEASED and its production ports are injected interfaces.
- W14 owns the consolidated execution Host. Its boundary is not interchangeable with W52 HostPort/RpcPort without an explicit adapter and safety proof.
- W122 owns the email domain: provider adapter, mailbox/message normalization, analysis, local draft workflow, approvals as a domain feature, and Gmail-specific reconciliation—subject to Core authority and approved host contracts.

**Decision recommendation:** W122 remains a domain product and must consume approved Core/W52/W14 contracts; it must not become a parallel ROOM-HOP platform.

## 2. Ownership and evidence matrix
| Boundary | Canonical responsibility | Evidence observed | Status for W122 | Required proof |
|---|---|---|---|---|
| Core identity and tenant | Authenticate principal; resolve tenant/member; bind mailbox owner/delegation | W11 production boundary summarized in W122 Architecture Intake §19.2; W113 Discover says source-level Core contracts unreadable in inspected connector | NOT EVIDENCED as callable approved contract | Versioned Core API/schema, service owner, auth mechanism, tenant/mailbox binding and negative tests |
| Core authorization/policy | Server-side action decision; scope/policy version; deny-by-default | W01/W02 source components exist, but source presence does not prove live endpoint or production wiring (W113 Discover) | NOT EVIDENCED at runtime | Approved policy contract, principal propagation, scope/action checks, revocation and audit proof |
| Core persistence/audit | Canonical IDs, correlation, dedupe, durable events and tamper-evident audit | W11 boundary assigns message/event identity, correlation, persistence and deduplication to Core; W122 intake says audit contract not evidenced | NOT EVIDENCED | Durable event/audit interface, idempotency semantics, retention and read-back evidence |
| W52 A2A contract | Provider-neutral task/event orchestration and state mapping | W52 v0.1 contract/event model DRAFT; schemas lack typed Assignment/Dispatch/Attempt/DeliveryReceipt/Recipient ACK and enforced ACK state (W17 GAP-01 Entries 035–038) | PARTIAL DESIGN ONLY | Owner-approved versioned schema and loss-aware mapping to W70/W112 |
| W52 engine lifecycle | ACCEPTED/RUNNING must represent actual recipient/session lifecycle accurately | W17 GAP-01 Entry 034 records ACCEPTED before Host.open and RUNNING before provider handshake; no authenticated recipient ACK bound to assignment/dispatch/attempt/session | NOT PROVEN | Corrected lifecycle and authenticated ACK evidence before any possible Host side effect |
| W52 CorePort/AuthorityPort | Bind orchestration to real Core identity and policy | Candidate ports are injected Protocols; no production implementations in inspected candidate (W17 GAP-01 Entry 036) | NOT IMPLEMENTED IN CANDIDATE | Core-owned concrete adapter, contract tests against real Core and runtime read-back |
| W14 HostPort/RpcPort | Own provider process/session, streams, isolation, cancellation and descendant shutdown | W17 GAP-01 Entry 039 says W52 HostPort requires long-lived bidirectional RpcPort; inspected W14 POST /execute is one-shot HTTP subprocess execution; no direct binding found | INCOMPATIBLE / NOT PROVEN | W14-owned adapter or explicit redesign; process isolation, cancellation, stop confirmation, audit and no-side-effect-before-ACK proof |
| Current 8030 surface | Expose authorized Work operations | W12 boundary and W113 Discover/Architecture say current surface exposes Sandbox file APIs, not Work Host/process/Git/CI/browser adapters or typed private dispatch/receipt/ACK | NOT AVAILABLE THROUGH INSPECTED SURFACE | Newly exposed approved API with exact schema, permission and runtime verification |
| W122 email domain | Gmail adapter, normalization, analysis, local drafts, mailbox-specific reconciliation | W122 Architecture Intake §§10–19 and security/state-machine drafts | DESIGN PROPOSAL | G2 approval, Core contract, provider scope decision, independent review and later G3 |

## 3. Critical technical gaps
### INT-01 — Core authority is not a callable, evidenced contract
W122 needs an authoritative identity and policy decision before mailbox data can be read or any side effect can occur. W01/W02 code artifacts or role labels are insufficient. No endpoint should be guessed. Do not create a second W122 user/tenant registry.

### INT-02 — W52 v0.1 does not prove delivery or recipient acceptance
W17 GAP-01 Entries 035–038 report missing typed assignment/dispatch/attempt, delivery receipt, recipient identity proof and ACK event/state. The inspected engine lifecycle can mark ACCEPTED/RUNNING before provider session acceptance. Reuse W112 DOC-001's loss-aware mapping and ACK-before-Host.open semantics as a reference; do not duplicate or silently patch W52 v0.1 from W122.

### INT-03 — W52 HostPort and W14 execution endpoint are different contracts
W52 expects HostPort.open(adapter, task) returning a persistent bidirectional RpcPort with request/notify/receive/respond/close. The inspected W14 POST /execute is a one-shot WorkContext + ExecutionRequest call returning a completed result. They are not drop-in compatible. W14 owner must decide whether to implement a compatible adapter or version the W52 Host contract.

### INT-04 — Current 8030 capability is not an execution substrate
The inspected ROOM-HOP tool surface exposes Sandbox file operations and meeting-scoped actions, not process manager, Work Host, Git gateway, CI, browser agent or authenticated private task delivery. Sandbox write/read evidence is not agent dispatch or production execution proof.

### INT-05 — Evidence age and source scope matter
W17 GAP-01 is a historical source trace dated 2026-11-19; W113 Discover records a scoped inspected environment and historical W14 attestation. Treat them as leads and known design gaps, not proof that every deployment today is unavailable. Recheck exact current source SHA/runtime only when an approved read-only path and owner are available.

## 4. Recommended integration sequence (proposal only)
1. Core owner publishes versioned identity/tenant/mailbox-owner, policy decision, event persistence, audit and idempotency contracts.
2. W70 confirms Work Assignment/readiness lifecycle and authority boundary.
3. W52 publishes a versioned compatible A2A schema carrying Assignment, Dispatch, Attempt, delivery receipt and authenticated recipient ACK, preserving state distinctions and W112 loss-aware mapping.
4. W14 owner defines HostPort/RpcPort compatibility or a versioned alternative, including isolation, cancellation, process lifecycle, side-effect semantics and durable run evidence.
5. Enforce recipient-authenticated ACK before Host.open or any possible external side effect; prove with negative tests.
6. Independent Ka/QE review and authorized live E2E on exact source SHA; no self-attestation.
7. Only after these contracts and W122 G2 approval, prepare a separate W122 G3 build proposal.

## 5. Reuse boundaries
- Reuse W112 DOC-001 Addenda 11.1–11.13 as the existing cross-Work mapping and ACK semantics reference; do not create a parallel A2A master spec inside W122.
- Preserve W52 v0.1 candidate unchanged until its owner-approved version decision; no opportunistic edits from W122.
- Do not treat W14 one-shot /execute as an interactive provider RPC transport.
- Do not call guessed Core/Gateway/Event Listener/Agent Runtime routes.
- Do not use the retired meeting relay as a private task dispatch mechanism.
- W122 may continue provider-neutral email domain design and synthetic fixture planning without runtime integration.

## 6. Required evidence checklist
- [ ] Core API/schema version, owner, authentication and principal/tenant propagation.
- [ ] Mailbox owner/delegation and tenant isolation policy.
- [ ] Core policy decision and revocation semantics.
- [ ] Durable event/audit interface, idempotency and read-back.
- [ ] W70 Assignment/readiness lifecycle mapping.
- [ ] W52 typed dispatch/attempt/delivery receipt/recipient ACK schema and runtime evidence.
- [ ] W14 Host contract, isolation, cancellation and process-stop evidence.
- [ ] ACK-before-side-effect negative test.
- [ ] Exact source SHA/config and deployed runtime attestation.
- [ ] Independent Ka/QE verdict and canonical Owner decision.

## 7. Current truth
- This is Xu's read-trace draft; no live Core/W52/W14 endpoint was called.
- Core approved callable identity/policy/audit contract: NOT EVIDENCED.
- W52 v0.1: DRAFT / NOT RELEASED; delivery receipt and recipient ACK gate NOT PROVEN in cited trace.
- W52↔W14 HostPort/RpcPort binding: NOT PROVEN.
- Current 8030 inspected surface: no Work Host or typed private dispatch/ACK capability evidenced.
- G2: NOT READY / NOT APPROVED.
- G3: BUILD NOT AUTHORIZED.
- No source/runtime changes in W01/W02/W11/W12/W14/W52/W70/W112; W120/W121 untouched.
- No Gmail OAuth, mailbox read, Gmail draft, send, paid commitment or test execution.
