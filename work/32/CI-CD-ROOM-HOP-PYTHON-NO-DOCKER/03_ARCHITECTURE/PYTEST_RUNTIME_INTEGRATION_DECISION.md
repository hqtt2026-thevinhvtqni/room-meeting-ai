# Work 32 — Pytest Runtime Integration Decision

**Date:** 2026-10-24  
**Status:** TRACE COMPLETE FOR AVAILABLE CONTRACTS; LIVE EXECUTION BLOCKED

## Findings from existing Work artifacts

1. Work 12 defines the Work Execution Environment (WEE) contract and an Execution Host interface with discover, execute, runtime_info, workspace_info, collect_artifact and cleanup operations.
2. Work 27 defines an execution request/result contract with task_id, run_id, workspace_id, immutable source_revision, argv, cwd, timeout, resource/network profiles, authenticated requester, exit code, logs, and evidence reference.
3. Work 27's RuntimeAdapter delegates to an injected Transport and does not launch processes itself. The documented canonical transport is Work 13's POST /execute. Work 27 explicitly says it will not create a competing execution host or arbitrary-shell API.
4. Work 27's cross-work decision record states real E2E is BLOCKED because an authorized executable host capability is not exposed through the current ROOM-HOP route. Current Sandbox MCP exposes file operations, not process launch.
5. Work 12's existing TestRunner prototype calls subprocess.run without a timeout or explicit cwd in the inspected version. Do not treat that prototype alone as sufficient isolation or production readiness.

## Decision

- Work 32 will not implement a second process execution service.
- Work 32 will build the test-result evidence classifier and acceptance tests as a pure, standard-library component.
- Actual Python/pytest execution must be routed through the existing authorized Work 12/13 execution contract after the live host and isolation controls are attested.
- Until that prerequisite is met, end-to-end execution status is BLOCKED; classifier source and tests are not claimed to have run.
- GitHub Actions may be designed as a remote fallback, but workflow activation remains a separate authorized gate.

## Required runtime behavior

- Execute argv only; never accept arbitrary shell text.
- Enforce workspace confinement, non-root identity, bounded timeout/output, resource profile, default-deny network and secret-free environment in the worker.
- Bind each run to a source revision/snapshot and preserve previous evidence across retries.
- Treat zero collected tests, missing counters, missing exit code, process-not-launched, timeout and missing artifacts as non-PASS.
- Keep environment failures separate from product-code failures.
