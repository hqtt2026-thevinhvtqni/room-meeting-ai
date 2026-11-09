# W113 PRODUCT REQUIREMENTS
- Document ID: DOC-007 | Priority: P1 | Read order: 7 | Status: DRAFT — NOT APPROVED
- Product: ROOM-HOP Universal Dashboard | Date: 2026-11-09

## Product objective
Provide one secure, coherent, role-adaptive control surface for ROOM-HOP across Web and Mobile.

## Functional requirements (proposed)
- FR-01 Global Home summarizes verified system health, Work progress, active/idle/blocked agent status, pending decisions, alerts and evidence freshness.
- FR-02 Provide unified navigation to Company, Sandbox and Meeting.
- FR-03 Company views show only authorized organization, member, role and governance data from Company-owned contracts.
- FR-04 Sandbox views show Work portfolio, Work status, WP progress, blockers and evidence references without replacing each Work's canonical records or W70 Work Dashboard.
- FR-05 Meeting views show authorized meeting lists, sessions, participants and outputs using Meeting-owned contracts; do not reimplement W71.
- FR-06 Control Center presents service health, integration state, security events, permission-aware alerts and audit references from verified sources.
- FR-07 Adapt navigation, data and available actions to authenticated identity, role, assignment and permissions. Never rely on hidden UI alone for security.
- FR-08 Human and AI modes are role-specific projections within one product.
- FR-09 Responsive Web and Mobile experiences share API contracts, identity and authorization; mobile interaction is designed for small screens and one-handed use.
- FR-10 Any command/action is routed through the owning service with server-side authorization, validation and audit; default views are read-only.
- FR-11 Display provenance, source mode, as-of time, revision and freshness; represent UNKNOWN, STALE, NOT VERIFIED and unavailable explicitly.
- FR-12 Provide notifications and pending approvals only where verified event/notification contracts exist.
- FR-13 Support accessibility, localization and resilient loading/error/empty states.
- FR-14 No direct DB/filesystem access and no secrets in client code, logs or evidence.
- FR-15 Preserve distinct Work Dashboard vs Product Dashboard responsibilities under W70 DOC-085.

## Non-functional requirements (proposed)
Security by default, least privilege, fail-closed authorization, auditability, accessibility, responsive performance, freshness visibility, reliability, maintainability and testability.

## Non-goals
Rebuilding domain services; changing authoritative Work lifecycle; replacing W0000 governance, W70 Work dashboards or W71 Meeting; introducing unverified APIs; claiming native app support before technical decision.

## Acceptance criteria (draft)
- AC-01 Role matrix is derived from verified identity/authorization sources and enforced server-side.
- AC-02 Each module's data source, owner, API contract, permission and freshness semantics are documented.
- AC-03 No unauthorized cross-module data leakage in positive and negative tests.
- AC-04 No Dashboard path writes authoritative domain state except approved commands routed through owner APIs.
- AC-05 Global Home indicators are traceable to source records and timestamps; no mock data presented as live.
- AC-06 Work, Company and Meeting views preserve domain boundaries and link to canonical products.
- AC-07 Web and Mobile workflows pass defined responsive/device/browser test matrix.
- AC-08 Accessibility, error, empty, stale and offline states are verified.
- AC-09 Independent QE and security review pass with evidence.
- AC-10 Vinh explicitly accepts release after W70 gates and evidence are satisfied.

All requirements remain proposed until DISCOVER and DEFINE gates are completed.
