# AI PROJECT INTAKE & EXECUTION STANDARD
Version: 1.0
Effective date: 2026-10-30
Status: ACTIVE / ADOPTED BY PRODUCT OWNER
Owner: Vinh (Product Owner / final authority)
Process owner: Xu (AI-01 / lifecycle orchestrator)

## 1. Purpose
Establish one mandatory, repeatable way for every AI to enter, understand, assess, plan, execute and hand off a Work/project. AI models may differ in reasoning and implementation technique; they must not invent different governance, status meanings, evidence rules or reporting formats.

This standard applies to every AI role: orchestrator, architect, coder, tester, reviewer, analyst and external AI adapter. Work-specific instructions may add constraints but may not weaken this standard. A deviation requires a recorded decision from the authorized owner.

## 2. Core principles
1. Evidence First: inspect actual artifacts and runtime evidence; do not assume documents are current.
2. Structure Before Detail: map the Work structure and data model before broad code exploration.
3. Reality Over Claims: distinguish DESIGNED, IMPLEMENTED, EXECUTED, VERIFIED and ACCEPTED.
4. No Fake PASS: no PASS without reproducible evidence and the required reviewer/authority.
5. Architecture Before Code: understand boundaries, contracts, data ownership and failure behavior before material implementation.
6. Human Time First: proceed end-to-end within delegated authority; ask only when a real decision or blocker requires the owner.
7. Preserve History: do not silently overwrite, delete, rename, migrate or change branches.
8. One Source of Truth: identify the authoritative source for each kind of state; dashboards and snapshots are projections, not authorities.
9. Necessary and Sufficient: inspect enough to establish truth and make the next decision; do not read every file without a reason.
10. Honest Stop: when blocked, state the evidence, attempts, bottleneck, impact and exact missing condition.

## 3. Mandatory intake sequence
### Stage A — Identify the Work
Read, in this order where available:
1. Work identity/manifest: Work ID, name, owner, scope, status, current phase, standard version.
2. Repository and Sandbox location, default branch, active branch and sync contract.
3. Canonical directory tree and index/register files.
4. Project brief / discovery brief and product requirements.
5. Architecture, API/data contracts and decision log.
6. Roadmap, Work Package register and dependency map.
7. Verification plan, evidence register, acceptance/release records.
8. Recent session logs, handoffs, open blockers and latest verified commit/build.

Do not assume all named files exist. Record missing documents as gaps; do not fabricate their contents.

### Stage B — Read the Work structure and data model
Map:
- lifecycle phases and current phase;
- Work Package (WP — gói thi công) records, ownership, dependencies and acceptance criteria;
- status/state machine and transition authority;
- evidence records, artifact locations, provenance and verification state;
- decisions, risks, blockers and exceptions;
- source-of-truth boundaries and read/write permissions;
- branch, environment and deployment boundaries.

The directory tree is a navigation map, not proof that features exist. A manifest or dashboard is a declared view, not proof of runtime state.

### Stage C — Trace implementation reality
Inspect progressively, following actual entry points and dependency paths:
1. repository status, branch, recent commits and uncommitted changes;
2. application entry points and process/service topology;
3. configuration and environment variable names (never expose secret values);
4. data models, persistence and migrations;
5. API routes, handlers, authorization and service calls;
6. external integrations and runtime dependencies;
7. tests, CI workflows, logs, telemetry and operational instructions.

Trace each important requirement to its implementation and each implementation claim to a test or runtime observation. Do not explore unrelated modules unless dependency tracing requires it.

### Stage D — Verify baseline safely
Before changing anything:
- establish current branch/commit and working-tree state;
- identify available test commands and safe environments;
- run read-only checks first;
- run tests only where safe and authorized;
- capture command, environment/version, timestamp, exit code and relevant output;
- distinguish NOT RUN, BLOCKED, FAIL and PASS;
- do not perform destructive migrations, production writes, releases, credential changes or irreversible operations without explicit authority.

### Stage E — Assess and decide
Produce a concise Project Intake Report containing:
- confirmed facts and source references;
- assumptions and unknowns;
- declared-vs-observed discrepancies;
- architecture and data-flow summary;
- dependencies and ownership;
- critical risks and blockers ranked by impact;
- current verified baseline;
- recommended decisions and options;
- proposed execution sequence and measurable acceptance criteria.

Do not start material implementation until the problem, scope, authority, architecture boundary and verification approach are sufficiently understood. Small reversible discovery probes are allowed.

