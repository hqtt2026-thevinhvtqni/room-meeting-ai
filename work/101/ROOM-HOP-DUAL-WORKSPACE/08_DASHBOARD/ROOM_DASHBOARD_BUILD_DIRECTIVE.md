# ROOM-HOP — ROOM-WIDE DASHBOARD BUILD DIRECTIVE
**Authority:** Vinh  
**Purpose:** Build one operational Dashboard for the entire ROOM-HOP system, not a dashboard dedicated to Work 101.  
**Status:** BUILD SPECIFICATION — not proof of implementation or runtime connectivity.

## 1. Mission and scope
Build a single Room-wide control/observability surface at the existing Dashboard boundary (:3000). It must let Vinh and authorized Room agents inspect the health, lifecycle, progress, dependencies, evidence, and blockers of the whole ROOM-HOP environment and all Works. Work 101 Dual Workspace is only one module/card in that Dashboard.

The Dashboard is a read-only presentation layer. It must not become a second source of truth, execute arbitrary commands, modify Works, merge/push code, change lifecycle, approve integration, or enable synchronization.

## 2. Mandatory execution protocol
Follow this sequence without skipping steps:
1. READ — read MAIN_SOURCE, Room context, Work Index 99, existing Dashboard, Core route registration, API schemas, auth/audit rules, and relevant Work contracts.
2. TRACE — trace every displayed field from its authoritative source through Core/service/API to Dashboard. Trace dependencies for Works 24, 27, 28, and 14 where they affect workspace/runtime/build status. Do not assume an endpoint exists because it is mentioned in a mockup.
3. ANALYZE — list source-of-truth, data freshness, access control, unavailable sources, schema conflicts, lifecycle disagreements, and missing contracts.
4. DECIDE — record architecture decisions and blockers before coding. Core :8000 remains the single source of truth; Dashboard :3000 remains render-only.
5. BUILD — implement only against verified contracts. Prefer a Room-wide read model/API owned by Core or its approved application service; do not query databases/filesystems directly from the browser or MCP.
6. VERIFY — run unit, contract, security, accessibility/basic UI, and runtime tests. Verify the real Dashboard against a running Core; capture timestamped evidence. If runtime cannot be reached, report BLOCKED/NOT VERIFIED, not PASS.
7. HANDOFF — report changed files, branch/commit, tests and evidence, unresolved blockers, and exact next gate.

## 3. Room-wide Dashboard information architecture
Provide these views/sections:
- **Room overview:** overall service availability, current environment/version, last successful health check, data freshness, and explicit unknown states.
- **Service health:** Core :8000, Dashboard :3000, Workspace :8010, Gateway :8040, MCP :8020, Build MCP :8030, W13 bridge/provider :8031, Event Listener :8050, Agent Runtime :8051, and Browser provider :8787 where available. Show configured/observed/unavailable separately; do not infer a process is running from configuration alone.
- **Works registry:** all Works from authoritative Work Index 99, with Work ID/name, lifecycle, owner/assigned AI, dependencies, status, last update, blockers, and evidence links. Never invent Works or overwrite their lifecycle.
- **Execution/build activity:** recent runs, outcomes, duration if measured, test summary, artifact/evidence links, and source timestamp. Separate simulation/mock from real API/runtime runs.
- **Dependencies and blockers:** upstream/downstream Works, blocked gates, missing contracts, and conflicts. Highlight contradictory evidence instead of choosing one silently.
- **Evidence and audit:** link to source evidence and show when/where it was observed. Dashboard must not manufacture PASS status.
- **Dual Workspace (Work 101):** Sandbox/GitHub source revisions, baseline binding, content-hash parity, conflicts, deletion-pending items, stale status, and integration approval state. This is a module of the whole-Room Dashboard, not its root identity.
- **Governance and security:** read-only visibility into pending approvals, policy gates, permission failures, and audit events. Do not expose credentials, tokens, private secrets, or sensitive raw payloads.

