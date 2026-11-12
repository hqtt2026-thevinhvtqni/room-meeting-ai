# DOC-006 — VERIFICATION PLAN / KẾ HOẠCH KIỂM CHỨNG

## Required test groups
1. Schema: valid/invalid Trigger definitions, version compatibility, missing owner/scope.
2. Scheduler: timezone, daylight-saving transitions, missed schedule, pause/resume, clock drift.
3. Event gateway: invalid signature, expired timestamp, replay, malformed payload, oversized payload, unknown source.
4. Condition engine: typed comparisons, AND/OR/NOT, null/missing values, boundary thresholds, time windows; reject arbitrary code.
5. Authorization: unauthenticated, wrong Work/WP, revoked assignment, stale policy, gate not satisfied, action outside scope.
6. Reliability: duplicate delivery, out-of-order events, retry exhaustion, queue unavailable, database unavailable, audit unavailable.
7. Safety: kill switch, human approval, allow-list enforcement, rate limit, cooldown, secret redaction, prompt injection in event payload.
8. Dispatch: distinguish QUEUED, SENT, RECEIVED and ACKNOWLEDGED; no fabricated delivery proof.
9. Dashboard: read-only, responsive mobile/desktop, stale/unknown source, empty/error states.
10. Recovery: dead-letter replay, rollback Trigger version, disable/restore, audit continuity.

## Release criteria
- All critical security and authorization tests pass.
- No duplicate side effect under replay/idempotency tests.
- Audit/evidence chain is complete for each execution.
- Kill switch and pause/disable are verified.
- Independent QE sign-off and Vinh acceptance recorded.
- No unresolved critical/high blocker without explicit accepted risk.

## Current verification status
NOT_STARTED. This file is a test plan only; no test execution is claimed.


## Static-review regression addendum — prototype PR #53
These cases are mandatory regression tests if the prototype is used as a starting point. They are test specifications only; they have NOT been executed.

| Test ID | Area | Input / setup | Required result |
|---|---|---|---|
| W76-CE-001 | Time normalization | Compare timezone-aware datetime values with UTC and non-UTC offsets | Normalize to UTC without NameError; preserve instant equality/order |
| W76-CE-002 | AST validation | Equality/comparison node omits `left` or `right` | Reject as malformed ConditionEvaluationError; must never treat missing operands as null literals |
| W76-CE-003 | Relative time window | Event timestamp is within, exactly on, older than, and later than the configured `last_seconds` window | Apply a documented UTC reference clock; accept only the defined inclusive/exclusive boundary; reject stale/future events according to policy |
| W76-CE-004 | Explicit time window | `since` / `until` boundaries with UTC offsets, naive timestamps and inverted ranges | Normalize aware timestamps; reject naive/inverted ranges; verify exact boundary behavior |
| W76-RG-001 | Version activation | v1 ACTIVE; publish v2 DRAFT; activate v2; query active versions | At most one ACTIVE version per trigger_id; activation and prior-version retirement are atomic; no stale duplicate in active_triggers() |
| W76-RG-002 | Lifecycle consistency | Pause/resume/disable across multiple versions | Only the intended version transitions; registry query and persisted JSON agree after reload |
| W76-MD-001 | Semantic immutability | Mutate nested condition, schedule or action parameters after construction/publication | Mutation is rejected or cannot change stored definition/content digest |
| W76-MD-002 | Numeric validation | Retry max_attempts/backoff values include bool, string, negative, NaN, infinity and extreme values | Reject invalid/non-finite values with stable validation errors; retry budget remains bounded |
| W76-EV-001 | Event input validation | event_id/provider/event_type supplied as null, number, empty string or malformed type | Reject deterministically with declared validation exception; no leaked AttributeError |
| W76-EV-002 | Untrusted payload | Payload contains instruction-like strings, nested objects and oversized structures | Treat as data only; enforce schema/size limits; no policy/action mutation |

### Acceptance mapping for this addendum
- Condition evaluator cases W76-CE-001…004 map to DOC-003 FR-04, DOC-004 Condition Evaluator / Security boundaries, and DOC-006 group 4.
- Registry cases W76-RG-001…002 map to DOC-003 FR-01, DOC-004 Trigger lifecycle, and DOC-006 groups 1 and 10.
- Model integrity cases W76-MD-001…002 map to DOC-003 FR-01/NFR-06 and DOC-006 groups 1 and 6.
- Event cases W76-EV-001…002 map to DOC-003 FR-03/NFR-01 and DOC-006 groups 3 and 7.
- Each test result must retain test ID, exact source commit, command, environment, raw output, exit code and artifact hash. Static inspection or a planned test is not execution evidence.


## Requirements-to-verification traceability matrix (DESIGN / NOT EXECUTED)

The matrix closes the traceability gap between DOC-003 FR/NFR, DOC-004 logical components and DOC-006 test groups. IDs below are proposed test specifications, not evidence of implementation or execution. Test fixtures, commands, source commit and raw results must be attached only when the relevant runtime exists and gates authorize execution.

