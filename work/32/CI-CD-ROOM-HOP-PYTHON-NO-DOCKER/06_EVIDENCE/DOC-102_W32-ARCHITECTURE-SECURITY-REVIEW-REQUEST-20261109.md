# DOC-102 — Work32 Architecture and Security Review Request

- **Document Number:** DOC-102
- **Priority Order:** P0 — Runtime concurrency and pre-release security review
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Name:** Ka
- **Title:** CSA / Delegated Work32 Execution Owner
- **Date-Time:** 2026-11-09 02:38 (+07:00)
- **Status:** REVIEW REQUEST PREPARED — no reviewer decision recorded

## 1. Xu — review Browser Adapter concurrency model

**Existing decision:** W32-ADR-002 already locks Public V1 to exactly four tools: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`. Join/start remain Core HTTP lifecycle routes. No further Xu decision is needed on this four-tool inventory.

**Implementation finding:** Browser Adapter owns one process-wide Playwright browser/context/page and mutable logs. Concurrent FastAPI sync handlers can run on different worker threads and workflows can interleave against the same page.

**Ka's mitigation:** Re-entrant operation lock serializes lifecycle/workflow calls; dedicated single-worker executor pins all Playwright sync operations to one thread. Each workflow still opens its own bounded MCP stdio session and exact transcript readback. Two tests cover workflow isolation and one-thread ownership.

**Review question:** Is serialized single-browser ownership acceptable for Work32 v1, or should the adapter move to request/workflow-scoped browser contexts to preserve true parallel browser sessions? Current implementation favors deterministic correctness over throughput.

## 2. CTO — security review before staging/production

DOC-065 states that registry-resolved `identity_id` is not an independently authenticated transport principal, and SQLite coordinates only same-host local processes/filesystem.

**Review questions:**
1. What authenticated principal / transport binding is required before paste operations are exposed to untrusted clients?
2. Is the identity-based F4 quota acceptable for local/single-host product testing only?
3. Confirm multi-host deployment must replace SQLite with an approved shared atomic store.
4. Review subprocess environment minimization, disposable-store guards, HTTP 429 / Retry-After and artifact/evidence handling.

## 3. Ka execution while review is pending

- Build and test the clean branch from main; keep main unchanged.
- Run exact-SHA CI and inspect all job logs/artifacts.
- Preserve F4 limits and the four-tool Public V1 contract.
- Do not deploy staging/production or claim RELEASED before CTO/security and operational gates.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Delegated Work32 Execution Owner
- **Date-Time:** 2026-11-09 02:38 (+07:00)
- **Record:** Prepared focused review requests from source evidence; no Xu/CTO decision is claimed.

## NHẬT KÝ
- **Name:** Ka
- **Title:** CSA / Delegated Work32 Execution Owner
- **Date-Time:** 2026-11-09 02:38 (+07:00)
- **Priority:** P0
- **Action:** Identified singleton Playwright concurrency/thread-affinity risk; implemented serialization and dedicated worker ownership; routed architecture tradeoff to Xu and security boundary to CTO.
- **Result:** Review pending; Work32 ACTIVE — NOT RELEASED.
