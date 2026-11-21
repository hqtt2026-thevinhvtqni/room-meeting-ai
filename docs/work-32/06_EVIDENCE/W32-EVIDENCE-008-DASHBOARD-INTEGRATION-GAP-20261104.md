# W32-EVIDENCE-008 — DASHBOARD–WORKSPACE–CORE INTEGRATION GAP
**Document Number:** W32-EVIDENCE-008  
**Priority Order:** P1 — required before whole-product browser Auto E2E  
**Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER  
**Date-Time:** 2026-11-04 06:48–07:00 (Asia/Ho_Chi_Minh)  
**Status:** BLOCKED — integration not implemented/proven; browser E2E NOT RUN

## 1. Purpose
Record the source-audited boundary between the Dashboard, Workspace, and ROOM HOP Core after the Core product Auto E2E and immutable-artifact gates passed. This is an evidence/gap record, not approval to change the Dashboard, Workspace, or Core architecture.

## 2. Evidence inspected
1. Dashboard repository: `hqtt2026-thevinhvtqni/hqtt-Dashboard-note`, branch `hqtt-ai-project-structure-082c9`.
   - `src/App.tsx`, blob SHA `08304e4145ff5db5efdf852dc30fafc5acc7a60e`.
   - `src/room-hop/bridge/RoomHOPBridge.ts`, blob SHA `8eef5f269e9756017a4f4348e68a81bb8339895e`.
2. Core repository: `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `work/32-ci-cd-python-ci-v2`.
   - `API_CONTRACT.md`, blob SHA `29b33cfd4aca4252d9786965f7e54b519a77f72b`.
3. Work 32 exact-SHA CI run #71:
   - URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41724493715
   - Commit: `021c8b842baf937e0ca06f8dcb44050f2741cc7e`
   - Unit: 157 passed.
   - Core product Auto E2E: 39 passed, 1 warning.
   - Immutable artifact E2E: 1 passed.

## 3. Direct source findings
### 3.1 Dashboard
- `App.tsx` uses `bridge ?? createMockBridge()`; therefore the default runtime is the mock bridge.
- The bridge source explicitly labels itself MOCK / temporary and says it is client-side only.
- The bridge seeds `mock-meeting-001` and stores mutable meeting state in a local closure.
- Its current interface contains UI working-state methods (notes, participants, enhance, action toggles, clear, export, subscribe); it is not evidence of a production HTTP adapter.
- No `httpBridge.ts` was found at the initially expected `src/httpBridge.ts` path. This is not a claim that no adapter exists anywhere in the repository; the audited App import path and bridge file are the evidence cited here.

### 3.2 Core / Workspace boundary in the current contract document
- `API_CONTRACT.md` states Core (:8000) owns meeting identity and lifecycle.
- It separately assigns Workspace (:8010) authority over working-state (notes, UI participants, minutes, actions, title/date), referencing `core_meeting_id`.
- It assigns create-session orchestration to the Bridge/Application Service, not the UI.
- The contract's status is “LOCKED (pending Xu/Mê final sign-off on implementation diff)”. A documented contract is not proof that the Workspace service, Bridge adapter, or routes are implemented and running.
- Core lifecycle HTTP endpoints and MCP public tools are distinct contracts. Do not treat MCP lifecycle coverage as proof of Dashboard HTTP/browser integration.

## 4. Gap determination
| Gate | Evidence / current result |
|---|---|
| Core lifecycle product journey | PASS — exact-SHA CI run #71 |
| MCP stdio public contract in Core journey | PASS — exact four-tool boundary tested |
| Immutable source artifact and artifact-level E2E | PASS — exact-SHA CI run #71 |
| Dashboard default real adapter | BLOCKED — App defaults to mock |
| Workspace (:8010) runtime/API implementation | NOT PROVEN by inspected sources |
| Dashboard → Bridge → Workspace → Core browser E2E | NOT RUN — no verified real runtime path |
| CD/staging/production | BLOCKED — no attested target/credentials/approval/rollback evidence |
| Independent Vibe review | PENDING |

## 5. Required next gates (contract-first; no implementation shortcut)
1. Xu confirms the authoritative Dashboard–Bridge–Workspace–Core contract and signs off the implementation diff boundary.
2. Read-only source/runtime audit proves the Workspace (:8010) service, persistence owner, auth model, and exact routes exist at a pinned commit. If absent, record the gap; do not invent endpoints.
3. Verify identity propagation and meeting lifecycle orchestration: identity selection; Core-created meeting ID; Bridge application-service orchestration; Workspace working-state persistence referencing that Core ID; no duplicate meeting authority.
4. Only after gates 1–3 pass, implement the real adapter within the approved boundary and add browser E2E against real services.
5. Browser E2E must cover create/select meeting, join/start lifecycle as authorized, persist/reload notes and working-state, verify transcript/evidence readback from Core, close meeting, and prove no mock data or second source of truth is used.
6. Run the same tests against an immutable exact-SHA artifact, then request independent Vibe review.
7. CD remains a separate gate requiring a real staging target, protected approval, credentials, health checks, and tested rollback.

## 6. Explicit non-actions / safety
- No Dashboard source changed.
- No Core source or API contract changed.
- No Workspace endpoint was invented or called.
- No direct Dashboard → Core bypass was added.
- No mock handler was relabeled as production.
- No merge, rebase, cherry-pick, PR merge, deployment, or release was performed.

## 7. Disposition
**Work 32: ACTIVE — NOT RELEASED.**  
Core CI + Core product Auto E2E + immutable artifact E2E are PASS. Whole-product Dashboard browser E2E remains BLOCKED / NOT RUN pending verified Workspace runtime and Xu-approved integration contract. CD and independent review remain open.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Independent Architecture & Backend Reviewer (Work 32 execution)
- **Date-Time:** 2026-11-04 07:00 Asia/Ho_Chi_Minh
- **Record:** Source-audited integration boundary and outstanding product-level E2E gates; no implementation authority exercised outside Work 32 evidence recording.

## NHẬT KÝ
- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 07:00 Asia/Ho_Chi_Minh
- **Priority:** P1
- **Action:** Inspected Dashboard App and bridge source plus Core API contract; recorded the distinction between Core product E2E PASS and whole-product Dashboard browser E2E NOT RUN.
- **Result:** BLOCKED on real Workspace runtime/contract proof; implementation and release remain withheld.
