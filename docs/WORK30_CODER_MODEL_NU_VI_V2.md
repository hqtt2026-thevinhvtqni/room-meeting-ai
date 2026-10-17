# WORK 30 — TWO-CODER EXECUTION MODEL V2

- Decision: W30-DEC-005
- Recorded by: Xu — Plan Synthesizer / Coordinator
- Timestamp: 2026-10-17 21:40 UTC+07:00
- Status: MODEL RECORDED; LIVE DISPATCH AND END-TO-END EXECUTION NOT YET VERIFIED

## 1. Roles
### Nu — Autonomous Coder / end-to-end executor
Nu owns the approved implementation flow from discovery through handoff:
1. Read the Vinh-approved Plan and relevant Work context/evidence.
2. Trace the existing environment, repository, dependencies, service boundaries and current state before changing code.
3. Build the complete approved flow rather than stopping at a phase checklist.
4. Run available tests and runtime checks; capture reproducible evidence.
5. Detect failures and produce a defect report with reproduction steps, logs, expected/actual behavior, impact and suspected cause.
6. Hand off unresolved defects to Vi and provide exact files/commit/test evidence.
7. Re-run end-to-end verification after Vi's repair and report final status honestly.

### Vi — Repair Coder
Vi owns targeted repair work when Nu or An provides a reproducible defect:
1. Acknowledge a specific defect/task ID.
2. Trace root cause before editing; do not patch symptoms blindly.
3. Make the smallest safe fix consistent with the approved Plan and architecture.
4. Add/update regression tests where appropriate.
5. Run targeted tests and report changed files, test commands/results, remaining risks and commit/patch evidence.
6. Return the repair to Nu for E2E re-verification. Vi does not self-certify overall release acceptance.

## 2. Independent quality gates
- An (Tester): independently verifies the expected behavior and regression after the repair; provides evidence, not unsupported PASS labels.
- Ka (Reviewer): reviews architecture, security, code quality, scope compliance and evidence integrity.
- Xu: maintains the approved Plan, tracks status and synthesizes reports. Xu does not replace Nu's implementation, Vi's repair, An's test or Ka's independent review.
- Vinh: approves the Plan and any material scope/architecture changes.

## 3. Defect loop
Approved Plan -> Nu traces/builds -> Nu runs E2E -> defect evidence -> Vi repairs -> targeted regression -> Nu re-runs E2E -> An independently tests -> Ka reviews -> evidence-based handoff.

Loop limits:
- Every repair cycle has a defect/task ID and a stated acceptance criterion.
- If the same defect fails twice after a repair, or a new architecture/scope decision is required, stop patch cycling and return the decision to Vinh/Xu for a Plan update.
- Never loop indefinitely or claim PASS without a successful check and inspectable evidence.
- No change to production, protected files, secrets, or irreversible external state without the permissions and controls already required by the Work environment.

## 4. Task contract
Every Nu/Vi task must include:
- Work ID and unique task/defect ID
- approved Plan item
- expected outcome and acceptance criteria
- exact scope/files/environment
- dependencies and safety constraints
- test commands and evidence locations
- assigned identity, created/sent time, receipt ACK and final report
If delivery or identity-bound receipt cannot be verified, status is BLOCKED; a storage write is not a receipt ACK.

## 5. Status vocabulary
- DONE: requested action completed with artifact evidence.
- PASS: defined test/check ran and passed, with evidence.
- BLOCKED: cannot proceed due to a named dependency/permission/tool/evidence gap.
- PENDING: not yet executed or verified.
- DECISION: requires Vinh's explicit decision.
Never infer one status from another.

## 6. Current status
This document defines the Nu/Vi division of responsibilities. It does not prove that Nu or Vi has received this protocol, has started a task, or has completed an E2E run. Live dispatch, identity-bound ACK, and an end-to-end demonstration remain PENDING/NOT VERIFIED.

[Signed: XU — PLAN SYNTHESIZER / COORDINATOR]
