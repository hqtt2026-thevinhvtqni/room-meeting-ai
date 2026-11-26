"""Additive SQLite lifecycle migration and compare-and-set transition primitives.

Used by the isolated Cloud Drive UploadSessionManager prototype. Apply only to an isolated DB copy after backup; production migration remains gated.
"""
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone

STATES = {"CREATED", "UPLOADING", "VERIFYING", "COMMITTING", "COMPLETED", "ABORTED", "EXPIRED", "FAILED", "RECOVERY_REQUIRED"}
TRANSITIONS = {
    "CREATED": {"UPLOADING", "RECOVERY_REQUIRED", "ABORTED"},
    "UPLOADING": {"VERIFYING", "ABORTED", "EXPIRED"},
    "VERIFYING": {"COMMITTING", "FAILED", "RECOVERY_REQUIRED"},
    "COMMITTING": {"COMPLETED", "RECOVERY_REQUIRED"},
    "RECOVERY_REQUIRED": {"COMPLETED", "UPLOADING", "FAILED"},
}

class LifecycleError(Exception): pass
class InvalidTransition(LifecycleError): pass
class ConcurrentTransition(LifecycleError): pass

def migrate_upload_sessions(conn: sqlite3.Connection) -> list[str]:
    """Add columns without rewriting legacy states or assuming staging exists.

    Caller owns transaction/commit. Existing OPEN rows remain OPEN and are
    treated as a compatibility alias for UPLOADING during CAS transitions.
    """
    columns = {row[1] for row in conn.execute("PRAGMA table_info(upload_sessions)")}
    if not columns:
        raise LifecycleError("upload_sessions table does not exist")
    additions = {
        "state_version": "INTEGER NOT NULL DEFAULT 0",
        "lease_owner": "TEXT",
        "lease_expires_at": "INTEGER",
        "fencing_token": "INTEGER NOT NULL DEFAULT 0",
        "last_error_code": "TEXT",
        "provider_object_version": "TEXT",
        "updated_at": "INTEGER",
        "completed_at": "INTEGER",
        "commit_sha256": "TEXT",
        "commit_size": "INTEGER",
        "commit_manifest_version": "INTEGER",
    }
    added = []
    for name, declaration in additions.items():
        if name not in columns:
            conn.execute(f"ALTER TABLE upload_sessions ADD COLUMN {name} {declaration}")
            added.append(name)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_upload_sessions_status_expiry ON upload_sessions(status, expires_at)")
    return added

def transition_session(conn: sqlite3.Connection, *, session_id: str, expected_state: str,
                       new_state: str, expected_version: int | None = None,
                       error_code: str | None = None,
                       provider_object_version: str | None = None) -> int:
    """CAS update; caller MUST hold BEGIN IMMEDIATE and commit/rollback."""
    expected = "UPLOADING" if expected_state == "OPEN" else expected_state
    target = "UPLOADING" if new_state == "OPEN" else new_state
    if expected not in STATES or target not in STATES or target not in TRANSITIONS.get(expected, set()):
        raise InvalidTransition(f"transition {expected} -> {target} is not allowed")
    now = int(datetime.now(timezone.utc).timestamp())
    if expected == "UPLOADING":
        where = "session_id=? AND status IN (?, ?)"
        params: list[object] = [target, now, error_code, provider_object_version, session_id, "UPLOADING", "OPEN"]
    else:
        where = "session_id=? AND status=?"
        params = [target, now, error_code, provider_object_version, session_id, expected_state]
    if expected_version is not None:
        where += " AND state_version=?"
        params.append(expected_version)
    cursor = conn.execute(
        "UPDATE upload_sessions SET status=?, updated_at=?, last_error_code=?, "
        "provider_object_version=COALESCE(?, provider_object_version), "
        "state_version=state_version+1, fencing_token=fencing_token+1 " + "WHERE " + where,
        tuple(params),
    )
    if cursor.rowcount != 1:
        raise ConcurrentTransition("session state/version changed or session not found")
    return int(conn.execute("SELECT state_version FROM upload_sessions WHERE session_id=?", (session_id,)).fetchone()[0])

def claim_completion(conn: sqlite3.Connection, *, session_id: str, expected_version: int | None = None) -> int:
    return transition_session(conn, session_id=session_id, expected_state="UPLOADING",
                              new_state="VERIFYING", expected_version=expected_version)

def finalize_completion(conn: sqlite3.Connection, *, session_id: str, expected_version: int,
                        completed_sha256: str, completed_size: int,
                        provider_object_version: str | None = None) -> int:
    """Persist final metadata atomically with COMMITTING -> COMPLETED.

    Caller must verify provider bytes first and wrap this call in one transaction.
    """
    import re
    if not re.fullmatch(r"[a-f0-9]{64}", completed_sha256) or completed_size < 0:
        raise LifecycleError("invalid verified completion metadata")
    version = transition_session(conn, session_id=session_id, expected_state="COMMITTING",
                                  new_state="COMPLETED", expected_version=expected_version,
                                  provider_object_version=provider_object_version)
    conn.execute("UPDATE upload_sessions SET completed_sha256=?, completed_size=?, completed_at=updated_at WHERE session_id=?",
                 (completed_sha256, completed_size, session_id))
    return version