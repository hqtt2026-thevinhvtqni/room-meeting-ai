# Work 33 — Investigation and Delivery Plan

## Phase 1 — READ
1. Inspect existing implementations and contracts in Work 24, Work 28, and Work 30.
2. Identify the current source of truth for file paths, storage, and permissions.
3. Record actual tool names, schemas, service boundaries, and relevant file paths.
4. Capture baseline evidence without changing PC files or running services.

## Phase 2 — TRACE
1. Follow `sandbox_read` from caller through MCP 8020, Core, runtime/storage adapter, and response serialization as applicable.
2. Compare the read contract with the known working implementation on port 8030, if confirmed by evidence.
3. Reproduce the empty-object result and determine the earliest layer where expected content disappears.
4. Record root cause only when supported by trace evidence.

## Phase 3 — DECIDE
1. Choose the smallest compatible design for shared file storage and content retrieval.
2. Define path normalization, access policy, file size limits, binary handling, error semantics, and integrity checks.
3. Identify what requires Vinh's approval before implementation or live integration.

## Phase 4 — BUILD (approval-gated)
1. Implement only the approved scope on an isolated branch/workspace.
2. Add unit and contract tests for success, missing files, denied access, malformed paths, empty files, and binary files where supported.
3. Avoid changing live services until explicitly approved.

## Phase 5 — VERIFY
1. Write a test file with known UTF-8 content and a recorded SHA-256 digest.
2. Read it back through the intended shared-file interface.
3. Compare exact content and digest; test authorized access from Xu, Vi, An, and Ka.
4. Preserve tool responses, timestamps, test results, and commit identifiers as evidence.

## Phase 6 — HANDOFF
Report DONE / PASS / DECISION / BLOCKED per item, list evidence paths and hashes, disclose remaining risks, and wait for Vinh's approval before integration.
