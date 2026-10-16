# Xu Master Plan — Work 28 E2E Auto
- Recorded: 2026-10-16 21:18 ICT (UTC+07:00)
- Owner: Xu — Plan / CSA
- Decision authority: Vinh — Work Owner
- Team flow: Xu Plan → Vi Coder → An Tester → Ka Review
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/28-mcp-tooling-platform
- Status: ACTIVE / NOT RELEASED. This is a plan, not evidence of implementation or runtime PASS.

## 1. Objective
Deliver a bounded autonomous end-to-end loop, not merely a tool registry or dashboard. An authorized task must be received, understood in its Work context, planned, executed through the existing approved architecture, verified, repaired within limits when safe, independently tested/reviewed, and handed off with inspectable evidence.

Canonical path: AI → MCP :8020 → Core :8000 → approved capability/runtime → output/evidence.
Do not create a duplicate MCP/Core/runtime, bypass Core, enable unrestricted command execution, merge to main, or modify protected Work 13, PC services, or live registry without explicit authorization.

## 2. End-to-end lifecycle
1. Receive an authorized task from a task assignment/Inbox or explicitly approved request.
2. Read this plan, the Work 28 journal, the relevant issue, current source/revision, previous decisions, known blockers and acceptance criteria.
3. Trace startup, provider construction, dependencies and execution path before editing.
4. Write a bounded task plan: allowed actions, approval points, test plan, retry cap, stop conditions and evidence location.
5. Validate AI identity, WorkContext, ownership, authorization and capability through Core before consequential actions.
6. Execute via the existing MCP :8020 → Core :8000 → approved runtime/capability path.
7. Validate actual output and observable state; preserve raw logs and revision IDs.
8. If a safe, reversible in-scope defect is reproduced, make the smallest fix and rerun targeted plus regression tests. Never retry indefinitely.
9. Stop and mark BLOCKED for missing approval/provider, unsafe ambiguity, failed isolation, exhausted retry budget or insufficient evidence.
10. An verifies; Ka reviews independently; Xu checks all gates and records acceptance or a specific fix request.
11. Handoff status, commit, tests, evidence links, residual risks and next owner.

## 3. Inbox, Proposal, Task and wake-up
Treat these as separate concepts:
- Message: communication; not automatically a task.
- Proposal: suggested action/decision; not authorization until accepted by the correct authority.
- Task/Inbox item: actionable record with task ID, target AI identity, Work ID, status, scope, acceptance criteria, owner, timestamps and evidence links.
- Wake-up/dispatch: mechanism that prompts an AI/runtime to inspect or claim eligible work. A read-inbox tool does not prove wake-up works.
- Execution record: evidence of actual action/result; not implied by Proposal acceptance or a status change.

Required lifecycle to trace and verify:
message/proposal → authorized decision → task created/updated → assigned to AI identity → dispatch or AI pull → authorized execution → verification → result + evidence → closed/blocked.

First discover the existing canonical implementation. Do not create a duplicate Inbox, Proposal service, queue, Core or runtime. If a stage is not evidenced, record the precise gap as BLOCKED and propose the smallest compatible change. Test rejected/unapproved proposals, wrong identity, cross-Work access, duplicate dispatch, stale/closed tasks, missing provider/auth, time/resource caps, and attempts to mark PASS without evidence.

## 4. No-repeat protocol
Before asking Vinh or another AI to repeat information:
1. Read this plan and the current Work 28 journal.
2. Read the assigned issue and comments plus linked artifacts.
3. Inspect current branch/source/commit and existing test/evidence records.
4. Compare against recorded decisions and blockers.
5. Ask only if a genuinely missing decision changes the implementation; state what was checked and what remains unknown.
6. Record new decisions once in the journal and update the relevant issue/plan reference. Do not create competing versions.

Every handoff must state named owner and role, exact task, source paths/revision, constraints, acceptance criteria, evidence path, dependencies, stop conditions and next owner. Continue from the latest verified records rather than restarting discovery.

## 5. Security invariants
- Core :8000 remains the authorization and canonical-state authority.
- No Core bypass, duplicate runtime, unrestricted shell/Python, caller-controlled identity, privilege self-escalation or cross-Work access.
- Sandbox/GitHub access must use trusted providers and scope-limited paths/branches/permissions.
- Require human approval for policy-designated privileged, destructive, external, security-sensitive or release-affecting actions.
- Bound retries, time and resources. Fail closed when trusted identity/provider/isolation cannot be proven.
- No merge to main or release until gates G1–G9 pass and Xu records acceptance.

## 6. Team lanes
### Xu — Plan / Planner
Maintain the source of truth, architecture trace, handoffs, gate checklist, readback and final acceptance. Do not claim implementation PASS from documentation alone.

### Vi — Coder / Implementer
First identify the actual existing MCP :8020 startup entrypoint and trusted provider bindings. Integrate the existing adapters only where source evidence supports the wiring. Preserve existing tools, add focused tests and commit only to the Work 28 branch. If startup/provider wiring is missing, record the exact blocker; do not guess.

### An — Tester / Verification
Test a specific commit. Run authorized unit/regression/integration tests; capture live tools/list; demonstrate one real authorized E2E run. Record timestamp, command/request, exit code, stdout/stderr, test counts, log path/hash, readback and result. If no approved runner/probe is available, mark BLOCKED.

### Ka — Independent Reviewer
Review the diff, negative tests, authorization boundaries, Inbox/Proposal transitions and raw E2E evidence independently. Record PASS/FAIL/BLOCKED per gate and residual risk.

### Xu — Acceptance / Handoff
Read back evidence and issue a final gate-by-gate decision. Return precise evidence-linked fixes when necessary. Do not merge/release while any required gate is not PASS.

## 7. Acceptance gates
- G1 Source/startup: actual MCP :8020 startup and provider construction traced.
- G2 Registry: approved tool set appears in live tools/list and existing tools are preserved.
- G3 Core security: identity, WorkContext, authorization, ownership, resource limits and fail-closed behavior proven.
- G4 Sandbox: Work isolation, path/payload bounds, write policy and readback/hash proven.
- G5 GitHub: authenticated provider, branch policy, write/commit and readback proven.
- G6 Tests: results tied to exact commit with exit code, inventory and logs.
- G7 E2E: real authorized request traverses MCP → Core → runtime/capability → verified output/evidence.
- G8 Ka: independent security and acceptance review.
- G9 Xu: final acceptance and handoff recorded.

## 8. Required evidence bundle
For each run record run ID, ICT timestamp, initiating AI identity, task/Work IDs, authorization decision, source commit, provider/config identity (no secrets), request/tool calls/correlation IDs, test command, exit code, stdout/stderr, test counts, runtime outcome, before/after state, readback and hashes, retry/fix chain, An verdict, Ka review, Xu decision, residual risks and links from the journal/issues. Redact secrets and personal data.

## 9. Definition of done
Work 28 is release-eligible only when G1–G9 pass with inspectable evidence tied to the accepted revision; live MCP preserves existing tools and exposes the approved tools; one real E2E run proves the authorized path; security and negative tests pass; Ka review is independent; and Xu acceptance is recorded. Otherwise keep ACTIVE / NOT RELEASED and give each incomplete gate a concrete owner and next action.

## 10. Status at plan creation
This document records the intended plan only. It does not prove startup wiring, live registration, Inbox wake-up, test execution or E2E. The last source audit did not prove actual startup wiring or live tool registration. Vi must resolve that first from repository evidence; An must verify runtime behavior; Ka must review independently.
