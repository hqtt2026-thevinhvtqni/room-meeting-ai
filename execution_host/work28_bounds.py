"""WP20 — Hard bounds for Work 28 snapshot execution (fail-closed).

Does not open MCP tools. Isolation remains NOT_VERIFIED.
"""
from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Iterator

MAX_SNAPSHOT_BYTES = 1_048_576  # 1 MiB
MAX_OUTPUT_CHARS = 32_768
MAX_GLOBAL_CONCURRENT = 2

_global_sem = threading.Semaphore(MAX_GLOBAL_CONCURRENT)
_work_locks: dict[str, threading.Lock] = {}
_work_locks_guard = threading.Lock()


class BoundsError(ValueError):
    """Input or output exceeded configured bound."""


def assert_snapshot_size(path_size: int) -> None:
    if path_size < 0 or path_size > MAX_SNAPSHOT_BYTES:
        raise BoundsError("snapshot_too_large")


def truncate_output(text: object, *, limit: int = MAX_OUTPUT_CHARS) -> str:
    if text is None:
        return ""
    s = text if isinstance(text, str) else str(text)
    if len(s) <= limit:
        return s
    return s[:limit] + "\n...[truncated]..."


def _lock_for_work(work_id: str) -> threading.Lock:
    with _work_locks_guard:
        lock = _work_locks.get(work_id)
        if lock is None:
            lock = threading.Lock()
            _work_locks[work_id] = lock
        return lock


@contextmanager
def execution_slot(work_id: str) -> Iterator[None]:
    """Acquire global concurrency slot + exclusive per-work lock."""
    if not isinstance(work_id, str) or not work_id:
        raise BoundsError("work_id_required_for_slot")
    work_lock = _lock_for_work(work_id)
    if not _global_sem.acquire(blocking=True, timeout=30):
        raise BoundsError("global_concurrency_saturated")
    acquired_work = work_lock.acquire(blocking=True, timeout=30)
    if not acquired_work:
        _global_sem.release()
        raise BoundsError("work_concurrency_saturated")
    try:
        yield
    finally:
        work_lock.release()
        _global_sem.release()


__all__ = [
    "MAX_SNAPSHOT_BYTES",
    "MAX_OUTPUT_CHARS",
    "MAX_GLOBAL_CONCURRENT",
    "BoundsError",
    "assert_snapshot_size",
    "truncate_output",
    "execution_slot",
]
