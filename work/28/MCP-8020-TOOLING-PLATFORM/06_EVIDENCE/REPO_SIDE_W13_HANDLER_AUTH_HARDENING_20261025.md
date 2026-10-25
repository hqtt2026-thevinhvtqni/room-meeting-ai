# Repository-Side Evidence — W13 /execute Handler Caller Authentication Hardening

* Date: 2026-10-25
* Branch: work/28-mcp-tooling-platform
* Fix commit: 1f0e6916bf317b0e5bebed819f100ec08ac35945
* Follow-up commit: 5d52cf2e6b4e4e5d758327c5925ea7c5345a1822
* Bootstrap wiring commit: dc91ffc71bc5985ac1056c78182708f87a039ba2
* Bootstrap syntax fix commit: 769b13fed8b070d8cacf987cb8729eab5c8df998
* Provenance: repository source audit only. This file records what was read
  and changed on this branch; no Sandbox state was accessed or claimed.

## 1. Finding (source audit on this branch)

`execution_host/server.py` before the fix:

* POST /execute accepted any request with a JSON body. There was no caller
  authentication at the handler.
* The `authorized` flag inside the client-supplied `work_context` was passed
  through and used as the authorization decision. A caller could set it to true.
* This confirms the audit gap reported on 2026-10-25: the W13 /execute
  boundary did not prove a trusted execution path.

## 2. Change applied (fail-closed)

* New `authenticate_caller(provided, auth_token)` in `execution_host/server.py`:
  constant-time comparison via `hmac.compare_digest`; an unarmed server
  (no token configured) never authenticates; non-string inputs fail closed.
* POST /execute now requires header `X-Room-Hop-Execution-Auth` to match the
  deployment-issued token, otherwise 401 BLOCKED `caller_authentication_failed`
  before the host is invoked.
* The client-supplied `authorized` flag is no longer trusted; authorization is
  bound to the authenticated caller by the handler.
* `serve(host, port, auth_token=None)` exposes the trusted token injection point.
* Regression tests: `05_TEST/test_w13_execute_handler_auth.py` locks the gate
  (exact-token pass, wrong/missing token denied, unarmed fail-closed,
  non-string fail-closed, pinned header name, serve signature).

Compatibility check: no existing test in this repository POSTs to the live
HTTP handler (root tests exercise `ExecutionHost` directly or use a fake
transport), so the fail-closed default breaks no regression test.

## 3. Explicitly NOT claimed

* This is not a claim that E2E connectivity is proven, that MCP :8020 is
  available, or that Work 28 may be released. Work 28 remains
  ACTIVE / BLOCKED / NOT RELEASED.
* The two Sandbox evidence files reported on 2026-10-25 —
  `XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md` and
  `XU_EXECUTION_TOOL_CONTINUATION_JOURNAL_20261025.md` — are NOT present on
  this branch at audit time. Their content is Sandbox-owned and is not
  reconstructed or fabricated here. Sync of those files from the Sandbox to
  this branch remains an open action item.
* The token itself must be issued by the trusted deployment configuration
  (Core :8000 authority chain). No token value is stored in this repository.

## 4. Next gates (unchanged)

1. Sandbox evidence sync to this branch.
2. Live MCP 8020/8030 connectivity re-verification.
3. E2E: MCP -> Core -> approved runtime -> evidence, under the new auth gate.

## 5. Addendum (2026-10-25, second pass after independent review)

The independent review correctly separated three evidence levels: CI green,
source fix, real deployment verification. Two review findings were accepted
and addressed in commit 5d52cf2:

1. The first regression pass only exercised unit-level seams; it did not
   prove that a real HTTP request with a missing/wrong token receives 401
   and that the host is never invoked. Fixed: `05_TEST/test_w13_execute_handler_http_boundary.py`
   now POSTs real HTTP requests into a ThreadingHTTPServer with a recording
   fake host and asserts, per case, both the status code and that
   `host.calls` is empty for 401/403 paths. The earlier wording that the
   first test 'locked the gate' overstated its scope; the live HTTP test
   closes that gap at the handler level.
