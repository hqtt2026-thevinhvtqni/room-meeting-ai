"""WP2 close-out tests: structured BLOCKED mapping for start_service()
and concurrency / repeated spawn-cleanup race coverage.

These tests do NOT claim OS isolation and do not touch the quarantined
historical MCP :8020 listener. They verify:
  1. A containment failure at service spawn surfaces as a structured
     BLOCKED result (never an uncaught OSError) and registers nothing.
  2. Repeated spawn -> cleanup cycles reap every leader and leave no
     surviving member behind.
  3. Concurrent spawn/cleanup of several managed processes reaps all of
     them (race coverage for the shared processes registry and cleanup
     path).
"""
from __future__ import annotations

import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from execution_host.host import ExecutionHost
from execution_host.models import WorkContext
from execution_host.process_job import (
    JobObjectUnavailable,
    spawn_managed,
)


def _ctx(base: Path) -> WorkContext:
    root = base / "root"
    (root / "workspace").mkdir(parents=True, exist_ok=True)
    (root / "evidence").mkdir(parents=True, exist_ok=True)
    return WorkContext(
        work_id="W28",
        work_name="WORK28",
        workspace_root=str(root),
        execution_workspace=str(root / "workspace"),
        evidence_root=str(root / "evidence"),
        authorized=True,
        execution_id="wp2-race",
    )


class StartServiceBlockedMappingTests(unittest.TestCase):
    def test_containment_failure_maps_to_structured_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()

            def failing_spawn(args, *, cwd, env):
                raise JobObjectUnavailable(
                    ["job_object_create_failed", "kernel32_unavailable"],
                    process_reaped=True,
                )

            with patch(
                "execution_host.host.spawn_managed_service",
                side_effect=failing_spawn,
            ):
                result = host.start_service(
                    "svc", [sys.executable, "-c", "import time; time.sleep(5)"], ctx
                )

            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blocker"], "job_object_attach_failed")
            self.assertIn("job_object_create_failed", result["notes"])
            self.assertTrue(result["process_reaped"])
            self.assertIsNone(result["pid"])
            self.assertNotIn("svc", host.processes)

    def test_blocked_start_registers_nothing_and_retry_can_pass(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            calls = {"n": 0}

            def flaky_spawn(args, *, cwd, env):
                calls["n"] += 1
                if calls["n"] == 1:
                    raise JobObjectUnavailable(["assign_failed"], process_reaped=True)
                return spawn_managed(
                    args, cwd=cwd, env=env,
                )

            cmd = [sys.executable, "-c", "import time; time.sleep(5)"]
            with patch(
                "execution_host.host.spawn_managed_service",
                side_effect=flaky_spawn,
            ):
                first = host.start_service("svc", cmd, ctx)
                self.assertEqual(first["status"], "BLOCKED")
                self.assertEqual(host.service_status("svc", ctx)["status"], "STOPPED")

                second = host.start_service("svc", cmd, ctx)
                self.assertEqual(second["status"], "PASS")

            stop = host.stop_service("svc", ctx)
            self.assertEqual(stop["status"], "PASS")
            self.assertTrue(stop["process_reaped"])


class RepeatedSpawnCleanupTests(unittest.TestCase):
    def test_repeated_spawn_cleanup_cycles_reap_every_leader(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
            for cycle in range(5):
                managed = spawn_managed(cmd, cwd=ctx.execution_workspace, env={})
                self.assertIsNone(managed.poll(), f"cycle {cycle}: not started")
                result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
                self.assertTrue(
                    result.process_reaped,
                    f"cycle {cycle}: not reaped ({result.notes})",
                )
                self.assertIsNotNone(managed.poll())

    def test_spawn_cleanup_of_exited_process_is_still_reaped(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            cmd = [sys.executable, "-c", "pass"]
            managed = spawn_managed(cmd, cwd=ctx.execution_workspace, env={})
            deadline = time.monotonic() + 10
            while managed.poll() is None and time.monotonic() < deadline:
                time.sleep(0.05)
            result = managed.cleanup(terminate_first=False, wait_timeout=5.0)
            self.assertTrue(result.process_reaped, f"notes={result.notes}")


class ConcurrentSpawnCleanupTests(unittest.TestCase):
    def test_concurrent_spawn_cleanup_all_reaped(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
            results: list = []
            errors: list = []
            lock = threading.Lock()

            def worker(i: int) -> None:
                try:
                    managed = spawn_managed(cmd, cwd=ctx.execution_workspace, env={})
                    time.sleep(0.05 * (i % 3))
                    res = managed.cleanup(terminate_first=True, wait_timeout=10.0)
                    with lock:
                        results.append((i, res.process_reaped, managed.poll()))
                except Exception as exc:  # pragma: no cover - surfaced below
                    with lock:
                        errors.append((i, repr(exc)))

            threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=60)

            self.assertEqual(errors, [])
            self.assertEqual(len(results), 4)
            for i, reaped, poll in results:
                self.assertTrue(reaped, f"worker {i}: not reaped")
                self.assertIsNotNone(poll, f"worker {i}: still running")


if __name__ == "__main__":
    unittest.main()
