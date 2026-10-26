# Work 28 — Xu continuation journal: execution-tool integration
**Date:** 2026-10-25 (Asia/Ho_Chi_Minh)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** Work 28 only. Continue via MCP 8030 Sandbox; GitHub is fallback/reference only when MCP access is insufficient.

## Evidence-backed discovery
- Live MCP 8030 tool surface available to this session exposes Sandbox file operations and ROOM/meeting context tools; no execution/command-running tool is exposed in the current tool list.
- Sandbox inventory confirms Work 28 is present as work_id `28`, with `MCP-8020-TOOLING-PLATFORM` and existing execution-gateway/catalog/server code and tests.
- Sandbox inventory confirms Work 27 is present as work_id `27`, with `SANDBOX-EXECUTION-RUNTIME-VSCODE`, including `sandbox_runtime/adapter.py`, `contract.py`, `http_transport.py`, `policy.py`, and unit tests.
- Work 28 includes prior artifacts for execution-tool contract, gateway, live tool registration, and raw tools/list evidence. This indicates the execution capability may already be partly designed/implemented; do not create a duplicate runner before tracing these artifacts.
- Current inspection did not establish whether the Work 27 runtime is reachable from the live 8030 service. No runtime execution was performed in this turn; no PASS claim is made.

## Ordered continuation
1. Read and reconcile the existing Work 28 execution contract, gateway, catalog/registry, server binding, and latest live tools/list evidence.
2. Trace Work 27 runtime transport and its authorization/policy contract; establish the exact supported request/response schema and reachable endpoint from existing evidence, without guessing hostnames or URLs.
3. Compare intended execution tool(s) against the live 8030 registration. If code and handler exist, repair the missing registration/binding/transport only; avoid duplicate implementations.
4. If a necessary implementation is genuinely absent, implement the smallest compatible change in Work 28 and preserve the Work 27 runtime boundary. Core :8000 must never be placed inside Sandbox.
5. Add/adjust tests for valid Python execution, pytest execution, timeout, non-zero exit, output capture, working-directory confinement, and denied/unauthorized requests.
6. Validate with actual execution evidence through the authorized runtime, capture stdout/stderr/exit code and tool-list result, and record precise status.
7. Update this journal with files changed, tests actually run, evidence paths, and remaining blockers. No fake PASS; if live execution cannot be reached from this MCP session, record BLOCKED with the exact missing dependency and continue independent work.

## Acceptance criteria
- An execution tool is visible in the live 8030 tools/list surface.
- The tool runs a minimal Python command and a pytest command in the intended Work Sandbox, not on the user's PC and not in Core :8000.
- Output, error output, exit code, timeout behavior, authorization and path restrictions are verified.
- Existing file tools and Work 27 runtime tests remain compatible.
- Evidence and journal are saved under Work 28 standard structure.


## 2026-10-25 continuation — source trace result
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Result:** Root cause narrowed to an intentionally unwired execution integration, not merely a missing tool name.

### Confirmed source facts
1. `MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md` explicitly says DESIGN / NOT REGISTERED / NOT LIVE and sets integration decision NO-GO until the authenticated Core :8000 route, canonical W12/W13 runtime reachability, and OS isolation are evidenced.
2. `04_CODE/mcp8020_execution_gateway_v54.py` says “protocol-complete but deliberately UNWIRED”; it defines seven handlers but uses a fail-closed `BlockedExecutionClient` unless a verified Core execution client is injected.
3. `04_CODE/mcp8020_catalog_v54.py` includes seven execution/evidence tools, but marks them `NOT_IMPLEMENTED`.
4. `04_CODE/mcp8020_service_v54.py` returns `NOT_IMPLEMENTED` before dispatch for those catalog entries; an injected gateway alone does not enable them while catalog status remains unchanged.
5. `04_CODE/mcp8020_server_v54.py` supports optional gateway injection, but it is only an adapter and does not own the live host lifecycle.
6. `04_CODE/mcp8020_connector_v54_adapter.py` explicitly blocks all seven execution/evidence tools before transport. Its evidence note says live host registration and wiring to the 8030 transport are not done.
7. Work 27 already has an execution contract, policy and RuntimeAdapter. The adapter uses an injected transport and explicitly states it does not launch processes itself. Its implementation note says the HTTP transport was authored but real runtime/tests remain unverified.
8. Work 27 cross-work decision states W12/W13 are canonical; the current MCP Sandbox surface exposes file operations only and has no live connection to PC localhost. It forbids creating a competing execution host.

### Decision
Do NOT merely flip catalog status or remove adapter guards. That would expose a tool schema without a working, authorized execution path and would violate the existing fail-closed contract.

### Next safe implementation slice
A. Read the Work 13 canonical bridge/attestation and Work 27 HTTP transport contract, including actual deployed identity/route evidence.
B. Verify whether the existing W13 POST /execute route is reachable from an authenticated Core route and whether it enforces Work authorization, OS isolation, immutable source binding and protected evidence.
C. If those gates are evidenced, implement the smallest concrete CoreExecutionClient that calls the canonical route, wire it into the existing gateway/server lifecycle, then enable only execution tools with verified handlers.
D. If gates are not evidenced, complete offline contract/adapter tests and write a precise blocker handoff; do not route MCP directly to localhost:8031, do not create a second execution host, and do not ask the user to operate the PC unless a truly user-only authorization/attestation step is demonstrated.

### Status update
- PASS: source trace identifies the reason execution tools are unavailable and the existing components to reuse.
- BLOCKED: no authorized live execution route or real runtime attestation has been evidenced from this session; no Python/pytest process was launched.
- Work 28 remains ACTIVE / NOT RELEASED.


## Canonical W13 dependency verification (same continuation)
- Work 13 `EXECUTION-HOST-INFRASTRUCTURE/03_ARCHITECTURE/WEE_8031_BRIDGE_STATUS.md` confirms the canonical bridge contract is implemented in source, posts to `/execute`, and defaults to `http://127.0.0.1:8031`; however, LIVE HTTP :8031 and tests are explicitly NOT RUN because PC localhost is unreachable from the current MCP session.
- Work 13 `06_EVIDENCE/W13_CANONICAL_PC_RUNTIME_DECISION_LOG.md` states source implementation READY, but canonical Windows PC runtime attestation BLOCKED. Required evidence is canonical source → Windows startup → PID/process identity → build_hash → /health → /execute with the same runtime identity.
- Work 12 manifest says Work 12 is COMPLETED/LOCKED; future integration/testing belongs to Work 14. Do not modify Work 12 or create a replacement host.
- Therefore the blocker is now precise: **the existing canonical W13 runtime is not attested as live/reachable from the authorized path**, so Work 28 cannot safely instantiate the concrete execution client or claim code execution via MCP. This is not a missing Python handler alone.

### Next action without PC dependency
Continue the offline implementation audit and tests authored in Work 28/27, check Work 14 for the currently owned canonical W12/W13 integration contract, and prepare a minimal adapter patch plan that can be applied once the canonical runtime attestation becomes available. Do not perform any live execution claim until that gate is satisfied.


## Evidence reconciliation — historical Work 14 attestation
Work 14 file `06_EVIDENCE/W13_CANONICAL_PC_ATTESTATION_RESULT_20261012.md` records a successful W13 health + execute attestation on 2026-10-12, with correlated runtime identity and build hash. It explicitly limits that PASS to the attestation request and says it does not prove the full Work 14 E2E.

Do not discard this historical PASS, but do not assume the same process/build is still live on 2026-10-25 or reachable through the current MCP/Core path. Reconcile the older PASS and later blocker by obtaining fresh readiness/identity evidence through an authorized route; do not restart the PC host based on guesswork.

Status: historical attestation PASS for its recorded request; current 8030-to-authorized-Core-to-W13 reachability NOT VERIFIED in this session. No current runtime PASS is claimed.


