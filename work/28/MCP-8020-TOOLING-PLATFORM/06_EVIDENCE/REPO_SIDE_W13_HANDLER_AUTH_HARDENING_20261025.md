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


## 11. Independent architecture trace (2026-10-25): staged seam is not a Core adapter yet

Audit scope: current branch source at `c04c2e0041d587128f331c0e4e17ac0487a62772`, including the v54 service, v54 gateway, staged client, WEE bridge, and W13 handler. This is static source inspection; no live deployment or Sandbox process execution was performed.

### 11.1 Confirmed fixes and boundaries

* `execution_host/wee_bridge.py` now conditionally sends `X-Room-Hop-Execution-Auth` when a trusted token is supplied or loaded from `ROOM_HOP_EXECUTION_AUTH_TOKEN`; its `HTTPError` handler preserves 401/403 as `execution_host_http_<code>`. This is source-level confirmation, backed by bridge tests and the reported green CI run.
* `mcp8020_w13_core_client_v1.py` exists and structurally satisfies the seven-method Protocol. Its tests use a recording fake bridge; they do not call a deployed W13 service or Core.
* `mcp8020_service_v54.py` only binds an execution gateway when explicitly injected. Its public catalog status remains the controlling gate; this client is not imported or composed by the service.

### 11.2 Additional semantic gap: the staged client does not implement seven authoritative Core operations

The current adapter passes a protocol-shape test, but several methods are local projections rather than authoritative execution/evidence operations:

* `get_status` and `get_result` read the in-memory submission record; they do not query Core or W13 for an authoritative current status/result. The process-local registry also cannot survive service restart or coordinate multiple MCP workers.
* `generate_evidence` returns a newly assembled dictionary around an existing `evidence_ref`; it does not call an evidence service, persist an evidence record, or independently verify the referenced evidence.
* `create_handoff` validates and returns a dictionary; it does not persist a handoff in Core/Work state or verify that each evidence reference belongs to the specified Work/run.
* `submit` delegates WorkContext derivation and request construction to injected callables, but this repository does not show a concrete trusted Core :8000 provider/composition supplying them. The bridge itself posts directly to the W13 `/execute` endpoint; it is not proof of the required MCP -> Core -> canonical W12/W13 path.

Therefore “implements all seven methods” is accurate only at the Python interface/signature level, not at the semantic/authority level required for release. The fake-bridge tests establish fail-closed local behavior, not production correctness.

### 11.3 Required next implementation slice

1. Identify the already-deployed authenticated Core :8000 execution API and its exact contract, deployed SHA, caller identity and WorkContext derivation. Do not invent a route or let request arguments supply authority.
2. Implement the adapter against that Core API, including server-side Work-scoped run authorization and durable status/result lookup. Keep direct MCP -> standalone W13 host calls prohibited unless the architecture owner explicitly revises the approved contract.
3. Route evidence generation and handoff creation through the authoritative evidence/Work service, with ownership checks and durable references; do not treat locally assembled dictionaries as persisted evidence.
4. Add integration tests using a real Core test instance or contract-faithful test server, including 401, 403, unknown/cross-Work run IDs, restart/multi-worker behavior, evidence-ref mismatch, and downstream timeout/cleanup cases.
5. Only then evaluate gateway composition and catalog status changes. Release gate still requires deployment startup proof, live auth probes, canonical runtime/isolation evidence, and an E2E run whose evidence binds Work, source hash, run ID, exit status and output refs.

**Decision:** do not wire `W13CoreExecutionClientV1` into the live v54 service yet. The remaining blocker is not merely deployment evidence; the adapter's status/result/evidence/handoff methods currently lack authoritative Core backing. Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.


## 12. Cross-Work canonical Work 13 Sandbox comparison (2026-10-25)

Read-only cross-Work probes via MCP 8030 inspected the current Work 13 Sandbox files:
- `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/server.py`
- `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/models.py`
- `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/wee_bridge.py`
- `13/EXECUTION-HOST-INFRASTRUCTURE/06_EVIDENCE/W13-CANONICAL-RUNTIME-IDENTITY/W13_CANONICAL_RUNTIME_IDENTITY_FINAL_RESULT.json`

Findings:

