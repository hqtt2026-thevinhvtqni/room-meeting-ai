# Work 28 gateway contract reconciliation

Date: 2026-10-25
Reviewer: Xu (AI-01)
Scope: static source review only; no runtime validation.

## Finding
The execution gateway interface is inconsistent with the strict execution contract. The gateway currently accepts script/command and args and emits RUN_COMMAND. The strict contract requires entry_path and expected_source_sha256, permits RUN_SCRIPT or RUN_TESTS, and rejects inline code and arbitrary command arguments.

The service currently returns NOT_IMPLEMENTED for tools whose catalog status is NOT_IMPLEMENTED before provider dispatch. Keep that status and fail-closed behavior unchanged.

## Required next steps
1. Align gateway inputs and requests to the strict hash-bound contract.
2. Add tests for request shape, path/hash/operation validation, Work authorization, and rejection before submission.
3. Verify lifecycle authorization for status, result, cancellation, artifacts, evidence, and handoff.
4. Obtain CI run evidence, then validate against the authorized canonical runtime and perform end-to-end tests.
5. Only after all gates pass may a separately reviewed change bind the gateway and change catalog status.

## Status
Static mismatch confirmed. Runtime not wired. Tests not run in this session. No PASS claimed.

## Follow-up implementation evidence — 2026-10-25

Two staged files were added on this branch after the static finding:

- `04_CODE/mcp8020_strict_execution_gateway_v1.py` — commit `0935bc7b3838cf5bc5e1ce8152a2b06daef19112`.
- `05_TEST/test_mcp8020_strict_execution_gateway_v1.py` — commit `b265230c1393ca10fd1f7639466b05fd3d35d6c1`.

The adapter validates the narrow request envelope before calling an injected `submit(request)` client. The accompanying tests cover accepted request forwarding, rejection-before-submit for malformed/forbidden fields, source/Work binding in the shape-level PASS guard, and non-empty test summaries.

### Explicit integration boundary

This is a staged adapter, **not a replacement for** `mcp8020_execution_gateway_v54.py`. It does not implement the seven v54 execution/evidence handler names and must not be passed to `V54Service.bind_execution_gateway()`. The v54 catalog schemas still expose the older `script`/`command` shapes, and the service still short-circuits every `NOT_IMPLEMENTED` tool before dispatch. These remain known blockers; no catalog status was changed.

### Verification status

- Source files committed: DONE.
- Unit tests authored: DONE.
- Unit tests executed: NOT VERIFIED in this session.
- GitHub Actions run/status for commit `b265230c1393ca10fd1f7639466b05fd3d35d6c1`: no run/status was returned by the queried endpoints. This is not a PASS and does not establish that Actions did not run, because the workflow-run connector query is limited to pull-request-triggered runs.
- Live Core :8000 → canonical W12/W13 runtime route, authorization, source snapshot/hash binding, process-tree cleanup, and E2E: NOT VERIFIED.
- Execution catalog: remains `NOT_IMPLEMENTED`.

## Next bounded tasks

1. Add the strict contract as a separately versioned catalog schema or a deliberate catalog migration; do not silently change v54 public schemas.
2. Add explicit regression coverage proving all seven execution/evidence tools remain `NOT_IMPLEMENTED` even when a gateway object is injected, until an approved activation gate is introduced.
3. Run the branch workflow through an observable GitHub Actions run and preserve the run URL/result as evidence.
4. Continue the canonical runtime attestation and security/E2E gates through the existing W12/W13 route; do not create a second execution host.

## CI regression run — 2026-10-25

The initial CI run exposed a mismatch in the test fixture: two path cases used raw strings containing the literal sequences `\\n` and `\\x7f`, rather than actual newline/DEL control characters. The contract validator was strengthened to reject all ASCII control characters (U+0000–U+001F and U+007F); the test cases were corrected to contain the actual characters.

- Validator fix commit: `93d977c249e80d2033344a966dd7b8e13f6c9a76`.
- Test-fixture correction commit: `1d8a48c544842d4e566a74c2684ec83d577cbd13`.
- GitHub Actions run: [run 40149449011](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40149449011).
- Final workflow conclusion: **success**.
- Test output: `Ran 171 tests`; `OK (skipped=4)`.

Interpretation: the Work 28 branch's automated unit/regression suite passed at commit `1d8a48c544842d4e566a74c2684ec83d577cbd13`, with four tests skipped. This verifies repository-level tests only. It does **not** verify live Core/runtime integration or authorize activation of execution tools. A checkout post-job warning about the repository's `.gitmodules` entry was logged, but the workflow's final conclusion was success.

Execution tools remain `NOT_IMPLEMENTED` pending canonical runtime, authorization, source-hash binding, cleanup, and end-to-end evidence.

## Versioned contract migration staged — 2026-10-25

To avoid silently changing the public v54 catalog, a separate draft execution catalog was added:

- `04_CODE/mcp8020_execution_catalog_v1.py` — commit `6bc20a64de1529409df8515c500863a6e8957927`.
- `05_TEST/test_mcp8020_execution_catalog_v1.py` — commit `801a340b3dd33b6252dfed9b4750ace72895b9dc`.

The staged v1 catalog defines seven future execution/evidence tool schemas. The two run operations require Work ID, Work-relative entry path, and lowercase SHA-256 source binding. The arbitrary `sandbox_run_command` shape is intentionally absent from the staged v1 catalog; the existing v54 public catalog remains unchanged. All staged v1 entries are hard-coded `NOT_IMPLEMENTED`; the module is not registered with MCP and cannot activate execution.

The new test file checks seven unique tools, fail-closed statuses, closed schemas, required hash binding, forbidden free-form execution fields, and the explicit staged rename from `sandbox_run_command` to `sandbox_run_tests`.

- CI run for the catalog module alone: [40149717872](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40149717872) — success on commit `6bc20a64de1529409df8515c500863a6e8957927`. That run occurred before the new catalog test file was committed, so it does not validate the new tests.
- CI run including the new catalog test file: [40149729939](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40149729939) — launched for commit `801a340b3dd33b6252dfed9b4750ace72895b9dc`; result must be checked before reporting its final status.

This is schema staging and repository-level validation only. It does not satisfy Core authorization, source snapshot/hash verification, canonical W12/W13 runtime identity, process-tree cleanup, or live E2E. No execution tool is enabled.

### CI result for staged v1 catalog tests

- Run: [40149729939](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40149729939)
- Commit tested: `801a340b3dd33b6252dfed9b4750ace72895b9dc`
- Conclusion: **success**
- Log: `Ran 178 tests`; `OK (skipped=4)`.
- The five new `test_mcp8020_execution_catalog_v1` cases all passed, including closed schemas, hash-bound run requests, seven unique entries, all entries remaining `NOT_IMPLEMENTED`, and explicit absence of the legacy arbitrary-command tool in the staged v1 catalog.

This passing run validates the staged schema module and repository test suite only. It is not a live MCP registration, Core/runtime integration, or authorization/E2E PASS.
