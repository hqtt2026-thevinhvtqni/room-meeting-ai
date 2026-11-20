# TASK BOARD — WORK 117 ROOM MEDIA HUB
- Work ID: 117
- Canonical task board: this file only
- Product authority: Vinh
- Coordinator: Xu / AI-01
- Date: 2026-11-17
- Status: W117 DASHBOARD BUILD AUTHORIZED (DASHBOARD SCOPE ONLY); MEDIA HUB PRODUCT BUILD NOT AUTHORIZED
- Last updated by: Vibe (2026-11-17 11:42 +07) — GitHub support pass: snapshot refresh + Xu audit fixes 1–6; Vibe ACK recorded in Journal

## Status legend
PLANNED = defined, not started; ASSIGNED — DISPATCH UNCONFIRMED = allocated in canonical board, agent receipt not verified; ACKNOWLEDGED = agent explicitly accepted; READY = dependencies and authorization satisfied; IN_PROGRESS = evidence-backed work underway; BLOCKED = cannot proceed and blocker is recorded; DONE = task action completed; PASS = verification criterion passed; FAIL = verification failed; NOT RUN = no test executed; NOT AUTHORIZED = requires explicit approval.

## Active task register
| Task ID | Work Package | Task / deliverable | Accountable owner (proposed) | Dependencies | Acceptance / evidence | Status |
|---|---|---|---|---|---|---|
| W117-T001 | WP01 | Maintain one canonical architecture/context and decision set; reconcile all existing architecture notes into the Plan/Minutes without creating a second plan | Xu; Cla technical assurance | Current audit and requirements | Architecture decisions, open items and source evidence reconciled | IN_PROGRESS |
| W117-T002 | WP03/WP04/WP06 | Re-verify W33 source and current service/API state; distinguish implemented from proposed contracts | Cla | Repo/source access | File/commit references, commands/method, findings and limits in Journal | PLANNED |
| W117-T003 | WP06 | Verify actual Core identity/authorization contract and supported integration path | Cla; Ka reviews | Core source/runtime access | Contract evidence and positive/negative test plan; no assumed endpoints | BLOCKED — access/evidence not verified |
| W117-T004 | WP07 | Review threat model, privacy, per-Work access, encryption/key ownership and fail-closed behavior | Ka | Architecture package | Independent CSA findings with severity and mitigation | BLOCKED — reviewer dispatch/acceptance not verified |
| W117-T005 | WP12 | Define independent QE strategy and measurable acceptance criteria for all P0 requirements | Qw | Requirements and architecture draft | Traceability matrix, test cases, test data and pass/fail thresholds | BLOCKED — reviewer dispatch/acceptance not verified |
| W117-T006 | WP01/WP04/WP11 | Compare internal/Cloud topology, provider-neutral adapter, zero-cost options and billing risk | Xu coordinates; Go candidate reviewer | Cost/provider evidence | Evidence-backed comparison; no provider selected without approval | IN_PROGRESS |
| W117-T007 | WP02/WP03/WP04/WP06/WP07/WP08/WP09/WP10/WP11 | Verify Go's primary Builder dispatch/access/acceptance and Vibe's independent architecture-review + GitHub support dispatch/access/acceptance | Xu | Candidate capability and access verification | Go named as primary Builder; Vibe named as independent challenger/support Builder; separate acceptance and access evidence | IN PROGRESS — Go ACK recorded 2026-11-17; Vibe still unverified |
| W117-T008 | WP01 | Finalize architecture baseline and ADR package for Vinh's decision | Xu; Cla reconciles; Ka reviews | T001–T007 | Review findings reconciled; risks/options and recommendation recorded | NOT READY |
| W117-T009 | WP02/WP03/WP04/WP06/WP07 | Foundation implementation after gate approval | Go primary Builder; Vibe supports assigned GitHub tasks; Qc coder | T008 and explicit Vinh BUILD authorization | Code, migrations, contracts, tests and review evidence | NOT AUTHORIZED |
| W117-T010 | WP05/WP08/WP09 | Media processing, gallery UI and search | Go primary Builder; Vibe supports assigned GitHub tasks; Qc coder | T009; approved UX/API contracts | Browser E2E, processing and search evidence | NOT AUTHORIZED |
| W117-T011 | WP10/WP11 | Backup/recovery and operational deployment pipeline | Go primary Builder; Cla technical review/repair; Vibe supports assigned GitHub tasks | T009; approved operational targets | Restore rehearsal, CI, observability and cost guard evidence | NOT AUTHORIZED |
| W117-T012 | WP12 | Independent regression, security, integration, E2E and recovery verification | Qw; An support if available | T009–T011 | Test report, defect disposition and independent recommendation | NOT RUN |
| W117-T013 | All | Product acceptance, release and operations handoff | Vinh final authority; Xu coordinates | T012 PASS/disposition | Explicit Vinh acceptance and release approval | NOT AUTHORIZED |

