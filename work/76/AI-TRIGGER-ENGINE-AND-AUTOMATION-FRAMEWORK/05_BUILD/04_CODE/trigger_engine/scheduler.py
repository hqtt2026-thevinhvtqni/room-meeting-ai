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
        if not isinstance(self.schedule_id,str) or not self.schedule_id.strip():
            raise ValueError("schedule_id is required")
        if not isinstance(self.work_id,str) or not self.work_id.strip():
            raise ValueError("work_id is required")
        if not isinstance(self.run_at,datetime) or self.run_at.tzinfo is None:
            raise ValueError("run_at requires a timezone-aware datetime")
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
    def __init__(self, due_store: DueStore | None):
        self._store = due_store

    def due(self, schedule: OneShotSchedule, now: datetime) -> DueOccurrence | None:
        if self._store is None:
            raise SchedulerBlocked("durable due-store unavailable")
        if not isinstance(schedule,OneShotSchedule):
            raise ValueError("schedule must be a OneShotSchedule")
        if not isinstance(now,datetime) or now.tzinfo is None:
            raise ValueError("now requires a timezone-aware datetime")
        now_utc=now.astimezone(timezone.utc)
        if now_utc < schedule.run_at:
            return None
        key = f"{schedule.schedule_id}:{schedule.run_at.isoformat()}"
        try:
            claimed=self._store.claim_once(schedule.schedule_id, key)
        except Exception as exc:
            raise SchedulerBlocked("durable due-store claim failed; occurrence must fail closed") from exc
        if claimed is False:
            return None
        if claimed is not True:
            raise SchedulerBlocked("durable due-store returned an indeterminate claim result")
        return DueOccurrence(schedule.schedule_id, schedule.work_id, schedule.run_at, key)

    @staticmethod
    def recurring_not_supported(*args, **kwargs):
        raise SchedulerBlocked("recurrence/DST/HA policy requires ADR-76-005 approval")
