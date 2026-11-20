# W113 PRODUCT ARCHITECTURE — INITIAL BASELINE
- Document ID: DOC-008 | Priority: P1 | Read order: 8
- Version: 1.1
- Updated: 2026-11-13 04:59 (+07)
- Status: DRAFT — CONTRACTS NOT VERIFIED
- Date opened: 2026-11-09

## Logical view
Human / AI clients (Web and Mobile)
→ ROOM-HOP Dashboard UI
→ Dashboard Bridge / API gateway (only verified published contracts)
→ owning domains: Company | Sandbox/Work | Meeting | Core/system services

## Domain ownership
- Company owns company governance, member and organization records.
- Sandbox/Work owners retain Work files, lifecycle, WP and evidence records.
- Meeting owns meetings, participants, sessions and meeting outputs.
- Core remains authoritative for identity, authorization and core-owned lifecycle/evidence metadata where implemented and verified.
- Dashboard is a presentation/orchestration client, not an authority or persistence layer.

## Experience model
One product and navigation shell. Home and module visibility are computed from authenticated role/permissions. Human/AI labels may guide workflow but are not authorization primitives. Web uses a desktop-oriented layout; Mobile uses compact navigation and task-focused views. Both consume the same contracts.

## Security
Authenticate through the verified identity provider. Enforce authorization on the server for every resource and command. Deny by default; scope access by identity, role, assignment, Work/resource and action. Never trust client-side visibility. Audit sensitive reads/actions where supported. Do not expose tokens/secrets to the UI.

## Data contract
Every displayed datum must carry or resolve: domain owner, resource identity, source reference, source revision, as-of timestamp, freshness/status and access classification. Missing values remain UNKNOWN/NOT VERIFIED. No fabricated live data.

## Command contract
Default to read-only. A state-changing action must be explicitly supported by the owning domain API, validated and authorized server-side, idempotent where applicable, and audited. No direct DB or filesystem operations.

## Mobile strategy
Responsive Web is the baseline requirement. PWA/native packaging decision is deferred until user journeys, offline/notification requirements, device support and available infrastructure are verified.

## Architecture decisions required before BUILD
1. Identity and role claim source.
2. API gateway/Bridge and service-by-service contracts.
3. Company/Sandbox/Meeting data ownership and field-level permissions.
4. Command/event model and audit.
5. Web deployment, mobile strategy and supported device matrix.
6. Observability, freshness, caching, offline and failure semantics.
7. Threat model, privacy, accessibility and performance budgets.

## Discovery-backed integration boundaries — 2026-11-13 (FACT, not approval)
| Area | Existing owner/reference inspected | What is evidenced | What remains unverified |
|---|---|---|---|
| Work lifecycle / gates / Work Dashboard standard | W70 DOC-042, DOC-043, DOC-085, DOC-096 | Active governance rules; Work Dashboard is distinct from Product Dashboard | Live Core lifecycle APIs and live projection contract |
| AI assignment / dispatch | W70 DOC-064/065; W52 A2A v0.1 | Hybrid provider-neutral design and logical contract proposals | Approved runtime API, private-session dispatch, receipt and authenticated ACK |
| Cross-Work correlation / evidence | W112 Charter and DOC-001 baseline | Contract ownership and correlation model proposed | Runtime event bus, evidence store, locks/leases and auth enforcement |
| Graph/context projection | W114 ADRP-114-001 and bridge/capability matrices | Read-only graph and context architecture proposed; current 8030 tool surface lacks typed private dispatch/ACK | Approved live graph source contracts and dispatch integration |
| AI membership | W11 Member Contract / Production Integration Boundary | Provider-neutral member adapter boundary described | Live Core wiring, verified identity/authentication and session binding |
| Gateway/authentication | W01 Gateway source; W02 authorization Work | Gateway/auth ownership components and W02 scope documented | Deployed endpoint, server-side policy enforcement and current runtime health |
| Meeting | W71 Product Architecture; 8030 Meeting tools | Meeting-specific product architecture and meeting-scoped tools exist | Complete live Meeting API/permission contract for Dashboard use |
| Candidate product UI | hqtt2026-thevinhvtqni/PL.room-meeting-ai.dash main @ dc4be09bc43c02630f60eb892782e72a07c782b8 | Meeting SessionView UI/Contract Lab; mock bridge is default in inspected source | Suitability as W113 universal product source; real endpoint security and runtime behavior |

## Dashboard responsibility split (inherited W70 DOC-085)
- W113 Work Dashboard: execution view for Work 113 itself; canonical W0 dashboard contract/status stays under W113 DASHBOARD/ and DOC-012.
- W113 Product Dashboard: ROOM-HOP Universal Dashboard product for authorized Company, Sandbox/Works, Meeting and Control Center views.
- These two views may link by Work/Product IDs but must not share lifecycle semantics or duplicate domain stores.
- The candidate PL.room-meeting-ai.dash repository is not adopted as canonical W113 Product Dashboard source by this document.

