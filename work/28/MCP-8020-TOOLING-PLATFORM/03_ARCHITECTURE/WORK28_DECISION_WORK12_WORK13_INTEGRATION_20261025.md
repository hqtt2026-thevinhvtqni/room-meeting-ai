# Work 28 Decision — Work 12 / Work 13 integration boundary

- Date: 2026-10-25
- Decision owner: Xu (AI-01), architecture/integration coordination
- Scope: decide whether Work 12 or Work 13 must be reopened to complete Work 28.
- Status: DECISION RECORDED / IMPLEMENTATION AND LIVE VERIFICATION STILL REQUIRED

## Decision

**Do not reopen Work 12. Reopen Work 13 narrowly for runtime-boundary hardening, while Work 28 remains the owner of MCP integration and acceptance.** Static source evidence already shows that the existing W13 host path cannot currently guarantee the exact snapshot/hash, trusted runtime pinning, and verified process-tree cleanup required by Work 28. These controls cannot be honestly supplied by a Work 28 wrapper alone while the canonical host still accepts arbitrary command vectors and does not expose the required guarantees. This is a bounded W13 change request, not a restart of Work 13 or permission to build another host.

### Work 12 — keep frozen

- Treat Work 12 as COMPLETED / LOCKED.
- Do not edit its frozen contract, duplicate its host, or create Core 2 / another execution host.
- Work 28 must consume the canonical interfaces already agreed for the execution path.
- Reopen Work 12 only if a concrete incompatibility is proven to require changing a Work 12-owned contract; record the exact incompatible field/behavior and obtain an explicit scope decision before modifying it.

### Work 13 — reuse the canonical host and reopen only its runtime boundary

- Reuse the existing Work 13 Execution Host at :8031 and its bridge/adapter; do not build a parallel runtime.
- Work 28 owns the public narrow request contract, MCP service/connector integration, fail-closed gates, result/evidence binding, and integration tests.
- **Required bounded W13 scope:** establish trusted Core authorization at the canonical request boundary; replace arbitrary command-vector forwarding with the narrow Work 28 operation mapping; enforce Work-relative immutable snapshot/hash verification; pin runtime identity from trusted configuration; enforce timeout and verify process-tree cleanup. Keep these changes confined to the existing W13 host/bridge; no new host and no Work 12 changes.
- Work 28 must implement and test the caller-facing contract/adapter and end-to-end evidence checks in parallel. Do not silently fake host guarantees in the Work 28 wrapper; the wrapper must fail closed until W13 exposes enforceable guarantees.

## Required integration contract

The external Work 28 request is limited to:
- `work_id`
- Work-relative `entry_path`
- `operation`: `RUN_SCRIPT` or `RUN_TESTS`
- `expected_source_sha256`
- optional bounded `timeout_seconds`

Do not accept caller-supplied command/argv/script/cwd/shell/env/principal/authorized fields. Caller identity must originate from authenticated server middleware; Work authorization must be established by trusted Core. The exact immutable snapshot whose SHA-256 was checked must be the snapshot executed. Results must bind request/run IDs, Work ID, snapshot, source hash, approved runtime identity, exit code, evidence reference, and verified process-tree cleanup. A test run can pass only with total > 0 and failed = errors = 0.

## Ownership split and activation gate

- Work 13 reopened scope: only canonical host/bridge runtime-boundary controls listed above.
- Work 28 scope: adapter contract, MCP registration/service, connector guard coordination, regression tests, evidence package, and final activation decision.
- Work 12: remains frozen and untouched.



Until both unit/regression tests and authorized live Core → existing W13 HTTP :8031 end-to-end verification pass with inspectable evidence:
- Keep all seven execution/evidence MCP tools `NOT_IMPLEMENTED`.
- Keep the connector execution guard in place.
- Do not claim runtime integration PASS or release Work 28.
- Do not send live execution requests or modify host/runtime configuration without an authorized test path.

## Evidence basis

- `03_ARCHITECTURE/WORK28_W13_ADAPTER_IMPLEMENTATION_PLAN_V1.md`
- `06_EVIDENCE/WORK28_W13_STATIC_RECONCILIATION_20261025.md`

The cited findings are static source review, not live runtime evidence. This decision authorizes a narrowly scoped Work 13 continuation for the identified host-boundary gaps; it does not reopen Work 12, restart all of Work 13, or claim Work 28 integration is complete.
