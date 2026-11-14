"""Work 76 trigger registry with single-ACTIVE-version invariant.

Implements DOC-004 lifecycle invariants:
- at most one ACTIVE version per trigger_id; activation atomically retires
  the previous ACTIVE version (regression W76-RG-001),
- expected-revision compare-and-swap for state changes,
- pause/resume/disable transitions with persistence round-trip consistency
  (W76-RG-002).
"""

from __future__ import annotations

from typing import Any, Mapping

from .errors import ConcurrencyError, RegistryError, StateError, ValidationError
from .models import Trigger

VALID_TRANSITIONS = {
    "DRAFT": {"ACTIVE", "DISABLED"},
    "ACTIVE": {"PAUSED", "DISABLED", "RETIRED"},
    "PAUSED": {"ACTIVE", "DISABLED"},
    "DISABLED": set(),
    "RETIRED": set(),
}


class TriggerRegistry:
    """In-memory canonical registry with JSON round-trip support."""

    def __init__(self) -> None:
        self._triggers: dict[tuple[str, int], Trigger] = {}

    # -- helpers ---------------------------------------------------------
    def _get(self, trigger_id: str, version: int) -> Trigger:
        trigger = self._triggers.get((trigger_id, version))
        if trigger is None:
            raise RegistryError(f"trigger not found: {trigger_id} v{version}")
        return trigger

    def _check_revision(self, trigger: Trigger, expected_revision: int | None) -> None:
        if expected_revision is not None and trigger.revision != expected_revision:
            raise ConcurrencyError(
                f"revision conflict for {trigger.trigger_id} v{trigger.version}: "
                f"expected {expected_revision}, actual {trigger.revision}"
            )

    def _active(self, trigger_id: str) -> Trigger | None:
        actives = self.active_triggers(trigger_id=trigger_id)
        return actives[0] if actives else None

    def _commit(self, updated: list[Trigger]) -> None:
        for trigger in updated:
            self._triggers[(trigger.trigger_id, trigger.version)] = trigger

    # -- public API ------------------------------------------------------
    def publish(self, trigger: Trigger) -> Trigger:
        if not isinstance(trigger, Trigger):
            raise ValidationError("publish expects a Trigger instance")
        key = (trigger.trigger_id, trigger.version)
        if key in self._triggers:
            raise RegistryError(f"trigger version already exists: {trigger.trigger_id} v{trigger.version}")
        if trigger.status != "DRAFT":
            raise StateError("new versions must be published as DRAFT")
        self._triggers[key] = trigger
        return trigger

    def activate(self, trigger_id: str, version: int, expected_revision: int | None = None) -> Trigger:
        trigger = self._get(trigger_id, version)
        self._check_revision(trigger, expected_revision)
        if trigger.status not in ("DRAFT", "PAUSED"):
            raise StateError(f"cannot activate from status {trigger.status}")
        updates = [trigger.with_status("ACTIVE", trigger.revision + 1)]
        current = self._active(trigger_id)
        if current is not None and current.version != version:
            # Atomic single-ACTIVE invariant: retire the previous ACTIVE
            # version in the same commit (W76-RG-001).
            updates.append(current.with_status("RETIRED", current.revision + 1))
        self._commit(updates)
        return updates[0]

    def pause(self, trigger_id: str, version: int, expected_revision: int | None = None) -> Trigger:
        trigger = self._get(trigger_id, version)
        self._check_revision(trigger, expected_revision)
        if "PAUSED" not in VALID_TRANSITIONS[trigger.status]:
            raise StateError(f"cannot pause from status {trigger.status}")
        updated = trigger.with_status("PAUSED", trigger.revision + 1)
        self._commit([updated])
        return updated

    def resume(self, trigger_id: str, version: int, expected_revision: int | None = None) -> Trigger:
        trigger = self._get(trigger_id, version)
        self._check_revision(trigger, expected_revision)
        if "ACTIVE" not in VALID_TRANSITIONS[trigger.status]:
            raise StateError(f"cannot resume from status {trigger.status}")
        current = self._active(trigger_id)
        if current is not None and current.version != version:
            raise StateError(
                f"another version ({current.version}) is ACTIVE; retire it before resuming v{version}"
            )
        updated = trigger.with_status("ACTIVE", trigger.revision + 1)
        self._commit([updated])
        return updated

    def disable(self, trigger_id: str, version: int, expected_revision: int | None = None) -> Trigger:
        trigger = self._get(trigger_id, version)
        self._check_revision(trigger, expected_revision)
        if "DISABLED" not in VALID_TRANSITIONS[trigger.status]:
            raise StateError(f"cannot disable from status {trigger.status}")
        updated = trigger.with_status("DISABLED", trigger.revision + 1)
        self._commit([updated])
        return updated

    def get(self, trigger_id: str, version: int) -> Trigger:
        return self._get(trigger_id, version)

    def active_triggers(self, trigger_id: str | None = None) -> list[Trigger]:
        """All ACTIVE versions; at most one per trigger_id by invariant."""
        result: list[Trigger] = []
        seen: set[str] = set()
        for (tid, _version), trigger in sorted(self._triggers.items()):
            if trigger_id is not None and tid != trigger_id:
                continue
            if trigger.status == "ACTIVE" and tid not in seen:
                seen.add(tid)
                result.append(trigger)
        return result

    def list_triggers(self, trigger_id: str | None = None) -> list[Trigger]:
        return [
            trigger
            for (tid, _version), trigger in sorted(self._triggers.items())
            if trigger_id is None or tid == trigger_id
        ]

    # -- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "triggers": [trigger.to_dict() for trigger in self.list_triggers()],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TriggerRegistry":
        registry = cls()
        for item in data.get("triggers", []):
            trigger = Trigger.from_dict(item)
            # Restore persisted state directly; publish() only accepts DRAFT.
            registry._triggers[(trigger.trigger_id, trigger.version)] = trigger
        return registry