## Role boundaries
- Cla: technical reconciliation, planning, repair, code review and debugging; not default feature builder.
- Go: selected primary Builder; accountable for construction leadership. Go has explicitly ACKNOWLEDGED Dashboard scope and delivered working package (2026-11-17).
- Vibe: selected independent architecture challenger and supporting Builder on GitHub; can challenge Go's design and contribute assigned code. Dispatch, task acceptance and access still require evidence.
- Qc: implementation coding for authorized UI/Backend tasks.
- Qw: independent testing and acceptance recommendation; no self-approval of own implementation.
- Ka: independent CSA/security reviewer.
- Xu: coordinator and owner of canonical records; cannot approve on Vinh's behalf.
- Vinh: final authority for architecture gate, BUILD, cost exposure, real-media test, deployment and release.

## Blocker register
| Blocker | Impact | Evidence / current state | Resolution owner | Next action |
|---|---|---|---|---|
| Reviewer dispatch channel unavailable/unverified | Architecture/security/QE reviews cannot be claimed complete | Prior Custom Agent discovery returned entitlement_required; no accepted review evidence recorded | Xu | Find authorized dispatch path or record reviewer unavailable and propose mitigation |
| Builder dispatch/access not verified | Implementation cannot start until the selected lead and support roles have working access and accepted tasks | Vinh selected Go as primary Builder and Vibe as independent architecture challenger/support Builder; Go ACK + working package recorded 2026-11-17; Vibe still unverified | Xu | Verify Vibe GitHub access; record explicit acceptance |
| Core contract not verified | Authorization integration cannot be safely designed as implemented | Existing docs describe intended authority; actual supported path remains unverified | Cla | Inspect source/runtime and record exact evidence |
| Storage provider and internal target unresolved | Hybrid build topology and cost remain open | Zero-cost screening is documentary only; no provider selected | Xu / Go candidate | Complete T0 screening design; request Vinh approval before account/API/test activity |
| Measurable NFRs unresolved | Performance/recovery acceptance thresholds cannot be set | Capacity, max file size, throughput, RPO/RTO and retention not yet approved | Xu; Qw proposes | Prepare evidence-based options for Vinh decision |

## Update protocol
Every task state change must be reflected here and appended to the single canonical Journal. Decisions affecting scope, authority, cost or gates must also be recorded in the single canonical Minutes. Do not create another task tracker or shadow plan.


## W117 DASHBOARD — USER-AUTHORIZED BUILD TRACK (2026-11-17)
- Authority: Vinh directly instructed Xu to assign all Dashboard work into this canonical Task Board and Journal, with Agents to proceed independently through completion without waiting for repeated prompts.
- Scope: Build a dedicated, read-only operational Dashboard for Work 117 only. It monitors W117 progress, task status, assigned agents and evidence. This is NOT the ROOM-wide/HQTT dashboard and does not expand the media product scope.
- BUILD authorization: GRANTED by Vinh for the W117 Dashboard only. This does not authorize implementation of the underlying ROOM MEDIA HUB product tasks T009–T011, paid services, billing/payment setup, cloud account/token creation, real-media upload, production deployment or release.
- Canonical inputs: this TASK_BOARD.md and 00_ROOT/NHAT_KY_THI_CONG.md. Dashboard must not invent progress or or infer an Agent is online/active from role assignment. Agent acceptance/session/activity may be shown only when supported by verifiable runtime evidence. Until such evidence exists, show "DISPATCH/ACK NOT VERIFIED".
- Operating rule: parallelize independent review/build tasks; Go owns delivery and resolves integration. Qc implements assigned UI/Backend slices. Cla, Ka and Qw perform independent assurance in their domains. No repeated user confirmation is needed for work inside this scope. Escalate only hard blockers, security/privacy concerns, irreversible external actions, or anything outside this authorization.
- Delivery target: working local/preview Dashboard with source provenance, followed by independent QE and technical/security review. Production deployment/release remains separately gated.

