"""Fail-closed readiness validator for owner-approved W118 runtime contracts.

This module does not discover endpoints, authenticate, send requests, execute
Work, or claim runtime success. It validates a contract bundle supplied by
the accountable service owners before a separate, explicitly authorized
runtime preflight can be designed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit


REQUIRED_COMPONENTS = {
    "core_task_authority": ("read_task",),
    "w102_assignment_ack": ("authorize_assignment", "acknowledge_assignment"),
    "w14_execution_host": ("execute_work",),
    "w33_evidence_ingress": ("ingest_evidence",),
    "w70_evidence_register": ("register_evidence", "read_evidence"),
}
ALLOWED_AUTH_MODES = {
    "BEARER_REF", "MTLS", "SIGNED_REQUEST", "WORKLOAD_IDENTITY"
}
ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
SENSITIVE_KEYS = {
    "token", "access_token", "refresh_token", "password", "secret",
    "client_secret", "private_key", "api_key", "authorization",
}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _find_sensitive_values(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key).strip().lower()
            if key_text in SENSITIVE_KEYS:
                findings.append(f"{path}.{key}: raw credential field is forbidden")
            findings.extend(_find_sensitive_values(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_find_sensitive_values(child, f"{path}[{index}]"))
    return findings


def _validate_endpoint(value: Any, path: str, errors: list[str]) -> None:
    if not _non_empty_string(value):
        errors.append(f"{path} must be a non-empty URL")
        return
    parsed = urlsplit(value.strip())
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        errors.append(f"{path} must be an absolute HTTP(S) URL")
        return
    loopback = parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}
    if parsed.scheme != "https" and not loopback:
        errors.append(f"{path} must use HTTPS outside loopback development")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        errors.append(f"{path} must not embed credentials, query parameters or fragments")


def _validate_operation(
    component: str,
    operation_name: str,
    operation: Any,
    errors: list[str],
) -> None:
    path = f"dependencies.{component}.operations.{operation_name}"
    if not isinstance(operation, Mapping):
        errors.append(f"{path} must be an object")
        return
    method = operation.get("method")
    if not isinstance(method, str) or method.upper() not in ALLOWED_METHODS:
        errors.append(f"{path}.method must be an allowed HTTP method")
    route = operation.get("path")
    if (
        not _non_empty_string(route)
        or not route.startswith("/")
        or route.startswith("//")
        or ".." in route.split("/")
    ):
        errors.append(f"{path}.path must be an absolute service-relative path without traversal")
    for field in ("request_schema_ref", "response_schema_ref"):
        if not _non_empty_string(operation.get(field)):
            errors.append(f"{path}.{field} must reference an owner-supplied schema")
    if operation.get("side_effect") not in {"READ_ONLY", "MUTATION"}:
        errors.append(f"{path}.side_effect must be READ_ONLY or MUTATION")


def validate_runtime_contract(bundle: Any) -> dict[str, Any]:
    """Validate a contract bundle without making network or runtime calls."""
    errors: list[str] = []
    if not isinstance(bundle, Mapping):
        return _report(["bundle must be a JSON object"], [])

    errors.extend(_find_sensitive_values(bundle))
    if bundle.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if bundle.get("work_id") != "118":
        errors.append("work_id must be '118'")

    dependencies = bundle.get("dependencies")
    if not isinstance(dependencies, Mapping):
        errors.append("dependencies must be an object keyed by canonical component ID")
        return _report(errors, list(REQUIRED_COMPONENTS))

    unknown = sorted(set(dependencies) - set(REQUIRED_COMPONENTS))
    missing = sorted(set(REQUIRED_COMPONENTS) - set(dependencies))
    for component in unknown:
        errors.append(f"dependencies.{component} is not an approved W118 integration component")
    for component in missing:
        errors.append(f"dependencies.{component} contract is missing")

    for component, required_operations in REQUIRED_COMPONENTS.items():
        spec = dependencies.get(component)
        if spec is None:
            continue
        path = f"dependencies.{component}"
        if not isinstance(spec, Mapping):
            errors.append(f"{path} must be an object")
            continue

        for field in ("owner", "contract_id", "contract_version", "source_revision", "contract_ref"):
            if not _non_empty_string(spec.get(field)):
                errors.append(f"{path}.{field} must be supplied by the accountable owner")
        if spec.get("approved") is not True:
            errors.append(f"{path}.approved must be true; proposed/unapproved contracts are blocked")

        _validate_endpoint(spec.get("base_url"), f"{path}.base_url", errors)

        auth = spec.get("auth")
        if not isinstance(auth, Mapping):
            errors.append(f"{path}.auth must be an owner-defined authentication object")
        else:
            if auth.get("mode") not in ALLOWED_AUTH_MODES:
                errors.append(f"{path}.auth.mode is unsupported or missing")
            if not _non_empty_string(auth.get("credential_ref")):
                errors.append(f"{path}.auth.credential_ref must reference a secret manager entry; raw secrets are forbidden")

        operations = spec.get("operations")
        if not isinstance(operations, Mapping):
            errors.append(f"{path}.operations must be an object")
            continue
        for operation_name in required_operations:
            if operation_name not in operations:
                errors.append(f"{path}.operations.{operation_name} is required")
            else:
                _validate_operation(component, operation_name, operations[operation_name], errors)

        evidence = spec.get("evidence")
        if not isinstance(evidence, Mapping):
            errors.append(f"{path}.evidence must define evidence binding")
        else:
            for field in ("correlation_id_field", "receipt_id_field"):
                if not _non_empty_string(evidence.get(field)):
                    errors.append(f"{path}.evidence.{field} must be owner-defined")

    return _report(errors, missing)


def _report(errors: list[str], missing: list[str]) -> dict[str, Any]:
    ready = not errors
    return {
        "work_id": "118",
        "check": "RUNTIME_CONTRACT_READINESS",
        "status": "READY_FOR_RUNTIME_PREFLIGHT" if ready else "BLOCKED",
        "runtime_execution_performed": False,
        "runtime_pass": False,
        "authority_granted": False,
        "missing_components": missing,
        "errors": errors,
        "limitations": [
            "This is static contract-bundle validation only.",
            "No endpoint was contacted and no credential was loaded.",
            "Readiness does not prove service availability, authorization or Runtime E2E.",
            "A separate owner-authorized preflight and evidence read-back are still required.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, help="Path to owner-supplied runtime contract JSON")
    args = parser.parse_args()
    try:
        bundle = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(_report([f"cannot read contract bundle: {exc}"], list(REQUIRED_COMPONENTS)), indent=2))
        return 2
    report = validate_runtime_contract(bundle)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "READY_FOR_RUNTIME_PREFLIGHT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
