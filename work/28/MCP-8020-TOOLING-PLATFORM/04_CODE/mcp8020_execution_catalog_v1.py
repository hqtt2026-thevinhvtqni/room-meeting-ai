"""Versioned staging catalog for the strict Work 28 execution contract.

This is NOT the public v54 catalog and is NOT wired to MCP registration.
All entries remain NOT_IMPLEMENTED. It defines a deliberate future schema
migration without silently changing the existing 54-tool public contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CATALOG_VERSION = "execution-v1.0.0-draft"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


def _object(properties: dict[str, Any], required: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
        "additionalProperties": False,
    }


STRING = {"type": "string", "minLength": 1}
WORK_ID = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"}
SHA256 = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
TIMEOUT = {"type": "integer", "minimum": 1, "maximum": 300, "default": 30}
STRING_ARRAY = {"type": "array", "items": {"type": "string"}}


@dataclass(frozen=True)
class ExecutionToolSpec:
    name: str
    status: str
    description: str
    input_schema: dict[str, Any]


_RUN_SCHEMA = _object(
    {
        "work_id": WORK_ID,
        "entry_path": STRING,
        "expected_source_sha256": SHA256,
        "timeout_seconds": TIMEOUT,
    },
    ("work_id", "entry_path", "expected_source_sha256"),
)

EXECUTION_TOOL_SPECS: tuple[ExecutionToolSpec, ...] = (
    ExecutionToolSpec(
        "sandbox_run_python", NOT_IMPLEMENTED,
        "Run a Work-relative Python entrypoint bound to its expected source SHA-256; requires authorized Core/W12-W13 runtime.",
        _RUN_SCHEMA,
    ),
    ExecutionToolSpec(
        "sandbox_run_tests", NOT_IMPLEMENTED,
        "Run the approved test entrypoint bound to its expected source SHA-256; requires authorized Core/W12-W13 runtime.",
        _RUN_SCHEMA,
    ),
    ExecutionToolSpec(
        "sandbox_get_execution_status", NOT_IMPLEMENTED,
        "Read status for a run authorized to the caller and Work.",
        _object({"run_id": STRING}, ("run_id",)),
    ),
    ExecutionToolSpec(
        "sandbox_get_execution_result", NOT_IMPLEMENTED,
        "Read result for a run authorized to the caller and Work.",
        _object({"run_id": STRING}, ("run_id",)),
    ),
    ExecutionToolSpec(
        "sandbox_collect_artifact", NOT_IMPLEMENTED,
        "Collect a run artifact after authorization and Work-relative path validation.",
        _object({"run_id": STRING, "artifact_path": STRING}, ("run_id", "artifact_path")),
    ),
    ExecutionToolSpec(
        "sandbox_generate_evidence", NOT_IMPLEMENTED,
        "Generate an evidence record from trusted runtime data for an authorized run.",
        _object(
            {"run_id": STRING, "evidence_type": STRING, "refs": STRING_ARRAY},
            ("run_id", "evidence_type"),
        ),
    ),
    ExecutionToolSpec(
        "sandbox_create_handoff", NOT_IMPLEMENTED,
        "Create a handoff only from trusted, verified evidence and authorized Work state.",
        _object(
            {
                "work_id": WORK_ID,
                "status": STRING,
                "evidence_refs": STRING_ARRAY,
                "next_action": STRING,
            },
            ("work_id", "status", "next_action"),
        ),
    ),
)


def tool_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in EXECUTION_TOOL_SPECS)


def get_tool_spec(name: str) -> ExecutionToolSpec | None:
    return next((spec for spec in EXECUTION_TOOL_SPECS if spec.name == name), None)


def validate_execution_catalog() -> None:
    names = tool_names()
    if len(names) != 7 or len(set(names)) != len(names):
        raise ValueError("execution catalog must contain seven unique tool names")
    for spec in EXECUTION_TOOL_SPECS:
        if spec.status != NOT_IMPLEMENTED:
            raise ValueError(f"{spec.name} must remain fail-closed in staging")
        schema = spec.input_schema
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            raise ValueError(f"{spec.name} must use a closed object schema")
        if not set(schema.get("required", ())).issubset(schema.get("properties", {})):
            raise ValueError(f"{spec.name} has invalid required fields")
    for name in ("sandbox_run_python", "sandbox_run_tests"):
        schema = get_tool_spec(name).input_schema
        required = set(schema["required"])
        if not {"work_id", "entry_path", "expected_source_sha256"}.issubset(required):
            raise ValueError(f"{name} must bind Work, entry path and source hash")
        if {"script", "command", "args", "principal", "cwd", "shell"} & set(schema["properties"]):
            raise ValueError(f"{name} exposes a forbidden execution field")


__all__ = [
    "CATALOG_VERSION",
    "EXECUTION_TOOL_SPECS",
    "NOT_IMPLEMENTED",
    "get_tool_spec",
    "tool_names",
    "validate_execution_catalog",
]
