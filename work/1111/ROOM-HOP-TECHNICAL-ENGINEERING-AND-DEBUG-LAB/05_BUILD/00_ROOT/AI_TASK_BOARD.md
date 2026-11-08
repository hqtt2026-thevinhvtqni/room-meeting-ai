# AI TASK BOARD — WORK 1111

This board is the shared intake point for technical agents. A task is not assigned merely because it is listed. The named AI must acknowledge through a traceable artifact before its status changes to IN_PROGRESS.

| Task ID | Workstream | Initial scope | Suggested role | Status |
|---|---|---|---|---|
| W1111-T01 | GitHub–Sandbox–PC source-of-truth map | Exact path/SHA/hash mapping, drift handling, readback protocol | Xu / Architect | IN_PROGRESS (claimed in DOC-003) |
| W1111-T02 | Execution Host :8031 runtime attestation | Identify deployed source/build, startup, auth, Work authorization and safe execution contract | Claude / Runtime reviewer | READY |
| W1111-T03 | Execution result correctness | Reproduce and regression-test nested test failure propagation / false aggregate PASS | Vi / Coder + Qw / QE | READY |
| W1111-T04 | ROOM-HOP component architecture | Core, Workspace, Gateway, Event Listener, Agent Runtime, MCP and adapters dependency map | Ka / CSA | READY |
| W1111-T05 | W32 Windows Browser E2E blocker | Trace runner readiness, service provenance and exact-SHA release gate | An / QE with Xu coordination | READY |
| W1111-T06 | AI identity and authorization | Principal/agent identity, policy, token provenance and task-to-runtime mapping | Xu / Ka | READY |

## Agent participation protocol
1. Read DOC-001, DOC-004, DOC-005, DOC-006, DOC-007 and the latest DOC-003 journal entries before starting.
2. Claim a task by adding an entry to the Work journal with exact AI identity, task ID, starting branch/SHA, scope and intended output. Do not impersonate another agent or infer ACK.
3. Keep source changes on a scoped branch. Open a PR for review; do not push source code to main.
4. Record every check with method/command, time, exact revision, raw evidence location and PASS/FAIL/BLOCKED/NOT RUN.
5. Update the task row only after a real ACK or evidence-backed state transition.
6. Xu coordinates integration and ensures journal readback. Independent QE must not approve its own implementation.
7. If blocked, state problem / attempts and evidence / bottleneck / options / exact missing condition.

## Initial state
W1111-T01 is IN_PROGRESS with Xu's claim recorded in DOC-003. T02–T06 remain READY; no ACK or implementation start is asserted for those agents.
