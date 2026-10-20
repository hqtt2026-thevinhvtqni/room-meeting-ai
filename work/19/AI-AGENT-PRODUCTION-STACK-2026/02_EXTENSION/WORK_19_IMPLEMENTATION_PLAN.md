# Work 19 — Implementation Plan

- Work ID: 19
- Name: CẤU TRÚC HỌC TẬP — AI AGENT PRODUCTION STACK 2026
- Owner / decision maker: Vinh
- Coordinator / plan owner: Xu (AI-01)
- Plan date: 2026-10-20 (UTC+07:00)
- Status: PLAN RECORDED; phases G0–G7 have not been accepted.
- Authority: Vinh > Xu > Agent

## 1. Vision
Build a practical learning and verification path for production-grade AI Agent systems, using ROOM-HOP as the target architecture. The result must distinguish documented intent, implemented behavior and independently verified evidence.

## 2. Operating principles
1. Human Time First: use clear gates and minimize unnecessary manual micro-steps.
2. Evidence first: no PASS without inspectable evidence.
3. Architecture before code; documentation first.
4. Core :8000 is the source of truth; Dashboard :3000 is render-only.
5. Least privilege, bounded execution and explicit failure semantics.
6. No unnecessary framework or scope expansion.
7. Record owner, AI identity/role, timestamp, decision, evidence and next action.
8. Sandbox and GitHub are separate workspaces; sync is not proof of runtime correctness.

## 3. Intended outcomes
- O1 — Stack map: document the six layers, responsibilities and interfaces.
- O2 — Actual topology: map ROOM-HOP services and relevant Works to the layers, marking unknowns honestly.
- O3 — Contracts: define request/response/error, identity, timeout and resource-limit behavior at each boundary.
- O4 — E2E evidence: establish one inspectable request trace through MCP → Core → runtime → artifact, as applicable to the selected path.
- O5 — Readiness checks: cover reliability, scalability, security, observability, cost and evaluation.
- O6 — Data/recovery: document storage, backup, restore, retention and evidence integrity requirements.
- O7 — Handoff: provide verified results, unresolved gaps, evidence references and a clear next decision.

## 4. Phased plan and gates

### G0 — READ: inventory and establish baseline
Actions:
- Inspect Work 19 files and repository/work conventions.
- Read relevant ROOM-HOP governance and current project state.
- Inventory available documents, code, tests and evidence without changing implementation.
- Separate facts, hypotheses, historical state and unknowns.
Outputs: source inventory, baseline snapshot, missing-evidence list.
Gate: inventory references accessible sources and does not claim live status without evidence.

### G1 — TRACE: follow a real request
Actions:
- Choose one bounded end-to-end use case with Vinh's approval if scope selection is needed.
- Trace caller → MCP :8020 → Core :8000 → selected runtime/service → artifact/evidence.
- Record IDs, timestamps, inputs/outputs, error paths and persistence behavior.
- Identify any alternate path or direct backend access that bypasses the intended control plane.
Outputs: sequence/flow diagram, trace table, evidence links and gap list.
Gate: every asserted hop is supported by logs, tool output, code path or reproducible test.

### G2 — ANALYZE & DECIDE: architecture and priorities
Actions:
- Compare observed behavior with the six stack layers and production properties.
- Rank gaps by risk, user impact, dependency and effort.
- Present options and trade-offs; record decisions before coding.
- Defer optional technologies unless a use case and acceptance threshold justify them.
Outputs: architecture map, risk register, decision record and prioritized backlog.
Gate: decisions have a rationale and owner; unresolved items are explicitly BLOCKED or undecided.

### G3 — BUILD: implement only approved gaps
Actions:
- Write/update contracts and acceptance tests before changing code.
- Implement the smallest approved change in the designated Work/branch.
- Preserve protected Core and frozen baseline rules.
- Keep Sandbox and GitHub changes traceable; no unapproved merge or push to protected branches.
Outputs: scoped change, tests, change record and reproducible commands.
Gate: scope matches the recorded decision; tests and changed-file review are available.

