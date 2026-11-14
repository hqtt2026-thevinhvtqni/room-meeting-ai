"""Work 76 trigger engine error types.

All engine errors derive from TriggerEngineError so callers can fail closed
with a stable exception family. Validation errors never leak as AttributeError
or TypeError from malformed input (regression W76-EV-001).
"""


class TriggerEngineError(Exception):
    """Base class for all trigger engine errors."""


class ValidationError(TriggerEngineError):
    """Input failed structural or type validation."""


class ConditionValidationError(ValidationError):
    """Condition AST is malformed or violates the typed-expression contract."""


class ConditionEvaluationError(TriggerEngineError):
    """Condition evaluation failed at runtime (INVALID/ERROR, never a silent match)."""


class RegistryError(TriggerEngineError):
    """Registry-level invariant violation."""


class ConcurrencyError(RegistryError):
    """Optimistic concurrency (expected revision) conflict."""


class StateError(RegistryError):
    """Illegal lifecycle transition."""
