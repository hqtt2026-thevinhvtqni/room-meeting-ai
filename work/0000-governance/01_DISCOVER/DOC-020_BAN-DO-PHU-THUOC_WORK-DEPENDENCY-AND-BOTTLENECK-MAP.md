# DOC-020 — BẢN ĐỒ PHỤ THUỘC VÀ ĐIỂM NGHẼN DANH MỤC WORK / COMPANY WORK DEPENDENCY & BOTTLENECK MAP

- Document ID: DOC-020 | Priority: P0 | Read order: 20
- Status: ACTIVE — DISCOVERY MAP / DEPENDENCIES PARTLY VERIFIED
- Version: 1.0 | Updated: 2026-11-03
- Owner: Work 0000 / HQTT Company Governance
- Governing standard: Work 70 lifecycle, document, assignment and gate standards.
- Evidence boundary: Manifest, architecture/contract documents, source-review reports and registry snapshots. This is not runtime, integration, test or release evidence.

## 1. Purpose and authority
This document maps cross-Work dependencies, ownership boundaries and delivery blockers for portfolio coordination. Work 0000 tracks the relationships; it does not take ownership of member Work source, implementation, gates or release. Work 70 remains the mandatory lifecycle and delivery standard. Each member Work remains authoritative for its own product records and evidence. Vinh retains final authority.

Dependency labels:
- CONFIRMED-DOCUMENTED: explicit relationship in a read Manifest or controlled document.
- DECLARED / NOT VERIFIED: stated relationship, but implementation or operational connection not proven.
- CANDIDATE: plausible capability relationship requiring owner/contract confirmation.
- CONFLICT: documents contain incompatible or stale references requiring controlled reconciliation.
- BLOCKED: a prerequisite currently prevents the downstream activity.

## 2. High-confidence dependency map

| Upstream | Downstream | Relationship | Evidence / current limit |
|---|---|---|---|
| Work 70 | All Works | Mandatory lifecycle, documentation, assignment, evidence and gate standard | Founder-confirmed D0000-002; Work 71 Manifest explicitly adopts W70. This is governance dependency, not code dependency. |
| Work 12 + Work 13 | Work 14 | Historical execution-environment and execution-host foundations absorbed by W14 | W12 Manifest COMPLETED+LOCKED; W13 Manifest COMPLETED+LOCKED+ABSORBED_BY_W14; W14 is sole future product/delivery/release owner. Does not prove W14 E2E/release. |
| Work 09 / Work 091 | Work 14 | Browser adapter / browser workflow engine provider relationship | W14 Manifest declares provider relationship; exact Work-ID mapping, API contract and runtime acceptance remain to verify. |
| Work 27 | Work 32 | Shared sandbox execution runtime dependency | W32 Manifest declares W27 dependency; W27 runtime/E2E acceptance is NOT VERIFIED. W32 live execution remains BLOCKED. |
| Work 32 | Work 51 | CI/test execution capability consumed by coder-tester workflow | W32 Manifest identifies W51 as consumer; W32 live execution BLOCKED, so W51 end-to-end operation is not established. |
| Work 37 | Work 28 / Work 39 | Core source-of-truth and Build MCP integration boundary | W37 owns Core scope; W28 integration blocked; W39 owns 8030 service/tooling scope. Core owner/API/auth/persistence and live integration remain NOT VERIFIED. |
| Work 38 | Work 28 / Work 39 | Gateway 8040 service boundary and possible routing integration | W38 Manifest says service/runtime unknown and GitHub mirror not verified; relationship is architectural boundary only, not live integration. |
| Work 39 | Work 28 | 8030 service/tooling implementation and operational contract | W39 ACTIVE; listing shows code/test/evidence zones but no proof of live 8030 acceptance from listing alone. Work 28 remains integration blocked. |
| Work 91 | Work 99 | W91 registration requirement in W99 Work Index | W99 WORK_INDEX.md contains W91 row; registration CONFIRMED. W99 runtime Entry Gate enforcement remains NOT VERIFIED. |
| Work 70 DOC-064/065/066 | Work 0000 portfolio / future dispatch capability | Target Hybrid AI Dispatch architecture, logical contract and implementation/test plan | All design-only; DOC-072 confirms no Core Work/Assignment/Evidence API, authoritative persistence or Core owner identified in inspected scope; no dispatch or ACK executed. |
| Work 50 APDS | Work 70 | Proposed engineering/product-delivery extension | APDS v1.0 is PROPOSED; APDS-01..23 CHƯA XÁC MINH. Work 70 remains lifecycle/delivery standard; APDS must not create parallel lifecycle. |
| Work 103 | Work 28 / Core | RAG retrieval runtime and integration dependency | W103 Manifest contains stale :8020 architecture reference; policy conflict with current no-use boundary. Actual runtime routing/integration not verified. Do not use :8020. |
| Work 101 | Work 27 / Workspace sync | Dual-workspace runtime/sync dependency | W101 Manifest: DRY_RUN, target unbound, parity and adapter E2E not verified; W27 dependency declared. |
| Work 104 | Work 0000 / portfolio evidence | AI usage evidence tracking candidate | W104 ACTIVE; files/schema listed, but runtime ingestion and integration not verified. |
| Work 111 | Work 14 / E2E source lifecycle | E2E source snapshot process candidate | W111 ACTIVE; process/build/evidence files listed; integration with W14 not verified. |
| Work 33 | Work 50 / Work 0000 | Shared evidence hub candidate | Candidate capability only; no integration or current runtime/test acceptance verified. |
| Work 23 | AI provider integration consumers | Gemini provider adapter candidate | W23 ACTIVE; Kha receipt/acceptance and real API E2E not verified. |
| Work 092 | Browser UX / W09 / W14 | Static browser prototype candidate | Two Manifest/status records conflict; DONE/PASS T1-T17 claim is limited to static mock scope, not real browser/runtime. Identity/status reconciliation required. |
| Work 200 | Portfolio | Registry anomaly | Canonical Manifest unresolved; remains UNASSESSED. |

