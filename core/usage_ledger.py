"""Fail-safe, append-only usage ledger for provider-call metadata.

No prompt/response bodies or credentials are persisted. This module never raises
into the AI request path: failed writes are counted best-effort and sent to stderr.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

_VN_TZ = timezone(timedelta(hours=7))
_SCHEMA_VERSION = "1"
_MAX_FILE_BYTES = 20 * 1024 * 1024
_FIELDS = (
    "event_id", "occurred_at", "event_type", "ingested_at", "ai_id", "ai_role",
    "provider", "model", "usage_source", "input_tokens", "output_tokens",
    "cached_input_tokens", "reasoning_tokens", "other_usage", "work_id",
    "task_id", "room_id", "meeting_id", "turn_number", "attempt_id",
    "parent_event_id", "caller", "provider_request_id", "cost_amount",
    "cost_currency", "pricing_version", "cost_status", "status", "error_class",
    "latency_ms", "content_hash", "redaction_status", "schema_version",
)


def _now() -> str:
    return datetime.now(_VN_TZ).isoformat()


def new_usage_event(
    *, provider: str, model: str | None, ai_id: str | None = None,
    ai_role: str | None = None, caller: str, correlation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an in-memory event before sending the provider request."""
    event: dict[str, Any] = {
        "event_id": str(uuid.uuid4()), "occurred_at": _now(),
        "event_type": "provider_call", "ingested_at": None,
        "ai_id": ai_id, "ai_role": ai_role, "provider": provider, "model": model,
        "usage_source": "unavailable", "input_tokens": None, "output_tokens": None,
        "cached_input_tokens": None, "reasoning_tokens": None, "other_usage": {},
        "work_id": None, "task_id": None, "room_id": None, "meeting_id": None,
        "turn_number": None, "attempt_id": None, "parent_event_id": None,
        "caller": caller, "provider_request_id": None, "cost_amount": None,
        "cost_currency": "USD", "pricing_version": None, "cost_status": "unavailable",
        "status": "ok", "error_class": None, "latency_ms": None,
        "content_hash": None, "redaction_status": "metadata_only",
        "schema_version": _SCHEMA_VERSION,
    }
    if correlation:
        for key in ("work_id", "task_id", "room_id", "meeting_id", "turn_number", "attempt_id", "parent_event_id"):
            if correlation.get(key) is not None:
                event[key] = correlation[key]
    return event


def extract_usage(provider: str, usage: Any) -> dict[str, Any]:
    """Normalize known provider usage fields; absent fields remain None."""
    result = {
        "usage_source": "provider_reported",
        "input_tokens": None, "output_tokens": None,
        "cached_input_tokens": None, "reasoning_tokens": None, "other_usage": {},
    }
    if usage is None:
        result["usage_source"] = "unavailable"
        return result
    if not isinstance(usage, Mapping):
        usage = {k: getattr(usage, k) for k in (
            "prompt_tokens", "completion_tokens", "input_tokens", "output_tokens",
            "cached_tokens", "prompt_tokens_details", "cache_read_input_tokens",
            "thoughts_token_count", "candidates_token_count", "prompt_token_count",
            "cached_content_token_count",
        ) if hasattr(usage, k)}
    p = (provider or "").lower()
    if p in ("anthropic", "claude"):
        result["input_tokens"] = usage.get("input_tokens")
        result["output_tokens"] = usage.get("output_tokens")
        result["cached_input_tokens"] = usage.get("cache_read_input_tokens", usage.get("cache_creation_input_tokens"))
    elif p in ("openai", "groq"):
        result["input_tokens"] = usage.get("prompt_tokens", usage.get("input_tokens"))
        result["output_tokens"] = usage.get("completion_tokens", usage.get("output_tokens"))
        details = usage.get("prompt_tokens_details") or {}
        if not isinstance(details, Mapping):
            details = {}
        result["cached_input_tokens"] = details.get("cached_tokens", usage.get("cached_tokens"))
        completion_details = usage.get("completion_tokens_details") or {}
        if isinstance(completion_details, Mapping):
            result["reasoning_tokens"] = completion_details.get("reasoning_tokens")
    elif p in ("google", "gemini"):
        result["input_tokens"] = usage.get("prompt_token_count")
        result["output_tokens"] = usage.get("candidates_token_count")
        result["cached_input_tokens"] = usage.get("cached_content_token_count")
        result["reasoning_tokens"] = usage.get("thoughts_token_count")
        result["other_usage"] = {
            k: v for k, v in usage.items()
            if k not in {"prompt_token_count", "candidates_token_count", "cached_content_token_count", "thoughts_token_count"}
            and isinstance(v, (str, int, float, bool, type(None)))
        }
    else:
        result["usage_source"] = "unavailable"
    return result


