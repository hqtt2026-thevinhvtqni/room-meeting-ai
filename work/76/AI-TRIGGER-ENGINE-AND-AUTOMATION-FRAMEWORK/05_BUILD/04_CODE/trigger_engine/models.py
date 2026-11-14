"""Work 76 trigger engine immutable model layer.

Implements DOC-004 contract baseline:
- deep-frozen nested structures (regression W76-MD-001),
- strict numeric validation incl. bool/NaN/infinity rejection (W76-MD-002),
- strict event input validation with declared errors, no AttributeError leak
  (W76-EV-001),
- payload treated as untrusted data with size/depth limits (W76-EV-002),
- stable canonical-JSON content digest over semantic fields.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator, Mapping

from .errors import ValidationError

TRIGGER_TYPES = ("TIME", "EVENT", "CONDITION", "MANUAL", "COMPOSITE")
TRIGGER_STATUSES = ("DRAFT", "ACTIVE", "PAUSED", "DISABLED", "RETIRED")

MAX_PAYLOAD_BYTES = 65536
MAX_PAYLOAD_DEPTH = 16
MAX_BACKOFF_SECONDS = 2592000.0  # 30 days hard cap; retry budget must stay bounded
MAX_ATTEMPTS = 100


def _require_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value


def deep_freeze(value: Any, _depth: int = 0) -> Any:
    """Return a deeply immutable copy of value; reject unsupported types."""
    if _depth > MAX_PAYLOAD_DEPTH:
        raise ValidationError("structure exceeds maximum depth")
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValidationError("non-finite float is not allowed")
        return value
    if isinstance(value, Mapping):
        return FrozenDict({str(k): deep_freeze(v, _depth + 1) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(deep_freeze(v, _depth + 1) for v in value)
    raise ValidationError(f"unsupported value type: {type(value).__name__}")


def unfreeze(value: Any) -> Any:
    """Convert frozen structures back to plain dict/list for serialization."""
    if isinstance(value, FrozenDict):
        return {k: unfreeze(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [unfreeze(v) for v in value]
    return value


class FrozenDict(Mapping):
    """Immutable mapping; mutation attempts raise TypeError."""

    __slots__ = ("_data",)

    def __init__(self, data: Mapping[str, Any]) -> None:
        object.__setattr__(self, "_data", dict(data))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"FrozenDict({self._data!r})"


def canonical_json(value: Any) -> str:
    """Deterministic canonical JSON encoding for digests and storage."""
    return json.dumps(
        unfreeze(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def content_digest(value: Any) -> str:
    """SHA-256 digest of the canonical encoding of value."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    backoff_seconds: float
    max_backoff_seconds: float = 3600.0

    def __post_init__(self) -> None:
        # bool is a subclass of int: reject it explicitly (W76-MD-002).
        if isinstance(self.max_attempts, bool) or not isinstance(self.max_attempts, int):
            raise ValidationError("max_attempts must be an integer")
        if not 1 <= self.max_attempts <= MAX_ATTEMPTS:
            raise ValidationError(f"max_attempts must be within 1..{MAX_ATTEMPTS}")
        for name in ("backoff_seconds", "max_backoff_seconds"):
            v = getattr(self, name)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValidationError(f"{name} must be a number")
            if not math.isfinite(float(v)):
                raise ValidationError(f"{name} must be finite")
            if v < 0:
                raise ValidationError(f"{name} must be non-negative")
        if self.backoff_seconds > MAX_BACKOFF_SECONDS or self.max_backoff_seconds > MAX_BACKOFF_SECONDS:
            raise ValidationError(f"backoff values must not exceed {MAX_BACKOFF_SECONDS}")
        if self.backoff_seconds > self.max_backoff_seconds:
            raise ValidationError("backoff_seconds must not exceed max_backoff_seconds")


@dataclass(frozen=True)
class ActionSpec:
    action_type: str
    parameters: Any = None

    def __post_init__(self) -> None:
        _require_str(self.action_type, "action_type")
        object.__setattr__(self, "parameters", deep_freeze(self.parameters))