## Architecture status
This document remains a draft. The table records inspected design/source evidence only. No endpoint, API version, permission scope, live service status, source repository adoption or runtime path is approved by this update. No product code was changed.


## Additional owner-boundary evidence — 2026-11-13 (FACT, not approval)
| Area | Owner evidence inspected | Verified boundary | Remaining gap |
|---|---|---|---|
| Core :8000 | W37 Manifest, CORE_8000_SCOPE and single-Core rule | W37 is an evidence workspace for one Core, not Core 2; Core is intended single source of truth | Core entrypoint, API schemas, auth, persistence and live health still require source/runtime verification |
| Gateway :8040 | W38 Manifest and Sandbox Mirror Role | W38 is an isolated investigation workspace; initial status CREATED | Live process, routes, authorization and downstream behavior not audited |
| Build MCP :8030 | W39 Work identity; current 8030 room context and tool inventory | Current connection supports Sandbox file operations and meeting-scoped operations | No typed task dispatch, private-session delivery/receipt or authenticated ACK action |
| Execution Host / E2E | W14 Manifest and absorbed W12 Execution Host Boundary | W14 owns consolidated Autonomous E2E Builder; current 8030 surface exposes no executable Work Host/process/Git/CI/browser adapter | Callable Host, grants/revocation, Run Record and full real-browser E2E not verified |
| AI skills | W21 Manifest and Skill Contract | Skill defines procedure/capability and does not grant authority | Skill registry/runtime binding and Core integration not verified |
| AI identity roster | W0000 DOC-010 and W70 DOC-043 | W70 is identified by W0000 as operational roster reference | W0000 DOC-010 AI-ID rows conflict with W70 mapping; governance reconciliation required before assignment |

These records are discovery references only. They do not authorize W113 to call an endpoint, run code, issue grants or modify another Work.


---

## Delegated architecture baseline — Universal Dashboard + shared Work Dashboard ingress + Auto E2E (2026-11-21)

**Disposition:** ARCHITECTURE BASELINE AUTHORED BY CO UNDER D-113-005; source-owner/API/runtime verification and independent review remain open. This is a controlled design baseline, not evidence that existing services already implement these contracts.

### A. Product and dashboard topology
W113 delivers one responsive Universal Dashboard product with two distinct responsibilities:
1. **Universal Product Dashboard:** the user-facing product shell and domain experiences for Global Home, Company, Sandbox/Works, Meeting and Control Center.
2. **Work Dashboard host/navigation:** a common entry surface through which authorized Work-specific dashboards can be reached. Each Work's dashboard remains its own projection and ownership boundary.

The two responsibilities may share the shell and ingress but must not share lifecycle semantics, authoritative stores, credentials or permissions. W70 DOC-085 remains binding: Work Dashboard ≠ Product Dashboard.

### B. Shared port 3000
- Target topology: one authoritative ingress/listener on the verified existing bind address, owned by the existing Dashboard Host/Router once its real owner and implementation are identified.
- W113 must not create a second competing listener or let individual Work modules bind port 3000.
- The ingress resolves registered routes to approved dashboard modules. A route registry is metadata, not a security boundary.
- Proposed route contract (subject to compatibility review): `/` = Universal Home; `/company`; `/sandbox`; `/meeting`; `/control-center`; `/works/{work_id}` = that Work's dashboard; deep links only when the target Work declares and authorizes them.
- Route resolution validates Work ID, module registration, caller identity and resource-level permission on the server. Unknown Work, missing registration or denied access fails closed.
- Each Work module is isolated by route namespace and API/data contract. Shared port does not imply shared data or authority.
- Existing port-3000 process, startup command, reverse-proxy topology, base path and current route behavior are **NOT VERIFIED**. Do not reconfigure or restart the listener until read-only runtime attestation and owner contracts identify the actual host.

### C. Logical component architecture
```text
Browser / Mobile Web
        |
        v
Shared Dashboard Ingress :3000 (existing owner to be verified)
        |
        +--> Universal Dashboard Shell (W113)
        |       +--> Global Home
        |       +--> Company module
        |       +--> Sandbox / Work module
        |       +--> Meeting module
        |       +--> Control Center
        |
        +--> Registered Work Dashboard routes
                +--> W70 / W71 / other Work modules
                (each retains its own Work identity and authority)

UI modules
   |
   v
Typed Dashboard Data / Command Ports
   |
   +--> Verified Gateway / Bridge contracts (owner and endpoint to be proven)
   +--> Company owning service
   +--> Work / Sandbox owning service
   +--> Meeting owning service
   +--> Core identity / authorization services
   |
   v
Authoritative domain stores and audit records (never accessed directly by UI)
```

