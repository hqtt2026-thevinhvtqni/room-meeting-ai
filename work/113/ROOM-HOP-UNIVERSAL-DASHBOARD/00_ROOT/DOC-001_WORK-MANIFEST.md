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
- Product source repository/path: NOT DECLARED. The separate repository `hqtt2026-thevinhvtqni/PL.room-meeting-ai.dash` is an independent earlier project, unrelated to W113; it is NOT a W113 source, candidate, dependency, migration target or code reference.
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


## Product source baseline — delegated Auto E2E delivery (2026-11-21)
- **Canonical repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`.
- **Canonical product source path:** `work/113/ROOM-HOP-UNIVERSAL-DASHBOARD/05_BUILD/04_CODE/product/`.
- **Implementation branch:** `work/113/room-hop-universal-dashboard-auto-e2e`, created from GitHub main at commit `8339f1f2a004704e76b163acd8db66d6d596cef1` and fetched at the same SHA at branch creation.
- **Work records:** remain under `work/113/ROOM-HOP-UNIVERSAL-DASHBOARD/` on main; code changes are isolated to the implementation branch and delivered through PR/review, not direct code commits to main.
- **Boundary:** `DASHBOARD/` remains the W113 Work Dashboard read-only projection; it is not the Universal Dashboard product source. Product code belongs under `05_BUILD/04_CODE/product/`.
- **Source status:** canonical location and branch are declared; product implementation has not yet been created. No claim of build, runtime or E2E PASS.
- **Excluded source:** `hqtt2026-thevinhvtqni/PL.room-meeting-ai.dash` remains an unrelated earlier project and is not adopted, copied, migrated or used as a dependency.
- **Authority:** D-113-005 / D-113-006 and assignment `ASG-W113-CO-AUTOE2E-20261121`; Co owns W113 architecture/implementation under the recorded boundaries; Vinh retains final acceptance.


## Source baseline correction — local PC Vite application reconciliation (2026-11-21)
**Correction to the preceding source-baseline addendum:** the path `work/113/ROOM-HOP-UNIVERSAL-DASHBOARD/05_BUILD/04_CODE/product/` and branch `work/113/room-hop-universal-dashboard-auto-e2e` are a **W113 isolated candidate/staging location**, not yet the final canonical source baseline.

A prior PC trace in the conversation record (2026-11-20) reported an existing root Vite application: root `package.json` and `vite.config.js`, `index.html` importing `/dashboard/main.tsx`, and an untracked `dashboard/` tree including `dashboard/room-hop/`. The same trace reported local `main` at `05db862cd2ff01cd288cf64cf0be5a9aa05ee816`, 728 commits behind, and untracked `dashboard/`, `app_workspace/`, `package.json` and `vite.config.js`. It also reported no listener on port 3000 at the last probe. These are **historical PC findings from the prior session, not freshly re-attested in this session**.

Therefore:
- Do not treat the new GitHub branch (based on main commit `8339f1f2a004704e76b163acd8db66d6d596cef1`) as containing the local root Vite application.
- Do not pull, reset, clean, checkout, overwrite or delete the local dirty/untracked tree.
- The final canonical product source must be selected only after read-only PC inventory and exact path/hash/revision reconciliation of the existing root Vite app, then recorded in Manifest and Decision Log.
- The candidate W113 source path/branch may be retained as an isolated design/build staging area, but do not create a competing second application or duplicate the existing Dashboard shell.
- The current :3000 host is not live at the last historical probe; startup/route owner remains NOT VERIFIED. No listener change or runtime restart is authorized by this source-path declaration.