1. **The Work 13 Sandbox's canonical `server.py` is not the hardened branch version.** The readable Sandbox copy's `do_POST /execute` accepts the JSON body, constructs `WorkContext` and `ExecutionRequest`, and invokes the host without the token-authentication or per-Work allow-list checks present in the Work 28 branch copy. This is a source comparison, not a live request.
2. **The Work 13 Sandbox's `wee_bridge.py` is also the pre-token version.** Its constructor has no `auth_token` parameter, does not load `ROOM_HOP_EXECUTION_AUTH_TOKEN`, and sends only Content-Type/Accept headers. Therefore the b132df29 bridge fix and hardened server in the Work 28 repository branch have NOT been shown to be synchronized into the canonical Work 13 Sandbox or deployed runtime.
3. The Work 13 Sandbox's recorded canonical runtime identity result says `BLOCKED`: canonical startup, `/health`, `/execute`, runtime identity and build hash were NOT OBSERVED; the record says the available Room-HOP tool inventory lacks process-start/attach-runtime capability.
4. A historical `EXECUTION-CURRENT.json` labels a narrower HTTP-host E2E as PASS, but that does not establish that the current source revision is running, that the new token/allow-list hardening is deployed, or that the required Work 28 → authenticated Core → canonical W13/W12 route passes today.

**Consequence:** do not interpret CI-green repository changes as hardening the canonical Work 13 Sandbox/runtime. The outstanding work is a controlled cross-Work source synchronization/review followed by an authorized deployment and live verification in the trusted environment. No secret token is to be copied into source or evidence, and no deployment or runtime activation was attempted in this audit.

This adds a separate, concrete gate to sections 10–11: **canonical Work 13 source/runtime alignment is unverified and the Sandbox source currently read is pre-hardening.** Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.

## 13. Repo-side audit (2026-10-25): Core :8000 has no execution authority; proposed contract

