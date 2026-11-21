# W32-EVIDENCE-009 — WORKSPACE :8010 SOURCE AUDIT & CONTRACT RECONCILIATION

- **Document Number:** W32-EVIDENCE-009
- **Priority Order:** P1 — prerequisite to real Dashboard Browser Auto E2E
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Date-Time:** 2026-11-04 07:10 Asia/Ho_Chi_Minh
- **Status:** BLOCKED — Workspace runtime/source and approved integration contract not established

## 1. Purpose

Continue the product-level Auto E2E source audit after Core lifecycle Auto E2E passed. Determine whether the documented App Workspace (:8010) working-state service and the Dashboard adapter are implemented in the inspected source. This is read-only evidence, not authorization to alter architecture or create routes.

## 2. Exact sources inspected

### Dashboard
Repository: `hqtt2026-thevinhvtqni/hqtt-Dashboard-note`  
Branch: `hqtt-ai-project-structure-082c9`  
Tree SHA: `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`

- `src/App.tsx`, blob `08304e4145ff5db5efdf852dc30fafc5acc7a60e`
- `src/room-hop/bridge/RoomHOPBridge.ts`, blob `8eef5f269e9756017a4f4348e68a81bb8339895e`
- `docs/api/hqtt-bridge.md`, blob `7367ebfb33f6032293d775a7a300651dd2d6409c`
- `docs/discovery/05-bridge-implementation.md`, blob `cdb9ea60e9256a5273f7e98b162c570816d72725`
- `README.md`, blob `8dea4143aaed2ebc6fd2b38c5c22cc6c25545943`

