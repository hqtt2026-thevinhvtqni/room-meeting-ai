import hashlib
import io
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from cloud_drive.service.audit import AuditWriter
from cloud_drive.storage.protocol import ObjectRef, StoredObject
from cloud_drive.uploads.session_manager import (
    UploadSessionManager, UploadConflict, UploadNotFound
)


class MemoryStorage:
    def __init__(self):
        self.objects = {}
        self.lock = threading.Lock()

    def put_stream(self, key, source, *, max_bytes):
        data = source.read()
        with self.lock:
            self.objects[key] = data
        return StoredObject(ObjectRef(key), len(data), hashlib.sha256(data).hexdigest())

    def head(self, ref):
        with self.lock:
            data = self.objects[ref.key]
        return StoredObject(ref, len(data), hashlib.sha256(data).hexdigest())


class BlockingReader(io.BytesIO):
    def __init__(self, payload, entered, release):
        super().__init__(payload)
        self.entered = entered
        self.release = release
        self.once = False

    def read(self, size=-1):
        if not self.once:
            self.once = True
            self.entered.set()
            assert self.release.wait(5), "test synchronization timed out"
        return super().read(size)


def make_manager(tmp_path, *, quota=None):
    db = tmp_path / "concurrency.sqlite3"
    audit = AuditWriter(str(db))
    storage = MemoryStorage()
    manager = UploadSessionManager(
        database=db, staging_root=tmp_path / "staging", storage=storage,
        audit_writer=audit, quota_manager=quota,
    )
    return db, audit, storage, manager


def start(manager, payload=b"payload"):
    return manager.begin_upload(
        scope_id="scope-a", expected_size=len(payload), actor_id="human:vinh"
    )


def put(manager, session, payload, part=1):
    return manager.put_part(
        session_id=session.session_id, scope_id="scope-a", part_number=part,
        source=io.BytesIO(payload), actor_id="human:vinh",
    )


def test_concurrent_same_part_identical_payload_is_idempotent(tmp_path):
    db, audit, storage, manager = make_manager(tmp_path)
    session = start(manager, b"same-payload")
    barrier = threading.Barrier(2)

    def writer():
        barrier.wait()
        return put(manager, session, b"same-payload")

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: writer(), range(2)))
    assert results[0] == results[1]
    assert manager.list_parts(session_id=session.session_id, scope_id="scope-a")[0]["size_bytes"] == 12
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM upload_parts").fetchone()[0] == 1
        assert conn.execute(
            "SELECT COUNT(*) FROM audit_events WHERE action='UPLOAD_PART_ACCEPTED'"
        ).fetchone()[0] == 1
    assert audit.verify_chain()


def test_concurrent_same_part_different_payload_fails_closed(tmp_path):
    db, audit, storage, manager = make_manager(tmp_path)
    session = start(manager, b"alpha")
    barrier = threading.Barrier(2)

    def writer(payload):
        barrier.wait()
        try:
            return ("OK", put(manager, session, payload))
        except UploadConflict:
            return ("CONFLICT", None)

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(writer, [b"alpha", b"bravo"]))
    assert sorted(x[0] for x in outcomes) == ["CONFLICT", "OK"]
    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT size_bytes, sha256 FROM upload_parts WHERE session_id=? AND part_number=1",
            (session.session_id,),
        ).fetchone()
        events = conn.execute(
            "SELECT COUNT(*) FROM audit_events WHERE action='UPLOAD_PART_ACCEPTED'"
        ).fetchone()[0]
    assert row[1] in {hashlib.sha256(b"alpha").hexdigest(), hashlib.sha256(b"bravo").hexdigest()}
    assert events == 1
    assert audit.verify_chain()


def test_completion_claim_prevents_inflight_part_writer_from_committing(tmp_path):
    db, audit, storage, manager = make_manager(tmp_path)
    session = start(manager, b"late")
    entered, release = threading.Event(), threading.Event()
    result = {}

    def delayed_writer():
        try:
            manager.put_part(
                session_id=session.session_id, scope_id="scope-a", part_number=1,
                source=BlockingReader(b"late", entered, release), actor_id="human:vinh",
            )
            result["writer"] = "ACCEPTED"
        except UploadConflict:
            result["writer"] = "REJECTED"

    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(delayed_writer)
        assert entered.wait(5)
        # No part is yet committed. Completion must claim VERIFYING and fail
        # closed rather than accepting a part after the snapshot.
        with pytest.raises(UploadConflict):
            manager.complete_upload(
                session_id=session.session_id, scope_id="scope-a", actor_id="human:vinh"
            )
        release.set()
        future.result(timeout=5)

    with sqlite3.connect(db) as conn:
        state = conn.execute(
            "SELECT status FROM upload_sessions WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
        part_count = conn.execute(
            "SELECT COUNT(*) FROM upload_parts WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
    assert result["writer"] == "REJECTED"
    assert state == "RECOVERY_REQUIRED"
    assert part_count == 0
    # Failed completion is left in VERIFYING for explicit recovery, not reopened.


def test_two_concurrent_completion_claims_allow_only_one_provider_write(tmp_path):
    db, audit, storage, manager = make_manager(tmp_path)
    session = start(manager, b"once")
    put(manager, session, b"once")
    barrier = threading.Barrier(2)

    def complete():
        barrier.wait()
        try:
            manager.complete_upload(
                session_id=session.session_id, scope_id="scope-a", actor_id="human:vinh"
            )
            return "COMPLETED"
        except UploadConflict:
            return "CONFLICT"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(lambda _: complete(), range(2)))
    assert sorted(outcomes) == ["COMPLETED", "CONFLICT"]
    assert len(storage.objects) == 1
    with sqlite3.connect(db) as conn:
        state = conn.execute(
            "SELECT status FROM upload_sessions WHERE session_id=?", (session.session_id,)
        ).fetchone()[0]
        completed_events = conn.execute(
            "SELECT COUNT(*) FROM audit_events WHERE action='UPLOAD_COMPLETED'"
        ).fetchone()[0]
    assert state == "COMPLETED"
    assert completed_events == 1
    assert audit.verify_chain()
