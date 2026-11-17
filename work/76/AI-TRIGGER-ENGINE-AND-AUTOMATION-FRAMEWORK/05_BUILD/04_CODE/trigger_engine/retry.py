"""Bounded retry and deduplication contracts; production stores must be durable/atomic."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol
from .models import RetryPolicy

class IdempotencyStore(Protocol):
    def claim(self, scope: str, key: str, expires_at: datetime) -> bool: ...

class DuplicateExecution(RuntimeError): pass
class IdempotencyGuard:
    def __init__(self, store: IdempotencyStore | None):
        self._store=store
    def claim(self, work_id: str, idempotency_key: str, *, now: datetime, ttl_seconds: int) -> None:
        if self._store is None: raise RuntimeError("durable idempotency store unavailable")
        if not work_id.strip() or not idempotency_key.strip() or ttl_seconds <= 0: raise ValueError("scope/key/positive TTL required")
        if now.tzinfo is None: raise ValueError("now must be timezone-aware")
        expires=now.astimezone(timezone.utc)+timedelta(seconds=ttl_seconds)
        if self._store.claim(work_id,idempotency_key,expires) is not True:
            raise DuplicateExecution("idempotency key already claimed")

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
        if now.tzinfo is None: raise ValueError("now must be timezone-aware")
        if not retryable: return RetryDecision(False,completed_attempts,None,"failure is not retryable")
        if completed_attempts >= self._policy.max_attempts:
            return RetryDecision(False,completed_attempts,None,"retry budget exhausted")
        delay=min(float(self._policy.backoff_seconds)*(2**(completed_attempts-1)),float(self._policy.max_backoff_seconds))
        due=now.astimezone(timezone.utc)+timedelta(seconds=delay)
        return RetryDecision(True,completed_attempts+1,due,"bounded exponential backoff")
