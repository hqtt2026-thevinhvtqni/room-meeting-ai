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