Follow-up to section 11.3 step 1 ("identify the already-deployed authenticated
Core :8000 execution API"). The repository-side answer is: **no such API
exists in code today.**

* `room_hop_mcp/adapter/http_server.py` and `core/meeting_service.py` were
  read directly on this branch. Core :8000 is a meeting lifecycle service
  only (`API_CONTRACT.md`, LOCKED v0.1). Its full HTTP surface is
  `GET /identities`, `GET /meetings`, `GET /meetings/{id}`,
  `GET /meetings/{id}/transcript`, `POST /meetings`,
  `POST /meetings/{id}/paste|open|join|start|close`. The strings
  `execute`, `work_id`, `WorkContext` do not appear in the Core package.
* The canonical Work 13 source tree (`13/EXECUTION-HOST-INFRASTRUCTURE/`)
  does NOT exist in this repository — confirmed by direct path lookup. The
  canonical Work 13 source lives only in the Sandbox (section 12). Its
  synchronization/review is therefore Sandbox-owned and cannot be performed
  or verified from this branch.
* Consequence: the MCP -> Core :8000 -> W13 route cannot be wired yet,
  because the Core half of the route does not exist. Per the discipline
  "do not invent an endpoint", the response was to PROPOSE a contract for
  architecture-owner review, not to implement one:
  `03_ARCHITECTURE/PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md`
  (commit 241bdba) defines a Work-scoped, time-bounded execution grant
  surface (POST /works/{work_id}/execution-grants, grant status lookup,
  record-only run outcomes), authority invariants, the integration seam
  with `W13CoreExecutionClientV1.work_context_provider`, and open questions
  (token model, durability, composer, separation from the LOCKED v0.1
  meeting contract).
* Nothing was implemented, wired, or claimed: the v54 execution tools
  remain NOT_IMPLEMENTED. The staged client (section 11.2) keeps its
  acknowledged semantic limits until the contract is approved, implemented,
  and verified live.
* Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.

## 14. Independent review verdict and contract V1.1 (2026-10-25)

The independent reviewer evaluated the round that produced sections 13 and
the V1 contract and returned a bounded verdict:

* Step 1 (Work 13 source alignment): PASS, repo-side scope only. The
  canonical Work 13/12 trees are not on the branch; their source lives in
  the Sandbox and no claim of synchronization or deployment verification
  may be made from this repository.
* Step 2 (Core :8000 route search): PASS, static inspection. Core source
  shows meeting-lifecycle and identity APIs only; no WorkContext execution
  grant contract exists in the audited scope.
* CI green on commits 241bdba and 6038072 is CI-quality evidence only: it
  does not prove Core can grant execution authority, nor that a production
  execution path works.

The reviewer proposed five architectural principles (Core decides and MCP
never self-authorizes; grants bound to Work/caller/purpose/expiry/checkable
status; durable authoritative storage for runs/evidence/handoffs rather
than an in-process registry; W13/W12 remains the only canonical runtime
with no MCP-to-Execution-Host bypass; fail-closed on every error branch)
and a five-step sequence (approve contract, implement Core side, verify W13
in the Sandbox at runtime, security + E2E testing, only then wire the
gateway/catalog).

Response on this branch (commit 1936ad3): the proposed contract was revised
to V1.1 — DESIGN ONLY, NOT APPROVED, NOT IMPLEMENTED, NOT WIRED. The five
principles are recorded as normative invariants INV-1..INV-5 (pending
approval), and the four open questions were converted into decision
requests DR-1..DR-4, each with a recommended default from the repo-side
agent (service identity first; separate short-lived grant token;
Core-managed append-only store; separate app mount) and an explicit note
that recommendations are proposals for the architecture owner. Section 6
of the contract restates the reviewer's five gates in order, none
skippable.

Nothing was implemented, wired, or claimed: the v54 execution tools remain
NOT_IMPLEMENTED. No CI pass is interpreted as a production pass. Work 28
remains ACTIVE / BLOCKED / NOT RELEASED.

## 15. Xu review of the decision requests; contract V1.2 (2026-10-25)

The architecture reviewer (Xu) reviewed DR-1..DR-4 as presented in V1.1 and
returned a conditional endorsement, recorded here verbatim in substance:

* DR-2 (grant token): agreed in principle — short-lived separate token,
  with the added condition that rights, Work, action scope, and expiry are
  validated server-side, and the token value never appears in logs or
  evidence.
* DR-3 (durable store): agreed that Core manages append-only records, with
  the added condition that durability, restart recovery, and run/result/
  evidence/handoff linkage must be PROVEN; the existence of the
  `meeting_log` pattern is precedent, not proof.
* DR-4 (deployment separation): agreed on separation from the LOCKED v0.1
  meeting API, with the added condition that the new component remains
  inside the Core authority boundary — not a second Core and not an
  independent execution route.
* DR-1 (caller identity): REVISED DIRECTION REQUIRED. Service identity is
  agreed, but it must be an identity that Core itself enrolls and
  authorizes — not hardcoded to port 8020 or 8030 — so that port
  migrations or adapter replacements never require redesigning the
  authority mechanism.

Gate status recorded per the reviewer: Gate 1 (decision lock) IN REVIEW;
Gate 2 (Core implementation) BLOCKED; Gates 3-4 (runtime verification,
security/E2E) BLOCKED; Gate 5 (gateway/catalog wiring) NOT OPENED. No PC or
Sandbox action is required from the owner at this stage; the pending item
is the architecture decision itself.

Response on this branch (commit 98808c5): the contract was revised to V1.2 —
still DESIGN ONLY, NOT APPROVED, NOT IMPLEMENTED, NOT WIRED. DR-1 now
specifies a Core-enrolled, port-agnostic service identity registry with
per-deployment credential injection; DR-2/DR-3/DR-4 carry the reviewer's
conditions as explicit, testable proof obligations (server-side validation
and token non-leak; restart persistence, append-only history, and
verifiable linkage; additive mount inside the Core authority boundary).
Final approval remains with Vinh and has NOT been given. The v54 execution
tools remain NOT_IMPLEMENTED. Work 28 remains ACTIVE / BLOCKED /
NOT RELEASED.

## 16. Gate 2 opened: Core execution authority implemented (2026-10-25)

The owner (Vinh) opened Gate 2 ("Ok Gate 2 mở"). The Core-side implementation
per the approved contract V1.2 was committed as de0667b:

* Package `core/execution_authority/` — inside the Core package boundary per
  DR-4 (code ownership and governance under Core), with a SEPARATE HTTP mount
  (`http_server.py`, its own process/port via EXECUTION_AUTHORITY_PORT) so
  fail-closed startup/shutdown can never regress the LOCKED v0.1 meeting API.
* DR-1: `load_enrolled_identities` parses deployment-injected
  `EXECUTION_AUTHORITY_ENROLLED_IDENTITIES` (name=credential); enrollment is
  by identity name, not port or process. Per-Work rights come from the works
  registry (`EXECUTION_AUTHORITY_WORKS_FILE`: work fields plus
  `allowed_identities`). Port migration or adapter replacement requires no
  authority redesign.
* DR-2: grants carry a separate short-lived token
  (`secrets.token_urlsafe`); records store ONLY its SHA-256; the token value
  is returned exactly once to the caller;
  `validate_grant_token` performs the server-side check (active grant AND
  constant-time token hash match) and every run recording goes through it;
  the HTTP handler never logs headers and never echoes secrets.
* DR-3 proof obligations, as tests:
  `05_TEST/test_core_execution_authority_v1.py` (26 tests) proves
  restart recovery (a fresh store/authority over the same directory reloads
  grants and runs), append-only (duplicate record ids refused; the public
  store surface exposes append/get/records only — no mutation or deletion
  path), durability (append flushes and fsyncs), and full run linkage
  (grant id, work, identity, source hash, exit status, output refs,
  evidence refs — required non-empty — and handoff ids).
* DR-4 boundary tests over a live ThreadingHTTPServer on an ephemeral port:
  401 missing/wrong identity, 403 enrolled-but-not-allowed-for-Work,
  404 unknown work/route, 409 duplicate active grant, grant status
  round-trip without token exposure, run recording with forged-token
  rejection, and credential/token non-leakage into errors and records.
* Fail-closed configuration: `main()` raises loudly on missing/malformed
  identity, works registry, or data dir; work ids pinned to W<number>.

Scope discipline (unchanged): this is the CORE side only. It does NOT wire
`W13CoreExecutionClientV1`, does NOT touch the v54 catalog (the seven
execution tools remain NOT_IMPLEMENTED), and does NOT claim any deployment
or Sandbox state. Gates 3-4 (runtime verification in the Sandbox, live
probes, E2E) remain BLOCKED; Gate 5 (gateway/catalog wiring) remains NOT
OPENED. CI result for de0667b: FAILED (see incident 16.1 below).

### 16.1 Incident record (2026-10-25): CI red on de0667b / 9a8124d, fixed in 337d64f

* CI run #166 (commit de0667b) and run #167 (commit 9a8124d, docs-only over
  the same tree) FAILED in ~13-15s. The public checks page showed
  "1 error, 2 warnings, 1 notice" with no test-level annotation: the
  annotation step only surfaces collection-time ImportError lines, not
  assertion/KeyError failures, so the failing tests were located by direct
  source audit of the test module against the authority implementation.