2. A valid token must not grant execution of every Work. Fixed:
   `authorize_work(work_id, authorized_works)` now enforces a fail-closed
   per-Work allow-list injected from the trusted deployment configuration;
   handler returns 403 `caller_not_authorized_for_work` before invoking the
   host when the Work is not allow-listed or the allow-list is not configured.
   `serve(..., authorized_works=...)` is the trusted injection point.

## 6. Addendum (2026-10-25, third pass: startup configuration wiring)

Review finding accepted: setting environment variables alone did not prove
the service loaded them, because the `__main__` entrypoint still called
`serve()` with no arguments. Addressed in commit dc91ffc:

* `load_execution_auth_config()` reads `ROOM_HOP_EXECUTION_AUTH_TOKEN` and
  `ROOM_HOP_AUTHORIZED_WORKS` from the environment and validates them at
  startup: missing, blank, or malformed configuration raises loudly, so an
  unconfigured service can never start silently in a half-armed state.
* Work id format is pinned to canonical `W<number>` (e.g. W28); `28` is
  deliberately rejected with an explicit error message.
* `main()` is the new entrypoint; the `__main__` block calls `main()`, which
  passes the loaded configuration into `serve()` as explicit arguments.
* Token confidentiality: the token value never appears in error messages,
  startup output, or evidence; startup announces only the armed Work ids
  and the bind address. Locked by test:
  `05_TEST/test_w13_execution_auth_config_bootstrap.py` covers config
  loading, fail-loud behavior, the pinned Work id format, token non-leakage
  into errors/output, and that `main()` forwards the configuration to
  `serve()` (with `serve` monkeypatched, so no server is started in CI).

## 7. Incident record (2026-10-25): CI red on dc91ffc, fixed in 769b13f

