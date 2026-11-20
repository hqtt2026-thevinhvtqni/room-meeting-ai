# W113 DISCOVER BRIEF
- Document ID: DOC-006 | Priority: P1 | Read order: 6
- Version: 1.1
- Updated: 2026-11-13 04:59 (+07)
- Status: DRAFT — DISCOVERY IN PROGRESS
- Date opened: 2026-11-09 | Product Owner: Vinh | Orchestrator: Xu

## Problem
ROOM-HOP has distinct Company, Sandbox and Meeting spaces, but lacks an identified unified user-facing control surface that lets authorized humans and AI participants understand and navigate the whole system across Web and Mobile.

## Users
- Human: Product Owner, company/Work operators, reviewers and members, according to assigned permissions.
- AI: Xu/orchestrator, architects, coders, QE and other registered agents, each restricted to role and assignment scope.
- Exact role catalogue and authorization claims: to be discovered from authoritative identity and permission services.

## Product hypothesis
One responsive Dashboard can present a unified global overview and role-adaptive views across Company, Sandbox, Meeting and system control, while leaving authoritative data and actions with owning services.

## Existing scope initially inspected (2026-11-09)
- W0000: Company governance and portfolio dashboard snapshot; README says read-only projection and explicitly not live/portfolio-wide release certificate.
- W70: mandatory Work lifecycle and Work Dashboard/Product Dashboard distinction; DOC-085 forbids conflating Work and Product dashboards.
- W71: next-generation Meeting product; separate scope.
- Work inventory: 61 entries returned by ROOM-HOP 8030 at initial inspection. Inventory snapshot DOC-018 in W0000 was dated 2026-11-03, 56 entries, explicitly not fully reconciled.
- Full 61-Work product-scope audit: NOT COMPLETED.

## Discovery addendum — 2026-11-13

### 1. FACT — current Work inventory and governance boundaries
- ROOM-HOP 8030 sandbox_list_works returned 64 Works on 2026-11-13. This is a current Sandbox registry count, not a full product-scope audit; several entries have generic/legacy names and need reconciliation.
- W70 DOC-085 explicitly separates each Work's Work Dashboard (execution/lifecycle progress) from its Product Dashboard (the product's own user-facing experience). W113 therefore has two distinct deliverables:
  1. W113 Work Dashboard: tracks W113's own lifecycle, WP, gates, decisions, blockers and evidence; its canonical W0 projection is DASHBOARD/ and DOC-012.
  2. W113 Product Dashboard: the ROOM-HOP Universal Dashboard product for Global Home, Company, Sandbox/Works, Meeting and Control Center.
  These are not two competing universal product dashboards and must not be merged into one responsibility.
- W70 DOC-042/DOC-043/DOC-096 are active operating standards for assignment governance, role/capability verification, independent review, session integrity and append-only journaling. Roster labels do not prove online status, capability, session reachability, authorization or participation.
- W70 DOC-064/DOC-065 describe Hybrid AI Dispatch and its contract as DRAFT / NOT IMPLEMENTATION APPROVED. W70 DOC-068 records that the dispatch design does not prove adapter/Core API/private-session dispatch and that the current MCP 8030 surface has no direct private-conversation dispatch tool.
- W01 08_DASHBOARD/README.md reserves an operational dashboard for actual runtime/API state and explicitly forbids claiming a dashboard implementation from file presence or preview data.

### 2. FACT — collaboration and integration Works inspected
- W52 (ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION):
  - Provider-neutral A2A task/event contract v0.1 and state machine are DRAFT.
  - The contract distinguishes runtime SUCCEEDED from independent VERDICT_RECORDED PASS.
  - Capability matrix reports live Codex/Qwen CLI absent in the specific inspected environment; Core authoritative dispatch/identity ACK is BLOCKED in that measured profile. This does not prove provider unavailability on every machine.
  - Permission, retry, timeout and cancellation documents are design proposals; some numeric timing values are explicitly unverified.
  - W52's own charter says no E2E evidence and not released.
