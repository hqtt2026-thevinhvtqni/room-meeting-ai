# Work 31 — ROOM-HOP WORKFLOW MODEL

- **Work ID:** W31
- **Status:** ACTIVE — DESIGN / BASELINE
- **Owner / final authority:** Vinh
- **Coordinator / Planner:** Xu
- **Implementation role:** Vi (Coder)
- **Verification role:** An (Tester)
- **Review role:** Ka (Reviewer)
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Working branch:** `work/31-room-hop-workflow-model`
- **Created:** 2026-10-18 (UTC+7)
- **Scope note:** This is the initial charter, not proof that a runtime workflow has been implemented or tested.

## 1. Mission

Design, document, and validate a reusable workflow model for ROOM-HOP so each Work can move from request to verified handoff through explicit states, role ownership, gates, and evidence.

W31 designs the workflow standard. It does not replace the responsibilities or execution systems of W12, W27, W28, or other Works.

## 2. Operating principles

1. **Human Time First:** minimize repeated manual micro-commands and make blockers/action owners explicit.
2. **Evidence First:** never report PASS without inspectable evidence.
3. **Documentation First:** record decisions, work logs, and handoff outcomes.
4. **Architecture Before Code:** agree on scope, contracts, and acceptance criteria before implementation.
5. **One source of truth per Work:** identify its canonical context, branch, artifacts, and evidence.
6. **Explicit authority:** Vinh retains final approval; no unapproved scope expansion or integration to `main`.
7. **Honest status:** use DONE / PASS / DECISION / BLOCKED; distinguish planned, implemented, and verified.

## 3. Proposed standard lifecycle

`RECEIVE → READ → TRACE → ANALYZE → PLAN → DECIDE → ASSIGN → BUILD → VERIFY → REVIEW → HANDOFF`

| Stage | Required output / exit gate |
|---|---|
| RECEIVE | Request, requester, date/time, objective captured |
| READ | Relevant Work context, constraints, and existing artifacts inspected |
| TRACE | Dependencies, source-of-truth locations, and execution path identified |
| ANALYZE | Current state, risks, unknowns, and scope documented |
| PLAN | Smallest viable plan, role owners, acceptance criteria, and rollback/recovery path |
| DECIDE | Explicit decision/approval recorded where required |
| ASSIGN | Named AI/person, role, task, expected evidence, and due/checkpoint |
| BUILD | Changes made only in the authorized Work context/branch |
| VERIFY | Tests and end-to-end checks run; commands, outputs, artifacts, and hashes recorded where appropriate |
| REVIEW | Independent review against scope and acceptance criteria |
| HANDOFF | DONE/PASS/DECISION/BLOCKED summary, evidence links, remaining risks, next owner |

A stage may be skipped only when the Work log records why it is unnecessary. Failed gates return to the appropriate earlier stage; they do not silently advance.

## 4. Status semantics

- **DONE:** the stated task or artifact was completed.
- **PASS:** defined acceptance checks were executed and passed with evidence.
- **DECISION:** an explicit human or designated authority decision is required or recorded.
- **BLOCKED:** progress cannot continue; state the cause, evidence, owner, and next action.
- **PROPOSED / NOT RUN:** planned or documented only; not implemented or verified.

Do not equate file creation, unit tests, a green CI run, or a report from an agent with full end-to-end PASS unless that is exactly what the acceptance criteria require.

## 5. Required Work record

Each Work should record:
- Work ID, objective, scope, out-of-scope items, owner, and status.
- AI/person identity, role, timestamp (UTC+7 where that is the team convention), action, and outcome.
- Decisions and approvals, including who authorized them.
- Acceptance criteria, test commands/results, evidence locations, and known gaps.
- Current blocker, next action, and named next owner.
- Handoff summary and integration approval state.

## 6. W31 deliverables

1. Workflow lifecycle and state-transition specification.
2. Role and responsibility matrix for Planner, Coder, Tester, Reviewer, and final approver.
3. Work intake / execution / verification / handoff templates.
4. Gate rules and evidence contract, including when PASS is permitted.
5. Exception, retry, blocked-state, and recovery workflow.
6. Mapping of the standard model to ROOM-HOP services and existing Works without duplicating their responsibilities.
7. Test plan and evidence demonstrating that the model is usable in a real Work.

## 7. Initial acceptance criteria

- [ ] Lifecycle states and legal transitions are documented.
- [ ] Each stage has an owner, required input/output, and exit criteria.
- [ ] PASS/BLOCKED decisions are evidence-based and auditable.
- [ ] Templates support AI identity, timestamps, decisions, and handoff.
- [ ] Boundaries with W12, W27, W28, and existing Core/MCP/runtime responsibilities are reviewed.
- [ ] A representative Work is walked through the model and gaps are logged.
- [ ] Ka review and Vinh approval are recorded before declaring the standard approved.
- [ ] Runtime integration is not claimed until implemented and tested.

## 8. Work log — initial entry

- **Date/time:** 2026-10-18 (UTC+7; exact time not recorded in this commit).
- **Actor:** Xu — Planner / coordinator.
- **Action:** Created W31 charter on a dedicated Work branch after Vinh assigned Work ID 31 and defined its purpose as workflow-model design.
- **Result:** Charter documented. Runtime behavior, local Sandbox mirror, E2E execution, and approval are **NOT YET VERIFIED**.
- **Next:** inspect existing Work templates and contracts; draft lifecycle/state transitions and role matrix; identify overlaps and dependencies; submit for Ka review and Vinh decision.

## 9. Change control

W31 must not directly modify `main` or silently impose workflow changes on other Works. Publish proposed changes on the W31 branch, review the diff and evidence, and obtain Vinh's approval before integration/adoption.