### Continuation checkpoint — 2026-10-25
- AI attempted to continue source inspection through MCP 8030. `sandbox_list` for Work 27 returned the expected inventory, but subsequent `sandbox_read` / `sandbox_read_probe` calls were rejected by the tool safety checker before a file result was returned. Work 28 listing and journal append were also rejected by the safety checker during this checkpoint; no source files were modified by these rejected calls.
- GitHub fallback confirmed repository `hqtt2026-thevinhvtqni/room-meeting-ai` exists and is public, but the guessed Work 28 path was not found on the queried ref and code search did not return the sandbox-only v54 file. No claim of source parity or deployment is made.
- Status remains: source-level root cause previously established; execution tool integration and runtime execution NOT VERIFIED. Continue once the authorized file-read/write path is available; do not change tool exposure or route around authorization controls.


### Remediation plan checkpoint — 2026-10-25
- Created `06_EVIDENCE/WORK28_EXECUTION_INTEGRATION_REMEDIATION_PLAN_20261025.md` in Work 28 Sandbox via MCP 8030 (write returned status=ok).
- Plan breaks the remaining work into canonical API, lifecycle/evidence, negative tests, authorized runtime integration, and release gates. It explicitly preserves the hard rule: execution tools remain NOT_IMPLEMENTED until current Core route, current W13 runtime identity, OS isolation, protected evidence, Cla review and Go independent E2E are evidenced.
- No PC/VS Code action is needed for the current offline planning/source-reconciliation step. PC validation will be requested only if authorized tools cannot obtain current Windows :8031 attestation and real end-to-end output.
- No code/test was executed or deployed in this checkpoint. Work 28 remains ACTIVE / NOT RELEASED.


### Contract validator added — 2026-10-25
Added `04_CODE/mcp8020_execution_contract_v1.py` and `05_TEST/test_mcp8020_execution_contract_v1.py` to GitHub branch `work/28-mcp-tooling-platform`. Validator rejects caller identity/command fields, traversal and ambiguous paths, invalid source SHA-256, invalid operation/timeouts, and does not accept PASS without source-hash match, run/runtime/evidence references; RUN_TESTS also requires a nonzero test count and zero failures/errors. This is contract-level groundwork only; not wired into the live service and tests have not been executed. GitHub commits: `f4fe68da976c0f131c65f8eaec581fdcc4fb98be`, `ad199b4abfcd5f7cb0fa1ee0e36c760ce9f61e5a`, `5a23c45fbbee091ea60ec24cf3670bd8ecc8de4c`. CI status query for the test commit returned no statuses.

### Contract validator synced to Sandbox — 2026-10-25
The new contract validator and unit tests have now been copied from GitHub branch `work/28-mcp-tooling-platform` into the corresponding Work 28 Sandbox paths through MCP 8030. Both sandbox_write calls returned status=ok. GitHub blob SHAs: validator `2e22fb0204988f8466e2c566c7ede29cb75fceff`; tests `0cffb6b55b0d99fa0ef2e34e65e1ea5baf659018`. These writes prove file sync only. The MCP surface available here has no authorized Python/pytest execution tool, so tests are NOT RUN and the validator is not yet wired into the live gateway/service. Next gate is test execution in an authorized sandbox/runtime, then integration review; no PC action needed yet.

### Additional fail-closed edge cases — 2026-10-25
Updated the contract validator to reject control characters in `entry_path` and to require an integer `exit_code` exactly equal to zero (so `0.0` is not accepted). Added regression cases for these inputs. Latest GitHub commits: validator `6c60b751f6d11585c8377a03afe6bac2395238c8`; tests `e0a6ef91ae378af158830970d1a70f0776e037f5`. Both latest files have been synced to Work 28 Sandbox through MCP 8030 with status=ok. The existing GitHub Actions workflow is configured to run `python -m unittest discover -s 05_TEST -v` on pushes to the Work 28 branch, but this session has not obtained a run/result record; therefore no test PASS is claimed. Execution tools remain NOT_IMPLEMENTED until authorized runtime integration and security gates pass.

### Migration-gate regression guard — 2026-10-25
Added a regression test to `05_TEST/test_mcp8020_execution_contract_v1.py` that asserts all seven legacy execution/evidence catalog entries remain `NOT_IMPLEMENTED` and confirms the legacy `sandbox_run_python` schema still accepts `script` rather than the candidate contract's `entry_path` + `expected_source_sha256`. This intentionally prevents accidental activation by gateway injection alone. Commit: `e683875073f7c0c71109ba0cbc4e1b63a162a597`; updated test blob SHA `284f691be799fb887b87d9781170fb8d6c88aef9`. Test file synced to Sandbox with MCP 8030 (`status=ok`). No test execution result is available yet; CI run status not verified.

### Execution contract migration map — 2026-10-25
Created `03_ARCHITECTURE/EXECUTION_CONTRACT_MIGRATION_MAP_20261025.md` on GitHub branch `work/28-mcp-tooling-platform`, commit `cff08f2f3f3adf166ce53cd899903d99dce46856`. It maps all seven current execution/evidence tools to the proposed Python contract, records schema incompatibilities and mandatory runtime/security gates, and preserves the NOT_IMPLEMENTED release gate. Attempted to sync the document into Sandbox via MCP 8030; the platform safety checker blocked that write, so Sandbox sync is BLOCKED (not claimed complete). No execution tool was activated and no test PASS is claimed.

## Continuation update — 2026-10-25 (MCP 8030 static trace)
- Read back `04_CODE/mcp8020_execution_gateway_v54.py` through the Sandbox diagnostic read path. Confirmed gateway is explicitly UNWIRED and defaults to `BlockedExecutionClient`; seven methods are only protocol handlers against an injected client.
- Read back `04_CODE/mcp8020_service_v54.py`. `call_tool()` returns `NOT_IMPLEMENTED` before argument validation/dispatch for catalog entries marked `NOT_IMPLEMENTED`. `bind_execution_gateway()` checks interface completeness, but binding alone does not override catalog status or prove authorization/runtime readiness.
- The gateway payload for `sandbox_run_python` currently uses `operation=RUN_SCRIPT`, `entry=script`, and `args`; the proposed contract requires `entry_path` plus `expected_source_sha256`, and supports only `RUN_SCRIPT`/`RUN_TESTS`. This is a concrete schema migration blocker, not a reason to bypass catalog guards.
- Read-back was static only. No pytest, CI, live Core route, or Windows runtime test was executed; no PASS is claimed. Keep all seven tools NOT_IMPLEMENTED until server-derived identity/Work authorization, canonical Core :8000 → existing W12/W13 runtime, OS isolation, immutable source snapshot/hash, protected evidence, and independent E2E are evidenced.
- GitHub fetch via the currently available connector returned 404 for the previously referenced `work/28/...` paths; the branch itself is discoverable. No GitHub file mutation was attempted in this continuation. Treat MCP Sandbox read-back as current evidence only for the returned files, not proof of GitHub/Sandbox synchronization.


### Xu independent read-back — Go offline completion bundle (2026-10-25)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB  
**Scope:** static inspection of Go artifacts through MCP 8030; no runtime execution performed.

**Confirmed from read-back**
- `GO_FULL_OFFLINE_SUITE_20261025.log` records `Ran 208 tests`, `OK (skipped=4)`; this is recorded agent-host output, not a rerun by Xu.
- `mcp8020_execution_alignment_v1.py` asserts the seven catalog entries remain NOT_IMPLEMENTED, validates the target request through the v1 validator, and checks service short-circuit behavior.
- `mcp8020_execution_gateway_v54.py` raises `ToolCallError("POLICY_REFUSED", ...)` directly from `sandbox_run_command`; that method contains no client dispatch.
- `mcp8020_execution_contract_v1.py` explicitly documents that validation is shape-only and does not authorize callers, launch processes, or prove a live route.
- Integration probe records Core :8000 unreachable, `/core` HTTP 404, and `/build/mcp` HTTP 406. These do not establish a working E2E execution path.

