"""Adversarial tests for the V8 acceptance manifest semantic validator."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "04_CODE"
sys.path.insert(0, str(CODE))

from acceptance_validator import (  # noqa: E402
    POLICY_PATH,
    SCHEMA_PATH,
    validate_file,
    verify_attestation,
)

VALIDATOR_PATH = CODE / "acceptance_validator.py"
SOURCE_COMMIT = "a" * 40
HMAC_KEY_TEXT = "0123456789abcdef" * 4
HMAC_KEY = bytes.fromhex(HMAC_KEY_TEXT)
FAILED = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def architecture() -> str:
    machine = platform.machine().casefold()
    return "arm64" if machine in {"arm64", "aarch64"} else "x86_64"


def base_environment() -> dict[str, str]:
    return {
        "COMPUTER_AGENT_VALIDATOR_SHA256": sha(VALIDATOR_PATH.read_bytes()),
        "COMPUTER_AGENT_VALIDATOR_SCHEMA_SHA256": sha(SCHEMA_PATH.read_bytes()),
        "COMPUTER_AGENT_VALIDATOR_POLICY_SHA256": sha(POLICY_PATH.read_bytes()),
        "COMPUTER_AGENT_VALIDATOR_HMAC_KEY": HMAC_KEY_TEXT,
        "COMPUTER_AGENT_VALIDATOR_KEY_ID": "W10-UNIT-TEST-ONLY",
        "COMPUTER_AGENT_VALIDATOR_RUNNER_ID": platform.node(),
        "COMPUTER_AGENT_SOURCE_COMMIT": SOURCE_COMMIT,
    }


def make_case():
    temp = tempfile.TemporaryDirectory(prefix="w10-v8-validator-")
    root = Path(temp.name)
    fixture = b'{"fixture":"W10 V8 test fixture"}\n'
    artifact = b"W10 V8 oracle evidence\n"
    (root / "fixture.json").write_bytes(fixture)
    (root / "oracle.log").write_bytes(artifact)
    now = datetime.now(timezone.utc)
    state = {
        "outcome": "REJECTED",
        "admission": "CLOSED",
        "gate": "CLOSED",
        "process_state": "EXITED",
        "containment_state": "EMPTY",
        "lease_state": "RELEASED",
        "owner_state": "CURRENT",
    }
    manifest = {
        "schema_version": "1.2.0",
        "work_id": "10",
        "profile": {
            "profile_id": "w10-v8-test-fixture",
            "os_family": "windows" if os.name == "nt" else "linux",
            "support_status": "SUPPORTED",
            "fixture_sha256": sha(fixture),
            "host_build": platform.version(),
            "architecture": architecture(),
            "fixture_manifest_ref": "fixture.json",
        },
        "test": {
            "test_id": "W10-V8-TEST-001",
            "category": "SAFETY",
            "review_revision": "V8",
        },
        "stimulus": {
            "injection_point": "negative-safety-guard",
            "description": "A forbidden operation is rejected by the trusted guard.",
            "parameters": {"operation": "forbidden"},
        },
        "expected": dict(state),
        "observed": {
            **state,
            "oracle_evidence": [{
                "oracle_id": "ORACLE-001",
                "source": "test_runner",
                "result": "The forbidden operation was rejected.",
                "artifact_ref": "oracle.log",
            }],
        },
        "artifacts": [
            {"name": "fixture.json", "status": "PRESENT", "sha256": sha(fixture)},
            {"name": "oracle.log", "status": "PRESENT", "sha256": sha(artifact)},
        ],
        "verdict": "PASS",
        "reviewer": "Co",
        "recorded_at": iso(now),
        "run_context": {
            "execution_id": str(uuid.uuid4()),
            "runner_id": platform.node(),
            "source_commit": SOURCE_COMMIT,
            "started_at": iso(now - timedelta(seconds=2)),
            "finished_at": iso(now - timedelta(seconds=1)),
        },
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return temp, root, path, manifest


def run_case(root, path, env=None):
    merged = base_environment()
    if env:
        merged.update(env)
    with patch.dict(os.environ, merged, clear=False):
        return validate_file(path, root, root / "attestation.json")


def check(name, fn):
    try:
        outcome = fn()
        if outcome is False:
            raise AssertionError("check returned False")
        print(f"  PASS  {name}")
    except Exception as exc:
        FAILED.append(f"{name}: {exc}")
        print(f"  FAIL  {name}: {exc}")


def main():
    print("Work 10 — V8 Acceptance Validator Tests")
    print("=" * 62)

    temp, root, path, manifest = make_case()
    try:
        result = run_case(root, path)
        check("valid negative test can have verdict PASS with observed outcome REJECTED",
              lambda: result["status"] == "PASS" and result["acceptance_eligible"] is True)
        attestation = result["attestation"]
        check("validator emits HMAC-signed attestation with pinned hashes",
              lambda: verify_attestation(
                  attestation, HMAC_KEY,
                  expected_input_sha256=result["input_sha256"],
                  expected_validator_sha256=sha(VALIDATOR_PATH.read_bytes()),
                  expected_schema_sha256=sha(SCHEMA_PATH.read_bytes()),
                  expected_policy_sha256=sha(POLICY_PATH.read_bytes()),
              ) and (root / "attestation.json").is_file())
        def validate_attestation_schema():
            import jsonschema
            attestation_schema = json.loads(
                (ROOT / "06_EVIDENCE" / "W10_P0_VALIDATOR_ATTESTATION_V1.schema.json").read_text(encoding="utf-8")
            )
            jsonschema.Draft202012Validator(attestation_schema).validate(attestation)
            return True
        check("emitted attestation conforms to its versioned schema", validate_attestation_schema)

        tampered_attestation = json.loads(json.dumps(attestation))
        tampered_attestation["result"]["acceptance_eligible"] = False
        check("attestation tampering invalidates HMAC",
              lambda: not verify_attestation(tampered_attestation, HMAC_KEY))

        # Caller-authored consistency flags are not accepted in V8.
        forged = dict(manifest)
        forged["consistency_check"] = {
            "outcome_match": True, "state_match": True,
            "validator_id": "caller", "validator_result": "PASS",
        }
        path.write_text(json.dumps(forged), encoding="utf-8")
        forged_result = run_case(root, path)
        check("caller-supplied consistency flags are schema-rejected",
              lambda: forged_result["status"] == "FAIL"
              and any("consistency_check" in error for error in forged_result["errors"]))

        mismatch = json.loads(json.dumps(manifest))
        mismatch["observed"]["owner_state"] = "FENCED"
        path.write_text(json.dumps(mismatch), encoding="utf-8")
        mismatch_result = run_case(root, path)
        check("PASS with expected/observed state mismatch is rejected",
              lambda: mismatch_result["status"] == "FAIL"
              and any("state tuple mismatch" in error for error in mismatch_result["errors"]))

        unknown = json.loads(json.dumps(manifest))
        unknown["observed"]["lease_state"] = "UNKNOWN"
        path.write_text(json.dumps(unknown), encoding="utf-8")
        unknown_result = run_case(root, path)
        check("PASS with UNKNOWN lease state is schema-rejected",
              lambda: unknown_result["status"] == "FAIL")

        disallowed = json.loads(json.dumps(manifest))
        disallowed["expected"]["outcome"] = "PASS"
        disallowed["observed"]["outcome"] = "PASS"
        path.write_text(json.dumps(disallowed), encoding="utf-8")
        disallowed_result = run_case(root, path)
        check("PASS with category-disallowed outcome is rejected",
              lambda: disallowed_result["status"] == "FAIL"
              and any("not allowed for PASS" in error for error in disallowed_result["errors"]))

        # Artifact bytes are re-hashed; caller-provided SHA values are not trusted.
        (root / "oracle.log").write_text("tampered", encoding="utf-8")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        artifact_result = run_case(root, path)
        check("artifact hash substitution is rejected",
              lambda: artifact_result["status"] == "FAIL"
              and any("artifact SHA-256 mismatch" in error for error in artifact_result["errors"]))
        (root / "oracle.log").write_bytes(b"W10 V8 oracle evidence\n")

        (root / "fixture.json").write_text('{"fixture":"tampered"}', encoding="utf-8")
        fixture_result = run_case(root, path)
        check("fixture manifest hash substitution is rejected",
              lambda: fixture_result["status"] == "FAIL"
              and any("fixture_sha256" in error for error in fixture_result["errors"]))
        (root / "fixture.json").write_bytes(b'{"fixture":"W10 V8 test fixture"}\n')

        bad_ref = json.loads(json.dumps(manifest))
        bad_ref["observed"]["oracle_evidence"][0]["artifact_ref"] = "missing.log"
        path.write_text(json.dumps(bad_ref), encoding="utf-8")
        ref_result = run_case(root, path)
        check("oracle must reference a verified PRESENT artifact",
              lambda: ref_result["status"] == "FAIL"
              and any("oracle references no verified" in error for error in ref_result["errors"]))

        forged_runner = json.loads(json.dumps(manifest))
        forged_runner["run_context"]["runner_id"] = "caller-controlled-runner"
        path.write_text(json.dumps(forged_runner), encoding="utf-8")
        runner_result = run_case(root, path)
        check("caller-forged runner identity is rejected",
              lambda: runner_result["status"] == "FAIL"
              and any("runner_id" in error for error in runner_result["errors"]))

        wrong_commit = json.loads(json.dumps(manifest))
        wrong_commit["run_context"]["source_commit"] = "b" * 40
        path.write_text(json.dumps(wrong_commit), encoding="utf-8")
        commit_result = run_case(root, path)
        check("stale or substituted source commit is rejected",
              lambda: commit_result["status"] == "FAIL"
              and any("source_commit" in error for error in commit_result["errors"]))

        # A valid FAIL record is integrity-valid but never acceptance-eligible.
        failed_test = json.loads(json.dumps(manifest))
        failed_test["verdict"] = "FAIL"
        path.write_text(json.dumps(failed_test), encoding="utf-8")
        failed_result = run_case(root, path)
        check("valid FAIL record can be attested but is not acceptance-eligible",
              lambda: failed_result["status"] == "PASS"
              and failed_result["acceptance_eligible"] is False)

        no_key = run_case(root, path, {"COMPUTER_AGENT_VALIDATOR_HMAC_KEY": ""})
        check("missing trusted HMAC key is BLOCKED, never PASS",
              lambda: no_key["status"] == "BLOCKED" and not no_key.get("attestation"))

        bad_pin = run_case(root, path, {"COMPUTER_AGENT_VALIDATOR_SHA256": "0" * 64})
        check("stale validator build pin is BLOCKED",
              lambda: bad_pin["status"] == "BLOCKED"
              and any("validator" in error for error in bad_pin["errors"]))
    finally:
        temp.cleanup()

    print("=" * 62)
    print(f"Acceptance validator tests: {len(FAILED)} failed")
    if FAILED:
        for item in FAILED:
            print(f"  - {item}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
