"""SQLite-backed same-host rolling-window limiter for Core meeting pastes."""
from __future__ import annotations

import hashlib
import math
import sqlite3
import time
from pathlib import Path
from typing import Callable

MAX_PASTE_REQUESTS_PER_WINDOW = 100
PASTE_RATE_WINDOW_SECONDS = 60
LEGACY_UNIDENTIFIED_PRINCIPAL = "legacy:unidentified"


class PasteRateLimitExceeded(Exception):
    def __init__(self, retry_after_seconds: int):
        self.retry_after_seconds = max(1, int(retry_after_seconds))
        super().__init__(
            "RATE_LIMIT_EXCEEDED "
            f"retry_after_seconds={self.retry_after_seconds}"
        )


class PasteRateAdmission:
    """Owns a write transaction until append success is committed or rolled back."""

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._committed = False

    def __enter__(self) -> "PasteRateAdmission":
        return self

    def commit(self) -> None:
        self._connection.commit()
        self._committed = True

    def __exit__(self, exc_type, exc, traceback) -> None:
        try:
            if not self._committed:
                self._connection.rollback()
        finally:
            self._connection.close()


class SQLitePasteRateLimiter:
    """100 accepted pastes per resolved identity/meeting per rolling 60 seconds."""

    def __init__(
        self,
        database_path: str | Path,
        *,
        limit: int = MAX_PASTE_REQUESTS_PER_WINDOW,
        window_seconds: int = PASTE_RATE_WINDOW_SECONDS,
        clock: Callable[[], float] = time.time,
    ):
        if limit < 1 or window_seconds < 1:
            raise ValueError("limit and window_seconds must be positive")
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.limit = int(limit)
        self.window_seconds = int(window_seconds)
        self._clock = clock
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path, timeout=30, isolation_level=None
        )
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def _initialize(self) -> None:
        connection = self._connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS paste_rate_events (
                    meeting_id TEXT NOT NULL,
                    principal_key_hash TEXT NOT NULL,
                    accepted_at REAL NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_paste_rate_scope_time
                ON paste_rate_events (
                    meeting_id, principal_key_hash, accepted_at
                )
                """
            )
        finally:
            connection.close()

    @staticmethod
    def _principal_key_hash(principal_key: str) -> str:
        return hashlib.sha256(principal_key.encode("utf-8")).hexdigest()

    def admission(
        self, meeting_id: str, principal_key: str
    ) -> PasteRateAdmission:
        """Atomically reserve a slot; caller commits after raw append succeeds."""
        connection = self._connect()
        try:
            # BEGIN IMMEDIATE serializes check-and-insert across local processes.
            connection.execute("BEGIN IMMEDIATE")
            now = float(self._clock())
            cutoff = now - self.window_seconds
            connection.execute(
                "DELETE FROM paste_rate_events WHERE accepted_at <= ?",
                (cutoff,),
            )
            principal_hash = self._principal_key_hash(principal_key)
            events = connection.execute(
                """
                SELECT accepted_at FROM paste_rate_events
                WHERE meeting_id = ? AND principal_key_hash = ?
                  AND accepted_at > ?
                ORDER BY accepted_at ASC
                """,
                (meeting_id, principal_hash, cutoff),
            ).fetchall()
            if len(events) >= self.limit:
                retry = math.ceil(events[0][0] + self.window_seconds - now)
                connection.rollback()
                raise PasteRateLimitExceeded(retry)
            connection.execute(
                """
                INSERT INTO paste_rate_events
                    (meeting_id, principal_key_hash, accepted_at)
                VALUES (?, ?, ?)
                """,
                (meeting_id, principal_hash, now),
            )
            return PasteRateAdmission(connection)
        except Exception:
            try:
                if connection.in_transaction:
                    connection.rollback()
            finally:
                try:
                    connection.close()
                except Exception:
                    pass
            raise