* Commit dc91ffc introduced an unterminated string literal in
  `load_execution_auth_config` (missing closing quote on the
  ' (comma-separated, e.g. W28) line), causing an import-time SyntaxError.
* CI runs #128 and #129 (both against dc91ffc / 9b6e082) FAILED: the test
  step exited with code 1 in ~2s, consistent with a collection-time import
  error, not test assertions.
* Commit 769b13f closes the string literal. Note: because the workflow is
  filtered to `work/28/**` path changes, a server.py-only commit does not
  trigger CI by itself; this evidence update triggers the run that must
  confirm the fix. The passing CI run referenced by this entry is the run
  triggered by this commit (recorded below once green).
* Lesson: `execution_host/**` is outside the workflow path filter; handler
  changes need an accompanying `work/28/**` change (or workflow_dispatch)
  to be CI-verified.

Still NOT claimed: verification that a deployed service process actually
loaded the configuration. That requires booting the service in the trusted
environment (e.g. checking the armed-works startup line and a live 401/403
probe), which remains a deployment-level gate. Work 28 remains
ACTIVE / BLOCKED / NOT RELEASED.


## 8. Incident record (2026-10-25): wrapped-line corruption in 769b13f, rebuilt in c46655a

* Commit 769b13f closed the missing quote from section 7 but was built by
  re-fetching the file through a web fetch layer that hard-wraps long lines
  near column 70. The wrapped text was committed as-is, breaking three long
  lines (e.g. the `self._send(200, ...)` line split into `self._s` /
  `end(200, ...)`), producing a SyntaxError at line 98.
* CI runs #128-#133 all failed on this import-time error; the public
  annotation steps added to the workflow surfaced the failing line, which
  located the root cause.
* Commit c46655aa rebuilds server.py from the clean original source (not from
  any fetched copy) and verifies, before pushing, that no continuation
  fragments exist and the fixed string literal has balanced quotes.
* Lesson recorded for future pushes: never rebuild a file by round-tripping
  content through a fetching layer that may reformat it; always assemble from
  the original source and assert structural invariants before committing.
* The workflow now also publishes failure details as public annotations and
  a job summary so future incidents are diagnosable without log access.

Still NOT claimed: deployment-level verification (service boot, token loaded
from protected configuration, live 401/403 probe). Work 28 remains
ACTIVE / BLOCKED / NOT RELEASED.


## 9. Confirmation (2026-10-25): CI green after clean rebuild

* CI run for commit b1b9f71 (work/28 path change triggering the workflow,
  with the clean server.py from c46655a on the branch): the unit and
  regression suite PASSED in ~7s. All W13 boundary tests now run: unit auth
  gates, live HTTP 401/403 boundary with recording host, and the startup
  configuration bootstrap tests (config loading, fail-loud behavior, pinned
  W<number> work id format, token non-leakage, main() -> serve() wiring).
* The wrapped-line corruption is fully remediated at commit c46655a.
* Evidence levels reached so far: source fix + CI green + handler-level live
  HTTP verification. Deployment-level verification and E2E remain open;
  Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.

## 10. Addendum (2026-10-25, fourth pass: bridge token fix + staged Core client seam)

### 10.1 WEE bridge authentication gap (found and fixed in b132df29)

Source audit after the handler hardening found that
`execution_host/wee_bridge.py` still POSTed to /execute WITHOUT the
`X-Room-Hop-Execution-Auth` header, so every bridge caller would have
received 401 from the hardened server — the hardening silently broke the
legitimate bridge path. Two defects fixed in commit b132df29:

* The bridge now accepts `auth_token` (explicit argument, defaulting to the
  `ROOM_HOP_EXECUTION_AUTH_TOKEN` environment variable) and sends it via the
  pinned `AUTH_HEADER` imported from `execution_host.server`. The token
  value is never logged, echoed, or returned in any blocker.
* `error.HTTPError` is now mapped to the exact blocker
  `execution_host_http_<code>` BEFORE the URLError clause, so 401/403 from
  the boundary are distinguishable from genuine unreachability. Previously
  every HTTP failure surfaced as `execution_host_unreachable`, hiding the
  real status.
* Locked by `05_TEST/test_w13_bridge_execution_token.py` (6 tests: pinned
  header, no-header-without-token, env default, exact 401/403 codes, token
  non-leakage).
* CI for b132df29: the unit-regression-tests job SUCCEEDED in ~7s (full
  suite, verified via the public checks page on 2026-10-25). Root bridge
  tests (`tests/test_wee_8031_bridge.py`) use a FakeTransport with the same
  `(url, body, timeout)` signature and remained green.

### 10.2 Staged CoreExecutionClient seam (commit 4da5752)

The architecture blocker traced by the Sandbox reviewer — the v54 execution
gateway is UNWIRED (only `BlockedExecutionClient`) — is now answered by a
staged seam, NOT a wiring:

* `04_CODE/mcp8020_w13_core_client_v1.py` implements
  `W13CoreExecutionClientV1`: the seven-method CoreExecutionClient protocol
  expected by `ExecutionGateway`, over the token-carrying
  `ExecutionHostBridge`. Fail-closed properties: construction validates
  the injected `bridge` / `work_context_provider` / `request_builder`
  callables; `submit` requires a non-empty work_id and refuses results
  without an execution_id (surfacing the exact blocker); unknown run_ids
  answer BLOCKED; unknown host statuses map to BLOCKED; `cancel` is refused
  (`cancel_not_supported_synchronous_boundary`) until a verified
  process-tree cancellation path exists; artifacts must appear in the run
  manifest; evidence generation requires a bound evidence_ref; handoff status
  is restricted to PASS/FAIL/BLOCKED/TIMEOUT with non-empty refs.
* `05_TEST/test_mcp8020_w13_core_client_v1.py` (15 tests) locks all of the
  above against a recording fake bridge, and proves the client satisfies
  `ExecutionGateway` construction (the gateway accepts it as a
  CoreExecutionClient).
* This module is deliberately NOT imported by any MCP registration, catalog,
  or v54 service code. The v54 execution tools remain NOT_IMPLEMENTED.
  Wiring it requires deployment evidence: armed startup line, live 401/403
  probe against the deployed service, and one E2E Core :8000 -> W13 run with
  bound evidence, per the Work 28 gate rules.

### 10.3 Evidence levels (explicit, unchanged discipline)

* Reached: source fix + CI green (b132df29) + handler/bridge-level live
  boundary tests + staged seam with unit coverage.
* NOT reached: deployment-level verification (service boot actually loading
  token/allow-list, live probe) and E2E through Core :8000.
* CI for 4da5752: unit-regression-tests SUCCEEDED in ~9s (verified via the
  public checks page on 2026-10-25; no test-failure annotations).
* Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.