### G4 — VERIFY: test the whole path
Actions:
- Run unit/contract tests and relevant integration/E2E tests.
- Verify success and failure paths, authentication/authorization and limits.
- Inspect the resulting artifact and read it back through the intended route.
- Record test command, exit code, environment, timestamp and evidence reference.
Outputs: verification report, raw results/logs and known limitations.
Gate: each criterion is PASS only with matching evidence; otherwise BLOCKED/FAIL/CHƯA XÁC MINH.

### G5 — OBSERVE & EVALUATE
Actions:
- Confirm structured logs, correlation IDs, health signals and useful error details.
- Define representative evaluation cases and thresholds.
- Measure latency, success rate, resource use and cost where data is available.
- Test retries, timeouts, duplicate operations and dependency outages.
Outputs: observability checklist, evaluation set and measurements.
Gate: measurement method and limits are explicit; no unsupported scalability or production claim.

### G6 — DATA & RECOVERY
Actions:
- Identify authoritative records, generated artifacts, metadata and retention needs.
- Define backup frequency, retention, integrity checks, restore objectives and access controls.
- Perform a restore exercise only in an approved, safe environment.
- Verify evidence and artifacts remain addressable after recovery.
Outputs: data map, backup/restore plan and restore evidence if executed.
Gate: distinguish a written plan from an executed and verified restore.

### G7 — HANDOFF
Actions:
- Summarize outcomes against O1–O7.
- Link commits, tests, logs, artifacts and decisions.
- List residual risks, blocked gates and the next owner decision.
- Update the canonical plan and shared work log.
Outputs: handoff record and next-step recommendation.
Gate: no phase is marked accepted solely because documents were written.

## 5. Acceptance checklist
- [ ] Stack and service map grounded in inspectable sources.
- [ ] Source of truth and each control boundary are clear.
- [ ] One selected request path traced end to end with evidence.
- [ ] Success and failure paths tested.
- [ ] Identity, authorization and least-privilege boundaries reviewed.
- [ ] Timeouts, retries, resource budgets and failure semantics documented/tested.
- [ ] Logs/traces/artifacts are correlated and readable.
- [ ] Cost/performance/evaluation thresholds defined or explicitly deferred with rationale.
- [ ] Backup/restore requirements documented; execution status stated honestly.
- [ ] Every result labeled DONE, PASS, BLOCKED, DECISION or CHƯA XÁC MINH accurately.
- [ ] Handoff names remaining risks and the next decision owner.

## 6. Roles
- Vinh — Owner / decision maker: approves scope, architecture decisions, risk acceptance and integration/merge.
- Xu (AI-01) — Coordinator / plan owner: maintains the plan, dependencies, status and handoff.
- Assigned implementer: works only within approved scope and records commands, diffs and results.
- Independent reviewer/tester: checks acceptance criteria and evidence; does not mark PASS from the implementer's claim alone.

## 7. Explicit non-goals
- Do not install every framework mentioned in the learning material.
- Do not introduce RAG/vector storage without a demonstrated retrieval requirement.
- Do not add Kubernetes, A2A or multi-provider orchestration solely for completeness.
- Do not claim Production-ready from a localhost demo or unit tests alone.
- Do not alter protected Core, frozen baselines or merge to main without authorization.

## 8. Current status
- Sandbox Work 19 exists and its listing shows the original learning file and this plan.
- GitHub branch is a working mirror, not an integration/merge.
- Exact byte-for-byte synchronization with Sandbox remains CHƯA XÁC MINH because source read-back did not return document content during this session.
- G0 is the next phase; G0–G7 are not yet accepted.

## 9. Change log
2026-10-20 UTC+07:00 — Xu (AI-01), coordinator — plan mirrored/reconstructed into the Work 19 GitHub branch; exact Sandbox comparison still pending.
