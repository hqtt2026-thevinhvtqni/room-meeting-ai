"""Authenticated event intake; crypto/schema/replay persistence are injected ports."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Mapping, Protocol
from .errors import ValidationError
from .models import Event, MAX_PAYLOAD_BYTES

class GatewayRejected(ValidationError): pass
class SignatureVerifier(Protocol):
    def verify(self, source_id: str, headers: Mapping[str, str], body: bytes) -> bool: ...
class ReplayStore(Protocol):
    def reserve(self, source_id: str, event_id: str, expires_at: datetime) -> bool: ...
class PayloadSchema(Protocol):
    def validate(self, payload: Mapping[str, Any]) -> None: ...

@dataclass(frozen=True)
class SourceRegistration:
    source_id: str
    work_id: str
    allowed_event_types: frozenset[str]
    schema: PayloadSchema
    def __post_init__(self):
        if not self.source_id.strip() or not self.work_id.strip() or not self.allowed_event_types or self.schema is None:
            raise GatewayRejected("source registration requires source, trusted Work, event types and schema")

@dataclass(frozen=True)
class IngestedEvent:
    event: Event
    source_id: str
    work_id: str
    payload_digest: str
    received_at: datetime

class EventGateway:
    def __init__(self, registrations: Mapping[str, SourceRegistration], verifier: SignatureVerifier | None,
                 replay_store: ReplayStore | None, *, max_body_bytes: int = MAX_PAYLOAD_BYTES,
                 replay_window_seconds: int = 300):
        if max_body_bytes <= 0 or replay_window_seconds <= 0: raise ValueError("limits must be positive")
        self._registrations, self._verifier, self._replay = dict(registrations), verifier, replay_store
        self._max_body, self._window = max_body_bytes, replay_window_seconds
    def ingest(self, source_id: str, headers: Mapping[str, str], body: bytes,
               *, received_at: datetime | None = None) -> IngestedEvent:
        if self._verifier is None or self._replay is None: raise GatewayRejected("authentication/replay dependency unavailable")
        reg = self._registrations.get(source_id)
        if reg is None: raise GatewayRejected("unknown event source")
        if not isinstance(body, bytes) or len(body) > self._max_body: raise GatewayRejected("invalid or oversized body")
        try: verified = self._verifier.verify(source_id, headers, body)
        except Exception as exc: raise GatewayRejected("source authentication failed") from exc
        if verified is not True: raise GatewayRejected("source authentication failed")
        try: data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise GatewayRejected("body must be UTF-8 JSON") from exc
        if not isinstance(data, dict): raise GatewayRejected("event envelope must be an object")
        eid, etype, occurred = data.get("event_id"), data.get("event_type"), data.get("occurred_at")
        if not isinstance(eid, str) or not eid.strip(): raise GatewayRejected("event_id required")
        if etype not in reg.allowed_event_types: raise GatewayRejected("event_type not allowed")
        if not isinstance(occurred, str): raise GatewayRejected("occurred_at required")
        try: occurred_at = datetime.fromisoformat(occurred.replace("Z", "+00:00"))
        except ValueError as exc: raise GatewayRejected("occurred_at malformed") from exc
        if occurred_at.tzinfo is None: raise GatewayRejected("occurred_at requires explicit UTC offset")
        occurred_at = occurred_at.astimezone(timezone.utc)
        now = received_at or datetime.now(timezone.utc)
        if now.tzinfo is None: raise GatewayRejected("received_at must be timezone-aware")
        now = now.astimezone(timezone.utc)
        if abs((now - occurred_at).total_seconds()) > self._window: raise GatewayRejected("event outside accepted clock window")
        payload = data.get("payload")
        if not isinstance(payload, dict): raise GatewayRejected("payload must be an object")
        try: reg.schema.validate(payload)
        except Exception as exc: raise GatewayRejected("payload schema validation failed") from exc
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        if self._replay.reserve(source_id, eid, now + timedelta(seconds=self._window)) is not True:
            raise GatewayRejected("duplicate/replayed event")
        return IngestedEvent(Event(eid, source_id, etype, occurred_at, payload), source_id, reg.work_id, digest, now)
