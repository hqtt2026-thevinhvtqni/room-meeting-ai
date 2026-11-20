# W113 — KẾ HOẠCH TRIỂN KHAI / IMPLEMENTATION ROADMAP
- Document ID: DOC-009 | Priority: P1 | Read order: 9
- Version: 2.0
- Updated: 2026-11-12 22:20 UTC+7
- Status: APPROVED PLAN BASELINE — BUILD NOT AUTHORIZED
- Work: 113 — ROOM-HOP-UNIVERSAL-DASHBOARD
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu / AI-01
- Governing standard: W70 lifecycle, gates, Work Package, evidence and acceptance rules
- Canonical plan: this document only; no parallel implementation plan is authorized.

## 1. Mission and product boundary

Build one unified, role-adaptive ROOM-HOP Dashboard for Web and Mobile, presenting authorized views across:
- Global Home / system overview.
- Company.
- Sandbox / Works.
- Meeting.
- Control Center (health, alerts, permissions and operational status).
- AI collaboration visibility: AI roster, assignments, ACK, progress, handoff, blockers, review and evidence, only where verified owning-service contracts exist.

W113 owns the unified presentation experience, navigation, read projections, dashboard-specific interaction and integration orchestration at the client/Bridge boundary. W113 does NOT become a second Core, identity provider, authorization authority, Task Registry, Agent Runtime, Execution Host, Meeting engine, Work lifecycle store or evidence database.

The multi-AI collaboration capability is surfaced and integrated by W113; underlying assignment, identity, execution authority, run ledger and meeting records remain with their verified owning services. If an owner/API is not verified, show NOT AVAILABLE / NOT VERIFIED and record a blocker; do not simulate live operation.

## 2. Governing decisions and constraints

1. One Dashboard product with role/permission-adaptive projections; Web and Mobile are access modes of the same product.
2. Core and each domain service remain authoritative for records and rules they actually own.
3. Dashboard reads only through verified, authorized API/Bridge contracts.
4. State-changing actions are disabled by default and may be enabled only through the owning service's authenticated, authorized and audited command contract.
5. No direct database or filesystem access from Dashboard; no secrets in client code.
6. Do not duplicate W70 Work Execution Dashboard, W70 Product Dashboard, W0000 governance dashboard or W71 Meeting product.
7. Reuse existing ROOM services only after manifest, source and contract verification; Work names alone do not prove a usable integration.
8. Unknown, stale, unavailable and unverified data must be explicit. No mock presented as live.
9. No implementation, source mutation, deployment, migration or release before Work Entry and required lifecycle gates are verified and authorized.
10. Every material action and verification is recorded in DOC-005 with time, participant, scope, method, evidence, status and next step.

## 3. Delivery phases and Work Packages

