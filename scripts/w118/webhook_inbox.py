"""Authenticated, idempotent GitHub webhook inbox for the Sandbox event listener.

This module verifies GitHub's HMAC signature, delivery ID, event allowlist and
repository binding before storing an immutable pending inbox record. It does
not mutate Task state; a separately authorized reconciler must process events.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


ALLOWED_EVENTS = {
    "push", "issues", "issue_comment", "pull_request",
    "pull_request_review", "workflow_run",
}
SIGNATURE_RE = re.compile(r"^sha256=([0-9a-f]{64})$")


class WebhookSecurityError(PermissionError):
    """Webhook failed authentication or trust-boundary validation."""


class WebhookReplayConflict(RuntimeError):
    """A delivery ID was reused with a different payload."""


def verify_github_signature(secret: str, raw_body: bytes, signature_header: str) -> bool:
    if not isinstance(secret, str) or len(secret) < 32:
        raise WebhookSecurityError("webhook secret must contain at least 32 characters")
    if not isinstance(raw_body, bytes):
        raise WebhookSecurityError("raw webhook body must be bytes")
    if not isinstance(signature_header, str):
        raise WebhookSecurityError("X-Hub-Signature-256 is required")
    match = SIGNATURE_RE.fullmatch(signature_header.strip())
    if not match:
        raise WebhookSecurityError("signature header must use sha256=<64 lowercase hex>")
    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, match.group(1)):
        raise WebhookSecurityError("GitHub webhook signature mismatch")
    return True


def _validate_delivery_id(delivery_id: str) -> str:
    if not isinstance(delivery_id, str):
        raise WebhookSecurityError("X-GitHub-Delivery is required")
    try:
        parsed = uuid.UUID(delivery_id)
    except (ValueError, AttributeError) as exc:
        raise WebhookSecurityError("delivery ID must be a UUID") from exc
    if str(parsed) != delivery_id.lower():
        raise WebhookSecurityError("delivery ID must use canonical UUID form")
    return str(parsed)


def _validate_received_at(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("received_at must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("received_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("received_at must include a timezone")
    return value


class WebhookInbox:
    """SQLite inbox with delivery-ID idempotency and immutable payload storage."""

    def __init__(self, database: str | Path = ":memory:") -> None:
        self._db = sqlite3.connect(str(database), isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA journal_mode = WAL")
        self._db.execute("PRAGMA synchronous = FULL")
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS github_webhook_inbox (
                delivery_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                repository TEXT NOT NULL,
                payload_sha256 TEXT NOT NULL,
                received_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                processing_state TEXT NOT NULL,
                result_json TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_github_webhook_pending
                ON github_webhook_inbox(processing_state, received_at);
            """
        )

    def close(self) -> None:
        self._db.close()

    def __enter__(self) -> "WebhookInbox":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def ingest(
        self,
        *,
        delivery_id: str,
        event_type: str,
        signature_header: str,
        secret: str,
        raw_body: bytes,
        expected_repository: str,
        received_at: str,
    ) -> dict[str, Any]:
        delivery_id = _validate_delivery_id(delivery_id)
        if event_type not in ALLOWED_EVENTS:
            raise WebhookSecurityError("event type is not allowlisted")
        if not isinstance(expected_repository, str) or not expected_repository.strip():
            raise WebhookSecurityError("expected repository must be configured")
        verify_github_signature(secret, raw_body, signature_header)
        received_at = _validate_received_at(received_at)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WebhookSecurityError("webhook body must be valid UTF-8 JSON") from exc
        if not isinstance(payload, Mapping):
            raise WebhookSecurityError("webhook payload must be a JSON object")
        repository = payload.get("repository")
        if not isinstance(repository, Mapping) or repository.get("full_name") != expected_repository:
            raise WebhookSecurityError("webhook repository does not match configured repository")

        payload_sha256 = hashlib.sha256(raw_body).hexdigest()
        payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self._db.execute("BEGIN IMMEDIATE")
        try:
            existing = self._db.execute(
                "SELECT * FROM github_webhook_inbox WHERE delivery_id = ?", (delivery_id,)
            ).fetchone()
            if existing:
                if existing["payload_sha256"] != payload_sha256 or existing["event_type"] != event_type:
                    raise WebhookReplayConflict("delivery ID was reused with different event content")
                self._db.execute("COMMIT")
                return {
                    "status": "DUPLICATE",
                    "delivery_id": delivery_id,
                    "event_type": existing["event_type"],
                    "payload_sha256": existing["payload_sha256"],
                    "processing_state": existing["processing_state"],
                }
            self._db.execute(
                "INSERT INTO github_webhook_inbox VALUES (?, ?, ?, ?, ?, ?, 'PENDING', NULL)",
                (delivery_id, event_type, expected_repository, payload_sha256, received_at, payload_json),
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {
            "status": "RECEIVED",
            "delivery_id": delivery_id,
            "event_type": event_type,
            "repository": expected_repository,
            "payload_sha256": payload_sha256,
            "processing_state": "PENDING",
            "state_effect": "INBOX_ONLY_NO_TASK_TRANSITION",
        }

    def list_pending(self, limit: int = 100) -> list[dict[str, Any]]:
        if type(limit) is not int or limit < 1 or limit > 1000:
            raise ValueError("limit must be an integer from 1 to 1000")
        rows = self._db.execute(
            "SELECT delivery_id, event_type, repository, payload_sha256, received_at, processing_state "
            "FROM github_webhook_inbox WHERE processing_state = 'PENDING' "
            "ORDER BY received_at, delivery_id LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_delivery(self, delivery_id: str) -> dict[str, Any]:
        row = self._db.execute(
            "SELECT * FROM github_webhook_inbox WHERE delivery_id = ?", (delivery_id,)
        ).fetchone()
        if not row:
            raise KeyError(f"unknown delivery_id: {delivery_id}")
        result = dict(row)
        result["payload"] = json.loads(result.pop("payload_json"))
        result_json = result.pop("result_json")
        result["result"] = json.loads(result_json) if result_json else None
        return result

    def mark_processed(self, delivery_id: str, result: Mapping[str, Any]) -> None:
        if not isinstance(result, Mapping):
            raise ValueError("processing result must be an object")
        encoded = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        cursor = self._db.execute(
            "UPDATE github_webhook_inbox SET processing_state = 'PROCESSED', result_json = ? "
            "WHERE delivery_id = ? AND processing_state = 'PENDING'",
            (encoded, delivery_id),
        )
        if cursor.rowcount != 1:
            raise ValueError("delivery is unknown or is no longer PENDING")
