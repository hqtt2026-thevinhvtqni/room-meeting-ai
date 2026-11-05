# DOC-068 — W32 TEST & SYSTEM-STRUCTURE EVIDENCE CONSOLIDATION

- **Document Number:** DOC-068
- **Priority:** P1 — Required for architecture continuity, test traceability and Xu review
- **Work:** 32 — CI/CD Python CI v2
- **Branch under test:** `work/32-ci-cd-python-ci-v2`
- **Latest confirmed branch SHA:** `c601c18712ed1d58990314d517409478f41ee11b`
- **Prepared by:** Ka — CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05; exact clock time was not present in the captured evidence
- **Audience:** Xu — CEO / Lead Architect; Ka — CSA; project owner — acceptance authority
- **Status:** EVIDENCE CONSOLIDATION; Work 32 remains ACTIVE — NOT RELEASED

## 1. Purpose and recording rule

This record consolidates test and runtime checks discussed and evidenced during Work 32 continuation. It is a traceability record, not a claim that every system layer has passed. Every result is classified by its actual execution environment and exact scope. A passing CI run does not imply that PC runtime, MCP transport, Browser Adapter handoff, transcript persistence, staging or release has passed.

Future Work 32 tests must be recorded with: test ID/name, date-time, environment, branch and exact SHA, command or invocation, expected/actual result, artifact/log reference, status, limitations, and follow-up owner.

## 2. GitHub CI — confirmed results

| Run | Commit / scope | Evidence captured | Result |
|---|---|---|---|
| #34 | F4 Option A implementation; SHA prefix `c7359d4` | 4/4 jobs successful; unit 189, product E2E 45, tooling 20, immutable artifact 1 | PASS for the run and tested scope |
| #36 | GitHub Actions Node 24-compatible pinned actions | 4/4 jobs successful; zero Node20 deprecation warnings reported | PASS for the run and warning scope |
| #39 | Starlette/httpx2 compatibility and dependency constraints; SHA prefix `17d7d87` | 4/4 jobs successful; `pip check` PASS; zero StarletteDeprecationWarning and Node20 warnings reported | PASS for the run and dependency/warning scope |
| #41 | Documentation-only update; exact SHA `c601c18712ed1d58990314d517409478f41ee11b` | GitHub Actions completed SUCCESS, 4/4 jobs | PASS for CI validation of this exact SHA |

Historical full run IDs retained in the project evidence:
- Run #34: `41805684024`
- Run #36: `41806199038`
- Run #39: `41806906885`
- Run #41: `41807578306`

These are CI-run results only. They do not prove PC runtime integration or product release readiness.

## 3. F4 resource-limit implementation and regression scope

F4 Option A was implemented and CI-verified with the following contract:
- 100 accepted paste requests per meeting and resolved identity in a rolling 60-second window.
- SQLite-backed persistent rolling window and `BEGIN IMMEDIATE` concurrency control.
- Reservation rollback when append fails.
- Missing identity uses a shared legacy bucket.
- SQLite is certified only for multiple processes sharing the same local filesystem; this evidence does not certify multi-host distributed operation.
- `identity_id` is resolved through the registry; transport-level independent authentication was not proven by this test record.

F4 result is PASS within these explicit limitations. Do not expand the claim to multi-host rate limiting or authenticated identity without separate tests.

## 4. Browser Adapter — local E2E result (not a Work 32 branch PASS)

Original local repository:
`D:\\ROOM-HOP-CLEAN\\room-meeting-ai`

Observed local Git state at test time:
- Branch: `main`
- HEAD: `d7c90d9d31062d389810808e43dfdd19d7711b75`
- Working tree was dirty and local main was behind origin; it was not the authorized Work 32 branch.

Command:
`python tests/test_browser_agent_adapter_e2e.py`

Observed:
- Browser HTTP execution returned HTTP 200.
- `ok=true`.
- Final URL: `https://en.wikipedia.org/wiki/Headless_browser`.
- Page title: `Headless browser - Wikipedia`.
- Local evidence JSON: `.ai-workspace/release/WORK09/evidence/wikipedia-browser-e2e-1793824482.json`.
- ROOM HOP submission returned `status=deferred`, reason `ROOMHOP_MCP_URL not configured`.
- Test assertion failed at line 56 because it expected submission status `pass`.

Classification:
- Browser navigation/execution: PASS for the local invocation.
- ROOM HOP MCP handoff: DEFERRED.
- Transcript readback/persistence: NOT PROVEN.
- Overall Browser Adapter E2E: FAIL / NOT PASS.
- This run was executed from local `main`, not the Work 32 branch; it must not be counted as Work 32 CI/E2E PASS.

## 5. Safe Work 32 clone verification

A separate clone was created without modifying the dirty original repository:
`D:\\ROOM-HOP-CLEAN\\room-meeting-ai-w32-test`

