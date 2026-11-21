# W118-17 — TEST MATRIX: PUSH / CI EVENT RECONCILIATION

- **Architecture:** TD-118-012
- **Implementation:** `scripts/w118/event_reconciler.py`
- **Test code:** `tests/w118/test_event_reconciler.py`
- **Status:** CONTRACT TESTS PASS AT TESTED SHA — EVENT LISTENER RUNTIME PENDING

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T17-R01 | Signed push matches repository, Work, Task, Issue and exact SHA | PUSH_BOUND evidence appended | PASS |
| T17-R02 | Existing aggregate branch push | UNBOUND; no Task guessed or mutated | PASS |
| T17-R03 | CI event arrives before matching push | DEFERRED; delivery remains PENDING | PASS |
| T17-R04 | Push arrives, then deferred CI is retried | CI event reconciled to exact Task/SHA | PASS |
| T17-R05 | CI conclusion success | CI_PASS_EVIDENCE_ONLY; Task state unchanged | PASS |
| T17-R06 | CI conclusion failure | CI_FAIL_EVIDENCE_ONLY; Task state unchanged | PASS |
| T17-R07 | Push Issue ID differs from linked Task Issue | ReconciliationError; inbox remains PENDING | PASS |
| T17-R08 | CI workflow name is not allowlisted | Reject | PASS |
| T17-R09 | Processed delivery is received again | ALREADY_PROCESSED; no duplicate Task event | PASS |

## Exact CI evidence

- Tested SHA: `4e5c1e0d23cf145ddbcfca88c32255069ab3c642`.
- Push run [#44877879841](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877879841): SUCCESS; **118 tests PASS / 0.380s**.
- PR run [#44877883249](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877883249): SUCCESS.
- Artifact ID `14697131158`; SHA-256 `db783c9329e95f2cdb0dce68c21911d56bb2bc7e318088fb53617936c9861011`.
- The tested reconciler uses an in-memory SQLite Task Registry and authenticated in-memory WebhookInbox; it proves contract behavior only, not deployment to ROOM-HOP.

## Runtime gates not yet proven

- Event Listener :8050 HTTP route, HMAC secret, TLS/network policy and durable SQLite volume.
- Real GitHub webhook delivery and replay.
- Production Task Registry persistence and multi-process coordination.
- Real Agent Registry/dispatch/ACK.
- Task-specific branch push and actual GitHub Actions workflow_run callback.
- CI callback processing by a running Sandbox service.
- Full Plan → Task → Issue → Agent → Branch → Commit → Push → CI → Sandbox → Review → Owner acceptance E2E.

**Disposition:** push/CI reconciliation contract PASS at tested SHA; runtime E2E NOT VERIFIED.
