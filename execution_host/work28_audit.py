"""WP21 — Structured audit events (no secrets, no tokens)."""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any

_FORBIDDEN_KEYS = frozenset(
    {
        "token",
        "auth_token",
        "password",
        "secret",
        "authorization",
        "ROOM_HOP_EXECUTION_AUTH_TOKEN",
        "api_key",
    }
)

_lock = threading.Lock()
_ring: list[dict[str, Any]] = []
_MAX_RING = 256


class AuditError(ValueError):
    pass


def _scrub(payload: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in payload.items():
        lk = str(k).lower()
        if k in _FORBIDDEN_KEYS or any(
            f in lk for f in ("token", "secret", "password", "authorization")
        ):
            continue
        if isinstance(v, (str, int, float, bool)) or v is None:
            out[str(k)] = v
        else:
            out[str(k)] = str(v)[:256]
    return out


def record_audit(
    event: dict[str, Any], *, sink_path: str | Path | None = None
) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise AuditError("audit_event_must_be_object")
    entry = _scrub(event)
    entry.setdefault("ts_unix", time.time())
    with _lock:
        _ring.append(entry)
        if len(_ring) > _MAX_RING:
            del _ring[0 : len(_ring) - _MAX_RING]
    if sink_path:
        path = Path(sink_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def recent_audits(limit: int = 20) -> list[dict[str, Any]]:
    with _lock:
        return list(_ring[-max(1, min(limit, _MAX_RING)) :])


def clear_audits_for_tests() -> None:
    with _lock:
        _ring.clear()


__all__ = ["AuditError", "record_audit", "recent_audits", "clear_audits_for_tests"]