| Phase | WP | Objective / deliverables | Exit criteria | Status |
|---|---|---|---|---|
| P0 — PLAN BASELINE | WP-113-00 | Approve this roadmap; confirm product boundary, authority, no-build constraints and decision owners | Vinh approval recorded; plan readback verified | APPROVED |
| P1 — DISCOVER & CONSULT | WP-113-01 | Inventory Company, Sandbox, Meeting, Core, identity, permission, Gateway/Bridge, AI collaboration and dashboard surfaces; collect independent AI reviews; map overlap with W0000/W52/W70/W71/W114 and relevant runtime Works | FACT/ASSUMPTION/BLOCKED register; source/owner map; consultation comparison and unresolved questions | IN PROGRESS |
| P2 — DEFINE | WP-113-02 | Confirm user journeys, personas, role/permission matrix, product requirements, responsive Web/Mobile requirements, KPI definitions and acceptance criteria | Requirements reviewed; data/action ownership and user journeys traceable; DEFINE gate evidence | PLANNED |
| P3 — ARCHITECT & CONTRACTS | WP-113-03 | Verify identity/auth, API/Bridge contracts, domain schemas, events, freshness, errors, audit, command safety, session/ACK/handoff projections and mobile delivery strategy | Architecture decision approved; each integration has owner, contract/version, permission, source and failure semantics; ARCHITECT gate evidence | PLANNED |
| P4 — DELIVERY DESIGN | WP-113-04 | Establish UI information architecture, navigation, responsive design system, component contracts, API adapter strategy, observability, security and test matrix; identify canonical product source repository/path | Baseline design, dependency graph, WP estimates and risk register; canonical source and build workflow authorized | PLANNED |
| P5 — FOUNDATION BUILD | WP-113-05A | Build shared app shell, authenticated session handling, role-aware navigation, loading/error/empty/stale states and read-only data adapter foundation | Contract tests and security checks pass for foundation; no mock/live confusion; build gate authorized | NOT AUTHORIZED |
| P6 — DOMAIN INTEGRATION | WP-113-05B | Integrate Global Home, Company, Sandbox/Work, Meeting and Control Center through verified domain contracts; link to canonical domain products where appropriate | Per-domain contract, authorization, provenance and freshness tests pass; no duplicate domain state | NOT AUTHORIZED |
| P7 — AI COLLABORATION PROJECTION | WP-113-05C | Display AI identities/roles, task assignments, dispatch/ACK, execution status, handoff, blockers, review and evidence only from verified owning-service contracts; route permitted actions to owner services | Authenticated source, lifecycle semantics and audit verified; unknown capabilities shown honestly; no W113-owned duplicate Task/Run database | NOT AUTHORIZED |
| P8 — VERIFY & HARDEN | WP-113-06 | Independent contract, authz, cross-domain isolation, security, browser, mobile, accessibility, performance, failure/recovery and regression testing | Reproducible evidence per test; independent QE and security findings closed or explicitly accepted by Vinh | NOT RUN |
| P9 — ACCEPT & RELEASE | WP-113-07 / WP-113-08 | Product Owner acceptance, deployment readiness, release, rollback and operational handoff | All required gates PASS; release authorization and rollback/monitoring evidence | NOT AUTHORIZED |
| P10 — OPERATE | WP-113-09 | Monitor availability, latency, freshness, errors, access denials, audit, support and improvement backlog | Operational ownership, SLO/alerts and incident procedure accepted | PLANNED |

## 4. AI consultation and responsibility model

- Vinh: Product Owner and final decision/acceptance authority.
- Xu / AI-01: lifecycle orchestration, scope decomposition, synthesis, dependency/risk management and gate recommendation; cannot self-approve independent QA.
- Ka / AI-02: independent architecture/security boundary review.
- Cla / AI-03: technical/runtime feasibility and code/security review when assigned.
- Kha / AI-04: product strategy, user journeys and product requirements.
- Qw / AI-05: independent QE, test strategy and acceptance evidence.
- Go / AI-06: cost, operational risk and independent assurance within demonstrated capability.
- Co / AI-07, Vi and Qc: implementation support only after build authorization and scoped assignments.
- An: test execution support under Qw/independent QE direction.
- Mê / other consultants: independent architecture input; consultation does not grant implementation authority.

Actual identity, capability, session reachability and permission must be verified at assignment time. A role label is not an authorization credential. No AI may approve its own implementation.

## 5. Candidate integration dependencies — NOT YET VERIFIED

W0000 (company/governance), W01 (Gateway), W02 (authorization), W11 (AI member/identity adapter), W12/W13/W14 (execution environment/host/build runtime), W16 (workflow), W52 (AI communication/A2A), W70 (lifecycle and Work/Product Dashboard standards), W71 (Meeting), W76 (triggers/automation), W102 (agent loop), W114 (graph/provenance).

These are discovery candidates, not approved dependencies or evidence of available APIs. Xu must inspect current manifests, owners, source revisions, contracts and runtime evidence before binding W113 to any of them. W113 must not absorb another Work's authority or create duplicate registries.

## 6. Required architecture and delivery decisions before BUILD

