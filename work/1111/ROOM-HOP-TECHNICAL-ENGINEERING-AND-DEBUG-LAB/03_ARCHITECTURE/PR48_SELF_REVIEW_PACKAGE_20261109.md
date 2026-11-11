# PR #48 SELF-REVIEW PACKAGE — W1111 C06

- Prepared by: Co — Coder under Cla (CTO)
- Date: 2026-11-09 (UTC+7)
- Review target: draft PR #48, branch `work/w1111-core-execution-authority-v1-2`
- Evidence basis: PR diff and branch source readback; tests listed below. This is a test-coverage inventory, not a security certification.

## 1. Existing tests observed

| Area | Existing test(s) / source evidence | Current coverage | Gap / risk |
|---|---|---|---|
| Caller-supplied work_id / authorized spoofing | `test_old_caller_supplied_work_context_is_rejected`; `test_core_grant_is_obtained_before_host_and_workcontext_is_not_forwarded`; `test_core_denial_prevents_host_network_call`; `test_wrong_bearer_grant_is_denied_before_execution`; `test_bad_credential_and_wrong_work_fail_closed`; `test_wrong_purpose_and_invalid_work_id_rejected`; `test_wrong_token_and_wrong_grant_work_fail_closed` | Positive/negative in-process boundary tests exist; forged body fields are rejected/ignored at W13 boundary; wrong Work/token denied | Add HTTP-level tests for forged `work_id`, `authorized=true`, workspace/evidence roots and wrong route Work all together; confirm no process invocation and stable 4xx |
| Grant expiry | `get_grant_status`/validation implementation and deployment contract describe active/expired/revoked | No expiry-specific test function found in `tests/test_execution_authority.py` | HIGH: no test proves expired token is denied at W13 on every call; add deterministic clock injection or short TTL test |
| Grant replay / reuse | Token validation and run-record tests exist; `test_run_record_links_grant_source_exit_and_evidence` | Tests one grant → one run and revocation; no replay/second-use test | HIGH / policy decision: active short-lived grant may be reusable. Define intended single-use vs bounded multi-run semantics, then test duplicate run/replay and revoked/expired reuse |
| Grant token leakage | Existing `test_secret_redaction` in older host tests covers generic output redaction; deployment doc says grant token must stay in WEE memory | No test scans WEE/W13 stdout, stderr, exception, blocker, FINAL_RESULT, Core journal or CI logs for the exact grant token | HIGH: add sentinel token and assert it is absent from every log/evidence/journal/error surface |
| Path traversal / symlink / reparse | `test_work_paths_cannot_escape_work_root`; `test_workspace_snapshot_rejects_symlink` | Work policy path escape and snapshot symlink rejection covered; symlink test may skip if runner cannot create symlink | HIGH: no explicit `..` request path test, evidence-root traversal test, Windows junction/reparse-point test, or race/symlink swap between snapshot and process start |
| source_sha256 drift | `test_workspace_snapshot_is_deterministic_and_content_sensitive`; integration test computes a snapshot and passes it through the normal grant flow | Helper determinism/content sensitivity and same-snapshot happy path covered | HIGH: no test issues grant at hash A, mutates workspace to hash B before W13 execution, and proves denial before process start; no race-window test |
| Core RUN_RECORDED failure | Deployment document states W13 downgrades result and rewrites final evidence to BLOCKED when Core recording fails | No test simulates Core `record_run` returning 5xx/timeout/invalid response after successful W12 execution | HIGH: add test proving final result + FINAL_RESULT.json are BLOCKED, blocker is stable, and no PASS is exposed |
| Child process cleanup | W12 `test_real_host_enforces_execution_timeout`; `test_core_grant_to_w12_real_host_and_append_only_run_record`; `test_full_core_wee_w13_w12_execution_and_core_run_record` assert cleanup metadata | Timeout and cleanup flag covered for a process; integrated path asserts process-tree cleanup verified | MEDIUM: no explicit descendant-spawn fixture in the reviewed PR test files to prove grandchild termination on Windows Job Object/reparse edge cases |
| 30-second maximum | WEE bridge tests send `timeout_seconds=30`; deployment doc states one pytest command and 30-second W12 timeout | Happy-path 30-second value is exercised | HIGH: no explicit negative test for 30.001/31 seconds, grant max_timeout_seconds above 30, missing/negative/NaN timeout, or timeout clamping at every boundary |

