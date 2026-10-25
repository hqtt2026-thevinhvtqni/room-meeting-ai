"""Contract tests for the staged strict execution gateway adapter.

These tests are authored but have not been executed in this environment.
The fake client only proves request forwarding/short-circuit semantics.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_execution_contract_v1 import ExecutionContractError
from mcp8020_strict_execution_gateway_v1 import StrictExecutionGatewayV1


HASH = "a" * 64
VALID = {
    "work_id": "work28",
    "entry_path": "04_CODE/smoke.py",
    "operation": "RUN_SCRIPT",
    "expected_source_sha256": HASH,
    "timeout_seconds": 30,
}


class FakeClient:
    def __init__(self):
        self.calls = []

    def submit(self, request):
        self.calls.append(request)
        return {"status": "QUEUED", "request_id": "REQ-1"}


class StrictGatewayTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient()
        self.gateway = StrictExecutionGatewayV1(self.client)

    def test_valid_request_forwards_only_normalized_contract(self):
        request = dict(VALID)
        result = self.gateway.run(request)
        self.assertEqual(result["status"], "QUEUED")
        self.assertEqual(len(self.client.calls), 1)
        self.assertEqual(self.client.calls[0], VALID)
        self.assertEqual(set(self.client.calls[0]), set(VALID))

    def test_invalid_requests_are_rejected_before_client_call(self):
        bad_requests = [
            {**VALID, "script": "print('unsafe')"},
            {**VALID, "command": "curl"},
            {**VALID, "args": ["--dangerous"]},
            {**VALID, "principal": "admin"},
            {**VALID, "entry_path": "../outside.py"},
            {**VALID, "expected_source_sha256": "not-a-hash"},
            {**VALID, "operation": "RUN_COMMAND"},
            {**VALID, "timeout_seconds": True},
        ]
        for payload in bad_requests:
            with self.subTest(payload=payload):
                with self.assertRaises(ExecutionContractError):
                    self.gateway.run(payload)
        self.assertEqual(self.client.calls, [])

    def test_non_object_core_response_is_rejected(self):
        class BadResponseClient:
            def submit(self, request):
                return ["PASS"]

        gateway = StrictExecutionGatewayV1(BadResponseClient())
        with self.assertRaises(RuntimeError):
            gateway.run(dict(VALID))

    def test_client_without_submit_is_rejected_at_construction(self):
        with self.assertRaises(TypeError):
            StrictExecutionGatewayV1(object())

    def test_missing_required_field_is_rejected_before_submit(self):
        payload = dict(VALID)
        del payload["expected_source_sha256"]
        with self.assertRaises(ExecutionContractError):
            self.gateway.run(payload)
        self.assertEqual(self.client.calls, [])

    def test_verified_pass_requires_source_work_and_runtime_evidence_binding(self):
        result = {
            "status": "PASS",
            "exit_code": 0,
            "source_sha256": HASH,
            "request_id": "REQ-1",
            "run_id": "RUN-1",
            "work_id": "work28",
            "runtime_identity": "runtime-8031",
            "evidence_ref": "evidence://RUN-1",
        }
        self.assertTrue(self.gateway.verified_pass(result, HASH, "RUN_SCRIPT", "work28"))
        self.assertFalse(self.gateway.verified_pass(result, "b" * 64, "RUN_SCRIPT", "work28"))
        self.assertFalse(self.gateway.verified_pass(result, HASH, "RUN_SCRIPT", "other"))
        self.assertFalse(self.gateway.verified_pass({**result, "exit_code": True}, HASH, "RUN_SCRIPT", "work28"))

    def test_test_pass_requires_nonzero_test_count_and_zero_failures(self):
        result = {
            "status": "PASS",
            "exit_code": 0,
            "source_sha256": HASH,
            "request_id": "REQ-1",
            "run_id": "RUN-1",
            "work_id": "work28",
            "runtime_identity": "runtime-8031",
            "evidence_ref": "evidence://RUN-1",
            "test_summary": {"total": 2, "failed": 0, "errors": 0},
        }
        self.assertTrue(self.gateway.verified_pass(result, HASH, "RUN_TESTS", "work28"))
        self.assertFalse(self.gateway.verified_pass({**result, "test_summary": {"total": 0, "failed": 0, "errors": 0}}, HASH, "RUN_TESTS", "work28"))
        self.assertFalse(self.gateway.verified_pass({**result, "test_summary": {"total": 2, "failed": 1, "errors": 0}}, HASH, "RUN_TESTS", "work28"))


if __name__ == "__main__":
    unittest.main()
