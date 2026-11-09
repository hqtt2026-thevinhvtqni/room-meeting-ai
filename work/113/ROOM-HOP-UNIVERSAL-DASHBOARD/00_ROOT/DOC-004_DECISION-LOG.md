# W113 DECISION LOG
- Document ID: DOC-004 | Priority: P0 | Read order: 4 | Status: ACTIVE
- Authority: Vinh, Product Owner. Xu may make routine reversible decisions within delegated scope.

## D-113-001 — Unified role-adaptive Dashboard (2026-11-09)
- Decision: Adopt option C — one Dashboard product whose navigation, data projection and permitted actions adapt to the authenticated user's role and permissions.
- Experience: Web and Mobile are two responsive access modes of one product, not separate products.
- Product areas: Global Home, Company, Sandbox, Meeting and Control Center.
- Human and AI experiences are role-specific projections, not separate applications.
- Rationale: one consistent control surface while preserving domain ownership and authorization boundaries.
- Status: DECIDED by user confirmation in conversation; formal Work Entry and architecture verification remain open.

## D-113-002 — Preserve existing domain ownership (2026-11-09)
- Core and each owning domain remain authoritative. Dashboard consumes verified authorized APIs/Bridge contracts only.
- No direct database/filesystem access; no duplicate Core or parallel source of truth.
- W70 Work dashboards and W0000 portfolio dashboard remain distinct products/operational projections; W71 remains owner of its Meeting product scope.
- Status: DESIGN BASELINE; detailed API and permission contracts NOT VERIFIED.

## D-113-003 — W70 is mandatory delivery standard (2026-11-09)
- Adopt W70 lifecycle, gates, Work Entry, WP planning, documentation, evidence, verification, acceptance and release controls.
- W113 implementation is not authorized by creation alone.
- Status: ADOPTED AS GOVERNING BASELINE; per-participant Work Entry NOT ASSESSED.
