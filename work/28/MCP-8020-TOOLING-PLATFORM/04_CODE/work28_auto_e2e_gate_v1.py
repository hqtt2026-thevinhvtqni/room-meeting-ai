"""Fail-closed acceptance gate for Work 28 automatic E2E evidence.

This module evaluates evidence produced by a trusted deployed runner. It does
not authorize, dispatch, or execute work. Caller-supplied status text is never
used to calculate PASS.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_WORK = re.compile(r"^W[0-9]+$")
_SECRET_KEYS = {"credential", "grant_token", "token", "authorization_header", "secret"}


def evaluate_e2e_evidence(record: Any) -> dict[str, Any]:
    """Return PASS only when every Auto-E2E stage has verifiable evidence."""
    if not isinstance(record, dict):
        return {"status": "BLOCKED", "blockers": ["evidence_record_must_be_object"], "failed_checks": []}

    leaked = sorted(_SECRET_KEYS.intersection(record))
    if leaked:
        return {"status": "FAIL", "blockers": [], "failed_checks": ["secret_material_must_not_be_in_evidence:" + ",".join(leaked)]}

    required_strings = (
        "source_commit", "mcp_build_identity", "mcp_process_identity",
        "mcp_tools_list_sha256", "core_build_identity", "principal_ref",
        "work_id", "capability", "snapshot_ref", "source_sha256",
        "runtime_identity", "approved_runtime_identity", "isolation_profile",
        "execution_host_identity", "request_id", "run_id", "evidence_ref",
        "evidence_sha256", "readback_ref", "readback_sha256",
    )
    missing = [key for key in required_strings if not isinstance(record.get(key), str) or not record[key].strip()]
    if record.get("schema_version") != 1:
        missing.append("schema_version=1")
    if missing:
        return {"status": "BLOCKED", "blockers": ["missing_or_invalid:" + ",".join(missing)], "failed_checks": []}

    failed: list[str] = []
    blockers: list[str] = []
    if not _COMMIT.fullmatch(record["source_commit"]):
        failed.append("source_commit_invalid")
    for key in ("mcp_tools_list_sha256", "source_sha256", "evidence_sha256", "readback_sha256"):
        if not _SHA256.fullmatch(record[key]):
            failed.append(key + "_invalid")
    if not _WORK.fullmatch(record["work_id"]):
        failed.append("core_work_id_not_canonical")
    if record.get("authorization_decision") != "ALLOW":
        return {"status": "DENIED", "blockers": ["core_authorization_not_allow"], "failed_checks": failed}
    if record.get("snapshot_immutable") is not True:
        blockers.append("immutable_snapshot_not_attested")
    if record.get("isolation_attested") is not True:
        blockers.append("runtime_os_isolation_not_attested")
    if record["runtime_identity"] != record["approved_runtime_identity"]:
        failed.append("runtime_identity_mismatch")
    if record["evidence_sha256"] != record["readback_sha256"]:
        failed.append("evidence_readback_checksum_mismatch")
    if record["evidence_ref"] != record["readback_ref"]:
        failed.append("evidence_readback_reference_mismatch")
    if isinstance(record.get("exit_code"), bool) or not isinstance(record.get("exit_code"), int):
        blockers.append("actual_integer_exit_code_missing")
    elif record["exit_code"] != 0:
        failed.append("nonzero_exit_code")
    if record.get("process_tree_cleanup_verified") is not True:
        blockers.append("process_tree_cleanup_not_verified")

    operation = record.get("operation")
    if operation not in ("RUN_TESTS", "RUN_SCRIPT"):
        failed.append("operation_invalid")
    elif operation == "RUN_TESTS":
        summary = record.get("test_summary")
        if not isinstance(summary, dict):
            blockers.append("test_summary_missing")
        else:
            total, failures, errors = summary.get("total"), summary.get("failures"), summary.get("errors")
            if isinstance(total, bool) or not isinstance(total, int) or total < 1:
                failed.append("zero_or_invalid_tests_run")
            if isinstance(failures, bool) or not isinstance(failures, int) or failures != 0:
                failed.append("test_failures_nonzero_or_invalid")
            if isinstance(errors, bool) or not isinstance(errors, int) or errors != 0:
                failed.append("test_errors_nonzero_or_invalid")

    if failed:
        status = "FAIL"
    elif blockers:
        status = "BLOCKED"
    else:
        status = "PASS"
    return {"status": status, "blockers": blockers, "failed_checks": failed,
            "source_commit": record["source_commit"], "work_id": record["work_id"],
            "request_id": record["request_id"], "run_id": record["run_id"],
            "evidence_ref": record["evidence_ref"], "evidence_sha256": record["evidence_sha256"]}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(json.dumps({"status": "BLOCKED", "blockers": ["usage: work28_auto_e2e_gate_v1.py evidence.json"]}))
        return 2
    try:
        record = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print(json.dumps({"status": "BLOCKED", "blockers": ["evidence_file_unreadable_or_invalid_json"]}))
        return 2
    result = evaluate_e2e_evidence(record)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else (1 if result["status"] in ("FAIL", "DENIED") else 2)


if __name__ == "__main__":
    raise SystemExit(main())
