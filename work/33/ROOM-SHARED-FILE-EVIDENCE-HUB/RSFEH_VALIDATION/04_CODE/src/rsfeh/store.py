"""Content-addressable store + SQLite catalog for RSFEH."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class RSFEHError(Exception):
    """Base error with stable code for CLI."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _sanitize_name(name: str) -> str:
    base = os.path.basename(name.replace("\\", "/"))
    if not base or base in (".", "..") or "\x00" in base:
        raise RSFEHError("INVALID_NAME", f"Invalid original name: {name!r}")
    return base


class Store:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.blobs = self.root / "blobs"
        self.db_path = self.root / "meta.db"
        self.audit_path = self.root / "audit.jsonl"
        self._conn: Optional[sqlite3.Connection] = None

    def init(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.blobs.mkdir(parents=True, exist_ok=True)
        conn = self._get_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS files (
                file_id TEXT PRIMARY KEY,
                sha256 TEXT NOT NULL UNIQUE,
                original_name TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                media_type TEXT,
                work_id TEXT,
                evidence_ref TEXT,
                agent TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                notes TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_files_sha ON files(sha256);
            CREATE INDEX IF NOT EXISTS idx_files_work ON files(work_id);
            CREATE INDEX IF NOT EXISTS idx_files_name ON files(original_name);
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                agent TEXT NOT NULL,
                action TEXT NOT NULL,
                file_id TEXT,
                result TEXT NOT NULL,
                detail TEXT,
                sha256 TEXT
            );
            """
        )
        conn.commit()
        self._audit("system", "init", None, "ok", {"root": str(self.root)}, None)

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            if not self.root.exists():
                raise RSFEHError("NOT_INITIALIZED", f"Store not initialized: {self.root}")
            self._conn = sqlite3.connect(str(self.db_path), isolation_level=None)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA journal_mode=WAL")
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _audit(
        self,
        agent: str,
        action: str,
        file_id: Optional[str],
        result: str,
        detail: Any,
        sha256: Optional[str],
    ) -> None:
        ts = _utc_now()
        detail_s = json.dumps(detail, ensure_ascii=False) if not isinstance(detail, str) else detail
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO audit_events (ts, agent, action, file_id, result, detail, sha256) VALUES (?,?,?,?,?,?,?)",
            (ts, agent, action, file_id, result, detail_s, sha256),
        )
        line = {
            "ts": ts,
            "agent": agent,
            "action": action,
            "file_id": file_id,
            "result": result,
            "detail": detail if not isinstance(detail, str) else detail,
            "sha256": sha256,
        }
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    def put(
        self,
        data: bytes,
        original_name: str,
        agent: str = "system",
        media_type: Optional[str] = None,
        work_id: Optional[str] = None,
        evidence_ref: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        name = _sanitize_name(original_name)
        if not isinstance(data, (bytes, bytearray)):
            raise RSFEHError("INVALID_DATA", "data must be bytes")
        sha = hashlib.sha256(data).hexdigest()
        size = len(data)
        blob_path = self.blobs / sha

        conn = self._get_conn()
        # Dedup: if same hash already active, return existing
        row = conn.execute(
            "SELECT * FROM files WHERE sha256=? AND status='active'", (sha,)
        ).fetchone()
        if row is not None:
            self._audit(agent, "put", row["file_id"], "ok", {"dedup": True, "name": name}, sha)
            return dict(row)

        file_id = str(uuid.uuid4())
        created = _utc_now()
        try:
            # Write blob first (idempotent)
            if not blob_path.exists():
                tmp = blob_path.with_suffix(".tmp")
                tmp.write_bytes(data)
                tmp.replace(blob_path)
            conn.execute("BEGIN")
            conn.execute(
                """INSERT INTO files
                   (file_id, sha256, original_name, size_bytes, media_type, work_id,
                    evidence_ref, agent, created_at, status, notes)
                   VALUES (?,?,?,?,?,?,?,?,?,'active',?)""",
                (
                    file_id,
                    sha,
                    name,
                    size,
                    media_type,
                    work_id,
                    evidence_ref,
                    agent,
                    created,
                    notes,
                ),
            )
            conn.execute("COMMIT")
        except Exception as e:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            self._audit(agent, "put", file_id, "error", str(e), sha)
            raise RSFEHError("PUT_FAILED", str(e)) from e

        self._audit(
            agent,
            "put",
            file_id,
            "ok",
            {"name": name, "size": size, "work_id": work_id},
            sha,
        )
        return {
            "file_id": file_id,
            "sha256": sha,
            "original_name": name,
            "size_bytes": size,
            "media_type": media_type,
            "work_id": work_id,
            "evidence_ref": evidence_ref,
            "agent": agent,
            "created_at": created,
            "status": "active",
            "notes": notes,
        }

    def get_bytes(self, file_id: str, agent: str = "system") -> bytes:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM files WHERE file_id=? AND status='active'", (file_id,)
        ).fetchone()
        if row is None:
            self._audit(agent, "get", file_id, "error", "NOT_FOUND", None)
            raise RSFEHError("NOT_FOUND", f"file_id not found or deleted: {file_id}")
        blob = self.blobs / row["sha256"]
        if not blob.exists():
            self._audit(agent, "get", file_id, "error", "BLOB_MISSING", row["sha256"])
            raise RSFEHError("BLOB_MISSING", f"Blob missing for {file_id}")
        data = blob.read_bytes()
        self._audit(agent, "get", file_id, "ok", {"size": len(data)}, row["sha256"])
        return data

    def get_meta(self, file_id: str) -> dict:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM files WHERE file_id=?", (file_id,)).fetchone()
        if row is None:
            raise RSFEHError("NOT_FOUND", f"file_id not found: {file_id}")
        return dict(row)

    def list_files(
        self,
        work_id: Optional[str] = None,
        status: str = "active",
        limit: int = 100,
    ) -> list[dict]:
        conn = self._get_conn()
        if work_id:
            rows = conn.execute(
                "SELECT * FROM files WHERE status=? AND work_id=? ORDER BY created_at DESC LIMIT ?",
                (status, work_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM files WHERE status=? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def search(
        self,
        query: str,
        work_id: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        conn = self._get_conn()
        q = f"%{query}%"
        if work_id:
            rows = conn.execute(
                """SELECT * FROM files WHERE status='active' AND work_id=?
                   AND (original_name LIKE ? OR sha256 LIKE ? OR file_id LIKE ? OR notes LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (work_id, q, q, q, q, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM files WHERE status='active'
                   AND (original_name LIKE ? OR sha256 LIKE ? OR file_id LIKE ? OR notes LIKE ?
                        OR IFNULL(work_id,'') LIKE ? OR IFNULL(evidence_ref,'') LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (q, q, q, q, q, q, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def verify(self, file_id: str, agent: str = "system") -> dict:
        meta = self.get_meta(file_id)
        if meta["status"] != "active":
            self._audit(agent, "verify", file_id, "error", "DELETED", meta.get("sha256"))
            raise RSFEHError("DELETED", f"File is deleted: {file_id}")
        blob = self.blobs / meta["sha256"]
        if not blob.exists():
            self._audit(agent, "verify", file_id, "error", "BLOB_MISSING", meta["sha256"])
            raise RSFEHError("BLOB_MISSING", f"Blob missing: {file_id}")
        data = blob.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        ok = actual == meta["sha256"] and len(data) == meta["size_bytes"]
        result = "ok" if ok else "error"
        detail = {
            "expected_sha": meta["sha256"],
            "actual_sha": actual,
            "expected_size": meta["size_bytes"],
            "actual_size": len(data),
            "match": ok,
        }
        self._audit(agent, "verify", file_id, result, detail, meta["sha256"])
        if not ok:
            raise RSFEHError("INTEGRITY_FAIL", f"Integrity check failed for {file_id}")
        return detail

    def link_work(
        self,
        file_id: str,
        work_id: str,
        evidence_ref: Optional[str] = None,
        agent: str = "system",
    ) -> dict:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM files WHERE file_id=? AND status='active'", (file_id,)
        ).fetchone()
        if row is None:
            self._audit(agent, "link", file_id, "error", "NOT_FOUND", None)
            raise RSFEHError("NOT_FOUND", f"file_id not found: {file_id}")
        conn.execute(
            "UPDATE files SET work_id=?, evidence_ref=COALESCE(?, evidence_ref) WHERE file_id=?",
            (work_id, evidence_ref, file_id),
        )
        self._audit(
            agent,
            "link",
            file_id,
            "ok",
            {"work_id": work_id, "evidence_ref": evidence_ref},
            row["sha256"],
        )
        return self.get_meta(file_id)

    def soft_delete(self, file_id: str, agent: str = "system") -> None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM files WHERE file_id=?", (file_id,)).fetchone()
        if row is None:
            raise RSFEHError("NOT_FOUND", f"file_id not found: {file_id}")
        conn.execute("UPDATE files SET status='deleted' WHERE file_id=?", (file_id,))
        self._audit(agent, "delete", file_id, "ok", {"soft": True}, row["sha256"])

    def audit_tail(self, limit: int = 50) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM audit_events ORDER BY event_id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in reversed(rows)]