This is a logical diagram. It does not assert that the current :3000 host, Gateway, Core or domain endpoints already expose these contracts.

### D. Module boundaries
- **App Shell:** global navigation, responsive layout, route loading, error boundaries and accessible interaction.
- **Route Registry:** approved route metadata, Work ID, dashboard type, module version, owner, required permission identifiers and source revision. It cannot grant permissions.
- **Identity Adapter:** consumes only the verified session/identity contract; no client-generated identity claims.
- **Authorization Guard:** hides unavailable navigation for usability but relies on server-side authorization for every resource and action.
- **Dashboard Data Ports:** typed read adapters per domain; each includes timeout, cancellation, retry policy, cache policy and source provenance.
- **Command Ports:** disabled by default; only expose commands with a verified owner API, explicit permission, idempotency key and audit receipt.
- **Provenance/Status Layer:** standardizes source, revision, as-of, freshness, access classification and status.
- **AI Collaboration View:** separates assigned, dispatch-requested, delivered, ACKed, running, done, verified, blocked and unknown. No inferred online state.
- **Observability:** correlation ID, request timing, source health, denied requests and client errors; no secrets or sensitive payloads in logs.

### E. Domain authority and integration rules
| Domain | Authority rule | W113 integration rule |
|---|---|---|
| Identity / authorization | Core or verified owning authorization service | Consume authenticated identity and policy decisions; never mint or elevate identity |
| Company | Company-owning Work/service | Read through its published contract only |
| Sandbox / Works | Each Work's canonical records and owning service | Show Work metadata/projections; no direct filesystem or SQLite access |
| Meeting | W71 / Meeting-owning service | Use meeting-scoped contracts; no duplicate meeting store |
| AI collaboration | Verified identity, assignment, dispatch and execution owners | Display distinct lifecycle evidence; never treat delivery as ACK or ACK as execution |
| System health | Each service's health/telemetry owner | Display source timestamp and confidence; no synthetic live state |

Candidate Works are dependencies to verify, not presumed integrations. No endpoint name, schema or permission is invented by this architecture. Missing owner contract means NOT VERIFIED / NOT AVAILABLE and remains read-only.

### F. Data and status contract
Every data projection must preserve:
- `domain`, `resource_id`, `source_system`, `source_ref`, `source_revision`;
- `as_of`, `fetched_at`, `freshness`, `status`;
- `access_classification`, `correlation_id`;
- optional owner-provided `schema_version`.

Canonical display states include `VERIFIED`, `RECORDED`, `PENDING`, `STALE`, `UNKNOWN`, `UNAVAILABLE`, `NOT_AUTHORIZED`, `ERROR`. A successful UI fetch is not proof that source data is authoritative. Missing provenance renders UNKNOWN; stale snapshots remain visibly stale.

### G. Security and privacy baseline
- Deny by default; enforce authorization server-side for each Work, resource and action.
- Separate authentication, role membership, assignment, Work scope and action permission.
- Do not rely on client route hiding, local-storage flags, URL obscurity or shared bearer tokens as authorization.
- No secrets in browser bundles, query strings, logs or screenshots.
- Apply least privilege, session expiry, CSRF protections where cookie-based, safe CORS, CSP, output encoding, dependency pinning and audit for sensitive operations.
- Work Dashboard and Product Dashboard may link but must not share credentials/session state by implication.
- Cross-Work isolation tests must attempt horizontal access to another Work's data and routes.
- Until verified identity/authorization contracts exist, use no live privileged command path.

### H. Responsive Web and Mobile
- One responsive Web application is the baseline; desktop navigation collapses to touch-friendly mobile navigation.
- Use semantic HTML, keyboard support, focus management, screen-reader labels, contrast and reduced-motion support.
- PWA/native packaging, offline writes and push notifications remain deferred until user/device needs and owning service capabilities are verified.
- Mobile viewport E2E is required even if native packaging is not selected.

### I. Auto E2E delivery and CI
Each vertical slice follows: source baseline → implementation → static/type/lint checks → unit/component tests → schema/contract tests → integration tests against controlled test services → browser E2E → responsive/accessibility/security checks → artifact publication → defect fix → full regression rerun.

Required automated lanes:
1. **PR gate:** dependency lock integrity, formatting/lint, type/static checks, unit/component tests, schema validation and secret/dependency scan.
2. **Contract lane:** versioned fixtures and consumer/provider compatibility tests; mocks explicitly marked TEST_ONLY.
3. **Integration lane:** isolated test services or verified staging APIs; no production mutation.
4. **Browser lane:** pinned browser automation, desktop and mobile viewports, navigation, data states, access-denied and outage flows.
5. **Security lane:** unauthenticated, wrong-role, wrong-Work, expired-session, CSRF/CORS and XSS/input handling tests as applicable.
6. **Accessibility lane:** automated accessibility checks plus keyboard/focus and semantic checks; manual screen-reader review remains independent evidence.
7. **Artifact lane:** JUnit/XML, browser traces/screenshots, console/network logs, build manifest, commit SHA, dependency lock hash and run metadata.
8. **Regression:** any defect fix reruns the failing test and full affected suite; no test weakening or deletion merely to get green.

