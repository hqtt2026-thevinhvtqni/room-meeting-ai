"""Work 28 v54 protocol-agnostic service: schema validation + dispatch.

tools/list and tools/call semantics live here so they are testable without
the mcp package. The MCP adapter in mcp8020_server_v54 wraps this service.
Fail-closed binding: every IMPLEMENTED tool must resolve to a provider
handler at construction time.
"""
from __future__ import annotations
import re
from typing import Any
from mcp8020_catalog_v54 import (CATALOG_VERSION, GROUP_BROWSER, GROUP_COMPUTER, GROUP_ROOM, GROUP_SANDBOX,
                                 IMPLEMENTED, NOT_IMPLEMENTED, TOOL_SPECS, ToolCallError, export_mcp_tools)

class V54BindingError(RuntimeError):
    pass

def _matches_type(value: Any, type_spec: Any) -> bool:
    if isinstance(type_spec, list):
        return any(_matches_type(value, item) for item in type_spec)
    if type_spec == "string":
        return isinstance(value, str)
    if type_spec == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_spec == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_spec == "boolean":
        return isinstance(value, bool)
    if type_spec == "array":
        return isinstance(value, list)
    if type_spec == "object":
        return isinstance(value, dict)
    if type_spec == "null":
        return value is None
    return True

def _validate_property(name: str, key: str, value: Any, prop: dict[str, Any]) -> None:
    type_spec = prop.get("type")
    if type_spec is not None and not _matches_type(value, type_spec):
        raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' has an invalid type")
    if "enum" in prop and value not in prop["enum"]:
        raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' must be one of " + repr(prop["enum"]))
    if isinstance(value, str):
        if "minLength" in prop and len(value) < prop["minLength"]:
            raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' is shorter than minLength")
        if "maxLength" in prop and len(value) > prop["maxLength"]:
            raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' is longer than maxLength")
        if "pattern" in prop and re.search(prop["pattern"], value) is None:
            raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' does not match the required pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in prop and value < prop["minimum"]:
            raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' is below the minimum")
        if "maximum" in prop and value > prop["maximum"]:
            raise ToolCallError("INVALID_INPUT", name + ": argument '" + key + "' is above the maximum")
    if isinstance(value, list) and "items" in prop:
        item_type = prop["items"].get("type")
        for index, item in enumerate(value):
            if item_type is not None and not _matches_type(item, item_type):
                raise ToolCallError("INVALID_INPUT", name + ": item " + str(index) + " of '" + key + "' has an invalid type")

def _validate_arguments(name: str, schema: dict[str, Any], args: Any) -> None:
    if not isinstance(args, dict):
        raise ToolCallError("INVALID_INPUT", name + ": tool arguments must be an object")
    properties = schema.get("properties", {})
    for key in schema.get("required", []):
        if key not in args:
            raise ToolCallError("INVALID_INPUT", name + ": missing required argument: " + key)
    for key in args:
        if key not in properties:
            raise ToolCallError("INVALID_INPUT", name + ": unsupported argument: " + key)
    for key, value in args.items():
        _validate_property(name, key, value, properties[key])

_EXECUTION_GATEWAY_TOOLS = (
    "sandbox_run_python", "sandbox_run_command", "sandbox_get_execution_status",
    "sandbox_get_execution_result", "sandbox_collect_artifact",
    "sandbox_generate_evidence", "sandbox_create_handoff",
)

class V54Service:
    def __init__(self, *, room: Any, sandbox: Any, computer: Any = None, browser: Any = None,
                 execution: Any = None) -> None:
        self._providers = {GROUP_ROOM: room, GROUP_SANDBOX: sandbox, GROUP_COMPUTER: computer, GROUP_BROWSER: browser}
        # The execution gateway is an optional provider that answers the seven
        # sandbox execution/evidence tools. It is protocol-complete but its
        # default client stays fail-closed BLOCKED until a verified Core route
        # exists; catalog statuses for those tools stay NOT_IMPLEMENTED either
        # way (no status promotion without implementation + evidence).
        self._execution = execution
        self._specs_by_name = {spec.name: spec for spec in TOOL_SPECS}
        for spec in TOOL_SPECS:
            if spec.status != IMPLEMENTED:
                continue
            provider = self._providers.get(spec.group)
            if provider is None or not callable(getattr(provider, spec.name, None)):
                raise V54BindingError("required provider handler unavailable: " + spec.name)
        if execution is not None:
            for tool in _EXECUTION_GATEWAY_TOOLS:
                if not callable(getattr(execution, tool, None)):
                    raise V54BindingError("required execution gateway handler unavailable: " + tool)

    def list_tools(self) -> list[dict[str, Any]]:
        return export_mcp_tools()

    def call_tool(self, name: str, arguments: Any = None) -> dict[str, Any]:
        spec = self._specs_by_name.get(name)
        if spec is None:
            return {"ok": False, "tool": name, "error": {"code": "UNKNOWN_TOOL", "message": "unknown Work 28 v54 tool: " + name}}
        if spec.status == NOT_IMPLEMENTED:
            # Honest catalog status is never promoted. When an execution
            # gateway is injected, the seven execution/evidence tools are
            # routed to it so the client's real answer (default: fail-closed
            # BLOCKED) is returned instead of a generic stub message.
            if self._execution is not None and name in _EXECUTION_GATEWAY_TOOLS:
                args = arguments if arguments is not None else {}
                try:
                    _validate_arguments(name, spec.input_schema, args)
                except ToolCallError as exc:
                    return {"ok": False, "tool": name, "error": {"code": exc.code, "message": exc.message}}
                handler = getattr(self._execution, name)
                try:
                    data = handler(**args)
                except ToolCallError as exc:
                    return {"ok": False, "tool": name, "error": {"code": exc.code, "message": exc.message, "status": NOT_IMPLEMENTED}}
                except Exception as exc:  # fail-closed: never leak a raw traceback as success
                    return {"ok": False, "tool": name, "error": {"code": "HANDLER_ERROR", "message": str(exc), "status": NOT_IMPLEMENTED}}
                return {"ok": False, "tool": name, "data": data,
                        "catalog_status": NOT_IMPLEMENTED,
                        "contract_version": CATALOG_VERSION}
            return {"ok": False, "tool": name, "error": {"code": "NOT_IMPLEMENTED", "message": name + " is not implemented in this build; see the tool catalog status", "status": NOT_IMPLEMENTED}}
        args = arguments if arguments is not None else {}
        try:
            _validate_arguments(name, spec.input_schema, args)
        except ToolCallError as exc:
            return {"ok": False, "tool": name, "error": {"code": exc.code, "message": exc.message}}
        handler = getattr(self._providers[spec.group], spec.name)
        try:
            data = handler(**args)
        except ToolCallError as exc:
            return {"ok": False, "tool": name, "error": {"code": exc.code, "message": exc.message}}
        except Exception as exc:  # fail-closed: never leak a raw traceback as success
            return {"ok": False, "tool": name, "error": {"code": "HANDLER_ERROR", "message": str(exc)}}
        return {"ok": True, "tool": name, "data": data, "contract_version": CATALOG_VERSION}

def create_v54_service(*, room: Any, sandbox: Any, computer: Any = None, browser: Any = None,
                       execution: Any = None) -> V54Service:
    return V54Service(room=room, sandbox=sandbox, computer=computer, browser=browser, execution=execution)
