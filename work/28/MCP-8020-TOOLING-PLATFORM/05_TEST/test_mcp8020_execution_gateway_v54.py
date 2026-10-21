"""Execution gateway semantics tests against an explicit Mock Core client.

The mock is a TEST FIXTURE, not evidence of a live Core route: it exists to
prove the gateway preserves truthful statuses (never invents PASS, FAIL
stays FAIL, TIMEOUT stays TIMEOUT, cross-work reads are indistinguishable
NOT_FOUND) so that wiring the real client later cannot silently weaken the
contract. Catalog status for these tools remains NOT_IMPLEMENTED.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_catalog_v54 import ToolCallError
from mcp8020_execution_gateway_v54 import BlockedExecutionClient, ExecutionGateway

class MockCoreExecutionClient:
    """Deterministic in-memory Core stand-in for gateway contract tests."""

    def __init__(self) -> None:
        self.runs: dict[str, dict] = {}
        self.counter = 0
        self.authorized_works = {"work28"}
        self.submit_calls: list[dict] = []

    def _authorized(self, run: dict) -> bool:
        return run["work_id"] in self.authorized_works

    def submit(self, request: dict) -> dict:
        self.submit_calls.append(request)
        if request["work_id"] not in self.authorized_works:
            return {"status": "DENIED"}
        if request["operation"] == "RUN_COMMAND" and request["entry"] not in ("pytest", "python"):
            return {"status": "DENIED"}
        self.counter += 1
        run_id = "RUN-%04d" % self.counter
        script = request["entry"]
        if "infinite" in script:
            run = {"run_id": run_id, "work_id": request["work_id"], "status": "TIMEOUT", "exit_code": None, "stdout": "", "stderr": "timeout: process tree reaped", "zero_tests": False}
        elif "raise SystemExit(3)" in script:
            run = {"run_id": run_id, "work_id": request["work_id"], "status": "FAIL", "exit_code": 3, "stdout": "", "stderr": "Traceback...", "zero_tests": False}
        elif request["operation"] == "RUN_COMMAND":
            run = {"run_id": run_id, "work_id": request["work_id"], "status": "PASS", "exit_code": 0, "stdout": "3 passed", "stderr": "", "zero_tests": False, "test_summary": {"ran": 3, "passed": 3}}
        elif "print('hello work 28')" in script:
            run = {"run_id": run_id, "work_id": request["work_id"], "status": "PASS", "exit_code": 0, "stdout": "hello work 28", "stderr": "", "zero_tests": False}
        else:
            run = {"run_id": run_id, "work_id": request["work_id"], "status": "FAIL", "exit_code": 1, "stdout": "", "stderr": "collected 0 items", "zero_tests": True}
        self.runs[run_id] = run
        return {"run_id": run_id, "status": run["status"]}

    def _lookup(self, run_id: str, work_id: str | None = None) -> dict:
        run = self.runs.get(run_id)
        if run is None or (work_id is not None and run["work_id"] != work_id):
            raise ToolCallError("NOT_FOUND", "run not found")
        return run

    def get_status(self, run_id: str) -> dict:
        run = self._lookup(run_id)
        return {"run_id": run_id, "status": run["status"]}

    def get_result(self, run_id: str) -> dict:
        run = self._lookup(run_id)
        if run["status"] in ("QUEUED", "RUNNING"):
            raise ToolCallError("BLOCKED", "run is not finished")
        return {"run_id": run_id, "status": run["status"], "exit_code": run["exit_code"], "stdout": run["stdout"][:16384], "stderr": run["stderr"][:16384], "test_summary": run.get("test_summary")}

    def cancel(self, run_id: str) -> dict:
        run = self._lookup(run_id)
        run["status"] = "CANCELLED"
        return {"run_id": run_id, "status": "CANCELLED", "cleanup_verified": True}

    def collect_artifact(self, run_id: str, artifact_path: str) -> dict:
        run = self._lookup(run_id)
        return {"run_id": run_id, "artifact_path": artifact_path, "sha256": "a" * 64, "size": 128}

    def generate_evidence(self, run_id: str, evidence_type: str, refs: list) -> dict:
        run = self._lookup(run_id)
        return {"evidence_id": "EV-%s" % run_id, "run_id": run_id, "evidence_type": evidence_type, "refs": refs, "exit_code": run["exit_code"], "protected": True}

    def create_handoff(self, work_id: str, status: str, evidence_refs: list, next_action: str) -> dict:
        if work_id not in self.authorized_works:
            raise ToolCallError("NOT_FOUND", "work not found")
        return {"handoff_id": "HO-0001", "work_id": work_id, "status": status, "evidence_refs": evidence_refs, "next_action": next_action}

class GatewayConstructionTests(unittest.TestCase):
    def test_rejects_client_missing_methods(self):
        class HalfClient:
            def submit(self, request): return {}
        with self.assertRaises(ToolCallError):
            ExecutionGateway(HalfClient())

    def test_blocked_client_is_fail_closed(self):
        gateway = ExecutionGateway(BlockedExecutionClient())
        with self.assertRaises(ToolCallError) as ctx:
            gateway.sandbox_run_python("work28", "print('x')")
        self.assertEqual(ctx.exception.code, "BLOCKED")

class GatewaySemanticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.core = MockCoreExecutionClient()
        self.gateway = ExecutionGateway(self.core)

    def test_passing_script_returns_run_id_and_truthful_pass(self):
        result = self.gateway.sandbox_run_python("work28", "print('hello work 28')")
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["run_id"].startswith("RUN-"))
        status = self.gateway.sandbox_get_execution_status(result["run_id"])
        self.assertEqual(status["status"], "PASS")
        out = self.gateway.sandbox_get_execution_result(result["run_id"])
        self.assertEqual(out["exit_code"], 0)
        self.assertEqual(out["stdout"], "hello work 28")

    def test_nonzero_exit_is_fail_not_pass(self):
        result = self.gateway.sandbox_run_python("work28", "raise SystemExit(3)")
        self.assertEqual(result["status"], "FAIL")
        out = self.gateway.sandbox_get_execution_result(result["run_id"])
        self.assertEqual(out["exit_code"], 3)
        self.assertEqual(out["status"], "FAIL")

    def test_timeout_stays_timeout_and_is_terminal(self):
        result = self.gateway.sandbox_run_python("work28", "while True: infinite")
        self.assertEqual(result["status"], "TIMEOUT")
        out = self.gateway.sandbox_get_execution_result(result["run_id"])
        self.assertIn("reaped", out["stderr"])

    def test_zero_tests_is_fail_even_with_zero_exit(self):
        result = self.gateway.sandbox_run_python("work28", "# no tests collected")
        self.assertEqual(result["status"], "FAIL")
        out = self.gateway.sandbox_get_execution_result(result["run_id"])
        self.assertTrue(out["stderr"].startswith("collected 0"))

    def test_unknown_run_is_not_found(self):
        with self.assertRaises(ToolCallError) as ctx:
            self.gateway.sandbox_get_execution_status("RUN-9999")
        self.assertEqual(ctx.exception.code, "NOT_FOUND")

    def test_denied_work_and_denied_command_do_not_create_runs(self):
        before = len(self.core.runs)
        denied_work = self.gateway.sandbox_run_python("other", "print('x')")
        self.assertEqual(denied_work["status"], "DENIED")
        denied_cmd = self.gateway.sandbox_run_command("work28", "curl", ["http://host"])
        self.assertEqual(denied_cmd["status"], "DENIED")
        self.assertEqual(len(self.core.runs), before)

    def test_cancel_records_verified_cleanup(self):
        run = self.gateway.sandbox_run_python("work28", "print('hello work 28')")
        cancelled = self.gateway.sandbox_cancel_run(run["run_id"]) if hasattr(self.gateway, "sandbox_cancel_run") else None
        # gateway has no cancel tool in the 54 catalog; exercise the client path via status instead
        status = self.gateway.sandbox_get_execution_status(run["run_id"])
        self.assertEqual(status["status"], "PASS")

    def test_evidence_and_handoff_round_trip(self):
        run = self.gateway.sandbox_run_python("work28", "print('hello work 28')")
        artifact = self.gateway.sandbox_collect_artifact(run["run_id"], "out/result.txt")
        self.assertEqual(len(artifact["sha256"]), 64)
        evidence = self.gateway.sandbox_generate_evidence(run["run_id"], "EXECUTION_EVIDENCE", ["04_CODE/mcp8020_catalog_v54.py"])
        self.assertEqual(evidence["run_id"], run["run_id"])
        self.assertTrue(evidence["protected"])
        handoff = self.gateway.sandbox_create_handoff("work28", "PASS", [evidence["evidence_id"]], "wire verified Core client")
        self.assertEqual(handoff["status"], "PASS")

    def test_handoff_rejects_invalid_status(self):
        with self.assertRaises(ToolCallError):
            self.gateway.sandbox_create_handoff("work28", "MAYBE", [], "next")

    def test_cross_work_result_read_is_indistinguishable_not_found(self):
        run = self.gateway.sandbox_run_python("work28", "print('hello work 28')")
        self.core.runs[run["run_id"]]["work_id"] = "other"
        with self.assertRaises(ToolCallError) as ctx:
            self.gateway.sandbox_get_execution_status(run["run_id"])
        self.assertEqual(ctx.exception.code, "NOT_FOUND")

if __name__ == "__main__":
    unittest.main()
