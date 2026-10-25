# Work 28 — Canonical W13 compatibility guard
**TÊN:** Co  
**CHỨC DANH:** Coder / ROOM-HOP  
**NGÀY:** 25/10/2026  
**GIỜ - PHÚT:** 11:12 (UTC+7)

## Change made in Sandbox
Added:
- `04_CODE/mcp8020_w13_contract_compatibility_v1.py`
- `05_TEST/test_mcp8020_w13_contract_compatibility_v1.py`

## Why this change
Static source reads of Work 13 canonical `models.py` show:
- WorkContext requires `work_id, work_name, workspace_root, execution_workspace, evidence_root, authorized`.
- ExecutionRequest accepts `command, timeout_seconds, collect_artifacts, run_test`.
- Work 28 contract uses `work_id, entry_path, operation, expected_source_sha256, timeout_seconds`.

A mapper that returns a two-part payload and calls it W13-compatible is misleading: the execution request has unsupported fields and no `command`; the context may be missing required fields. Mapping `entry_path` to `command` is not safe and would erase the intended fixed-entrypoint/hash-bound model.

## Fail-closed behavior
The new audit helper validates Work 28 request shape, verifies canonical WorkContext field presence, and then refuses the current incompatible schema with explicit diagnostic errors. It does not call HTTP, infer authorization from `authorized=True`, translate an entry path into a command, or activate tools.

## Tests authored (NOT RUN in this session)
Five offline regression cases cover:
1. Current W28 hash-bound schema rejected as W13-incompatible.
2. Incomplete WorkContext rejected.
3. Caller-provided `authorized=True` does not bypass context completeness.
4. No unsafe `entry_path` → `command` mapping.
5. Invalid SHA-256 request rejected.

## Verification boundary
MCP 8030 provides Sandbox file operations only in this session. No Python/pytest execution action was available, so tests are **AUTHORED / NOT RUN**. This change is not deployed to Work 13/Core and is not wired into the live service. Seven execution/evidence tools remain NOT_IMPLEMENTED; `sandbox_run_command` remains POLICY_REFUSED.

## Required next integration work
Work 13/Core owners must expose a versioned, authenticated, server-derived execution contract that accepts a constrained entrypoint + immutable source snapshot/hash without arbitrary command strings. Authentication, authorization, source hashing at execution time, process isolation, runtime identity, protected evidence, and end-to-end read-back must be wired and independently verified before activation.

**Work 28: ACTIVE / BLOCKED / NOT RELEASED.**
