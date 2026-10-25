# Work 28 Decision — Work 12 / Work 13 integration boundary

- Date: 2026-10-25
- Decision owner: Xu (AI-01), architecture/integration coordination
- Scope: decide whether Work 12 or Work 13 must be reopened to complete Work 28.
- Status: DECISION RECORDED / IMPLEMENTATION AND LIVE VERIFICATION STILL REQUIRED

## Decision

**Do not reopen Work 12 or Work 13 by default. Integrate their existing contracts/components into Work 28, and open a source Work only if implementation evidence proves a change to that Work's owned boundary is necessary.**

### Work 12 — keep frozen

- Treat Work 12 as COMPLETED / LOCKED.
- Do not edit its frozen contract, duplicate its host, or create Core 2 / another execution host.
- Work 28 must consume the canonical interfaces already agreed for the execution path.
- Reopen Work 12 only if a concrete incompatibility is proven to require changing a Work 12-owned contract; record the exact incompatible field/behavior and obtain an explicit scope decision before modifying it.

### Work 13 — reuse the canonical execution host

- Reuse the existing Work 13 Execution Host at :8031 and its bridge/adapter; do not build a parallel runtime.
- Work 28 owns the public narrow request contract, MCP service/connector integration, fail-closed gates, result/evidence binding, and integration tests.
- Work 13 should be reopened only for changes to its owned runtime boundary that cannot safely be implemented in the Work 28 integration layer. Current static evidence identifies such gaps in the existing :8031 path: authenticated Core authorization is not established by the inspected HTTP handler; command-vector interface does not match the narrow Work 28 contract; expected source hash/immutable snapshot is not enforced; runtime identity is not pinned by the bridge; process-tree cleanup is not verified.
- First implement a Work 28-side adapter/protocol and tests against the existing host contract. If a required control necessarily belongs inside the canonical W13 host (snapshot execution, timeout/process-tree cleanup, or trusted runtime identity enforcement), record a narrowly scoped W13 change request instead of silently changing W13 from Work 28.

## Required integration contract

The external Work 28 request is limited to:
- `work_id`
- Work-relative `entry_path`
- `operation`: `RUN_SCRIPT` or `RUN_TESTS`
- `expected_source_sha256`
- optional bounded `timeout_seconds`

Do not accept caller-supplied command/argv/script/cwd/shell/env/principal/authorized fields. Caller identity must originate from authenticated server middleware; Work authorization must be established by trusted Core. The exact immutable snapshot whose SHA-256 was checked must be the snapshot executed. Results must bind request/run IDs, Work ID, snapshot, source hash, approved runtime identity, exit code, evidence reference, and verified process-tree cleanup. A test run can pass only with total > 0 and failed = errors = 0.

## Activation gate

Until both unit/regression tests and authorized live Core → existing W13 HTTP :8031 end-to-end verification pass with inspectable evidence:
- Keep all seven execution/evidence MCP tools `NOT_IMPLEMENTED`.
- Keep the connector execution guard in place.
- Do not claim runtime integration PASS or release Work 28.
- Do not send live execution requests or modify host/runtime configuration without an authorized test path.

## Evidence basis

- `03_ARCHITECTURE/WORK28_W13_ADAPTER_IMPLEMENTATION_PLAN_V1.md`
- `06_EVIDENCE/WORK28_W13_STATIC_RECONCILIATION_20261025.md`

The cited findings are static source review, not live runtime evidence. This decision does not declare Work 12 or Work 13 newly completed, and does not claim Work 28 integration is complete.
