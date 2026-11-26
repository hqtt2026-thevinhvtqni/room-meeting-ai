# DOC-006 — Core Identity & Execution Authority Source Trace

- Work: 33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-27
- Review mode: read-only GitHub source inspection; no runtime/PC changes
- Decision status: EVIDENCE / BLOCKED FOR INTEGRATION
- Scope: Core identity discovery, Execution Authority V1.2 branch, WEE/W13/W12 execution path
- Explicit non-scope: Cloud Drive human/AI user authentication, upload/download/share authorization, production deployment

## 1. Main branch baseline

Inspected main source:
- core/identity.py blob cc0d8bc1310949c37cb1d5211ca0451b3a0d24e4
- core/identity_resolution.py blob 207c0ea74e3c77929c1723b0e66beba4ccf36201
- core/governance.py blob aa68e79304465b9bac3bfffe95d94943b97bfecd
- room_hop_mcp/core_http_main.py blob 8dd6bb5ea500026d932ca52eb6079c980d722ab0
- room_hop_mcp/adapter/http_server.py blob 54cb3ecbce2e6b13083f31c14f0c1f0738f1457d
- execution_host/security.py blob 4aa20fbc9c5939c49c85222916dc28fb8dd8075
- execution_host/models.py blob 2488b7c95cf3784fc26eaf677044fe5ab0866420
- execution_host/server.py blob 45aec57525b5d55bb63544b7bd7fd23062e06151
- CORE_EXECUTION_AUTHORITY_V1_2_DEPLOYMENT.md blob ce130f1f9a95daeaafff75ef37eacd4dffc797e2

Findings:
1. GET /identities is read-only registry discovery. It lists registry IDs/names/types; it does not authenticate the caller or issue signed credentials.
2. core/identity_resolution.py resolves whether an ID exists in PrincipalRegistry or AgentRegistry. It is registry classification, not proof of possession or authorization.
3. core/identity.py::verify_identity_claim compares text claims with process runtime identity and logs UNVERIFIED; it is not cryptographic authentication.
4. core/governance.py is a local identity-string capability/path check with fallback identity agent_llama; it is not an HTTP bearer-token verifier.
5. Main room_hop_mcp/core_http_main.py builds the Meeting API only. Main room_hop_mcp/adapter/http_server.py has no import/mount of ExecutionAuthority or /works/{work_id}/execution-grants routes in the inspected snapshot.
6. Main execution_host/server.py accepts caller-supplied WorkContext JSON, including authorized; main execution_host/security.py::validate_context trusts the boolean. No online Core grant check is wired in this inspected main path.
7. Therefore the deployment document's described authority route behavior is not proof that current main has those routes mounted or that the live :8000/:8031 runtime uses them.

## 2. W1111 PR #48 — distinct feature implementation

Inspected immutable feature snapshot c70eb2b82f54a000a81263dc519078ddf105f075 and PR #48 metadata.
- PR #48 title: feat(core): implement Work-scoped Execution Authority V1.2
- State: OPEN, DRAFT, NOT MERGED.
- Head branch: work/w1111-core-execution-authority-v1-2
- PR metadata reports 157 commits, 88 changed files; base was main SHA a663bd5afda524cb9dc7ca685945ca96c68d664d.
- PR description claims an earlier CI run 42732254869 on 9bbeed63...; current immutable head c70eb2b... has no GitHub status contexts in the status endpoint checked. Do not treat old run as exact-current-HEAD CI evidence.

Feature source reviewed:
- core/execution_authority.py blob 163b126178b67c6e0a3f68ba33eaf7b9e6d91503
- room_hop_mcp/adapter/execution_authority_http.py blob 8cb21fadf6bf2318f4884d368b77f2abf796b807
- room_hop_mcp/adapter/http_server.py feature snapshot mounts additive authority routes
- room_hop_mcp/core_http_main.py feature snapshot builds app through adapter
- 13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/server.py feature snapshot validates bearer grant online, obtains canonical Work binding from Core, recomputes source digest, calls W12
- 13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/wee_bridge.py blob 712170a82cdd8a3b910fe4cadca6f13b91f129a9
- 12/WORK-EXECUTION-ENVIRONMENT/04_CODE/wee/authority.py blob 31375a230005e224a22039d80bda0dda3433203c
- tests/test_execution_authority.py blob 4ea5158c07df1e66183a6fbe7a6f79042332605d

Feature architecture:
1. Enrolled service identity authenticates using high-entropy credential whose SHA-256 digest is stored in Core config.
2. Core issues short-lived Work/purpose-bound bearer grant and appends grant events to a local fsynced hash-chained JSONL store.
3. WEE bridge requests grant; W13 Host validates it online with Core, checks Work/purpose/timeout, recomputes source snapshot, then delegates to canonical W12 host.
4. This is a service-to-execution-host authority path, not general Cloud Drive human/AI user authentication.

## 3. Confirmed defect and limits

ExecutionAuthority.issue_grant() stores grant ID, Work ID, service identity, purpose, timeout, expiry, token hash and status in GRANT_ISSUED, but the inspected implementation does not pin source_sha256 or an immutable Work policy revision in that event.

validate_grant_token() obtains current mutable Work policy from _work_policies when returning source_sha256. record_run() revalidates bearer token and SHA-256 syntax, but does not compare submitted source_sha256 against an immutable digest pinned to the grant. The feature test explicitly submits "b"*64 when configured Work source digest is "a"*64 and expects HTTP 200; this encodes the defect rather than a safe negative test.

Required repair before any use:
- Pin immutable source SHA-256 and Work policy revision/digest into GRANT_ISSUED.
- Validate against the pinned snapshot, not current mutable policy.
- record_run() must reject any source digest not equal to grant-pinned digest.
- Add negative unit + HTTP tests for mismatch and policy drift.
- Review grant revoke/run-record race and startup/config hardening.
- Verify exact current PR HEAD CI before considering review closure.

## 4. Cloud Drive integration decision

- Do NOT reuse this W1111 grant as Cloud Drive's user/agent identity contract.
- It is scoped to a registered service identity + Work + pytest_run purpose.
- Cloud Drive requires a separate Core-backed principal/authentication and authorization adapter covering spaces, objects, uploads, parts, versions, shares, quota, audit, and recovery, with explicit resource/action scope and tenant isolation.
- Keep UnconfiguredAuthorizer fail-closed until Core token issuer/verifier contract is proven and negative tests pass.
- Do not accept caller-supplied Principal.subject_id, display name, agent ID, or authorized=true as authentication.

## 5. Verification status

- Static source trace: DONE for the listed snapshots.
- Live Core :8000 and Host :8031: NOT VERIFIED.
- Feature PR merge/deployment: NOT AUTHORIZED / NOT DONE.
- Cloud Drive Core-backed authentication: NOT IMPLEMENTED.
- Production security acceptance: BLOCKED.

## 6. Next actions

1. Keep PR #48 separate; request/perform exact-HEAD source repair and CI evidence before any merge decision.
2. Draft a distinct Cloud Drive Core principal contract and adapter only after identifying a real Core token issuer/verifier API. No invented endpoint.
3. Test forged subject, invalid/expired/revoked token, wrong audience/issuer, cross-Work/tenant access, timeout/fail-closed, and audit failure.
4. Record all new evidence in Work 33 journal. No PC restart, deployment, secret provisioning, or live config change without explicit authorization.