Every test record binds to exact repository, branch, commit SHA, workflow run ID, environment, command, exit code and artifact URL. CI PASS is not live-service PASS. Browser E2E against test doubles is not production integration E2E. No auto-deploy is included.

### J. Source and release model
- Canonical W113 product source path: `work/113/ROOM-HOP-UNIVERSAL-DASHBOARD/05_BUILD/04_CODE/product/`.
- Implementation branch: `work/113/room-hop-universal-dashboard-auto-e2e`, created from main at `8339f1f2a004704e76b163acd8db66d6d596cef1`.
- Work governance records remain on main; product source changes use the implementation branch and PR/review. Never push product code directly to main.
- Sandbox mirrors are synchronized after each meaningful source/document change; exact GitHub fetch/readback is mandatory.
- Release artifacts and deployment configuration are separate deliverables and are not authorized by the Auto E2E build delegation.

### K. Architecture decisions and unresolved verification
| ID | Decision / disposition |
|---|---|
| ADR-113-01 | One shared port-3000 ingress for all authorized Work Dashboards — adopted as product requirement; existing host owner/runtime NOT VERIFIED |
| ADR-113-02 | One Universal Product Dashboard shell with domain modules — baseline adopted |
| ADR-113-03 | Work Dashboard and Product Dashboard remain separate responsibilities — mandatory per W70 DOC-085 |
| ADR-113-04 | Domain-owned APIs/Bridge only; no direct DB/filesystem — mandatory |
| ADR-113-05 | Provenance/freshness and explicit UNKNOWN/STALE/UNAVAILABLE states — mandatory |
| ADR-113-06 | Auto E2E CI with exact-SHA artifacts; no auto-deploy — delegated delivery baseline |
| ADR-113-07 | Responsive Web first; PWA/native deferred — baseline |

Open blockers before live integration: current :3000 listener and startup ownership; canonical identity/auth provider and server-side claims; actual Gateway/Bridge routes and schemas; Company/Sandbox/Meeting API contracts; route registration owner; browser runner availability; deployment/release owner and rollback contract.

**Architecture status:** W113 DESIGN BASELINE RECORDED BY DELEGATED ARCHITECT; CONTRACTS/RUNTIME NOT VERIFIED; independent architecture/security review pending.  
**Build status:** delegated Auto E2E mandate active; implementation may proceed only after exact source baseline and applicable owner/gate authorization are evidenced.  
**Acceptance:** Vinh only.


---

## Addendum — correction: source and runtime baseline are not yet reconciled (2026-11-21)

A prior PC trace retrieved from the conversation record on 2026-11-20 reported:
- Root Vite entry: root `index.html` → `/dashboard/main.tsx`; root `package.json` and `vite.config.js`; strict port-3000 configuration.
- The `dashboard/` tree (including `dashboard/room-hop/` and `dashboard/entry/`) and root `package.json` / `vite.config.js` were untracked in local Git status.
- Local `main` was at `05db862cd2ff01cd288cf64cf0be5a9aa05ee816`, 728 commits behind; Node v24.18.0 and npm 11.16.0; `dashboard/package.json` and `dashboard/node_modules` absent.
- Last port-3000 probe reported no listener; HTTP/TCP connection refused.
- `start-dev.ps1` was reported to check `dashboard/package.json` although the Vite package is at repository root.
- Two SessionLifecycleBridge implementations reportedly diverged (one restores latest draft on F5; the other returns null); mock and real RoomHOP bridges coexist; persistence was reported optimistic with errors logged but no demonstrated rollback/readback.

**Evidence classification:** prior-session PC observations only; not freshly re-run or independently read from PC in this session. W1111 owns technical tracing and repair of runtime/source issues; W113 owns product architecture and product behavior.

**Correction to Section J above:** the W113 source path and branch declared in D-113-006 are candidate/staging only until the local root Vite tree is read-only inventoried and exact hashes are mapped. Do not build a second app in parallel or overwrite the local tree. Final product source integration must preserve the existing Vite entry and route/bridge work after the source owner and branch strategy are verified.

**Port 3000 disposition:** shared ingress remains a product requirement. The last reported PC probe found no active listener, so it is incorrect to describe port 3000 as currently serving the Dashboard. The process owner, startup command, route registry and server-side auth contract remain NOT VERIFIED. No process/listener change has been made.

**Current architecture status:** logical design baseline recorded; source topology and runtime deployment not verified; PC source reconciliation and W1111 technical handoff are required before selecting the final implementation integration point.