**Reconciliation finding — artifact set is not yet self-consistent**
- The read-back of `test_mcp8020_execution_alignment_v1.py` imports `mcp8020_strict_execution_gateway_v1.StrictExecutionGatewayV1`.
- A direct MCP 8030 probe for `MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_strict_execution_gateway_v1.py` returned FileNotFoundError, and the Work 28 Sandbox inventory does not list that module.
- Therefore the reported 208-test agent-host log cannot be independently reproduced from the exact current Sandbox file inventory as read here. Possible working-tree/snapshot mismatch remains unresolved; do not downgrade Go's recorded run to FAIL, but do not claim reproducible PASS from the Sandbox snapshot.
- The SHA manifest records hashes for the strict gateway and related modules, but hash lines alone do not supply the missing source file or prove that the listed bytes match the current Sandbox tree.

**Decision / next action**
1. Keep all seven execution/evidence tools NOT_IMPLEMENTED; keep Work 28 ACTIVE / BLOCKED / NOT RELEASED.
2. Reconcile the missing strict gateway source and any other test dependencies into one exact, hash-pinned source snapshot, then rerun the full suite against that snapshot in an authorized Python environment.
3. Do not modify Core, expose execution handlers, flip catalog status, or RELEASE without current authenticated Core → canonical W12/W13 runtime, OS-isolation, immutable snapshot/evidence and independent E2E evidence.
4. PC action remains limited to the live Windows/Core/runtime attestation that cannot be obtained through this MCP surface; no PC action is needed for this static artifact discrepancy.

**Result:** Static source review PASS for the stated fail-closed logic; artifact reproducibility gate BLOCKED; live integration gates BLOCKED.


### Xu reconciliation of Go rerun evidence — 2026-10-25
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB

- Read back `06_EVIDENCE/GO_RERUN_SUITE_20261025T021309Z.log` through MCP 8030. The log ends with `Ran 208 tests in 0.053s` and `OK (skipped=4)`. This supports recorded offline suite PASS; Xu did not execute the suite independently.
- The same log identifies four skipped tests as live MCP server tests skipped because the `mcp` package is not installed in that environment. This reinforces that offline suite PASS is not live MCP execution evidence.
- Sandbox inventory now lists `04_CODE/mcp8020_strict_execution_gateway_v1.py` and `05_TEST/test_mcp8020_strict_execution_gateway_v1.py`, resolving the earlier apparent missing-file discrepancy at the current inventory level. A direct read probe had transiently returned FileNotFoundError; do not treat that earlier response as proof the file is absent.
- The user-referenced `06_EVIDENCE/GO_E2E_ATTEMPT_20261025T021436Z.log` was not present in the current Sandbox inventory, and direct read returned FileNotFoundError. Therefore the E2E details in the handoff remain user/Go-reported evidence rather than independently read-back log evidence in this session. The live path remains BLOCKED regardless; no E2E PASS is claimed.
- Official status unchanged: ACTIVE / BLOCKED (Core·runtime·OS isolation·immutable evidence·live E2E) / NOT RELEASED. Keep all seven execution/evidence tools NOT_IMPLEMENTED.


### Xu continuation — strict gateway and integration-plan reconciliation (2026-10-25)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** read-only source inspection through MCP 8030; no code changed and no runtime launched.

**Fresh source findings**
1. Read-back confirms `mcp8020_strict_execution_gateway_v1.py` exists. It validates the target contract envelope and forwards it to an injected `StrictCoreExecutionClient.submit()`, but its module docstring explicitly says it is a staging seam and is **not wired into v54 service**. It does not authorize callers, read/hash source files, launch processes, or prove runtime identity.
2. The strict gateway unit tests use a fake client. They cover shape rejection and PASS-result shape checks only; they do not prove Core authorization, hash snapshot enforcement, runtime isolation, or live execution.
3. `mcp8020_service_v54.py` still short-circuits all catalog entries marked `NOT_IMPLEMENTED` before argument validation/dispatch. This is intentional fail-closed behavior, not a wiring bug to bypass.
4. `mcp8020_execution_gateway_v54.py` is a separate legacy-shaped gateway. Its `sandbox_run_python` still builds `entry=script` + `args` and omits `expected_source_sha256`, which does not match contract v1's `entry_path` + hash envelope. Its command handler is hard `POLICY_REFUSED` before dispatch.
5. `mcp8020_execution_alignment_v1.py` explicitly asserts all seven execution/evidence tools remain `NOT_IMPLEMENTED` and that the service keeps returning `NOT_IMPLEMENTED` even with a gateway bound.
6. The remediation plan's older statement that contract-parity tests are not updated is partially superseded by Go's later alignment report and the 208-test rerun log. However, no read-back evidence shows a concrete authenticated Core client or current live runtime path; the core integration gate remains BLOCKED.
7. `GO_EXECUTION_ALIGNMENT_RESPONSE_20261025.md` reports agent-host passes for alignment, gateway, contract and strict-gateway tests, but these are offline tests and not live E2E. The broader rerun log separately records 208 tests, OK (skipped=4).

**Decision / next step**
- Keep all seven execution/evidence tools `NOT_IMPLEMENTED`; do not wire the strict adapter to a fake or guessed endpoint, do not flip catalog statuses, and do not add a direct MCP-to-`:8031` path.
- Offline contract alignment is now better covered; the remaining decisive blocker is current, authenticated Core `:8000` → canonical W12/W13 runtime evidence, including deployed revision, runtime identity/build hash, OS isolation, immutable source snapshot and protected evidence.
- No PC action is needed for this source reconciliation. A bounded PC attestation becomes necessary only for current Windows/Core/runtime proof unavailable through authorized MCP tools.

**Status:** static reconciliation PASS for the listed source facts; live integration BLOCKED; Work 28 ACTIVE / BLOCKED / NOT RELEASED.


### Cross-Work dependency trace — W27/W13 adapter contract (2026-10-25)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** read-only inspection of Work 27 and Work 13 Sandbox artifacts via MCP 8030.

**Confirmed**
- Work 13's existing canonical bridge contract expects `execute_work(work_context, execution_request)` and posts a nested JSON envelope to W13 `POST /execute`; its default `127.0.0.1:8031` endpoint is not reachable from this MCP session and is not evidence of a live route.
- Work 27 `sandbox_runtime/http_transport.py` implements `HttpTransport.execute(work_context, execution_request)` and sends that nested envelope. The transport itself is a thin client; it does not launch processes.
- Work 27 `sandbox_runtime/adapter.py` currently invokes its injected transport as `self._t.execute(single_payload_dict)`, where the payload contains `schema_version/task_id/run_id/workspace_id/source_revision/argv/cwd/timeout_seconds/resource_profile/network_profile/requested_by`. This does not match the two-argument `HttpTransport.execute(work_context, execution_request)` signature or Work 13's required nested envelope.
- Work 27's own cross-work decision says it must not create a competing execution host and that current MCP Sandbox exposes file operations only; authenticated Core/PC transport and canonical workspace binding remain prerequisites.
- Historical Work 14 attestation on 2026-10-12 proves one specific W13 health + execute request at that time (instance `w13-249361af3a7b4372bbc4b30f03bff2c7`, build hash `a3ab13f49fd10501588a6da26028b1c147ba7097836884ae39264af49e124012`). It does not prove that same instance/build is live now or reachable from current MCP 8030/Core. Do not restart port 8031 or assume this historical runtime identity remains current.

