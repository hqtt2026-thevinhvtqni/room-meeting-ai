# TASK BOARD — WORK 117 ROOM MEDIA HUB
- Work ID: 117
- Canonical task board: this file only
- Product authority: Vinh
- Coordinator: Xu / AI-01
- Date: 2026-11-17
- Status: PLANNING — BUILD NOT AUTHORIZED

## Status legend
PLANNED = defined, not started; READY = dependencies and authorization satisfied; IN_PROGRESS = evidence-backed work underway; BLOCKED = cannot proceed and blocker is recorded; DONE = task action completed; PASS = verification criterion passed; FAIL = verification failed; NOT RUN = no test executed; NOT AUTHORIZED = requires explicit approval.

## Active task register
| Task ID | Work Package | Task / deliverable | Accountable owner (proposed) | Dependencies | Acceptance / evidence | Status |
|---|---|---|---|---|---|---|
| W117-T001 | WP01 | Maintain one canonical architecture/context and decision set; reconcile all existing architecture notes into the Plan/Minutes without creating a second plan | Xu; Cla technical assurance | Current audit and requirements | Architecture decisions, open items and source evidence reconciled | IN_PROGRESS |
| W117-T002 | WP03/WP04/WP06 | Re-verify W33 source and current service/API state; distinguish implemented from proposed contracts | Cla | Repo/source access | File/commit references, commands/method, findings and limits in Journal | PLANNED |
| W117-T003 | WP06 | Verify actual Core identity/authorization contract and supported integration path | Cla; Ka reviews | Core source/runtime access | Contract evidence and positive/negative test plan; no assumed endpoints | BLOCKED — access/evidence not verified |
| W117-T004 | WP07 | Review threat model, privacy, per-Work access, encryption/key ownership and fail-closed behavior | Ka | Architecture package | Independent CSA findings with severity and mitigation | BLOCKED — reviewer dispatch/acceptance not verified |
| W117-T005 | WP12 | Define independent QE strategy and measurable acceptance criteria for all P0 requirements | Qw | Requirements and architecture draft | Traceability matrix, test cases, test data and pass/fail thresholds | BLOCKED — reviewer dispatch/acceptance not verified |
| W117-T006 | WP01/WP04/WP11 | Compare internal/Cloud topology, provider-neutral adapter, zero-cost options and billing risk | Xu coordinates; Go candidate reviewer | Cost/provider evidence | Evidence-backed comparison; no provider selected without approval | IN_PROGRESS |
| W117-T007 | WP02/WP03/WP04/WP06/WP07/WP08/WP09/WP10/WP11 | Verify Go's primary Builder dispatch/access/acceptance and Vibe's independent architecture-review + GitHub support dispatch/access/acceptance | Xu | Candidate capability and access verification | Go named as primary Builder; Vibe named as independent challenger/support Builder; separate acceptance and access evidence | IN PROGRESS — role decision made; execution acceptance/access still unverified |
| W117-T008 | WP01 | Finalize architecture baseline and ADR package for Vinh's decision | Xu; Cla reconciles; Ka reviews | T001–T007 | Review findings reconciled; risks/options and recommendation recorded | NOT READY |
| W117-T009 | WP02/WP03/WP04/WP06/WP07 | Foundation implementation after gate approval | Go primary Builder; Vibe supports assigned GitHub tasks; Qc coder | T008 and explicit Vinh BUILD authorization | Code, migrations, contracts, tests and review evidence | NOT AUTHORIZED |
| W117-T010 | WP05/WP08/WP09 | Media processing, gallery UI and search | Go primary Builder; Vibe supports assigned GitHub tasks; Qc coder | T009; approved UX/API contracts | Browser E2E, processing and search evidence | NOT AUTHORIZED |
| W117-T011 | WP10/WP11 | Backup/recovery and operational deployment pipeline | Go primary Builder; Cla technical review/repair; Vibe supports assigned GitHub tasks | T009; approved operational targets | Restore rehearsal, CI, observability and cost guard evidence | NOT AUTHORIZED |
| W117-T012 | WP12 | Independent regression, security, integration, E2E and recovery verification | Qw; An support if available | T009–T011 | Test report, defect disposition and independent recommendation | NOT RUN |
| W117-T013 | All | Product acceptance, release and operations handoff | Vinh final authority; Xu coordinates | T012 PASS/disposition | Explicit Vinh acceptance and release approval | NOT AUTHORIZED |

## Role boundaries
- Cla: technical reconciliation, planning, repair, code review and debugging; not default feature builder.
- Go: selected primary Builder; accountable for construction leadership. Dispatch, task acceptance and access still require evidence.
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
| Builder dispatch/access not verified | Implementation cannot start until the selected lead and support roles have working access and accepted tasks | Vinh selected Go as primary Builder and Vibe as independent architecture challenger/support Builder; no execution acceptance/access evidence yet | Xu | Dispatch separate scopes; verify Go build access and Vibe GitHub access; record explicit acceptance |
| Core contract not verified | Authorization integration cannot be safely designed as implemented | Existing docs describe intended authority; actual supported path remains unverified | Cla | Inspect source/runtime and record exact evidence |
| Storage provider and internal target unresolved | Hybrid build topology and cost remain open | Zero-cost screening is documentary only; no provider selected | Xu / Go candidate | Complete T0 screening design; request Vinh approval before account/API/test activity |
| Measurable NFRs unresolved | Performance/recovery acceptance thresholds cannot be set | Capacity, max file size, throughput, RPO/RTO and retention not yet approved | Xu; Qw proposes | Prepare evidence-based options for Vinh decision |

## Update protocol
Every task state change must be reflected here and appended to the single canonical Journal. Decisions affecting scope, authority, cost or gates must also be recorded in the single canonical Minutes. Do not create another task tracker or shadow plan.