### ROOM HOP Core
Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`  
Default branch reviewed at `157e88e2cd821a0b53bdcabd6483956e6bc2074a`.

- `API_CONTRACT.md`, blob `29b33cfd4aca4252d9786965f7e54b519a77f72b`
- `room_hop_mcp/adapter/http_server.py`, blob `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d`
- Work 70 `03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md`, blob `7f931b58776c287ccb806a79e864d8839645d8e5`

Searches covered `WorkspaceService`, `app_workspace`, `working_state`, `workspace routes`, `workspace persistence`, `8010 FastAPI`, and `core_meeting_id` in the inspected Core repository. No dedicated Workspace service implementation or :8010 route source was returned. Installed repository search for a separate workspace repository also returned no result. These are bounded search results, not proof about uninspected PC-only sources or private repositories outside the connector's scope.

## 3. Verified findings

### 3.1 Dashboard is still mock-backed by default
- `App.tsx` selects `bridge ?? createMockBridge()`.
- The bridge is explicitly documented as MOCK / temporary / client-side.
- `createMockBridge()` seeds `mock-meeting-001` and holds mutable meeting state in a closure.
- The interface is synchronous (`getCurrentMeeting`, `setNotes`, `enhance`, `subscribe`, etc.). No HTTP adapter implementation appears in the inspected repository tree.
- `docs/api/hqtt-bridge.md` explicitly says the backend endpoints are not created in the Dashboard repository and labels the proposed paths as expected/proposed contract.

### 3.2 The Dashboard's proposed bridge API is not the locked Core HTTP API
The Dashboard proposes `GET /api/meetings/{id}/hqtt-bridge` and several notes/minutes/participant mutation routes. The inspected Core HTTP router exposes identity and Meeting lifecycle/transcript/paste routes; it does not register the proposed `hqtt-bridge` or Workspace routes.

### 3.3 The Core contract describes Workspace, but description is not implementation evidence
- `API_CONTRACT.md` assigns Core (:8000) authority over meeting identity/lifecycle.
- It describes App Workspace (:8010) as authority for working-state and says it references `core_meeting_id`.
- The same document states the contract is LOCKED pending Xu/Mê final sign-off on the implementation diff.
- The inspected Core HTTP adapter registers `/identities`, `/meetings`, meeting detail/transcript/paste and lifecycle routes. No Workspace router is registered in this file.
- Work 70 DOC-010 says the proposed Work-scoped Dashboard read endpoints are not verified routes and that Core's Meeting artifact save operation must not be repurposed as generic Work storage.

### 3.4 Integration contract gaps
Before a real adapter can be implemented, the architecture authority must resolve:
1. The actual owner/repository/deployment unit for Workspace :8010 and its pinned source revision.
2. Workspace persistence model and schema, including the authoritative key and lifecycle for `core_meeting_id`.
3. AuthN/AuthZ, caller identity propagation, CORS/CSRF/session model, and authorization for each read/write intent.
4. The Bridge/Application Service boundary that orchestrates Core create → open → join participants → start and Workspace working-state persistence.
5. Mapping semantics for transcript evidence (append-only), editable working context, parsed minutes, approved decisions, action items, and close-meeting artifact.
6. Async command/error/refresh/subscribe behavior. The existing synchronous mock interface is not proof that a production HTTP contract exists.
7. Idempotency, concurrency, retry, stale-data and partial-failure recovery across Core and Workspace.

## 4. Gate matrix

| Gate | Result | Basis |
|---|---|---|
| Core lifecycle HTTP + MCP stdio Auto E2E | PASS | Exact-SHA CI run #71 |
| Immutable source artifact E2E | PASS | Exact-SHA CI run #71 |
| Dashboard mock source identified | PASS | App + bridge source |
| Dashboard real HTTP adapter | NOT FOUND in inspected branch | Full repository tree + source |
| Workspace :8010 source/runtime/persistence | NOT PROVEN | Bounded repository and code search |
| Xu/Mê final sign-off of implementation contract | PENDING | API_CONTRACT.md status |
| Dashboard → Bridge → Workspace → Core browser E2E | NOT RUN | No verified real integration path |
| CD / staging / production | BLOCKED | No attested deployment target/approval/credentials/rollback |

## 5. Required next actions

1. Xu/Mê must confirm the authoritative implementation contract and identify the canonical Workspace :8010 source/revision and runtime owner.
2. Ka performs read-only source/runtime verification against that pinned source: routes, auth, persistence, schema, process health, and Core ID linkage.
3. Reconcile the Dashboard bridge interface to the approved asynchronous application-service contract; do not assume the current mock interface or proposed Dashboard endpoints are authoritative.
4. Only after contract sign-off and source/runtime proof, implement the adapter and real-service browser Auto E2E.
5. Test create/select → Core ID allocation → authorized join/start → Workspace save/reload → Core transcript readback → close/final artifact → reload and verify no mock state.
6. Repeat the product E2E against an immutable exact-SHA artifact and request independent Vibe review.
7. Keep CD separate until staging, approval, credentials, health checks and rollback are evidenced.

## 6. Explicit non-actions

- No source code changed in Dashboard, Workspace or Core.
- No route, endpoint, schema, database or adapter was invented.
- No direct Dashboard → Core bypass.
- No reuse of Meeting artifact persistence as Workspace storage.
- No branch merge, rebase, cherry-pick, PR merge, deployment or release.

## 7. Disposition

**Work 32: ACTIVE — NOT RELEASED.** Core product CI and immutable artifact E2E remain PASS on run #71. Whole-product Dashboard Browser E2E remains BLOCKED / NOT RUN until Xu/Mê confirm the contract and the actual Workspace source/runtime is identified and verified.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Architecture & Backend Audit Owner — Work 32
- **Date-Time:** 2026-11-04 07:10 Asia/Ho_Chi_Minh
- **Record:** Read-only Dashboard–Workspace–Core contract and source audit; no implementation authority exercised outside the approved evidence scope.

## NHẬT KÝ
- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 07:10 Asia/Ho_Chi_Minh
- **Priority:** P1
- **Action:** Inspected Dashboard repository tree, App/bridge/docs, Core API contract and HTTP router; searched for Workspace service/runtime source and route implementation.
- **Result:** Dashboard mock default confirmed; Workspace :8010 source/runtime not proven in inspected source; Xu/Mê sign-off remains pending. Real browser E2E remains NOT RUN.
