# WORK STATE MACHINE — V1.1

## Work lifecycle
NOT_STARTED → ACTIVE → (BLOCKED ↔ ACTIVE) → ACCEPTED → RELEASED → OPERATING → CLOSED.
CANCELLED requires an authorized owner and recorded reason. Reopening a closed Work requires an audited transition and reason.

## Phase state
NOT_STARTED | PLANNED | ACTIVE | BLOCKED | DONE | CANCELLED.
Exactly one current phase is selected. A phase becomes DONE only after its exit gate is PASS. A later phase cannot become current while the predecessor gate is unresolved.

## Gate state
NOT_READY | PENDING | PASS | FAIL | WAIVED.
PASS requires mandatory criteria satisfied by verified evidence and authorized evaluation. WAIVED is exceptional and is not equivalent to PASS.

## Work Package state
DRAFT → READY → IN_PROGRESS → IN_REVIEW → DONE.
Any active state may become BLOCKED. Rejected review returns to IN_PROGRESS with findings. CANCELLED requires owner decision and reason. DONE requires WP acceptance criteria and evidence.

## Transition invariants
1. Validate actor identity and server-side permission on every state-changing request.
2. Validate expected current version/state to prevent concurrent lost updates.
3. Enforce predecessor gate and required evidence before advancing.
4. Record actor, role, timestamp, reason, correlation ID and evidence references.
5. Reject unknown states and illegal transitions (fail closed).
6. Use idempotency keys for retried commands.
7. Never allow Dashboard or adapter clients to write authoritative state directly.

Progress percentage is not gate status. UNKNOWN is valid. Missing data must not default to zero, DONE or PASS.
