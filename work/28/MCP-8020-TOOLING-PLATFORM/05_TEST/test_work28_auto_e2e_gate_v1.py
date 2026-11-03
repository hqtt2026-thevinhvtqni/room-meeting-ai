from __future__ import annotations

import unittest

from work28_auto_e2e_gate_v1 import evaluate_e2e_evidence


def valid_record():
    return {
        "schema_version": 1,
        "source_commit": "a" * 40,
        "mcp_build_identity": "mcp8030-build-1",
        "mcp_process_identity": "pid-ref-1",
        "mcp_tools_list_sha256": "b" * 64,
        "core_build_identity": "core-build-1",
        "principal_ref": "service:mcp8030",
        "work_id": "W28",
        "capability": "execution.run_tests",
        "authorization_decision": "ALLOW",
        "snapshot_ref": "snapshot://run-1",
        "snapshot_immutable": True,
        "source_sha256": "c" * 64,
        "runtime_identity": "runtime-w13-build-1",
        "approved_runtime_identity": "runtime-w13-build-1",
        "isolation_profile": "approved-profile-v1",
        "isolation_attested": True,
        "execution_host_identity": "execution-host-8031-build-1",
        "operation": "RUN_TESTS",
        "request_id": "req-1",
        "run_id": "run-1",
        "exit_code": 0,
        "process_tree_cleanup_verified": True,
        "test_summary": {"total": 12, "failures": 0, "errors": 0},
        "evidence_ref": "protected-evidence://run-1",
        "evidence_sha256": "d" * 64,
        "readback_ref": "protected-evidence://run-1",
        "readback_sha256": "d" * 64,
        # Deliberately ignored: status text cannot grant PASS.
        "reported_status": "PASS",
    }


class Work28AutoE2EGateTests(unittest.TestCase):
    def test_complete_evidence_passes(self):
        self.assertEqual(evaluate_e2e_evidence(valid_record())["status"], "PASS")

    def test_missing_live_identity_blocks(self):
        record = valid_record()
        del record["runtime_identity"]
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "BLOCKED")

    def test_authorization_denial_never_passes(self):
        record = valid_record()
        record["authorization_decision"] = "DENY"
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "DENIED")

    def test_unattested_isolation_blocks(self):
        record = valid_record()
        record["isolation_attested"] = False
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "BLOCKED")

    def test_zero_tests_fails_even_when_reported_pass(self):
        record = valid_record()
        record["test_summary"]["total"] = 0
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "FAIL")

    def test_nonzero_exit_fails(self):
        record = valid_record()
        record["exit_code"] = 1
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "FAIL")

    def test_checksum_mismatch_fails(self):
        record = valid_record()
        record["readback_sha256"] = "e" * 64
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "FAIL")

    def test_runtime_identity_mismatch_fails(self):
        record = valid_record()
        record["runtime_identity"] = "unapproved-runtime"
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "FAIL")

    def test_secret_material_is_rejected(self):
        record = valid_record()
        record["grant_token"] = "must-not-be-recorded"
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "FAIL")

    def test_missing_cleanup_blocks(self):
        record = valid_record()
        record["process_tree_cleanup_verified"] = False
        self.assertEqual(evaluate_e2e_evidence(record)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