**Integration implication**
There is a concrete adapter/transport contract mismatch in the existing Work 27 source. Do not paper over it by calling localhost from MCP, passing caller-controlled identity/WorkContext, or creating a second runtime. The next code change must be a narrowly reviewed mapping at the authorized Core/W12/W13 boundary, with WorkContext derived by Core and explicit tests for the exact nested request envelope. Because Work 28 owns the MCP integration, first document the required mapping here; do not mutate Work 27 files as part of this Work 28 continuation.

**Status**
- PASS: source-level signature/envelope mismatch reproduced by read-back.
- BLOCKED: no current authenticated Core route, current W13 runtime attestation, or OS-isolation evidence.
- Work 28 remains ACTIVE / BLOCKED / NOT RELEASED; seven execution/evidence tools remain NOT_IMPLEMENTED.


### Go integration-boundary mapping — Xu read-back review (2026-10-25)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Review scope:** read-back through MCP 8030 of the two new modules, six-test file, Go evidence note, contract validator, service v54, and execution gateway v54. No code changed; no runtime or host was launched.

**Read-back findings**
1. `mcp8020_w13_execute_envelope_v1.py` calls the existing contract-v1 validator, requires a non-empty `work_context.work_id`, rejects Work ID mismatch, and emits the W13 two-part envelope. The resulting execution request contains `operation`, `entry_path`, `expected_source_sha256`, `timeout_seconds`, `language`, and `work_id`; it does not include inline script/command fields.
2. The contract validator rejects extra fields (including `script`/identity fields), requires the SHA-256 and only permits `RUN_SCRIPT` / `RUN_TESTS`; `RUN_COMMAND` is rejected.
3. `mcp8020_w27_http_transport_bridge_v1.py` accepts the single-dict protocol shape only when both `work_context` and `execution_request` are present, then calls the injected two-argument transport. Flat adapter payloads are refused.
4. The new test file contains six test methods covering envelope construction, Work ID mismatch, legacy shape, missing hash, two-argument forwarding and flat-payload refusal. These are offline tests using a fake HTTP transport. The user/Go-reported result is 6 tests / exit 0; this session performed source read-back only and did not independently execute them.
5. The new evidence note explicitly limits the change to offline mapping and says no service wiring, runtime enablement or live E2E was done.
6. Service v54 still short-circuits catalog `NOT_IMPLEMENTED` tools before dispatch. Gateway v54's public `sandbox_run_python` still has the legacy `script/entry/args` signature, while the new envelope builder is a separate pure function; the new bridge modules are not shown wired into service/gateway/server or a concrete Core client.
7. Important trust boundary: the envelope builder can check the supplied `work_context` shape and Work ID equality, but cannot itself prove that context was created by Core. That remains an upstream authenticated-Core responsibility. The W27 bridge likewise adapts arity only; it does not establish authorization, hash snapshot integrity, runtime identity, OS isolation or protected evidence.

**Assessment**
- PASS: the two pure mapping components and negative-test intent are present in Sandbox; source shape aligns with Go's stated scope.
- PASS (reported, not independently rerun): Go states 6 tests passed with exit 0.
- BLOCKED: production integration/wiring and live Core → canonical W12/W13 execution path remain unproven.
- No reason to change the catalog: all seven execution/evidence tools remain `NOT_IMPLEMENTED`.
- No direct MCP → `:8031` path, no second host, no runtime activation, no RELEASE.

**Next work within scope**
Continue static contract audit and test/evidence reconciliation; identify whether the mapping modules have dedicated regression tests for malformed context/request types and forbidden extra keys at the boundary. Do not wire them to service v54 until the authenticated Core route and all runtime/security gates are evidenced.

**Status:** Work 28 ACTIVE / BLOCKED / NOT RELEASED.


### Xu — review of Go expanded boundary tests and closure-time decision (2026-10-25)
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** read-back via MCP 8030 of Go's expanded test file and both new evidence artifacts; no code execution or runtime launch.

**Fresh read-back**
- `test_mcp8020_integration_boundary_v1.py` is present and contains 16 test methods: 1 happy path, 5 context-negative cases, 6 request/legacy cases, and 4 bridge cases. Coverage includes None/list context, missing/blank/mismatched Work ID, non-dict request, missing hash/path, extra shell/argv, legacy script/entry, flat/non-dict payload, and non-dict envelope parts.
- `GO_BOUNDARY_NEGATIVE_TESTS_AND_EVIDENCE_20261025.md` reports 16 tests / exit 0. Xu read the test source but did not independently execute it; result remains Go-reported, not Xu-rerun.
- `GO_CORE_RUNTIME_EVIDENCE_CROSSCHECK_20261025T022935Z.log` records localhost Core :8000 and runtime :8031 connection failures, public /core 404, and catalog execution tools NOT_IMPLEMENTED.
- No artifact supplies a current authenticated Core route, current runtime identity/build hash, isolation proof, or immutable evidence-store proof. Modules remain deliberately NOT WIRED.

**Closure decision**
- The offline boundary-test workstream has reached a useful stopping point. Do not keep adding more shape-only negative tests unless a concrete defect or new interface contract is found.
- Remaining critical path is environmental/integration evidence: (1) current Core authenticated route, (2) current canonical W13 runtime attestation and reachability, (3) OS/network/secret isolation, (4) immutable source snapshot and protected evidence, then (5) wire through the existing canonical route, run authorized live E2E and obtain Cla review + Go independent verification.
- Honest schedule: offline artifact reconciliation and handoff can be closed in a bounded short pass (estimate 1–2 focused hours if no new source inconsistency appears). Live integration/release has no defensible calendar ETA while Core :8000 and runtime :8031 are unreachable and no authorized evidence route exists. It is a dependency-blocked gate, not an amount of coding that Xu can promise to finish by a date.
- To unblock other Works, freeze Work 28's offline boundary scope now; continue only non-blocking documentation/reconciliation. Do not hold unrelated Works waiting for runtime availability. Resume the critical path when fresh authorized Core/runtime evidence is obtainable. No user PC action is requested in this entry.

**Status:** boundary source review PASS; 16-test result Go-reported (not independently rerun); live integration BLOCKED; Work 28 ACTIVE / BLOCKED / NOT RELEASED; seven execution/evidence tools remain NOT_IMPLEMENTED.


### Xu — PC connectivity refresh from user-provided PowerShell output (2026-10-25)
**Evidence source:** user-provided console transcript, not independently executed by Xu.
- Core listener: 127.0.0.1:8000, PID 4548; GET /health returns 404. This proves a listener, not that the intended health route or Core execution API is healthy.
- Execution runtime listener: 127.0.0.1:8031, PID 20504; GET /health returns HTTP 200 and JSON begins {"status":"PASS","service":"execution-host","provider":"W12_REAL_EXECUTION_HO..."}. Runtime is running; full identity/version/build/source hash and authorized invocation are not yet evidenced.
- MCP 8020 listener PID 21584; MCP Build 8030 process PID 11260 is present. Tailscale Funnel routes / and /meeting to 8020, /build to 8030.
- Runtime process command line points to D:\ROOM-HOP-CLEAN\room-meeting-ai\.ai-workspace\sessions\AI-BUILD-GATEWAY-V1\workspace\13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE and python -m execution_host.server. Treat this as a candidate runtime location, not proof of unique/canonical/secure runtime.
**Decision:** update previous blanket “Core/runtime unreachable” finding. Current evidence says the runtime is listening and health responds; Core is listening but /health is the wrong/unconfirmed path (404). The end-to-end Core→runtime authorized execution path remains BLOCKED until the actual Core route and runtime identity/security evidence are verified.
**Next diagnostic:** read-only discovery of Core/runtime route manifests/OpenAPI and exact service metadata; no restart, no direct runtime execution, no tool activation. Keep seven execution/evidence tools NOT_IMPLEMENTED; status ACTIVE / BLOCKED / NOT RELEASED.