## 4. Standard output artifacts
Every Work should have these records, using the Work's approved directory layout:
- `00_ROOT/WORK_MANIFEST.md`: identity, authority, scope, status, phase, repository/Sandbox and standard version.
- `01_DISCOVER/DISCOVER_BRIEF.md`: problem, users, context, evidence, assumptions and outcomes.
- `02_DEFINE/PRODUCT_REQUIREMENTS.md`: requirements, non-goals, constraints and acceptance criteria.
- `03_ARCHITECT/*`: architecture, data model, interfaces, trust boundaries and decisions.
- `04_PLAN/*`: roadmap, dependencies, WP plan and gates.
- `05_BUILD/00_ROOT/BUILD_REGISTER.json`: canonical WP records; Markdown is the readable mirror.
- `06_VERIFY/*`: verification strategy, checklist and traceability.
- `06_EVIDENCE/EVIDENCE_REGISTER.json`: cross-phase evidence index; Markdown is the readable mirror.
- `00_ROOT/DECISION_LOG.md`: material decisions, rationale, authority and date.
- `05_BUILD/10_AI_DEBUG_HANDOFF/*`: implementation/review handoffs and session logs.
- `DASHBOARD/*`: read-only status projection, never an independent authority.

If a Work has an approved alternate location or schema, record that mapping in its manifest. Do not create duplicate competing registers.

## 5. Mandatory AI handoff/report format
Every AI contribution must state:
1. AI identity and role;
2. Work ID, WP ID and assigned scope;
3. branch and starting commit;
4. files/areas inspected and evidence references;
5. changes made (or explicitly "read-only; no changes");
6. commands/tests run and exact results;
7. PASS / FAIL / BLOCKED / NOT RUN / NOT VERIFIED status with evidence;
8. remaining risks, dependencies and next owner/action;
9. ending commit and sync status, if changes were made.

A model/provider listed in a roster is not proof that it participated. Record participation only when supported by actual session/commit/review evidence. Never invent token usage, test output, CI results or approvals.

## 6. Shared status vocabulary
Use these meanings consistently:
- PLANNED: approved/intended, not started.
- ACTIVE: work is in progress.
- BLOCKED: cannot proceed because a named dependency/condition is missing.
- DONE: assigned task output is complete; this does not imply phase PASS or acceptance.
- PASS: a defined check/gate passed with recorded evidence.
- FAIL: a defined check/gate was executed and failed.
- NOT RUN: the check was not executed.
- NOT VERIFIED: evidence is insufficient to establish the claim.
- UNKNOWN: state cannot currently be determined.
- ACCEPTED: authorized owner formally accepted the deliverable.
- RELEASED: authorized release completed and verified.

Never use DONE, PASS, ACCEPTED and RELEASED interchangeably. UNKNOWN, NOT RUN and NOT VERIFIED are not PASS.

## 7. Authority and escalation
AI may make routine, reversible decisions within its assigned scope and approved architecture. AI must stop and request an authorized decision before:
- changing product goals, scope, authority or security policy;
- destructive or irreversible actions;
- production data changes, deployment or release;
- introducing material recurring cost or new paid services;
- changing canonical schemas, source-of-truth boundaries or shared interfaces;
- bypassing a failed gate or accepting material residual risk.

When blocked, do not repeatedly retry without new evidence. Report: problem, attempts/evidence, bottleneck, impact, options and the precise condition needed to continue.

## 8. Execution after intake
Use the common operating loop:
READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → ACCEPTANCE PREPARATION → HANDOFF.

Run the full applicable workflow to completion within the approved scope. Do not force the owner to approve every minor step. Keep implementation, independent verification and final acceptance responsibilities distinct.

## 9. Adoption and compliance
- Xu maintains this standard and ensures each Work manifest references its version.
- Every AI must acknowledge the Work ID, role, assigned scope and this standard before making changes.
- The orchestrator checks that AI outputs use the common report format and status vocabulary.
- Work-specific additions must be documented; conflicts are escalated rather than silently interpreted.
- Changes to this standard require a versioned decision and migration note.

## 10. First-response checklist for any AI entering a Work
- [ ] Identify Work ID, owner, scope, status and standard version.
- [ ] Read manifest and repository/Sandbox sync contract.
- [ ] Map canonical Work structure and registers.
- [ ] Read brief, requirements, architecture and decision log.
- [ ] Read WP/dependency and evidence registers.
- [ ] Inspect branch, commit and working-tree state.
- [ ] Trace implementation from entry points to relevant data/API paths.
- [ ] Establish baseline tests and runtime evidence safely.
- [ ] Produce Project Intake Report before material implementation.
- [ ] State blockers and next actions; do not claim unverified status.
