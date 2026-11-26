import hashlib
import io
import sqlite3

import pytest

from cloud_drive.service.audit import AuditWriter, AuditWriteError
from cloud_drive.storage.protocol import ObjectRef, StoredObject
from cloud_drive.uploads.session_manager import UploadSessionManager


class MemoryStorage:
    def __init__(self):
        self.objects = {}

    def put_stream(self, key, source, *, max_bytes):
        payload = source.read()
        assert len(payload) <= max_bytes
        self.objects[key] = payload
        return StoredObject(ObjectRef(key), len(payload), hashlib.sha256(payload).hexdigest())

    def head(self, ref):
        payload = self.objects[ref.key]
        return StoredObject(ref, len(payload), hashlib.sha256(payload).hexdigest())


def _manager(tmp_path):
    db = tmp_path / "shared.sqlite3"
    audit = AuditWriter(str(db))
    storage = MemoryStorage()
    manager = UploadSessionManager(
        database=db,
        staging_root=tmp_path / "staging",
        storage=storage,
        audit_writer=audit,
    )
    return db, audit, storage, manager


def _start(manager, payload=b"transactional audit"):
    session = manager.begin_upload(
        scope_id="scope-a", expected_size=len(payload), actor_id="human:vinh"
    )
    manager.put_part(
        session_id=session.session_id, scope_id="scope-a", part_number=1,
        source=io.BytesIO(payload), actor_id="human:vinh",
    )
    return session, payload


def test_upload_lifecycle_events_share_metadata_database_and_hash_chain(tmp_path):
    db, audit, storage, manager = _manager(tmp_path)
    session, payload = _start(manager)
    manager.complete_upload(
        session_id=session.session_id, scope_id="scope-a", actor_id="human:vinh"
    )

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            "SELECT action, actor_id FROM audit_events ORDER BY sequence"
        ).fetchall()
        state = conn.execute(
            "SELECT status FROM upload_sessions WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
    assert rows == [
        ("UPLOAD_SESSION_CREATED", "human:vinh"),
        ("UPLOAD_PART_ACCEPTED", "human:vinh"),
        ("UPLOAD_COMMIT_INTENT", "human:vinh"),
        ("UPLOAD_COMPLETED", "human:vinh"),
    ]
    assert state == "COMPLETED"
    assert audit.verify_chain()


def test_commit_intent_audit_failure_rolls_back_digest_and_state(tmp_path):
    db, audit, storage, manager = _manager(tmp_path)
    session, payload = _start(manager)
    with sqlite3.connect(db) as conn:
        conn.execute("""
            CREATE TRIGGER fail_commit_intent
            BEFORE INSERT ON audit_events
            WHEN NEW.action='UPLOAD_COMMIT_INTENT'
            BEGIN SELECT RAISE(ABORT, 'injected audit failure'); END
        """)

    with pytest.raises(AuditWriteError):
        manager.complete_upload(
            session_id=session.session_id, scope_id="scope-a", actor_id="human:vinh"
        )

    with sqlite3.connect(db) as conn:
        state, commit_sha, commit_size = conn.execute(
            "SELECT status, commit_sha256, commit_size FROM upload_sessions WHERE session_id=?",
            (session.session_id,),
        ).fetchone()
    assert state == "VERIFYING"
    assert commit_sha is None and commit_size is None
    assert not storage.objects


def test_missing_verified_actor_fails_before_session_creation(tmp_path):
    db, audit, storage, manager = _manager(tmp_path)
    with pytest.raises(AuditWriteError):
        manager.begin_upload(scope_id="scope-a", expected_size=1, actor_id=None)
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM upload_sessions").fetchone()[0] == 0
