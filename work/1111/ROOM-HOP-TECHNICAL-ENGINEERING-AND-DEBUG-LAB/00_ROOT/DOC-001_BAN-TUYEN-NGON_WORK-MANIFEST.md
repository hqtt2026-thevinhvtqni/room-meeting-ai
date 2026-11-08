# WORK MANIFEST — WORK 1111
- **Document ID:** DOC-001
- **Priority:** P0
- **Read order:** 1
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-11-08
- **Work ID:** 1111
- **Work Name:** ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB
- **Display Name:** 1111 — ROOM-HOP Technical Engineering & Debug Lab
- **Work Type:** Shared technical engineering / debugging / integration lab
- **Created:** 2026-11-08
- **Product Owner / Final Authority:** Vinh
- **Lifecycle / Technical Coordinator:** Xu (registered identity: xu)
- **Canonical GitHub Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Canonical GitHub Work Path:** work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/
- **Canonical Branch for Work records:** main
- **Sandbox Work ID:** 1111
- **Sandbox root:** ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/
- **Baseline GitHub revision inspected before initialization:** dc87d852920514357f082b9615c050733699e847

## 1. Purpose
A shared engineering room where Xu and authorized ROOM-HOP AI participants inspect, trace, diagnose, design, build, test, review and hand off technical changes across ROOM-HOP.

## 2. Scope
- ROOM-HOP repository, source architecture, service contracts and runtime boundaries.
- GitHub / Sandbox / PC source-of-truth and synchronization model.
- Core, Dashboard, Workspace, Gateway, Event Listener, Agent Runtime, MCP Build and Execution Host.
- AI registry, identity, principal, policy, token and task handoff.
- CI/CD, runners, unit/integration/browser E2E and evidence quality.
- Cross-Work technical blockers, root-cause analysis, regression prevention and integration.

## 3. Non-goals and boundaries
- Not a product/business Work; product-specific lifecycle artifacts are included only when useful.
- GitHub is canonical for source code and Work records; Sandbox is the shared AI collaboration/workspace layer.
- PC/runtime is an execution environment, not a canonical source merely because a process is running.
- No silent overwrite, reset, cleanup, migration, deletion or branch switch.
- No code push directly to main by AI agents. Code changes use scoped branches and review/PR. Work governance records may be updated on main within this approved initialization scope.
- No modification of other Works except explicitly scoped, evidence-backed coordination.
- No PASS without reproducible evidence.

## 4. Operating sequence
READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → HANDOFF.

## 5. Source-of-truth model
| Information | Canonical home |
|---|---|
| Work identity, scope, governance and decisions | GitHub Work 1111 00_ROOT |
| Chronological Work activity | GitHub 00_ROOT/DOC-003 |
| Shared AI working copies and collaboration | Sandbox Work 1111 |
| Source code | Repository/path declared by the relevant component or Work |
| Test evidence | Exact-SHA CI/runtime evidence linked from Work 1111 |
| PC runtime state | Read-only runtime attestation with PID/build hash/time; never inferred from source files |
| Dashboard/status projection | Read-only view derived from canonical records |

## 6. Lifecycle status
- Work status: ACTIVE.
- DISCOVER: PARTIAL.
- Architecture baseline: PARTIAL.
- BUILD: NOT STARTED as a Work 1111 implementation stream.
- Verification: NOT RUN for this GitHub initialization.
- Acceptance/release: NOT IN SCOPE / NOT RELEASED.

## 7. Core records
See DOC-009 Document Register. The official minutes, plan and journal each have one canonical location. Sandbox files are collaboration copies to be reconciled by exact readback; they are not a second GitHub authority.
