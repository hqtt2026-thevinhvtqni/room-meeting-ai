"""WP14: Work 28 contract validation + immutable source snapshot (offline)."""
from __future__ import annotations

import hashlib
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

from execution_host.work28_contract import (
    Work28ContractError,
    create_source_snapshot,
    validate_request,
)
from execution_host.work28_execute import run_verified_snapshot
from execution_host.host import ExecutionHost
from execution_host.models import WorkContext


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ValidateRequestTests(unittest.TestCase):
    def test_happy_path(self):
        digest = "a" * 64
        req = validate_request(
            {
                "work_id": "28",
                "entry_path": "scripts/run.py",
                "operation": "RUN_SCRIPT",
                "expected_source_sha256": digest,
                "timeout_seconds": 10,
            }
        )
        self.assertEqual(req.entry_path, "scripts/run.py")
        self.assertEqual(req.timeout_seconds, 10)

    def test_rejects_escape_and_absolute(self):
        digest = "b" * 64
        for bad in ("../x.py", "/etc/passwd", "a/../../b.py", "C:/windows"):
            with self.assertRaises(Work28ContractError):
                validate_request(
                    {
                        "work_id": "28",
                        "entry_path": bad,
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                    }
                )

    def test_rejects_extra_and_missing(self):
        with self.assertRaises(Work28ContractError):
            validate_request({"work_id": "28"})
        with self.assertRaises(Work28ContractError):
            validate_request(
                {
                    "work_id": "28",
                    "entry_path": "a.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": "c" * 64,
                    "evil": 1,
                }
            )

    def test_rejects_run_command_style(self):
        with self.assertRaises(Work28ContractError):
            validate_request(
                {
                    "work_id": "28",
                    "entry_path": "a.py",
                    "operation": "RUN_COMMAND",
                    "expected_source_sha256": "d" * 64,
                }
            )


class SnapshotTests(unittest.TestCase):
    def test_create_and_hash_match(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "work"
            root.mkdir()
            src = root / "hello.py"
            body = b'print("wp14")\n'
            src.write_bytes(body)
            digest = _sha(body)
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "hello.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                }
            )
            snap = create_source_snapshot(
                request=req,
                authoritative_work_id="28",
                work_root=root,
                snapshot_root=Path(td) / "snaps",
            )
            self.assertEqual(snap.source_sha256, digest)
            self.assertTrue(snap.snapshot_path.is_file())
            mode = snap.snapshot_path.stat().st_mode
            self.assertFalse(mode & stat.S_IWUSR)

    def test_hash_mismatch_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "work"
            root.mkdir()
            (root / "x.py").write_bytes(b"print(1)\n")
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "x.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": "e" * 64,
                }
            )
            with self.assertRaises(Work28ContractError) as ctx:
                create_source_snapshot(
                    request=req,
                    authoritative_work_id="28",
                    work_root=root,
                    snapshot_root=Path(td) / "snaps",
                )
            self.assertIn("source_hash_mismatch", str(ctx.exception))

    def test_symlink_component_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "work"
            root.mkdir()
            real = root / "real.py"
            real.write_bytes(b"print(1)\n")
            link = root / "link.py"
            try:
                link.symlink_to(real)
            except OSError:
                self.skipTest("symlink not supported")
            digest = _sha(b"print(1)\n")
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "link.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                }
            )
            with self.assertRaises(Work28ContractError) as ctx:
                create_source_snapshot(
                    request=req,
                    authoritative_work_id="28",
                    work_root=root,
                    snapshot_root=Path(td) / "snaps",
                )
            self.assertIn("symlink", str(ctx.exception))

    def test_work_binding_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "work"
            root.mkdir()
            (root / "a.py").write_bytes(b"x\n")
            digest = _sha(b"x\n")
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "a.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                }
            )
            with self.assertRaises(PermissionError):
                create_source_snapshot(
                    request=req,
                    authoritative_work_id="99",
                    work_root=root,
                    snapshot_root=Path(td) / "snaps",
                )


class RunVerifiedSnapshotTests(unittest.TestCase):
    def test_run_uses_snapshot_not_work_root(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "worktree"
            root.mkdir()
            host_root = base / "hostroot"
            host_root.mkdir()
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            body = b'print("from-snapshot")\n'
            (root / "job.py").write_bytes(body)
            digest = _sha(body)
            req = validate_request(
                {
                    "work_id": "28",
                    "entry_path": "job.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                    "timeout_seconds": 15,
                }
            )
            snap = create_source_snapshot(
                request=req,
                authoritative_work_id="28",
                work_root=root,
                snapshot_root=Path(td) / "snaps",
            )
            (root / "job.py").write_bytes(b'print("mutated")\n')

            ctx = WorkContext(
                work_id="28",
                work_name="WORK28",
                workspace_root=str(host_root),
                execution_workspace=str(ws),
                evidence_root=str(ev),
                authorized=True,
                execution_id="wp14-test",
            )
            host = ExecutionHost()
            result = run_verified_snapshot(host, ctx, req, snap)
            self.assertIn(result.get("status"), ("PASS", "TIMEOUT", "FAIL"))
            if result.get("status") == "PASS":
                summary = result.get("stdout_summary") or result.get("stdout") or ""
                self.assertIn("from-snapshot", summary)
            self.assertEqual(result.get("source_sha256"), digest)
            self.assertEqual(result.get("wp14_path"), "verified_snapshot_only")
            cleanup = result.get("cleanup") or {}
            self.assertTrue(cleanup.get("process_reaped") or result.get("status") != "PASS")


if __name__ == "__main__":
    unittest.main()
