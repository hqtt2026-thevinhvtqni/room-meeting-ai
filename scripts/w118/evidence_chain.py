"""Structural verifier for a normalized five-stage W118 runtime evidence chain.

The verifier checks receipt linkage, correlation continuity, source binding,
chronology and artifact digest consistency. It does NOT authenticate issuers,
verify signatures, contact services, or declare Runtime E2E PASS.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


STAGES = (
    ("core_task_snapshot", "TASK_READ"),
    ("w102_assignment_ack", "ACKNOWLEDGED"),
    ("w14_execution", "EXECUTED"),
    ("w33_ingestion", "INGESTED"),
    ("w70_readback", "READBACK_VERIFIED"),
)
SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
TASK_RE = re.compile(r"^W118-TASK-[0-9]{3,6}$")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_time(value: Any) -> datetime | None:
    if not _text(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def verify_evidence_chain(bundle: Any) -> dict[str, Any]:
    """Return structural chain status; authenticity is deliberately unverified."""
    errors: list[str] = []
    if not isinstance(bundle, Mapping):
        return _report(["bundle must be a JSON object"])

    if bundle.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if bundle.get("work_id") != "118":
        errors.append("work_id must be '118'")
    if not _text(bundle.get("task_id")) or TASK_RE.fullmatch(bundle.get("task_id", "")) is None:
        errors.append("task_id must be a W118-TASK-### or W118-TASK-###### identifier")
    if not _text(bundle.get("correlation_id")):
        errors.append("correlation_id must be non-empty")
    source_revision = bundle.get("source_revision")
    if not isinstance(source_revision, str) or SHA40_RE.fullmatch(source_revision) is None:
        errors.append("source_revision must be a full 40-character Git SHA")

    receipts = bundle.get("receipts")
    if not isinstance(receipts, list):
        errors.append("receipts must be an ordered array")
        return _report(errors)
    if len(receipts) != len(STAGES):
        errors.append(f"exactly {len(STAGES)} ordered stage receipts are required")
    if len(receipts) > len(STAGES):
        return _report(errors)

    seen_ids: set[str] = set()
    previous_id: str | None = None
    previous_time: datetime | None = None
    stage_receipts: dict[str, Mapping[str, Any]] = {}

    for index, (stage_name, expected_outcome) in enumerate(STAGES):
        if index >= len(receipts):
            errors.append(f"missing receipt for stage {stage_name}")
            continue
        receipt = receipts[index]
        path = f"receipts[{index}]"
        if not isinstance(receipt, Mapping):
            errors.append(f"{path} must be an object")
            continue

        if receipt.get("stage") != stage_name:
            errors.append(f"{path}.stage must be {stage_name}")
        receipt_id = receipt.get("receipt_id")
        if not _text(receipt_id):
            errors.append(f"{path}.receipt_id must be non-empty")
        elif receipt_id in seen_ids:
            errors.append(f"{path}.receipt_id must be unique")
        else:
            seen_ids.add(receipt_id)

        for field, expected in (
            ("work_id", "118"),
            ("task_id", bundle.get("task_id")),
            ("correlation_id", bundle.get("correlation_id")),
            ("source_revision", source_revision),
        ):
            if receipt.get(field) != expected:
                errors.append(f"{path}.{field} does not match the evidence bundle")

        for field in ("issuer_principal", "authority_ref", "attestation_ref"):
            if not _text(receipt.get(field)):
                errors.append(f"{path}.{field} must identify its asserted issuer/authority evidence")

        if receipt.get("outcome") != expected_outcome:
            errors.append(f"{path}.outcome must be {expected_outcome}")

        artifact_digest = receipt.get("artifact_sha256")
        if not isinstance(artifact_digest, str) or SHA256_RE.fullmatch(artifact_digest) is None:
            errors.append(f"{path}.artifact_sha256 must be a full SHA-256 digest")

        expected_previous = previous_id
        if receipt.get("previous_receipt_id") != expected_previous:
            errors.append(f"{path}.previous_receipt_id does not link to the immediately prior stage")

        observed_at = _parse_time(receipt.get("observed_at"))
        if observed_at is None:
            errors.append(f"{path}.observed_at must be an ISO-8601 timestamp with timezone")
        elif previous_time is not None and observed_at < previous_time:
            errors.append(f"{path}.observed_at is earlier than the previous stage")
        if observed_at is not None:
            previous_time = observed_at

        if _text(receipt_id):
            previous_id = receipt_id
        stage_receipts[stage_name] = receipt

    execution = stage_receipts.get("w14_execution")
    ingestion = stage_receipts.get("w33_ingestion")
    readback = stage_receipts.get("w70_readback")
    if execution and ingestion and str(execution.get("artifact_sha256", "")).lower() != str(ingestion.get("artifact_sha256", "")).lower():
        errors.append("W33 ingestion artifact digest must match W14 execution artifact")
    if ingestion and readback and str(ingestion.get("artifact_sha256", "")).lower() != str(readback.get("artifact_sha256", "")).lower():
        errors.append("W70 read-back artifact digest must match W33 ingested artifact")

    return _report(errors)


def _report(errors: list[str]) -> dict[str, Any]:
    complete = not errors
    return {
        "work_id": "118",
        "check": "RUNTIME_EVIDENCE_CHAIN_STRUCTURE",
        "status": "STRUCTURALLY_COMPLETE_UNAUTHENTICATED" if complete else "BLOCKED",
        "runtime_e2e_pass": False,
        "authenticity_verified": False,
        "acceptance_granted": False,
        "errors": errors,
        "limitations": [
            "This verifies normalized receipt structure, linkage, correlation continuity, chronology and digest equality only.",
            "Issuer identity, authority references and attestation references are not cryptographically authenticated by this tool.",
            "No runtime service was contacted and no execution was performed.",
            "STRUCTURALLY_COMPLETE_UNAUTHENTICATED is not Runtime E2E PASS, Work acceptance or release.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="Path to normalized W118 evidence-chain JSON")
    args = parser.parse_args()
    try:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(_report([f"cannot read evidence bundle: {exc}"]), indent=2))
        return 2
    report = verify_evidence_chain(bundle)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "STRUCTURALLY_COMPLETE_UNAUTHENTICATED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
