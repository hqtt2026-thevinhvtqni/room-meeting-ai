"""SQLite-backed same-host rolling-window limiter for Core meeting pastes."""
from __future__ import annotations

import hashlib
import math
import sqlite3
import time
import uuid
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


class PasteRateStoreUnavailable(Exception):
    """The local quota store could not complete an atomic reservation."""

    def __init__(self, retry_after_seconds: int = 1):
        self.retry_after_seconds = max(1, int(retry_after_seconds))
        super().__init__("PASTE_RATE_STORE_UNAVAILABLE")


class PasteRateAdmission:
    """A committed short-lived reservation, compensated unless append succeeds."""

    def __init__(self, limiter: "SQLitePasteRateLimiter", event_id: str):
        self._limiter = limiter
        self._event_id = event_id
        self._committed = False

    def __enter__(self) -> "PasteRateAdmission":
        return self

    def commit(self) -> None:
        # The reservation transaction is already committed before this context
        # is returned. This only confirms that the transcript append succeeded.
        self._committed = True

    def __exit__(self, exc_type, exc, traceback) -> None:
        if not self._committed:
            self._limiter._compensate(self._event_id)


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
                    accepted_at REAL NOT NULL,
                    event_id TEXT
                )
                """
            )
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(paste_rate_events)"
                ).fetchall()
            }
            if "event_id" not in columns:
                connection.execute(
                    "ALTER TABLE paste_rate_events ADD COLUMN event_id TEXT"
                )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_paste_rate_scope_time
                ON paste_rate_events (
                    meeting_id, principal_key_hash, accepted_at
                )
                """
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_paste_rate_event_id
                ON paste_rate_events (event_id)
                WHERE event_id IS NOT NULL
                """
            )
        finally:
            connection.close()

    @staticmethod
    def _principal_key_hash(principal_key: str) -> str:
        return hashlib.sha256(principal_key.encode("utf-8")).hexdigest()

    def _compensate(self, event_id: str) -> None:
        """Delete only the reservation created by the failed append."""
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "DELETE FROM paste_rate_events WHERE event_id = ?",
                (event_id,),
            )
            connection.commit()
        except sqlite3.OperationalError:
            try:
                if connection.in_transaction:
                    connection.rollback()
            finally:
                connection.close()
            raise PasteRateStoreUnavailable() from None
        finally:
            try:
                connection.close()
            except Exception:
                pass

    def admission(
        self, meeting_id: str, principal_key: str
    ) -> PasteRateAdmission:
        """Commit a quota reservation, then let caller append outside the DB lock."""
        connection = self._connect()
        event_id = uuid.uuid4().hex
        try:
            # Only the check + reservation are inside BEGIN IMMEDIATE.
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
                    (meeting_id, principal_key_hash, accepted_at, event_id)
                VALUES (?, ?, ?, ?)
                """,
                (meeting_id, principal_hash, now, event_id),
            )
            connection.commit()
            return PasteRateAdmission(self, event_id)
        except PasteRateLimitExceeded:
            raise
        except sqlite3.OperationalError:
            if connection.in_transaction:
                connection.rollback()
            raise PasteRateStoreUnavailable() from None
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()
