# KA — WORK 28 COORDINATION DECISION
Date: 2026-10-14 (+07)
Authority: Vinh. Technical coordination: Ka / CSA.
Status: ACTIVE / NOT LOCKED. Execution registration: NO-GO.

## Decision
Ka takes active end-to-end technical coordination; Xu is not a dependency for sequencing. Target is authenticated MCP -> Core-authorized WorkContext -> immutable snapshot/hash -> isolated canonical runtime -> trusted result -> protected evidence -> independent readback. Automatic repair/retest must preserve history and cannot self-approve.

## Current live evidence
- MCP Sandbox discovery confirms Work 28 exists and manifest_exists=true.
- Work 28 file listing confirms contract, tests, Blueprint, Cla report and Go report artifacts exist.
- Readback of 04_CODE/tool_contracts.py confirms CONTRACT_VERSION=1.1.0.
- get_pending_tasks(identity_id="cla") returned tasks=[]. No claim that Cla received a new task.
- No approved runner output, deployed PC SHA/route evidence, OS isolation proof or live MCP-to-runtime E2E was obtained in this action.

## Gate state
G1 inventory: PARTIAL; deployed PC revision and live route not verified.
G2 contract/policy: NOT PASS; strengthen test-summary strictness and operation-specific result validation.
G3 approved runner: BLOCKED; not executed here.
G4 authorization/path/OS isolation: BLOCKED.
G5 live MCP -> Core -> runtime -> protected evidence/readback: BLOCKED.
G6 full automatic E2E and compatibility: BLOCKED.

## Immediate orders
1. Collect read-only PC evidence for MCP 8020 and Core 8000 process, deployed branch/SHA, registered tools, principal derivation, WorkContext route, canonical W12/W13/Work 27 runtime and evidence location.
2. Harden contracts and regression tests in a reviewable slice. In RUN_TESTS, missing failures/errors/skipped counters must not default to zero; reject bool counters; reject zero tests and all-skipped; compare executed count to approved inventory.
3. Cla independently reviews threat model and negative cases; preserve NO-GO for unresolved critical/high findings.
4. Only after WP0-WP4 evidence, integrate at existing canonical seam. No second execution host and no caller-controlled command strings.
5. Go independently executes the actual MCP E2E matrix and verifies evidence readback after security approval.

## Security and evidence constraints
Core :8000 remains the sole authorization/WorkContext authority. MCP :8020 is an adapter. Never trust caller-supplied authorized or identity as permission. No arbitrary host shell/Python. Require OS isolation, no host secrets/network/loopback, bounded resources, timeout/process-tree cleanup, immutable source snapshot, server-generated IDs and tamper-resistant evidence. Sandbox documentation is not equivalent to Core task dispatch.

## Honest status
python_run remains NOT REGISTERED / NOT ENABLED. No G3 PASS or live E2E PASS is claimed. Work 28 remains ACTIVE / NOT LOCKED.
