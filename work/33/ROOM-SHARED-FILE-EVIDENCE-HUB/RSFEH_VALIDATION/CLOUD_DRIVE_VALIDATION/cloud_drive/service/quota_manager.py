"""Transactional per-scope quota reservations for the Cloud Drive pilot."""
from __future__ import annotations

import sqlite3
import time
import uuid
from dataclasses import dataclass


class QuotaError(Exception):
    pass


class QuotaExceeded(QuotaError):
    pass


class ReservationNotFound(QuotaError):
    pass


@dataclass(frozen=True)
class QuotaSnapshot:
    scope_id: str
    limit_bytes: int
    used_bytes: int
    reserved_bytes: int

    @property
    def available_bytes(self) -> int:
        return max(0, self.limit_bytes - self.used_bytes - self.reserved_bytes)


class QuotaManager:
    """SQLite prototype; BEGIN IMMEDIATE serializes reservations on one host."""

    def __init__(self, database: str, *, default_limit_bytes: int):
        if default_limit_bytes < 0:
            raise ValueError("default quota cannot be negative")
        self.database = database
        self.default_limit_bytes = default_limit_bytes
        with self._connect() as db:
            self.ensure_schema(db)

    def _connect(self):
        db = sqlite3.connect(self.database, timeout=20, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=20000")
        return db

    @staticmethod
    def ensure_schema(conn: sqlite3.Connection) -> None:
        """Create quota tables on a caller-owned database connection."""
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS quota_accounts(
                scope_id TEXT PRIMARY KEY,
                limit_bytes INTEGER NOT NULL CHECK(limit_bytes >= 0),
                used_bytes INTEGER NOT NULL DEFAULT 0 CHECK(used_bytes >= 0)
            );
            CREATE TABLE IF NOT EXISTS quota_reservations(
                reservation_id TEXT PRIMARY KEY,
                scope_id TEXT NOT NULL REFERENCES quota_accounts(scope_id),
                bytes INTEGER NOT NULL CHECK(bytes > 0),
                state TEXT NOT NULL CHECK(state IN ('HELD','COMMITTED','RELEASED')),
                actual_bytes INTEGER,
                created_at INTEGER NOT NULL
            );
        """)
        columns = {r["name"] for r in conn.execute("PRAGMA table_info(quota_reservations)")}
        if "actual_bytes" not in columns:
            conn.execute("ALTER TABLE quota_reservations ADD COLUMN actual_bytes INTEGER")

    def reserve_in_transaction(self, conn: sqlite3.Connection, scope_id: str, amount: int) -> str:
        if amount <= 0:
            raise ValueError("reservation must be positive")
        row = conn.execute("SELECT * FROM quota_accounts WHERE scope_id=?", (scope_id,)).fetchone()
        if row is None:
            conn.execute("INSERT INTO quota_accounts(scope_id,limit_bytes,used_bytes) VALUES(?,?,0)",
                         (scope_id, self.default_limit_bytes))
            limit_bytes, used_bytes = self.default_limit_bytes, 0
        else:
            limit_bytes, used_bytes = row["limit_bytes"], row["used_bytes"]
        held = conn.execute("""SELECT COALESCE(SUM(bytes),0) n FROM quota_reservations
            WHERE scope_id=? AND state='HELD'""", (scope_id,)).fetchone()["n"]
        if used_bytes + held + amount > limit_bytes:
            raise QuotaExceeded("quota would be exceeded")
        rid = uuid.uuid4().hex
        conn.execute("""INSERT INTO quota_reservations
            (reservation_id,scope_id,bytes,state,actual_bytes,created_at)
            VALUES(?,?,?,'HELD',NULL,?)""", (rid, scope_id, amount, int(time.time())))
        return rid

    @staticmethod
    def commit_in_transaction(conn: sqlite3.Connection, reservation_id: str, *, actual_bytes: int) -> None:
        if actual_bytes < 0:
            raise ValueError("actual_bytes cannot be negative")
        row = conn.execute("SELECT * FROM quota_reservations WHERE reservation_id=?",
                           (reservation_id,)).fetchone()
        if row is None:
            raise ReservationNotFound(reservation_id)
        if row["state"] == "COMMITTED":
            if row["actual_bytes"] == actual_bytes:
                return
            raise QuotaError("reservation already committed with a different amount")
        if row["state"] != "HELD" or actual_bytes > row["bytes"]:
            raise QuotaError("reservation is not held or actual size exceeds reservation")
        conn.execute("UPDATE quota_accounts SET used_bytes=used_bytes+? WHERE scope_id=?",
                     (actual_bytes, row["scope_id"]))
        conn.execute("UPDATE quota_reservations SET state='COMMITTED',actual_bytes=? WHERE reservation_id=?",
                     (actual_bytes, reservation_id))

    @staticmethod
    def release_in_transaction(conn: sqlite3.Connection, reservation_id: str) -> None:
        row = conn.execute("SELECT state FROM quota_reservations WHERE reservation_id=?",
                           (reservation_id,)).fetchone()
        if row is None:
            raise ReservationNotFound(reservation_id)
        if row["state"] == "COMMITTED":
            raise QuotaError("committed usage needs a separately audited adjustment")
        conn.execute("UPDATE quota_reservations SET state='RELEASED' WHERE reservation_id=?",
                     (reservation_id,))

    def configure_scope(self, scope_id: str, *, limit_bytes: int, used_bytes: int | None = None):
        """Create a scope or change its limit without silently resetting recorded usage."""
        if not scope_id or limit_bytes < 0 or (used_bytes is not None and used_bytes < 0):
            raise ValueError("invalid scope quota")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT used_bytes FROM quota_accounts WHERE scope_id=?",
                             (scope_id,)).fetchone()
            if row is None:
                actual_used = 0 if used_bytes is None else used_bytes
                db.execute("INSERT INTO quota_accounts(scope_id,limit_bytes,used_bytes) VALUES(?,?,?)",
                           (scope_id, limit_bytes, actual_used))
            else:
                actual_used = row["used_bytes"]
                if used_bytes is not None and used_bytes != actual_used:
                    db.rollback()
                    raise QuotaError("usage cannot be overwritten through configuration; use an audited adjustment")
                db.execute("UPDATE quota_accounts SET limit_bytes=? WHERE scope_id=?",
                           (limit_bytes, scope_id))
            held = db.execute("""SELECT COALESCE(SUM(bytes),0) n FROM quota_reservations
                WHERE scope_id=? AND state='HELD'""", (scope_id,)).fetchone()["n"]
            if actual_used + held > limit_bytes:
                db.rollback()
                raise QuotaExceeded("new limit is below used plus reserved bytes")
            db.commit()

    def reserve(self, scope_id: str, amount: int) -> str:
        if amount <= 0:
            raise ValueError("reservation must be positive")
        rid = uuid.uuid4().hex
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM quota_accounts WHERE scope_id=?", (scope_id,)).fetchone()
            if row is None:
                db.execute("INSERT INTO quota_accounts(scope_id,limit_bytes,used_bytes) VALUES(?,?,0)",
                           (scope_id, self.default_limit_bytes))
                limit_bytes, used_bytes = self.default_limit_bytes, 0
            else:
                limit_bytes, used_bytes = row["limit_bytes"], row["used_bytes"]
            held = db.execute("""SELECT COALESCE(SUM(bytes),0) n FROM quota_reservations
                WHERE scope_id=? AND state='HELD'""", (scope_id,)).fetchone()["n"]
            if used_bytes + held + amount > limit_bytes:
                db.rollback()
                raise QuotaExceeded("quota would be exceeded")
            db.execute("""INSERT INTO quota_reservations
                (reservation_id,scope_id,bytes,state,actual_bytes,created_at)
                VALUES(?,?,?,'HELD',NULL,?)""", (rid, scope_id, amount, int(time.time())))
            db.commit()
        return rid

    def commit(self, reservation_id: str, *, actual_bytes: int):
        if actual_bytes < 0:
            raise ValueError("actual_bytes cannot be negative")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM quota_reservations WHERE reservation_id=?",
                             (reservation_id,)).fetchone()
            if row is None:
                db.rollback()
                raise ReservationNotFound(reservation_id)
            if row["state"] == "COMMITTED":
                if row["actual_bytes"] == actual_bytes:
                    db.commit()
                    return
                db.rollback()
                raise QuotaError("reservation already committed with a different amount")
            if row["state"] != "HELD" or actual_bytes > row["bytes"]:
                db.rollback()
                raise QuotaError("reservation is not held or actual size exceeds reservation")
            db.execute("UPDATE quota_accounts SET used_bytes=used_bytes+? WHERE scope_id=?",
                       (actual_bytes, row["scope_id"]))
            db.execute("UPDATE quota_reservations SET state='COMMITTED',actual_bytes=? WHERE reservation_id=?",
                       (actual_bytes, reservation_id))
            db.commit()

    def release(self, reservation_id: str):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT state FROM quota_reservations WHERE reservation_id=?",
                             (reservation_id,)).fetchone()
            if row is None:
                db.rollback()
                raise ReservationNotFound(reservation_id)
            if row["state"] == "COMMITTED":
                db.rollback()
                raise QuotaError("committed usage needs a separately audited adjustment")
            db.execute("UPDATE quota_reservations SET state='RELEASED' WHERE reservation_id=?",
                       (reservation_id,))
            db.commit()

    def snapshot(self, scope_id: str) -> QuotaSnapshot:
        with self._connect() as db:
            row = db.execute("SELECT * FROM quota_accounts WHERE scope_id=?", (scope_id,)).fetchone()
            if row is None:
                return QuotaSnapshot(scope_id, self.default_limit_bytes, 0, 0)
            held = db.execute("""SELECT COALESCE(SUM(bytes),0) n FROM quota_reservations
                WHERE scope_id=? AND state='HELD'""", (scope_id,)).fetchone()["n"]
            return QuotaSnapshot(scope_id, row["limit_bytes"], row["used_bytes"], held)
