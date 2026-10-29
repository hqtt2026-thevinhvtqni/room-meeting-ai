"""Lifecycle tests for ManagedProcess: counter, cleanup, process tree honesty.

Windows Job Object is intentionally NOT_ATTACHED. Process-tree tests record the
child PID (via a side-car file) and assert BOTH parent and child are gone after
cleanup — parent-only checks are not sufficient (Xu gate 2026-10-29).
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
    _posix_group_members,
    spawn_managed,
    wrap_existing_popen,
)


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
        self.assertEqual(result.job_object, "NOT_ATTACHED")
        if result.leader_pid:
            self.assertFalse(_pid_alive(result.leader_pid))


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


class ProcessTreeTests(unittest.TestCase):
    """Capture child PID to a file; assert parent AND child dead after cleanup."""

    def test_job_object_never_claimed_attached(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print(1)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        managed.process.communicate(timeout=10)
        result = managed.cleanup(terminate_first=False)
        self.assertEqual(result.job_object, "NOT_ATTACHED")

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

    def test_parent_and_child_pids_reaped_after_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            pid_file = Path(td) / "child.pid"
            managed, child_pid = self._start_tree(pid_file)
            self.assertIsNotNone(child_pid, "child PID file not written")
            parent_pid = managed.pid
            self.assertTrue(_pid_alive(parent_pid), "parent should be alive before cleanup")
            self.assertTrue(_pid_alive(child_pid), "child should be alive before cleanup")

            result = managed.cleanup(terminate_first=True, wait_timeout=8.0)

            self.assertEqual(result.job_object, "NOT_ATTACHED")
            self.assertTrue(result.process_reaped, f"parent not reaped: {result.as_dict()}")
            self.assertFalse(
                _pid_alive(parent_pid),
                f"parent pid {parent_pid} still alive",
            )
            self.assertFalse(
                _pid_alive(child_pid),
                f"child pid {child_pid} still alive after cleanup notes={result.notes}",
            )

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
            self.assertEqual(result.job_object, "NOT_ATTACHED")
            self.assertTrue(result.process_reaped)
            self.assertFalse(_pid_alive(parent_pid), f"parent {parent_pid} alive")
            self.assertFalse(
                _pid_alive(child_pid),
                f"child {child_pid} alive after timeout cleanup notes={result.notes}",
            )

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
        if not result.process_reaped:
            self.assertTrue(
                any("fail" in n or "timeout" in n for n in result.notes),
                f"expected reaped or failure notes: {result.notes}",
            )


def _wait_for_child_pid_file(path: Path, timeout_sec: float = 5.0) -> int | None:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if path.is_file():
            text = path.read_text(encoding="utf-8").strip()
            if text.isdigit():
                return int(text)
        time.sleep(0.05)
    return None


def _pid_alive(pid: int | None) -> bool:
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
