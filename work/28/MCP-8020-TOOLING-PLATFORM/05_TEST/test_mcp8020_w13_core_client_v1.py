"""Unit tests for the staged W13 CoreExecutionClient seam.

These tests lock the fail-closed contract of W13CoreExecutionClientV1 against
a recording fake bridge: construction validation, registry-keyed lookups,
BLOCKED for unknown runs, refused cancel at the synchronous boundary, artifact
manifest enforcement, evidence binding, and handoff validation. They also
prove the client satisfies the CoreExecutionClient protocol accepted by
ExecutionGateway. No test touches a real execution host.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[4]
CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
for path in (REPO_ROOT, CODE_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from mcp8020_catalog_v54 import ToolCallError
from mcp8020_execution_gateway_v54 import ExecutionGateway, _REQUIRED_METHODS
from mcp8020_w13_core_client_v1 import W13CoreExecutionClientV1


def make_result(execution_id="exec-1", status="PASS", exit_code=0,
                evidence_ref="ev-1", artifacts=None, blocker=None):
    def as_dict():
        return {
            "execution_id": execution_id, "work_id": "W28", "status": status,
            "evidence_ref": evidence_ref, "exit_code": exit_code,
            "stdout_ref": "stdout://1", "stderr_ref": "stderr://1",
            "artifacts": artifacts if artifacts is not None else ["out.log"],
            "blocker": blocker,
        }
    return SimpleNamespace(
        execution_id=execution_id, work_id="W28", status=status,
        evidence_ref=evidence_ref, exit_code=exit_code,
        stdout_ref="stdout://1", stderr_ref="stderr://1",
        artifacts=artifacts if artifacts is not None else ["out.log"],
        blocker=blocker, as_dict=as_dict,
    )


class FakeBridge:
    def __init__(self, result):
        self.result = result
        self.calls = []
    def invoke(self, context, request):
        self.calls.append({"context": context, "request": request})
        return self.result


def build_client(result=None, context_provider=None, request_builder=None):
    bridge = FakeBridge(result or make_result())
    provider = context_provider or (lambda work_id: {"work_id": work_id, "authorized": True})
    builder = request_builder or (lambda request: dict(request))
    return W13CoreExecutionClientV1(bridge=bridge, work_context_provider=provider, request_builder=builder), bridge


class ConstructionTests(unittest.TestCase):
    def test_rejects_bridge_without_invoke(self):
        with self.assertRaises(ToolCallError):
            W13CoreExecutionClientV1(bridge=object(), work_context_provider=lambda w: {}, request_builder=lambda r: r)

    def test_rejects_non_callable_providers(self):
        bridge = FakeBridge(make_result())
        with self.assertRaises(ToolCallError):
            W13CoreExecutionClientV1(bridge=bridge, work_context_provider=None, request_builder=lambda r: r)
        with self.assertRaises(ToolCallError):
            W13CoreExecutionClientV1(bridge=bridge, work_context_provider=lambda w: {}, request_builder=None)

    def test_satisfies_gateway_protocol(self):
        client, _ = build_client()
        for method in _REQUIRED_METHODS:
            self.assertTrue(callable(getattr(client, method, None)), method)
        ExecutionGateway(client)


class SubmitTests(unittest.TestCase):
    def test_submit_returns_run_id_and_records_run(self):
        client, bridge = build_client()
        outcome = client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        self.assertEqual(outcome["run_id"], "exec-1")
        self.assertEqual(outcome["status"], "PASS")
        self.assertEqual(bridge.calls[0]["context"], {"work_id": "W28", "authorized": True})
        self.assertEqual(client.get_status("exec-1")["status"], "PASS")

    def test_submit_rejects_missing_work_id(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.submit({"operation": "RUN_SCRIPT"})

    def test_submit_blocked_result_without_execution_id_fails_closed(self):
        blocked = make_result(execution_id=None, status="BLOCKED", blocker="execution_host_http_403")
        client, _ = build_client(result=blocked)
        with self.assertRaises(ToolCallError) as ctx:
            client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        self.assertIn("execution_host_http_403", ctx.exception.message)

    def test_submit_maps_unknown_status_to_blocked(self):
        odd = make_result(status="WEIRD")
        client, _ = build_client(result=odd)
        outcome = client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        self.assertEqual(outcome["status"], "BLOCKED")


class RegistryTests(unittest.TestCase):
    def test_unknown_run_status_is_blocked(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.get_status("nope")

    def test_unknown_run_result_is_blocked(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.get_result("nope")

    def test_get_result_returns_bound_output_references(self):
        client, _ = build_client()
        client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        result = client.get_result("exec-1")
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["stdout_ref"], "stdout://1")
        self.assertEqual(result["evidence_ref"], "ev-1")

    def test_cancel_is_refused_at_synchronous_boundary(self):
        client, _ = build_client()
        client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        with self.assertRaises(ToolCallError) as ctx:
            client.cancel("exec-1")
        self.assertIn("cancel_not_supported_synchronous_boundary", ctx.exception.message)


class ArtifactEvidenceTests(unittest.TestCase):
    def test_collect_artifact_requires_manifest_entry(self):
        client, _ = build_client()
        client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        self.assertEqual(client.collect_artifact("exec-1", "out.log")["artifact_path"], "out.log")
        with self.assertRaises(ToolCallError):
            client.collect_artifact("exec-1", "not-in-manifest.log")

    def test_collect_artifact_unknown_run_is_blocked(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.collect_artifact("nope", "out.log")

    def test_generate_evidence_binds_run_evidence_reference(self):
        client, _ = build_client()
        client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        record = client.generate_evidence("exec-1", "unit_test_run", ["commit:abc"])
        self.assertEqual(record["evidence_ref"], "ev-1")
        self.assertEqual(record["refs"], ["commit:abc"])

    def test_generate_evidence_without_bound_evidence_is_blocked(self):
        client, _ = build_client(result=make_result(evidence_ref=None))
        client.submit({"operation": "RUN_SCRIPT", "work_id": "W28"})
        with self.assertRaises(ToolCallError):
            client.generate_evidence("exec-1", "unit_test_run", [])


class HandoffTests(unittest.TestCase):
    def test_valid_handoff_is_returned(self):
        client, _ = build_client()
        record = client.create_handoff("W28", "PASS", ["ev-1"], "run E2E next")
        self.assertEqual(record["status"], "PASS")
        self.assertEqual(record["evidence_refs"], ["ev-1"])

    def test_invalid_handoff_status_rejected(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.create_handoff("W28", "RUNNING", ["ev-1"], "")

    def test_empty_evidence_refs_rejected(self):
        client, _ = build_client()
        with self.assertRaises(ToolCallError):
            client.create_handoff("W28", "PASS", [], "")
        with self.assertRaises(ToolCallError):
            client.create_handoff("W28", "PASS", ["  "], "")


if __name__ == "__main__":
    unittest.main()
