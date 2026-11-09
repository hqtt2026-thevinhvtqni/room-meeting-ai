# WORK MANIFEST — W113
- Document ID: DOC-001
- Priority: P0 | Read order: 1 | Status: ACTIVE — INITIALIZED / DISCOVER IN PROGRESS
- Version: 1.1 | Updated: 2026-11-09
- Work ID: 113
- Work Name: ROOM-HOP-UNIVERSAL-DASHBOARD
- Product Name: ROOM-HOP Universal Dashboard
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu (ROOM-HOP identity: xu; HQTT role: AI-01)
- Governing Standard: Work 70 — ROOM-HOP Product Lifecycle & Work Dashboard
- Standard baseline: W70 canonical lifecycle, gates, documentation, evidence and dashboard rules
- Sandbox: Work 113 via ROOM-HOP Build MCP 8030
- GitHub Work records repository: hqtt2026-thevinhvtqni/room-meeting-ai
- GitHub Work records canonical path: work/113/ROOM-HOP-UNIVERSAL-DASHBOARD/ on main
- Product source repository/path: NOT DECLARED; existing PL.room-meeting-ai.dash is a candidate for discovery only, not yet adopted as W113 canonical source
- Product Dashboard: W113 product itself; canonical source NOT DECLARED

## Purpose
Build the unified, role-adaptive ROOM-HOP user-facing dashboard for Web and Mobile, presenting Company, Sandbox and Meeting through one coherent control surface.

## Scope
- Global Home and system overview.
- Company, Sandbox and Meeting navigation and authorized views.
- Control Center for system health, alerts, permissions and operational status.
- Role-adaptive experiences for human users and AI agents.
- Responsive Web and Mobile experience, with a shared product/API contract.
- Provenance, freshness, auditability, accessibility and secure authorization.

## Non-goals
- Rebuild or replace ROOM-HOP Core, Company, Sandbox, Meeting, Execution Host or existing services.
- Duplicate W70 Work Execution Dashboard, W70 Product Dashboard, W0000 Company Governance Dashboard or W71 Meeting product.
- Create a second source of truth, direct database access, direct filesystem access, or bypass authorization.
- Claim live data, mobile-native packaging, API availability or production readiness without verification.

## Architecture principles
- Core/domain services remain authoritative for their own records and business rules.
- Dashboard reads through verified, authorized API/Bridge contracts only.
- Any state-changing command must pass the owning service's authorization and audit controls.
- Human/AI views are role-based projections of one product, not separate products.
- Unknown, stale, unavailable and unverified data must be shown honestly.
- Web and Mobile share identity, permissions, domain contracts and source provenance.

## Initial status
- Lifecycle phase: 01_DISCOVER
- G0–G5: NOT ASSESSED / NOT PASS
- Product source: NOT DECLARED
- Core API contracts: NOT VERIFIED
- UI implementation: NOT STARTED
- Browser E2E / Mobile E2E: NOT RUN
- Independent QE: NOT RUN
- Acceptance / Release: NOT AUTHORIZED

## Initial structure note
The creation tool supplied a legacy scaffold (01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE). Those entries are preserved; they are not treated as the W70 canonical lifecycle structure. The W70-aligned structure is being instantiated alongside them. No legacy path is deleted or silently renamed.