def sha256_text(value: str | None) -> str | None:
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def _active_path(event: Mapping[str, Any]) -> Path:
    configured = os.environ.get("USAGE_LEDGER_PATH")
    if configured:
        return Path(configured)
    stamp = event.get("occurred_at") or _now()
    try:
        month = datetime.fromisoformat(str(stamp)).strftime("%Y%m")
    except ValueError:
        month = datetime.now(_VN_TZ).strftime("%Y%m")
    return Path("docs") / f"usage_ledger-{month}.jsonl"


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":"), default=str) + "\n")
        handle.flush()


def _rotate_if_needed(path: Path) -> Path:
    try:
        if not path.exists() or path.stat().st_size < _MAX_FILE_BYTES:
            return path
        suffix = 2
        while path.with_name(f"{path.stem}.part{suffix}{path.suffix}").exists():
            suffix += 1
        rotated = path.with_name(f"{path.stem}.part{suffix}{path.suffix}")
        path.replace(rotated)
        try:
            lines = rotated.read_bytes().splitlines()
            first = json.loads(lines[0]) if lines else {}
            last = json.loads(lines[-1]) if lines else {}
            index_row = {
                "file": str(rotated), "first_event_at": first.get("occurred_at"),
                "last_event_at": last.get("occurred_at"), "event_count": len(lines),
                "sha256_first_line": hashlib.sha256(lines[0]).hexdigest() if lines else None,
                "sha256_last_line": hashlib.sha256(lines[-1]).hexdigest() if lines else None,
                "indexed_at": _now(),
            }
            _append_jsonl(Path("docs/usage_ledger_index.jsonl"), index_row)
        except Exception as exc:
            _fallback("ledger index write failed", exc, count_loss=False)
        return path
    except Exception as exc:
        _fallback("ledger rotation failed", exc, count_loss=False)
        return path


def _fallback(message: str, exc: BaseException, *, count_loss: bool = True) -> None:
    stamp = _now()
    if count_loss:
        try:
            failure_path = Path(os.environ.get("USAGE_LEDGER_FAILURES_PATH", "docs/usage_ledger_failures.log"))
            _append_jsonl(failure_path, {"timestamp": stamp, "count": 1})
        except Exception:
            pass
    try:
        sys.stderr.write(f"[usage-ledger] {stamp} {message}: {type(exc).__name__}\n")
        sys.stderr.flush()
    except Exception:
        pass


def record_usage_event(event: Mapping[str, Any]) -> None:
    """Append one completed event; never interrupt the primary AI workflow."""
    try:
        row = {key: event.get(key) for key in _FIELDS}
        row["event_id"] = row.get("event_id") or str(uuid.uuid4())
        row["occurred_at"] = row.get("occurred_at") or _now()
        row["ingested_at"] = _now()
        row["event_type"] = row.get("event_type") or "provider_call"
        row["other_usage"] = row.get("other_usage") if isinstance(row.get("other_usage"), dict) else {}
        row["cost_status"] = row.get("cost_status") or "unavailable"
        if row["cost_status"] == "unavailable":
            row["cost_amount"] = None
        row["redaction_status"] = "metadata_only"
        row["schema_version"] = _SCHEMA_VERSION
        path = _rotate_if_needed(_active_path(row))
        _append_jsonl(path, row)
    except Exception as exc:
        _fallback("ledger append failed", exc)
