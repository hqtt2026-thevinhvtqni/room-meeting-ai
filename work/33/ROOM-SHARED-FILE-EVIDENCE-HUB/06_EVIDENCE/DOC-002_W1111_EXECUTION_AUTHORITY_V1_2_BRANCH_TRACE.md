# DOC-002 — WORK 33: W1111 EXECUTION AUTHORITY V1.2 BRANCH TRACE

- Work: W33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-26 (+07)
- Status: FEATURE-BRANCH SOURCE TRACE / DEFECT CONFIRMED BY STATIC TEST ASSERTION / NOT RUNTIME VERIFIED
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch inspected: work/w1111-core-execution-authority-v1-2
- Mode: READ / TRACE ONLY. No test execution, runtime probe, secret access, code edit, merge, deployment, or configuration change.

## 1. Why this trace was required

The prior main-branch trace found a mismatch: deployment documentation described Core execution-grant routes, but the inspected main source did not mount them. This follow-up checks the named W1111 feature branch to determine whether the implementation exists elsewhere.

## 2. Branch source evidence

| Path | Blob SHA | Finding |
|---|---|---|
| `core/execution_authority.py` | `163b126178b67c6e0a3f68ba33eaf7b9e6d91503` | Core service credential authentication, Work/purpose-scoped grant issuance, expiry/revocation, hash-chained append-only event store, online token validation. |
| `room_hop_mcp/adapter/execution_authority_http.py` | `8cb21fadf6bf2318f4884d368b77f2abf796b807` | Implements POST grant issuance, GET status, GET validate, POST run record and POST revoke routes. Missing configuration returns 503. |
| `room_hop_mcp/adapter/http_server.py` | `48e05c0f5d8121e35ba9bea01ebd8f338529073c` | Imports ExecutionAuthority and mounts the execution-grant routes in `create_http_app()`; unconfigured authority remains fail-closed. |
| `room_hop_mcp/core_http_main.py` | `d990dd2e152e487c678f67e27add4c0ac94fef53` | Calls `create_http_app(service)`; on this feature branch, the HTTP adapter mount is therefore in the Core entrypoint path. |
| `execution_host/server.py` | `dd65fcfacfc171e673000ecbeba01d5842a42e8c` | Requires grant ID, Work ID, purpose and bearer token; validates online with Core; restricts operation to pytest_run; checks timeout and workspace source snapshot; constructs trusted WorkContext only after grant validation. |
| `execution_host/source_snapshot.py` | `b24675dc1fe17e285a083b582cd6b25400135101` | Computes deterministic SHA-256 over sorted workspace file paths and contents; rejects symlinks and special files. |
| `execution_host/models.py` | `64e3de59375daf451d875eacf0df91ccb7e30dbe` | WorkContext still has an `authorized` field, but the HTTP handler constructs it internally after online Core validation rather than accepting it in request JSON. |
| `execution_host/wee_bridge.py` | `eec29b8f43d907e06551329f4ed9e350f51352dc` | Still sends the legacy caller-supplied WorkContext + ExecutionRequest to `/execute`, requires `authorized is True`, and does not attach grant ID/purpose/bearer token. It is not adapted to the new Host request contract. |
| `tests/test_execution_authority.py` | `4ea5158c07df1e66183a6fbe7a6f79042332605d` | Tests grant issuance, wrong credentials, Work/purpose restrictions, revocation, hash chain and HTTP routes. Contains a source-hash mismatch acceptance test described below. |
| `tests/test_execution_host_authority.py` | `f83ec99e1f95e5bc1ee4203b1e0dd608ba4e9d37` | Tests source snapshot determinism/symlink rejection and Host execution behaviors; tests were read, not run. |

## 3. Confirmed source-hash binding defect

The test fixture creates a Work policy with `source_sha256 = "a" * 64`. It then issues a grant for that Work. In the HTTP test, the POST run-record request supplies `source_sha256 = "b" * 64` and asserts that the endpoint returns HTTP 200 and records the supplied `"b" * 64`.

The implementation explains why this is accepted:
- `ExecutionAuthority.record_run()` revalidates the bearer token, checks only that the supplied source hash is syntactically a 64-character lowercase SHA-256, then appends that supplied value.
- It does not compare the supplied hash with the source hash bound to the grant/Work policy.
- The issued event does not persist an immutable source snapshot digest for later comparison.
- `validate_grant_token()` currently resolves source binding from the current Work policy, rather than an immutable source digest captured at issuance.

This is a confirmed static implementation/test defect, not a runtime exploit demonstration. The required repair is to pin the canonical source snapshot digest into the immutable grant-issued event and reject run records unless the submitted digest exactly matches that grant-pinned digest. Add negative tests for mismatched source hash and policy drift after grant issuance.

## 4. Integration gap: legacy WEE bridge

Although the Core route mount and new Host request path exist on this feature branch, `execution_host/wee_bridge.py` remains on the legacy contract:
- requires `work_context.authorized is True`;
- posts `work_context` and `execution_request`;
- does not send the grant ID, purpose or bearer token expected by the new Host handler.

Therefore, the branch contains the new Core/Host authority path but the inspected WEE bridge is not wired to it. Do not infer end-to-end execution from the presence of the Core routes and Host handler alone.

## 5. Additional review notes

1. The Host's `/health` response reports status PASS when the Host object exists even if Core authority is not configured; it separately reports `core_authority_configured: false`. Consumers must not interpret this as protected execution readiness.
2. The Core service credential is used to issue grants; the Host then validates bearer grants online. Private TLS/network isolation remains a deployment requirement.
3. The append-only JSONL hash chain detects content modification when read, but does not by itself provide an independent remote/WORM anchor or verified backup/restore.
4. No Core runtime, Host runtime, route probe, test suite, CI run, deployment, merge, or security review was performed in this trace.

## 6. Disposition for Work 33

- Positive: the W1111 feature branch does contain a concrete Core grant service, HTTP route mount and Host-side online validation path.
- Blocking defect: run-record source hash is not bound to the grant's canonical source snapshot.
- Blocking integration gap: legacy WEE bridge does not speak the new grant-based Host contract.
- Branch status/merge/deployment must be checked independently before any adoption; feature-branch source is not proof of current-main or runtime behavior.
- Work 33 must continue to use `UnconfiguredAuthorizer` and deny access until an approved, corrected, integrated, source-matched and independently tested Core adapter exists.
- No PASS is claimed.

## 7. Required next actions

1. Send the source-hash binding defect and bridge contract mismatch to the W1111 owner for correction; do not patch another Work's branch from W33.
2. Require tests that reject mismatched source hash, grant-policy drift, expired/revoked/wrong-Work grants, missing Core, wrong purpose, timeout overflow and legacy WorkContext spoofing.
3. Adapt the WEE bridge only under W1111 ownership and prove it supplies a short-lived grant without exposing the token in logs.
4. Reconcile the exact branch head, PR status and merge approval before considering main integration.
5. Run source-matched tests and isolated E2E only after authorized review; record exact commit, command, output and independent QE verdict.
6. Only then design and test the Cloud Drive Core Authorizer adapter against the verified contract.