## 3. Critical bottlenecks and order of resolution

### P0 — Core authority and authorization boundary
- DOC-071 / DOC-072 report no identified accountable Core owner in inspected repository metadata/search scope.
- Work/WP/Assignment/Evidence APIs, authoritative persistence, authorization middleware and commit-time enforcement are NOT VERIFIED.
- DOC-063 remains design-only; protected mutation/recovery separation and commit-time authorization are NOT IMPLEMENTED / NOT VERIFIED.
- Consequence: no new authoritative assignment API, shadow database, Core mutation or dispatch implementation may be assumed or introduced.

### P0 — Work 70 lifecycle gate
- DOC-072 records G0/G1 NOT_READY and lifecycle G4 NOT_READY / NOT PASS; BUILD NOT AUTHORIZED.
- DOC-064/065/066 do not override DOC-004, DOC-057 or the Work Entry gate.
- Consequence: continue read-only discovery, contract reconciliation and test design only; no code build based solely on the dispatch proposal.

### P1 — AI dispatch capability
- DOC-043 says roster identity does not prove online, connected or capable.
- DOC-066 says 8030 toolset inspected does not expose direct dispatch to private AI conversations.
- SESSION_HANDOFF remains a user-mediated candidate; creating a packet is not delivery, and a typed AI ID is not verified ACK.
- No private ChatGPT conversation dispatch, provider connector capability, delivery, ACK or token usage is proven.
- Consequence: no assignment may be labelled DISPATCHED/DELIVERED/ACKNOWLEDGED without the corresponding evidence.

### P1 — Execution and browser chain
- W14 is sole owner for W12/W13 consolidation but real Chromium E2E and release remain unproven.
- W27 runtime/E2E is unverified; W32 live execution blocked; W51 consumes W32 capability.
- W09/W091-to-W14 exact interface contract remains open.
- Consequence: do not report coder-tester or E2E chain operational based on source/listing alone.

### P1 — Legacy route and identity/data quality
- Stale :8020 references exist in W103, W99, W15, W30, W101, W96, W37 and other historical docs. They are documentation conflicts only; do not call or route to :8020.
- W092 has conflicting manifests/status; W200 unresolved; Work 99 historical counts 39/53 are stale against current registry count 56.
- Consequence: controlled document corrections and identity reconciliation; no renaming/deletion by inference.

## 4. Recommended execution sequence (read-only until gates authorize build)
1. Identify accountable Core owner and obtain the current source baseline, runtime entrypoint, Work/WP/Assignment/Evidence API, auth, persistence/audit and test contract.
2. Have Ka independently review DOC-061/063/064/065/072 reconciliation; review must not be represented as approval.
3. Have Vi produce bounded source-path/symbol evidence only when a new baseline or accountable owner handoff is available; do not repeat old source traces without new evidence.
4. Have An/Qw prepare independent negative/race/idempotency/authorization test design; distinguish design from executed tests.
5. Reconcile W09/W091/W14 and W27/W32/W51 interface ownership with source and owner evidence.
6. Keep AI Dispatch in design-only status until G0/G1/G4, Core owner, authorization contract and Work Entry conditions are satisfied.
7. After explicit authorization, pilot one non-sensitive SESSION_HANDOFF assignment with manual receipt; never describe it as automated private-session dispatch.
8. Correct stale :8020 documentation through controlled changes only; do not probe, restart, activate or route traffic to that listener.

