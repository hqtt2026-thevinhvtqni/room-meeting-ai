"""Work 76 — Trigger Engine error taxonomy.

Every failure mode in the engine is represented by a dedicated exception so
callers can distinguish "rejected by policy" from "invalid input" from
"dependency unavailable". The engine fails closed: whenever an authorization,
audit or identity dependency cannot be reached, a ``FailClosedError`` (or a
subclass) is raised and no action is dispatched.

See DOC-004 §Security boundaries and DOC-006 §Required test groups.
"""

from __future__ import annotations


class TriggerEngineError(Exception):
    """Base class for every error raised by the Trigger Engine."""


class InvalidTriggerDefinition(TriggerEngineError):
    """A Trigger definition violates the contract in DOC-004."""


class ConditionEvaluationError(TriggerEngineError):
    """The typed condition expression could not be evaluated safely."""


class EventIntakeError(TriggerEngineError):
    """An inbound event was malformed, oversized, unknown-source or expired."""


class AuthenticationError(EventIntakeError):
    """The event source could not be authenticated (bad signature/token)."""


class ReplayDetected(EventIntakeError):
    """The event is a duplicate of one already processed (dedupe hit)."""


class AuthorizationDenied(TriggerEngineError):
    """Policy explicitly denied the action (not a dependency failure)."""


class ApprovalRequired(TriggerEngineError):
    """The action requires a human approval that has not been granted."""


class FailClosedError(TriggerEngineError):
    """A required dependency (identity, policy, audit, transport) is
    unavailable or unverified. Execution is refused, never guessed."""


class AuditUnavailableError(FailClosedError):
    """The evidence/audit store could not persist the record."""


class TransportUnverifiedError(FailClosedError):
    """No verified dispatch transport exists for this target.

    WP-76-07 / blocker B-76-02: the engine must never fabricate delivery
    proof. Dispatch through an unverified transport is refused outright.
    """


class ActionNotAllowed(TriggerEngineError):
    """The requested action_type is outside the execution allow-list."""


class KillSwitchEngaged(TriggerEngineError):
    """New intake/dispatch is stopped by the kill switch."""


class TriggerNotFound(TriggerEngineError):
    """No registered Trigger matches the requested id/version."""


class ImmutableTriggerVersion(TriggerEngineError):
    """Attempted to mutate an already-published Trigger version."""