### Xu — Core OpenAPI route inventory from Vinh (2026-10-25)
Source: PowerShell output pasted by Vinh; Xu did not execute the query. Core OpenAPI inventory returned 12 routes: GET /global-sources, GET /global-sources/{source_id}, GET /identities, GET /meetings, POST /meetings, GET /meetings/{meeting_id}, POST /meetings/{meeting_id}/close, POST /meetings/{meeting_id}/join, POST /meetings/{meeting_id}/open, POST /meetings/{meeting_id}/paste, POST /meetings/{meeting_id}/start, GET /meetings/{meeting_id}/transcript. No execution/runtime route appears in the published schema. This does not rule out an internal Core-to-W13 call not exposed in OpenAPI; source/config trace is required. Runtime /health freshly reports PASS and build_hash a3ab13f49fd10501588a6da26028b1c147ba7097836884ae39264af49e124012, with current instance ID w13-cbdb24aff30948aaa6d155332541d5bf and PID 20504. Status: Core OpenAPI reachable PASS; runtime health/identity reported PASS; authorized Core-to-runtime path NOT VERIFIED; seven Work 28 execution/evidence tools remain NOT_IMPLEMENTED; Work 28 ACTIVE / BLOCKED / NOT RELEASED. Next: inspect Core source/config and W13 startup/route binding for an internal authorized execution path; read-only, no POST calls, no restart, no direct MCP-to-8031 route.### Xu — PC listener inventory and source grep reviewed (2026-10-25; user-provided pasted outputs)
Source files: user-provided `Pasted text(2).txt` and `Pasted text(3).txt`; Xu inspected the uploaded outputs, did not run commands on the PC.
- Listener inventory at time of capture shows 127.0.0.1 ports 8000 (PID 4548), 8020 (PID 21584), 8031 (PID 20504), and 8051 (PID 4904). Ports 8030, 8040, 8050 are absent from that particular `Get-NetTCPConnection` output. Tailscale Serve/Funnel output routes `/` to 8020, `/meeting` to 8020, and `/build` to 8030. This is a discrepancy requiring a fresh check only if the MCP 8030 connection itself fails; do not assume local :8030 listener from this capture.
- Core OpenAPI route inventory (from Vinh's separate output) contains only identities/global-sources/meetings routes, no execution/runtime endpoint.
- Read-only recursive source grep found canonical active W13 source under `.ai-workspace\sessions\AI-BUILD-GATEWAY-V1\workspace\13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host\server.py`, with `/execute` dispatch, and `wee_bridge.py` that defaults to `http://127.0.0.1:8031` and posts to `/execute`. W13 canonical attestation scripts also exist in workspace 13. Search hits prove source artifacts and intended bridge exist; they do NOT prove Core :8000 imports/calls the bridge or that deployed source matches these files.
- The same grep also returns backup/older staged code and many unrelated Work 09/091 browser workflow routes. Avoid conflating those with Core-to-W13 integration.
- Current conclusion: Core HTTP API is meeting/identity/source adapter; W13 runtime is healthy and has `/execute` source implementation; likely missing/undemonstrated integration is the call path from Work 28 MCP/Core authorization layer into the existing W13 bridge, plus runtime authorization/snapshot/evidence gates. Do not add a new runner or directly expose 8031 through MCP. Next source-level step is inspect the active Core adapter's startup/module/imports and the active WEE/Work 28 gateway wiring to see whether `ExecutionHostBridge` or `execute_work` is referenced. Keep all execution/evidence tools NOT_IMPLEMENTED until proven and tested.
Status: source grep evidence only; no live Core→W13 invocation executed. Work 28 ACTIVE / BLOCKED / NOT RELEASED.


## XU REASSESSMENT — 2026-10-25
**AI ID:** AI-01 / Xu (GPT CEO, coordinator)  
**Decision:** Correct prior wording: do not label the whole system “not connected” merely because the exact Core→W13 execution call path has not yet been proven. Evidence already recorded: MCP 8030 sandbox read/list worked; PC Core :8000 OpenAPI returned HTTP 200 and published 12 management routes; Execution Host :8031 `/health` returned HTTP 200 with runtime enabled and REAL provider; active W13 source grep found `/execute` and `wee_bridge.py` targeting `127.0.0.1:8031/execute`. These are separate PASS findings at transport/readability, Core management API, and runtime liveness layers.
**Remaining uncertainty:** published Core OpenAPI does not expose an execution route, but that alone cannot rule out an internal Core→W13 call. Need source-level trace of active deployed Core adapter and Work 28 gateway/connector, plus proof of trusted WorkContext/authentication, source snapshot binding, runtime identity correlation, isolation and protected evidence. Do not ask Vinh to rerun already completed PC diagnostics unless new contradictory evidence appears.
**Status:** Work 28 remains ACTIVE / NOT RELEASED. Execution/evidence tools remain NOT_IMPLEMENTED pending the actual release gates. Current status is “transport and runtime individually verified; end-to-end authorized execution path not yet demonstrated,” not “the system is not connected.”


## OPERATIONS DECISION — W13 EXECUTION HOST STARTUP / NO REPEATED PC PROBES
**AI ID:** AI-01 / Xu (GPT CEO, coordinator)  
**Date:** 2026-10-25  
**Decision from Vinh:** Treat local port 8031 (W13 Execution Host) as a persistent ROOM service and configure it to start with ROOM; do not allow it to remain stopped and then repeatedly ask for manual PC checks.  
**Operational requirement:** startup dependency must be explicit in ROOM's startup orchestration; readiness/health check once during startup and on actual failure/deployment change; restart policy and logs must be defined. Do not claim the configuration is implemented until the active `start-dev.ps1` (or its actual service supervisor) is inspected and the startup change is made and verified. Keep 8020 during migration; 8030 remains the AI build MCP endpoint.  
**Avoid churn:** Do not ask Vinh to repeat `GET :8031/health` or port-list commands when existing evidence is still valid. Investigate startup wiring from source first; request PC intervention only if a change cannot be applied through the available authorized MCP path.  
**Status:** DECISION RECORDED; implementation/verification of startup wiring remains to be confirmed from the active startup script/service configuration.


### Continuation after ROOM startup — 2026-10-25
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** Work 28 only; MCP 8030 Sandbox-first.

**Fresh evidence read through MCP 8030**
- Work 28 sandbox is present and readable; Work 28 execution contract, envelope mapper, transport arity bridge, connector adapter, and boundary tests were read back.
- The contract validator is explicitly shape validation only; it does not authorize a caller, open files, launch processes, or prove the live Core/runtime route.
- The W13 envelope mapper validates request shape and Work-ID equality, but cannot prove the supplied WorkContext was created by authenticated Core.
- The W27 arity bridge only adapts a nested {work_context, execution_request} envelope to a two-argument transport. It does not itself establish authorization, snapshot integrity, runtime identity, isolation, or protected evidence.
- Connector v54 hard-blocks all seven execution/evidence tools as NOT_IMPLEMENTED before transport; this remains correct while the Core/runtime/security gates are not evidenced.
- Existing offline test source contains 16 integration-boundary test methods. Prior Go report says 16 passed, but Xu did not execute them in this session; this is not an independent PASS.

**Operational update from Vinh**
- Vinh supplied the ROOM startup console log showing Workspace :8010, Gateway :8040, MCP Meeting :8020, Event Listener :8050, Agent Runtime :8051, MCP Build :8030, Execution Host Work 13 :8031, and Dashboard :3000 reported started.
- Treat this as user-provided startup evidence only. It confirms the startup script reported the ports started; it does not prove a fresh runtime identity attestation or authorized MCP→Core→W13 execution E2E.

**Next implementation boundary**
1. Keep the seven execution/evidence tools NOT_IMPLEMENTED and keep sandbox_run_command POLICY_REFUSED.
2. Do not connect MCP directly to localhost:8031 and do not create another execution host.
3. Continue static reconciliation of the active Core adapter/source and canonical W13 bridge; do not wire the pure mapper into the live gateway until the authenticated Core route, trusted WorkContext, immutable snapshot/hash, OS isolation, and protected evidence are proven.
4. Test execution remains BLOCKED in this MCP session because the exposed 8030 tool surface has file operations but no authorized Python/pytest execution tool. Do not claim the existing tests were rerun.

**Status:** Source-contract readback PASS; runtime startup log reported PASS by Vinh; independent execution test NOT RUN; authorized end-to-end execution BLOCKED; Work 28 ACTIVE / NOT RELEASED.


### Fresh W13 security-boundary readback — 2026-10-25
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Source:** Work 13 Sandbox read through MCP 8030; static inspection only.

**Confirmed from canonical source**
- `execution_host/server.py` binds by default to `127.0.0.1:8031`, exposes `GET /health` and `POST /execute`, and constructs `WorkContext(**body["work_context"])` directly from the submitted JSON envelope before invoking the W12 adapter.
- The server source itself shows no HTTP authentication/principal validation on `POST /execute`. The W12 adapter's context validation and the bridge's `authorized is True` check are not substitutes for an authenticated Core boundary if the caller can submit the envelope directly.
- `wee_bridge.py` requires authoritative context fields and blocks when `authorized` is not exactly true, but it does not authenticate the origin of that context. That authority must be established by the caller/Core route.
- `EXECUTION-CURRENT.json` records a historical PASS for `W13-HTTP-REAL-EXECUTE-001`, while also recording that bridge contract tests were written but not executed. This is historical evidence for its stated narrow scope, not proof of a current authenticated Core→W13 path.
- The currently exposed MCP 8030 tools still provide Sandbox file operations and context tools only; there is no execution tool exposed to this session.

**Decision / safety consequence**
- Do not wire the W13 bridge directly into the public MCP connector or treat a caller-provided `authorized` flag as trusted identity.
- Before activation, Core must derive principal and WorkContext from authenticated transport, validate Work authorization, bind the immutable source snapshot/hash, and invoke the canonical W13 path through the existing approved boundary. Runtime isolation and protected evidence must be proven independently.
- No production code changed in this readback; no process was executed; no new PASS is claimed.

**Status:** Static security boundary finding recorded; Work 28 ACTIVE / BLOCKED / NOT RELEASED.


### Priority directive — authenticated Python/pytest E2E — 2026-10-25
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Decision:** Make MCP 8030 → authenticated Core :8000 → canonical W13/W12 execution the sole P0 focus within Work 28.
**Artifact:** `06_EVIDENCE/WORK28_AUTHENTICATED_PYTEST_E2E_INTEGRATION_PLAN_20261025.md`.
**Write/readback:** PASS — artifact written and read back through MCP 8030.
**Root cause confirmed:** Work 28 has a protocol-complete but deliberately unwired execution gateway; v54 service/catalog fail closed as NOT_IMPLEMENTED. Existing envelope/arity adapters are not authentication boundaries. W13 POST /execute source does not show HTTP principal authentication, so direct MCP→W13 wiring is unsafe.
**Immediate work sequence:** locate and pin deployed Core source/revision; identify trusted auth middleware and canonical Work authority; implement/verify Core route and immutable snapshot binding; then inject authenticated CoreExecutionClient into MCP only after negative tests pass. Keep sandbox_run_command POLICY_REFUSED and do not enable unrelated evidence tools prematurely.
**No fake PASS:** no Python/pytest execution was performed in this step; no live E2E PASS is claimed.
**Status:** Plan committed to Work 28 Sandbox through MCP 8030; implementation remains ACTIVE / BLOCKED pending Core source-of-truth and trusted route discovery.


### Offline canonical contract compatibility audit — 2026-10-25
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Action:** Continued Work 28 without PC via MCP 8030 Sandbox; no process or tests were run.

**New concrete finding:** Static readback of Work 13 canonical source shows the current Work 28 mapper is incompatible with W13's dataclasses. Work 28 emits `operation`, `entry_path`, `expected_source_sha256`, `language`, and `work_id` inside `execution_request`, while W13 `ExecutionRequest` accepts `command`, `timeout_seconds`, `collect_artifacts`, and `run_test`. The mapper also checks only `work_context.work_id`, while W13 `WorkContext` requires `work_name`, `workspace_root`, `execution_workspace`, `evidence_root`, and `authorized`. Since W13 `server.py` directly constructs those dataclasses from the body, the current envelope would fail schema construction. This is a source-level deduction, not a live HTTP test.

**Security consequence:** W13 server source has no visible caller-principal authentication on `POST /execute`; `authorized=True` in a submitted context is not proof of who authorized it. W13 request models also do not enforce the Work 28 source hash / immutable snapshot contract. Therefore no direct mapper-to-W13 wiring is safe.

**Evidence:** `06_EVIDENCE/XU_OFFLINE_CANONICAL_CONTRACT_COMPATIBILITY_AUDIT_20261025.md` (written via MCP 8030; awaiting readback verification).

**Decision:** Do not patch W12/W13 from Work 28, do not translate entry_path to caller-controlled argv, and do not activate tools. A versioned, reviewed Core-authenticated contract alignment is required. Keep all seven execution/evidence tools `NOT_IMPLEMENTED`, `sandbox_run_command` `POLICY_REFUSED`, Work 28 `ACTIVE / BLOCKED / NOT RELEASED`.

**Offline work outcome:** Static compatibility audit completed and blocker made precise. Python/pytest execution and live runtime remain NOT RUN / BLOCKED; no test PASS or E2E PASS is claimed.

**Readback verification update:** The new audit file was read back successfully through MCP 8030 (`status=ok`, 4,422 bytes), and the appended journal entry was also read back (`status=ok`). This verifies Sandbox persistence only, not code execution or runtime integration.


### Xu — Independent review of Co's W28↔W13 compatibility guard
**Ngày:** 25/10/2026 (UTC+7)  
**Chức danh:** AI-01 GPT CEO / Quân sư LAB

- Đọc trực tiếp qua MCP 8030 mã guard, mapper và hai bộ test Co vừa thêm/sửa.
- Phát hiện 2 test âm tính có thể pass sai lý do: test_work_id_mismatch và test_work_context_empty_work_id dùng context thiếu trường W13, nên lỗi bị chặn ở bước thiếu trường trước khi kiểm tra đúng điều kiện được đặt tên.
- Đã sửa guard để kiểm tra rõ Work ID rỗng và Work ID của context không khớp request; bổ sung 2 regression test và sửa 2 test boundary để assert mã lỗi cụ thể.
- MCP 8030 trả status=ok cho ba lần ghi: compatibility guard, compatibility tests, integration-boundary tests.
- **Chưa chạy Python/pytest**; không claim test PASS. Đây là source change + static review.
- Mapper vẫn fail-closed vì hợp đồng request W28 chưa tương thích ExecutionRequest W13. Không sửa W12/W13, không bật execution tool, không chạy E2E.
- Gate giữ nguyên: bảy execution/evidence tools NOT_IMPLEMENTED; sandbox_run_command=POLICY_REFUSED; Work 28 ACTIVE / BLOCKED / NOT RELEASED.
- Evidence: 06_EVIDENCE/XU_INDEPENDENT_REVIEW_CO_COMPATIBILITY_FIX_20261025.md.
- Bước kế tiếp: hợp đồng Core có xác thực, ủy quyền server-side, snapshot bất biến + SHA-256, runtime identity và evidence bảo vệ; sau đó mới chạy kiểm thử runtime và QA độc lập.


### Xu — Integration trace v54 → Authorized Adapter → W13/W12
**Ngày:** 25/10/2026 (UTC+7)  
**Chức danh:** AI-01 GPT CEO / Quân sư LAB

- Đọc qua MCP 8030 các đoạn nguồn trả về được của v54 gateway, service/catalog, execution contract, authorized adapter và W13 server/models.
- Xác nhận gateway v54 vẫn tạo payload legacy gồm entry/args; contract hash-bound v1 yêu cầu entry_path + expected_source_sha256 và từ chối trường ngoài hợp đồng.
- Xác nhận adapter có các interface injection nhưng header nói rõ chưa nối vào MCP/service và không tự xác thực caller, đọc/hash source, launch process hoặc attestation evidence.
- W13 ExecutionRequest hiện chỉ nhận command, timeout_seconds, collect_artifacts, run_test; WorkContext yêu cầu thêm các trường context. Server tạo dataclass trực tiếp từ body. Không được chuyển entry_path sang command tùy ý.
- Đoạn W13 POST /execute đọc được không thể hiện kiểm tra caller principal ở handler; đây là quan sát tĩnh, không kết luận về bảo vệ mạng ở nơi khác. W13 startup cấu hình W12ExecutionAdapter(allow_processes=True), nên cần đường Core xác thực và invocation cố định trước khi nối.
- Một số lần gọi sandbox_read trả object rỗng; lần đọc authorized adapter bị safety checker chặn. Không tìm cách lách và không coi đó là bằng chứng mất file/hỏng Sandbox. Báo cáo chỉ dựa trên nội dung đã trả về thành công.
- Đã ghi báo cáo XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md qua MCP 8030. Chưa chạy test hoặc runtime; cần readback xác minh.
- Gate không đổi: 7 tool NOT_IMPLEMENTED, sandbox_run_command POLICY_REFUSED, Work 28 ACTIVE / BLOCKED / NOT RELEASED.


### Readback verification — Xu integration trace
- Sau khi ghi báo cáo XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md và append nhật ký, Xu đọc lại cả hai qua sandbox_read_probe trên MCP 8030.
- Báo cáo trả status=ok, size_bytes=5829; nội dung có phần contract mismatch và tuyên bố rõ không claim PASS.
- Nhật ký trả status=ok, size_bytes=51891; phần append mới hiện diện ở cuối tệp.
- Cập nhật này chỉ xác nhận ghi/đọc lại tệp, không phải xác nhận test hay runtime.


## 2026-10-25 — Bổ sung bằng chứng runtime từ Vinh (PowerShell)

**Người cung cấp bằng chứng:** Vinh. **Người ghi nhật ký:** Xu (AI-01 GPT CEO / Quân sư LAB). **Phạm vi:** đối chiếu trạng thái dịch vụ trên máy; không coi đây là xác nhận tích hợp Work 28.

### Dữ liệu quan sát được trong đầu ra được cung cấp
- TCP listener `127.0.0.1:8031`, PID `1276`; listener `127.0.0.1:8000`, PID `28868`.
- `GET http://127.0.0.1:8031/health` trả `status=PASS`, `service=execution-host`, `provider=W12_REAL_EXECUTION_HOST`, `runtime_provider=REAL`, `runtime_enabled=true`, `runtime_allow_processes=true`.
- Runtime identity trả `instance_id=w13-7bba62a5741b45f0987219d65c13caef`, `build_hash=a3ab13f49fd10501588a6da26028b1c147ba7097836884ae39264af49e124012`, `started_at=2026-10-25T03:09:30.928103+00:00`, PID `1276`, platform `Windows-10-10.0.19045-SP0`, bind `127.0.0.1:8031`.
- `GET http://127.0.0.1:8000/health` trả `404 Not Found`.
- Danh sách tiến trình có nhiều `python.exe` và PowerShell, nhưng đầu ra đã rút gọn command line; chưa thể gán chắc PID nào cho module/build cụ thể chỉ từ phần này.

### Diễn giải có giới hạn
1. Có bằng chứng do người dùng cung cấp rằng listener :8031 đang phản hồi health với runtime thật được cấu hình bật và có identity/build hash.
2. Đây **chưa phải** bằng chứng độc lập rằng build hash khớp với source revision đã duyệt, runtime identity được xác minh bởi caller tin cậy, hay Core đã xác thực và ủy quyền yêu cầu trước khi dispatch.
3. `404` ở `/health` trên :8000 chỉ cho thấy route đó không tồn tại/không được phục vụ tại URL đã thử; không kết luận Core không hoạt động. Cần xác định health/readiness route đúng từ source/config hoặc route được công bố, không đoán endpoint.
4. Vì :8031 bind `127.0.0.1`, nó là listener loopback trên máy này; không tự chứng minh khả năng truy cập từ MCP 8030 hoặc từ máy khác.
5. `runtime_allow_processes=true` là một cấu hình rủi ro cần kiểm soát bằng xác thực, phân quyền, command allowlist, cô lập, giới hạn thời gian/đầu ra và evidence integrity trước khi nối vào Work 28.

### Quyết định / gate
- **PASS có giới hạn:** nhận diện được phản hồi health và runtime identity trong đầu ra do Vinh cung cấp.
- **NOT VERIFIED:** Core health/readiness route; process-to-source/build mapping; runtime identity attestation; caller authentication/authorization; Core→W13 routing; immutable source snapshot/hash binding; execution evidence integrity; live E2E.
- **Không kích hoạt** execution tools và không tuyên bố pytest/E2E PASS.
- Work 28 vẫn **ACTIVE / BLOCKED / NOT RELEASED**. Giữ các execution tools chưa triển khai ở trạng thái fail-closed cho đến khi các gate trên có bằng chứng kiểm chứng được.

### Bước tiếp theo
Dùng MCP/Sandbox để tiếp tục đối chiếu tĩnh route/config của Core và W13; không yêu cầu Vinh chạy thêm lệnh PC chỉ để tiếp tục công việc tĩnh. Chỉ khi cần xác nhận live route hoặc authorized E2E mới ghi rõ đó là gate phụ thuộc môi trường được ủy quyền.

## 2026-10-25 — Static review W13 `/execute` boundary and Work 28 compatibility

**Người thực hiện:** Xu (AI-01 GPT CEO / Quân sư LAB). **Nguồn:** Work 13 và Work 28 Sandbox qua MCP 8030. **Phạm vi:** đọc source tĩnh; không chạy code/pytest và không gọi endpoint thực thi.

### Kết quả mới
- Đọc `server.py`, `models.py`, `w12_adapter.py`, `identity.py` của Work 13; đọc lại service/catalog/gateway/contract/authorized adapter liên quan của Work 28.
- Xác định trong `server.py` handler POST `/execute` đang parse body rồi tạo trực tiếp `WorkContext(**body["work_context"])` và `ExecutionRequest(...)`; phần handler được đọc không lấy authenticated principal hoặc gọi Core authorization. Trường `authorized` nằm trong payload caller. Do đó không thể xem trường này là bằng chứng quyền truy cập; phải xác minh có trusted boundary khác bảo vệ route trước khi cho phép tích hợp.
- W13 request model dùng `command: tuple[str, ...]`, trong khi Work 28 contract v1 dùng `entry_path`, `operation`, `expected_source_sha256`; gateway v54 vẫn phát `entry`/`args`. Ba hợp đồng không tương thích để wire trực tiếp.
- W13 adapter trả `cleanup={}` và đoạn `execute_work` đã đọc không gọi `cleanup()`; đây không chứng minh cleanup thực tế thất bại, nhưng không đáp ứng yêu cầu Work 28 phải có cleanup được xác minh.
- `/health` trả runtime identity/build hash có ích nhưng chưa độc lập chứng minh source tree đang chạy đúng revision đã duyệt hoặc identity được xác thực từ bên tin cậy.
- Core `:8000/health` 404 không đủ kết luận Core chết; cần xác định route đúng từ source/config.

### Artifact
- Đã ghi báo cáo: `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_W13_BOUNDARY_REVIEW_20261025.md` (MCP sandbox_write trả `status=ok`).

### Quyết định
- Không wire adapter trực tiếp, không bật các tool thực thi; tiếp tục giữ fail-closed.
- Bước tiếp theo: đọc source/config Core để xác định route health/readiness và trusted caller/auth boundary, sau đó lập bản đồ hợp đồng Core→W13; chỉ sửa source sau khi có đủ source liên quan và testable design.
- Không tuyên bố pytest, runtime source/build correlation hoặc live E2E PASS. Work 28 vẫn ACTIVE / BLOCKED / NOT RELEASED.
### Addendum static review — Work 02 / Work 12
- Work 02 authorization wrappers were inspected but are not shown in the inspected W13 `/execute` path; cannot count their existence as active protection.
- Work 12 `wee/bridge/real_host.py` inspected `execute()` calls `subprocess.run(...)` without a `timeout=` argument. W13's accepted timeout value does not itself enforce a runtime deadline on this path. Require canonical runtime timeout + process-tree termination/cleanup evidence before release.
- Added these findings to `06_EVIDENCE/XU_W13_BOUNDARY_REVIEW_20261025.md`. No runtime was launched and no pytest/E2E PASS claimed.

### Xu — Authorization boundary reconciliation (2026-10-25, UTC+7)
- Read Work 02 authorization prototypes, Work 13 WEE→:8031 bridge status, and Work 27 HTTP transport/contract through MCP 8030.
- Work 02's inspected boundary authorizes meeting participation; the unified gate's `sandbox:pytest` check is a Sandbox prototype, not evidence of a deployed Core-authenticated execution route.
- Work 13 bridge documents the two-part W13 envelope but marks live :8031 and tests NOT RUN in that evidence context.
- Work 27 transport is a thin HTTP client; its V0 contract differs from Work 28's hash-bound entrypoint contract.
- Wrote `06_EVIDENCE/XU_AUTH_BOUNDARY_RECONCILIATION_20261025.md` via MCP 8030. This records static source evidence only.
- No code changed; no Python/pytest run; no live endpoint called. No PASS claimed.
- Decision unchanged: seven execution/evidence tools remain NOT_IMPLEMENTED; `sandbox_run_command` remains POLICY_REFUSED; Work 28 ACTIVE / BLOCKED / NOT RELEASED.
- Next action: trace the actual deployed Core/authenticated adapter route and determine whether server-derived principal + Work authorization precedes W13 `/execute`; do not wire directly to localhost or trust caller-supplied authorization.

## 2026-10-25 — Xu continuation: current Sandbox runtime capability check
**AI identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Action:** Inspected the exposed MCP 8030 tool inventory and current Work 28/Work 13 Sandbox inventories without PC access.
- MCP 8030 exposes Sandbox file operations and context/listing tools in this session; it exposes no Python/pytest/command execution tool.
- Work 28 contains Python and pytest source plus historical pycache artifacts; this does not prove current runtime execution.
- Work 13 inventory includes a staged Python 3.14 interpreter file under its workspace. Inventory alone does not prove runnable dependencies, isolation, or authorized execution for Work 28.
- Reconciled with current Core/W13 reports: direct MCP→W13 execution remains unsafe because caller authentication and Core-derived WorkContext are not proven, and Work 28/W13 request schemas differ.
- Wrote MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_CONTINUATION_RUNTIME_CAPABILITY_CHECK_20261025.md. No production source was changed; no process, Python, pytest, or HTTP execution endpoint was invoked.
- Gate remains: sandbox_run_command=POLICY_REFUSED; seven execution/evidence tools=NOT_IMPLEMENTED; Work 28 ACTIVE / BLOCKED / NOT RELEASED.
- Next required capability is a narrow, authenticated RUN_TESTS route backed by Core-derived authorization, immutable source hash, approved isolated runtime, bounded timeout/cleanup, and protected run evidence. Do not claim test PASS from file inventory or readback.

## Xu independent review of W13 auth fix — 2026-10-25
- Read GitHub diffs for fix commit `1f0e6916bf317b0e5bebed819f100ec08ac35945` and evidence commit `ca782f59bf64257696db4be5f40ea643f38757d0`.
- Confirmed source adds a fail-closed token check before request-body parsing/host invocation, using `hmac.compare_digest`.
- Found remaining gaps: the new regression test does not issue HTTP POST to the real handler; it does not assert HTTP 401 or that the host is not invoked. After token match, the handler sets `authorized=True` without visible per-work/operation authorization from Core. `serve()` still defaults to no token and the direct module entrypoint calls `serve()` without injection.
- Created `06_EVIDENCE/XU_INDEPENDENT_REVIEW_W13_AUTH_FIX_20261025.md` in Sandbox. MCP write returned status=ok.
- No tests, live HTTP calls, runtime dispatch, deployment checks, or E2E were executed. No PASS declared. Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.


## Xu independent review — W13 auth + per-Work allow-list + HTTP boundary tests (2026-10-25)
- Reviewed GitHub diffs for commits `5d52cf2e6b4e4e5d758327c5925ea7c5345a1822` and `db3ff41b6ee433d0e3b57db6ed34d9d295c88695`.
- Positive: token check uses constant-time comparison; failed auth is rejected before body parsing; allow-list rejects missing/invalid config and unlisted Work; HTTP tests POST to a real ephemeral loopback ThreadingHTTPServer and use a RecordingHost that launches no process.
- Remaining P0 configuration gap: `serve()` accepts explicit auth_token/authorized_works arguments but `if __name__ == '__main__': serve()` still supplies neither. The proposed `ROOM_HOP_EXECUTION_AUTH_TOKEN` and `ROOM_HOP_AUTHORIZED_WORKS` environment variables are not read in the inspected diff. Setting env vars alone does not arm this startup path; it remains fail-closed.
- Confirm canonical Work ID convention before deployment: tests use `W28`, while Work 28 Sandbox ID in the current project evidence is `28`. Do not normalize silently.
- Allow-list is process-global, not per-principal authorization. Suitable only if explicitly intended as a narrow service-wide Work allow-list; multiple caller principals require Core-bound authorization.
- Verify test import provenance resolves `execution_host.server` to the intended canonical Work 13 source, not a duplicate package.
- Combined status calls available in this review returned no status entries; CI #126/#127 remain claims supplied by Vinh, not independently certified here.
- Wrote `06_EVIDENCE/XU_INDEPENDENT_REVIEW_W13_AUTHZ_HTTP_V2_20261025.md` via MCP 8030; write status=ok. No tests, deployed HTTP calls, or E2E were run. Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.


## 2026-10-25 — Xu: MCP 8030 restored, pytest path checked
- MCP 8030 file operations recovered: `sandbox_list_works` returned 53 Works; Work 28 list and test-plan readback returned `status=ok`.
- Current exposed MCP 8030 inventory has 17 tools and no command/Python/pytest execution tool. Thus no pytest was run; do not claim PASS.
- Work 28 test plan's canonical local contract command is `python -m unittest discover -s 05_TEST -t . -v`; approved-runner G3 and live E2E remain BLOCKED.
- Evidence written: `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_SANDBOX_PYTEST_PATH_DIAGNOSTIC_20261025.md`.
- Decision: MCP file access PASS; pytest execution path BLOCKED / NOT RUN; Work 28 remains ACTIVE / BLOCKED / NOT RELEASED. Next: use only authenticated Core -> canonical W12/W13 RUN_TESTS with immutable source/hash, bounded execution/cleanup and captured evidence. No direct unauthenticated W13 bypass.