# DOC-002 — WORK 33: W1111 EXECUTION AUTHORITY V1.2 BRANCH TRACE

- Work: W33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-26 (+07)
- Status: FEATURE-BRANCH SOURCE TRACE / STATIC DEFECTS & INTEGRATION RISKS FOUND / NOT RUNTIME VERIFIED
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/w1111-core-execution-authority-v1-2
- Observed branch HEAD: c70eb2b82f54a000a81263dc519078ddf105f075
- PR: #48, OPEN / DRAFT / NOT MERGED
- Compare main...branch: DIVERGED, ahead 157 / behind 1004, 88 changed files
- Exact HEAD workflow runs and combined status exposed by the available GitHub reads: none returned. Historical CI claims in the PR body are not current-HEAD proof.
- Mode: READ / TRACE ONLY. No tests, runtime probes, code edits, secret access, merge, deployment, or configuration change.

## 1. Purpose and branch resolution

The prior Work 33 main-branch trace did not find execution-grant route mounting. This follow-up traced PR #48's changed-file list and its canonical Work 13 / Work 12 source paths. The implementation does exist on the W1111 feature branch; it must not be conflated with the older top-level legacy `execution_host/` files or assumed to exist on main.

## 2. Canonical branch source evidence

| Path | Blob SHA | Finding |
|---|---|---|
| `core/execution_authority.py` | `163b126178b67c6e0a3f68ba33eaf7b9e6d91503` | Core service-credential authentication, Work/purpose-scoped grant, expiry/revocation, append-only hash-chained journal and validation. |
| `room_hop_mcp/adapter/execution_authority_http.py` | `8cb21fadf6bf2318f4884d368b77f2abf796b807` | Grant issuance/status/validate/run-record/revoke routes. |
| `room_hop_mcp/adapter/http_server.py` | `48e05c0f5d8121e35ba9bea01ebd8f338529073c` | Mounts the grant routes in `create_http_app()`. |
| `room_hop_mcp/core_http_main.py` | `d990dd2e152e487c678f67e27add4c0ac94fef53` | Calls `create_http_app(service)`; feature-branch route mount is in this entrypoint path. |
| `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/server.py` | `b0d8308121a63332e1f0dcbff15e6f0da9c273e0` | W13 Host requires grant fields + bearer token, validates online with Core, restricts purpose to pytest_run, verifies Work snapshot and delegates to W12 adapter. |
| `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/wee_bridge.py` | `712170a82cdd8a3b910fe4cadca6f13b91f129a9` | Canonical W13 bridge obtains Core grant with service credential, then calls Host using short-lived bearer grant. Requires HTTPS for remote endpoints; loopback HTTP permitted for development. |
| `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/w12_adapter.py` | present in PR changed-file list | W13 Host delegates to the canonical W12 execution adapter. |
| `13/EXECUTION-HOST-INFRASTRUCTURE/05_TEST/test_core_wee_w13_w12_e2e.py` | present in PR changed-file list | In-process Core API + WEE bridge + W13 HTTP handler + W12 adapter E2E test. |
| `13/EXECUTION-HOST-INFRASTRUCTURE/05_TEST/test_core_grant_host_integration.py` | present in PR changed-file list | Host/Core grant integration and negative legacy-WorkContext / wrong-token tests. |
| `12/WORK-EXECUTION-ENVIRONMENT/04_CODE/wee/authority.py` | `31375a230005e224a22039d80bda0dda3433203c` | Canonical WorkBinding resolver; Work scope resolver, not principal authentication. |

## 3. Corrected bridge and E2E assessment

An earlier preliminary note incorrectly treated the top-level legacy `execution_host/wee_bridge.py` as the canonical bridge. That conclusion is withdrawn.

The actual PR #48 W13 path is different:
- The canonical W13 `wee_bridge.py` authenticates to Core using the enrolled service credential and obtains a short-lived Work-scoped grant.
- It sends grant ID, purpose and bearer grant to W13 Host; it does not send caller WorkContext as authority.
- W13 Host validates the grant online with Core, checks Work/purpose, verifies the source snapshot, then constructs its internal WorkContext and delegates to W12.
- The E2E test calls the bridge with caller context containing `authorized: false` and forged workspace data, yet expects execution to pass using the Core-issued binding. This is intended evidence that caller-supplied WorkContext is ignored.
- The negative integration test expects legacy caller-supplied WorkContext JSON to be rejected and a wrong bearer grant to be denied.

