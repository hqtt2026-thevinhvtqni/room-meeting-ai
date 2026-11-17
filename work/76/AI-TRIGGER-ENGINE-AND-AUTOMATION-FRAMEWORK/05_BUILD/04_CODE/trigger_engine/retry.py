"""Bounded retry and fail-closed idempotency contracts; production stores must be durable/atomic."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol
from .models import RetryPolicy

class IdempotencyStore(Protocol):
    def claim(self, scope: str, key: str, expires_at: datetime) -> bool: ...

class DuplicateExecution(RuntimeError): pass
class IdempotencyUnavailable(RuntimeError): pass

class IdempotencyGuard:
    def __init__(self, store: IdempotencyStore | None):
        self._store=store

    def claim(self, work_id: str, idempotency_key: str, *, now: datetime, ttl_seconds: int) -> None:
        if self._store is None:
            raise IdempotencyUnavailable("durable idempotency store unavailable")
        if not isinstance(work_id,str) or not work_id.strip():
            raise ValueError("work_id is required")
        if not isinstance(idempotency_key,str) or not idempotency_key.strip():
            raise ValueError("idempotency_key is required")
        if isinstance(ttl_seconds,bool) or not isinstance(ttl_seconds,int) or ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be a positive integer")
        if not isinstance(now,datetime) or now.tzinfo is None:
            raise ValueError("now must be a timezone-aware datetime")
        expires=now.astimezone(timezone.utc)+timedelta(seconds=ttl_seconds)
        try:
            claimed=self._store.claim(work_id,idempotency_key,expires)
        except Exception as exc:
            raise IdempotencyUnavailable("idempotency store claim failed; execution must fail closed") from exc
        if claimed is False:
            raise DuplicateExecution("idempotency key already claimed")
        if claimed is not True:
            raise IdempotencyUnavailable("idempotency store returned an indeterminate result")

@dataclass(frozen=True)
class RetryDecision:
    retry: bool
    attempt: int
    due_at: datetime | None
    reason: str

class RetryPlanner:
    def __init__(self, policy: RetryPolicy):
        self._policy=policy

    def plan(self, *, completed_attempts: int, now: datetime, retryable: bool) -> RetryDecision:
        if isinstance(completed_attempts,bool) or not isinstance(completed_attempts,int) or completed_attempts < 1:
            raise ValueError("completed_attempts must be a positive integer")
        if not isinstance(now,datetime) or now.tzinfo is None:
            raise ValueError("now must be a timezone-aware datetime")
        if not isinstance(retryable,bool):
            raise ValueError("retryable must be a boolean")
        if not retryable:
            return RetryDecision(False,completed_attempts,None,"failure is not retryable")
        if completed_attempts >= self._policy.max_attempts:
            return RetryDecision(False,completed_attempts,None,"retry budget exhausted")
        delay=min(float(self._policy.backoff_seconds)*(2**(completed_attempts-1)),float(self._policy.max_backoff_seconds))
        due=now.astimezone(timezone.utc)+timedelta(seconds=delay)
        return RetryDecision(True,completed_attempts+1,due,"bounded exponential backoff")
