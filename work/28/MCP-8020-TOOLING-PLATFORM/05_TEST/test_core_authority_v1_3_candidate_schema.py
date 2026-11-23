"""Candidate-only Draft 2020-12 schema guard tests for DOC-W28-078.

These tests validate schema structure and fail-closed wire shapes. They do not
prove Core/W52/W14 integration or authorize endpoint implementation.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


WORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    WORK_ROOT
    / "03_ARCHITECTURE"
    / "schemas"
    / "DOC-W28-078_V1_3_CANDIDATE.schema.json"
)


class CandidateSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.checker = FormatChecker()

    def validator(self, name: str) -> Draft202012Validator:
        return Draft202012Validator(
            {"$schema": self.schema["$schema"], "$ref": f"#/$defs/{name}", "$defs": self.schema["$defs"]},
            format_checker=self.checker,
        )

    def valid_grant_request(self) -> dict:
        return {
            "request_id": "f6b22c4d-11e8-4c10-99b1-4c8f50f8c7d1",
            "contract_version": "1.3.0",
            "sent_at": "2026-11-23T08:00:00Z",
            "work_id": "W28",
            "wp_id": "WP5",
            "task_id": "TASK-W28-001",
            "assignment_id": "ASG-W28-001",
            "operation": "pytest_run",
            "entry_path": "tests/test_work28_dispatch.py",
            "source_repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "source_branch": "work/28-mcp-tooling-platform",
            "source_commit": "a" * 40,
            "source_tree_sha256": "b" * 64,
            "environment_sha256": "c" * 64,
            "capability_scope": ["pytest.run"],
            "provider_id": "provider-readonly-test",
            "host_id": "W14-HOST",
            "idempotency_key": "idem-001",
            "correlation_id": "corr-001",
            "purpose": "pytest_run",
            "recipient_ack_event_id": "ACK-001",
            "recipient_ack_sequence": 3,
        }

    def test_schema_is_draft_2020_12_and_contains_required_envelopes(self) -> None:
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        for name in (
            "grantIssueRequest",
            "grantIssueResponse",
            "grantValidationRequest",
            "grantValidationResponse",
            "runStartRequest",
            "runCompleteRequest",
            "runAckResponse",
            "eventEnvelope",
            "errorResponse",
        ):
            self.assertIn(name, self.schema["$defs"])

    def test_grant_request_accepts_full_binding_and_recipient_ack_reference(self) -> None:
        errors = list(self.validator("grantIssueRequest").iter_errors(self.valid_grant_request()))
        self.assertEqual(errors, [])

    def test_grant_request_rejects_caller_work_context_and_authorized_flag(self) -> None:
        for field, value in (
            ("work_context", {"work_id": "W28", "authorized": True}),
            ("authorized", True),
            ("agent_principal_id", "caller-asserted-agent"),
            ("workspace_root", "C:/caller/path"),
            ("gate_state", "OPEN"),
        ):
            request = self.valid_grant_request()
            request[field] = value
            with self.subTest(field=field):
                self.assertTrue(list(self.validator("grantIssueRequest").iter_errors(request)))

    def test_grant_request_requires_authenticated_recipient_ack_reference(self) -> None:
        request = self.valid_grant_request()
        request.pop("recipient_ack_event_id")
        self.assertTrue(list(self.validator("grantIssueRequest").iter_errors(request)))

    def test_grant_request_rejects_malformed_source_digest(self) -> None:
        request = self.valid_grant_request()
        request["source_tree_sha256"] = "not-a-sha256"
        self.assertTrue(list(self.validator("grantIssueRequest").iter_errors(request)))

    def test_validation_request_rejects_caller_context(self) -> None:
        request = {
            "request_id": "f6b22c4d-11e8-4c10-99b1-4c8f50f8c7d1",
            "contract_version": "1.3.0",
            "sent_at": "2026-11-23T08:00:00Z",
            "grant_token": "opaque-secret",
            "host_instance_id": "W14-HOST-INSTANCE-1",
            "grant_id": "GRANT-001",
            "task_id": "TASK-W28-001",
            "assignment_id": "ASG-W28-001",
            "operation": "pytest_run",
            "entry_path": "tests/test_work28_dispatch.py",
            "source_tree_sha256": "b" * 64,
            "environment_sha256": "c" * 64,
            "execution_request_id": "EXEC-001",
            "correlation_id": "corr-001",
            "work_context": {"authorized": True},
        }
        self.assertTrue(list(self.validator("grantValidationRequest").iter_errors(request)))

    def test_completed_run_requires_containment_and_descendants_exited(self) -> None:
        request = {
            "request_id": "f6b22c4d-11e8-4c10-99b1-4c8f50f8c7d1",
            "contract_version": "1.3.0",
            "sent_at": "2026-11-23T08:00:00Z",
            "execution_request_id": "EXEC-001",
            "grant_id": "GRANT-001",
            "host_instance_id": "W14-HOST-INSTANCE-1",
            "task_id": "TASK-W28-001",
            "assignment_id": "ASG-W28-001",
            "correlation_id": "corr-001",
            "sequence": 4,
            "terminal_status": "RUN_COMPLETED",
            "exit_code": 0,
            "started_at": "2026-11-23T08:00:00Z",
            "finished_at": "2026-11-23T08:00:05Z",
            "output_refs": ["stdout://EXEC-001"],
            "evidence_refs": ["evidence://EXEC-001"],
            "containment": "FAIL",
            "cancellation": "NOT_REQUESTED",
            "descendants_exited": False,
        }
        self.assertTrue(list(self.validator("runCompleteRequest").iter_errors(request)))
        request["containment"] = "PASS"
        request["descendants_exited"] = True
        self.assertEqual(list(self.validator("runCompleteRequest").iter_errors(request)), [])


    def test_run_ack_requires_durable_ack_and_correlation(self) -> None:
        response = {
            "request_id": "f6b22c4d-11e8-4c10-99b1-4c8f50f8c7d1",
            "contract_version": "1.3.0",
            "server_time": "2026-11-23T08:00:00Z",
            "status": "ACKNOWLEDGED",
            "execution_request_id": "EXEC-001",
            "event_id": "EVENT-001",
            "sequence": 2,
            "durable_ack": True,
        }
        self.assertEqual(list(self.validator("runAckResponse").iter_errors(response)), [])
        response["durable_ack"] = False
        self.assertTrue(list(self.validator("runAckResponse").iter_errors(response)))

    def test_event_envelope_requires_correlated_ordered_identity(self) -> None:
        event = {
            "event_id": "EVENT-001",
            "request_id": "f6b22c4d-11e8-4c10-99b1-4c8f50f8c7d1",
            "execution_request_id": "EXEC-001",
            "grant_id": "GRANT-001",
            "work_id": "W28",
            "task_id": "TASK-W28-001",
            "assignment_id": "ASG-W28-001",
            "host_instance_id": "W14-HOST-INSTANCE-1",
            "correlation_id": "corr-001",
            "sequence": 2,
            "occurred_at": "2026-11-23T08:00:00Z",
            "event_type": "RUN_STARTED",
            "payload_sha256": "d" * 64,
        }
        self.assertEqual(list(self.validator("eventEnvelope").iter_errors(event)), [])
        event.pop("correlation_id")
        self.assertTrue(list(self.validator("eventEnvelope").iter_errors(event)))



if __name__ == "__main__":
    unittest.main()
