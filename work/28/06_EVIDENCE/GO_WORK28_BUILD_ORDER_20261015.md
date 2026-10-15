# GO — WORK 28 BUILD EXECUTION ORDER
**Order ID:** GO_WORK28_BUILD_ORDER_20261015  
**Issued by:** Ka — CSA / Work 28 Coordinator  
**Date:** 2026-10-15  
**Role:** GO is the primary builder/implementer for Work 28. This is a BUILD assignment, not an independent-review-only assignment.

## MISSION
Continue building Work 28 end-to-end and produce a working, testable implementation. Do not stop after listing blockers or writing a review report. Work from the actual Work 28 source and current manifest; do not infer implementation from excerpts alone.

## REQUIRED STARTUP
1. Read `MCP-8020-TOOLING-PLATFORM/00_ROOT/WORK_MANIFEST.md`.
2. Read `MCP-8020-TOOLING-PLATFORM/01_ORIGINAL/WORK_28_REQUIREMENT.md`.
3. Read the current architecture/build orders:
   - `MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/WORK_28_ARCHITECTURE_PLAN.md`
   - `MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`
   - `MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/KA_WORK28_E2E_AUTOMATIC_BUILD_ORDER_20261014.md`
4. Read current code, tests, and latest evidence, including the 2026-10-15 blocked report and listener identity evidence.
5. Record the actual source/revision, working-tree status, runtime constraints, and exact implementation gaps before editing.

## BUILD WORK PACKAGES
### WP1 — Source/runtime identity evidence
Implement or complete a reproducible, read-only diagnostic path that records listener PID, executable/command line, working directory, loaded module/entrypoint and adapter paths where technically observable, effective non-secret configuration, and SHA-256 hashes of relevant source files. Explicitly label any property that cannot be reliably observed; do not guess.

### WP2 — MCP protocol and tool discovery
Build a reproducible test/diagnostic client for MCP initialize and tools/list against the intended local listener. Capture raw request/response, endpoint, timestamps, protocol version and exit status. Do not claim a response came from PID 6748 unless the process-to-endpoint correlation is actually evidenced.

### WP3 — Contracts and adapters
Review and implement the approved tool contracts and adapter boundaries using the existing architecture and source as authority. Add positive and negative regression tests for invalid arguments, unauthorized identities, malformed inputs, adapter failures, timeout/error handling and forbidden execution paths as applicable. Do not add tools or expand permissions merely to make the demo pass.

### WP4 — Principal and WorkContext
Implement or complete the Core-derived principal and WorkContext propagation contract. Reject caller-supplied identity/context that bypasses trusted Core derivation. Add regression tests demonstrating both allowed and denied cases.

### WP5 — Isolation and execution safety
Implement/test process lifecycle, cleanup, timeouts, resource limits, path/workspace boundaries and failure recovery for any execution-related code. Keep arbitrary Python execution and tool registration disabled unless separately authorized by Vinh after required security acceptance.

### WP6 — Automatic E2E runner
Create or complete a deterministic E2E runner that executes the canonical tests and negative contract/adapter tests, emits machine-readable and human-readable results, preserves stdout/stderr, records exit codes and test counters, and returns non-zero on any required failure. Ensure cleanup runs on both success and failure.

### WP7 — Evidence and journal
Write implementation notes, exact commands, changed-file list, source hashes, test logs, exit codes, counters, known limitations and readback confirmation into Work 28 evidence/journal. Do not report a file as persisted until it has been read back successfully.

## EXECUTION RULES
- Implement in small, reviewable increments; preserve unrelated work and inspect diffs before changing files.
- No scope creep; do not rewrite Core or bypass architecture boundaries without explicit authorization.
- Do not use sandbox list/read success as live E2E evidence.
- Do not fabricate listener identity, runtime config, hashes, test output, exit codes or security results.
- Keep registry change, arbitrary python_run, write/sync/merge/release and production tool registration NO-GO until their required authorization gates are explicitly cleared.
- If a dependency requires PC/runtime access, build all locally testable parts first, then record the exact external dependency and continue with other work; do not idle waiting for PC.
- Cla owns security-specific implementation/review work in parallel. Coordinate interface and evidence requirements with Cla, but do not treat Cla's review as a substitute for your implementation tests.
- Go must not self-certify the final independent acceptance. Your job here is BUILD + self-tests + evidence. Independent acceptance remains a separate gate.

## REQUIRED DELIVERABLES
1. Actual implementation changes in the authoritative Work 28 source/workspace.
2. Regression tests covering success and denial/error cases.
3. One deterministic E2E runner with clear exit behavior.
4. Evidence report with changed files, commands, logs, exit codes, counters and unresolved blockers.
5. Updated work journal and successful readback.
6. A concise handoff to Ka and Cla stating what is implemented, what tests ran, what failed, and what can proceed next.

## FIRST RESPONSE REQUIRED FROM GO
Acknowledge this as a BUILD assignment, then return:
- authoritative source/workspace path and revision found;
- exact build plan with WP1-WP7 status;
- first implementation slice to execute now;
- dependencies that truly require PC/runtime access;
- no claim of PASS until the runner has actually run.

**Acceptance of this assignment means beginning implementation, not merely returning another BLOCKED review.**
