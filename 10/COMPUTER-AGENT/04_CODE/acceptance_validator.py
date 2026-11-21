"""Trusted semantic validator for Work 10 P0 acceptance manifests (V8).

The validator never trusts caller-authored consistency flags. It recomputes
state equality, category/outcome policy, fixture/artifact hashes and host
provenance, then emits an HMAC-signed attestation. A missing or mismatched
trust configuration is BLOCKED, never PASS.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import hmac
import json
import os
import platform
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = WORK_ROOT / "06_EVIDENCE" / "W10_P0_ACCEPTANCE_MANIFEST_V8.schema.json"
POLICY_PATH = WORK_ROOT / "06_EVIDENCE" / "W10_P0_CATEGORY_OUTCOME_POLICY_V8.json"
VALIDATOR_ID = "W10-P0-ACCEPTANCE-VALIDATOR"
VALIDATOR_VERSION = "1.0.0"
STATE_FIELDS = (
    "outcome", "admission", "gate", "process_state",
    "containment_state", "lease_state", "owner_state",
)
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _architecture() -> str:
    machine = platform.machine().casefold()
    if machine in {"amd64", "x86_64", "x64"}:
        return "x86_64"
    if machine in {"arm64", "aarch64"}:
        return "arm64"
    return machine


def _os_family() -> str:
    return "windows" if os.name == "nt" else "linux"


def _safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("artifact reference must be a non-empty relative path")
    raw = Path(relative)
    if raw.is_absolute() or any(part == ".." for part in raw.parts):
        raise ValueError("artifact reference must not be absolute or contain '..'")
    resolved_root = root.resolve(strict=True)
    resolved = (resolved_root / raw).resolve(strict=True)
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        raise ValueError("artifact reference resolves outside evidence_root") from None
    if not resolved.is_file():
        raise ValueError("artifact reference is not a regular file")
    return resolved


def _trust_config():
    expected = {
        "validator": os.getenv("COMPUTER_AGENT_VALIDATOR_SHA256", "").lower(),
        "schema": os.getenv("COMPUTER_AGENT_VALIDATOR_SCHEMA_SHA256", "").lower(),
        "policy": os.getenv("COMPUTER_AGENT_VALIDATOR_POLICY_SHA256", "").lower(),
    }
    actual = {
        "validator": _sha256_file(Path(__file__).resolve()),
        "schema": _sha256_file(SCHEMA_PATH),
        "policy": _sha256_file(POLICY_PATH),
    }
    missing = [name for name, value in expected.items() if not SHA256_RE.fullmatch(value)]
    if missing:
        raise RuntimeError("pinned trust hashes missing/invalid: " + ", ".join(missing))
    mismatched = [name for name in expected if not hmac.compare_digest(expected[name], actual[name])]
    if mismatched:
        raise RuntimeError("pinned trust hash mismatch: " + ", ".join(mismatched))

    raw_key = os.getenv("COMPUTER_AGENT_VALIDATOR_HMAC_KEY", "")
    if not raw_key:
        raise RuntimeError("COMPUTER_AGENT_VALIDATOR_HMAC_KEY is not configured")
    if re.fullmatch(r"[0-9a-fA-F]{64,}", raw_key):
        key = bytes.fromhex(raw_key)
    else:
        key = raw_key.encode("utf-8")
    if len(key) < 32:
        raise RuntimeError("validator HMAC key must contain at least 32 bytes")
    key_id = os.getenv("COMPUTER_AGENT_VALIDATOR_KEY_ID", "")
    if not key_id:
        raise RuntimeError("COMPUTER_AGENT_VALIDATOR_KEY_ID is not configured")
    return actual, key, key_id


def _load_trust_files():
    try:
        import jsonschema
        from jsonschema import Draft202012Validator, FormatChecker
    except Exception as exc:
        raise RuntimeError(f"jsonschema dependency unavailable: {exc}") from exc
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker()), policy


def _semantic_errors(manifest: dict, evidence_root: Path, policy: dict) -> list[str]:
    errors: list[str] = []
    category = manifest["test"]["category"]
    category_policy = policy.get("categories", {}).get(category)
    if not isinstance(category_policy, dict):
        return [f"category has no pinned outcome policy: {category}"]

    run_context = manifest["run_context"]
    actual_runner = os.getenv("COMPUTER_AGENT_VALIDATOR_RUNNER_ID") or platform.node()
    if run_context["runner_id"] != actual_runner:
        errors.append("run_context.runner_id does not match trusted runner identity")

    expected_commit = os.getenv("COMPUTER_AGENT_SOURCE_COMMIT") or os.getenv("GITHUB_SHA")
    recorded_commit = run_context["source_commit"]
    if expected_commit:
        if recorded_commit.lower() != expected_commit.lower():
            errors.append("run_context.source_commit does not match trusted source commit")
    elif recorded_commit == "LOCAL" and os.getenv("COMPUTER_AGENT_VALIDATOR_ALLOW_LOCAL") == "1":
        pass
    else:
        errors.append("trusted source commit is unavailable or manifest commit is unpinned")

    try:
        started = _parse_time(run_context["started_at"])
        finished = _parse_time(run_context["finished_at"])
        recorded = _parse_time(manifest["recorded_at"])
        if started > finished or finished > recorded:
            errors.append("run_context timestamps are not monotonic")
    except Exception:
        errors.append("run_context timestamps are invalid")

    profile = manifest["profile"]
    if profile["os_family"] != _os_family():
        errors.append("profile.os_family does not match trusted runner OS")
    if profile.get("host_build") != platform.version():
        errors.append("profile.host_build does not match trusted runner build")
    if profile.get("architecture") != _architecture():
        errors.append("profile.architecture does not match trusted runner architecture")

    fixture_ref = profile.get("fixture_manifest_ref")
    if profile.get("support_status") == "SUPPORTED":
        try:
            fixture_path = _safe_file(evidence_root, fixture_ref)
            fixture_hash = _sha256_file(fixture_path)
            if not hmac.compare_digest(fixture_hash, str(profile.get("fixture_sha256", "")).lower()):
                errors.append("profile.fixture_sha256 does not match fixture manifest bytes")
        except Exception as exc:
            errors.append(f"fixture manifest invalid: {exc}")

    present_artifacts: set[str] = set()
    for artifact in manifest.get("artifacts", []):
        if artifact.get("status") != "PRESENT":
            continue
        name = artifact.get("name", "")
        try:
            path = _safe_file(evidence_root, name)
            actual_hash = _sha256_file(path)
            expected_hash = str(artifact.get("sha256", "")).lower()
            if not hmac.compare_digest(actual_hash, expected_hash):
                errors.append(f"artifact SHA-256 mismatch: {name}")
            else:
                present_artifacts.add(name)
        except Exception as exc:
            errors.append(f"artifact invalid ({name}): {exc}")

    for oracle in manifest.get("observed", {}).get("oracle_evidence", []):
        ref = oracle.get("artifact_ref")
        if ref not in present_artifacts:
            errors.append(f"oracle references no verified PRESENT artifact: {ref}")

    if manifest.get("verdict") == "PASS":
        if profile.get("support_status") != "SUPPORTED":
            errors.append("PASS requires profile.support_status=SUPPORTED")
        expected_state = manifest["expected"]
        observed_state = manifest["observed"]
        mismatches = [
            field for field in STATE_FIELDS
            if expected_state.get(field) != observed_state.get(field)
        ]
        if mismatches:
            errors.append("expected/observed state tuple mismatch: " + ", ".join(mismatches))

        if observed_state.get("outcome") not in category_policy.get("pass_allowed_outcomes", []):
            errors.append(
                f"observed outcome {observed_state.get('outcome')} is not allowed for PASS "
                f"in category {category}"
            )
        if observed_state.get("lease_state") not in category_policy.get("allowed_lease_states", []):
            errors.append("lease_state is UNKNOWN or not allowed for this category")
        if observed_state.get("owner_state") not in category_policy.get("allowed_owner_states", []):
            errors.append("owner_state is UNKNOWN or not allowed for this category")
        if observed_state.get("admission") != "CLOSED":
            errors.append("PASS requires admission=CLOSED")
        if observed_state.get("gate") != "CLOSED":
            errors.append("PASS requires gate=CLOSED")
        if observed_state.get("containment_state") != "EMPTY":
            errors.append("PASS requires containment_state=EMPTY")
        if observed_state.get("process_state") not in {"ABSENT", "EXITED"}:
            errors.append("PASS requires process_state ABSENT or EXITED")
        if not present_artifacts:
            errors.append("PASS requires at least one verified PRESENT artifact")
        if not manifest["observed"].get("oracle_evidence"):
            errors.append("PASS requires structured oracle evidence")

    return errors


def _build_attestation(manifest: dict, validation_status: str, acceptance_eligible: bool,
                       errors: list[str], hashes: dict[str, str], key: bytes, key_id: str,
                       input_sha256: str) -> dict:
    started = _utc_now()
    runner = {
        "runner_id": os.getenv("COMPUTER_AGENT_VALIDATOR_RUNNER_ID") or platform.node(),
        "pid": os.getpid(),
        "os_family": _os_family(),
        "host_build": platform.version(),
        "architecture": _architecture(),
        "python_version": platform.python_version(),
        "source_commit": os.getenv("COMPUTER_AGENT_SOURCE_COMMIT") or os.getenv("GITHUB_SHA") or "UNPINNED",
        "execution_id": str(uuid.uuid4()),
        "started_at": started,
    }
    result = {
        "validation_status": validation_status,
        "acceptance_eligible": bool(acceptance_eligible),
        "manifest_verdict": manifest.get("verdict") if isinstance(manifest, dict) else None,
        "errors": errors,
    }
    unsigned = {
        "attestation_version": "1.0.0",
        "validator_id": VALIDATOR_ID,
        "validator_version": VALIDATOR_VERSION,
        "validator_sha256": hashes["validator"],
        "schema_sha256": hashes["schema"],
        "policy_sha256": hashes["policy"],
        "input_sha256": input_sha256,
        "semantic_result_sha256": _sha256_bytes(_canonical(result)),
        "runner_provenance": runner,
        "result": result,
        "issued_at": _utc_now(),
    }
    signature = hmac.new(key, _canonical(unsigned), hashlib.sha256).hexdigest()
    unsigned["signature"] = {
        "algorithm": "HMAC-SHA256",
        "key_id": key_id,
        "value": signature,
    }
    return unsigned


def verify_attestation(attestation: dict, key: bytes, *, expected_input_sha256: str | None = None,
                       expected_validator_sha256: str | None = None,
                       expected_schema_sha256: str | None = None,
                       expected_policy_sha256: str | None = None) -> bool:
    try:
        signature = attestation["signature"]
        if signature["algorithm"] != "HMAC-SHA256":
            return False
        unsigned = copy.deepcopy(attestation)
        unsigned.pop("signature")
        actual = hmac.new(key, _canonical(unsigned), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(actual, signature["value"]):
            return False
        checks = (
            (expected_input_sha256, attestation["input_sha256"]),
            (expected_validator_sha256, attestation["validator_sha256"]),
            (expected_schema_sha256, attestation["schema_sha256"]),
            (expected_policy_sha256, attestation["policy_sha256"]),
        )
        return all(expected is None or hmac.compare_digest(expected.lower(), value.lower())
                   for expected, value in checks)
    except (KeyError, TypeError, AttributeError):
        return False


def validate_file(manifest_path: str | Path, evidence_root: str | Path,
                  attestation_path: str | Path | None = None) -> dict:
    manifest_path = Path(manifest_path).resolve(strict=True)
    evidence_root = Path(evidence_root).resolve(strict=True)
    try:
        manifest_path.relative_to(evidence_root)
    except ValueError:
        return {"status": "BLOCKED", "acceptance_eligible": False,
                "error": "manifest path is outside evidence_root"}

    raw = manifest_path.read_bytes()
    input_sha256 = _sha256_bytes(raw)
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        return {"status": "FAIL", "acceptance_eligible": False,
                "input_sha256": input_sha256, "errors": [f"manifest JSON invalid: {exc}"]}

    try:
        hashes, key, key_id = _trust_config()
        schema_validator, policy = _load_trust_files()
    except Exception as exc:
        return {"status": "BLOCKED", "acceptance_eligible": False,
                "input_sha256": input_sha256, "errors": [str(exc)]}

    schema_errors = sorted(
        schema_validator.iter_errors(manifest),
        key=lambda error: list(error.absolute_path),
    )
    errors = [
        f"schema:{'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in schema_errors[:50]
    ]
    if not errors:
        errors.extend(_semantic_errors(manifest, evidence_root, policy))

    validation_status = "FAIL" if errors else "PASS"
    acceptance_eligible = validation_status == "PASS" and manifest.get("verdict") == "PASS"
    attestation = _build_attestation(
        manifest, validation_status, acceptance_eligible, errors,
        hashes, key, key_id, input_sha256,
    )
    attestation_bytes = _canonical(attestation) + b"\n"
    attestation_sha256 = _sha256_bytes(attestation_bytes)
    output_path = None
    if attestation_path is not None:
        output_path = Path(attestation_path).resolve(strict=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = output_path.with_name(f".{output_path.name}.{uuid.uuid4().hex}.tmp")
        try:
            with temp_path.open("xb") as handle:
                handle.write(attestation_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, output_path)
        finally:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass

    return {
        "status": validation_status,
        "acceptance_eligible": acceptance_eligible,
        "input_sha256": input_sha256,
        "attestation_sha256": attestation_sha256,
        "attestation_path": str(output_path) if output_path else None,
        "attestation": attestation,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Work 10 P0 V8 acceptance manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--attestation-out")
    args = parser.parse_args()
    result = validate_file(args.manifest, args.evidence_root, args.attestation_out)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if result["status"] == "PASS":
        return 0
    if result["status"] == "BLOCKED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
