"""WP20: size/output bounds and concurrency slot."""
from __future__ import annotations

import hashlib
import tempfile
import threading
import time
import unittest
from pathlib import Path

from execution_host.work28_bounds import (
    BoundsError,
    MAX_SNAPSHOT_BYTES,
    assert_snapshot_size,
    truncate_output,
    execution_slot,
)
from execution_host.host import ExecutionHost
from execution_host.work28_contract import create_source_snapshot, validate_request
from execution_host.work28_grant import issue_grant_for_tests
from execution_host.work28_dispatch import dispatch_execute


class BoundsUnitTests(unittest.TestCase):
    def test_snapshot_too_large(self):
        with self.assertRaises(BoundsError):
            assert_snapshot_size(MAX_SNAPSHOT_BYTES + 1)
        assert_snapshot_size(100)

    def test_truncate(self):
        s = truncate_output("x" * 100, limit=10)
        self.assertTrue(s.startswith("xxxxxxxxxx"))
        self.assertIn("truncated", s)


class ConcurrencySlotTests(unittest.TestCase):
    def test_per_work_exclusive(self):
        order: list[str] = []
        released = threading.Event()

        def worker_a():
            with execution_slot("28"):
                order.append("a-in")
                released.wait(timeout=2)
                order.append("a-out")

        t1 = threading.Thread(target=worker_a)
        t1.start()
        time.sleep(0.05)

        def unlock():
            time.sleep(0.1)
            released.set()

        threading.Thread(target=unlock, daemon=True).start()
        with execution_slot("28"):
            order.append("b-in")
            order.append("b-out")
        t1.join(timeout=5)
        self.assertEqual(order[0], "a-in")
        self.assertIn("a-out", order)
        self.assertIn("b-in", order)


class SnapshotSizeInExecuteTests(unittest.TestCase):
    def test_large_snapshot_refused(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            work = base / "w"
            work.mkdir()
            body = b"print(1)\n"
            (work / "t.py").write_bytes(body)
            digest = hashlib.sha256(body).hexdigest()
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "t.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                    "timeout_seconds": 10,
                }
            )
            snap = create_source_snapshot(
                request=req,
                authoritative_work_id="28",
                work_root=work,
                snapshot_root=base / "snaps",
            )
            assert_snapshot_size(Path(snap.snapshot_path).stat().st_size)


class DispatchStillOkTests(unittest.TestCase):
    def test_small_dispatch(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            host_root = base / "root"
            host_root.mkdir()
            body = b'print("wp20")\n'
            (host_root / "job.py").write_bytes(body)
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            digest = hashlib.sha256(body).hexdigest()
            grant = issue_grant_for_tests(
                grant_id="g20",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            result = dispatch_execute(
                ExecutionHost(),
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": str(host_root),
                    "execution_workspace": str(ws),
                    "evidence_root": str(ev),
                    "authorized": True,
                    "execution_id": "wp20",
                },
                body={
                    "mode": "work28_snapshot",
                    "execution_grant_id": "g20",
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "job.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                        "timeout_seconds": 15,
                    },
                },
                grant_registry={"g20": grant},
            )
            self.assertIn("bounds", result)
            self.assertEqual(result.get("grant_id"), "g20")


if __name__ == "__main__":
    unittest.main()
