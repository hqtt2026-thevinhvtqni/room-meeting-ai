# STORAGE & EXPORT — ACCEPTANCE / VERIFICATION PLAN
- **STT / Document ID:** DOC-024
- **Priority:** P2
- **Read order:** 29
- **Depends on:** DOC-016; DOC-015
- **Status:** PLANNED — NOT EXECUTED
- **Version / Updated:** 1.0 / 2026-10-30

Version: 1.0
Date: 2026-10-30
Status: PLANNED — NOT EXECUTED
Scope: Work 70 / 05_BUILD

## Test principles

- No fake PASS. Planned tests are not executed tests.
- Test against real Core/storage/export contracts, not invented mock routes.
- Keep Core as the only authority for Work state and authorization.
- Every test records build/commit, environment, actor, input, expected result, actual result and evidence reference.

## Acceptance matrix

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| ST-01 | Save valid evidence artifact | Backend confirms artifact ID, version, metadata and read-after-write hash | NOT_RUN |
| ST-02 | Upload same request twice with same idempotency key | One logical artifact result; no duplicate canonical record | NOT_RUN |
| ST-03 | Upload with invalid media type/size | Rejected with explicit reason; no persisted PASS | NOT_RUN |
| ST-04 | Storage write interrupted | FAILED or PENDING_RECONCILIATION; retry is safe | NOT_RUN |
| ST-05 | Read artifact after write | Bytes and SHA-256 match registered metadata | NOT_RUN |
| ST-06 | Create a new version of an existing artifact | Old version remains immutable and traceable | NOT_RUN |
| ST-07 | Unauthorized user saves/reads restricted evidence | Server denies; denial is audited; no data leak | NOT_RUN |
| EX-01 | Export Work dossier as JSON | Valid schema/version, consistent snapshot and provenance | NOT_RUN |
| EX-02 | Export tabular index as CSV | UTF-8, stable columns, correct row counts and formula injection protection | NOT_RUN |
| EX-03 | Export readable dossier as Markdown | Correct lifecycle/WP/blocker/decision/evidence references | NOT_RUN |
| EX-04 | Export selected WP only | No records outside selected Work/WP scope | NOT_RUN |
| EX-05 | Export restricted evidence | Restricted content excluded or denied according to policy | NOT_RUN |
| EX-06 | Export while source changes | Export remains bound to one explicit snapshot/version | NOT_RUN |
| EX-07 | Export generation fails | FAILED state, traceable error and safe retry | NOT_RUN |
| EX-08 | Download after expiry | Denied; new export required | NOT_RUN |
| AU-01 | Save/export/download actions | Actor, timestamp, scope, result and correlation ID appear in audit trail | NOT_RUN |
| AU-02 | Secret scanning of generated files | No credentials, API keys or private tokens in output | NOT_RUN |
| UI-01 | Core/storage unavailable | UI shows unavailable; does not claim saved/exported | NOT_RUN |
| UI-02 | Local browser cache only | Never labelled canonical/persisted evidence | NOT_RUN |

## Required evidence per executed test

- Test ID and exact test command or action.
- Commit/build identifier and environment.
- Input fixture identifiers (no secrets).
- Expected and actual outcome.
- Relevant API response or UI observation with sensitive fields redacted.
- Artifact/export hash where applicable.
- Reviewer identity and timestamp.

## Release decision

All mandatory tests must be executed against the integrated implementation. Any NOT_RUN, BLOCKED, flaky or missing-evidence result prevents an overall PASS. Independent QE review is required before release recommendation.

Current result: **NOT_RUN — no implementation/runtime evidence attached**.
