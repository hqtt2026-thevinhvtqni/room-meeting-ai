"""Work 76 — Trigger Engine data contracts.

Implements the trigger definition contract drafted in DOC-004 §"Trigger
definition contract (draft)" and the two state machines in DOC-004
§"Trigger lifecycle" / §"Execution lifecycle".

Design rules carried over from the repository conventions
(`core/execution_authority.py`, `core/principal_registry.py`):

* canonical JSON encoding for digests: ``sort_keys=True``, compact separators,
  ``ensure_ascii=False``;
* SHA-256 hex digests are lowercase 64-char strings;
* all timestamps are timezone-aware UTC ``datetime`` objects; ISO-8601 with
  ``+00:00`` when serialized;
* unknown/ambiguous input is refused at construction time, never coerced.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

# --------------------------------------------------------------------------
# Constants — vocabulary frozen from DOC-003 / DOC-004
# --------------------------------------------------------------------------

TRIGGER_TYPES = ("TIME", "EVENT", "CONDITION", "MANUAL", "COMPOSITE")

TRIGGER_STATUSES = ("DRAFT", "VALIDATING", "READY", "ACTIVE", "PAUSED", "DISABLED")

EXECUTION_STATES = (
    "RECEIVED",
    "VALIDATED",
    "EVALUATED",
    "SUPPRESSED",
    "AUTHORIZED",
    "QUEUED",
    "DISPATCHED",
    "ACKNOWLEDGED",
    "SUCCEEDED",
    "FAILED",
    "EXPIRED",
)

TERMINAL_EXECUTION_STATES = frozenset(
    {"SUPPRESSED", "SUCCEEDED", "FAILED", "EXPIRED"}
)

#: Legal transitions of the execution state machine (DOC-004).
EXECUTION_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "RECEIVED": ("VALIDATED", "SUPPRESSED", "FAILED"),
    "VALIDATED": ("EVALUATED", "SUPPRESSED", "FAILED"),
    "EVALUATED": ("AUTHORIZED", "SUPPRESSED", "FAILED"),
    "AUTHORIZED": ("QUEUED", "SUPPRESSED", "FAILED"),
    "QUEUED": ("DISPATCHED", "EXPIRED", "FAILED"),
    "DISPATCHED": ("ACKNOWLEDGED", "FAILED", "EXPIRED"),
    "ACKNOWLEDGED": ("SUCCEEDED", "FAILED"),
    "SUPPRESSED": (),
    "SUCCEEDED": (),
    "FAILED": (),
    "EXPIRED": (),
}

APPROVAL_MODES = ("NONE", "HUMAN_BEFORE_ACTION")

_SHA256_LEN = 64


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        raise ValueError("naive datetime is not allowed; use timezone-aware UTC")
    return value.astimezone(timezone.utc).isoformat()


def parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp {value!r} must be timezone-aware")
    return dt.astimezone(timezone.utc)


def new_execution_id() -> str:
    return f"exe_{uuid.uuid4().hex}"


def canonical_json(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == _SHA256_LEN and all(
        c in "0123456789abcdef" for c in value.lower()
    )


# --------------------------------------------------------------------------
# Trigger definition
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceSpec:
    """Where events for an EVENT/COMPOSITE trigger come from."""

    provider: str
    event_type: str
    authentication_profile: str
    schema_version: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "event_type": self.event_type,
            "authentication_profile": self.authentication_profile,
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True)
class ActionSpec:
    """Allow-listed action executed when a trigger fires."""

    action_type: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"action_type": self.action_type, "parameters": self.parameters}


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    backoff_seconds: float = 2.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("retry.max_attempts must be >= 1")
        if self.backoff_seconds < 0:
            raise ValueError("retry.backoff_seconds must be >= 0")

    def delay_for_attempt(self, attempt: int) -> float:
        """Exponential backoff for 1-based ``attempt`` numbers."""
        if attempt < 1:
            raise ValueError("attempt must be >= 1")
        return float(self.backoff_seconds) * (2 ** (attempt - 1))

    def as_dict(self) -> dict[str, Any]:
        return {"max_attempts": self.max_attempts, "backoff_seconds": self.backoff_seconds}


@dataclass(frozen=True)
class Trigger:
    """A versioned, owned, policy-bound trigger definition (DOC-004)."""

    trigger_id: str
    name: str
    version: int
    trigger_type: str
    owner_principal: str
    work_id: str
    wp_id: str
    scope: str
    action: ActionSpec
    status: str = "DRAFT"
    description: str = ""
    source: Optional[SourceSpec] = None
    condition: Optional[dict[str, Any]] = None
    target_ai_identity: Optional[str] = None
    policy_ref: Optional[str] = None
    approval_mode: str = "NONE"
    cooldown_seconds: float = 0.0
    rate_limit_per_minute: Optional[int] = None
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    idempotency_key_template: str = "{trigger_id}:{version}:{event_id}"
    schedule: Optional[dict[str, Any]] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    created_by: str = ""

    # ---- validation ------------------------------------------------------

    def __post_init__(self) -> None:
        for fname in (
            "trigger_id",
            "name",
            "trigger_type",
            "owner_principal",
            "work_id",
            "wp_id",
            "scope",
        ):
            value = getattr(self, fname)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Trigger.{fname} must be a non-empty string")
        if not isinstance(self.version, int) or self.version < 1:
            raise ValueError("Trigger.version must be an integer >= 1")
        if self.trigger_type not in TRIGGER_TYPES:
            raise ValueError(
                f"Trigger.trigger_type must be one of {TRIGGER_TYPES}, got {self.trigger_type!r}"
            )
        if self.status not in TRIGGER_STATUSES:
            raise ValueError(f"Trigger.status must be one of {TRIGGER_STATUSES}")
        if self.approval_mode not in APPROVAL_MODES:
            raise ValueError(f"Trigger.approval_mode must be one of {APPROVAL_MODES}")
        if self.cooldown_seconds < 0:
            raise ValueError("Trigger.cooldown_seconds must be >= 0")
        if self.rate_limit_per_minute is not None and self.rate_limit_per_minute < 1:
            raise ValueError("Trigger.rate_limit_per_minute must be >= 1 or None")
        if not self.idempotency_key_template:
            raise ValueError("Trigger.idempotency_key_template must not be empty")
        if self.expires_at is not None:
            if self.expires_at.tzinfo is None:
                raise ValueError("Trigger.expires_at must be timezone-aware")
        if self.trigger_type in ("EVENT", "COMPOSITE") and self.source is None:
            raise ValueError(
                f"{self.trigger_type} triggers require a source spec (DOC-004)"
            )
        if self.trigger_type == "TIME" and not self.schedule:
            raise ValueError("TIME triggers require a schedule block (DOC-004)")
        if self.created_at.tzinfo is None or self.updated_at.tzinfo is None:
            raise ValueError("Trigger timestamps must be timezone-aware")

    # ---- identity / hashing ---------------------------------------------

    def content_digest(self) -> str:
        """SHA-256 over the semantic content of this version (excludes mutable
        bookkeeping such as ``updated_at`` so re-publishing stays stable)."""
        payload = {
            "trigger_id": self.trigger_id,
            "name": self.name,
            "version": self.version,
            "trigger_type": self.trigger_type,
            "owner_principal": self.owner_principal,
            "work_id": self.work_id,
            "wp_id": self.wp_id,
            "scope": self.scope,
            "source": self.source.as_dict() if self.source else None,
            "condition": self.condition,
            "action": self.action.as_dict(),
            "target": self.target_ai_identity,
            "policy_ref": self.policy_ref,
            "approval_mode": self.approval_mode,
            "cooldown_seconds": self.cooldown_seconds,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "retry_policy": self.retry_policy.as_dict(),
            "idempotency_key_template": self.idempotency_key_template,
            "schedule": self.schedule,
            "expires_at": iso(self.expires_at),
        }
        return sha256_hex(canonical_json(payload))

    def as_dict(self) -> dict[str, Any]:
        return {
            "trigger_id": self.trigger_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "trigger_type": self.trigger_type,
            "owner_principal": self.owner_principal,
            "work_id": self.work_id,
            "wp_id": self.wp_id,
            "scope": self.scope,
            "source": self.source.as_dict() if self.source else None,
            "condition": self.condition,
            "action": self.action.as_dict(),
            "target_ai_identity": self.target_ai_identity,
            "policy_ref": self.policy_ref,
            "approval_mode": self.approval_mode,
            "cooldown_seconds": self.cooldown_seconds,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "retry_policy": self.retry_policy.as_dict(),
            "idempotency_key_template": self.idempotency_key_template,
            "schedule": self.schedule,
            "expires_at": iso(self.expires_at),
            "status": self.status,
            "created_at": iso(self.created_at),
            "updated_at": iso(self.updated_at),
            "created_by": self.created_by,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Trigger":
        missing = [
            f
            for f in (
                "trigger_id",
                "name",
                "version",
                "trigger_type",
                "owner_principal",
                "work_id",
                "wp_id",
                "scope",
                "action",
            )
            if f not in data
        ]
        if missing:
            raise ValueError(f"Trigger definition missing fields: {missing}")
        action_raw = data["action"]
        if not isinstance(action_raw, dict) or "action_type" not in action_raw:
            raise ValueError("Trigger.action must be an object with 'action_type'")
        source_raw = data.get("source")
        source = None
        if source_raw is not None:
            source = SourceSpec(**source_raw)
        retry_raw = data.get("retry_policy") or {}
        retry = RetryPolicy(**retry_raw) if isinstance(retry_raw, dict) else RetryPolicy()
        expires_raw = data.get("expires_at")
        created_raw = data.get("created_at")
        updated_raw = data.get("updated_at")
        return Trigger(
            trigger_id=data["trigger_id"],
            name=data["name"],
            version=data["version"],
            trigger_type=data["trigger_type"],
            owner_principal=data["owner_principal"],
            work_id=data["work_id"],
            wp_id=data["wp_id"],
            scope=data["scope"],
            action=ActionSpec(
                action_type=action_raw["action_type"],
                parameters=dict(action_raw.get("parameters") or {}),
            ),
            status=data.get("status", "DRAFT"),
            description=data.get("description", ""),
            source=source,
            condition=data.get("condition"),
            target_ai_identity=data.get("target_ai_identity"),
            policy_ref=data.get("policy_ref"),
            approval_mode=data.get("approval_mode", "NONE"),
            cooldown_seconds=float(data.get("cooldown_seconds", 0.0)),
            rate_limit_per_minute=data.get("rate_limit_per_minute"),
            retry_policy=retry,
            idempotency_key_template=data.get(
                "idempotency_key_template", "{trigger_id}:{version}:{event_id}"
            ),
            schedule=data.get("schedule"),
            expires_at=parse_iso(expires_raw) if expires_raw else None,
            created_at=parse_iso(created_raw) if created_raw else utcnow(),
            updated_at=parse_iso(updated_raw) if updated_raw else utcnow(),
            created_by=data.get("created_by", ""),
        )

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now = now or utcnow()
        return self.expires_at is not None and now >= self.expires_at


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Event:
    """A normalized inbound event. Payload is untrusted DATA, never code."""

    event_id: str
    provider: str
    event_type: str
    occurred_at: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    received_at: datetime = field(default_factory=utcnow)
    source_digest: str = ""

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("Event.event_id must be non-empty")
        if self.occurred_at.tzinfo is None or self.received_at.tzinfo is None:
            raise ValueError("Event timestamps must be timezone-aware")
        if not isinstance(self.payload, dict):
            raise ValueError("Event.payload must be a dict (untrusted data)")

    def digest(self) -> str:
        return sha256_hex(
            canonical_json(
                {
                    "event_id": self.event_id,
                    "provider": self.provider,
                    "event_type": self.event_type,
                    "occurred_at": iso(self.occurred_at),
                    "payload": self.payload,
                }
            )
        )


# --------------------------------------------------------------------------
# Executions
# --------------------------------------------------------------------------


@dataclass
class ExecutionRecord:
    """One run of one trigger against one event. Audited at every transition."""

    execution_id: str
    trigger_id: str
    trigger_version: int
    trigger_digest: str
    state: str
    started_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    event_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    work_id: str = ""
    wp_id: str = ""
    principal: Optional[str] = None
    authorization_decision: Optional[str] = None  # ALLOW | DENY | UNAVAILABLE
    approval_status: Optional[str] = None  # NOT_REQUIRED | PENDING | GRANTED | REFUSED
    dispatch_receipt: Optional[str] = None
    ack: Optional[str] = None
    outcome: Optional[str] = None
    suppression_reason: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 0
    dry_run: bool = False
    replay: bool = False
    trace: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.state not in EXECUTION_STATES:
            raise ValueError(f"unknown execution state {self.state!r}")

    def can_transition_to(self, new_state: str) -> bool:
        return new_state in EXECUTION_TRANSITIONS.get(self.state, ())

    def transition(self, new_state: str, *, reason: str = "", now: Optional[datetime] = None) -> None:
        if new_state not in EXECUTION_STATES:
            raise ValueError(f"unknown execution state {new_state!r}")
        if not self.can_transition_to(new_state):
            raise ValueError(
                f"illegal execution transition {self.state} -> {new_state} "
                f"(execution_id={self.execution_id})"
            )
        now = now or utcnow()
        self.trace.append(
            {"from": self.state, "to": new_state, "at": iso(now), "reason": reason}
        )
        self.state = new_state
        self.updated_at = now

    def as_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "trigger_id": self.trigger_id,
            "trigger_version": self.trigger_version,
            "trigger_digest": self.trigger_digest,
            "state": self.state,
            "event_id": self.event_id,
            "idempotency_key": self.idempotency_key,
            "work_id": self.work_id,
            "wp_id": self.wp_id,
            "principal": self.principal,
            "authorization_decision": self.authorization_decision,
            "approval_status": self.approval_status,
            "dispatch_receipt": self.dispatch_receipt,
            "ack": self.ack,
            "outcome": self.outcome,
            "suppression_reason": self.suppression_reason,
            "error": self.error,
            "attempts": self.attempts,
            "dry_run": self.dry_run,
            "replay": self.replay,
            "started_at": iso(self.started_at),
            "updated_at": iso(self.updated_at),
            "trace": self.trace,
        }

    @staticmethod
    def new(trigger: Trigger, *, event_id: Optional[str] = None,
            idempotency_key: Optional[str] = None, dry_run: bool = False,
            replay: bool = False) -> "ExecutionRecord":
        return ExecutionRecord(
            execution_id=new_execution_id(),
            trigger_id=trigger.trigger_id,
            trigger_version=trigger.version,
            trigger_digest=trigger.content_digest(),
            state="RECEIVED",
            event_id=event_id,
            idempotency_key=idempotency_key,
            work_id=trigger.work_id,
            wp_id=trigger.wp_id,
            dry_run=dry_run,
            replay=replay,
        )


__all__ = [
    "TRIGGER_TYPES",
    "TRIGGER_STATUSES",
    "EXECUTION_STATES",
    "TERMINAL_EXECUTION_STATES",
    "EXECUTION_TRANSITIONS",
    "APPROVAL_MODES",
    "utcnow",
    "iso",
    "parse_iso",
    "new_execution_id",
    "canonical_json",
    "sha256_hex",
    "SourceSpec",
    "ActionSpec",
    "RetryPolicy",
    "Trigger",
    "Event",
    "ExecutionRecord",
]
