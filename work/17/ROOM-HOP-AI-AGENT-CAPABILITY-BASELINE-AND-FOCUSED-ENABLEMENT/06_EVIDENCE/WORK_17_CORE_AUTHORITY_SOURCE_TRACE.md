# WORK 17 — CORE / AUTHORITY SOURCE TRACE

- Work ID: 17
- Date: 2026-11-19 (+07)
- Scope: GitHub `main` source-level inspection of Core HTTP composition, identity registries, governance, Execution Host request boundary and related tests.
- Mode: READ / TRACE ONLY. No source changes, process execution, tests, endpoint calls, secrets/config changes or runtime probing.
- Repository snapshot: `main` HEAD `384283a2d2894700436e3a1d1ea15369f1ca3402`; recursive tree SHA same; `truncated=false`, 1,097 entries.

## 1. Executive finding

**P0 security blocker — the documented Core-issued execution-grant boundary is not wired into the inspected runtime source path.** The current source exposes a direct Execution Host `POST /execute` path that accepts a caller-supplied `WorkContext`, including `authorized: true`. The Host's local guard checks that boolean; the inspected request path does not authenticate a service identity, validate a Core-issued bearer grant, bind an active Assignment/ACK, or revalidate a source revision against Core before execution.

This is a source-level finding, not a claim that the endpoint is currently publicly reachable. Live bind address, process, proxy/network exposure and deployed build remain NOT VERIFIED. Treat protected execution as DENY until the trusted Core→Host path is implemented and independently tested.

## 2. Source evidence

| Path | Blob SHA | Observation |
|---|---|---|
| `room_hop_mcp/core_http_main.py` | `8dd6bb5ea500026d932ca52eb6079c980d722ab0` | `build_app()` constructs MeetingManager/MeetingService and returns `create_http_app(service)`; no execution-grant router is mounted in this entrypoint. |
| `room_hop_mcp/adapter/http_server.py` | `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d` | Inspected full adapter exposes `/identities` and Meeting routes; no `/works/{work_id}/execution-grants` routes. |
| `execution_host/server.py` | `45aec57525b5d55bb63544b7bd7fd23062e06151` | `POST /execute` parses JSON, constructs `WorkContext(**body['work_context'])`, constructs request and directly calls `host.execute_work`; no request authentication or Core call in handler. |
| `execution_host/models.py` | `2488b7c95cf3784fc26eaf677044fe5ab0866420` | `WorkContext` contains caller-populated boolean `authorized`; no grant token, principal, assignment, ACK, policy version or expiry field. |
| `execution_host/security.py` | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | `validate_context()` accepts/rejects based on `ctx.authorized` boolean and path containment; it does not verify the boolean with Core. |
| `execution_host/host.py` | `977b5bc5072eaf0a3ad054aecd22491483d621b1` | `execute_command()` calls `validate_context` then executes validated command locally. No Core grant validation appears in the inspected execution path. |
| `execution_host/wee_bridge.py` | `eec29b8f43d907e06551329f4ed9e350f51352dc` | Bridge checks local `authorized is True` then sends WorkContext JSON to Host; it does not attach a bearer grant or service credential. |
| `CORE_EXECUTION_AUTHORITY_V1_2_DEPLOYMENT.md` | `ce130f1f9a95daeaafff75ef37eacd4dffc797e2` | Deployment document specifies service credential, Core-issued short-lived grant, Host online validation and pytest-only operation. These requirements are not evidenced as wired into the inspected entrypoint/Host handler above. |
| `tests/test_execution_host.py` | `183cba2959db9d9fb00751055efdeddd09c14a64` | Unit tests create `WorkContext(authorized=True)` directly and test local execution; these tests do not prove Core-issued grant enforcement. |
| `tests/test_core_http_main.py` | `4ffa0f9a977f53387b3350644da02a68ac89890d` | Test confirms missing authority env causes `POST /works/W28/execution-grants` to return 503. It does not prove configured grant issuance/validation/revocation routes or Host integration. |

## 3. Findings and risks

### F-01 — Caller-controlled authorization boolean reaches execution (P0)

The direct HTTP handler accepts `work_context` from request JSON. The dataclass has a public `authorized` field. `validate_context()` treats `True` as authorization evidence. No trusted principal or grant is resolved on this path.

**Risk:** a caller able to reach this Host endpoint may assert `authorized=true` and request execution within the local path/command constraints. This is not equivalent to bypassing all filesystem constraints, but it defeats the intended authority source.

### F-02 — Core execution-grant API contract is documented but not mounted in inspected Core entrypoint (P0)

The deployment document describes five execution-grant routes and required environment variables. The inspected `core_http_main.build_app()` returns the Meeting HTTP app; the complete inspected adapter contains no Work grant routes. The test only covers the unconfigured 503 response for the grant URL.

