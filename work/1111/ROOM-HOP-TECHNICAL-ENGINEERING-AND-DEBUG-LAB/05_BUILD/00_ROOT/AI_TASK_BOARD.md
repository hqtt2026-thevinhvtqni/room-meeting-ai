# AI TASK BOARD — WORK 1111

This board is the shared intake point for technical agents. A task is not assigned merely because it is listed. The named AI must acknowledge through a traceable artifact before its status changes to IN_PROGRESS.

| Task ID | Workstream | Initial scope | Suggested role | Status |
|---|---|---|---|---|
| W1111-T01 | GitHub–Sandbox–PC source-of-truth map | Exact path/SHA/hash mapping, drift handling, readback protocol | Xu / Architect | IN_PROGRESS (claimed in DOC-003) |
| W1111-T02 | Execution Host :8031 runtime attestation | Absorbed into W1111-T07-VI; no separate AI assignment | Vi (coder) | SUPERSEDED — MERGED INTO T07-VI |
| W1111-T03 | Execution result correctness | Absorbed into W1111-T07-VI; Vi owns implementation and tests | Vi (coder) | SUPERSEDED — MERGED INTO T07-VI |
| W1111-T04 | ROOM-HOP component architecture | Xu performs architecture integration directly; no separate AI assignment | Xu | COORDINATOR OWNED — NOT A CODER TASK |
| W1111-T05 | W32 Windows Browser E2E blocker | Deferred until Execution Host and authorization boundary are implemented; no separate AI assignment | Xu coordinates with Vi evidence | DEFERRED — NO ACTIVE ASSIGNMENT |
| W1111-T06 | AI identity and authorization | Absorbed into W1111-T07-CO; Co owns implementation, Xu owns architecture | Co (coder) | SUPERSEDED — MERGED INTO T07-CO |
| W1111-T07 | ROOM-HOP authorization boundary & protected mutation remediation | Parent workstream decomposed into three coder-owned packages; see CODER_TASK_BREAKDOWN_CO_VI_XUCO_20261110.md | Xu coordinates; Co, Xuco, Vi execute | ACTIVE PLAN — CHILD TASKS BELOW |


| W1111-T07-CO | Trusted Identity & Authorization Core | Trusted principal, scoped Work/Assignment/Task grant, policy decision API, expiry/revocation and durable fail-closed audit | Co (coder) | READY — ACK REQUIRED |
| W1111-T07-XUCO | Gateway & Sandbox Enforcement | Gateway :8040 / MCP :8030 / SandboxService choke point, action/path enforcement and bypass closure | Xuco (coder) | READY — ACK REQUIRED |
| W1111-T07-VI | Execution Host & Result Integrity | Host :8031 grant validation, isolated named execution, truthful nested result propagation and evidence | Vi (coder) | READY — ACK REQUIRED |

## Agent participation protocol
1. Read DOC-001, DOC-004, DOC-005, DOC-006, DOC-007 and the latest DOC-003 journal entries before starting.
2. Claim a task by adding an entry to the Work journal with exact AI identity, task ID, starting branch/SHA, scope and intended output. Do not impersonate another agent or infer ACK.
3. Keep source changes on a scoped branch. Open a PR for review; do not push source code to main.
4. Record every check with method/command, time, exact revision, raw evidence location and PASS/FAIL/BLOCKED/NOT RUN.
5. Update the task row only after a real ACK or evidence-backed state transition.
6. Xu coordinates integration and ensures journal readback. Independent QE must not approve its own implementation.
7. If blocked, state problem / attempts and evidence / bottleneck / options / exact missing condition.

## Initial state
W1111-T01 is IN_PROGRESS with Xu's claim recorded in DOC-003. W1111-T07 is the parent workstream, decomposed into T07-CO (Co), T07-XUCO (Xuco) and T07-VI (Vi). All three child tasks are READY — ACK REQUIRED; no coder ACK or implementation start is inferred. T02/T03/T06 are absorbed into the child tasks; T04 is Xu-owned coordination; T05 is deferred. No other AI is assigned to this active workstream.


## End-to-end execution standard — D70-022 (2026-11-10)
Every accepted child task is an outcome delegation, not a sequence of chat prompts. The named owner must READ the Work records and journal, TRACE exact source/revision/runtime/dependencies/permissions, PLAN the full route, EXECUTE all permitted steps, VERIFY acceptance and tests, RECORD evidence/status in the canonical journal/register, and HANDOFF once complete.

- Co, Xuco and Vi remain the only coder owners for W1111-T07; no additional AI is assigned by this rule.
- Initial ACK remains mandatory before IN_PROGRESS; after ACK the owner proceeds through dependent steps and in-scope repair/retry without asking Xu or Vinh what to do next at every step.
- Do not send repetitive progress pings. Journal material events; notify Xu at material milestone, completion, or genuine blocker requiring external authority/access/decision.
- DONE requires deliverable, all acceptance evidence, applicable test results and required review. Chat claims are not evidence.
- Continue safe unblocked work when one dependency is BLOCKED. Record exact missing condition and options.
- DOC-117 and all authorization/security gates remain in force. D70-022 does not grant protected execution, merge, deploy or release permission.