### Dashboard task register
| Task ID | Deliverable | Accountable owner | Contributors / reviewers | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|---|
| W117-DASH-001 | Own end-to-end Dashboard delivery; define minimal read-only data contract and coordinate integration | Go / AI-06 | Xu | User authorization recorded here | Working package + Journal + evidence | **DONE (implementation)** — awaiting independent reviews |
| W117-DASH-002 | Build Dashboard shell, Work Overview and task board views using canonical W117 task data | Go / AI-06 | Qc / Qwen Coder | DASH-001 data contract | UI source + snapshot counts match Task Board | **DONE (implementation)** |
| W117-DASH-003 | Build Agent Monitor with explicit assignment/dispatch/ACK/session/activity evidence states | Go / AI-06 | Qc; Cla verifies runtime contract | DASH-001 | Agent cards show provenance; unverified states explicit | **DONE (implementation)** |
| W117-DASH-004 | Build Activity & Evidence timeline from canonical Journal with traceable source references | Go / AI-06 | Qc | Journal parsing contract | Timeline maps to Journal entries | **DONE (implementation)** |
| W117-DASH-005 | Independent technical review of data flow, source-of-truth rules, failure behavior and maintainability | Cla / AI-03 | Go provides implementation evidence | DASH-001 and evolving implementation | Findings, severity, evidence and required fixes appended to Journal | ASSIGNED — DISPATCH UNCONFIRMED |
| W117-DASH-006 | Independent CSA review: read-only access, authorization boundary, data exposure and fail-closed behavior | Ka / AI-02 | Cla; Go | Data contract and preview build | CSA findings and remediation disposition recorded; no sensitive data exposure | ASSIGNED — DISPATCH UNCONFIRMED |
| W117-DASH-007 | Define independent QE matrix and measurable acceptance criteria | Qw / AI-05 | Xu | DASH-001; can draft in parallel | Traceability matrix and test cases covering overview, tasks, agents, timeline, stale/missing data and error states | ASSIGNED — DISPATCH UNCONFIRMED |
| W117-DASH-008 | Execute independent functional/regression/accessibility/data-integrity tests; verify fixes | Qw / AI-05 | Go accountable for fixes; Qc implements fixes | Testable preview build | Test logs, reproducible evidence, defect list and PASS/FAIL recommendation | ASSIGNED — DISPATCH UNCONFIRMED |
| W117-DASH-009 | Integrate, reconcile findings, complete handoff package and mark Dashboard complete only after evidence | Go / AI-06 | Xu coordinates; Cla/Ka/Qw sign off their domains | DASH-002–008 | Working preview, source revision, evidence, known limitations, independent QE PASS and technical/security disposition | IN_PROGRESS — package ready; waiting independent sign-off |
| W117-DASH-010 | Vibe GitHub support: refresh snapshot from canonical Task Board/Journal; apply Xu audit fixes (KPI derivation, Xu runtime state, HTML escaping, focus visibility, README data-source alignment) | Vibe | Go integrates; Cla/Ka/Qw review as part of DASH-005–008 | Vinh's standing instruction (build through unconfirmed items, record debts) | EVIDENCE/DASHBOARD_AUDIT_FIX_20261117_VIBE.md; Journal entry 2026-11-17 11:42 +07 | DONE (implementation) — awaiting independent review |

### Dashboard role allocation
- Go / AI-06: single accountable Builder and integration lead; drives all Dashboard tasks to completion. **Explicit ACK + working package delivered 2026-11-17.**
- Qc: UI/Backend implementation partner under Go's task breakdown.
- Cla / AI-03: technical assurance and runtime-contract verification; not the feature lead.
- Ka / AI-02: independent CSA/security review.
- Go / AI-06: default QE/QA owner under D70-026; does not independently review Go-authored implementation.
- Vibe: architecture challenger and optional GitHub support on a clearly scoped task; no delivery dependency unless access and acceptance are verified.
- Xu / AI-01: coordinator, canonical records and blocker resolution; does not substitute record writes for Agent dispatch.
- Vinh: final authority outside the explicitly granted Dashboard build scope.

### Dispatch and acceptance truth
The current ROOM-HOP Build MCP tool surface available to Xu exposes Sandbox read/write/list operations but no Agent task-dispatch or session-assignment operation. Therefore the allocations above are authoritative task assignments, but are NOT evidence that any Agent has received or accepted them unless an explicit ACK is recorded in the Journal (as Go did on 2026-11-17). Unverified agents remain "ASSIGNED — DISPATCH UNCONFIRMED". Do not mark an Agent IN_PROGRESS merely because its name appears here.

Recorded ACKs: Go / AI-06 (2026-11-17 05:55 +07, Journal); Vibe (2026-11-17 11:42 +07, Journal — self-ACK of the DASH-010 support scope). All other agents remain DISPATCH UNCONFIRMED.

### Working package location
```
05_BUILD/04_CODE/dashboard/
├── index.html | run.py | README.md
├── data/snapshot.json
├── assets/dashboard.css | dashboard.js
└── tests/test_snapshot.py

EVIDENCE/DASHBOARD_PREVIEW_20261117.md
```
Run: `cd 05_BUILD/04_CODE/dashboard && python tests/test_snapshot.py && python run.py` → http://127.0.0.1:8170/

