"""Read-only upload recovery reconciliation.

This module reports database/filesystem inconsistencies and optional provider
state. It never deletes, rewrites, promotes, or repairs data.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
import time
from pathlib import Path
from typing import Any

from ..storage.protocol import ObjectRef

_SESSION_ID = re.compile(r"^[A-Za-z0-9_-]{32,64}$")
_PART_NAME = re.compile(r"^part-(\d{5})\.bin$")


class RecoveryInspector:
    def __init__(self, database: str, staging_root: str, storage: Any | None = None):
        self.database = Path(database)
        root = Path(staging_root)
        if root.exists() and root.is_symlink():
            raise ValueError("staging root cannot be a symlink")
        root.mkdir(parents=True, exist_ok=True)
        self.staging_root = root.resolve(strict=True)
        if not self.staging_root.is_dir():
            raise ValueError("staging root must be a directory")
        self.storage = storage

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        return db

    @staticmethod
    def _finding(kind: str, session_id: str, severity: str = "REVIEW",
                 **details: Any) -> dict[str, Any]:
        return {"kind": kind, "severity": severity, "session_id": session_id, **details}

    def inspect(self, *, now: int | None = None) -> list[dict[str, Any]]:
        timestamp = int(time.time()) if now is None else now
        db = self._connect()
        try:
            columns = {row["name"] for row in db.execute("PRAGMA table_info(upload_sessions)")}
            commit_sha_expr = "commit_sha256" if "commit_sha256" in columns else "NULL AS commit_sha256"
            commit_size_expr = "commit_size" if "commit_size" in columns else "NULL AS commit_size"
            sessions = db.execute(
                "SELECT session_id, scope_id, object_key, status, expires_at, "
                "expected_size, expected_sha256, completed_size, completed_sha256, "
                + commit_sha_expr + ", " + commit_size_expr + " FROM upload_sessions"
            ).fetchall()
            parts_by_session: dict[str, list[sqlite3.Row]] = {}
            for part in db.execute(
                "SELECT session_id, part_number, size_bytes, sha256 FROM upload_parts "
                "ORDER BY session_id, part_number"
            ):
                parts_by_session.setdefault(part["session_id"], []).append(part)
        finally:
            db.close()

        findings: list[dict[str, Any]] = []
        known: set[str] = set()
        for row in sessions:
            sid = row["session_id"]
            if not isinstance(sid, str) or not _SESSION_ID.fullmatch(sid):
                findings.append(self._finding("INVALID_SESSION_ID", "[redacted]", "CRITICAL"))
                continue
            known.add(sid)
            path = self.staging_root / sid
            if path.is_symlink():
                findings.append(self._finding("STAGING_SYMLINK", sid, "CRITICAL"))
                continue
            if path.exists() and not path.is_dir():
                findings.append(self._finding("STAGING_NOT_DIRECTORY", sid, "CRITICAL"))
                continue
            status = row["status"]
            parts = parts_by_session.get(sid, [])

            if status in {"CREATED", "UPLOADING", "OPEN", "VERIFYING", "COMMITTING", "RECOVERY_REQUIRED"} and not path.is_dir():
                findings.append(self._finding("MISSING_STAGING_DIRECTORY", sid, "HIGH", status=status))
            if status in {"UPLOADING", "OPEN"} and row["expires_at"] < timestamp:
                findings.append(self._finding("EXPIRED_OPEN_SESSION", sid, "REVIEW", status=status))
            if status in {"VERIFYING", "COMMITTING", "RECOVERY_REQUIRED"}:
                findings.append(self._finding("NON_TERMINAL_RECOVERY_STATE", sid, "HIGH", status=status))
            if status == "COMPLETED":
                if row["completed_size"] is None or not row["completed_sha256"]:
                    findings.append(self._finding("COMPLETED_METADATA_INCOMPLETE", sid, "CRITICAL"))
                elif row["completed_size"] != row["expected_size"]:
                    findings.append(self._finding("COMPLETED_SIZE_MISMATCH", sid, "CRITICAL"))
                elif row["expected_sha256"] and row["completed_sha256"] != row["expected_sha256"]:
                    findings.append(self._finding("COMPLETED_DIGEST_MISMATCH", sid, "CRITICAL"))

            if path.is_dir():
                metadata = {p["part_number"]: p for p in parts}
                seen_parts: set[int] = set()
                for entry in path.iterdir():
                    if entry.is_symlink():
                        findings.append(self._finding("STAGING_SYMLINK_ENTRY", sid, "CRITICAL", entry=entry.name))
                        continue
                    match = _PART_NAME.fullmatch(entry.name)
                    if match:
                        number = int(match.group(1))
                        seen_parts.add(number)
                        if not entry.is_file():
                            findings.append(self._finding("PART_NOT_REGULAR_FILE", sid, "CRITICAL", part_number=number))
                            continue
                        part_meta = metadata.get(number)
                        if part_meta is None:
                            findings.append(self._finding("ORPHAN_PART_FILE", sid, "HIGH", part_number=number))
                            continue
                        digest = hashlib.sha256()
                        size = 0
                        with entry.open("rb") as stream:
                            while True:
                                chunk = stream.read(1024 * 1024)
                                if not chunk:
                                    break
                                size += len(chunk)
                                digest.update(chunk)
                        if size != part_meta["size_bytes"] or digest.hexdigest() != part_meta["sha256"]:
                            findings.append(self._finding("PART_CONTENT_MISMATCH", sid, "CRITICAL", part_number=number))
                    elif entry.name.startswith(".part-") or entry.name.startswith(".assembled-"):
                        findings.append(self._finding("TEMPORARY_STAGING_FILE", sid, "REVIEW", entry=entry.name))
                    else:
                        findings.append(self._finding("UNKNOWN_STAGING_ENTRY", sid, "REVIEW", entry=entry.name))

                for number in metadata.keys() - seen_parts:
                    findings.append(self._finding("PART_METADATA_WITHOUT_FILE", sid, "CRITICAL", part_number=number))

            if status == "COMMITTING":
                commit_digest = row["commit_sha256"]
                commit_size = row["commit_size"]
                if (not isinstance(commit_digest, str)
                        or not re.fullmatch(r"[a-f0-9]{64}", commit_digest)
                        or not isinstance(commit_size, int)
                        or commit_size < 0):
                    findings.append(self._finding(
                        "COMMITTING_COMMITMENT_MISSING_OR_INVALID", sid, "CRITICAL",
                        commit_size=commit_size, has_commit_digest=bool(commit_digest)))
                elif self.storage is not None:
                    try:
                        provider_object = self.storage.head(ObjectRef(row["object_key"]))
                        provider_hash = getattr(provider_object, "sha256", None)
                        if not isinstance(provider_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", provider_hash):
                            findings.append(self._finding(
                                "COMMITTING_PROVIDER_OBJECT_UNCONFIRMED", sid, "HIGH",
                                reason="PROVIDER_DIGEST_UNAVAILABLE",
                                provider_size=provider_object.size_bytes))
                        elif provider_object.size_bytes != commit_size or provider_hash != commit_digest:
                            findings.append(self._finding(
                                "COMMITTING_PROVIDER_OBJECT_MISMATCH", sid, "CRITICAL",
                                provider_size=provider_object.size_bytes, provider_sha256=provider_hash,
                                commit_size=commit_size, commit_sha256=commit_digest))
                        else:
                            findings.append(self._finding(
                                "COMMITTING_PROVIDER_OBJECT_MATCHES_COMMITMENT", sid, "HIGH",
                                provider_size=provider_object.size_bytes, provider_sha256=provider_hash))
                    except Exception as exc:
                        findings.append(self._finding(
                            "COMMITTING_PROVIDER_OBJECT_UNCONFIRMED", sid, "HIGH",
                            error_type=type(exc).__name__))

        for entry in self.staging_root.iterdir():
            if entry.name.startswith("."):
                findings.append(self._finding("ROOT_TEMPORARY_ENTRY", "[root]", "REVIEW", entry=entry.name))
            elif entry.name not in known:
                findings.append(self._finding("ORPHAN_STAGING_ENTRY", entry.name, "HIGH"))
        return findings
