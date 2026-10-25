"""Offline tests: W28→W13 envelope mapping and W27 transport arity bridge.

Includes negative cases Xu requested: wrong context type, invalid requests,
extra fields outside contract.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1] / "04_CODE"
sys.path.insert(0, str(CODE))

from mcp8020_w13_execute_envelope_v1 import (
    EnvelopeError,
    assert_not_legacy_v54_shape,
    build_w13_execute_envelope,
)
from mcp8020_w27_http_transport_bridge_v1 import (
    TransportBridgeError,
    W27HttpTransportBridge,
)

_SHA = "ab" * 32


def _valid_req(**over):
    base = {
        "work_id": "28",
        "entry_path": "tests/test_x.py",
        "operation": "RUN_TESTS",
        "expected_source_sha256": _SHA,
        "timeout_seconds": 60,
    }
    base.update(over)
    return base


class EnvelopeCompatibilityGateTests(unittest.TestCase):
    def test_current_w13_schema_fails_closed_instead_of_returning_incompatible_envelope(self):
        wc = {
            "work_id": "28",
            "work_name": "MCP-8020-TOOLING-PLATFORM",
            "workspace_root": "/trusted/workspace",
            "execution_workspace": "/trusted/workspace/28",
            "evidence_root": "/trusted/evidence",
            "authorized": True,
        }
        with self.assertRaisesRegex(
            EnvelopeError, "W13_CANONICAL_CONTRACT_NOT_COMPATIBLE"
        ):
            build_w13_execute_envelope(work_context=wc, run_request=_valid_req())


class EnvelopeNegativeContextTests(unittest.TestCase):
    def test_work_context_wrong_type_none(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(work_context=None, run_request=_valid_req())

    def test_work_context_wrong_type_list(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(work_context=["28"], run_request=_valid_req())

    def test_work_context_missing_work_id(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(
                work_context={"principal": "x"}, run_request=_valid_req()
            )

    def test_work_context_empty_work_id(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(
                work_context={"work_id": "  "}, run_request=_valid_req()
            )

    def test_work_id_mismatch(self):
        with self.assertRaisesRegex(EnvelopeError, "W13_WORK_CONTEXT_WORK_ID_MISMATCH"):
            build_w13_execute_envelope(
                work_context={
                    "work_id": "28", "work_name": "W28",
                    "workspace_root": "/trusted/workspace",
                    "execution_workspace": "/trusted/workspace/28",
                    "evidence_root": "/trusted/evidence", "authorized": True,
                },
                run_request=_valid_req(work_id="99"),
            )


class EnvelopeNegativeRequestTests(unittest.TestCase):
    def test_run_request_wrong_type(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(
                work_context={"work_id": "28"}, run_request="not-a-dict"
            )

    def test_missing_sha(self):
        req = _valid_req()
        del req["expected_source_sha256"]
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(work_context={"work_id": "28"}, run_request=req)

    def test_missing_entry_path(self):
        req = _valid_req()
        del req["entry_path"]
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(work_context={"work_id": "28"}, run_request=req)

    def test_extra_field_outside_contract(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(
                work_context={"work_id": "28"},
                run_request=_valid_req(shell=True, argv=["x"]),
            )

    def test_legacy_script_field_rejected_by_contract(self):
        with self.assertRaises(EnvelopeError):
            build_w13_execute_envelope(
                work_context={"work_id": "28"},
                run_request=_valid_req(script="print(1)"),
            )

    def test_assert_legacy_script_shape(self):
        with self.assertRaises(EnvelopeError):
            assert_not_legacy_v54_shape({"work_id": "28", "script": "print(1)"})
        with self.assertRaises(EnvelopeError):
            assert_not_legacy_v54_shape({"operation": "RUN_COMMAND", "entry": "curl"})
        with self.assertRaises(EnvelopeError):
            assert_not_legacy_v54_shape({"entry": "main.py"})  # no entry_path


class TransportBridgeTests(unittest.TestCase):
    def test_splits_payload_into_two_http_args(self):
        seen = {}

        class FakeHttp:
            def execute(self, work_context, execution_request):
                seen["wc"] = work_context
                seen["er"] = execution_request
                return {"status": "BLOCKED", "reason": "offline-test"}

        bridge = W27HttpTransportBridge(FakeHttp())
        out = bridge.execute({
            "work_context": {"work_id": "28"},
            "execution_request": {"entry_path": "a.py", "operation": "RUN_SCRIPT"},
        })
        self.assertEqual(seen["wc"]["work_id"], "28")
        self.assertEqual(out["status"], "BLOCKED")

    def test_refuses_flat_runtime_adapter_payload(self):
        class FakeHttp:
            def execute(self, work_context, execution_request):
                raise AssertionError("must not be called")

        bridge = W27HttpTransportBridge(FakeHttp())
        with self.assertRaises(TransportBridgeError):
            bridge.execute({"task_id": "t1", "argv": ["python", "x.py"], "cwd": "."})

    def test_refuses_non_dict_payload(self):
        class FakeHttp:
            def execute(self, work_context, execution_request):
                raise AssertionError("must not be called")

        with self.assertRaises(TransportBridgeError):
            W27HttpTransportBridge(FakeHttp()).execute(["x"])

    def test_refuses_non_dict_parts(self):
        class FakeHttp:
            def execute(self, work_context, execution_request):
                raise AssertionError("must not be called")

        bridge = W27HttpTransportBridge(FakeHttp())
        with self.assertRaises(TransportBridgeError):
            bridge.execute({
                "work_context": "28",
                "execution_request": {"entry_path": "a.py"},
            })


if __name__ == "__main__":
    unittest.main()
