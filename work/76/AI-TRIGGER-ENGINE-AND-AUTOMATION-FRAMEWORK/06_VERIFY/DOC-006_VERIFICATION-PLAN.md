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


## Observable acceptance criteria matrix — FR/NFR (DESIGN / NOT EXECUTED)

Purpose: turn the existing requirements-to-verification traceability into reviewable pass/fail criteria. This matrix is a specification only. It does not authorize implementation or execution, and it does not change DOC-006 overall status (NOT_STARTED).

| Requirement | Preconditions / controlled fixture | PASS criteria (all required) | FAIL / fail-closed criteria | Mandatory evidence artifact |
|---|---|---|---|---|
| FR-01 Registry | Authenticated test principal, isolated Work/WP, valid and invalid Trigger fixtures, two versions | Create/read/update/version/pause/resume/disable operations enforce owner + Work/WP scope; revision conflicts are rejected; activation leaves exactly one ACTIVE version per trigger_id; persisted reload matches accepted state | Cross-Work mutation, missing owner/scope, stale revision overwrite, multiple ACTIVE versions, or unapproved action state is rejected; no partial state change | Request/response fixtures, before/after registry snapshots, revision and active-version invariant report, audit IDs |
| FR-02 Scheduler | Fixed test clock; UTC and named-zone fixtures; DST gap/fold and missed-run cases | One-shot and recurrence produce the specified next_run; UTC instant is deterministic; DST and missed-run outcomes match an approved policy; pause/disable suppresses future enqueue | Ambiguous/invalid timezone, unapproved DST/missed-run policy, duplicate tick, or stale schedule cannot silently enqueue an action | Clock configuration, schedule definitions, tick trace, expected-vs-actual timestamps, dedupe/audit records |
| FR-03 Event intake | Registered and unregistered sources; valid/invalid signatures; clock skew, replay and oversized payload fixtures | Only authenticated, schema-valid, in-window events from registered sources enter accepted processing; trusted Work scope is resolved server-side; duplicate event is idempotently recognized | Invalid signature, unknown source, malformed/oversized body, stale/future timestamp outside policy, replay, or untrusted scope is rejected before evaluation/dispatch | Raw redacted request fixture, signature verification result, schema result, replay decision, accepted/rejected audit record |
| FR-04 Condition engine | Typed AST fixtures covering every operator, boolean arity, missing/null, boundaries and time windows | Valid AST evaluates deterministically to MATCH or NO_MATCH with evaluator version, timestamp and reason code; numeric/time comparisons obey declared type and boundary semantics | Unknown operator/key, missing operand, invalid arity/type, excessive depth/nodes, non-finite number, or malformed time window returns INVALID/ERROR and never MATCH | AST fixture, validation/evaluation result, reason code, evaluator version and deterministic replay output |
| FR-05 Dispatch | Approved provider contract, authenticated target identity, valid assignment/scope, policy decision and receiver test endpoint | State advances only with evidence: QUEUED from durable enqueue; SENT from transport evidence; RECEIVED from receiver receipt; ACKNOWLEDGED from authenticated receiver ACK bound to assignment/correlation/idempotency | Missing target identity, scope mismatch, expired assignment, untrusted/mismatched ACK, timeout, or provider outage never becomes ACKNOWLEDGED; retry does not duplicate logical side effect | Redacted dispatch envelope, provider request/response, receiver receipt/ACK, correlation/idempotency trace, state-transition audit |
| FR-06 Safety | Policy fixtures for ALLOW/DENY/REQUIRE_APPROVAL/INDETERMINATE, revoked assignment, rate/cooldown and kill switch | Protected action occurs only when current principal, scope, policy, required approval and kill-switch checks all allow it at the required enforcement points | DENY, missing approval, INDETERMINATE, stale/revoked policy, wrong scope, rate limit, cooldown or kill switch suppresses action; dependency outage fails closed | Policy input/revision, decision output, approval reference, enforcement-point trace, suppressed-action audit |
| FR-07 Observability | One correlated test execution with success, suppression, failure, expiry and retry paths | Each transition has event/trigger/version, correlation ID, actor reference, timestamp, reason and evidence link; state machine records only observed transitions | Missing correlation, impossible transition, inferred ACK/outcome, or missing audit evidence blocks terminal success claim | Append-only event timeline, state-transition table, correlation completeness report, audit references |
| FR-08 Dashboard | Read-only test principal; live/stale/unknown/empty/error fixtures; desktop and mobile viewports | Dashboard renders source mode and freshness; missing/stale data is UNKNOWN; views are read-only; filters/search and responsive layouts preserve correct Work/WP/gate identity | UI cannot mutate authoritative state; stale/local snapshot is never labeled Core live; missing fields are not inferred PASS; errors are visible | Browser test report, screenshots, network/read-only proof, viewport matrix, fixture/source revision and console output |
| FR-09 Replay | Archived event, current policy, dry-run default, duplicate and side-effect fixtures | Default replay is dry-run; explicit approved replay revalidates current authorization, policy, pause/kill-switch and idempotency; audit links original and replay | Replay cannot bypass current gate/approval, cannot create duplicate side effect, and cannot silently change original event evidence | Replay request, mode/approval, original↔replay correlation, policy recheck, idempotency and side-effect evidence |
| FR-10 Multi-tenant | At least two isolated Work scopes with principals and data in each | Reads, writes, queries, events, queue items, audit and dashboard projections are constrained to authorized Work/WP scope | Cross-Work access or leakage through payload, error, search, export or audit view is denied and logged; no fallback to global scope | Principal/scope matrix, positive/negative API results, redacted leakage scan, audit entries |
| NFR-01 Security | Threat fixtures for forged identity/role/authorized flags, invalid signatures, injection and secrets | Authentication and authorization are server-derived; least privilege is enforced; secrets are redacted; event text remains data, not executable instruction | Caller-supplied identity/role/authorized booleans do not grant access; invalid auth/signature or policy uncertainty denies protected operation | Threat-model test report, auth decision traces, signature fixtures, redaction assertions |
| NFR-02 Reliability | Duplicate/out-of-order delivery, process restart, transient dependency failures | At-least-once intake is handled idempotently; recovery preserves logical state and does not duplicate side effects; no exactly-once claim without proof | Duplicate side effect, lost accepted event without recoverable record, or unbounded retry is FAIL | Delivery sequence, restart/recovery logs, idempotency store snapshots, side-effect count and retry trace |
| NFR-03 Audit | Successful, denied, rejected, dispatched, timed-out and failed paths; audit-store outage | Every security-relevant transition has append-only provenance and correlation; tampering is detectable under the approved mechanism; privacy redaction is applied | Protected action is blocked if required audit cannot persist; missing/tampered provenance cannot be reported as complete | Audit export/hash-chain or approved integrity proof, access/redaction test, outage fail-closed trace |
| NFR-04 Resilience | Retryable/non-retryable failures, poison event, queue/database/audit outage, DLQ | Retry count/backoff is bounded; poison event reaches DLQ; recovery is operator-controlled, idempotent and audited | Infinite retry, silent drop, uncontrolled replay, or recovery that bypasses authorization/audit is FAIL | Retry schedule, DLQ record, operator action, recovery trace, duplicate-side-effect assertion |
| NFR-05 Performance | Owner-approved SLO, representative workload and controlled environment | Measured latency/throughput/availability meet explicitly approved targets over the agreed load/soak profile | No approved target, invalid measurement environment, insufficient sample or missed target means NOT VERIFIED/FAIL per agreed policy; no invented numeric threshold | Approved SLO/ADR, workload profile, raw metrics, environment manifest, analysis and reproducible report |
| NFR-06 Maintainability | Versioned schemas, previous-version fixtures, migration and rollback fixtures | Compatibility policy is explicit; supported migrations are deterministic; rollback restores a valid prior state; contract fixtures reproduce across supported versions | Silent incompatible migration, digest drift, undocumented breaking change or unreproducible contract is FAIL | Schema versions, migration logs, before/after fixtures, digest/test vectors and rollback report |
| NFR-07 Privacy | Synthetic private/prompt/secret/PII markers, retention and export scenarios | Only approved minimum data is stored; prohibited prompt/private conversation content is absent; secrets/PII are redacted; retention/access/deletion follow approved policy | Unapproved private content or secret persists, export leaks data, or retention policy is undefined for a required data class means BLOCKED | Data inventory, redaction scan, retention/access decision, export test and deletion verification |

### Cross-cutting test execution record (mandatory for every PASS)

A test may be marked PASS only when its evidence bundle contains: (1) requirement and test IDs; (2) exact source commit and dirty-state indicator; (3) command or invocation and parameters; (4) runtime/tool identity and authorization scope; (5) environment/dependency versions; (6) fixture/input digest; (7) raw stdout/stderr or structured request/response; (8) exit/result code; (9) expected-vs-actual assertion report; (10) artifact hashes and durable location; (11) reviewer identity and independent disposition where required. Missing any mandatory element yields NOT_VERIFIED or BLOCKED, not PASS.

### Review and decision boundary

- Criteria depending on unresolved ADRs remain BLOCKED until the relevant decision is approved (notably Core authorization, event authentication, dispatch/ACK, audit persistence, SLO and privacy/retention).
- These criteria do not select implementation technology, invent SLO numbers, or imply that a provider/API exists.
- Xu / architecture owner reviews the design; Ka/Qw independent review and QE remain separate; Vinh retains final acceptance and release authority.
- Status: ACCEPTANCE CRITERIA SPECIFIED / NOT EXECUTED / NOT APPROVED. No source/build mutation or gate transition is authorized by this addendum.
