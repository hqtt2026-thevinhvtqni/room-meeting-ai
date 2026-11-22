"""Pure JSON Schema validation helpers for the Work 28 unified MCP registry.

This module deliberately has no MCP SDK dependency so schema contracts can be
validated in offline CI and local test runners without importing a transport.
"""
from __future__ import annotations

from typing import Any
import inspect

from jsonschema import Draft202012Validator, SchemaError



def validate_registered_schemas(specs: Any = None) -> None:
    """Fail closed if any registered tool input schema is not Draft 2020-12."""
    if specs is None:
        # Lazy import avoids a registry <-> validator module cycle.
        from mcp8020_unified_registry_v1 import TOOL_SPECS
        specs = TOOL_SPECS
    for spec in specs:
        try:
            Draft202012Validator.check_schema(spec.input_schema)
        except SchemaError as exc:
            raise ValueError(
                f"{spec.name}: invalid registered input schema"
            ) from exc


def validate_tool_arguments(spec: Any, arguments: Any) -> dict[str, Any]:
    """Validate the complete schema before a provider can receive arguments.

    Error messages intentionally omit submitted values.
    """
    if not isinstance(arguments, dict):
        raise ValueError("tool arguments must be an object")
    try:
        Draft202012Validator.check_schema(spec.input_schema)
    except SchemaError as exc:
        raise ValueError(f"{spec.name}: invalid registered input schema") from exc

    errors = sorted(
        Draft202012Validator(spec.input_schema).iter_errors(arguments),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            str(error.validator),
        ),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        raise ValueError(
            f"{spec.name}: invalid arguments at {location} ({error.validator})"
        )
    return arguments



def validate_provider_handler_signature(spec: Any, handler: Any) -> None:
    """Ensure registry keyword arguments can be passed to a provider handler."""
    if not callable(handler):
        raise ValueError(f"{spec.name}: provider handler is not callable")
    try:
        signature = inspect.signature(handler)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{spec.name}: provider handler signature is not inspectable") from exc

    parameters = signature.parameters
    accepts_extra_keywords = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
    schema_properties = set(spec.input_schema.get("properties", {}))
    keyword_parameters = {
        name
        for name, parameter in parameters.items()
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }
    positional_only = {
        name
        for name, parameter in parameters.items()
        if parameter.kind is inspect.Parameter.POSITIONAL_ONLY
    }
    required_parameters = {
        name
        for name, parameter in parameters.items()
        if parameter.default is inspect.Parameter.empty
        and parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }
    schema_required = set(spec.input_schema.get("required", []))
    optional_schema_required_by_handler = {
        name
        for name, parameter in parameters.items()
        if name in (schema_properties - schema_required)
        and parameter.default is inspect.Parameter.empty
        and parameter.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }

    unsupported = schema_properties - keyword_parameters
    if accepts_extra_keywords:
        unsupported = schema_properties & positional_only
    missing_required = required_parameters - schema_properties
    if unsupported or missing_required or optional_schema_required_by_handler:
        raise ValueError(
            f"{spec.name}: provider handler signature is incompatible with registry schema"
        )
