# WORK STATE MACHINE — V1.1
Work: NOT_STARTED → ACTIVE → (BLOCKED ↔ ACTIVE) → ACCEPTED → RELEASED → OPERATING → CLOSED. CANCELLED requires authorized owner and reason.

Phase: NOT_STARTED | PLANNED | ACTIVE | BLOCKED | DONE | CANCELLED. Exactly one current phase is selected. A phase becomes DONE only after its exit gate is PASS. A later phase cannot become current while its predecessor gate is unresolved.

Gate: NOT_READY | PENDING | PASS | FAIL | WAIVED. PASS requires verified evidence and authorized evaluation. WAIVED is exceptional and is not PASS.

WP: DRAFT → READY → IN_PROGRESS → IN_REVIEW → DONE. Any active state may become BLOCKED. Rejected review returns to IN_PROGRESS. DONE requires acceptance criteria and evidence.

Invariants:
1. Server-side identity and permission check for every state-changing request.
2. Optimistic version/state check to prevent concurrent lost updates.
3. Enforce predecessor gate and required evidence.
4. Record actor, role, timestamp, reason, correlation ID and evidence refs.
5. Reject unknown/illegal transitions (fail closed).
6. Idempotency keys for retries.
7. Dashboard/adapters cannot directly mutate authoritative state.
Progress percentage is not gate status. UNKNOWN must never default to zero, DONE or PASS.
