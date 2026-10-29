"""WP2 completion tests: fail-closed Job Object gate on execution paths.

On Windows, if the Job Object cannot be created/attached the execution
path must BLOCK, not merely label NOT_ATTACHED and run anyway. The gate
is simulated with a synthetic ManagedProcess so the blocked path is
exercised on every CI platform. A real (unpatched) run also proves the
non-blocked path stays PASS. ISOLATION_STATUS remains NOT_VERIFIED.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_host.host import ExecutionHost
from execution_host.models import WorkContext
from execution_host.process_job import ManagedProcess, job_object_gate


def _finished_process():
    proc = subprocess.Popen(
        [sys.executable, "-c", "pass"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    proc.communicate(timeout=10)
    return proc


class JobObjectGateUnitTests(unittest.TestCase):
    def _managed(self, platform, job_object):
        return ManagedProcess(
            process=_finished_process(), platform=platform,
            session_leader=False, created_via_spawn=True,
            job_object=job_object, _job=None,
        )

    def test_windows_without_job_object_blocks(self):
        self.assertEqual(job_object_gate(self._managed("win32", "NOT_ATTACHED")), "job_object_attach_failed")

    def test_windows_with_job_object_passes(self):
        self.assertIsNone(job_object_gate(self._managed("win32", "ATTACHED")))

    def test_posix_session_group_passes_without_job_object(self):
        self.assertIsNone(job_object_gate(self._managed("linux", "NOT_ATTACHED")))


class ExecuteCommandFailClosedTests(unittest.TestCase):
    def _setup(self, td):
        base = Path(td)
        (base / "root" / "workspace").mkdir(parents=True, exist_ok=True)
        (base / "root" / "evidence").mkdir(parents=True, exist_ok=True)
        ctx = WorkContext(
            work_id="W28", work_name="WORK28",
            workspace_root=str(base / "root"),
            execution_workspace=str(base / "root" / "workspace"),
            evidence_root=str(base / "root" / "evidence"),
            authorized=True, execution_id="wp2-gate",
        )
        return ctx

    def test_execute_command_blocks_when_windows_job_object_missing(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = self._setup(td)
            host = ExecutionHost()
            real_process = subprocess.Popen(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )

            def fake_spawn(args, *, cwd, env, text=True):
                return ManagedProcess(
                    process=real_process, platform="win32",
                    session_leader=False, created_via_spawn=True,
                    job_object="NOT_ATTACHED", _job=None,
                )

            with patch("execution_host.host_run.spawn_managed", side_effect=fake_spawn):
                result = host.execute_command(ctx, [sys.executable, "-c", "print(1)"], 10)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blocker"], "job_object_attach_failed")
            self.assertEqual(result["cleanup"]["job_object"], "NOT_ATTACHED")
            self.assertIsNotNone(real_process.poll())
            self.assertTrue(Path(result["evidence_ref"]).is_file())

    def test_execute_command_unpatched_passes_on_ci_platform(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = self._setup(td)
            host = ExecutionHost()
            result = host.execute_command(ctx, [sys.executable, "-c", "print('wp2-gate')"], 15)
            self.assertEqual(result["status"], "PASS")
            self.assertIn("wp2-gate", result["stdout_summary"])
            self.assertTrue(Path(result["evidence_ref"]).is_file())


if __name__ == "__main__":
    unittest.main()