- W112 (ROOM-HOP-INTEGRATION-CONTRACTS-AND-EVIDENCE-ORCHESTRATION):
  - Integration Charter assigns cross-Work contract definitions/correlation to W112 while component owners retain their runtimes.
  - Cross-Work Integration Contract Baseline DOC-001 is DRAFT — DESIGN BASELINE; NOT APPROVED FOR RUNTIME ENFORCEMENT.
  - Event transport, live assignment/ACK API, evidence object store, lock/lease provider and live authorization enforcement are NOT DECIDED / NOT VERIFIED in the inspected baseline.
- W114 (ROOM-HOP-GRAPH-INTELLIGENCE-ARCHITECTURE):
  - ADRP-114-001 is DESIGN ONLY / NOT APPROVED FOR IMPLEMENTATION.
  - W114 explicitly defines Graph Intelligence as read-only decision support, not a dispatcher, task queue, identity authority, permission engine or execution host.
  - W114's Dispatch Capability Matrix reports: native connector NOT CONFIGURED / NOT VERIFIED; session handoff may prepare a packet but no target transfer/receipt is proven; Meeting relay tools are available only in meeting scope and do not prove private delivery or ACK; API adapter NOT CONFIGURED / NOT APPROVED; automated dispatch BLOCKED.
  - W114's Agent Task Bridge Contract states the current 8030 tool surface has Meeting and Sandbox actions, not typed Work task dispatch, private-session inbox, delivery receipt or authenticated ACK.
- W11 (AI-MEMBER-ADAPTER):
  - Member Contract v0.1 defines provider-neutral identity/transport/capability/connect/health/send/receive/disconnect/evidence fields.
  - Production Integration Boundary says source-level Core service contracts are not readable through the inspected connector; no guessed calls should be added. Membership is not authorization.
- W01 Gateway source contains boundary components for identity resolution, authentication, authorization, session management and principal context, but source presence alone does not verify a live endpoint or production wiring.
- W02 README identifies W02 as owner of unified authorization for MCP Meeting and MCP Build; the inspected README does not prove the runtime API or its current enforcement.
- W71 Product Architecture remains DRAFT — INITIAL ARCHITECTURE PRINCIPLES. Meeting is a separate product/domain; W113 should integrate through owner contracts, not reimplement Meeting lifecycle or media.

### 3. FACT — current Dashboard source candidate inspected
- GitHub repository hqtt2026-thevinhvtqni/PL.room-meeting-ai.dash exists; default branch main at commit dc4be09bc43c02630f60eb892782e72a07c782b8. Repository metadata reports code search index unavailable.
- Its README describes it as UI/Contract Lab and locks a Meeting Session Lifecycle Contract v0.1. It is a Meeting/session UI lab, not evidence of a complete ROOM-HOP Universal Dashboard.
- The inspected code has bridge/RoomHOPBridge.ts selecting mockBridge by default unless NEXT_PUBLIC_DASH_MODE=real; dashboard/Dashboard.tsx renders a Meeting SessionView. The real bridge code calls Core :8000 and Workspace :8010 with browser-side fetch. This requires a security/contract review before any reuse; the README's intended Dashboard → Bridge → Application Service sequence is not itself proof the implementation satisfies that boundary.
- GATE2-README.md and GATE4-README.md describe expected mock/real steps and endpoints; these instructions are not evidence that real endpoints are deployed or that Gate 4 passed.
- No tests were run during this read-only source inspection. No product source adoption decision is made.

### 4. FACT — W113 records and GitHub parity
- W113 DOC-013 remains NOT ASSESSED; G0–G5 are NOT ASSESSED; product source is NOT DECLARED; API/runtime contracts are NOT VERIFIED; UI/E2E/QE are NOT STARTED/NOT RUN; acceptance/release are NOT AUTHORIZED.
- W113 Sandbox DOC-009 v2.0 was written and read back successfully on 2026-11-12. This proves Sandbox persistence only.
- GitHub room-meeting-ai main was observed at 3e2140cd573497142ff8b4b457fcd6779c14123c. Its W113 04_PLAN/IMPLEMENTATION-ROADMAP.md is still the older DRAFT roadmap (blob SHA d592e79390b37a31db48406583e4b61a315d4dd9), not the Sandbox DOC-009 v2.0. Therefore Sandbox ↔ GitHub parity for the approved plan is NOT VERIFIED / currently divergent.
- ROOM-HOP Build MCP context says Working Source is read-only and AI cannot commit, push or merge. The current 8030 tool surface exposes Sandbox read/write, not a GitHub sync action. No GitHub write was attempted.

