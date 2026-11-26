"""Connection-scoped append-only audit events for Cloud Drive pilot transactions."""
from __future__ import annotations
import hashlib
import json
import sqlite3
import time
import uuid
from typing import Any


class AuditWriteError(RuntimeError):
    """An audit event could not be durably appended."""


class AuditWriter:
    """Hash-chained audit records; external anchoring is still required for tamper evidence."""

    def __init__(self, database: str):
        self.database = database
        with self._connect() as db:
            self.ensure_schema(db)

    def _connect(self):
        db = sqlite3.connect(self.database, timeout=20, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=20000")
        return db

    @staticmethod
    def ensure_schema(conn: sqlite3.Connection) -> None:
        conn.execute("""CREATE TABLE IF NOT EXISTS audit_events(
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL UNIQUE,
            occurred_at INTEGER NOT NULL,
            actor_id TEXT NOT NULL,
            action TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id TEXT NOT NULL,
            outcome TEXT NOT NULL,
            detail_json TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL UNIQUE
        )""")

    @staticmethod
    def append_in_transaction(conn: sqlite3.Connection, *, actor_id: str, action: str,
                              resource_type: str, resource_id: str, outcome: str,
                              detail: dict[str, Any] | None = None) -> str:
        """Append using caller-owned transaction; never commits or opens another DB."""
        if not all(isinstance(v, str) and v.strip() for v in
                   (actor_id, action, resource_type, resource_id, outcome)):
            raise AuditWriteError("verified actor/action/resource/outcome fields are required")
        try:
            detail_json = json.dumps(detail or {}, sort_keys=True, separators=(",", ":"))
            event_id, now = uuid.uuid4().hex, int(time.time())
            previous = conn.execute(
                "SELECT event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            previous_hash = previous["event_hash"] if previous else "0" * 64
            canonical = json.dumps({
                "event_id": event_id, "occurred_at": now, "actor_id": actor_id,
                "action": action, "resource_type": resource_type, "resource_id": resource_id,
                "outcome": outcome, "detail_json": detail_json, "previous_hash": previous_hash,
            }, sort_keys=True, separators=(",", ":"))
            event_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            conn.execute("""INSERT INTO audit_events
                (event_id,occurred_at,actor_id,action,resource_type,resource_id,outcome,
                 detail_json,previous_hash,event_hash) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (event_id, now, actor_id, action, resource_type, resource_id, outcome,
                 detail_json, previous_hash, event_hash))
            return event_id
        except AuditWriteError:
            raise
        except Exception as exc:
            raise AuditWriteError("audit append failed; caller transaction must roll back") from exc

    def append(self, *, actor_id: str, action: str, resource_type: str,
               resource_id: str, outcome: str, detail: dict[str, Any] | None = None) -> str:
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            event_id = self.append_in_transaction(
                db, actor_id=actor_id, action=action, resource_type=resource_type,
                resource_id=resource_id, outcome=outcome, detail=detail,
            )
            db.commit()
        return event_id

    def verify_chain(self) -> bool:
        previous_hash = "0" * 64
        with self._connect() as db:
            rows = db.execute("SELECT * FROM audit_events ORDER BY sequence").fetchall()
        for row in rows:
            canonical = json.dumps({
                "event_id": row["event_id"], "occurred_at": row["occurred_at"],
                "actor_id": row["actor_id"], "action": row["action"],
                "resource_type": row["resource_type"], "resource_id": row["resource_id"],
                "outcome": row["outcome"], "detail_json": row["detail_json"],
                "previous_hash": previous_hash,
            }, sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            if row["previous_hash"] != previous_hash or row["event_hash"] != digest:
                return False
            previous_hash = digest
        return True
