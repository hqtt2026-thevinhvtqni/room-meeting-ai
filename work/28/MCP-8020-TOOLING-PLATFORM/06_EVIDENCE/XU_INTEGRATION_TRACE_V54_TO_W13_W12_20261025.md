# Work 28 — Integration Trace: v54 → Authorized Adapter → W13/W12
**Date:** 2026-10-25 (UTC+7)
**Author:** Xu — AI-01 GPT CEO / Quân sư LAB
**Access method:** MCP 8030 Sandbox reads. Static source trace only; no process or test was executed.

## 1. Scope and evidence boundary

Successful sandbox_read_probe calls returned content for Work 28 gateway, sandbox tools, service/catalog excerpts, authorized adapter excerpt, execution contract, and Work 13 server/models. A subsequent ordinary read returned empty objects for several files; a read of the authorized adapter was blocked by the safety checker. That is an access-tool limitation, not evidence of file loss or sandbox failure. No bypass was attempted. Findings below are limited to returned source content and previously recorded verified facts.

## 2. Observed route and blockers

### A. Catalog and service boundary
- Catalog source identifies version 54.0.0-draft1, says Core :8000 is the authorization authority, and says caller-supplied identity is not proof of authority.
- The v54 execution gateway says it is deliberately unwired and that a concrete authenticated Core route, canonical W12/W13 runtime, and OS-isolation gate have not been evidenced.
- Seven execution/evidence tools remain NOT_IMPLEMENTED until a concrete evidenced client is wired. Binding an ExecutionGateway instance alone does not override the catalog/service implementation gate.
- sandbox_run_command is explicitly refused with POLICY_REFUSED; do not provide a generic command route.

### B. v54 gateway contract mismatch
The legacy sandbox_run_python(work_id, script, args, timeout_seconds) builds a request with operation=RUN_SCRIPT, language=python, work_id, entry, args, and timeout_seconds. The hash-bound v1 request validator allows only work_id, entry_path, operation, expected_source_sha256, and timeout_seconds, and requires the source hash. Therefore the legacy gateway request cannot be passed directly to the v1 validator. No direct wiring is safe.

### C. Authorized adapter is a seam, not a deployed trust chain
The readable adapter declares injected interfaces for Core caller authorization, immutable snapshot creation, pinned execution runtime, and approved runtime identity. Its header says the adapter is not wired into MCP registration or v54 service and does not itself authenticate, read/hash source bytes, launch processes, or attest evidence. Protocols and constructor injection do not prove concrete trusted providers exist or are connected.

### D. Canonical W13 request mismatch
The readable W13 models define WorkContext fields including work_id, work_name, workspace_root, execution_workspace, evidence_root, and authorized. ExecutionRequest accepts only command, timeout_seconds, collect_artifacts, and run_test. The W13 server constructs both dataclasses directly from the HTTP request body and then calls the W12 adapter. The current W28 hash-bound request shape is not a valid W13 ExecutionRequest. Do not map entry_path to a caller-controlled command.

The visible W13 POST /execute handler excerpt contains no caller-principal authentication check before parsing the body. This is a static source observation only; it does not prove there is no network-level protection elsewhere. Until a trusted Core-to-runtime authentication mechanism is evidenced, direct access to this endpoint must not be enabled from MCP.

The W13 server startup excerpt configures W12ExecutionAdapter(allow_processes=True, ...). This increases the importance of a tightly authenticated, server-derived request and fixed allowlisted invocation; it is not evidence that the current host is running or properly isolated.

## 3. Safe architecture decision
Keep execution disabled until all gates are satisfied:
1. MCP caller identity is authenticated by trusted middleware; public request fields cannot assert identity or authorization.
2. Core :8000 authorizes the principal for the requested Work and derives WorkContext server-side.
3. A canonical Work resolver rejects path traversal, symlinks/reparse points, and paths outside the authorized Work.
4. The resolver creates an immutable snapshot from exact bytes to execute and independently computes SHA-256; the hash must equal the caller's expected hash.
5. Core maps the operation to a fixed policy-approved Python/pytest entrypoint and controlled argv. No arbitrary shell/command/args passthrough.
6. Core calls only canonical W13/W12 over an authenticated channel and pins/attests runtime identity/build.
7. Result/evidence bind Work ID, snapshot reference, source hash, operation, runtime identity, exit code, bounded outputs, cleanup state, and evidence integrity.
8. Only after runtime authorization and isolation tests pass may service/catalog status change; negative tests must prove no runtime dispatch on every precondition failure.

## 4. Offline work vs runtime gates
Offline/source-only: contract mapping, fail-closed regression tests, catalog/service binding tests, explicit refusal behavior, documentation, and static review of exact source revisions returned by MCP.

Requires authorized runtime/host evidence: active Core :8000 identity/revision, live canonical W13 :8031 identity/revision, authenticated Core→W13 path, OS/process/network isolation, exact snapshot/hash at execution, real Python/pytest exit code, process-tree cleanup, and protected evidence integrity.

## 5. Status
- Source trace and this report: written to Sandbox; readback still required.
- Python/pytest: NOT RUN in this session.
- Live Core/W13 integration and E2E: NOT VERIFIED.
- Seven execution/evidence tools: NOT_IMPLEMENTED.
- sandbox_run_command: POLICY_REFUSED.
- Work 28: ACTIVE / BLOCKED / NOT RELEASED.

No claim of PASS is made for tests or live execution.