@dataclass(frozen=True)
class Trigger:
    trigger_id: str
    name: str
    version: int
    trigger_type: str
    owner_principal: str
    work_id: str
    condition: Any
    action: ActionSpec
    schedule: Any = None
    policy_ref: str = ""
    status: str = "DRAFT"
    revision: int = 1
    content_digest: str = ""

    def __post_init__(self) -> None:
        _require_str(self.trigger_id, "trigger_id")
        _require_str(self.name, "name")
        _require_str(self.owner_principal, "owner_principal")
        _require_str(self.work_id, "work_id")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise ValidationError("version must be a positive integer")
        if self.trigger_type not in TRIGGER_TYPES:
            raise ValidationError(f"trigger_type must be one of {TRIGGER_TYPES}")
        if self.status not in TRIGGER_STATUSES:
            raise ValidationError(f"status must be one of {TRIGGER_STATUSES}")
        if isinstance(self.revision, bool) or not isinstance(self.revision, int) or self.revision < 1:
            raise ValidationError("revision must be a positive integer")
        if not isinstance(self.action, ActionSpec):
            raise ValidationError("action must be an ActionSpec")
        object.__setattr__(self, "condition", deep_freeze(self.condition))
        if self.schedule is not None:
            object.__setattr__(self, "schedule", deep_freeze(self.schedule))
        if not self.content_digest:
            object.__setattr__(self, "content_digest", self.semantic_digest())

    def semantic_digest(self) -> str:
        """Digest over semantic content only (excludes status/revision bookkeeping)."""
        return content_digest(
            {
                "trigger_id": self.trigger_id,
                "name": self.name,
                "version": self.version,
                "trigger_type": self.trigger_type,
                "owner_principal": self.owner_principal,
                "work_id": self.work_id,
                "condition": unfreeze(self.condition),
                "action": {
                    "action_type": self.action.action_type,
                    "parameters": unfreeze(self.action.parameters),
                },
                "schedule": unfreeze(self.schedule) if self.schedule is not None else None,
                "policy_ref": self.policy_ref,
            }
        )

    def with_status(self, status: str, revision: int) -> "Trigger":
        if status not in TRIGGER_STATUSES:
            raise ValidationError(f"status must be one of {TRIGGER_STATUSES}")
        return Trigger(
            trigger_id=self.trigger_id,
            name=self.name,
            version=self.version,
            trigger_type=self.trigger_type,
            owner_principal=self.owner_principal,
            work_id=self.work_id,
            condition=self.condition,
            action=self.action,
            schedule=self.schedule,
            policy_ref=self.policy_ref,
            status=status,
            revision=revision,
            content_digest=self.content_digest,
        )

    def to_dict(self) -> dict:
        return {
            "trigger_id": self.trigger_id,
            "name": self.name,
            "version": self.version,
            "trigger_type": self.trigger_type,
            "owner_principal": self.owner_principal,
            "work_id": self.work_id,
            "condition": unfreeze(self.condition),
            "action": {
                "action_type": self.action.action_type,
                "parameters": unfreeze(self.action.parameters),
            },
            "schedule": unfreeze(self.schedule) if self.schedule is not None else None,
            "policy_ref": self.policy_ref,
            "status": self.status,
            "revision": self.revision,
            "content_digest": self.content_digest,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Trigger":
        try:
            action = data["action"]
            trigger = cls(
                trigger_id=data["trigger_id"],
                name=data["name"],
                version=data["version"],
                trigger_type=data["trigger_type"],
                owner_principal=data["owner_principal"],
                work_id=data["work_id"],
                condition=data["condition"],
                action=ActionSpec(
                    action_type=action["action_type"],
                    parameters=action.get("parameters"),
                ),
                schedule=data.get("schedule"),
                policy_ref=data.get("policy_ref", ""),
                status=data.get("status", "DRAFT"),
                revision=data.get("revision", 1),
                content_digest=data.get("content_digest", ""),
            )
        except KeyError as exc:
            raise ValidationError(f"missing required field: {exc.args[0]}") from exc
        # M1 (Grok review): verify the persisted digest against the recomputed
        # semantic digest so altered content cannot be silently accepted.
        provided = data.get("content_digest", "")
        if provided and provided != trigger.content_digest:
            raise ValidationError(
                "content_digest mismatch: persisted semantic content was altered"
            )
        return trigger


@dataclass(frozen=True)
class Event:
    event_id: str
    provider: str
    event_type: str
    occurred_at: datetime
    payload: Any = None

    def __post_init__(self) -> None:
        # Strict declared validation; malformed input raises ValidationError,
        # never AttributeError (W76-EV-001).
        _require_str(self.event_id, "event_id")
        _require_str(self.provider, "provider")
        _require_str(self.event_type, "event_type")
        if not isinstance(self.occurred_at, datetime):
            raise ValidationError("occurred_at must be a datetime")
        if self.occurred_at.tzinfo is None:
            raise ValidationError("occurred_at must be timezone-aware")
        object.__setattr__(self, "occurred_at", self.occurred_at.astimezone(timezone.utc))
        object.__setattr__(self, "payload", deep_freeze(self.payload))
        encoded = canonical_json(self.payload)
        if len(encoded.encode("utf-8")) > MAX_PAYLOAD_BYTES:
            raise ValidationError("payload exceeds maximum encoded size")
