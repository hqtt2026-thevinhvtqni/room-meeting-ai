# Work 28 Continuation — Canonical Execution Boundary Source Audit

**Date:** 2026-10-25  
**Owner:** Xu (AI-01)  
**Work:** 28 — MCP Tooling Platform  
**Branch:** `work/28-mcp-tooling-platform`  
**Status:** STATIC AUDIT COMPLETE / LIVE INTEGRATION BLOCKED / NOT RELEASED

## Scope and method

Read-only source inspection of the current branch files:
- `execution_host/server.py`
- `execution_host/security.py`
- `execution_host/identity.py`
- `execution_host/host.py`
- `execution_host/work28_contract.py`
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_authorized_execution_adapter_v1.py`
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_strict_execution_gateway_v1.py`
- `work/28/MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/WORK28_DECISION_WORK12_WORK13_INTEGRATION_20261025.md`

This is static source evidence only. No deployed Core or :8031 request was made; no host code was changed.

## Findings

1. **The staged Work 28 contract is not wired to the host endpoint.** The module header in `execution_host/work28_contract.py` explicitly says it is not wired to HTTP yet. It validates the narrow request and creates a hash-checked snapshot, but explicitly does not authorize callers or claim OS-level immutability.
2. **The current `POST /execute` endpoint trusts caller-supplied context.** In `execution_host/server.py`, the handler deserializes `body['work_context']` into `WorkContext` and `body['execution_request']` into `ExecutionRequest`, then calls `execute_work`. The inspected handler contains no authentication middleware or server-side Core authorization step.
3. **The host's `authorized` check is not itself an identity proof.** `execution_host/security.py` checks `ctx.authorized` as a boolean supplied through `WorkContext`; this alone does not establish who the caller is or whether Core authorized that caller for the requested Work.
4. **Runtime identity exists but is not yet bound to a verified run result.** `execution_host/identity.py` computes a source-tree build hash and instance metadata at process start. Static code inspection does not prove that the live deployed process matches this source or that each result is cryptographically/evidentially bound to that identity.
5. **The host accepts a command-vector path.** `execution_host/host.py` validates command arguments and starts a subprocess. Its current guardrails are useful defense-in-depth but do not satisfy the narrower Work 28 contract by themselves; they do not replace trusted Core authorization, exact immutable snapshot execution, and independently verified process-tree containment.
6. **The Work 28 adapter/gateway are staging seams.** `mcp8020_authorized_execution_adapter_v1.py` and `mcp8020_strict_execution_gateway_v1.py` are not wired into the v54 service/registration. Wiring them alone would not create the missing trusted authorization, snapshot, runtime, or evidence guarantees.

## Decision reaffirmed

- Keep Work 12 frozen; do not create a second host.
- Continue the already recorded narrow Work 13 runtime-boundary hardening request against the canonical existing host.
- Work 28 remains responsible for the caller-facing narrow contract, MCP integration, fail-closed behavior, evidence binding, and integration tests.
- Keep all seven execution/evidence tools `NOT_IMPLEMENTED` and the execution guard in place until the trusted route and live evidence pass.

## Bounded implementation sequence

### W13 host-boundary owner
1. Establish trusted caller authentication and server-side Core authorization at the canonical request boundary; reject caller-provided `authorized` as proof.
2. Route only the narrow request fields: `work_id`, Work-relative `entry_path`, `operation` (`RUN_SCRIPT` or `RUN_TESTS`), `expected_source_sha256`, bounded `timeout_seconds`.
3. Resolve canonical WorkContext from trusted Core; do not accept caller-supplied workspace/evidence paths, command/argv, environment, shell, or principal claims.
4. Execute the exact verified snapshot with pinned runtime identity and verified process-tree cleanup. If OS-level isolation cannot be proven, fail closed and report the exact blocker.

### W28 integration owner
1. Keep the candidate adapter disconnected until the W13 contract and authenticated route are inspectable.
2. Add a server-side client/registration only after the route is verified; preserve authorization on status/output reads.
3. Test hash mismatch, unauthorized caller, cross-Work access, malformed results, timeout, zero-test summary, runtime identity mismatch, and cleanup failure as negative cases.
4. Run authorized positive and negative live E2E through MCP 8030 → authenticated Core :8000 → existing W13 host :8031. Bind each result to run ID, Work ID, source hash, runtime identity, exit/test summary, and protected evidence reference.

## Acceptance gate

Do not mark PASS until all are evidenced against the exact deployed revisions:
- Unauthorized and forged-`authorized=true` requests are denied.
- A valid authorized request executes only the exact Work snapshot whose SHA-256 was checked.
- Cross-Work and path traversal requests are denied.
- Runtime identity matches trusted deployment configuration.
- Test summary has total > 0, failed = 0, errors = 0, exit code 0.
- Timeout and cancellation leave no child process running; cleanup is verified.
- Evidence is protected from ordinary Sandbox write/delete operations and is bound to the exact run.
- Independent security review and live E2E verification pass.

## Current disposition

**Static boundary audit: PASS (source inspection only).**  
**Authenticated live execution: BLOCKED / NOT VERIFIED.**  
**Work 28: ACTIVE / NOT RELEASED.**