* Root cause: `ExecutionAuthority.issue_grant` returned the grant keyed as
  `record_id` only; the issued-grant response carried no `grant_id` field.
  Every test reading `grant["grant_id"]` — 8 direct authority tests and 3
  HTTP boundary tests — raised KeyError at the client, so 11 of the 26 new
  tests failed; the run still took >10s because the remainder of the suite,
  including the other 15 new tests, executed to completion.
* Fix commit 337d64f: the stored grant record now carries an explicit
  `grant_id` field (same canonical value as `record_id`), so the once-only
  token response, the grant status endpoint, and the run linkage all expose
  the stable `grant_id` that the contract API surface promises. No other
  behavior changed; the store remains append-only (a new field on new
  records, not a mutation path for history).
* Because `core/**` is outside the workflow path filter, commit 337d64f
  does not trigger CI by itself; this evidence update (work/28 path change)
  triggers the run that must confirm the fix.

### 16.2 Confirmation (2026-10-25): CI green for the fixed tree

* CI run #168 (commit 36c89fe, the branch carrying fix 337d64f plus this
  evidence file): the unit-regression-tests job completed successfully in
  ~13s (full suite — duration consistent with the full test set, not a
  collection error). Verified via the public actions list on 2026-10-25.
* All 26 authority/HTTP-boundary tests for the Core execution authority now
  pass, including the 11 that previously raised KeyError on the missing
  `grant_id` field.
* Evidence levels reached: Core-side implementation per contract V1.2 +
  CI green. Still NOT claimed: deployment of the authority service (env
  configuration, boot, armed startup line), live 401/403 probes against a
  real process, Sandbox W13 runtime verification, and E2E
  MCP -> Core -> W13/W12. Gates 3-4 remain BLOCKED; Gate 5 remains NOT
  OPENED.
* Lesson: contract-facing identifiers must appear in contract-facing
  fields (`grant_id`), not only as internal record bookkeeping
  (`record_id`); and the public annotation channel covers import errors
  only, so assertion failures must be diagnosed from the run summary or by
  source audit.

Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.


## 17. Cross-identity grant access hardening

**Finding (source audit):** the first Gate 2 implementation authenticated an enrolled service identity and validated the bearer grant token, but the HTTP run-recording route did not require the authenticated identity to match the identity bound to the grant. The grant-status GET route also returned grant metadata to any enrolled identity that knew the grant ID. This violated the caller-identity binding invariant.

**Fix:**
- Commit `df7463fa45e8f6c212234b254a06fe295e72b93a`: bind grant-status reads to the issuing service identity (otherwise return non-disclosing `404 unknown_grant`); bind run recording to the grant's service identity (otherwise return `403 caller_not_authorized_for_grant`).
- Commit `136a346ec6326b621f1b31efe3d4537218270bfd`: add regression tests for cross-identity grant-status reads and run recording.