### 5. FACT — AI consultation status in W113 records
- Co / AI-07 has a substantive consultation recorded in DOC-015 and DOC-016; it is a recommendation, not an approved architecture decision.
- Mê supplied a substantive independent architecture assessment in the conversation. Xu reviewed it as consultation input; it is not yet registered as a canonical W113 evidence artifact in this discovery addendum.
- The W113 journal records a Kha-labelled submission that contained the consultation scope/brief, not a substantive architecture response.
- No substantive W113 architecture review or authenticated ACK from Ka, Cla, Qw or Go was located in the canonical W113 records inspected for this pass. This is NOT evidence that those agents are unavailable; their participation is unverified.
- No current tool exposed a typed agent-task dispatch/private-session delivery/authenticated recipient ACK action. Creating a Sandbox packet or posting a Meeting message cannot be represented as delivery or ACK.

### 6. ASSUMPTION — not accepted as fact
- Candidate ownership of the universal product source by PL.room-meeting-ai.dash.
- Availability of live Core, Gateway, Workspace, identity/authorization or Agent Runtime APIs for W113.
- Any provider's ability to continue or dispatch into a currently active private AI conversation.
- That an AI roster entry or a meeting participant alias is an authenticated principal.
- That W52/W112/W114 draft contracts are implemented or approved for runtime use.

### 7. BLOCKED / discovery conditions
1. Product source ownership: no canonical W113 Product Dashboard repository/path has been approved.
2. Integration contracts: no verified API/Bridge contract and source owner/revision for Company, Sandbox, Meeting, Core, identity/authorization and system health.
3. Multi-AI delivery: no verified native connector or authenticated private-session dispatch/receipt/ACK path in the current tool surface.
4. Authority: no verified end-to-end Core grant, Host enforcement, revocation and Run Record contract for Dashboard actions.
5. Evidence: W112/W52 contracts remain draft; no durable live event/evidence/lease implementation is established by the inspected files.
6. Consultation: independent reviews from all requested AI reviewers are not present in canonical W113 records.
7. Repository parity: Sandbox plan v2.0 and GitHub main roadmap differ; current 8030 boundary does not authorize AI commit/push.
8. Work Dashboard vs Product Dashboard: retain separate W70 responsibilities in all requirements and UI navigation.

## Discovery questions (remaining)
1. What are the verified APIs/contracts and authorization boundaries for Company, Sandbox, Meeting, Core and system health?
2. What is the canonical identity/role/permission source for humans and AI, and what evidence proves its runtime enforcement?
3. Which operations are read-only and which commands can be safely delegated to domain services?
4. What are the supported Web/Mobile delivery targets and browser/device baselines?
5. What freshness, offline, notification and audit guarantees are available?
6. Which existing screens/components can be reused without duplicating domain ownership?
7. What is the approved canonical Product Dashboard source repository/path, and how is it separated from W113's own Work Dashboard?
8. Which approved dispatch contract supports existing AI sessions, authenticated receipt/ACK, timeout/retry and recovery?

## Discovery exit criteria
P1 remains IN PROGRESS. Exit only after:
- scoped source/service inventory and owner map are reconciled;
- product source candidate is accepted/rejected through owner decision;
- data/action ownership and API/Bridge contracts are evidenced, or explicit BLOCKED conditions are accepted;
- current W52/W112/W114 and W70 dispatch/lifecycle boundaries are reconciled;
- consultation comparison distinguishes substantive opinions, scope-only submissions and missing reviews;
- Work Dashboard and Product Dashboard responsibilities are separated;
- GitHub/Sandbox source-of-truth and authorized sync path are resolved;
- evidence register and journal contain reproducible references.