Observed:
- Branch: `work/32-ci-cd-python-ci-v2`
- Working tree: clean
- HEAD: `c601c18712ed1d58990314d517409478f41ee11b`
- `git ls-remote` for the authorized branch returned the same SHA.

Classification: PASS for exact branch clone and clean-state verification. This does not prove the PC services are running this clone.

## 6. PC runtime observations — endpoint compatibility unresolved

Observed on the PC:
- TCP listener `127.0.0.1:8787`, PID 20468.
- TCP listener `127.0.0.1:8020`, PID 15048.
- `GET http://127.0.0.1:8787/health` returned `ok=True`, service `room-hop-browser-agent-adapter`, `browser_started=True`.
- `GET http://127.0.0.1:8020/openapi.json` returned HTTP 404. This alone does not establish that MCP is down.
- PID 20468 command line: Python + `uvicorn adapter:app --host 127.0.0.1 --port 8787`.
- PID 15048 command line: Python + `-m room_hop_mcp.mcp_http_main`.
- PID 15048 parent PowerShell command set `ROOM_HOP_MCP_PORT=8020` and launched from `D:\\ROOM-HOP-CLEAN\\room-meeting-ai`.

Important source comparison:
- The Work 32 GitHub tree at SHA `c601c18712ed1d58990314d517409478f41ee11b` does not contain `room_hop_mcp/mcp_http_main.py`.
- Work 32 contains `room_hop_mcp/__main__.py` (MCP stdio entrypoint) and the REST adapter files under `room_hop_mcp/adapter/`; the public MCP contract is separately defined in ADR-002.
- Therefore the running PC process cannot yet be attributed to the Work 32 source tree. Its actual imported module origin and the working directory/module origin of PID 20468 still require read-only verification.
- Previous tentative assumption that PID 15048 was only a REST service is corrected: its command line explicitly launches a module named `room_hop_mcp.mcp_http_main`. Its protocol compatibility with the Work 32 Browser Adapter remains unverified.

Classification:
- Adapter health endpoint: PASS.
- TCP listeners: PASS as process/listener observations only.
- MCP transport and tool compatibility: BLOCKED / NOT VERIFIED.
- PC runtime source-to-branch provenance: BLOCKED / NOT VERIFIED.
- No service was restarted, no environment variable was injected into an existing process, and no meeting transcript was mutated during these observations.

## 7. Architecture contract relevant to Xu

Work 32 ADR-002 defines the public MCP V1 inventory as exactly:
1. `list_meetings`
2. `get_meeting`
3. `get_transcript`
4. `add_paste_to_meeting`

Core lifecycle operations `join_meeting` and `start_meeting` remain at the approved Core HTTP boundary; do not add duplicate MCP lifecycle tools merely to make an integration client pass.

The Browser Adapter client must be validated against the actual public MCP transport and these four tools. The test path must prove:
1. Adapter process is loaded from the authorized Work 32 source/revision.
2. MCP endpoint and transport are compatible with the client implementation.
3. `tools/list` exposes the exact approved inventory.
4. Meeting selection and identity are valid.
5. `add_paste_to_meeting` records the intended test payload.
6. `get_transcript` reads back the same execution evidence, including execution/work/evidence identifiers required by the E2E contract.

A successful browser navigation alone is not proof of a successful ROOM HOP workflow. A successful tools/list alone is not proof of transcript persistence. Passing component contracts is not proof of cross-layer semantic contract.

## 8. Required follow-up and owners

| Priority | Action | Owner | Gate |
|---|---|---|---|
| P0 | Inspect actual module origin for PID 15048 and actual adapter module/cwd for PID 20468; read-only only | Ka | Runtime provenance |
| P0 | Compare actual PC transport and tool inventory with ADR-002 and Browser Adapter client | Ka | MCP compatibility |
| P0 | Verify target test meeting and identity before any transcript-mutating E2E | Ka | Safe test target |
| P0 | Run E2E only against a Work 32-controlled runtime and capture transcript readback | Ka | Browser Adapter E2E |
| P1 | Review this evidence consolidation and confirm architectural boundary/continuation decisions | Xu — CEO / Lead Architect | Architecture review |
| P1 | Keep CI run evidence, PC runtime evidence, and Sandbox evidence separately traceable | Ka | Evidence governance |

No restart, process termination, environment change to an existing service, or transcript-mutating E2E is authorized by this record alone.

## 9. Overall status

