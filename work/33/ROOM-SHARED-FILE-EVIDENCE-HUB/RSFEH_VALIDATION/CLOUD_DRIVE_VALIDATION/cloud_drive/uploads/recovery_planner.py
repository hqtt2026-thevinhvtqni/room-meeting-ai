"""Read-only recovery planner for upload lifecycle and quota reservations.

The planner emits operator-reviewable recommendations only. It never mutates
SQLite rows, staging files, or provider objects.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class RecoveryPlanner:
    def __init__(self, database: str | Path):
        self.database = Path(database)

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA query_only=ON")
        return db

    @staticmethod
    def _item(session_id: str, status: str, action: str, reason: str,
              approval: str = "REQUIRED", **details: Any) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "session_status": status,
            "recommended_action": action,
            "reason": reason,
            "mutation_performed": False,
            "approval_required": approval,
            **details,
        }

    def plan(self) -> list[dict[str, Any]]:
        """Return deterministic recommendations from a read-only DB snapshot."""
        db = self._connect()
        try:
            tables = {r["name"] for r in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
            if "upload_sessions" not in tables:
                raise RuntimeError("upload_sessions table is missing")
            session_columns = {r["name"] for r in db.execute(
                "PRAGMA table_info(upload_sessions)"
            )}
            required = {"session_id", "status", "expected_size"}
            if not required.issubset(session_columns):
                raise RuntimeError("upload_sessions schema is incomplete")

            quota_available = (
                "quota_reservations" in tables
                and "quota_accounts" in tables
                and "quota_reservation_id" in session_columns
            )
            extra = ", s.quota_reservation_id" if "quota_reservation_id" in session_columns else ""
            rows = db.execute(
                "SELECT s.session_id, s.status, s.expected_size, "
                "s.completed_size, s.completed_sha256" + extra +
                " FROM upload_sessions AS s ORDER BY s.session_id"
            ).fetchall()

            reservations = {}
            if quota_available:
                for r in db.execute(
                    "SELECT reservation_id, scope_id, bytes, state, actual_bytes "
                    "FROM quota_reservations"
                ):
                    reservations[r["reservation_id"]] = dict(r)
        finally:
            db.close()

        result: list[dict[str, Any]] = []
        for row in rows:
            sid, status = row["session_id"], row["status"]
            reservation_id = row["quota_reservation_id"] if "quota_reservation_id" in row.keys() else None
            reservation = reservations.get(reservation_id) if reservation_id else None

            if reservation_id and reservation is None:
                result.append(self._item(
                    sid, status, "INVESTIGATE_MISSING_QUOTA_RESERVATION",
                    "Session references a quota reservation that is absent or unavailable in the quota ledger.",
                ))
                continue

            if status == "COMMITTING":
                if reservation and reservation["state"] == "HELD":
                    action = "VERIFY_PROVIDER_AND_REVIEW_FINALIZATION"
                    reason = ("Provider object and staged bytes must be independently verified; "
                              "only then may an authorized operator decide whether to finalize.")
                else:
                    action = "INVESTIGATE_COMMITTING_STATE"
                    reason = "COMMITTING is non-terminal; reservation is missing or not HELD."
                result.append(self._item(
                    sid, status, action, reason,
                    reservation_state=reservation["state"] if reservation else None,
                ))
            elif status == "RECOVERY_REQUIRED":
                result.append(self._item(
                    sid, status, "INSPECT_EVIDENCE_AND_RETAIN_RESERVATION",
                    "Preserve staging/provider evidence. Do not promote, delete, reopen, or release quota automatically.",
                    reservation_state=reservation["state"] if reservation else None,
                ))
            elif status == "COMPLETED":
                if reservation and reservation["state"] == "HELD":
                    result.append(self._item(
                        sid, status, "VERIFY_COMPLETED_OBJECT_THEN_REVIEW_QUOTA_COMMIT",
                        "Completion metadata exists but quota remains HELD; independently verify stored bytes before an approved quota settlement.",
                        reservation_state="HELD",
                        expected_size=row["expected_size"],
                        completed_size=row["completed_size"],
                    ))
                elif reservation and reservation["state"] == "COMMITTED":
                    if reservation["actual_bytes"] != row["completed_size"]:
                        result.append(self._item(
                            sid, status, "RECONCILE_QUOTA_ACCOUNTING",
                            "Committed reservation bytes differ from completed upload size; require an audited adjustment decision.",
                            reservation_state="COMMITTED",
                            reserved_actual_bytes=reservation["actual_bytes"],
                            completed_size=row["completed_size"],
                        ))
            elif status == "ABORTED" and reservation and reservation["state"] == "HELD":
                result.append(self._item(
                    sid, status, "VERIFY_NO_ACTIVE_WRITER_THEN_REVIEW_QUOTA_RELEASE",
                    "Confirm no writer remains and no provider object was committed before approving release of held quota.",
                    reservation_state="HELD",
                ))
            elif status in {"UPLOADING", "OPEN"} and reservation and reservation["state"] == "HELD":
                # Expiry alone is insufficient proof that a writer has stopped.
                result.append(self._item(
                    sid, status, "CHECK_EXPIRY_AND_WRITER_OWNERSHIP",
                    "Do not release quota until expiry is confirmed and active writer ownership is disproved.",
                    reservation_state="HELD",
                ))
            elif status in {"CREATED", "VERIFYING"}:
                result.append(self._item(
                    sid, status, "INSPECT_STAGING_AND_LIFECYCLE",
                    "Non-terminal state requires evidence review; no automatic state transition is proposed.",
                    reservation_state=reservation["state"] if reservation else None,
                ))

        return result
