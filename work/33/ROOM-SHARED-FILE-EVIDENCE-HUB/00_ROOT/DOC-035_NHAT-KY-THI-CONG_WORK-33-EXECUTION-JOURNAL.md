# DOC-035 — NHẬT KÝ THI CÔNG WORK 33
# WORK 33 EXECUTION JOURNAL

- Work ID: W33
- Work name: ROOM-SHARED-FILE-EVIDENCE-HUB
- Status: ACTIVE / SOURCE INVESTIGATION
- Official journal: This file is the single execution journal for Work 33 on GitHub main.
- Timezone: Asia/Ho_Chi_Minh (+07)

---

## 2026-11-26 — Core identity, Work binding and execution authority trace

- **Activity:** READ → TRACE → ANALYZE → DECIDE → BUILD (evidence recording) → VERIFY.
- **Scope:** GitHub main source snapshot; tree SHA `c292956938c149f4c3f68c8c718c8caeb190f31f`.
- **Methods:** Read-only fetch of Core HTTP entrypoint/adapter, identity resolution, governance, Work authority resolver, Execution Host request boundary, deployment contract and related test.
- **Evidence:** `06_EVIDENCE/DOC-001_CORE_AUTHORITY_SOURCE_TRACE_ADDENDUM.md`.
- **Findings:**
  1. Identity registries and message identity resolution are not caller authentication.
  2. `wee/authority.py` resolves Work binding from local JSON but does not authenticate a principal or authorize a Cloud Drive action.
  3. Inspected Execution Host path still accepts caller-supplied `WorkContext.authorized`; no Core grant validation was found in the inspected handler/bridge path.
  4. `tests/test_core_http_main.py` expects a 503 execution-grant route, but the inspected Core entrypoint/HTTP adapter do not show that route. This is a source/test discrepancy, not a confirmed test failure.
- **Decision:** Keep Cloud Drive authorization fail-closed. Do not implement against guessed Core routes, claims, token formats or key URLs. Do not treat WorkBinding, registry membership, or `authorized=true` as authenticated authority.
- **Safety boundary:** No code/runtime/configuration changes, no secrets accessed, no deployment or port changes.
- **Verification:** GitHub evidence file written and read back from main; content length 5,962 characters. Runtime Core and Host NOT VERIFIED. Pytest NOT RUN. No PASS claimed.
- **Sandbox sync:** BLOCKED — ROOM-HOP Sandbox MCP returned UNAVAILABLE / connection failed. GitHub main is the evidence location for this entry until Sandbox connectivity is restored.
- **Next:** Restore Sandbox sync; inspect complete execution-authority implementation and test fixtures; run source-matched tests in authorized isolated environment; verify runtime routes read-only; then design the concrete Core-backed Cloud Drive Authorizer.

## 2026-11-26 — W1111 Execution Authority V1.2 feature-branch trace

- **Activity:** READ → TRACE → ANALYZE → DECIDE → BUILD (evidence recording) → VERIFY.
- **Scope:** Read-only inspection of branch `work/w1111-core-execution-authority-v1-2`; exact blob SHAs and source findings are recorded in `06_EVIDENCE/DOC-002_W1111_EXECUTION_AUTHORITY_V1_2_BRANCH_TRACE.md`.
- **Findings:** The feature branch contains Core grant service, execution-grant HTTP routes mounted by `create_http_app()`, and an Execution Host handler that validates bearer grants online and restricts execution to pytest_run. This resolves the earlier main-vs-feature-branch source discrepancy: the implementation is on the W1111 branch, not established on main by the prior trace.
- **Defect:** The test explicitly issues a grant whose policy source hash is `"a" * 64`, submits `"b" * 64` to the run-record endpoint, and asserts HTTP 200. `record_run()` validates hash syntax but does not compare it with a source digest pinned to the grant. Static defect confirmed; no runtime exploit claim.
- **Integration gap:** `execution_host/wee_bridge.py` still uses the legacy WorkContext/`authorized=true` request and does not provide grant ID, purpose or bearer token required by the new Host handler. The Core and Host pieces are therefore not demonstrated end-to-end through the inspected WEE bridge.
- **Additional note:** Host `/health` may report status PASS while Core authority is unconfigured; readiness must separately require `core_authority_configured=true` and a successful authority probe.
- **Decision:** Do not adopt the feature branch or implement the Work 33 Core adapter yet. Keep `UnconfiguredAuthorizer` fail-closed. Route the source-hash defect and bridge mismatch to W1111 owner; require immutable grant-bound source hash, negative tests, bridge adaptation, exact branch/PR reconciliation and independent QE.
- **Safety boundary:** No code changes, test execution, runtime probe, secret access, merge, deployment or configuration change. Pytest NOT RUN; Core :8000 and Host :8031 NOT VERIFIED; no PASS claimed.
- **GitHub evidence:** DOC-002 created on main in commit `771f0dbc01946037c147c1f6fd4d8303370858e1`. Read-back verification follows.
- **Sandbox sync:** Still BLOCKED from prior Sandbox MCP unavailability; GitHub main remains temporary evidence location.
- **Next:** W1111 owner correction and source-matched validation; reconcile branch/PR state; then re-evaluate Core-backed Cloud Drive Authorizer contract.
