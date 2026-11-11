# DOC-118 — Work32 Core-Owned Execution Authority Implementation Contract

- **Document Number:** DOC-118
- **Priority:** P0 — protected execution authorization
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Architecture decision owner:** Xu — DECISION APPROVED
- **Implementation branch:** work/32-core-owned-execution-authority-20261112
- **Starting source:** PR #49 head 0ec30f0b8c089fe9f7bcc75b062a4c7e03e281c6
- **Status:** IMPLEMENTATION SLICE CREATED — CI / SECURITY REVIEW PENDING — PROTECTED EXECUTION DENIED

## 1. Accepted authority boundary

Core :8000 is the sole Execution Authority owner:
- resolve an enrolled service credential to a server-side Agent principal;
- authorize the Work, Assignment, Task, target Host, purpose, source revision, environment and timeout;
- issue a short-lived scoped Grant, validate it online, revoke it, and persist an append-only audit/run journal.

Execution Host :8031 is the sole process execution owner:
- accept only a Grant reference/token, never a caller-supplied WorkContext or authorized boolean over HTTP;
- obtain the canonical binding from Core;
- recompute the immutable workspace source SHA-256;
- validate the Grant online and revalidate immediately before process creation;
- execute only the Core-bound pytest entrypoint;
- persist local evidence and submit a bound Run Record to Core.

Build MCP :8030 remains a tool interface and is not an authority owner.

Required chain:
Canonical Authority → WorkContext → LifecycleController → ExecutionHost.

## 2. Contract decisions made for the Work32 first protected operation

- Initial protected purpose is deliberately narrow: pytest_run only.
- A Grant is bound to Work ID, server-derived Agent principal, issuer service identity, Assignment ID, Task ID, target Host service identity, source SHA-256, environment ID, exact pytest entrypoint, timeout ceiling, policy version, issued time and expiry.
- Assignment and Task must be present in canonical WorkContext and must also be allow-listed in Core's Work policy. No caller can widen those allow-lists.
- The issuer identity and Host identity are separate enrolled service identities. Agent principal is resolved by Core from credential configuration and Agent Registry; it is not trusted from the request body.
- Grant token is returned once; only its SHA-256 digest is persisted. No token is logged or copied into Run Record.
- Host makes an online Core validation for each execution and a second online validation immediately before spawning the test process. No cached ALLOW decision is used.
- Core outage, invalid/revoked/expired Grant, source mismatch, policy mismatch, or Host inability to persist the Run Record blocks acceptance.
- Host and Core HTTP bind to loopback by default. Remote transport requires HTTPS; the current HTTP servers reject non-loopback bind.

## 3. Implemented source slice

The implementation branch introduces:
- core/execution_authority.py: Core-owned Grant state, service credential resolution, Work policy binding, short-lived tokens, revocation and hash-chained fsynced journal.
- room_hop_mcp/adapter/execution_authority_http.py: Core issue/status/validate/revoke/run-record HTTP routes; fail-closed when authority configuration is absent.
- room_hop_mcp/core_http_main.py: mounts the additive authority router in the existing Core process.
- execution_host/source_snapshot.py: deterministic immutable workspace source fingerprint; symlinks are rejected.
- execution_host/core_authority_client.py: Host online Core validation and Run Record client; remote HTTP is rejected.
- execution_host/granted_host.py and execution_host/server.py: grant-only Host HTTP boundary, Core-derived execution binding, pytest-only command, immediate revalidation, evidence and Run Record.
- wee/bridge/core_grant_host.py: WEE adapter that obtains a Core Grant, calls Host, then requests Grant revocation.
- wee/authority.py, wee/models.py, wee/controller.py, wee/cli.py: canonical Assignment/Task/Environment/Host binding is carried in WorkContext; LifecycleController no longer equates discovery with execution and requires the Core-grant adapter for protected execution.

## 4. Tests added to the Work32 CI workflow

