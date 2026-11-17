# KẾ HOẠCH TRIỂN KHAI — WORK 502 MÊ
- Document ID: W502-PLAN-001
- Version: 0.1
- Date: 2026-11-18
- Status: PROVISIONAL; BUILD NOT AUTHORIZED

## Objective
Deliver a private, auditable MÊ pilot that accepts one user request and completes a bounded vertical slice using AutoGPT Platform under ROOM-HOP control.

## Phases and gates
| Phase | Scope | Exit criteria | Status |
|---|---|---|---|
| P0 Discover | Read Work 70 standards and source contracts of Core, Gateway, Agent Runtime, Sandbox/Execution Host and related Works | Source-backed inventory, overlap map, unknowns | IN PROGRESS |
| P1 Define | PRD, user journeys, roles, assumptions, failure behavior and measurable DONE criteria | Requirements reconciled and approved | PLANNED |
| P2 Architect | AutoGPT version/license, adapter, identity/task mapping, model plane, tool gateway, data/evidence and security | ADRs closed or explicitly accepted; independent reviews reconciled | IN PROGRESS |
| P3 Plan | WPs, ownership, dependencies, budget, rollback and test plan | Work package plan and resource envelope approved | PLANNED |
| G-BUILD | Implementation authorization | Explicit Vinh approval after design and risk review | NOT READY |
| P4 Build | Minimal adapter + one role workflow + isolated workspace + evidence path | Build evidence and reproducible pilot | NOT AUTHORIZED |
| P5 Verify | Unit/integration/browser/E2E/security/recovery checks | Independent QA report; no unresolved P0/P1 defects | NOT AUTHORIZED |
| P6 Accept | User-flow demonstration and acceptance decision | Explicit acceptance with evidence | NOT AUTHORIZED |
| P7 Release | Private preview first; production only after separate approval | Release manifest, health checks, rollback and handoff | NOT AUTHORIZED |
| P8 Operate | Monitoring, backup, upgrades, incident and cost controls | Operational readiness | NOT AUTHORIZED |

## Initial work packages
- WP-502-01: ROOM-HOP contract discovery and source trace.
- WP-502-02: AutoGPT Platform release, license and security due diligence.
- WP-502-03: Work 501 integration contract and model policy.
- WP-502-04: MÊ architecture and role/workflow contracts.
- WP-502-05: identity/task/session adapter and audit design.
- WP-502-06: sandbox/tool gateway and permission model.
- WP-502-07: state, memory, evidence and dashboard design.
- WP-502-08: QA strategy, security test matrix and recovery.
- WP-502-09: independent review and reconciliation.
- WP-502-10: controlled lifecycle folder normalization.
- WP-502-11: minimal vertical-slice pilot (only after G-BUILD).
- WP-502-12: acceptance, private preview, release and handoff (only after gates).

## Cost and resource policy
Default budget ceiling for paid services = 0 until separate approval. Estimate CPU/RAM/disk, Docker storage, model memory/VRAM, electricity, bandwidth, backup and maintenance before installation. Local inference is not assumed costless. No model downloads or container deployment in this design phase.

## Pilot success criteria (proposed)
1. One natural-language request creates a traceable PRD and task graph without unnecessary clarification.
2. Every assumption is visible and reversible; high-risk unknowns stop for authorization.
3. Manager executes at least one complete role workflow through the AutoGPT adapter.
4. Source changes are confined to an isolated workspace with a reproducible diff.
5. QA runs objective automated checks and records logs/screenshots; Coder cannot self-approve.
6. Repair loop is bounded to three attempts per unchanged approach and terminates safely.
7. Model/provider selection is policy-controlled through Work 501; paid fallback is impossible by default.
8. ROOM-HOP identity and authorization remain authoritative.
9. Task state and evidence are recoverable after worker restart.
10. No public deployment occurs without separate approval; handoff reports completed, incomplete and blocked scope honestly.

## Dependencies
Work 70 standards; Work 501 model capability plane; ROOM-HOP Core/Gateway/Agent Runtime; Work 22 security; Work 14 E2E builder; Work 15 website builder; Work 16 workflow engine; Work 30 autonomous build team; Work 50 delivery standard. Reuse decisions require source inspection, not name-based assumptions.