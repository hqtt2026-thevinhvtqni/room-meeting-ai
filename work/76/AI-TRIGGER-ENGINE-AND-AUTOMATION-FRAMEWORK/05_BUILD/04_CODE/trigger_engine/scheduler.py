"""Deterministic UTC one-shot scheduler; durable occurrence claiming is injected."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
class SchedulerBlocked(RuntimeError): pass
@dataclass(frozen=True)
class OneShotSchedule:
    schedule_id: str
    work_id: str
    run_at: datetime
    def __post_init__(self):
        if not self.schedule_id.strip() or not self.work_id.strip(): raise ValueError("schedule_id and work_id required")
        if self.run_at.tzinfo is None: raise ValueError("run_at requires explicit timezone")
        object.__setattr__(self, "run_at", self.run_at.astimezone(timezone.utc))
@dataclass(frozen=True)
class DueOccurrence:
    schedule_id: str
    work_id: str
    scheduled_for: datetime
    idempotency_key: str
class DueStore(Protocol):
    def claim_once(self, schedule_id: str, occurrence_key: str) -> bool: ...
class TimeScheduler:
    def __init__(self, due_store: DueStore | None): self._store = due_store
    def due(self, schedule: OneShotSchedule, now: datetime) -> DueOccurrence | None:
        if self._store is None: raise SchedulerBlocked("durable due-store unavailable")
        if now.tzinfo is None: raise ValueError("now requires timezone")
        if now.astimezone(timezone.utc) < schedule.run_at: return None
        key = f"{schedule.schedule_id}:{schedule.run_at.isoformat()}"
        if self._store.claim_once(schedule.schedule_id, key) is not True: return None
        return DueOccurrence(schedule.schedule_id, schedule.work_id, schedule.run_at, key)
    @staticmethod
    def recurring_not_supported(*args, **kwargs):
        raise SchedulerBlocked("recurrence/DST/HA policy requires ADR-76-005 approval")
