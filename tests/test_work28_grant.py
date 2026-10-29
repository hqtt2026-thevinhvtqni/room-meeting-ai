"""WP15: grant \u2194 request binding before snapshot/execute."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from execution_host.work28_grant import (
    GrantError,
    bind_grant_to_request,
    issue_grant_for_tests,
)
from execution_host.work28_contract import create_source_snapshot
from execution_host.work28_execute import run_verified_snapshot
from execution_host.host import ExecutionHost
from execution_host.models import WorkContext


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class GrantBindTests(unittest.TestCase):
    def test_bind_ok(self):
        digest = "a" * 64
        grant = issue_grant_for_tests(
            grant_id="g1",
            work_id="28",
            entry_path="run.py",
            operation="RUN_SCRIPT",
            expected_source_sha256=digest,
        )
        req = bind_grant_to_request(
            grant,
            {
                "work_id": "28",
                "entry_path": "run.py",
                "operation": "RUN_SCRIPT",
                "expected_source_sha256": digest,
            },
        )
        self.assertEqual(req.entry_path, "run.py")

    def test_hash_mismatch_refused(self):
        grant = issue_grant_for_tests(
            grant_id="g1",
            work_id="28",
            entry_path="run.py",
            operation="RUN_SCRIPT",
            expected_source_sha256="a" * 64,
        )
        with self.assertRaises(GrantError) as ctx:
            bind_grant_to_request(
                grant,
                {
                    "work_id": "28",
                    "entry_path": "run.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": "b" * 64,
                },
            )
        self.assertIn("grant_hash_mismatch", str(ctx.exception))

    def test_entry_widen_refused(self):
        digest = "c" * 64
        grant = issue_grant_for_tests(
            grant_id="g1",
            work_id="28",
            entry_path="safe.py",
            operation="RUN_SCRIPT",
            expected_source_sha256=digest,
        )
        with self.assertRaises(GrantError):
            bind_grant_to_request(
                grant,
                {
                    "work_id": "28",
                    "entry_path": "other.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                },
            )

    def test_expired_grant(self):
        grant = issue_grant_for_tests(
            grant_id="g1",
            work_id="28",
            entry_path="run.py",
            operation="RUN_SCRIPT",
            expected_source_sha256="d" * 64,
            ttl_seconds=-1,
        )
        with self.assertRaises(GrantError) as ctx:
            bind_grant_to_request(
                grant,
                {
                    "work_id": "28",
                    "entry_path": "run.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": "d" * 64,
                },
            )
        self.assertIn("grant_expired", str(ctx.exception))

    def test_pipeline_grant_snapshot_execute(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            work = base / "worktree"
            work.mkdir()
            body = b'print("granted")\n'
            (work / "job.py").write_bytes(body)
            digest = _sha(body)
            grant = issue_grant_for_tests(
                grant_id="g-pipeline",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            req = bind_grant_to_request(
                grant,
                {
                    "work_id": "28",
                    "entry_path": "job.py",
                    "operation": "RUN_SCRIPT",
                    "expected_source_sha256": digest,
                    "timeout_seconds": 15,
                },
            )
            snap = create_source_snapshot(
                request=req,
                authoritative_work_id="28",
                work_root=work,
                snapshot_root=base / "snaps",
            )
            host_root = base / "hostroot"
            host_root.mkdir()
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            ctx = WorkContext(
                work_id="28",
                work_name="WORK28",
                workspace_root=str(host_root),
                execution_workspace=str(ws),
                evidence_root=str(ev),
                authorized=True,
                execution_id="wp15",
            )
            result = run_verified_snapshot(ExecutionHost(), ctx, req, snap)
            self.assertEqual(result.get("source_sha256"), digest)
            if result.get("status") == "PASS":
                out = result.get("stdout_summary") or ""
                self.assertIn("granted", out)


if __name__ == "__main__":
    unittest.main()