No implementation, source mutation, deployment, migration or release is authorized by this discovery update.


## Discovery addendum 2 — execution, Core, Gateway and identity ownership (2026-11-13)

### FACT — additional owner Works inspected
- W14 is the declared sole product/delivery/release owner for the Autonomous E2E Builder consolidation; W12/W13 are absorbed foundations, not separate parallel host products.
- W14's absorbed Execution Host Boundary states that only the ROOM-HOP Sandbox file API is exposed through the current room-hop MCP surface. No executable Work Host, process manager, Git gateway, CI adapter or WorkContext-bound browser adapter is available through that surface. Therefore W113 cannot assume it can run commands or obtain authoritative Run Records through the current 8030 connection.
- W14 Manifest reports a PC attestation for /health and POST /execute on 2026-10-12, but also says the complete UI → canonical Host → Browser Agent → real Chromium → verified artifact/E2E flow is not proven and security/release review remains open. This historical attestation is not current W113 runtime evidence.
- W37 is the evidence workspace for the single Core :8000, not a second Core. Its scope document records Core as the intended source of truth, but explicitly lists process entrypoint, routers, endpoint schemas, application services, persistence, authentication/authorization and health behavior as items still requiring source verification. W37 states its own initialization does not prove live Core connectivity or mirror completeness.
- W38 Gateway Work Manifest remains CREATED; technical audit is not started and live service status is UNKNOWN / NOT VERIFIED. Its Sandbox mirror role says Work 38 is an investigation/evidence area, not a duplicate Gateway.
- W39 is the separate Work for MCP 8030 build tools/service. The current 8030 tool inventory and room context confirm Sandbox file operations and meeting-scoped tools; they do not expose a typed task-dispatch/private-session delivery/ACK interface.
- W21 AI-SKILLS defines Skill as capability/procedure, not Model or Tool; its Skill Contract explicitly says a Skill does not grant authority. W21 Manifest says Core integration is NOT VERIFIED and independent QE is pending. W21 must not be treated as the task registry or authorization service.
- W0000 DOC-010 says W70 is the operational roster reference, but its displayed table maps AI-06 to Qc, AI-07 to Go and AI-08 to Co. W70 DOC-043 maps AI-06 to Go and AI-07 to Co, while Qc is separately listed without those AI IDs. This is a roster/document discrepancy requiring W0000/W70 reconciliation; do not assign by the conflicting W0000 AI-ID rows until resolved.
- W0000 DOC-018 is a 2026-11-03 snapshot of 56 Works and says it is not fully reconciled. The current 8030 registry returned 64 Works on 2026-11-13. This is a registry-count difference, not proof that all 64 Works have valid current manifests or product scope.

### Impact on W113
1. Core, Gateway, Execution Host, identity and authorization remain external authorities; W113 must consume verified owner contracts and cannot replace them.
2. No live command, run, dispatch or permission-changing action should be enabled in the Dashboard until the relevant owning service demonstrates authenticated server-side enforcement, audit, scope and revocation.
3. Current 8030 access supports document discovery and recording, not full AI execution orchestration. Do not treat file writes, meeting posts or role labels as task delivery or ACK.
4. AI identity and reviewer assignment must use the current W70 operational roster plus authenticated session/capability evidence; the W0000 roster mismatch must be resolved before formal multi-AI assignment.
5. The 64-versus-56 registry discrepancy must be reconciled by W0000; W113 uses the live registry count as a timestamped observation only.

### Remaining blockers (additions)
- Core :8000 source/API/runtime and auth enforcement not verified through W37.
- Gateway :8040 live service/API status not verified through W38.
- Execution Host :8031 callable boundary, permission grants, revocation and Run Record not available through current 8030 tool surface; W14 historical attestation does not close this.
- AI roster AI-ID discrepancy between W0000 DOC-010 and W70 DOC-043 needs governance reconciliation.
- Current Work inventory count 64 must be reconciled against W0000 DOC-018 snapshot 56.
