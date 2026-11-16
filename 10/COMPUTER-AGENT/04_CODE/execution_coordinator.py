"""Process-wide execution lease for the single browser-control service.

A lease covers adapter construction, runtime execution, and adapter shutdown.
It is intentionally non-blocking: concurrent HTTP requests are rejected rather
than creating competing browser sessions.
"""
from __future__ import annotations

import threading


class ExecutionCoordinator:
    def __init__(self) -> None:
        self._lock = threading.Lock()

    def try_acquire(self) -> bool:
        return self._lock.acquire(blocking=False)

    def release(self) -> None:
        if self._lock.locked():
            self._lock.release()

    @property
    def busy(self) -> bool:
        return self._lock.locked()
