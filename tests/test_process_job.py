"""Unit tests for process_job POSIX counter and ManagedProcess lifecycle."""
from __future__ import annotations

import subprocess
import sys
import unittest
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
            env={"PATH": __import__("os").environ.get("PATH", "")},
        )
        managed.process.communicate(timeout=10)
        result = managed.cleanup(terminate_first=False)
        self.assertIsInstance(result, CleanupResult)
        self.assertTrue(result.process_reaped)
        self.assertIsNotNone(result.leader_pid)

    def test_cleanup_timeout_child(self):
        managed = spawn_managed(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            cwd=".",
            env={"PATH": __import__("os").environ.get("PATH", "")},
        )
        try:
            managed.process.communicate(timeout=0.05)
            self.fail("expected TimeoutExpired")
        except subprocess.TimeoutExpired:
            pass
        result = managed.cleanup(terminate_first=True, wait_timeout=3.0)
        self.assertTrue(result.process_reaped)
        self.assertTrue(result.terminate_sent or result.kill_sent)


class SpawnLifecycleTests(unittest.TestCase):
    def test_spawn_marks_created_via_spawn(self):
        managed = spawn_managed(
            [sys.executable, "-c", "print(1)"],
            cwd=".",
            env={"PATH": __import__("os").environ.get("PATH", "")},
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


if __name__ == "__main__":
    unittest.main()
