# Work 28 — Execution Integration Remediation Plan
Date: 2026-10-25
Owner: Xu (AI-01 GPT CEO / Quân sư LAB)
Status: IN PROGRESS — implementation not yet verified
Scope: close the existing execution-tool gap only; no architecture expansion.

## Source-of-truth constraints
- Work 28 execution tools remain fail-closed until all hard gates in PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md are evidenced.
- Core :8000 remains the sole authorization authority.
- Reuse canonical W12/W13 Execution Host :8031 through an existing authenticated Core route. No direct MCP-to-8031 bypass and no second host.
- Do not mark a tool IMPLEMENTED merely because a handler/schema exists.
- Current branch tests use MockCoreExecutionClient and are unit-contract tests, not live-runtime evidence.

## Implementation sequence
### R1 — Canonical API
- Adopt the contract's four operations: python_run, python_status, python_output_read, python_cancel; map legacy sandbox_* names explicitly or keep them hidden/compatibility-only until migration is accepted.
- python_run accepts only work_id, entry_path, operation RUN_SCRIPT|RUN_TESTS, expected_source_sha256, timeout_seconds.
- Remove inline script, arbitrary command text, free-form argv, caller cwd/interpreter/env/identity from the public execution contract.
- Core must derive principal and WorkContext from authenticated transport, never from caller fields.
- Snapshot the authorized Work file immutably; hash it before dispatch; block if hash mismatches.
- Define bounded output/evidence response and nonzero/zero-test rules once, shared by Core and MCP.

### R2 — Lifecycle and evidence
- Add status, output-read and cancel routes to the same Core client contract.
- Reauthorize every status/output/cancel call against server-derived principal + Work.
- Cancellation is CANCELLED only when process-tree cleanup is verified.
- Evidence must be integrity-protected and not writable/deletable by normal Sandbox file tools.
- Fail closed for stale/unknown runtime identity, runtime down, missing evidence, malformed test summary, timeout cleanup uncertainty.

### R3 — Tests before activation
- Contract parity tests: catalog schema, gateway request and canonical contract.
- Negative tests: missing principal, spoofed identity, cross-Work run, path traversal/ADS/UNC/symlink, invalid hash, source mutation, forbidden network/host access, huge output, concurrency limits, timeout and child-process cleanup, zero tests, nonzero exit, evidence overwrite.
- Keep all execution tools NOT_IMPLEMENTED until R4 acceptance gates pass.

### R4 — Authorized runtime integration
- Identify exact deployed MCP/Core revisions and existing authenticated Core route.
- Verify current canonical W13 runtime identity/build hash/health/execute evidence and OS isolation.
- Wire the concrete Core client only through that route.
- Run real Python smoke, intentional nonzero exit, pytest with nonzero tests, zero-test rejection, timeout/cancel, output readback and evidence integrity.
- Record request/run IDs, source hash, runtime identity, bounded stdout/stderr, exit codes, test summaries and evidence refs.
- Cla reviews threat model and negative tests; Go independently runs E2E.
- Only then change tool status to IMPLEMENTED and release.

## Current gate state
- Static source review: PASS — concrete contract/schema/lifecycle mismatches identified.
- Contract parity: BLOCKED — implementation and tests not updated.
- Core route/current runtime identity/OS isolation: BLOCKED — not evidenced in this session.
- Real Python/pytest E2E: NOT RUN.
- Release: NO-GO; Work 28 remains ACTIVE / NOT RELEASED.

## PC/VS Code trigger
No PC action is requested for offline source/contract work. Request one bounded PC validation session only if authorized tools cannot provide current Windows :8031 runtime attestation and real E2E. Required action then: run the prepared Work 28 validation entrypoint on the already-approved host, capture exact commit/build identity, health and execute output; do not restart/create a host unless the evidence specifically proves it is required.
