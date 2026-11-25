import copy
import json
import unittest
from pathlib import Path

from scripts.w118.evidence_chain import STAGES, verify_evidence_chain


def valid_bundle():
    source_revision = "a" * 40
    correlation_id = "corr-w118-001"
    task_id = "W118-TASK-019"
    receipts = []
    previous_id = None
    for index, (stage, outcome) in enumerate(STAGES):
        receipt_id = f"receipt-{index + 1}"
        digest = "b" * 64 if index >= 2 else chr(99 + index) * 64
        receipts.append({
            "stage": stage,
            "receipt_id": receipt_id,
            "previous_receipt_id": previous_id,
            "work_id": "118",
            "task_id": task_id,
            "correlation_id": correlation_id,
            "source_revision": source_revision,
            "issuer_principal": f"principal:{stage}",
            "authority_ref": f"authority:{stage}",
            "attestation_ref": f"attestation:{stage}",
            "outcome": outcome,
            "artifact_sha256": digest,
            "observed_at": f"2026-11-25T10:0{index}:00+00:00",
        })
        previous_id = receipt_id
    return {
        "schema_version": "1.0",
        "work_id": "118",
        "task_id": task_id,
        "correlation_id": correlation_id,
        "source_revision": source_revision,
        "receipts": receipts,
    }


class EvidenceChainTests(unittest.TestCase):
    def test_complete_chain_is_structural_only_not_runtime_pass(self):
        report = verify_evidence_chain(valid_bundle())
        self.assertEqual(report["status"], "STRUCTURALLY_COMPLETE_UNAUTHENTICATED")
        self.assertFalse(report["runtime_e2e_pass"])
        self.assertFalse(report["authenticity_verified"])
        self.assertFalse(report["acceptance_granted"])

    def test_missing_stage_is_blocked(self):
        bundle = valid_bundle()
        bundle["receipts"].pop()
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_stage_order_is_enforced(self):
        bundle = valid_bundle()
        bundle["receipts"][1], bundle["receipts"][2] = bundle["receipts"][2], bundle["receipts"][1]
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_correlation_id_must_be_identical_across_stages(self):
        bundle = valid_bundle()
        bundle["receipts"][2]["correlation_id"] = "different-correlation"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_work_and_task_binding_must_match(self):
        bundle = valid_bundle()
        bundle["receipts"][1]["task_id"] = "W118-TASK-020"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_source_revision_must_match_full_sha(self):
        bundle = valid_bundle()
        bundle["source_revision"] = "short-sha"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_receipt_chain_links_immediately_previous_receipt(self):
        bundle = valid_bundle()
        bundle["receipts"][3]["previous_receipt_id"] = "receipt-1"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_duplicate_receipt_id_is_rejected(self):
        bundle = valid_bundle()
        bundle["receipts"][2]["receipt_id"] = "receipt-2"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_w33_digest_must_match_w14_execution_artifact(self):
        bundle = valid_bundle()
        bundle["receipts"][3]["artifact_sha256"] = "d" * 64
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_w70_readback_digest_must_match_w33_ingested_artifact(self):
        bundle = valid_bundle()
        bundle["receipts"][4]["artifact_sha256"] = "e" * 64
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_timestamp_requires_timezone(self):
        bundle = valid_bundle()
        bundle["receipts"][0]["observed_at"] = "2026-11-25T10:00:00"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_timestamps_must_be_monotonic(self):
        bundle = valid_bundle()
        bundle["receipts"][4]["observed_at"] = "2026-11-24T10:00:00+00:00"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_attestation_reference_is_required_but_not_authenticated(self):
        bundle = valid_bundle()
        bundle["receipts"][0].pop("attestation_ref")
        report = verify_evidence_chain(bundle)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertFalse(report["authenticity_verified"])

    def test_receipt_outcome_must_be_stage_specific(self):
        bundle = valid_bundle()
        bundle["receipts"][1]["outcome"] = "PASS"
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")

    def test_non_object_bundle_fails_closed(self):
        self.assertEqual(verify_evidence_chain(None)["status"], "BLOCKED")

    def test_duplicate_receipt_order_and_extra_receipt_are_rejected(self):
        bundle = valid_bundle()
        bundle["receipts"].append(copy.deepcopy(bundle["receipts"][-1]))
        self.assertEqual(verify_evidence_chain(bundle)["status"], "BLOCKED")


    def test_published_schema_declares_all_five_stages_in_order(self):
        schema_path = Path(__file__).resolve().parents[2] / "schemas" / "w118" / "evidence-chain.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        prefix = schema["properties"]["receipts"]["prefixItems"]
        self.assertEqual(
            [item["$ref"].rsplit("/", 1)[-1] for item in prefix],
            [stage for stage, _ in STAGES],
        )

    def test_digest_comparison_is_hex_case_insensitive(self):
        bundle = valid_bundle()
        bundle["receipts"][2]["artifact_sha256"] = "B" * 64
        bundle["receipts"][3]["artifact_sha256"] = "b" * 64
        bundle["receipts"][4]["artifact_sha256"] = "B" * 64
        self.assertEqual(
            verify_evidence_chain(bundle)["status"],
            "STRUCTURALLY_COMPLETE_UNAUTHENTICATED",
        )


if __name__ == "__main__":
    unittest.main()
