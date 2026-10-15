# Work 28 — Required Capability: AI Runs Python Through MCP

Date: 2026-10-11
Decision owner: Vinh
Execution lead: Xu
Status: REQUIRED / NOT IMPLEMENTED / NOT TESTED

## Requirement
ROOM-HOP AI members must be able to request Python execution through MCP :8020 using a governed, auditable tool flow. The AI should be able to write code in its authorized Work Sandbox, request execution, receive the real exit code and stdout/stderr, inspect failures, revise code, rerun tests, and read back evidence without requiring the user to manually operate a terminal for every iteration.

## Required flow
AI member -> MCP :8020 tool -> Core :8000 authorization and WorkContext -> canonical approved execution runtime (W12/W13 or Work 27 when genuinely integrated) -> result/logs/evidence -> AI member.

## Required tool family (proposed names; not live until registered)
- python_run: execute an approved Python entry point or test target in an authorized Work context.
- python_status: query the authoritative run status by run_id.
- python_output_read: retrieve bounded stdout/stderr and exit code.
- python_test: run an approved test target and return the real test summary.
- execution_cancel: cancel a run if the canonical runtime supports safe cancellation.
- evidence_collect: bind request_id, task_id, run_id, exit code, output references and source revision/hash.

## Safety and architecture constraints
1. MCP must not expose unrestricted shell or arbitrary host filesystem access.
2. Core :8000 owns authorization; every request is identity- and WorkContext-bound.
3. Python executes in an isolated, bounded runtime with timeout, resource limits, output limits and explicit allowed working directory.
4. Start with safe approved Python/test commands; package installation, network access, secrets and host access are denied by default unless separately authorized.
5. Reject path traversal and execution outside the authorized Work root.
6. Return truthful statuses: PASS, FAIL, BLOCKED, DENIED, TIMEOUT, NOT_FOUND or INVALID_REQUEST.
7. Never report PASS unless execution really ran and its exit code and evidence were captured.
8. Use canonical W12/W13 or integrated Work 27 runtime; do not create a parallel execution host and do not bypass Core.
9. The AI workflow must support the loop: write -> run -> inspect output -> fix -> rerun -> verify -> record evidence.

## Acceptance criteria
- A Python smoke test runs through the actual MCP :8020 entry point and returns a real run_id, exit code and output.
- A failing test returns FAIL with diagnostic output; it is not mislabeled PASS.
- A timeout returns TIMEOUT and does not leave an untracked process.
- Unauthorized Work context and path traversal are denied.
- The AI can revise a Sandbox file and rerun it through MCP, with readback and correlated evidence.
- An end-to-end trace proves MCP -> Core -> approved runtime -> result/evidence.

## Current evidence
This file records Vinh's required product capability. It does not prove implementation or runtime availability. Work 28 remains ACTIVE / NOT LOCKED until acceptance criteria pass with real evidence.
