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
