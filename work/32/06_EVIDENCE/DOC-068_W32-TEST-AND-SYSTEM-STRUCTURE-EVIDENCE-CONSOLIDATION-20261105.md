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
