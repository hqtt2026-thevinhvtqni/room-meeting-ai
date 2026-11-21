# W118-13 / W118-17 — TEST MATRIX: ISSUE MIRROR & WEBHOOK INBOX

- **Architecture:** TD-118-012
- **Implementation:** `scripts/w118/github_issue_adapter.py`, `scripts/w118/webhook_inbox.py`
- **Test code:** `tests/w118/test_github_issue_adapter.py`, `tests/w118/test_webhook_inbox.py`
- **Status:** CONTRACT TESTS PASS AT TESTED SHA — LIVE API / WEBHOOK RUNTIME PENDING

## 1. Sandbox → GitHub Issue mirror

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T13-I01 | Build Issue body | Stable Work/WP/Task marker and authority boundary | PASS |
| T13-I02 | First mirror | Create Issue, exact readback verified | PASS |
| T13-I03 | Repeat mirror | Same Issue returned; no duplicate create | PASS |
| T13-I04 | Task metadata changes | Existing Issue updated and read back | PASS |
| T13-I05 | PR contains same marker | PR excluded; create a real Issue | PASS |
| T13-I06 | Issue listing exceeds safe scan cap | Fail closed; do not create possible duplicate | PASS |
| T13-I07 | Invalid Task ID | Reject before API call | PASS |
| T13-I08 | Invalid repository / missing token | Reject configuration | PASS |

**Runtime limitation:** tests use an injected fake GitHub transport. No production GitHub token/API mutation was executed. Concurrent create race still needs Sandbox per-Task locking.

## 2. GitHub → Sandbox webhook inbox

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T17-W01 | Valid HMAC-SHA256 signature | Accept authenticated payload | PASS |
| T17-W02 | Invalid signature | DENY | PASS |
| T17-W03 | Malformed signature header | DENY | PASS |
| T17-W04 | Secret shorter than policy | DENY | PASS |
| T17-W05 | Non-allowlisted event | DENY | PASS |
| T17-W06 | Repository mismatch | DENY | PASS |
| T17-W07 | Invalid JSON body | DENY | PASS |
| T17-W08 | Invalid delivery UUID | DENY | PASS |
| T17-W09 | Duplicate delivery ID + same payload | Idempotent DUPLICATE | PASS |
| T17-W10 | Same delivery ID + different payload | Replay conflict | PASS |
| T17-W11 | Process pending delivery | State PROCESSED with result | PASS |
| T17-W12 | Re-process already processed delivery | Reject overwrite | PASS |
| T17-W13 | Pending query limit out of range | Reject | PASS |

**Runtime limitation:** no HTTP route is deployed to ROOM-HOP Event Listener :8050; no production webhook secret/TLS/request-size policy has been configured. Inbox receipt never mutates Task state.

## 3. Exact CI evidence

- Tested source code SHA: `343fb526f5284ca1dcc4a55d463d58bf0c437340`.
- Push run [#44877554435](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877554435): SUCCESS; **108 tests PASS / 0.503s**.
- PR run [#44877559607](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877559607): validate SUCCESS.
- Artifact ID `14696481659`; SHA-256 `9414a8c7184099475557f1a651c2e8efaed31eb1f5e839d59c4bbaaea2e4f0f6`.
- Existing aggregate branch remains `UNBOUND_LEGACY_BRANCH`; no Task state inferred.
- Event-specific handoff/ACK/review/controlled-failure jobs remain SKIPPED.

## 4. Next runtime gates

1. Integrate WebhookInbox into existing ROOM-HOP Event Listener :8050 (no new port).
2. Configure secret/TLS/network limits under explicit repository/runtime authority.
3. Connect inbox processor to Task Registry with idempotent reconciliation and exact SHA.
4. Connect Issue mirror adapter to Sandbox Task Registry with durable per-Task locking.
5. Execute controlled test Issue and task-scoped branch push; read back Issue/Branch/Commit/CI evidence.
6. Keep Agent dispatch and positive ACK blocked until a real Agent principal is verified.

**Disposition:** adapter/inbox contract PASS at tested SHA; live GitHub API, webhook receiver, Sandbox reconciliation and full runtime E2E are NOT VERIFIED.
