# DOC-001 — WORK 33: CORE AUTHORITY SOURCE TRACE ADDENDUM

- Work: W33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-26 (+07)
- Status: SOURCE TRACE RECORDED / RUNTIME NOT VERIFIED / NO BUILD AUTHORIZATION
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch inspected: main
- Tree SHA observed: c292956938c149f4c3f68c8c718c8caeb190f31f
- Mode: READ / TRACE ONLY. No code execution, runtime probe, configuration change, secret access, or deployment.

## 1. Purpose

Continue the Work 33 Core identity and authorization investigation. Determine whether existing ROOM-HOP identity, governance, Work binding, and execution authority modules can be reused as the trusted authorization boundary for Cloud Drive.

## 2. Source files inspected

| Path | Observation |
|---|---|
| `room_hop_mcp/core_http_main.py` | `build_app()` creates MeetingManager/MeetingService and returns `create_http_app(service)`. The inspected entrypoint does not mount an execution-grant router. |
| `room_hop_mcp/adapter/http_server.py` | Exposes read-only `GET /identities` and Meeting routes. No `/works/{work_id}/execution-grants` route found in the inspected file. |
| `core/identity_resolution.py` | Resolves an identity ID through PrincipalRegistry then AgentRegistry. It classifies registry membership; it does not authenticate the caller or authorize a Work action. |
| `core/identity.py` | Runtime identity is assigned at process initialization; text claims are treated as unverified. The module describes itself as a limited rule, not a full identity registry/attestation system. |
| `core/message_identity.py` | Builds a message header from registry data and rejects unresolved IDs. This is message attribution, not proof of authenticated request origin. |
| `core/governance.py` | Uses identity strings, capability/path matching, default fallback to `agent_llama`, and local audit text. It is not shown enforcing the Execution Host HTTP request. |
| `wee/authority.py` | `CanonicalWorkAuthority` reads a local JSON Work binding and checks required fields / Work ID. It resolves Work scope; it does not authenticate a principal or issue/validate a grant. |
| `execution_host/server.py` | The inspected handler accepts caller-supplied `WorkContext` JSON and forwards it to `ExecutionHost.execute_work`. |
| `execution_host/models.py` | `WorkContext` includes caller-populated `authorized: bool`. |
| `execution_host/security.py` | `validate_context()` rejects when that boolean is false; the inspected function does not validate a Core-issued grant. |
| `execution_host/wee_bridge.py` | Checks local `authorized is True` then sends WorkContext to Host; no bearer grant/service credential is attached in the inspected code. |
| `CORE_EXECUTION_AUTHORITY_V1_2_DEPLOYMENT.md` | Describes service credentials, Core-issued grants, online Host validation and pytest-only purpose. These requirements are not evidenced as wired into the inspected entrypoint/handler path. |

## 3. Test/source inconsistency

The inspected `tests/test_core_http_main.py`:
1. imports `build_app()`;
2. clears the three execution-authority environment variables;
3. posts to `/works/W28/execution-grants`;
4. expects HTTP 503 with `execution_authority_not_configured`.

However, the inspected `core_http_main.py` returns `create_http_app(service)`, and the inspected `http_server.py` contains no matching execution-grant route. On the inspected source alone, the expected route response appears inconsistent; a 404 is plausible.

This is a source-level discrepancy only. Pytest was NOT RUN. Do not report the test as failed or passed until executed against the exact same source snapshot and environment.

## 4. Security disposition for Work 33

- Registry membership is not authentication.
- Message identity/header is not authentication.
- Legacy Governance is not a demonstrated HTTP authorization boundary.
- Canonical WorkBinding is useful for resolving Work scope but is not caller authority.
- A caller-controlled `authorized=true` field must never authorize Cloud Drive access.
- Cloud Drive must fail closed until a verified Core-issued principal and Work-scoped authorization contract is implemented and independently tested.
- Do not reuse the documented execution-grant routes as if they were live endpoints until route mounting and runtime behavior are proven.

## 5. Decisions

1. Preserve current Cloud Drive `UnconfiguredAuthorizer` fail-closed behavior.
2. Do not implement a Core adapter against guessed routes, claims, token formats, or key URLs.
3. Keep Work binding resolution separate from principal authentication and action authorization.
4. Require explicit negative tests: missing/invalid/revoked credential, wrong Work, wrong space/object, cross-tenant access, expiry, replay, Core timeout, and identity spoofing.
5. Reconcile the route/test discrepancy before relying on the execution-authority test as evidence.

## 6. Verification boundary

- GitHub source fetch: completed for the paths listed above.
- Runtime Core :8000: NOT VERIFIED.
- Execution Host :8031 reachability: NOT VERIFIED.
- Pytest: NOT RUN.
- Sandbox synchronization: BLOCKED during this turn because ROOM-HOP Sandbox MCP returned UNAVAILABLE / connection failed.
- No PASS is claimed.
- No source or runtime code was modified.

## 7. Next actions

1. Restore Sandbox MCP connectivity and copy this evidence into the canonical Work 33 Sandbox evidence location; append a corresponding entry to the official Work 33 execution journal.
2. Inspect the full current execution-authority implementation and test fixtures, including the exact code path that the test expects.
3. Run source-matched unit tests in an authorized isolated environment; retain command, commit SHA, output, timestamp, and result.
4. Verify actual Core runtime routes and deployment build only through an authorized read-only diagnostic path.
5. Only after the above, design the concrete Core-backed Cloud Drive Authorizer adapter.
