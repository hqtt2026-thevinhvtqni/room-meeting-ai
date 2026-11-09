# W113 PRODUCT ARCHITECTURE — INITIAL BASELINE
- Document ID: DOC-008 | Priority: P1 | Read order: 8 | Status: DRAFT — CONTRACTS NOT VERIFIED
- Date: 2026-11-09

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

## Integration discovery — OPEN
No endpoint, event, API version, permission scope, live service status or runtime path is approved by this draft. Inspect source and runtime evidence before binding UI to a contract.

## Mobile strategy — OPEN
Responsive Web is the baseline requirement. PWA/native packaging decision is deferred until user journeys, offline/notification requirements, device support and available infrastructure are verified.

## Architecture decisions required before BUILD
1. Identity and role claim source.
2. API gateway/Bridge and service-by-service contracts.
3. Company/Sandbox/Meeting data ownership and field-level permissions.
4. Command/event model and audit.
5. Web deployment, mobile strategy and supported device matrix.
6. Observability, freshness, caching, offline and failure semantics.
7. Threat model, privacy, accessibility and performance budgets.
