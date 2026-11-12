"""Work 76 — WP-76-01: Trigger Registry.

Versioned, owned storage for trigger definitions with an explicit lifecycle
(DRAFT -> VALIDATING -> READY -> ACTIVE -> PAUSED / DISABLED). Published
versions are immutable; any change requires a new version so that every
execution can be attributed to the exact definition digest that produced it
(DOC-004 §Trigger lifecycle).

The registry is deliberately in-memory + JSON-file backed. It owns NO
authorization logic — permissions live behind the Policy adapter
(`policy.py`) and are re-checked at execution time.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Iterable, Optional

from .errors import ImmutableTriggerVersion, InvalidTriggerDefinition, TriggerNotFound
from .models import TRIGGER_STATUSES, Trigger, utcnow

#: Allowed transitions of the trigger *definition* lifecycle (DOC-004).
TRIGGER_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "DRAFT": ("VALIDATING", "DISABLED"),
    "VALIDATING": ("READY", "DRAFT", "DISABLED"),
    "READY": ("ACTIVE", "DISABLED"),
    "ACTIVE": ("PAUSED", "DISABLED"),
    "PAUSED": ("ACTIVE", "DISABLED"),
    "DISABLED": ("READY",),  # explicit re-enable goes through READY review
}


class TriggerRegistry:
    """Store of trigger definitions keyed by ``(trigger_id, version)``."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._lock = threading.RLock()
        self._versions: dict[str, dict[int, Trigger]] = {}
        self._status: dict[str, str] = {}
        self.path = Path(path) if path else None
        if self.path and self.path.exists():
            self._load(self.path)

    # ------------------------------------------------------------------
    # persistence
    # ------------------------------------------------------------------

    def _load(self, path: Path) -> None:
        raw = json.loads(path.read_text(encoding="utf-8"))
        for item in raw.get("triggers", []):
            trigger = Trigger.from_dict(item)
            self._versions.setdefault(trigger.trigger_id, {})[trigger.version] = trigger
            self._status[trigger.trigger_id] = trigger.status

    def save(self) -> None:
        if self.path is None:
            return
        with self._lock:
            payload = {
                "schema_version": "w76-trigger-registry/1",
                "saved_at": utcnow().isoformat(),
                "triggers": [
                    t.as_dict()
                    for tid in sorted(self._versions)
                    for v, t in sorted(self._versions[tid].items())
                ],
            }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def export(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                t.as_dict()
                for tid in sorted(self._versions)
                for _, t in sorted(self._versions[tid].items())
            ]

    # ------------------------------------------------------------------
    # registration
    # ------------------------------------------------------------------

    def register(self, trigger: Trigger) -> Trigger:
        """Register a *new* trigger id at version 1 in DRAFT status."""
        with self._lock:
            if trigger.trigger_id in self._versions:
                raise InvalidTriggerDefinition(
                    f"trigger_id {trigger.trigger_id!r} already registered; "
                    "use publish_version() to add a new version"
                )
            if trigger.version != 1:
                raise InvalidTriggerDefinition(
                    f"first version of a trigger must be 1, got {trigger.version}"
                )
            stored = _with_status(trigger, "DRAFT")
            self._versions[stored.trigger_id] = {stored.version: stored}
            self._status[stored.trigger_id] = stored.status
            self.save()
            return stored

    def publish_version(self, trigger: Trigger) -> Trigger:
        """Publish the next immutable version of an existing trigger."""
        with self._lock:
            versions = self._versions.get(trigger.trigger_id)
            if versions is None:
                raise TriggerNotFound(f"unknown trigger_id {trigger.trigger_id!r}")
            expected = max(versions) + 1
            if trigger.version != expected:
                raise InvalidTriggerDefinition(
                    f"new version must be {expected}, got {trigger.version}"
                )
            stored = _with_status(trigger, "DRAFT")
            versions[stored.version] = stored
            self.save()
            return stored

    def get(self, trigger_id: str, version: Optional[int] = None) -> Trigger:
        """Return a specific version, or the latest published one."""
        with self._lock:
            versions = self._versions.get(trigger_id)
            if not versions:
                raise TriggerNotFound(f"unknown trigger_id {trigger_id!r}")
            if version is None:
                return versions[max(versions)]
            if version not in versions:
                raise TriggerNotFound(
                    f"trigger {trigger_id!r} has no version {version}"
                )
            return versions[version]

    def get_active(self, trigger_id: str) -> Optional[Trigger]:
        """Latest version that is currently ACTIVE, else None."""
        with self._lock:
            versions = self._versions.get(trigger_id)
            if not versions:
                return None
            for v in sorted(versions, reverse=True):
                if versions[v].status == "ACTIVE":
                    return versions[v]
            return None

    def list_triggers(
        self,
        *,
        work_id: Optional[str] = None,
        wp_id: Optional[str] = None,
        status: Optional[str] = None,
        trigger_type: Optional[str] = None,
    ) -> list[Trigger]:
        with self._lock:
            out: list[Trigger] = []
            for tid in sorted(self._versions):
                for v in sorted(self._versions[tid]):
                    t = self._versions[tid][v]
                    if work_id is not None and t.work_id != work_id:
                        continue
                    if wp_id is not None and t.wp_id != wp_id:
                        continue
                    if status is not None and t.status != status:
                        continue
                    if trigger_type is not None and t.trigger_type != trigger_type:
                        continue
                    out.append(t)
            return out

    def active_triggers(self) -> list[Trigger]:
        return [t for t in self.list_triggers(status="ACTIVE")]

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def set_status(self, trigger_id: str, version: int, new_status: str) -> Trigger:
        if new_status not in TRIGGER_STATUSES:
            raise InvalidTriggerDefinition(f"unknown status {new_status!r}")
        with self._lock:
            trigger = self.get(trigger_id, version)
            allowed = TRIGGER_TRANSITIONS.get(trigger.status, ())
            if new_status == trigger.status:
                return trigger
            if new_status not in allowed:
                raise InvalidTriggerDefinition(
                    f"illegal trigger lifecycle transition "
                    f"{trigger.status} -> {new_status} for {trigger_id} v{version}"
                )
            updated = _with_status(trigger, new_status)
            self._versions[trigger_id][version] = updated
            self._status[trigger_id] = new_status
            self.save()
            return updated

    def pause(self, trigger_id: str) -> Trigger:
        active = self._require_active(trigger_id)
        return self.set_status(active.trigger_id, active.version, "PAUSED")

    def resume(self, trigger_id: str) -> Trigger:
        with self._lock:
            versions = self._versions.get(trigger_id)
            if not versions:
                raise TriggerNotFound(f"unknown trigger_id {trigger_id!r}")
            for v in sorted(versions, reverse=True):
                if versions[v].status == "PAUSED":
                    return self.set_status(trigger_id, v, "ACTIVE")
            raise InvalidTriggerDefinition(
                f"trigger {trigger_id!r} has nothing paused to resume"
            )

    def disable(self, trigger_id: str) -> Trigger:
        with self._lock:
            versions = self._versions.get(trigger_id)
            if not versions:
                raise TriggerNotFound(f"unknown trigger_id {trigger_id!r}")
            target = None
            for v in sorted(versions, reverse=True):
                if versions[v].status in ("ACTIVE", "PAUSED", "READY"):
                    target = versions[v]
                    break
            if target is None:
                return versions[max(versions)]
            return self.set_status(trigger_id, target.version, "DISABLED")

    def _require_active(self, trigger_id: str) -> Trigger:
        active = self.get_active(trigger_id)
        if active is None:
            raise InvalidTriggerDefinition(
                f"trigger {trigger_id!r} has no ACTIVE version"
            )
        return active


def _with_status(trigger: Trigger, status: str) -> Trigger:
    """frozen dataclass -> rebuild with a new status/updated_at."""
    from dataclasses import replace

    return replace(trigger, status=status, updated_at=utcnow())


__all__ = ["TriggerRegistry", "TRIGGER_TRANSITIONS", "ImmutableTriggerVersion"]
