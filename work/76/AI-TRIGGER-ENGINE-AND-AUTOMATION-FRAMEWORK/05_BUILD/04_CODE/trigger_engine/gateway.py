"""Authenticated event intake; crypto/schema/replay persistence are injected ports."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Mapping, Protocol
from .errors import ValidationError
from .models import Event, MAX_PAYLOAD_BYTES, canonical_json

class GatewayRejected(ValidationError): pass


def _reject_duplicate_object_keys(pairs):
    """Reject ambiguous JSON objects instead of silently keeping the last key."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result
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
        if not isinstance(self.source_id, str) or not self.source_id.strip():
            raise GatewayRejected("source registration requires a non-empty source_id")
        if not isinstance(self.work_id, str) or not self.work_id.strip():
            raise GatewayRejected("source registration requires a trusted Work id")
        if (not isinstance(self.allowed_event_types, frozenset)
                or not self.allowed_event_types
                or any(not isinstance(item, str) or not item.strip() for item in self.allowed_event_types)):
            raise GatewayRejected("source registration requires non-empty string event types")
        if self.schema is None or not callable(getattr(self.schema, "validate", None)):
            raise GatewayRejected("source registration requires a payload schema validator")

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
        if isinstance(max_body_bytes, bool) or not isinstance(max_body_bytes, int) or max_body_bytes <= 0:
            raise ValueError("max_body_bytes must be a positive integer")
        if isinstance(replay_window_seconds, bool) or not isinstance(replay_window_seconds, int) or replay_window_seconds <= 0:
            raise ValueError("replay_window_seconds must be a positive integer")
        if not isinstance(registrations, Mapping):
            raise ValueError("registrations must be a mapping")
        normalized = dict(registrations)
        for key, registration in normalized.items():
            if (not isinstance(key, str) or not key.strip()
                    or not isinstance(registration, SourceRegistration)
                    or key != registration.source_id):
                raise ValueError("registration keys must exactly match validated SourceRegistration.source_id")
        self._registrations, self._verifier, self._replay = normalized, verifier, replay_store
        self._max_body, self._window = max_body_bytes, replay_window_seconds

    def ingest(self, source_id: str, headers: Mapping[str, str], body: bytes,
               *, received_at: datetime | None = None) -> IngestedEvent:
        if self._verifier is None or self._replay is None:
            raise GatewayRejected("authentication/replay dependency unavailable")
        if not isinstance(source_id, str) or not source_id.strip():
            raise GatewayRejected("source_id required")
        if not isinstance(headers, Mapping):
            raise GatewayRejected("headers must be a mapping")
        reg = self._registrations.get(source_id)
        if reg is None:
            raise GatewayRejected("unknown event source")
        if not isinstance(body, bytes) or len(body) > self._max_body:
            raise GatewayRejected("invalid or oversized body")
        try:
            verified = self._verifier.verify(source_id, headers, body)
        except Exception as exc:
            raise GatewayRejected("source authentication failed") from exc
        if verified is not True:
            raise GatewayRejected("source authentication failed")
        try:
            data = json.loads(
                body.decode("utf-8"),
                object_pairs_hook=_reject_duplicate_object_keys,
            )
        except (UnicodeDecodeError, ValueError) as exc:
            raise GatewayRejected("body must be UTF-8 JSON without duplicate object keys") from exc
        if not isinstance(data, dict):
            raise GatewayRejected("event envelope must be an object")
        eid, etype, occurred = data.get("event_id"), data.get("event_type"), data.get("occurred_at")
        if not isinstance(eid, str) or not eid.strip():
            raise GatewayRejected("event_id required")
        if not isinstance(etype, str) or etype not in reg.allowed_event_types:
            raise GatewayRejected("event_type not allowed")
        if not isinstance(occurred, str):
            raise GatewayRejected("occurred_at required")
        try:
            occurred_at = datetime.fromisoformat(occurred.replace("Z", "+00:00"))
        except ValueError as exc:
            raise GatewayRejected("occurred_at malformed") from exc
        if occurred_at.tzinfo is None:
            raise GatewayRejected("occurred_at requires explicit UTC offset")
        occurred_at = occurred_at.astimezone(timezone.utc)
        now = received_at if received_at is not None else datetime.now(timezone.utc)
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise GatewayRejected("received_at must be a timezone-aware datetime")
        now = now.astimezone(timezone.utc)
        if abs((now - occurred_at).total_seconds()) > self._window:
            raise GatewayRejected("event outside accepted clock window")
        payload = data.get("payload")
        if not isinstance(payload, dict):
            raise GatewayRejected("payload must be an object")
        # The registered schema is an enforcement boundary, not merely
        # registration metadata. Validate before reserving replay identity so
        # rejected payloads cannot consume a legitimate event_id.
        try:
            reg.schema.validate(payload)
        except Exception as exc:
            raise GatewayRejected("payload schema validation failed") from exc
        try:
            payload_json = canonical_json(payload)
            event = Event(eid, source_id, etype, occurred_at, payload)
        except Exception as exc:
            raise GatewayRejected("payload/event failed strict validation") from exc
        digest = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        # Reserve replay identity only after the entire event has passed
        # validation; malformed data must not consume a valid event_id.
        try:
            replay_expires_at = now + timedelta(seconds=self._window)
        except OverflowError as exc:
            raise GatewayRejected("replay expiry exceeds supported datetime range") from exc
        try:
            reserved = self._replay.reserve(source_id, eid, replay_expires_at)
        except Exception as exc:
            raise GatewayRejected("replay protection unavailable") from exc
        if reserved is not True:
            raise GatewayRejected("duplicate/replayed event")
        return IngestedEvent(event, source_id, reg.work_id, digest, now)