- GitHub CI on exact Work 32 SHA: PASS (run #41, 4/4).
- F4: PASS within stated SQLite/identity limitations.
- Work 32 clone integrity: PASS.
- Browser Adapter browser execution on dirty local main: PASS for browser-only portion.
- ROOM HOP handoff in that local E2E: DEFERRED; test assertion failed.
- PC adapter health: PASS.
- PC MCP protocol and source provenance: BLOCKED / NOT VERIFIED.
- Browser Adapter end-to-end semantic workflow: NOT PASS.
- Work 32: ACTIVE — NOT RELEASED.

---

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05; exact clock time not captured in source evidence
- **Purpose:** Consolidate all currently evidenced Work 32 test outcomes and architecture dependencies for Xu review.
- **Disposition:** Evidence recorded; no release or architecture boundary changed.

## NHẬT KÝ

- **Name:** Ka
- **Title:** CSA
- **Date-Time:** 2026-11-05; exact clock time not captured in source evidence
- **Action:** Consolidated GitHub CI runs #34/#36/#39/#41, F4 scope, Browser Adapter local E2E failure/deferment, clean Work 32 clone, PC listeners/health and unresolved MCP runtime provenance.
- **Next:** Complete read-only runtime provenance and contract comparison before any restart or transcript-mutating test.


---

## DOC-068 Addendum A — PC MCP process source inspection (2026-11-05)

### Evidence supplied in the user's PowerShell capture

The user inspected the module from the original local repository root and obtained:

`D:\\ROOM-HOP-CLEAN\\room-meeting-ai\\room_hop_mcp\\mcp_http_main.py`

This is the module resolved by:
`importlib.util.find_spec('room_hop_mcp.mcp_http_main')`

The running PID 15048 was launched by parent PowerShell PID 1684, whose command line sets:
`ROOM_HOP_MCP_PORT='8020'`
and starts:
`python -m room_hop_mcp.mcp_http_main`
with working directory `D:\\ROOM-HOP-CLEAN\\room-meeting-ai`.

The inspected source configures:
- FastMCP server name `room-hop-http`
- `streamable_http_path="/mcp"`
- `stateless_http=True`
- `transport="streamable-http"`
- host `127.0.0.1`, port from `ROOM_HOP_MCP_PORT` (default 8020)

Therefore, the process is intended to serve MCP Streamable HTTP at the configured `/mcp` path. A 404 at `/openapi.json` is not a valid MCP protocol test and does not contradict that configured path.

### Tool inventory visible in this source

The source registers, among others:
- Work 32 ADR-002 public-boundary names: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`.
- Additional lifecycle tools: `join_meeting`, `start_meeting`.
- Additional sandbox tools: `sandbox_create_work`, `sandbox_list_works`, `sandbox_list`, `sandbox_read_probe`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`; it also calls `register_sandbox_read(mcp, sandbox)`.
- Additional agent-runtime tools: `get_pending_tasks`, `submit_proposal`.

This is materially broader than Work 32 ADR-002's exact public MCP V1 inventory of four tools. It is not compliant evidence for the Work 32 public MCP contract. The running process must not be treated as the Work 32 MCP runtime merely because some tool names overlap.

### Classification and impact

- PID 15048 source origin: CONFIRMED as the original local repository's `room_hop_mcp/mcp_http_main.py`, not the Work 32 GitHub tree at SHA `c601c18712ed1d58990314d517409478f41ee11b`.
- Intended transport configuration: CONFIRMED as Streamable HTTP at `/mcp` from inspected source.
- Actual live MCP handshake, `tools/list` result and request/response behavior: NOT YET TESTED.
- Compatibility with Work 32 ADR-002 exact four-tool public boundary: FAIL / NON-COMPLIANT SOURCE INVENTORY, pending confirmation of the live process loaded exactly this file (parent command and module origin strongly identify it).
- Browser Adapter PID 20468 actual module origin and working directory: STILL UNVERIFIED.
- Adapter-to-MCP end-to-end handoff and transcript readback: NOT PROVEN.

### Architecture finding for Xu

The PC currently exposes evidence of a legacy/broader Streamable HTTP POC that includes duplicate lifecycle operations and additional sandbox/agent tools. Work 32 ADR-002 explicitly keeps `join_meeting` and `start_meeting` at the Core HTTP boundary and defines only four public MCP V1 tools. This is a public-boundary drift risk, not a reason to widen ADR-002. Xu should decide how the legacy POC is retired, isolated, or replaced by a Work 32-conformant runtime after reviewing source provenance and dependencies.

No process was stopped or restarted. No source was edited. No tool call was made against the live `/mcp` endpoint. No meeting transcript was changed.

## DOC-068 Addendum A — BIÊN BẢN / NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05; exact clock time not present in supplied capture
- **Action:** Read and classified the user-supplied PC process/module inspection output; recorded actual module path, Streamable HTTP configuration, expanded tool inventory, and ADR-002 contract mismatch.
- **Disposition:** Evidence only; no runtime mutation and no release decision.


## Addendum B — Browser Adapter source audit (P0, 2026-11-05)
Exact branch HEAD c601c18712ed1d58990314d517409478f41ee11b; run #41 / 41807578306 SUCCESS, 4/4 jobs SUCCESS. MCP server and stdio CI test assert the exact four ADR-002 tools. Browser Adapter only requires three, does not reject extras, falls back to the first active meeting and defaults identity to xu. Its live E2E can mutate a real transcript. CI E2E_TESTS excludes tests/test_browser_agent_adapter_e2e.py, so run #41 is not Browser Adapter E2E evidence. Browser Adapter exact-contract enforcement GAP / NOT VERIFIED; live handoff BLOCKED / NOT RUN. No source edit, live MCP request, restart, meeting selection, transcript mutation, commit or push. Xu decision required on scope before patching. Work 32 ACTIVE — NOT RELEASED.


### Addendum B — BIÊN BẢN / NHẬT KÝ
- Name: Ka
- Title: CSA / Backend & Repository Custodian
- Date-Time: 2026-11-05; exact minute not captured
- Action: Rechecked exact branch SHA and GitHub Actions jobs; audited MCP server, Browser Adapter client, Browser Adapter E2E test and CI workflow at the exact SHA.
- Disposition: Recorded source-level contract gap and transcript-mutation safety risk. No code or workflow changed; no live request or transcript mutation performed. Xu decision required before implementation.


## Addendum C — Browser Adapter hardening / CI evidence (2026-11-05)
- Adapter source `room_hop_mcp/browser_agent_adapter/adapter.py` now enforces the exact ADR-002 four-tool inventory and rejects extras/missing tools.
- Submission requires `ROOMHOP_TEST_MODE=1`, `ROOMHOP_TEST_MEETING_ID`, and `ROOMHOP_TEST_IDENTITY_ID`; it no longer chooses the first active meeting or defaults identity to xu. The configured test meeting must exist and be active.
- Each browser workflow now has an `evidence_id`; readback checks the exact marker and execution/evidence/work/file identifiers.
- Five deterministic tests were added to `tests/test_browser_agent_adapter_contract.py` and included in CI. The PC live E2E test is guarded and skips without explicit disposable test configuration.
- Run #48 / 41922846395 at SHA `48abd852540621ac31ae46b311749d1959b58771`: E2E failed 49 passed / 1 failed due to comparing a raw marker after JSON escaping. The failure was retained and corrected by searching decoded transcript string values.
- Run #49 / 41923038244 at SHA `b4c6ba4e0d9cbe86cb5b300b8d315f051ecdfc81`: SUCCESS 4/4; Unit 189 passed; E2E 50 passed; tooling and product artifact PASS.
- Run #50 / 41923112138 at exact SHA `0a5f68083ea534c5fe3dd5651cd926756119e5e1`: SUCCESS 4/4; Unit 189 passed; E2E 50 passed including five Browser Adapter tests; tooling and immutable product artifact PASS.
- Run #50 artifacts: unit 13368101835; E2E 13367437810; tooling 13366784637; product 13367787377. SHA-256 digests are recorded in the canonical Work 32 journal W32-LOG-53.
- Still BLOCKED / NOT VERIFIED: Windows-local module origin and working directory for PID 20468; live MCP handshake and live transcript readback. Available connected tools cannot inspect the user's local Windows process table. CI contract tests mock MCP calls and do not prove live PC transport.
- PID 15048 is the legacy runtime on prohibited port :8020; no request was made to that port. No process restart/termination or real-meeting transcript mutation occurred. Work 32 ACTIVE — NOT RELEASED.


---

## Addendum D — independent review of PC runtime provenance (2026-11-05)

- **Document Number:** DOC-068 / Addendum D
- **Priority:** P0 — Runtime provenance and prevention of false Work32 E2E acceptance
- **Prepared by:** Ka — CSA / Backend & Repository Custodian
- **Authority:** Xu W32-LOG-20261105-61; Ka W32-LOG-20261105-62; PC evidence supplied by Vinh in W32-LOG-60.

### Evidence classification

1. PID 20468 returned HTTP 200 for GET `/health` and GET `/openapi.json`. This confirms the HTTP surface responded at the time of capture only.
2. Parent PID 9108 command line sets launch working directory and `PYTHONPATH` to `.ai-workspace/release/WORK09` before starting `uvicorn adapter:app`. This is strong WORK09 launch-context evidence, but not direct proof of the loaded module object's in-memory `__file__`.
3. PID 20468 CWD was unavailable. No import origin, source Git blob, containing repository metadata or comparison with Work32 Browser Adapter blob was produced.
4. Corrected diagnostic's child-process `find_spec('adapter')` is reconstructed import resolution only; it cannot inspect the target PID's already-loaded module or reproduce its private process environment.
5. Exact Work32 Browser Adapter source blob remains `8cd73faca62057cbfbbd0ac03c07254c02e8df6c`; no equality comparison against PID 20468's loaded source is available.

### Decision and next gate

- Existing PID 20468 is **NOT ACCEPTED as a verified Work32 runtime**. Work32 runtime provenance remains BLOCKED / NOT VERIFIED.
- Do not restart, terminate, reconfigure or repoint PID 20468. Do not use the legacy MCP process on `:8020`; do not call `/mcp`, POST endpoints, transcript APIs or mutate a meeting.
- The next safe path is a separate, isolated Browser Adapter process launched from the clean Work32 clone/authorized branch on a separately selected port. The old WORK09-context process remains untouched.
- Before any live MCP or transcript-writing E2E, establish the new process executable, CWD, launch command, exact source Git blob, compatible MCP endpoint/transport, exact ADR-002 four-tool inventory, and a dedicated disposable meeting plus identity. Keep each criterion independently evidenced.
- No isolated process was created or tested in this addendum. Live MCP handshake, live tool inventory and transcript readback remain NOT RUN.

### Overall status

- HTTP surface of existing PID 20468: PASS for GET checks only.
- Work32 runtime provenance: BLOCKED / NOT VERIFIED.
- Live MCP transport and transcript persistence: NOT RUN.
- Work 32: ACTIVE — NOT RELEASED.

### BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Disposition:** Addendum records independently reviewed evidence and safe next gate; no runtime or architecture mutation.

### NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Action:** Reconciled PC result W32-LOG-60 and independent review W32-LOG-62 into DOC-068 without promoting launch-context evidence to in-memory provenance.
- **Result:** Existing adapter not accepted as Work32 runtime; isolated runtime is the next controlled step. No PC execution, MCP call, transcript mutation, code change, merge, deployment or release.


---

## Addendum E — Transport compatibility review for isolated Work32 Browser Adapter (2026-11-05)

- **Document Number:** DOC-068 / Addendum E
- **Priority:** P0 — MCP transport compatibility / prevent an unusable isolated runtime
- **Prepared by:** Ka — CSA / Backend & Repository Custodian
- **Authority:** Vinh “OK tiếp”; prior gate DOC-068 Addendum D and W32-LOG-62/63.

### Exact Work32 source evidence reviewed

| Source | Git blob | Observed contract |
|---|---|---|
| `room_hop_mcp/browser_agent_adapter/adapter.py` | `8cd73faca62057cbfbbd0ac03c07254c02e8df6c` | Browser Adapter client sends HTTP JSON-RPC POST through `requests.post` to `ROOMHOP_MCP_URL`; negotiates MCP session/protocol headers; expects JSON or SSE response. |
| `room_hop_mcp/__main__.py` | `43adaa746f8e51a6ecce762a7b01694d0411d105` | Work32 MCP entrypoint creates the public server and runs `mcp.server.stdio.stdio_server()`; documented invocation is `python -m room_hop_mcp`. |
| `room_hop_mcp/adapter/server.py` | `b740f72b95ea3a6e0a7e1d19a3ef3275b9899815` | Shared MCP server factory registers exactly four ADR-002 tools and delegates to MeetingService. |
| `room_hop_mcp/adapter/http_server.py` | `f17d752f6badf2b600f78906e63982d18f70e859` | FastAPI Core HTTP routes; this is not an MCP Streamable HTTP server and does not expose the MCP `/mcp` JSON-RPC endpoint. |
| `tests/test_ci_mcp_stdio_e2e.py` | `b78d69e3a6f35c7c573c9fd699a9d3993b883c74` | CI integration launches the MCP stdio client/session and asserts the exact four-tool inventory plus persisted test transcript roundtrip. |
| `tests/test_browser_agent_adapter_contract.py` | `4151ea6eda790716b238806a35f11ba8c76b8a11` | Browser Adapter contract tests mock MCP calls; they do not establish a live HTTP MCP server. |

### Finding

A separate Browser Adapter process on another HTTP port, by itself, does **not** solve the integration gap. The Browser Adapter's current client expects an HTTP MCP endpoint, while the reviewed Work32 MCP entrypoint serves stdio. The existing Core HTTP adapter is a different REST contract and cannot be relabeled as MCP. The legacy process on `:8020` is not an acceptable substitute: its source inventory is broader than ADR-002 and it is outside the Work32 branch source.

Therefore the proposed isolated runtime is **BLOCKED pending an explicit transport decision**. Do not set `ROOMHOP_MCP_URL` to the Core REST base URL, the legacy `:8020` root, or the Browser Adapter's own `/mcp` route.

### Xu architecture decision required

Xu should select and define one supported transport path before implementation:

**Option A — retain Work32 MCP stdio as the only public transport.** Adapt the Browser Adapter integration to use the existing MCP stdio client/session boundary (or a bounded stdio bridge) while preserving the exact four-tool inventory. Xu must define subprocess/session lifecycle, shared `ROOM_HOP_MEETINGS_DIR`, concurrency, process ownership and cleanup. Do not introduce a network MCP endpoint.

**Option B — add a dedicated Work32 MCP Streamable HTTP entrypoint.** Reuse the existing `create_server(MeetingService)` factory so tool semantics and ADR-002 inventory remain identical. Define loopback binding, endpoint path, process lifecycle, test-only data directory, authentication/access controls, session behavior, and tests proving HTTP transport parity with the existing stdio contract. This is a new transport surface and requires Xu's architecture approval before code changes.

**Not accepted:** calling Core REST routes directly from Browser Adapter as a shortcut; widening the four-tool MCP inventory; using the legacy `:8020` runtime; or changing Core business/lifecycle semantics to make a client pass.

### Scope and safety boundary

- Work32 original design brief states PC changes and live-service changes are out of scope. No PC process was created, started, stopped or reconfigured in this review.
- No HTTP request was sent to `:8020`, `:8787`, or any `/mcp` endpoint.
- No POST, transcript read/write, meeting mutation, environment change, source/workflow edit, merge, deployment or release occurred.
- After Xu decides transport, Ka will review the implementation contract and deterministic tests. Any PC runtime execution remains separately gated and must not violate the no-PC-change boundary without explicit owner authorization.

### Status

- Browser Adapter source-level test guardrails: PASS for the tested CI scope.
- Work32 MCP stdio contract: source and CI test path confirmed.
- Work32 MCP Streamable HTTP endpoint: NOT PRESENT in the reviewed entrypoint/source.
- Browser Adapter ↔ Work32 transport compatibility: BLOCKED pending Xu decision.
- Isolated PC runtime: NOT CREATED / NOT TESTED.
- Work32: ACTIVE — NOT RELEASED.

### BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Disposition:** Transport mismatch identified from exact Work32 source. No transport implementation or PC runtime action authorized/performed.

### NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Action:** Audited Browser Adapter HTTP client, Work32 stdio MCP entrypoint, shared MCP server factory, Core REST adapter and CI stdio E2E test.
- **Result:** Isolated Browser Adapter process alone cannot connect to the reviewed Work32 MCP runtime. Submitted Option A/Option B transport decision to Xu; retained no-PC-change and no-live-service-mutation boundaries.


---

## Addendum F — Feasibility refinement for stdio reuse (2026-11-05)

- **Document Number:** DOC-068 / Addendum F
- **Priority:** P0 — Xu transport decision support
- **Prepared by:** Ka — CSA / Backend & Repository Custodian
- **Authority:** W32-LOG-64; exact Work32 source review.

### Additional source evidence

- `integration/room_hop_integration.py`, blob `dd0f544178f84e7b45cf9f7654af608e7ad2944c`, already provides an MCP client over the canonical stdio transport.
- Its `RoomHopIntegrationConfig` explicitly carries Python executable, module (`room_hop_mcp`), repository-root CWD and environment.
- `RoomHopIntegration.session()` starts `python -m room_hop_mcp` through `mcp.client.stdio.stdio_client`, performs MCP initialization, yields a `ClientSession`, and closes the subprocess/session on context exit.
- It provides 1:1 methods for the four ADR-002 tools. The CI stdio E2E uses this same integration boundary and an isolated `ROOM_HOP_MEETINGS_DIR`.
- Important limitation: `verify_capabilities()` currently checks that required tools exist but does not reject extra tools. Exact set equality is asserted by `tests/test_ci_mcp_stdio_e2e.py`; any Browser Adapter reuse must retain an exact four-tool check before tool calls.

### Feasibility assessment

Option A from Addendum E is technically grounded in an existing Work32 client and does not require a new MCP network listener. It is the lower-surface-area candidate because it reuses the already tested stdio server and client boundary. It is not yet approved or implemented.

Before choosing Option A, Xu must resolve:
1. Whether Browser Adapter is allowed to use the existing `integration.RoomHopIntegration` client boundary, rather than maintaining a second independent MCP client.
2. How the synchronous FastAPI/Playwright Browser Adapter invokes the asynchronous stdio session safely (thread/event-loop ownership and error propagation).
3. Whether a subprocess/session is opened per browser workflow or held by a managed lifecycle; define timeout, cleanup, concurrency and shutdown behavior.
4. The exact isolated `ROOM_HOP_MEETINGS_DIR` and test meeting/identity provisioning, with no default to production or real meetings.
5. Exact four-tool equality validation and transport/readback tests using the same semantic assertions as the existing stdio E2E.

Option B remains possible only with an explicit Xu decision and a new transport-parity test suite. No evidence currently supports an existing Work32 Streamable HTTP MCP server.

### Recommendation to Xu

Prefer evaluating **Option A first** because the stdio MCP boundary and its subprocess lifecycle already exist and are exercised in CI. Do not implement until Xu records the decision and the synchronous/asynchronous lifecycle, data isolation and exact-tool validation are specified. Option B should be selected only if a real requirement for HTTP MCP transport is confirmed.

### Boundaries and status

- This is a source-level feasibility assessment only; no source changes or runtime execution.
- No PC changes, service calls, MCP network requests, transcript mutation, process changes, merge, deployment or release.
- Transport decision remains PENDING Xu.
- Browser Adapter live handoff remains BLOCKED / NOT RUN.
- Work 32 ACTIVE — NOT RELEASED.

### BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Disposition:** Existing stdio client identified as a feasible lower-surface-area option; no implementation authority inferred.

### NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Backend & Repository Custodian
- **Date-Time:** 2026-11-05 (exact time not captured)
- **Action:** Inspected RoomHopIntegration configuration/session lifecycle and existing stdio E2E to refine Xu's transport decision.
- **Result:** Option A is grounded in existing code but requires Xu decision on async lifecycle, process ownership, isolation and exact tool inventory.


---

## Addendum G — Xu transport decision (2026-11-05)

- Xu selected Option A: reuse RoomHopIntegration over canonical stdio; no HTTP MCP listener.
- Browser Adapter source removes its independent HTTP JSON-RPC/SSE client and ROOMHOP_MCP_URL. Each workflow owns one stdio session through RoomHopIntegration; exact four-tool equality, exact active test meeting, explicit identity and transcript readback are required.
- Isolation requires ROOMHOP_TEST_MODE=1, explicit meeting and identity, absolute ROOMHOP_TEST_MEETINGS_DIR, an existing directory and exact .roomhop-disposable-test-store sentinel. Child ROOM_HOP_MEETINGS_DIR, CWD and PYTHONPATH are explicitly pinned.
- Contract tests now cover stdio lifecycle, store sentinel, explicit target, exact tools, missing/inactive meeting and readback. PC E2E requires the disposable store.
- CI validation is pending for the current implementation. No PASS claim until exact-SHA checks complete.
- PID 20468 remains untouched; its Work32 provenance is still unverified. No PC runtime action, MCP call, transcript mutation, :8020 use, merge, deploy or release.
- Next: inspect exact-SHA CI, repair failures, then submit implementation to Ka for independent review. PC runtime remains gated by Ka review and source provenance.
- Work32 ACTIVE — NOT RELEASED.


---

## Addendum H — Ka review findings and Xu corrective implementation (2026-11-05)

### Ka independent review
- Ka's Sandbox review W32-LOG-67 and W32-LOG-70 confirms the Option A stdio migration, exact tool inventory, explicit disposable target and mocked contract tests are present.
- Ka identified two remaining P0 gaps: no bounded timeout/cancellation policy around the async stdio session, and no real Browser Adapter -> RoomHopIntegration child -> Core transcript E2E in CI. The existing stdio E2E tested the MCP client independently, not the Browser Adapter submission function.
- Nested event-loop use also needed to fail closed before constructing the coroutine. The global Browser Adapter singleton (page/context/log state) may interleave under concurrent workflow calls; Ka marked this P2 and requested a separate concurrency contract rather than mixing it into the transport patch.

### Xu corrective implementation
- Added ROOMHOP_MCP_TIMEOUT_SECONDS with default 30 seconds and maximum 120 seconds.
- Wrapped the stdio submission in asyncio.wait_for. Timeout returns BLOCKED with an explicit uncertain-append outcome and no automatic retry.
- Added a running-event-loop guard before coroutine construction. Cancellation is not swallowed inside the stdio session, allowing the existing async context manager to unwind and clean up.
- Added tests for timeout/no-retry and nested-loop fail-closed behavior.
- Added tests/test_browser_agent_adapter_stdio_e2e.py. It creates a temporary store and sentinel, provisions an active disposable meeting, invokes the actual Browser Adapter submit_to_roomhop function, starts the real Work32 MCP stdio child through RoomHopIntegration, and verifies exact four tools, identity, artifact marker and Core transcript readback.
- Registered the real stdio E2E in ci-validation.yml E2E_TESTS.

### Validation boundary
- CI run #83 / ID 41950707518 passed all four jobs for the bounded-timeout/nested-loop source commit.
- CI run #85 / ID 41950798975 and #86 / ID 41950816354 were still running/pending when this addendum was prepared; these runs include the real stdio E2E addition. No PASS claim is made for the new real stdio test until an exact-SHA run completes.
- The global Adapter singleton concurrency concern remains DEFERRED / P2. Per-submission MCP sessions are isolated, but that does not prove the shared browser/page/log state is concurrency-safe.
- No PC process/service action, no live :8787 call, no transcript mutation outside CI's temporary test store, no :8020, no main merge, deploy or release.

Status: timeout/nested-loop implementation committed; real stdio E2E added to CI; exact-SHA validation pending; P2 browser singleton concurrency review deferred. Work32 ACTIVE — NOT RELEASED.


---

## Addendum I — Real Browser Adapter stdio E2E passes CI (2026-11-05)

- CI run #86 / ID 41950816354 validated commit c291bca97369ff15e7f867a51e3b8e1b89f0fe77. All four jobs completed SUCCESS.
- Product Auto E2E: 56 passed. The ten Browser Adapter contract tests all passed, including timeout/no-auto-retry and nested-loop guard. The new tests/test_browser_agent_adapter_stdio_e2e.py::test_browser_adapter_real_stdio_submission_roundtrip passed.
- The real test creates a temporary disposable store with the exact sentinel, provisions an active meeting through MeetingManager/MeetingService, calls the actual Browser Adapter submit_to_roomhop boundary, launches the real MCP stdio child through RoomHopIntegration, validates exact four tools and identity, then reads the Core transcript and verifies the artifact marker.
- Python 3.12 bounded unit tests: 189 passed. Tooling: 20 tests OK. Immutable product artifact E2E: 1 passed. Dependencies check clean.
- This is CI execution in a temporary isolated test store; it is not PC :8787 live E2E and does not validate PID 20468 provenance.
- Timeout behavior and no-auto-retry are covered by a deterministic test. Nested event-loop rejection is covered. Actual OS-level child-process termination under a real timed-out stdio operation is not independently measured yet; retain as a lifecycle verification limitation for Ka to assess.
- P2 global Browser Adapter singleton concurrency (page/context/log state) remains deferred pending a separate service concurrency contract.
- Ka is requested to independently review the updated timeout and real stdio E2E implementation, including the remaining cancellation/process-cleanup evidence boundary.
- No PC process/service action, no live endpoint call, no :8020, no real meeting mutation, no main merge, deploy or release.

Status: Real Browser Adapter -> Work32 MCP stdio -> Core transcript CI E2E PASS at the exact commit; Ka re-review pending; PC provenance remains BLOCKED / NOT VERIFIED. Work32 ACTIVE — NOT RELEASED.


---

## Addendum J — Explicit cancellation propagation and cleanup test (2026-11-05)

- Follow-up to Ka's W32-LOG-67/70 findings: bounded timeout alone is insufficient if RoomHopIntegration masks cancellation while unwinding its nested async context managers.
- Updated integration/room_hop_integration.py to preserve asyncio.CancelledError directly and to unwrap a CancelledError leaf from BaseExceptionGroup instead of converting cancellation into IntegrationError.
- Added a deterministic lifecycle test that simulates task-group cancellation during stdio teardown, asserts cancellation propagates to asyncio.wait_for, and verifies both ClientSession and stdio context exit paths run.
- The test exercises context-manager unwind behavior with a controlled fake stdio context; it does not independently prove OS-level child PID termination on the Windows PC. Actual PC process lifecycle remains gated.
- CI run #92 / ID 41951379259 for the test commit was pending at the time of this addendum. Run #91 for the preceding implementation commit was superseded/cancelled by the next push; do not count it as validation.
- The real Browser Adapter -> stdio -> Core transcript E2E remains PASS at run #86 / exact commit c291bca97369ff15e7f867a51e3b8e1b89f0fe77.
- P2 global Browser Adapter singleton concurrency remains deferred. No PC action, live endpoint call, :8020, main merge, deploy or release.

Status: cancellation propagation and deterministic unwind test committed; CI run #92 pending; OS-level PC child termination NOT VERIFIED. Work32 ACTIVE — NOT RELEASED.


## Addendum L — Cancellation test correction (2026-11-05)
- Run #92 failed 1 of 57 E2E tests. The test injected a synthetic exception group containing cancellation during teardown, which masked the timeout signal.
- Xu restored integration/room_hop_integration.py to its established blob dd0f544178f84e7b45cf9f7654af608e7ad2944c. No change to shared Integration error semantics is retained.
- The test now models direct task cancellation and asserts that the stdio and ClientSession context exits run before wait_for reports timeout.
- Run #96 / 41951719158 for the corrected test was queued; verification pending. This is context cleanup evidence, not OS process termination proof.


## Addendum M — CI confirmation (2026-11-05)
- Run #99 / 41952001890 validated source SHA 9d799e5bf6853ee0e7d3e3ecce6c9d19ccae9e0a; all four jobs passed.
- E2E 57 passed, including direct cancellation cleanup and real Browser Adapter stdio transcript roundtrip. Unit 189, tooling 20, product artifact E2E 1 passed.
- Direct cancellation test verifies async context exits. OS process termination and PC live runtime remain unverified.
- Ka review requested. P2 Browser Adapter singleton concurrency remains deferred.
