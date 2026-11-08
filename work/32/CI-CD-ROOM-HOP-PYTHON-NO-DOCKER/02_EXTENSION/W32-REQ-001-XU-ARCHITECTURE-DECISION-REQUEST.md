# W32-REQ-001 — XU/MÊ ARCHITECTURE DECISION REQUEST: DASHBOARD–BRIDGE–WORKSPACE–CORE

- **Document Number:** W32-REQ-001
- **Priority Order:** P1 — blocking whole-product Browser Auto E2E
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Date-Time:** 2026-11-04 07:15 Asia/Ho_Chi_Minh
- **Status:** DECISION REQUESTED — NOT APPROVED / NOT AN ADR

## 1. Purpose

Request Xu (CEO / Lead Architect) and Mê (if delegated as contract co-approver) to identify and confirm the authoritative implementation contract for Dashboard → Bridge/Application Service → Workspace (:8010) → Core (:8000), before Ka implements a production adapter or whole-product browser E2E.

This document records unresolved decisions only. It does not create an architecture decision, API, route, schema, implementation authorization, or release approval.

## 2. Evidence baseline

1. Dashboard repository hqtt2026-thevinhvtqni/hqtt-Dashboard-note, branch hqtt-ai-project-structure-082c9, tree SHA 32e41f43d2fdd6b8314185bbaa57bc8b04b41641:
   - src/App.tsx defaults to bridge ?? createMockBridge().
   - src/room-hop/bridge/RoomHOPBridge.ts is a synchronous client-side mock.
   - docs/api/hqtt-bridge.md says backend endpoints are not created in the Dashboard repo and lists expected/proposed paths.
2. Core repository hqtt2026-thevinhvtqni/room-meeting-ai, default branch source reviewed at 157e88e2cd821a0b53bdcabd6483956e6bc2074a:
   - API_CONTRACT.md assigns meeting identity/lifecycle to Core :8000 and working-state to App Workspace :8010, but status is LOCKED pending Xu/Mê final sign-off on the implementation diff.
   - room_hop_mcp/adapter/http_server.py registers identity and Meeting routes; no Workspace router was found in this inspected file.
3. Work 70 DOC-010 states its Work-scoped Dashboard read routes are proposals, not verified Core endpoints. Meeting artifact persistence is not a generic Work store.
4. Work 32 evidence W32-EVIDENCE-009 records bounded repository/source searches. Workspace :8010 source/runtime and persistence remain NOT PROVEN in the inspected source.

## 3. Decisions requested

### D1 — Canonical Workspace implementation
- Which repository, directory, branch/commit and deployment process own App Workspace :8010?
- Is :8010 an independently deployed service, a process inside another application, or a local-only runtime?
- Who owns its code and operational state?

### D2 — Authority and persistence
- Confirm Core :8000 is sole authority for meeting identity and lifecycle.
- Confirm Workspace :8010 is sole authority for editable working-state only.
- Specify canonical persistence technology/schema, migration owner, retention and concurrency behavior.
- Define how Workspace validates/handles core_meeting_id and what happens when Core meeting creation fails or the ID is unknown.
- Confirm there is no second meeting lifecycle or duplicate Meeting authority in Workspace/Dashboard.

### D3 — Bridge/Application Service orchestration
- Confirm the exact owner and source location of the Bridge/Application Service.
- Confirm whether the browser calls one application-service command for create-session and close-session, rather than orchestrating Core's create → open → join×N → start sequence itself.
- Specify the stable command/query contract and whether calls are asynchronous.
- Define identity propagation from authenticated user selection to Core created_by, join identities, Workspace caller identity and audit trail.

### D4 — Data semantics
- Define separate ownership and mutation rules for Core transcript/evidence (append-only); Workspace raw working notes/context (editable); parsed minutes and action-item working state; approved Core decisions; final closed-meeting artifact.
- Confirm whether the current Dashboard setNotes/addNote/enhance/toggleAction/clear semantics are acceptable or must be redesigned to preserve those boundaries.
- Specify how Workspace action objects are mapped to Core close-meeting action_items: list[str], and who performs the mapping.

### D5 — AuthN/AuthZ and transport
- Specify the canonical authentication/session mechanism, token handling, CORS, CSRF, origin policy and authorization rules for each operation.
- Define 401/403/404, stale/offline state, audit/correlation IDs, secret redaction, rate limits and cache behavior.
- No browser secret or trust in client-supplied identity/authorization booleans.

### D6 — Failure safety and consistency
- Define idempotency keys, duplicate submission behavior, optimistic concurrency/version checks, retry rules and partial failure recovery across Core and Workspace.
- Define whether Workspace can persist working state when Core is unavailable and how that state is reconciled without fabricating a Core meeting ID.
- Define close-session compensation/terminal behavior; Core closed meetings remain immutable under the existing lifecycle contract.

### D7 — Dashboard adapter migration
- Confirm whether RoomHOPBridge is intended to remain the UI abstraction boundary.
- Confirm the approved production adapter interface and how it handles loading, errors, refresh, subscription/realtime and stale state.
- Confirm migration strategy from createMockBridge() without changing the approved UI or creating a second source of truth.
- Clarify whether the separate Work 70 Dashboard read-only projection is a different product surface and must remain read-only, distinct from HQTT meeting notes UI.

## 4. Requested decision output

Xu/Mê should return:
1. Approved canonical source/revision for Workspace and Bridge/Application Service.
2. Approved sequence/authority diagram and API contract with request/response schemas.
3. Approved persistence owner and identity/auth model.
4. Explicit accepted/rejected semantics for notes, transcript, minutes, decisions, actions and final artifact.
5. Implementation boundary and named owners.
6. Required tests and evidence for authorization, persistence, consistency and browser Auto E2E.
7. Explicit decision status: APPROVED, REVISE, or BLOCKED, with date-time and signer.

## 5. Ka execution boundary while decision is pending

- Continue read-only source/runtime audit if a canonical Workspace source/revision becomes available.
- Do not implement endpoints, adapter, persistence schema, route, proxy or Core changes from assumptions.
- Do not use the Dashboard's proposed /api/meetings/{id}/hqtt-bridge as if it were a real API.
- Do not use the Core Meeting artifact save method as Workspace persistence.
- Do not connect Dashboard directly to Core as a shortcut.
- Do not mark browser Auto E2E PASS until real services and persisted state are exercised end-to-end.
- Keep Core CI and immutable artifact E2E PASS separate from whole-product Browser E2E status.

## 6. Current gate disposition

- Core product lifecycle Auto E2E: PASS (run #71, exact SHA 021c8b842baf937e0ca06f8dcb44050f2741cc7e).
- Immutable source artifact E2E: PASS (run #71).
- Dashboard real adapter: NOT FOUND in inspected Dashboard branch.
- Workspace :8010 source/runtime/persistence: NOT PROVEN in inspected source.
- Xu/Mê final contract sign-off: PENDING.
- Whole-product Dashboard → Bridge → Workspace → Core Browser Auto E2E: NOT RUN.
- Work 32: ACTIVE — NOT RELEASED.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Architecture & Backend Audit Owner — Work 32
- **Date-Time:** 2026-11-04 07:15 Asia/Ho_Chi_Minh
- **Record:** Issued a decision request to preserve architecture authority and prevent implementation based on proposed/unverified interfaces.

## NHẬT KÝ
- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 07:15 Asia/Ho_Chi_Minh
- **Priority:** P1
- **Action:** Prepared W32-REQ-001 listing the precise Xu/Mê decisions required to unblock the whole-product Browser Auto E2E.
- **Result:** REQUEST RECORDED; NOT APPROVED; no code or architecture mutation.
