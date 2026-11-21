"""Work 76 AI Trigger Engine - corrected implementation baseline.

Authored by Vibe under Vinh's delegation (ASG-W76-VIBE-20261114-01).
Fixes the six static-review findings recorded against prototype PR #53 and
implements the DOC-004 proposed contract baseline. See DOC-035 execution log
entry dated 2026-11-14.
"""

from .errors import (
    ConditionEvaluationError,
    ConditionValidationError,
    ConcurrencyError,
    RegistryError,
    StateError,
    TriggerEngineError,
    ValidationError,
)
from .models import (
    MAX_PAYLOAD_BYTES,
    MAX_PAYLOAD_DEPTH,
    ActionSpec,
    Event,
    FrozenDict,
    RetryPolicy,
    Trigger,
    canonical_json,
    content_digest,
    deep_freeze,
    unfreeze,
)
from .conditions import ConditionResult, evaluate, normalize_utc
from .registry import TriggerRegistry

__all__ = [
    "ActionSpec",
    "ConditionEvaluationError",
    "ConditionResult",
    "ConditionValidationError",
    "ConcurrencyError",
    "Event",
    "FrozenDict",
    "MAX_PAYLOAD_BYTES",
    "MAX_PAYLOAD_DEPTH",
    "RegistryError",
    "RetryPolicy",
    "StateError",
    "Trigger",
    "TriggerEngineError",
    "TriggerRegistry",
    "ValidationError",
    "canonical_json",
    "content_digest",
    "deep_freeze",
    "evaluate",
    "normalize_utc",
    "unfreeze",
]
