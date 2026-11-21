"""Stateless GitHub webhook signature and envelope verifier.

This is not a durable inbox or event queue. Core :8000 / the existing ROOM-HOP
event path owns deduplication, event persistence, sequence and state changes.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import uuid
from datetime import datetime
from typing import Any


class GitHubWebhookError(ValueError):
    """GitHub webhook failed authentication or envelope validation."""


ALLOWED_EVENTS = {
    "push", "issues", "issue_comment", "pull_request",
    "pull_request_review", "workflow_run",
}


def _validate_received_at(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GitHubWebhookError("received_at must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GitHubWebhookError("received_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise GitHubWebhookError("received_at must include a timezone")
    return value


def verify_github_webhook(
    *,
    raw_body: bytes,
    secret: str,
    signature_header: str,
    delivery_id: str,
    event_type: str,
    expected_repository: str,
    received_at: str,
    max_body_bytes: int = 1_000_000,
) -> dict[str, Any]:
    """Verify a GitHub webhook and return a transient verified envelope.

    The caller must forward the result to the canonical Core/event service.
    This function does not persist, queue, retry or assign event sequence.
    """
    if not isinstance(raw_body, bytes) or not raw_body:
        raise GitHubWebhookError("raw_body must be non-empty bytes")
    if type(max_body_bytes) is not int or max_body_bytes < 1:
        raise GitHubWebhookError("max_body_bytes must be a positive integer")
    if len(raw_body) > max_body_bytes:
        raise GitHubWebhookError("webhook body exceeds configured size limit")
    if not isinstance(secret, str) or len(secret) < 32:
        raise GitHubWebhookError("webhook secret must contain at least 32 characters")
    if not isinstance(signature_header, str) or not signature_header.startswith("sha256="):
        raise GitHubWebhookError("missing/invalid X-Hub-Signature-256")
    supplied = signature_header[7:]
    if len(supplied) != 64:
        raise GitHubWebhookError("signature digest has invalid length")
    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, supplied):
        raise GitHubWebhookError("webhook signature mismatch")

    try:
        parsed_delivery = uuid.UUID(delivery_id)
    except (ValueError, TypeError, AttributeError) as exc:
        raise GitHubWebhookError("X-GitHub-Delivery must be a UUID") from exc
    if str(parsed_delivery) != delivery_id.lower():
        raise GitHubWebhookError("X-GitHub-Delivery must use canonical UUID format")
    if event_type not in ALLOWED_EVENTS:
        raise GitHubWebhookError("GitHub event type is not allowlisted")
    if not isinstance(expected_repository, str) or expected_repository.count("/") != 1:
        raise GitHubWebhookError("expected_repository must be owner/name")
    received_at = _validate_received_at(received_at)

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitHubWebhookError("webhook body must be valid UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise GitHubWebhookError("webhook payload must be a JSON object")
    repository = payload.get("repository")
    if not isinstance(repository, dict) or repository.get("full_name") != expected_repository:
        raise GitHubWebhookError("webhook repository does not match the allowlisted repository")

    return {
        "delivery_id": delivery_id,
        "event_type": event_type,
        "repository": expected_repository,
        "received_at": received_at,
        "payload": payload,
        "payload_sha256": hashlib.sha256(raw_body).hexdigest(),
        "signature_verified": True,
        "persistence_owner": "ROOM_HOP_CORE_EVENT_PATH",
    }
