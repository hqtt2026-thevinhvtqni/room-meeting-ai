import hashlib
import io
import sqlite3

from cloud_drive.storage.protocol import ObjectRef, StoredObject
from cloud_drive.uploads.session_manager import UploadSessionManager


class InspectingStorage:
    def __init__(self, database):
        self.database = database
        self.payloads = {}
        self.commitment_seen = None

    def put_stream(self, key, source, *, max_bytes):
        payload = source.read()
        assert len(payload) <= max_bytes
        with sqlite3.connect(self.database) as db:
            row = db.execute(
                "SELECT status, commit_sha256, commit_size, commit_manifest_version "
                "FROM upload_sessions WHERE object_key=?", (key,)
            ).fetchone()
        self.commitment_seen = row
        self.payloads[key] = payload
        return StoredObject(ObjectRef(key), len(payload), hashlib.sha256(payload).hexdigest())

    def head(self, ref):
        payload = self.payloads[ref.key]
        return StoredObject(ref, len(payload), hashlib.sha256(payload).hexdigest())

    def open_read(self, ref):
        return io.BytesIO(self.payloads[ref.key])

    def delete(self, ref):
        self.payloads.pop(ref.key, None)

    def capabilities(self):
        return None


def test_commit_digest_is_durable_before_provider_put(tmp_path):
    database = tmp_path / "uploads.sqlite3"
    storage = InspectingStorage(database)
    manager = UploadSessionManager(
        database=database,
        staging_root=tmp_path / "staging",
        storage=storage,
    )
    payload = b"commit digest must precede provider write"
    session = manager.begin_upload(
        scope_id="scope-a",
        expected_size=len(payload),
        expected_sha256=None,
    )
    manager.put_part(
        session_id=session.session_id,
        scope_id="scope-a",
        part_number=1,
        source=io.BytesIO(payload),
    )

    stored = manager.complete_upload(
        session_id=session.session_id,
        scope_id="scope-a",
    )

    assert storage.commitment_seen == (
        "COMMITTING",
        hashlib.sha256(payload).hexdigest(),
        len(payload),
        1,
    )
    assert stored.sha256 == hashlib.sha256(payload).hexdigest()
    with sqlite3.connect(database) as db:
        final = db.execute(
            "SELECT status, commit_sha256, commit_size, completed_sha256 "
            "FROM upload_sessions WHERE session_id=?",
            (session.session_id,),
        ).fetchone()
    assert final == (
        "COMPLETED",
        hashlib.sha256(payload).hexdigest(),
        len(payload),
        hashlib.sha256(payload).hexdigest(),
    )
