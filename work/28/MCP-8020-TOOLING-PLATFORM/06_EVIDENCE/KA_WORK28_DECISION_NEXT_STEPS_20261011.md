# KA — WORK 28 TECHNICAL DECISION & NEXT EXECUTION ORDER
Date: 2026-10-11 (+07)
Authority: Vinh
Decision lead / independent CSA: Ka
Work: 28 — MCP-8020-TOOLING-PLATFORM
Status: ACTIVE / NOT LOCKED
Decision basis: live ROOM-HOP tool surface + readback of Work 28 requirement, architecture, contract code/tests, Go E2E report, Cla security report, checkpoint and work log.

## 1. Decision
**NO-GO for registering or enabling python_run today.** The current connected ROOM-HOP tool surface has no python_run/python_test/execution_submit family. The approved runtime path and MCP -> Core -> runtime trace have not been demonstrated. Work 28 remains ACTIVE / NOT LOCKED.

**GO for bounded contract hardening and integration discovery only**, in a separate implementation slice with regression tests. Do not claim runtime acceptance from Sandbox writes or a local/container-only test.

## 2. Findings accepted from independent reviews
- Go: Sandbox file operations + readback are observed working for Work 28; execution tool, canonical runtime route, run_id/exit_code/stdout/stderr, and end-to-end evidence remain BLOCKED.
- Cla: 7 existing unit tests passed only in Cla's separate container with PYTHONPATH; this is PASS-LOCAL, not G3. The default documented layout fails import (exit 1). Path validator accepted risky Unicode/Windows names. ToolResult can represent PASS without run_id, exit_code or evidence. Authorization principal source and evidence immutability are not proven.
- Ka's own live inspection: current connector exposes 18 operations, no execution tool. Work 28 Sandbox tree and review artifacts read back successfully. This session has no tool to execute Python or query the PC's canonical runtime directly.

## 3. Binding architecture decisions
1. Core :8000 remains the only authorization / WorkContext authority. MCP :8020 is an adapter, not an authorization substitute.
2. Do not create a second execution host. Before implementation, inspect the real MCP source, Core route and W12/W13/Work 27 integration seam. If source/route/runtime is inaccessible, record BLOCKED and stop at the interface boundary.
3. Do not expose general shell or caller-controlled command strings, interpreter, cwd, environment, stdin, or arbitrary argv.
4. Arbitrary Python is not made safe by an approved-command label. Execution requires OS-level isolation: no host secrets, no network/host loopback, least privilege, bounded CPU/RAM/PIDs/disk/output/time, and process-tree cleanup. If those controls cannot be proven, do not enable Python execution.
5. Run immutable source snapshots bound to source hash. The runner must derive status from trusted runner/test-report evidence and actual exit code; printed JSON or exit 0 alone is not enough if zero tests ran.
6. Generate request_id/run_id server-side; enforce identity/Work ownership on status/output/cancel. Evidence must be written by Core/runtime to a protected append-only or integrity-checked area, not be mutable by arbitrary agents.
7. Path validation is only one layer: reject Unicode confusables/bidi/invisible/control characters, Windows reserved names/trailing dot-space, option-like components, and ambiguous normalization; enforce canonical realpath containment and reject symlinks/reparse points at filesystem access. No path validation alone is a sandbox.

## 4. Ordered work packages
### WP0 — source and boundary discovery (BLOCKER / first)
- Xu/implementation owner: provide read-only source evidence for MCP :8020 registration/handler, Core :8000 authorization + WorkContext route, and canonical W12/W13/Work 27 runtime API, with exact file paths and current revision.
- Trace the existing authenticated principal source and sandbox authorization. Do not trust identity_id supplied in request body.
- Output: source map + interface contract + explicit unavailable dependencies. No endpoint invention.

### WP1 — contract hardening (GO, sandbox-only until reviewed)
- Fix ToolResult so PASS is impossible without required authoritative evidence fields for the relevant operation (at minimum run_id, exit_code=0, evidence_ref and a trusted runner/test summary; non-execution operations should use a different result contract or explicit operation type).
- Add non-terminal states QUEUED/RUNNING and terminal CANCELLED if status polling is part of the contract; never normalize them to FAIL.
- Generate request_id/run_id at trusted server boundary; define replay/idempotency behavior.
- Tighten path validation and add Cla cases B3-B6 plus regression tests. Keep real filesystem containment checks in the eventual adapter/runtime, not only this pure function.
- Fix package/test layout so a documented clean command works without ad hoc PYTHONPATH hacks; ensure test discovery fails if zero tests execute.
- Do not mark these changes PASS until an approved runner produces exact command, exit code and output.