- tests/test_execution_authority.py: scope denial, service identity, issue/validate/revoke, Run Record binding and journal tamper.
- tests/test_execution_source_snapshot.py: deterministic hash, cache exclusions and symlink rejection.
- tests/test_execution_host_grants.py: Host online validation twice, canonical pytest-only operation and revocation-before-spawn negative case.
- tests/test_wee_lifecycle_authority.py: no false EXECUTE PASS from discovery, real grant adapter path and test failure propagation.

The workflow's bounded unit/E2E lists were extended to include these tests. No test result is claimed until an exact-SHA run completes.

## 5. Deployment configuration contract — not provisioned

Core requires:
- ROOM_HOP_EXECUTION_IDENTITIES_JSON: service ID → credential SHA-256, kind (agent or host), and server-side principal ID for agent services.
- ROOM_HOP_EXECUTION_WORKS_JSON: Work policy including work_name, allowed_identities, allowed_host_identities, allowed_assignments, allowed_tasks, canonical paths, source SHA-256, environment ID, exact pytest entrypoint, max timeout and policy version.
- ROOM_HOP_EXECUTION_STORE_PATH: durable journal path.

Execution Host requires:
- ROOM_HOP_CORE_AUTHORITY_URL
- ROOM_HOP_EXECUTION_HOST_ID
- ROOM_HOP_EXECUTION_HOST_CREDENTIAL

Grant issuer requires:
- ROOM_HOP_CORE_AUTHORITY_URL
- ROOM_HOP_EXECUTION_AGENT_ID
- ROOM_HOP_EXECUTION_AGENT_CREDENTIAL
- canonical Work binding with Assignment, Task, Environment and Host identity.

No credentials, production policy, path, environment identity or live service state is invented or committed by this document.

## 6. Known implementation-review items

Before protected execution can be enabled:
1. Run exact-SHA CI including all new focused tests; resolve every failure.
2. Add HTTP-level tests for issue/validate/revoke/run routes and unconfigured fail-closed behavior.
3. Review hash-chain persistence and cross-process locking on Windows and POSIX; test restart replay, concurrent issue/revoke/record and corruption fail-closed.
4. Review token lifetime, credential rotation, identity mapping and revocation race semantics.
5. Verify source snapshot parity between canonical Work workspace, issuer and Host; verify the actual deployment uses the same immutable workspace.
6. Verify Run Record persistence failure behavior and evidence retention/ownership.
7. Independent security review and positive/negative live E2E on the exact deployed build.
8. Verify the actual LifecycleController → CoreGrantExecutionHost → Execution Host path, not only direct adapter tests.
9. Keep remote exposure, multi-process/multi-host deployment, staging, production, merge and release blocked until separately evidenced.

## 7. Change-control

- Work32 implementation branch only; main and PR #49 integration branch are not merged or modified by this implementation.
- No Core/Host process was started or reconfigured.
- No production credential or runtime Work policy was provisioned.
- No protected command was executed.
- MCP :8020 sandbox_read() restriction remains unchanged.

**Conclusion:** Core-owned Execution Authority is the accepted architecture. This branch is an implementation candidate, not proof of a live secure deployment. PROTECTED EXECUTION DENIED; Work32 remains ACTIVE — NOT RELEASED.

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Decision:** Recorded the implementation contract and the fail-closed acceptance boundary under Xu's approved architecture.

## NHẬT KÝ

- **W32-LOG-20261112-110**
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- Created isolated Core-owned Execution Authority implementation branch from exact PR #49 head.
- Added Core Grant authority/store/router, Host online validation and grant-only HTTP route, deterministic source fingerprint, WEE Core-grant adapter and lifecycle integration.
- Added focused tests and registered them in Work32 CI workflow.
- Opened draft PR #51 against the Work32 integration branch for review.
- Exact-SHA CI has not yet been observed; no PASS is claimed.