| Requirement | Design component / contract | Required verification IDs | Coverage expectation | Current status |
|---|---|---|---|---|
| FR-01 Registry lifecycle/versioning | Trigger Registry; lifecycle and single-ACTIVE invariant | W76-REG-001…004; W76-RG-001…002 | CRUD scope validation, version conflict, atomic activation, pause/resume/disable and reload consistency | SPECIFIED / NOT RUN |
| FR-02 Scheduler | Scheduler; timezone and missed-run policy | W76-SCH-001…006 | One-shot/recurring, UTC offsets, DST gap/fold, clock drift, missed-run policy, pause/resume and duplicate tick | SPECIFIED / NOT RUN |
| FR-03 Event intake | Event Gateway; normalized envelope and source-auth contract | W76-EVT-001…006; W76-EV-001…002 | Unknown source, signature/key rotation, malformed/oversized payload, timestamp skew, replay and trusted Work-scope resolution | SPECIFIED / NOT RUN |
| FR-04 Condition engine | Typed AST and deterministic evaluator | W76-COND-001…008; W76-CE-001…004 | Type/operator/arity validation, missing vs null, boolean composition, threshold boundaries, timezone and stale/future time windows | SPECIFIED / NOT RUN |
| FR-05 Dispatch | AI Dispatcher; assignment/target/receipt/ACK contract | W76-DSP-001…006 | Trusted target resolution, scope binding, QUEUED/SENT/RECEIVED/ACKNOWLEDGED separation, timeout UNKNOWN, retry/idempotency and mismatched ACK rejection | BLOCKED BY TRANSPORT / NOT RUN |
| FR-06 Safety | Policy adapter, approval, cooldown, rate limit, kill switch | W76-AUTH-001…010 | Unauthenticated/wrong scope/revoked assignment/stale policy/gate deny/approval missing; kill switch checked at enqueue, dispatch and execution | SPECIFIED / NOT RUN |
| FR-07 Observability | Orchestrator state machine and Audit/Evidence Store | W76-OBS-001…005 | Correlation continuity, legal state transitions, reason codes, terminal outcome and no inferred state from UI | SPECIFIED / NOT RUN |
| FR-08 Dashboard | Read-only API/projection | W76-DASH-001…006 | Read-only enforcement, source freshness/UNKNOWN, empty/error states, filter/search, desktop/mobile interaction and no local fixture masquerading as Core live | IN REVIEW / BROWSER QE NOT RUN |
| FR-09 Replay | Replay controller and idempotency boundary | W76-RPL-001…006 | Dry-run default, explicit side-effect opt-in, current authorization recheck, duplicate replay suppression, audit continuity and kill-switch enforcement | SPECIFIED / NOT RUN |
| FR-10 Multi-tenant | Work/scope isolation across registry, event, queue, audit and projection | W76-TEN-001…006 | Cross-Work read/write denial, scope inheritance from trusted registry, partition/query isolation, no leakage in errors and audit | SPECIFIED / NOT RUN |
| NFR-01 Security | Authentication, authorization, signature and secret handling | W76-SEC-001…008 | Forged identity/role/authorized flags, signature invalidation, key rotation, least privilege, injection-as-data and secret redaction | SPECIFIED / NOT RUN |
| NFR-02 Reliability | At-least-once intake + idempotent processing | W76-REL-001…006 | Duplicate/out-of-order delivery, crash/restart recovery, idempotency persistence and no exactly-once claim absent proof | SPECIFIED / NOT RUN |
| NFR-03 Audit | Append-only/tamper-evident audit contract | W76-AUD-001…006 | Missing audit store fail-closed, tamper detection, provenance completeness, correlation, redaction and mutation/audit consistency | SPECIFIED / NOT RUN |
| NFR-04 Resilience | Retry budget, backoff, DLQ and recovery | W76-RES-001…007 | Bounded retry, poison event, queue/database/audit outage, DLQ recovery, operator replay and recovery idempotency | SPECIFIED / NOT RUN |
| NFR-05 Performance | Measured SLO/throughput/latency | W76-PERF-001…004 | Load/soak/latency/throughput measurements against owner-approved SLO; no numeric target invented in this plan | BLOCKED — SLO NOT APPROVED |
| NFR-06 Maintainability | Versioned schemas and migration | W76-MAINT-001…006; W76-MD-001…002 | Backward compatibility, migration/rollback, schema rejection, digest stability and reproducible contract fixtures | SPECIFIED / NOT RUN |
| NFR-07 Privacy | Data minimization, retention and redaction | W76-PRIV-001…005 | Private conversation/prompt exclusion, secret/PII redaction, retention/deletion policy, access isolation and evidence export minimization | BLOCKED — POLICY/RETENTION ADR OPEN |

### Execution and acceptance rules
1. Every listed ID must be expanded into deterministic setup, input, expected output, cleanup and evidence artifact before implementation test execution.
2. The existing W76-CE/W76-RG/W76-MD/W76-EV regression cases remain mandatory; do not replace or renumber them.
3. Test status vocabulary: SPECIFIED, READY, RUNNING, PASS, FAIL, BLOCKED, NOT RUN. SPECIFIED is not PASS.
4. Independent QE must execute or independently reproduce critical security, reliability, dispatch and audit cases. Implementer static review is not QE sign-off.
5. Any test blocked by missing Core API, transport, SLO or retention decision must retain its explicit blocker and must not be silently marked skipped/pass.

Status: traceability specification only. DOC-006 overall remains NOT_STARTED; no tests have been executed by this addendum.
