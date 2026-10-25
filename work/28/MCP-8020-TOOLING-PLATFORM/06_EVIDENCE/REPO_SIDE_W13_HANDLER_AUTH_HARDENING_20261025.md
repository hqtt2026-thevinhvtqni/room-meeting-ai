# Repository-Side Evidence — W13 /execute Handler Caller Authentication Hardening

* Date: 2026-10-25
* Branch: work/28-mcp-tooling-platform
* Fix commit: 1f0e6916bf317b0e5bebed819f100ec08ac35945
* Follow-up commit: 5d52cf2e6b4e4e5d758327c5925ea7c5345a1822
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
  (no configured token) never authenticates; non-string inputs fail closed.
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

Still NOT claimed after this addendum: token issuance from protected
deployment configuration, absence of token leakage, or verification of the
actually deployed service. These remain open gates. Work 28 remains
ACTIVE / BLOCKED / NOT RELEASED.
