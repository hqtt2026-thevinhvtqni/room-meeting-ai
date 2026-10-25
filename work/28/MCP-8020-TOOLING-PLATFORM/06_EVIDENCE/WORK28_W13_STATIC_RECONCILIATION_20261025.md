# Work 28 / W13 static reconciliation

Date: 2026-10-25
Reviewer: Xu (AI-01)
Scope: source-only review of the existing canonical execution-host implementation on main. No live request was sent.

## Files reviewed

- `execution_host/server.py`
- `execution_host/wee_bridge.py`
- `execution_host/models.py`
- `execution_host/security.py`
- `execution_host/identity.py`
- `tests/test_wee_8031_bridge.py`
- `tests/test_execution_host.py`

## Findings

### BLOCKER 1 — authorization context is not established by the HTTP handler

The `POST /execute` handler constructs `WorkContext` from request JSON. The bridge forwards the supplied work context, including its `authorized` field. The host checks this field, but the inspected HTTP path does not establish it from an authenticated Core authorization decision. A boolean in request JSON must not be treated as proof of authority.

### BLOCKER 2 — request contract does not match Work 28 execution v1

The existing bridge forwards `execution_request.command` as a command argument vector. The staged Work 28 v1 run contract instead requires `work_id`, `entry_path`, `operation`, `expected_source_sha256`, and bounded `timeout_seconds`. These interfaces are not compatible and must not be wired together directly.

### BLOCKER 3 — expected source hash is not enforced in the inspected path

The inspected W13 request model does not carry `expected_source_sha256`; the reviewed bridge path does not prove that an immutable source snapshot matching the caller's expected hash is what ran.

### BLOCKER 4 — runtime identity is returned but not pinned by the bridge

W13 exposes runtime instance/build identity. The inspected bridge does not compare that identity against an independently approved expected runtime identity/build hash before returning a successful status.

### Scope note

The default host bind is `127.0.0.1:8031`, which reduces network exposure but does not replace authorization, Work binding, or source-hash verification. These are source-review findings only; no live exploit or execution was attempted.

## Required sequence

1. Keep all Work 28 execution/evidence tools `NOT_IMPLEMENTED`.
2. Establish caller identity and Work authorization at trusted Core; do not accept the request's boolean as authority.
3. Add a narrow adapter from the v1 contract to the canonical W13 host only after W13 can validate a Work-relative path, reject symlink/reparse escapes, hash an immutable source snapshot, and execute that exact snapshot.
4. Bind result/evidence to request ID, Work ID, expected source hash, approved runtime identity/build, exit code, non-empty test counts, and verified process-tree cleanup.
5. Add negative tests for missing/forged authorization context, mismatched source hash, runtime identity mismatch, path escape, and failed cleanup.
6. Run W13 unit tests, then authorized live E2E against the canonical host. Do not create a second execution host.

## Decision

The existing W13 host is a candidate canonical component, but static evidence does not yet support safe Work 28 activation. The current decision is BLOCKED pending the controls and evidence above. No execution tool is enabled.