Thus the feature branch does contain the WEE → Core grant → W13 Host → W12 adapter integration path at source/test level. Tests were read, NOT run here. Do not infer runtime proof.

## 4. Confirmed source-hash binding defect

The branch's `tests/test_execution_authority.py` configures the Work policy with `source_sha256 = "a" * 64`, issues a grant, then submits `source_sha256 = "b" * 64` to the run-record endpoint and asserts HTTP 200 with the mismatched hash recorded.

The implementation:
- `record_run()` revalidates the bearer token;
- checks that the submitted source hash is syntactically a SHA-256 string;
- does not compare it with a source digest immutably pinned to the grant;
- the `GRANT_ISSUED` event does not persist the source hash/policy snapshot;
- `validate_grant_token()` reads source binding from the current mutable Work policy.

This is a confirmed static implementation/test defect. Required remediation: persist immutable source hash and policy revision in the grant-issued event; validate and record against that grant-pinned hash; reject mismatch and policy drift; add negative unit and HTTP tests. No exploit was run.

## 5. Additional authority gaps recorded by W1111 review

The W1111 review document `work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/06_EVIDENCE/CO_CORE_AUTHORITY_REVIEW_20261110.md` also records:
1. **Task/assignment binding absent:** current grant binds service identity, Work, purpose, expiry and timeout, but not exact Task/Assignment ID, owner, ACK/claim state, assignment state/version/revocation, or task-level action/resource.
2. **Revocation/run-record race:** final grant validation and run-record append are separate operations; revoke and record may race. Requires serialized atomic state transition and concurrency tests.
3. **Runtime configuration and startup not verified:** production credentials, Work policy, durable store path, Core startup wiring and active runtime remain unproven.
4. **Work-level-only scope:** no task-specific authorization contract.
These are source-review risks/gaps, not runtime exploit findings.

## 6. Branch and CI integration risk

- Branch HEAD observed: `c70eb2b82f54a000a81263dc519078ddf105f075`.
- PR #48 remains OPEN / DRAFT / not merged.
- Branch comparison against main returned DIVERGED, ahead 157 / behind 1004, with 88 changed files.
- Available exact-HEAD workflow-run lookup and combined-status lookup returned empty collections for c70eb2b. PR body contains older successful CI run claims on other SHAs; they are not exact-current-HEAD evidence.
- The PR's large divergence means source correctness does not imply safe mergeability. Require controlled reconciliation, exact-head CI and owner approval.

## 7. Work 33 disposition

- Positive: W1111 feature branch has a concrete Core grant implementation, mounted routes, canonical W13 bridge, W13 Host → W12 adapter path, and integration/E2E tests.
- Confirmed defect: Core run-record endpoint/test accepts a source hash different from the Work policy hash; immutable grant-source binding is missing.
- Additional blockers: Task/Assignment authorization contract, atomic revoke/record semantics, production startup/configuration, exact-HEAD CI visibility and large branch divergence.
- Main remains unproven to contain this implementation; PR is not merged.
- Work 33 must keep `UnconfiguredAuthorizer` fail-closed. Do not implement the Cloud Drive adapter against an unapproved, unmerged, defective or runtime-unverified contract.
- No PASS is claimed.

## 8. Required next actions

1. W1111 owner corrects immutable grant-source binding and adds mismatch/policy-drift negative tests.
2. W1111 owner resolves task/assignment scope and atomic revoke/record contract.
3. W1111 owner reconciles branch against main under approved merge strategy; obtain exact-HEAD CI evidence.
4. Independently verify Core startup, secret enrollment, durable journal and W13/W12 runtime source parity only through approved diagnostics.
5. After correction, merge approval and runtime evidence, Work 33 can implement and test a Core-backed Authorizer adapter using the verified contract.
