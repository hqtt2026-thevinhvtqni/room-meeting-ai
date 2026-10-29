"""Lifecycle tests for ManagedProcess: Job Object (Windows) / session (POSIX).

On Windows, spawn_managed must attach a real Job Object (job_object=ATTACHED)
when CreateJobObject + Assign succeed. taskkill is not used as Job Object proof.

On Linux, job_object remains NOT_ATTACHED; process group + killpg is used.

ISOLATION_STATUS stays NOT_VERIFIED (OS sandbox != Job Object tree containment).
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_host.process_job import (
    CleanupResult,
    ISOLATION_STATUS,
    _posix_group_members,
    spawn_managed,
    spawn_managed_service,
    wrap_existing_popen,
)

_IS_WIN = sys.platform.startswith("win")


class PosixCounterTests(unittest.TestCase):
    def test_empty_and_blank_lines_do_not_block_count(self):
        fake = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="\n  123\n\n  456 \n", stderr=""
        )
        with patch("execution_host.process_job.subprocess.run", return_value=fake):
            self.assertEqual(_posix_group_members(999), 2)

    def test_non_digit_tokens_skipped(self):
        fake = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="abc\n42\n", stderr=""
        )
        with patch("execution_host.process_job.subprocess.run", return_value=fake):
            self.assertEqual(_posix_group_members(1), 1)

    def test_invalid_pgid(self):
        self.assertEqual(_posix_group_members(0), 0)
        self.assertEqual(_posix_group_members(-1), 0)


class ManagedProcessTests(unittest.TestCase):
    def test_cleanup_reaps_finished_process(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print('x')"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        managed.process.communicate(timeout=10)
        result = managed.cleanup(terminate_first=False)
        self.assertIsInstance(result, CleanupResult)
        self.assertTrue(result.process_reaped)
        if _IS_WIN:
            self.assertEqual(result.job_object, "ATTACHED")
            self.assertIn("job_object_assigned", getattr(managed, "_spawn_notes", ()))
        else:
            self.assertEqual(result.job_object, "NOT_ATTACHED")

    def test_cleanup_timeout_single_process(self):
        managed = spawn_managed(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        try:
            managed.process.communicate(timeout=0.05)
            self.fail("expected TimeoutExpired")
        except subprocess.TimeoutExpired:
            pass
        result = managed.cleanup(terminate_first=True, wait_timeout=3.0)
        self.assertTrue(result.process_reaped)
        if result.leader_pid:
            self.assertFalse(_pid_alive(result.leader_pid))
        if _IS_WIN:
            self.assertEqual(result.job_object, "ATTACHED")
            self.assertTrue(
                "TerminateJobObject_ok" in result.notes
                or "TerminateJobObject_failed" in str(result.notes)
            )


class SpawnLifecycleTests(unittest.TestCase):
    def test_spawn_marks_created_via_spawn(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print(1)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        managed.process.communicate(timeout=10)
        self.assertTrue(managed.created_via_spawn)
        result = managed.cleanup(terminate_first=False)
        if _IS_WIN:
            self.assertEqual(managed.job_object, "ATTACHED")
            self.assertEqual(result.job_object, "ATTACHED")
        else:
            self.assertEqual(result.job_object, "NOT_ATTACHED")
        self.assertNotIn("wrapped_existing_popen", result.notes)

    def test_wrap_existing_is_labeled(self):
        p = subprocess.Popen(
            [sys.executable, "-c", "print(1)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        p.communicate(timeout=10)
        managed = wrap_existing_popen(p)
        self.assertFalse(managed.created_via_spawn)
        result = managed.cleanup(terminate_first=False)
        self.assertIn("wrapped_existing_popen", result.notes)
        self.assertIn("job_object_cannot_attach_retroactively", result.notes)
        self.assertEqual(result.job_object, "NOT_ATTACHED")

    def test_isolation_status_not_verified(self):
        self.assertEqual(ISOLATION_STATUS, "NOT_VERIFIED")


class ProcessTreeTests(unittest.TestCase):
    def _start_tree(self, child_pid_file: Path):
        script = (
            "import subprocess, sys, time\n"
            f"path = r'{child_pid_file}'\n"
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(90)'])\n"
            "open(path, 'w', encoding='utf-8').write(str(child.pid))\n"
            "time.sleep(90)\n"
        )
        managed = spawn_managed(
            [sys.executable, "-c", script],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        child_pid = _wait_for_child_pid_file(child_pid_file, timeout_sec=5.0)
        return managed, child_pid

    def test_windows_job_object_attached_at_spawn(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print(1)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        try:
            if _IS_WIN:
                self.assertEqual(
                    managed.job_object,
                    "ATTACHED",
                    f"spawn_notes={getattr(managed, '_spawn_notes', ())}",
                )
                self.assertIsNotNone(managed._job)
            else:
                self.assertEqual(managed.job_object, "NOT_ATTACHED")
        finally:
            managed.process.communicate(timeout=10)
            managed.cleanup(terminate_first=False)

    def test_parent_and_child_pids_reaped_after_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            pid_file = Path(td) / "child.pid"
            managed, child_pid = self._start_tree(pid_file)
            self.assertIsNotNone(child_pid, "child PID file not written")
            parent_pid = managed.pid
            self.assertTrue(_pid_alive(parent_pid))
            self.assertTrue(_pid_alive(child_pid))
            if _IS_WIN:
                self.assertEqual(managed.job_object, "ATTACHED")
            result = managed.cleanup(terminate_first=True, wait_timeout=8.0)
            self.assertTrue(result.process_reaped, f"parent not reaped: {result.as_dict()}")
            self.assertFalse(_pid_alive(parent_pid), f"parent {parent_pid} alive")
            self.assertFalse(
                _pid_alive(child_pid),
                f"child {child_pid} alive notes={result.notes}",
            )
            if _IS_WIN:
                self.assertEqual(result.job_object, "ATTACHED")
                self.assertIn("TerminateJobObject_ok", result.notes)

    def test_timeout_then_parent_and_child_reaped(self):
        with tempfile.TemporaryDirectory() as td:
            pid_file = Path(td) / "child.pid"
            managed, child_pid = self._start_tree(pid_file)
            self.assertIsNotNone(child_pid)
            parent_pid = managed.pid
            try:
                managed.process.communicate(timeout=0.25)
                self.fail("expected TimeoutExpired")
            except subprocess.TimeoutExpired:
                pass
            result = managed.cleanup(terminate_first=True, wait_timeout=8.0)
            self.assertTrue(result.process_reaped)
            self.assertFalse(_pid_alive(parent_pid))
            self.assertFalse(
                _pid_alive(child_pid),
                f"child {child_pid} alive notes={result.notes}",
            )
            if _IS_WIN:
                self.assertEqual(result.job_object, "ATTACHED")

    def test_cleanup_failure_notes_when_wrap_only(self):
        p = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(15)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        managed = wrap_existing_popen(p)
        result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
        self.assertEqual(result.job_object, "NOT_ATTACHED")
        self.assertIn("wrapped_existing_popen", result.notes)
        self.assertIn("job_object_cannot_attach_retroactively", result.notes)


class ServiceSpawnTests(unittest.TestCase):
    def test_spawn_managed_service_job_object_rules(self):
        managed = spawn_managed_service(
            [sys.executable, "-c", "import time; time.sleep(20)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        try:
            self.assertTrue(managed.created_via_spawn)
            if _IS_WIN:
                self.assertEqual(
                    managed.job_object,
                    "ATTACHED",
                    f"spawn_notes={getattr(managed, '_spawn_notes', ())}",
                )
            else:
                self.assertEqual(managed.job_object, "NOT_ATTACHED")
            self.assertIsNone(managed.poll())
        finally:
            result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
            self.assertTrue(result.process_reaped)
            if _IS_WIN:
                self.assertIn("TerminateJobObject_ok", result.notes)


def _wait_for_child_pid_file(path: Path, timeout_sec: float = 5.0):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if path.is_file():
            text = path.read_text(encoding="utf-8").strip()
            if text.isdigit():
                return int(text)
        time.sleep(0.05)
    return None


def _pid_alive(pid):
    if pid is None or pid <= 0:
        return False
    if sys.platform.startswith("win"):
        try:
            completed = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            out = (completed.stdout or "").strip()
            if not out or "No tasks" in out or out.startswith("INFO:"):
                return False
            return str(pid) in out
        except (OSError, subprocess.TimeoutExpired):
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    unittest.main()
