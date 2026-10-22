# Work 51 — HQTT AI Coder–Tester Architecture

- **Work ID:** W51
- **Project:** HQTT AI Coder–Tester
- **Status:** PLAN COMMITTED / QWEN CODER IMPLEMENTATION ASSIGNED — implementation not yet verified
- **Implementation owner:** Qc — Qwen Coder; execute the canonical plan at `work/51/HQTT-AI-CODER-TESTER/01_PLAN/PLAN_WORK51_v1.0.md` end-to-end
- **Governance:** AI contributions are assigned by role/title; Vinh retains approval authority
- **Coordinator / record keeper:** Xu (AI-01) — sets scope and records handoffs/evidence; Qc owns implementation. Cla's earlier planning-lead assignment is superseded for execution.
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Work branch:** `work/51-hqtt-coder-tester`
- **Created:** 2026-10-22

## 1. Purpose

Design and then implement a controlled Coder–Tester workflow for HQTT AI. ROOM-HOP is the orchestration and evidence source of truth. Coder and Tester use the same AI provider initially but remain separate roles with separate instructions, sessions, permissions, and deliverables.

This Work is created as a planning and implementation container. Creating this record does **not** mean that Cla has completed the plan or that any integration exists.

## 2. Non-negotiable architecture constraints

1. ROOM-HOP coordinates the workflow and records task state, decisions, artifacts, and evidence.
2. Core :8000 remains the source of truth; do not create a second Core.
3. Keep the established flow AI → MCP :8020 → Core :8000 → Runtime/Workspace.
4. Sandbox remains a separate execution environment; do not deploy Core :8000 into Sandbox.
5. No direct AI-to-Drive/backend path that bypasses the approved architecture.
6. No PASS without verifiable evidence. Use DONE / PASS / DECISION / BLOCKED accurately.
7. No production code changes until the planning deliverables and required approvals are accepted.

## 3. Role-based contribution model

- **Qc (Qwen Coder): Implementation Owner.** Execute READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF autonomously using the canonical plan. Do not wait for routine approvals or ask Vinh to monitor the PC. Record real blockers with evidence.
- **Ka (AI-02): Architecture Reviewer.** Independently review boundaries, contracts, failure modes, security, versioning, and scope.
- **Vi: Coder role.** Implement only approved work packages; provide diffs, test commands/results, commit/artifact references, and known limitations.
- **An: Tester role.** Independently verify the original acceptance criteria against actual changes; report PASS/FAIL/BLOCKED with evidence.
- **Qw (AI-05): QE/QA only.** Independently review test coverage, evidence completeness, traceability, and release-gate compliance; not project lead.
- **Xu (AI-01): HQTT coordination and records.** Define scope, keep records, coordinate handoff and evidence; does not replace Qc as implementation owner.
- **Vinh: Product/architecture authority.** Approve scope, architecture decisions, risk exceptions, and gates designated for human approval.

Role names above describe intended responsibilities for this Work. Do not assume a particular API/model adapter, Skill, identity mapping, or automatic inter-agent calling mechanism already exists.

## 4. Canonical plan and implementation directive\n\nThe sole canonical plan is `work/51/HQTT-AI-CODER-TESTER/01_PLAN/PLAN_WORK51_v1.0.md`. Qc must follow it and update the plan in place (same filename) if a material plan change is necessary, recording a version and change log. Do not create parallel plan files.\n\nQc owns implementation and verification end-to-end. GitHub branch `work/51-hqtt-coder-tester` is the primary work channel because Qc cannot access ROOM-HOP directly. Do not claim ROOM assignment or MCP handoff without direct evidence.\n\n## 5. Initial planning deliverables (superseded by the canonical plan)