**Risk:** architecture/deployment documentation may be mistaken for an implemented Core authorization service. Configured behavior and persistent grant lifecycle are NOT VERIFIED.

### F-03 — Host request does not perform online grant validation (P0)

The Host handler and `ExecutionHost` call chain do not make an online Core validation request. The Bridge serializes caller context and does not send a grant token or service credential.

**Risk:** no demonstrated expiry/revocation check, Work/purpose binding, identity binding or source-hash revalidation through Core before effect.

### F-04 — Runtime command policy differs from deployment contract (P0)

Deployment document says Host accepts only `pytest_run`. Inspected Host command allowlist includes `python`, `python3`, `pytest`, `node`, `npm`, `npx`, `git`, `bash`, and `sh`; `validate_command` permits generic commands such as Python `-c`. The direct server forwards the request command to `execute_work`.

**Risk:** the source-level operation surface is broader than the documented pytest-only grant purpose. No claim is made about network reachability or production exposure.

### F-05 — Identity registries are directories, not authentication (P1)

`PrincipalRegistry` and `AgentRegistry` load YAML records. Their docstrings explicitly separate identity resolution from authorization; AgentRegistry says permissions/authority are deferred and no real API calls are made. `identity_resolution.resolve_identity()` classifies registry membership, not proof of authenticated session/provider identity.

**Risk:** registered name/ID cannot be treated as an authenticated principal, a live provider session or authorization to mutate a Work.

### F-06 — Legacy Governance is not a sufficient enforcement boundary (P1)

`core/governance.py` uses identity strings and path/capability matching, defaults unknown identities to `agent_llama`, and writes audit records to a local file. This is not the immutable tuple required by W32 DOC-117 (trusted principal, Work, active Assignment/ACK, exact path/action, source SHA, environment, expiry/revocation and durable audit). The inspected Core/Host path does not show it enforcing the Host HTTP request.

**Risk:** presence of a Governance class can be mistaken for a trusted request-level authorization boundary.

## 4. Current disposition

| Capability | Source-level status | Runtime status |
|---|---|---|
| Principal/Agent registry read | SOURCE EXISTS | NOT VERIFIED |
| Identity resolution | SOURCE EXISTS; membership classification only | NOT VERIFIED |
| Core Meeting HTTP composition | SOURCE EXISTS | NOT VERIFIED |
| Core execution-grant route mounting | NOT FOUND IN INSPECTED ENTRYPOINT/ADAPTER | NOT VERIFIED |
| Host service authentication | NOT FOUND IN INSPECTED HTTP handler | NOT VERIFIED |
| Core grant online validation | NOT FOUND IN INSPECTED Host/Bridge path | NOT VERIFIED |
| Caller-controlled `authorized` field | SOURCE EXISTS | Endpoint reachability NOT VERIFIED |
| Pytest-only command enforcement | CONTRADICTED BY INSPECTED ALLOWLIST | NOT VERIFIED |
| Durable append-only grant/run audit | Described in deployment document; implementation not found in inspected paths | NOT VERIFIED |

## 5. Required remediation design — NOT AUTHORIZED TO BUILD

1. Remove caller authority from request DTO: never accept `authorized`, Work paths or source digest as trusted caller input.
2. Authenticate enrolled service identity at Host ingress using a high-entropy credential over private TLS; reject missing/invalid/revoked identity.
3. Have Core issue a short-lived opaque/bearer grant bound to Work ID, purpose, exact immutable source snapshot, allowed command profile, timeout, policy version and correlation/idempotency IDs.
4. Host must validate grant online with Core immediately before execution and revalidate before protected side effects; Core unavailable or audit persistence failure => DENY.
5. Bind assignment/task state and accountable ACK where the operation requires an AI member task; assignment-ready is not ACK.
6. Enforce the purpose allowlist in code, not only documentation. For `pytest_run`, accept only a constrained pytest invocation and reject arbitrary Python/shell/node/git commands.
7. Persist append-only, hash-chained grant/run events on durable storage; verify restart recovery and tamper detection.
8. Add positive and negative integration tests: missing/invalid service credential, spoofed identity, wrong Work, wrong purpose, expired/revoked grant, source mismatch, over-timeout, arbitrary command, Core unavailable, audit-write failure, replay/idempotency, and concurrent revocation.
9. Obtain independent QE and accountable Core owner review before any G7 request.

## 6. Gate and safety disposition

- G3 Core/Auth trace: SOURCE TRACE DONE for this bounded slice; end-to-end trace NOT PASS.
- GAP-04 remains OPEN.
- New P0 security finding should be tracked as GAP-11.
- Protected execution: DENY / NOT RELEASED pending remediation and independent verification.
- No source change, test execution, endpoint invocation, deployment, permission grant, secret handling or runtime mutation occurred.
- This report does not prove the Host is reachable from an untrusted network; runtime topology and actual deployed build remain NOT VERIFIED.
