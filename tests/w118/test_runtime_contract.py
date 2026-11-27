import copy
import json
import unittest
from pathlib import Path

from scripts.w118.runtime_contract import (
    REQUIRED_COMPONENTS,
    validate_runtime_contract,
)


def valid_bundle():
    dependencies = {}
    for component, operations in REQUIRED_COMPONENTS.items():
        dependencies[component] = {
            "owner": f"owner:{component}",
            "contract_id": f"contract:{component}",
            "contract_version": "1.0",
            "source_revision": "revision-2026-11-25",
            "contract_ref": f"work-owner://{component}/approved-contract",
            "approved": True,
            "base_url": "https://service.example.test",
            "auth": {"mode": "BEARER_REF", "credential_ref": f"secret-manager://{component}"},
            "operations": {
                name: {
                    "method": "POST" if name not in {"read_task", "read_evidence"} else "GET",
                    "path": f"/owner-defined/{name}",
                    "request_schema_ref": f"schema://{component}/{name}/request",
                    "response_schema_ref": f"schema://{component}/{name}/response",
                    "side_effect": "READ_ONLY" if name in {"read_task", "read_evidence"} else "MUTATION",
                }
                for name in operations
            },
            "evidence": {
                "correlation_id_field": "owner_defined.correlation_id",
                "receipt_id_field": "owner_defined.receipt_id",
            },
        }
    return {"schema_version": "1.0", "work_id": "118", "dependencies": dependencies}


class RuntimeContractReadinessTests(unittest.TestCase):
    def test_complete_owner_approved_bundle_is_ready_for_preflight_only(self):
        report = validate_runtime_contract(valid_bundle())
        self.assertEqual(report["status"], "READY_FOR_RUNTIME_PREFLIGHT")
        self.assertFalse(report["runtime_execution_performed"])
        self.assertFalse(report["runtime_pass"])
        self.assertFalse(report["authority_granted"])

    def test_missing_dependency_fails_closed(self):
        bundle = valid_bundle()
        del bundle["dependencies"]["w14_execution_host"]
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("w14_execution_host", report["missing_components"])

    def test_unapproved_proposal_is_blocked(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["approved"] = False
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("approved must be true" in item for item in report["errors"]))

    def test_missing_required_operation_is_blocked(self):
        bundle = valid_bundle()
        del bundle["dependencies"]["w102_assignment_ack"]["operations"]["acknowledge_assignment"]
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")

    def test_unknown_operation_is_rejected_to_match_published_schema(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["operations"]["debug_shell"] = {
            "method": "POST",
            "path": "/owner-defined/debug-shell",
            "request_schema_ref": "schema://debug/request",
            "response_schema_ref": "schema://debug/response",
            "side_effect": "MUTATION",
        }
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("not part of the canonical W118 contract" in item for item in report["errors"]))

    def test_lowercase_http_method_is_rejected_to_match_schema(self):
        bundle = valid_bundle()
        bundle["dependencies"]["core_task_authority"]["operations"]["read_task"]["method"] = "get"
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")

    def test_root_only_operation_path_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w70_evidence_register"]["operations"]["read_evidence"]["path"] = "/"
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")

    def test_unknown_top_level_field_is_rejected(self):
        bundle = valid_bundle()
        bundle["runtime_pass"] = True
        self.assertEqual(validate_runtime_contract(bundle)["status"], "BLOCKED")

    def test_unknown_component_field_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["debug_mode"] = True
        self.assertEqual(validate_runtime_contract(bundle)["status"], "BLOCKED")

    def test_unknown_operation_field_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["operations"]["execute_work"]["shell"] = True
        self.assertEqual(validate_runtime_contract(bundle)["status"], "BLOCKED")

    def test_malformed_url_fails_closed_without_exception(self):
        bundle = valid_bundle()
        bundle["dependencies"]["core_task_authority"]["base_url"] = "https://[invalid"
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("syntactically valid" in item for item in report["errors"]))

    def test_external_plain_http_endpoint_is_blocked(self):
        bundle = valid_bundle()
        bundle["dependencies"]["core_task_authority"]["base_url"] = "http://core.example.test"
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("HTTPS outside loopback" in item for item in report["errors"]))

    def test_loopback_http_is_allowed_for_local_development_only(self):
        bundle = valid_bundle()
        bundle["dependencies"]["core_task_authority"]["base_url"] = "http://127.0.0.1:8000"
        report = validate_runtime_contract(bundle)
        self.assertEqual(report["status"], "READY_FOR_RUNTIME_PREFLIGHT")

    def test_raw_credential_field_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["auth"]["token"] = "do-not-store"
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("raw credential field is forbidden" in item for item in report["errors"]))

    def test_missing_secret_manager_reference_is_blocked(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w33_evidence_ingress"]["auth"].pop("credential_ref")
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("credential_ref" in item for item in report["errors"]))

    def test_path_traversal_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w14_execution_host"]["operations"]["execute_work"]["path"] = "/api/../admin"
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("without traversal" in item for item in report["errors"]))

    def test_absolute_operation_url_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w70_evidence_register"]["operations"]["read_evidence"]["path"] = "https://evil.test/read"
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("service-relative path" in item for item in report["errors"]))

    def test_missing_evidence_receipt_binding_is_blocked(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w33_evidence_ingress"]["evidence"].pop("receipt_id_field")
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("receipt_id_field" in item for item in report["errors"]))

    def test_unknown_component_is_rejected(self):
        bundle = valid_bundle()
        bundle["dependencies"]["local_dispatcher"] = copy.deepcopy(bundle["dependencies"]["w14_execution_host"])
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("not an approved" in item for item in report["errors"]))

    def test_non_object_bundle_fails_closed(self):
        report = validate_runtime_contract(["not", "an", "object"])
        self.assertEqual(report["status"], "BLOCKED")

    def test_wrong_work_id_is_rejected(self):
        bundle = valid_bundle()
        bundle["work_id"] = "999"
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("work_id must be '118'" in item for item in report["errors"]))

    def test_missing_schema_reference_is_blocked(self):
        bundle = valid_bundle()
        bundle["dependencies"]["w70_evidence_register"]["operations"]["register_evidence"].pop("response_schema_ref")
        report = validate_runtime_contract(bundle)
        self.assertTrue(any("response_schema_ref" in item for item in report["errors"]))


    def test_published_json_schema_declares_all_canonical_dependencies(self):
        schema_path = Path(__file__).resolve().parents[2] / "schemas" / "w118" / "runtime-contract.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required = schema["properties"]["dependencies"]["required"]
        self.assertEqual(set(required), set(REQUIRED_COMPONENTS))
        for component in REQUIRED_COMPONENTS:
            self.assertIn(component, schema["properties"]["dependencies"]["properties"])

    def test_owner_intake_template_is_explicitly_unapproved(self):
        template_path = (
            Path(__file__).resolve().parents[2]
            / "work" / "118" / "HQTT-GITHUB-WORKFLOW-AUTOMATION"
            / "05_BUILD" / "runtime-contract-template.json"
        )
        template = json.loads(template_path.read_text(encoding="utf-8"))
        report = validate_runtime_contract(template)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(all(spec["approved"] is False for spec in template["dependencies"].values()))


if __name__ == "__main__":
    unittest.main()