## 5. Portfolio action table

| Work | Portfolio disposition | Next accountable action |
|---|---|---|
| 14 | ACTIVE / E2E and release unverified | W14 owner to close real browser/execution/security/review evidence |
| 27 | ACTIVE / runtime unverified | Establish actual isolated runtime and acceptance evidence |
| 28 | ACTIVE / INTEGRATION BLOCKED / Gate CLOSED | Resolve 8030 provenance and runtime/registry alignment within W28 scope |
| 32 | LIVE EXECUTION BLOCKED | Resolve W27 runtime prerequisite and authorized CI execution path |
| 37 | OPEN / source and owner trace incomplete | Identify Core owner and authoritative service boundary |
| 38 | CREATED / runtime unknown | Establish 8040 source/runtime evidence under its own authority |
| 39 | ACTIVE / live acceptance unverified | Prove 8030 service/tool contract without altering running service absent authorization |
| 50 | APDS PROPOSED | Crosswalk with W70; do not activate parallel lifecycle |
| 70 | Governing standard / dispatch design only | Preserve DOC-064/065/066/072 as design artifacts until gates authorize |
| 91 | Registered in W99 | Continue audit against existing harness; no parallel harness |
| 99 | ACTIVE / runtime gate NOT VERIFIED | Prove server-side entry gate and bypass-resistant E2E |
| 101 | DRY_RUN / parity not verified | Bind target and prove adapter/sync/recovery only after authorization |
| 103 | ACTIVE / runtime integration unverified | Reconcile stale route text against no-use boundary before execution |
| 104 | ACTIVE / integration unverified | Establish actual evidence ingestion and provenance |
| 111 | ACTIVE / integration unverified | Map snapshot process to canonical E2E owner and evidence contract |

## 6. Evidence and limitations
Sources read in this review:
- Work 70 DOC-043, DOC-044, DOC-061, DOC-064, DOC-065, DOC-066 and DOC-072.
- Work 0000 DOC-018, DOC-003 and DASHBOARD/PRODUCT_STATUS.json.
- Individual Work Manifests and listings summarized in DOC-018, including W09, W091, W12, W13, W14, W27, W28, W32, W37-W40, W50, W51, W91, W99, W101, W103, W104 and W111.

Limitations:
- Manifest/listing presence does not prove code, test, runtime, security, integration or release.
- DOC-072 is bounded source/document reconciliation, not exhaustive proof that no Core owner or service exists outside inspected surfaces.
- No member Work source, configuration, service, permission, gate or GitHub branch was changed.
- No test was run and no dispatch/ACK was executed in this portfolio mapping.
- GitHub synchronization of Work 0000 remains NOT VERIFIED.

## 7. Final status
- Dependency map: DONE — DOCUMENTED DISCOVERY BASELINE.
- Confirmed operational integrations: NOT ESTABLISHED by this map.
- Core owner/API/auth/persistence: BLOCKED / NOT VERIFIED.
- AI private-session dispatch: NOT AVAILABLE / NOT PROVEN in inspected 8030 toolset.
- Work 70 G0/G1/G4 and BUILD: NOT READY / NOT AUTHORIZED.
- Member Work modifications: NONE.
- GitHub sync: NOT VERIFIED.


## 2026-11-09 — ROOM-HOP unified-machine dependency update (design baseline)
- W70 is the central control plane and system-level authority for Work lifecycle, assignment, gates, decisions and dashboard projections.
- W112 depends on W70 contracts and coordinates cross-boundary integration only; it is not a second lifecycle engine.
- W32 provides shared CI/test capability; W33 evidence storage; W52 AI communication/orchestration; W16 workflow execution; W51 coder-tester orchestration; W14 execution-host integration; W37 Core 8000; W38 Gateway 8040; W39 Build MCP 8030; W0000 governance registry; W21 Agent skills.
- Parallel development is contract-first. Each component owner retains implementation authority for its component. Integration is allowed incrementally when contracts and test/evidence interfaces are ready.
- All dependencies remain DESIGN / NEEDS DIRECT CONTRACT AND RUNTIME VERIFICATION unless their specific evidence proves otherwise. This map does not imply live integration or PASS.
