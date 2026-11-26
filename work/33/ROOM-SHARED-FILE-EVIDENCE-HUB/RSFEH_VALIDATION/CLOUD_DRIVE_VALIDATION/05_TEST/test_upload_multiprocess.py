import hashlib
import multiprocessing as mp
import sqlite3
from pathlib import Path

from cloud_drive.service.audit import AuditWriter
from cloud_drive.service.quota_manager import QuotaManager
from cloud_drive.storage.local import LocalStorageAdapter
from cloud_drive.uploads.session_manager import UploadSessionManager


def _build_manager(root):
    root = Path(root)
    db = root / "shared.sqlite3"
    audit = AuditWriter(str(db))
    storage = LocalStorageAdapter(root / "objects")
    manager = UploadSessionManager(
        database=db, staging_root=root / "staging", storage=storage,
        audit_writer=audit,
    )
    return db, audit, manager


def _put_part_process(root, session_id, part_number, payload, barrier, queue):
    try:
        _, _, manager = _build_manager(root)
        barrier.wait(15)
        result = manager.put_part(
            session_id=session_id, scope_id="scope-mp",
            part_number=part_number, source=__import__("io").BytesIO(payload),
            actor_id=f"test-process:{part_number}",
        )
        queue.put(("OK", part_number, result["sha256"]))
    except Exception as exc:
        queue.put(("ERROR", part_number, type(exc).__name__ + ":" + str(exc)))


def _quota_reserve_process(db_path, barrier, queue, amount):
    try:
        quota = QuotaManager(str(db_path), default_limit_bytes=1000)
        barrier.wait(15)
        reservation_id = quota.reserve("scope-quota-mp", amount)
        queue.put(("OK", reservation_id))
    except Exception as exc:
        queue.put(("ERROR", type(exc).__name__ + ":" + str(exc)))


def _join_processes(processes, timeout=30):
    for process in processes:
        process.join(timeout)
    alive = [p.pid for p in processes if p.is_alive()]
    if alive:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(5)
        raise AssertionError(f"worker processes did not exit: {alive}")
    bad = [(p.pid, p.exitcode) for p in processes if p.exitcode != 0]
    assert not bad, f"worker process exit failures: {bad}"


def test_independent_processes_write_distinct_parts_and_audit_chain(tmp_path):
    db, audit, manager = _build_manager(tmp_path)
    payloads = [bytes([65 + i]) for i in range(8)]
    session = manager.begin_upload(
        scope_id="scope-mp", expected_size=len(payloads), actor_id="test-parent"
    )

    ctx = mp.get_context("spawn")
    barrier = ctx.Barrier(len(payloads))
    queue = ctx.Queue()
    processes = [
        ctx.Process(
            target=_put_part_process,
            args=(str(tmp_path), session.session_id, i + 1, payloads[i], barrier, queue),
        )
        for i in range(len(payloads))
    ]
    for process in processes:
        process.start()
    _join_processes(processes)

    outcomes = [queue.get(timeout=5) for _ in processes]
    assert all(item[0] == "OK" for item in outcomes), outcomes
    with sqlite3.connect(db) as conn:
        parts = conn.execute(
            "SELECT part_number, size_bytes, sha256 FROM upload_parts "
            "WHERE session_id=? ORDER BY part_number", (session.session_id,)
        ).fetchall()
        audit_rows = conn.execute(
            "SELECT sequence, action FROM audit_events ORDER BY sequence"
        ).fetchall()
    assert [row[0] for row in parts] == list(range(1, 9))
    assert all(row[1] == 1 for row in parts)
    assert [row[0] for row in audit_rows] == list(range(1, 10))
    assert sum(row[1] == "UPLOAD_PART_ACCEPTED" for row in audit_rows) == 8
    assert audit.verify_chain()


def test_independent_process_quota_reservations_never_overbook(tmp_path):
    db = tmp_path / "quota-multiprocess.sqlite3"
    quota = QuotaManager(str(db), default_limit_bytes=100)
    quota.configure_scope("scope-quota-mp", limit_bytes=100)

    ctx = mp.get_context("spawn")
    worker_count = 12
    barrier = ctx.Barrier(worker_count)
    queue = ctx.Queue()
    processes = [
        ctx.Process(target=_quota_reserve_process, args=(str(db), barrier, queue, 10))
        for _ in range(worker_count)
    ]
    for process in processes:
        process.start()
    _join_processes(processes)

    outcomes = [queue.get(timeout=5) for _ in processes]
    successes = [item for item in outcomes if item[0] == "OK"]
    failures = [item for item in outcomes if item[0] == "ERROR"]
    snapshot = quota.snapshot("scope-quota-mp")
    assert len(successes) == 10, (len(successes), failures)
    assert len(failures) == 2, failures
    assert snapshot.reserved_bytes == 100
    assert snapshot.used_bytes == 0
    with sqlite3.connect(db) as conn:
        held = conn.execute(
            "SELECT COUNT(*) FROM quota_reservations WHERE state='HELD'"
        ).fetchone()[0]
        assert held == 10