### WP2 — security acceptance design (Cla owns review, not self-approval)
- Convert Cla's negative-test matrix into test IDs with expected result and evidence fields.
- Mark current runtime cases NOT RUN / BLOCKED. Do not probe another Work or production host without explicit authorization and an isolated test Work.
- Review isolation model and threat controls before any python_run implementation.

### WP3 — E2E acceptance (Go owns independent verification)
Only after WP0/WP1/WP2 evidence is ready:
- smoke success; intentional failure; timeout + process-tree cleanup; unauthorized WorkContext; path traversal/symlink escape; mutation -> run FAIL -> patch -> rerun PASS; output/evidence readback.
- Each case must capture request_id, run_id (where execution started), source hash, exact approved target, stdout/stderr or protected refs, exit code, status, timestamps, runtime identity and evidence_ref.
- Go independently verifies the trace through the actual MCP entry point and records failures honestly.

## 5. Acceptance gates
- G1 inventory: PARTIAL (connector surface known; PC live registry/source not independently inspected).
- G2 contract/policy: NOT PASS; critical contract/security gaps remain.
- G3 approved-runner unit/contract tests: BLOCKED.
- G4 negative authorization/path/isolation tests: BLOCKED.
- G5 live MCP -> Core -> canonical runtime -> evidence/readback E2E: BLOCKED.
- G6 compatibility with W12/W13/W14/W24: BLOCKED pending source/runtime seam review.

## 6. Immediate owner actions
- Ka: set the decision above and maintain evidence/status discipline.
- Go: preserve independent E2E checklist; do not certify until actual MCP entrypoint and canonical runtime are exercised.
- Cla: preserve security veto on Python execution until OS isolation, principal binding, evidence integrity and path containment are demonstrated.
- Xu / implementation owner: perform WP0 source discovery and then implement WP1 against actual source seam; no Core change merely to make a demo pass.
- Vinh: final authority remains unchanged; this record is a technical go/no-go recommendation within the assigned review role.

## 7. Current status (truthful)
- Work 28: ACTIVE / NOT LOCKED.
- python_run family: NOT REGISTERED / NOT TESTED.
- Canonical execution path: BLOCKED / NOT PROVEN.
- Go review: DONE (independent report present; E2E blocked).
- Cla review: DONE (independent security report present; runtime acceptance blocked).
- No runtime PASS claimed. No MCP/Core source modified by this decision.


## 2026-10-12 — Ka-led continuation (supersedes the earlier wait-for-Xu sequencing)
- Vinh assigned Ka to drive Work 28 end-to-end while Xu is occupied elsewhere. Ka is the active technical coordinator; Vinh remains final authority.
- WP0 source map recorded at `06_EVIDENCE/KA_WP0_SOURCE_BOUNDARY_MAP_20261012.md`.
- GitHub snapshot reviewed at commit candidate `d7c90d9d31062d389810808e43dfdd19d7711b75`; this does not prove deployed PC revision or live route alignment.
- Source findings: current inspected MCP public adapter only registers meeting/read/recording tools; no execution tool. Core MeetingService source inspected has no execution dispatch. WEE/W13 source classes exist, but live reachability is unproven. Alternate `execution_host/server.py` accepts caller-serialized `authorized` and shows no auth in handler; do not connect it to MCP. W13 RealExecutionHost source lacks visible OS-level isolation and timeout/kill-tree controls. NO-GO execution registration.
- Ka wrote contract 1.1.0 + expanded regression tests to Work Sandbox. The source/test files were read back successfully. These changes have NOT been executed by an approved runner and are NOT G3 PASS.
- Next sequence: (1) Cla reviews the hardening diff and threat-model requirements; (2) retrieve deployed PC MCP/Core SHAs and live routes via authorized read-only diagnostics; (3) prove authenticated principal + Core WorkContext resolution; (4) prove OS-level isolation and protected evidence; (5) only then plan adapter integration; (6) Go runs E2E independently.
- Work remains ACTIVE / NOT LOCKED.