1. **Current-state audit:** identify existing ROOM-HOP components and reusable interfaces; distinguish verified facts from assumptions and gaps.
2. **Target architecture:** Orchestrator, provider/model adapter, role configuration, Work Contract, Runtime execution boundary, Evidence/Handoff.
3. **Work Contract:** task identity, objective, scope, acceptance criteria, risk, repository/branch/base commit, role/model/config versions, outputs, evidence references, and status.
4. **State machine and workflow:** READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF; PASS, FAIL, BLOCKED, timeout, cancellation, retry limits, and escalation.
5. **Role boundaries and permissions:** separate Coder and Tester instructions/sessions/permissions; independent Tester input includes the original contract and actual code/artifacts, not only Coder's summary.
6. **Versioning and reproducibility:** provider/model ID, role prompt/Skill version, contract/schema version, tool policy, runtime/dependencies, commit SHA, artifact hashes, and workflow version.
7. **Security plan:** secrets handling, least privilege, untrusted repository content, network/tool allowlists, audit logs, resource/cost limits, and emergency stop.
8. **Acceptance plan:** E2E scenarios for PASS, FAIL and BLOCKED; contract validation; permission tests; evidence-to-commit binding; bounded retries and handoff.
9. **Phased implementation plan:** dependencies, deliverables, owners by role, acceptance criteria, rollback/stop conditions, and estimated effort/cost where evidence supports it.
10. **Decision register:** options, recommendation, impact, and explicit Vinh approval required for each unresolved architecture/security decision.

## 6. Proposed workflow

1. Xu/Vinh records the goal and approved scope.
2. Cla produces the plan and marks assumptions and decisions explicitly.
3. Ka reviews architecture and risk; Qw reviews test/evidence strategy.
4. Vinh approves the plan and any required risk decisions.
5. Vi implements one approved work package in the authorized branch/workspace.
6. An tests independently against the original contract.
7. Qw checks evidence completeness and release-gate compliance where assigned.
8. ROOM-HOP records status and evidence; Xu prepares the handoff.
9. Failed checks return to Vi within an approved retry limit; unresolved or risky cases become BLOCKED and are escalated.

## 7. Initial proposed acceptance gates

- **G1 Contract:** valid and invalid Work Contracts are tested; malformed or incomplete tasks are rejected.
- **G2 Separation:** Coder and Tester role configurations and permissions are distinct; Tester can inspect the actual artifact independently.
- **G3 Orchestration:** task-to-Coder-to-Tester-to-handoff flow has an end-to-end trace.
- **G4 PASS path:** test results and evidence refer to the exact tested commit/artifacts.
- **G5 FAIL path:** a seeded/reproducible failure is detected and routed back to Coder.
- **G6 BLOCKED path:** missing permission, environment, evidence, or timeout stops safely without false PASS.
- **G7 Security:** secrets are not exposed; unauthorized tools/actions are denied and logged.
- **G8 Versioning:** model/provider, role configuration, contract, runtime, policy, and commit are recorded.
- **G9 Limits and recovery:** retry, time, cost/resource, cancellation, and escalation behavior are tested.
- **G10 Handoff:** another authorized person/AI can verify the result from stored evidence without trusting an unsupported assertion.

These gates are proposed and must be refined by Cla, reviewed by Ka/Qw, and approved by Vinh before implementation.

## 8. Scope exclusions until approved

- Do not expand Work 28 or alter its deliverables under W51.
- Do not change Core/MCP/Runtime architecture without a documented impact analysis and approval.
- Do not implement production code in this initial planning step.
- Do not assume ChatGPT Skills can call one another or orchestrate separate chat sessions; automation requires an explicit, supported model/API/runtime adapter.
- Do not automatically push, merge protected branches, deploy, or modify secrets.

## 9. Initial status and evidence

- Work branch creation: recorded in GitHub.
- Planning document: this file.
- Canonical plan: **COMMITTED** at `work/51/HQTT-AI-CODER-TESTER/01_PLAN/PLAN_WORK51_v1.0.md` (commit `a2e371ad71c6f6e55804e26d84d02473f14652f9`).
- Architecture review: **NOT RUN**.
- Code implementation: **NOT YET VERIFIED**; Qc is assigned to implement on this branch.
- E2E validation: **NOT RUN**.

## 10. Required next handoff

Qc should execute the canonical plan and return:
- current-state findings and evidence,
- target component diagram and interface boundaries,
- prioritized work packages and dependencies,
- role-specific deliverables,
- risk/decision register for Vinh,
- acceptance tests and evidence requirements,
- a clear DONE / PASS / DECISION / BLOCKED summary.

Implementation may proceed within the authorized scope defined by the canonical plan. Stop only for a real permission, safety, infrastructure, or out-of-scope blocker; document evidence rather than asking Vinh to supervise routine steps.
