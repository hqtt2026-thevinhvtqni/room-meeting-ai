"""Persistent task store (D-08) — restart-safe task state.

PersistentTaskStore writes the full task map to a JSON file with an atomic
rename on every update, and reloads it on construction. Restarting an agent
backend with the same store path restores task state, so continuation,
idempotency and audit survive process restarts.

Known limits (documented in DECISION_REGISTER D-08):
- single-process assumption: no cross-process locking; one writer per file.
- flush is O(n) per update: fine for slice scale, not for high throughput.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path


class TaskStoreError(Exception):
    """Raised when a persistent store file is corrupt."""


class TaskStore:
    """In-memory store (default). Thread-safe via lock."""

    def __init__(self) -> None:
        self._tasks: dict[str, dict] = {}
        self._lock = threading.Lock()

    def get(self, task_id: str) -> dict | None:
        with self._lock:
            return self._tasks.get(task_id)

    def set(self, task: dict) -> dict:
        with self._lock:
            self._tasks[task["id"]] = task
        return task

    def ids(self) -> list[str]:
        with self._lock:
            return list(self._tasks.keys())


class PersistentTaskStore(TaskStore):
    """JSON-file backed store with atomic flush on every update."""

    def __init__(self, path: str | Path):
        super().__init__()
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self._load()

    # -- load ---------------------------------------------------------------

    def _load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise TaskStoreError(f"corrupt task store at {self.path}: {exc}") from exc
        if not isinstance(data, dict):
            raise TaskStoreError(f"corrupt task store at {self.path}: not a JSON object")
        tasks = {}
        for task_id, task in data.items():
            if not isinstance(task, dict) or task.get("id") != task_id \
                    or "state" not in task:
                raise TaskStoreError(f"corrupt task store entry: {task_id!r}")
            tasks[task_id] = task
        with self._lock:
            self._tasks = tasks

    def reload(self) -> None:
        """Re-read from disk — simulates restart with the same file."""
        if self.path.exists():
            self._load()

    # -- write --------------------------------------------------------------

    def set(self, task: dict) -> dict:
        super().set(task)
        self._flush()
        return task

    def _flush(self) -> None:
        with self._lock:
            snapshot = {k: dict(v) for k, v in self._tasks.items()}
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        os.replace(tmp, self.path)
