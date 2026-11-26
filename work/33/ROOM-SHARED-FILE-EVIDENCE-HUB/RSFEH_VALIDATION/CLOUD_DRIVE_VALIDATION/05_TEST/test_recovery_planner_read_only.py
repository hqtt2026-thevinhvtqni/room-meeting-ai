import sqlite3

from cloud_drive.uploads.recovery_planner import RecoveryPlanner


def _db(path, *, status, reservation_state="HELD"):
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE upload_sessions(
                session_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                expected_size INTEGER NOT NULL,
                completed_size INTEGER,
                completed_sha256 TEXT,
                quota_reservation_id TEXT
            );
            CREATE TABLE quota_accounts(
                scope_id TEXT PRIMARY KEY,
                limit_bytes INTEGER NOT NULL,
                used_bytes INTEGER NOT NULL
            );
            CREATE TABLE quota_reservations(
                reservation_id TEXT PRIMARY KEY,
                scope_id TEXT NOT NULL,
                bytes INTEGER NOT NULL,
                state TEXT NOT NULL,
                actual_bytes INTEGER
            );
        """)
        conn.execute(
            "INSERT INTO upload_sessions VALUES(?,?,?,?,?,?)",
            ("session-1", status, 64, None, None, "reservation-1"),
        )
        conn.execute(
            "INSERT INTO quota_accounts VALUES(?,?,?)",
            ("scope-1", 1024, 0),
        )
        conn.execute(
            "INSERT INTO quota_reservations VALUES(?,?,?,?,?)",
            ("reservation-1", "scope-1", 64, reservation_state, None),
        )


def test_committing_held_plan_is_review_only_and_never_finalizes(tmp_path):
    db = tmp_path / "recovery.sqlite3"
    _db(db, status="COMMITTING")
    before = db.read_bytes()

    plan = RecoveryPlanner(db).plan()

    assert db.read_bytes() == before
    assert len(plan) == 1
    item = plan[0]
    assert item["recommended_action"] == "VERIFY_PROVIDER_AND_REVIEW_FINALIZATION"
    assert item["mutation_performed"] is False
    assert item["approval_required"] == "REQUIRED"
    assert "independently verified" in item["reason"].lower()


def test_recovery_required_retains_held_quota_without_automatic_release(tmp_path):
    db = tmp_path / "recovery.sqlite3"
    _db(db, status="RECOVERY_REQUIRED")
    before = db.read_bytes()

    plan = RecoveryPlanner(db).plan()

    assert db.read_bytes() == before
    assert len(plan) == 1
    item = plan[0]
    assert item["recommended_action"] == "INSPECT_EVIDENCE_AND_RETAIN_RESERVATION"
    assert item["reservation_state"] == "HELD"
    assert item["mutation_performed"] is False
    assert item["approval_required"] == "REQUIRED"
    assert "do not promote, delete, reopen, or release" in item["reason"].lower()