## 2. Test files inspected

| File | Tests found |
|---|---|
| `tests/test_execution_authority.py` | `test_authenticate_and_issue_work_scoped_grant`; `test_bad_credential_and_wrong_work_fail_closed`; `test_wrong_purpose_and_invalid_work_id_rejected`; `test_wrong_token_and_wrong_grant_work_fail_closed`; `test_revocation_is_append_only_and_effective`; `test_run_record_links_grant_source_exit_and_evidence`; `test_hash_chain_detects_tampering`; `test_work_paths_cannot_escape_work_root`; `test_http_grant_flow_is_authenticated_and_work_scoped`; `test_unconfigured_authority_returns_503` |
| `tests/test_execution_host_authority.py` | `test_workspace_snapshot_is_deterministic_and_content_sensitive`; `test_workspace_snapshot_rejects_symlink`; `test_nested_test_failure_propagates_to_top_level`; `test_missing_nested_test_entrypoint_blocks_overall_pass`; `test_primary_failure_is_not_overwritten_by_nested_test_pass` |
| `tests/test_core_http_main.py` | `test_core_http_entrypoint_keeps_meeting_api_and_fails_closed_without_authority` |
| `13/EXECUTION-HOST-INFRASTRUCTURE/05_TEST/test_core_grant_host_integration.py` | `test_core_grant_to_w12_real_host_and_append_only_run_record`; `test_old_caller_supplied_work_context_is_rejected`; `test_wrong_bearer_grant_is_denied_before_execution` |
| `13/EXECUTION-HOST-INFRASTRUCTURE/05_TEST/test_core_wee_w13_w12_e2e.py` | `test_full_core_wee_w13_w12_execution_and_core_run_record` |
| `13/EXECUTION-HOST-INFRASTRUCTURE/05_TEST/test_wee_8031_bridge.py` | `test_core_grant_is_obtained_before_host_and_workcontext_is_not_forwarded`; `test_core_denial_prevents_host_network_call`; `test_missing_service_credential_blocks_without_network`; `test_blocked_host_response_is_not_promoted`; `test_core_network_error_blocks_before_host`; `test_host_network_error_blocks`; `test_noncanonical_work_and_non_pytest_operation_blocked` |
| `12/WORK-EXECUTION-ENVIRONMENT/05_TEST/test_real_execution_host.py` | `test_real_host_requires_explicit_enable`; `test_real_host_isolates_bound_workspace`; `test_missing_external_adapters_are_explicit`; `test_real_host_refuses_process_when_process_permission_is_off`; `test_real_host_enforces_execution_timeout`; `test_real_host_does_not_forward_unapproved_environment_secrets` |

## 3. Additional caution

- The W12 unit-test fixture still constructs internal `WorkContext(authorized=True)`. This is not by itself proof of production authorization; PR #48's W13 HTTP boundary is intended to reject caller-supplied WorkContext/`authorized` fields and construct internal context only after Core grant validation.
- A source-level claim that record failure downgrades to BLOCKED is not accepted as test evidence until the failure branch is exercised.
- A test that checks a hash helper's sensitivity is not equivalent to a grant-to-execution TOCTOU test.
- A process timeout test is not equivalent to a Windows descendant-process/job-object cleanup test.

## 4. Recommended additions before independent acceptance

1. Deterministic grant expiry + replay policy tests.
2. Grant-token sentinel scan across stdout/stderr/blocker/FINAL_RESULT/Core journal.
3. W13 request path traversal and Windows reparse/junction rejection tests.
4. Grant hash A → mutate to B → execution denied before W12 invocation.
5. Core run-record 5xx/timeout after successful process → final BLOCKED evidence.
6. Explicit descendant process tree cleanup on Windows.
7. Timeout boundary tests at 30 seconds and above.

**Disposition:** static test-coverage review complete; identified material missing negative tests. No test was executed in this review. READY FOR CLA REVIEW as a coverage package, not as a security PASS.
