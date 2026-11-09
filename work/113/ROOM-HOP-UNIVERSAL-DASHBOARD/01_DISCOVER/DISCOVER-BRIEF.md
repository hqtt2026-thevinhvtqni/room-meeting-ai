# W113 DISCOVER BRIEF
- Document ID: DOC-006 | Priority: P1 | Read order: 6 | Status: DRAFT — DISCOVERY IN PROGRESS
- Date: 2026-11-09 | Product Owner: Vinh | Orchestrator: Xu

## Problem
ROOM-HOP has distinct Company, Sandbox and Meeting spaces, but lacks an identified unified user-facing control surface that lets authorized humans and AI participants understand and navigate the whole system across Web and Mobile.

## Users
- Human: Product Owner, company/Work operators, reviewers and members, according to assigned permissions.
- AI: Xu/orchestrator, architects, coders, QE and other registered agents, each restricted to role and assignment scope.
- Exact role catalogue and authorization claims: to be discovered from authoritative identity and permission services.

## Product hypothesis
One responsive Dashboard can present a unified global overview and role-adaptive views across Company, Sandbox, Meeting and system control, while leaving authoritative data and actions with owning services.

## Existing scope inspected
- W0000: Company governance and portfolio dashboard snapshot; README says read-only projection and explicitly not live/portfolio-wide release certificate.
- W70: mandatory Work lifecycle and Work Dashboard/Product Dashboard distinction; DOC-085 forbids conflating Work and Product dashboards.
- W71: next-generation Meeting product; separate scope.
- Work inventory: 61 entries returned by ROOM-HOP 8030. Inventory snapshot DOC-018 in W0000 is dated 2026-11-03, 56 entries, explicitly not fully reconciled.
- Full 61-Work product-scope audit: NOT COMPLETED.

## Discovery questions
1. What are the verified APIs/contracts and authorization boundaries for Company, Sandbox, Meeting, Core and system health?
2. What is the canonical identity/role/permission source for humans and AI?
3. Which operations are read-only and which commands can be safely delegated to domain services?
4. What are the supported Web/Mobile delivery targets and browser/device baselines?
5. What freshness, offline, notification and audit guarantees are available?
6. Which existing screens/components can be reused without duplicating domain ownership?

## Risks / unknowns
- API/Bridge capabilities and live status are NOT VERIFIED.
- Work 0000 portfolio snapshot is stale relative to current inventory.
- Sandbox MCP 8030 context states Working Source is read-only and AI cannot merge/commit/push; GitHub canonical registration is pending.
- No product source repository/path has been declared.
- Native mobile vs responsive/PWA strategy is not decided.

## Discovery exit criteria
Complete a scoped system/source inventory; inspect relevant Work manifests and architecture; trace actual APIs, auth and data ownership; document confirmed capabilities vs unknowns; reconcile overlaps; obtain a reviewable evidence-backed problem and user map.
