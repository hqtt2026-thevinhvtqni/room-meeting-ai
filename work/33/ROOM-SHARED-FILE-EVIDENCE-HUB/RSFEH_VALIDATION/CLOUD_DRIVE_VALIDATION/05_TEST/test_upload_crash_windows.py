import hashlib
import io
import sqlite3

import pytest

from cloud_drive.service.audit import AuditWriter, AuditWriteError
from cloud_drive.storage.protocol import ObjectRef, StoredObject
from cloud_drive.uploads.recovery_inspector import RecoveryInspector
from cloud_drive.uploads.session_manager import UploadSessionManager


class FailOnActionAudit(AuditWriter):
    def __init__(self, database, action_to_fail):
        self.action_to_fail = action_to_fail
        super().__init__(str(database))

    def append_in_transaction(self, conn, **kwargs):
        if kwargs.get("action") == self.action_to_fail:
            raise AuditWriteError("injected crash-window audit failure")
        return super().append_in_transaction(conn, **kwargs)


class PersistentMemoryStorage:
    def __init__(self):
        self.objects = {}

    def put_stream(self, key, source, *, max_bytes):
        payload = source.read()
        if len(payload) > max_bytes:
            raise ValueError("object exceeds limit")
        self.objects[key] = payload
        return StoredObject(ObjectRef(key), len(payload), hashlib.sha256(payload).hexdigest())

    def head(self, ref):
        payload = self.objects[ref.key]
        return StoredObject(ref, len(payload), hashlib.sha256(payload).hexdigest())


def test_part_file_left_after_rename_before_metadata_commit_is_detected_read_only(tmp_path):
    database = tmp_path / "upload.sqlite3"
    staging = tmp_path / "staging"
    audit = FailOnActionAudit(database, "UPLOAD_PART_ACCEPTED")
    storage = PersistentMemoryStorage()
    manager = UploadSessionManager(
        database=database, staging_root=staging, storage=storage, audit_writer=audit
    )
    session = manager.begin_upload(
        scope_id="scope-crash", expected_size=9, actor_id="test-actor"
    )

    with pytest.raises(AuditWriteError):
        manager.put_part(
            session_id=session.session_id, scope_id="scope-crash", part_number=1,
            source=io.BytesIO(b"orphan-payload"), actor_id="test-actor",
        )

    part_file = staging / session.session_id / "part-00001.bin"
    assert part_file.is_file()
    with sqlite3.connect(database) as conn:
        state = conn.execute(
            "SELECT status FROM upload_sessions WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
        part_count = conn.execute(
            "SELECT COUNT(*) FROM upload_parts WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
    assert state == "UPLOADING"
    assert part_count == 0

    before_db = database.read_bytes()
    before_part = part_file.read_bytes()
    findings = RecoveryInspector(str(database), str(staging)).inspect(now=1)
    after_db = database.read_bytes()

    assert before_db == after_db
    assert part_file.read_bytes() == before_part
    assert any(
        item["kind"] == "ORPHAN_PART_FILE"
        and item["session_id"] == session.session_id
        and item["part_number"] == 1
        for item in findings
    )


def test_provider_put_success_then_finalize_audit_failure_is_reconciled_by_commitment(tmp_path):
    database = tmp_path / "upload.sqlite3"
    staging = tmp_path / "staging"
    audit = FailOnActionAudit(database, "UPLOAD_COMPLETED")
    storage = PersistentMemoryStorage()
    manager = UploadSessionManager(
        database=database, staging_root=staging, storage=storage, audit_writer=audit
    )
    payload = b"provider-write-before-finalize"
    expected = hashlib.sha256(payload).hexdigest()
    session = manager.begin_upload(
        scope_id="scope-crash", expected_size=len(payload), actor_id="test-actor"
    )
    manager.put_part(
        session_id=session.session_id, scope_id="scope-crash", part_number=1,
        source=io.BytesIO(payload), actor_id="test-actor",
    )

    with pytest.raises(AuditWriteError):
        manager.complete_upload(
            session_id=session.session_id, scope_id="scope-crash", actor_id="test-actor"
        )

    with sqlite3.connect(database) as conn:
        row = conn.execute(
            "SELECT status, commit_sha256, commit_size, completed_sha256 "
            "FROM upload_sessions WHERE session_id=?", (session.session_id,)
        ).fetchone()
        actions = [
            item[0] for item in conn.execute(
                "SELECT action FROM audit_events ORDER BY sequence"
            ).fetchall()
        ]
    assert row == ("COMMITTING", expected, len(payload), None)
    assert "UPLOAD_COMMIT_INTENT" in actions
    assert "UPLOAD_COMPLETED" not in actions
    assert storage.objects

    before_db = database.read_bytes()
    findings = RecoveryInspector(str(database), str(staging), storage).inspect(now=1)
    after_db = database.read_bytes()
    assert before_db == after_db
    assert any(
        item["kind"] == "COMMITTING_PROVIDER_OBJECT_MATCHES_COMMITMENT"
        and item["session_id"] == session.session_id
        for item in findings
    )
