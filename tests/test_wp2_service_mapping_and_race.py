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
from types import SimpleNamespace
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from execution_host.host import ExecutionHost
from execution_host.models import WorkContext
from execution_host.process_job import (
    JobObjectUnavailable,
    ManagedProcess,
    spawn_managed,
    spawn_managed_service,
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


class FakeServiceProcess:
    def __init__(self, pid: int, returncode: int | None = None):
        self.pid = pid
        self.returncode = returncode

    def poll(self):
        return self.returncode


class ServiceRegistryRecoveryTests(unittest.TestCase):
    def test_stop_retains_registry_entry_until_cleanup_is_verified(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            managed = ManagedProcess(
                process=FakeServiceProcess(7001, returncode=None),
                platform="linux",
                created_via_spawn=True,
            )
            failed = SimpleNamespace(
                process_reaped=False,
                as_dict=lambda: {"process_reaped": False, "notes": ["child_still_alive"]},
            )
            passed = SimpleNamespace(
                process_reaped=True,
                as_dict=lambda: {"process_reaped": True, "notes": ["group_drained"]},
            )
            managed.cleanup = Mock(side_effect=[failed, failed, passed])
            host.processes["svc"] = managed

            first = host.stop_service("svc", ctx)
            self.assertEqual(first["status"], "BLOCKED")
            self.assertIs(host.processes.get("svc"), managed)
            self.assertEqual(host.service_status("svc", ctx)["status"], "BLOCKED")

            # A new start must retry cleanup, not claim the still-running service is healthy.
            with patch("execution_host.host.spawn_managed_service") as spawn:
                retry_start = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)
            self.assertEqual(retry_start["status"], "BLOCKED")
            spawn.assert_not_called()

            second = host.stop_service("svc", ctx)
            self.assertEqual(second["status"], "PASS")
            self.assertNotIn("svc", host.processes)

    def test_start_does_not_replace_exited_leader_with_unreaped_descendants(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            managed = ManagedProcess(
                process=FakeServiceProcess(7002, returncode=0),
                platform="linux",
                created_via_spawn=True,
            )
            failed = SimpleNamespace(
                process_reaped=False,
                as_dict=lambda: {"process_reaped": False, "notes": ["descendant_remains"]},
            )
            managed.cleanup = Mock(return_value=failed)
            host.processes["svc"] = managed

            with patch("execution_host.host.spawn_managed_service") as spawn:
                result = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)

            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blocker"], "existing_service_cleanup_unverified")
            self.assertIs(host.processes.get("svc"), managed)
            spawn.assert_not_called()

    def test_service_status_does_not_call_dead_leader_stopped_with_live_members(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            managed = ManagedProcess(
                process=FakeServiceProcess(7003, returncode=0),
                platform="linux",
                created_via_spawn=True,
            )
            managed.members_count = Mock(return_value=1)
            host.processes["svc"] = managed

            result = host.service_status("svc", ctx)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["pid"], 7003)
            self.assertEqual(result["members"], 1)
            self.assertEqual(result["readiness"], "NOT_CHECKED")

    def test_concurrent_same_name_starts_register_exactly_one_process(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            managed = ManagedProcess(
                process=FakeServiceProcess(7004, returncode=None),
                platform="linux",
                created_via_spawn=True,
                job_object="ATTACHED",
            )
            calls = []
            results = []
            errors = []
            lock = threading.Lock()

            def fake_spawn(args, *, cwd, env):
                time.sleep(0.05)
                with lock:
                    calls.append(1)
                return managed

            def worker():
                try:
                    result = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)
                    with lock:
                        results.append(result)
                except Exception as exc:
                    with lock:
                        errors.append(repr(exc))

            with patch("execution_host.host.spawn_managed_service", side_effect=fake_spawn):
                threads = [threading.Thread(target=worker) for _ in range(6)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=10)

            self.assertEqual(errors, [])
            self.assertEqual(len(results), 6)
            self.assertEqual(len(calls), 1)
            self.assertTrue(all(item["pid"] == 7004 for item in results))
            self.assertEqual(sum(bool(item.get("already_running")) for item in results), 5)
            self.assertIs(host.processes.get("svc"), managed)


class LegacyPopenFailClosedTests(unittest.TestCase):
    def test_dead_legacy_popen_is_blocked_and_never_replaced(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()

            class DeadLegacyPopen:
                pid = 7020
                returncode = 0
                def poll(self):
                    return 0

            legacy = DeadLegacyPopen()
            host.processes["svc"] = legacy

            status = host.service_status("svc", ctx)
            self.assertEqual(status["status"], "BLOCKED")
            self.assertIsNone(status["members"])

            with patch("execution_host.host.spawn_managed_service") as spawn:
                result = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)

            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blocker"], "existing_service_cleanup_unverified")
            self.assertIs(host.processes.get("svc"), legacy)
            spawn.assert_not_called()

    def test_stop_legacy_popen_never_claims_tree_reaped(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()

            class DeadLegacyPopen:
                pid = 7021
                returncode = 0
                def poll(self):
                    return 0

            legacy = DeadLegacyPopen()
            host.processes["svc"] = legacy
            result = host.stop_service("svc", ctx)

            self.assertEqual(result["status"], "BLOCKED")
            self.assertFalse(result["process_reaped"])
            self.assertIs(host.processes.get("svc"), legacy)


class ConcurrentStartStopStatusTests(unittest.TestCase):
    def test_barrier_controlled_start_stop_status_has_one_registry_owner(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            cleanup_entered = threading.Event()
            allow_cleanup = threading.Event()

            old = ManagedProcess(
                process=FakeServiceProcess(7030, returncode=None),
                platform="linux",
                created_via_spawn=True,
            )
            def delayed_cleanup(*args, **kwargs):
                cleanup_entered.set()
                if not allow_cleanup.wait(timeout=5):
                    raise AssertionError("cleanup release timed out")
                return SimpleNamespace(
                    process_reaped=True,
                    as_dict=lambda: {"process_reaped": True, "notes": ["verified_empty"]},
                )
            old.cleanup = Mock(side_effect=delayed_cleanup)
            host.processes["svc"] = old

            replacement = ManagedProcess(
                process=FakeServiceProcess(7031, returncode=None),
                platform="linux",
                created_via_spawn=True,
                job_object="ATTACHED",
            )
            stop_results = []
            start_results = []
            status_results = []
            errors = []

            def stop_worker():
                try:
                    stop_results.append(host.stop_service("svc", ctx))
                except Exception as exc:
                    errors.append(repr(exc))

            def start_worker():
                try:
                    start_results.append(host.start_service("svc", [sys.executable, "-c", "pass"], ctx))
                except Exception as exc:
                    errors.append(repr(exc))

            def status_worker():
                try:
                    status_results.append(host.service_status("svc", ctx))
                except Exception as exc:
                    errors.append(repr(exc))

            with patch("execution_host.host.spawn_managed_service", return_value=replacement) as spawn:
                stop_thread = threading.Thread(target=stop_worker)
                stop_thread.start()
                self.assertTrue(cleanup_entered.wait(timeout=5), "stop did not enter cleanup")

                start_thread = threading.Thread(target=start_worker)
                status_thread = threading.Thread(target=status_worker)
                start_thread.start()
                status_thread.start()
                allow_cleanup.set()

                for thread in (stop_thread, start_thread, status_thread):
                    thread.join(timeout=10)
                    self.assertFalse(thread.is_alive(), "registry transition thread hung")

            self.assertEqual(errors, [])
            self.assertEqual(len(stop_results), 1)
            self.assertEqual(stop_results[0]["status"], "PASS")
            self.assertEqual(len(start_results), 1)
            self.assertEqual(start_results[0]["status"], "PASS")
            self.assertEqual(len(status_results), 1)
            self.assertIn(status_results[0]["status"], {"PASS", "STOPPED"})
            self.assertIs(host.processes.get("svc"), replacement)
            spawn.assert_called_once()


class AdditionalServiceBoundaryTests(unittest.TestCase):
    def test_generic_spawn_oserror_maps_to_structured_blocked_without_false_reap(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            with patch(
                "execution_host.host.spawn_managed_service",
                side_effect=OSError("injected process creation failure"),
            ):
                result = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)

            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["blocker"], "service_spawn_failed")
            self.assertEqual(result["spawn_error_type"], "OSError")
            self.assertIsNone(result["process_reaped"])
            self.assertNotIn("svc", host.processes)

    def test_service_status_does_not_claim_application_readiness(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            managed = ManagedProcess(
                process=FakeServiceProcess(7010, returncode=None),
                platform="linux",
                created_via_spawn=True,
            )
            host.processes["svc"] = managed
            result = host.service_status("svc", ctx)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["readiness"], "NOT_CHECKED")

    def test_restart_drains_real_child_after_parent_leader_exits(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            child_code = "import time; time.sleep(30)"
            parent_code = "import subprocess,sys; subprocess.Popen([sys.executable, '-c', sys.argv[1]])"
            old = spawn_managed_service(
                [sys.executable, "-c", parent_code, child_code],
                cwd=ctx.execution_workspace,
                env={},
            )
            old.process.wait(timeout=10)
            self.assertIsNotNone(old.poll(), "service leader should exit before replacement")

            deadline = time.monotonic() + 10
            members = old.members_count()
            while members in (0, None) and time.monotonic() < deadline:
                time.sleep(0.05)
                members = old.members_count()
            self.assertGreater(members or 0, 0, "child process should remain in the managed tree")

            cleanup_results = []
            real_cleanup = old.cleanup

            def capture_cleanup(*args, **kwargs):
                result = real_cleanup(*args, **kwargs)
                cleanup_results.append(result)
                return result

            old.cleanup = capture_cleanup
            replacement = ManagedProcess(
                process=FakeServiceProcess(7011, returncode=None),
                platform="linux",
                created_via_spawn=True,
                job_object="ATTACHED",
            )
            host.processes["svc"] = old

            with patch("execution_host.host.spawn_managed_service", return_value=replacement) as spawn:
                result = host.start_service("svc", [sys.executable, "-c", "pass"], ctx)

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(len(cleanup_results), 1)
            self.assertTrue(cleanup_results[0].process_reaped, cleanup_results[0].notes)
            self.assertIs(host.processes.get("svc"), replacement)
            spawn.assert_called_once()


class SpawnFailureCleanupEvidenceTests(unittest.TestCase):
    def test_unreaped_suspended_spawn_is_not_reported_as_no_process(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            failure = JobObjectUnavailable(
                ["AssignProcessToJobObject_failed_err=5", "abort_wait_timeout"],
                process_reaped=False,
            )
            with patch("execution_host.host_run.spawn_managed", side_effect=failure):
                result = host.execute_command(ctx, [sys.executable, "-c", "pass"])

            cleanup = result["cleanup"]
            self.assertFalse(cleanup["process_reaped"])
            self.assertIn("suspended_spawn_abort_reap_unconfirmed", cleanup["notes"])
            self.assertNotIn("no_process", cleanup["notes"])

    def test_reaped_suspended_spawn_preserves_positive_abort_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            ctx = _ctx(Path(td))
            host = ExecutionHost()
            failure = JobObjectUnavailable(
                ["AssignProcessToJobObject_failed_err=5"],
                process_reaped=True,
            )
            with patch("execution_host.host_run.spawn_managed", side_effect=failure):
                result = host.execute_command(ctx, [sys.executable, "-c", "pass"])

            cleanup = result["cleanup"]
            self.assertTrue(cleanup["process_reaped"])
            self.assertIn("suspended_spawn_abort_reaped", cleanup["notes"])
            self.assertNotIn("no_process", cleanup["notes"])


if __name__ == "__main__":
    unittest.main()