## 4. Data and API rules
- Core :8000 is the single source of truth. Dashboard is render-only.
- First inspect existing Core routes and application-service contracts. Reuse authoritative APIs where suitable. If a new aggregate/read-model endpoint is required, document and test its contract before connecting the UI.
- A proposed endpoint such as `GET /api/room/dashboard/status` is only a proposal until it is found or implemented, tested, and verified at runtime.
- Every status record should carry a source, observed_at/updated_at timestamp, freshness/stale indicator, and evidence/reference where applicable.
- Distinguish at minimum: `PASS`, `FAIL`, `BLOCKED`, `PENDING`, `UNKNOWN`, `STALE`, and `NOT_VERIFIED`. Missing data is UNKNOWN, not healthy.
- Never use hard-coded demo values as live data. If fixtures are used in development, label them DEMO/MOCK visibly and keep them out of production responses.
- Do not let browser code connect directly to GitHub using a token, local files, Workspace database, or service internals. Use authorized Core/API boundaries.
- Validate schemas server-side and client-side. Ensure JSON Schema composition does not accidentally reject legitimate fields or permit unspecified fields.
- Respect existing authentication, authorization, CORS, and audit policy. Fail closed when identity/permission is missing.

## 5. Safety and authority boundaries
- Dashboard actions are view/filter/navigate/refresh only unless Vinh separately authorizes a specific action and a safe, audited API contract exists.
- No merge, push, release, lifecycle mutation, destructive operation, or integration approval from this Dashboard by default.
- Work 101 sync remains non-writing/planning-only until separately approved; divergent same-path edits stay CONFLICT_PENDING; deletions stay DELETION_PENDING; never use last-write-wins.
- Approval, if later supported, must bind the exact operation ID, diff digest, destination branch, and base revision.
- Keep secrets, credentials, tokens, environment files, databases, logs, caches, temporary files, OS metadata, and key material out of sync and out of dashboard payloads.
- MAIN_SOURCE remains read-only for AI build operations. Build in the authorized Sandbox/feature branch. Do not write to main/master or integrate without Vinh's explicit approval.

## 6. Implementation sequence and acceptance gates
A. Inventory: read existing Dashboard files, Core route registration, Work Index 99 and service contracts; produce a source-to-widget mapping.
B. Contract: define a Room-wide read model and JSON schema, with examples for healthy, blocked, stale, unavailable, and partially populated states.
C. Backend: implement/reuse an authorized Core application-service endpoint; no direct storage bypass.
D. Frontend: build overview, service health, Works registry, activity, blockers/evidence, and Work 101 module. Ensure accessible labels, loading/error/empty states, and clear timestamps.
E. Tests: schema/contract tests; source-of-truth and authorization tests; missing/stale-data tests; no-secret exposure checks; frontend rendering tests; integration tests against actual Core.
F. Runtime verification: launch/inspect services through the established Room workflow, fetch the endpoint, load Dashboard, and verify displayed values against source evidence. Record request/response status, timestamps, commit SHA, and test output without including secrets.
G. Handoff: document what is DONE, PASS, BLOCKED, NOT VERIFIED, and the next gate. Do not claim E2E until the real runtime path is observed.

Acceptance criteria:
- One Dashboard represents the entire Room and discovers Works from Work Index 99 rather than hard-coded Work 101 data.
- All displayed live values trace to an authoritative source and include freshness/evidence.
- Missing/unreachable services show UNKNOWN/DISCONNECTED/STALE as appropriate, never fabricated healthy status.
- Dashboard cannot mutate lifecycle, approve integration, or perform writes by default.
- Work 101 appears as one module among Room-wide services and Works.
- Tests and runtime evidence are recorded; all unverified portions remain explicitly unverified.

## 7. Required handoff format
**DONE:** verified implementation artifacts only.  
**PASS:** named test/check plus evidence reference.  
**BLOCKED:** exact missing dependency/permission/contract and its effect.  
**NOT VERIFIED:** checks not run or runtime not observed.  
**DECISION NEEDED:** only decisions that genuinely require Vinh's authority.  
**NEXT GATE:** one concrete action that advances the system without repeating completed work.

## 8. Starting references
- Repository: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai
- Work 101 branch: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/tree/work/101-room-hop-dual-workspace
- Existing Work 101 dashboard prototype (reference only): https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/blob/work/101-room-hop-dual-workspace/work/101/ROOM-HOP-DUAL-WORKSPACE/08_DASHBOARD/index.html
- Work 101 manifest: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/blob/work/101-room-hop-dual-workspace/work/101/ROOM-HOP-DUAL-WORKSPACE/00_ROOT/WORK_MANIFEST.md

**Important:** this directive is the work order for AI agents. It does not claim that the Room-wide Dashboard, its API, or its runtime integration has already been built.
