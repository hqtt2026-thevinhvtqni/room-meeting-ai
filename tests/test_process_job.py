"""Lifecycle tests for ManagedProcess: counter, cleanup, process tree honesty.

Windows Job Object is intentionally NOT_ATTACHED in this build. Tests assert that
fact rather than treating green CI as proof of OS isolation.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_host.process_job import (
    CleanupResult,
    ManagedProcess,
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
        self.assertIsNotNone(result.leader_pid)
        self.assertEqual(result.job_object, "NOT_ATTACHED")

    def test_cleanup_timeout_child(self):
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
        self.assertTrue(
            result.terminate_sent or result.kill_sent or "taskkill_tree_attempted" in result.notes
        )
        self.assertEqual(result.job_object, "NOT_ATTACHED")


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
    """Parent + child process tree cleanup.

    On POSIX, start_new_session + killpg should reap the group.
    On Windows, Job Object is NOT_ATTACHED; taskkill /T is best-effort only.
    """

    _PARENT_CHILD_SCRIPT = (
        "import subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        "print(child.pid, flush=True)\n"
        "time.sleep(60)\n"
    )

    def test_job_object_never_claimed_attached(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print(1)"],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        managed.process.communicate(timeout=10)
        result = managed.cleanup(terminate_first=False)
        self.assertEqual(result.job_object, "NOT_ATTACHED")
        self.assertNotEqual(result.job_object, "ATTACHED")

    def test_parent_child_tree_cleanup(self):
        managed = spawn_managed(
            [sys.executable, "-c", self._PARENT_CHILD_SCRIPT],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        time.sleep(0.4)
        result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
        self.assertTrue(
            result.process_reaped,
            f"leader not reaped: {result.as_dict()}",
        )
        self.assertEqual(result.job_object, "NOT_ATTACHED")
        self.assertIsNotNone(result.leader_pid)
        if result.leader_pid:
            self.assertFalse(
                _pid_alive(result.leader_pid),
                f"leader pid {result.leader_pid} still alive after cleanup",
            )

    def test_timeout_then_cleanup_reaps_leader(self):
        managed = spawn_managed(
            [sys.executable, "-c", self._PARENT_CHILD_SCRIPT],
            cwd=".",
            env={"PATH": os.environ.get("PATH", "")},
        )
        try:
            managed.process.communicate(timeout=0.2)
            self.fail("expected TimeoutExpired")
        except subprocess.TimeoutExpired:
            pass
        result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
        self.assertTrue(result.process_reaped)
        self.assertEqual(result.job_object, "NOT_ATTACHED")
        if result.leader_pid:
            self.assertFalse(_pid_alive(result.leader_pid))


def _pid_alive(pid: int) -> bool:
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
            out = completed.stdout or ""
            return str(pid) in out and "No tasks" not in out
        except (OSError, subprocess.TimeoutExpired):
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    unittest.main()
