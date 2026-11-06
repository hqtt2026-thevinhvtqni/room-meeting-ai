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