- Canonical W113 product source repository/path and branch policy.
- Verified identity provider and server-side role/permission claims.
- Dashboard API/Bridge contract and service-by-service data ownership.
- Company, Sandbox/Work, Meeting and Control Center schemas and authorization.
- AI collaboration source of truth for assignment, transport receipt, authenticated ACK, execution, handoff, review and evidence.
- Whether each AI provider supports existing-session dispatch, session continuation or only explicit handoff/API adapter.
- Read/write/execute/commit permissions, grant lifecycle, expiry and revocation for any command exposed by UI.
- Provenance, source revision, freshness, caching, stale behavior and audit.
- Responsive Web baseline; PWA/native decision only after device, offline and notification needs are evidenced.
- Threat model, privacy, accessibility, performance budgets, observability and rollback.

Any missing critical contract remains BLOCKED; do not invent an endpoint or silently substitute a mock.

## 7. Verification and acceptance

Required test streams:
1. API/schema/version and contract behavior for each domain.
2. Authentication, role, assignment and resource-level authorization; deny-by-default.
3. Cross-domain isolation and unauthorized data-leakage tests.
4. Dashboard provenance, revision, freshness, stale/unknown/unavailable states.
5. AI collaboration projection correctness: delivery vs ACK vs execution vs DONE vs VERIFIED.
6. Command safety, idempotency, audit and server-side enforcement for any enabled action.
7. Browser functional, responsive, regression and supported-browser tests.
8. Mobile viewport/device, touch, accessibility and performance tests.
9. Accessibility including keyboard and screen-reader coverage.
10. Timeout, partial outage, lost session, retry, recovery and stale-cache behavior.
11. Independent QE/security review and Vinh's explicit acceptance.

Every evidence record must include timestamp, environment/build revision, scope/input, command or method, expected and actual result, exit code where applicable, artifact/log reference and PASS/FAIL/BLOCKED/NOT RUN. A plan, screenshot, mock, successful file write or ACK alone is not a product PASS.

## 8. Gate controls

- G0 / Work Entry: NOT ASSESSED. Must verify required Work Entry evidence, scope, owner, source boundary and authorization.
- G1 / Discovery: not passed until source inventory, owner map, user/problem evidence and blockers are reviewed.
- G2 / Define: not passed until requirements, user journeys, roles and acceptance criteria are baselined.
- G3 / Architecture: not passed until contracts, authority boundaries, security and canonical source are reviewed and approved.
- G4 / Build: NOT AUTHORIZED. Opens only after required prior gates and explicit build authorization.
- G5 / Verify/Accept/Release: not passed until independent evidence, owner acceptance and release controls are complete.

Current known baseline from W113 records: product source NOT DECLARED; API/runtime contracts NOT VERIFIED; G0–G5 NOT ASSESSED; UI implementation NOT STARTED; Browser/Mobile E2E NOT RUN; Independent QE NOT RUN; Acceptance/Release NOT AUTHORIZED.

## 9. Immediate next actions

1. Xu reconciles the W113 consultation set, including Mê's input and independent reviews from Ka, Cla, Kha, Qw, Go and implementation specialists where useful.
2. Xu checks W52/W70/W114 and candidate service manifests/contracts; records only verified facts and explicit unknowns.
3. Xu updates DOC-006/DOC-007/DOC-008 only when discovery evidence supports the changes; do not rewrite them speculatively.
4. Xu prepares the architecture recommendation and unresolved decision list for Vinh.
5. After Vinh's architecture decision, update DOC-004 and the official minutes/register as required; verify W70 Work Entry and G0–G3.
6. Only then request/open G4 build authorization and assign implementation WPs.

## 10. Approval and status

Vinh approved the W113 implementation-plan baseline in conversation on 2026-11-12. This approval applies to the plan and sequencing only. It does not approve the final technical architecture, does not issue a build grant and does not authorize source changes, deployment, migration or release.

**Plan status: APPROVED PLAN BASELINE.**
**Architecture status: CONSULTATION / RECONCILIATION IN PROGRESS.**
**Build status: NOT AUTHORIZED.**