**Verification:** GitHub Actions run #170 completed `success` for test commit `136a346ec6326b621f1b31efe3d4537218270bfd`: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40200480561

**Scope limit:** this is repository/CI evidence only. It does not prove the authority process is deployed or armed, that the live W13/W12 runtime is verified, or that MCP → Core → W13/W12 E2E is operational. Gate 3–4 remain BLOCKED; Gate 5 remains CLOSED.

## 18. Gate 3 preparation: live boot probe as a real process (2026-10-25)

Commit 7cf14f1 adds `05_TEST/test_core_execution_authority_boot_v1.py`,
which boots `core.execution_authority.http_server` as a REAL subprocess
(`python -m core.execution_authority.http_server`, fail-loud env:
identities, works registry, data dir, port), waits for the process to arm
(the port answers on TCP, within a 15s deadline), and then probes the LIVE
boundary over a real socket:

* 401 with missing and with wrong service-identity credential;
* 403 for an enrolled-but-unauthorized identity (`caller_not_authorized_for_work`);
* 404 unknown work; 200 grant issue (token + `grant_id` present);
* 409 duplicate active grant; 403 forged grant token; 200 valid run
  recording with run linkage to W13;
* fail-closed boot: a second process started WITHOUT the env configuration
  exits non-zero with the loud config error;
* non-leakage: the process output contains the armed startup line but never
  any credential value.

**Verification:** CI run #172 (commit 7cf14f1, on the tree that includes
the cross-identity binding fix df7463f): completed successfully in ~15s
(full suite), verified via the public actions list on 2026-10-25.

**Evidence level — CI-runtime, NOT Sandbox deployment.** This proves the
authority service arms from real process boot under real environment
configuration and answers live probes on a real socket inside the CI
runner. It does NOT prove: deployment in the trusted Sandbox/Core host,
the armed startup line of a production process, the canonical W13/W12
runtime, or E2E MCP -> Core -> W13/W12.

**Channel constraint, recorded:** the repo-side session that produced this
section has NO connector capable of reaching the MCP 8030 / Sandbox
runtime (available surfaces are repository read/push and CI only). Sandbox
runtime verification therefore cannot be performed or claimed from this
session. Gate 3 (W13/W12 runtime verification) and Gate 4 (security + E2E)
remain BLOCKED; Gate 5 remains NOT OPENED. The v54 execution tools remain
NOT_IMPLEMENTED.

Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.

## 19. Gate 4 prep: E2E client seam over a live authority process (2026-10-25)

Commit d4e6f3f adds `05_TEST/test_w13_client_live_authority_e2e_v1.py`:
the STAGED, UNWIRED `W13CoreExecutionClientV1` (no v54 registration —
unchanged) is driven end-to-end through a real HTTP bridge against a REAL
`core.execution_authority.http_server` subprocess booted in-test with
fail-loud env (enrolled identities, works registry W12+W13, data dir, port).

Proven at CI-runtime level:

* submit: the client obtains a real grant from the live authority and
  records a run; the append-only JSONL store ON DISK shows exactly one
  grant and one run record, with the run linked to the grant id, work W13,
  source hash, and evidence refs; the grant token VALUE and the credential
  appear nowhere in the store (only token SHA-256).
* the full seven-method client surface over the live boundary:
  get_status, get_result, collect_artifact, generate_evidence,
  create_handoff (W12 PASS handoff with evidence refs), cancel refused
  (BLOCKED), unknown run id BLOCKED.
* fail-closed path: a bridge with a WRONG credential gets 401 from the
  live authority, the client surfaces BLOCKED, and the store stays EMPTY
  (no partial grant or run records).
* live security probes: malformed JSON body -> 400; unknown route -> 404;
  GET grant status without the service-identity header -> 401.

**Verification:** CI run #174 (commit d4e6f3f): completed successfully in
~18s (longer runs consistent with three real process boots in the suite),
verified via the public actions list on 2026-10-25.

**Evidence level — repo-side CI E2E, NOT the full Gate 4.** This proves
the client seam -> Core authority HTTP boundary works end-to-end as code
against a real process. It does NOT prove: v54 gateway registration, the
real W13 execution host executing payloads, deployment on the trusted
Sandbox/Core host, or a production E2E run with bound production evidence.
Gate 3 (trusted runtime verification) and Gate 4 (deployment-grade
security + production E2E) remain BLOCKED pending trusted-environment
evidence; Gate 5 (wiring v54 execution tools to IMPLEMENTED) remains NOT
OPENED — flipping it without that evidence would violate the gate rules.

Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.