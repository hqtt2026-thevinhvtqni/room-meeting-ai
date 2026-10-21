"""Work 28 v54 tool catalog: the 54-tool planning set from WORK28_TOOL_CONTRACT_CATALOG_V1_54.md.

DESIGN/CONTRACT stage. This catalog defines schemas, groups, and per-tool
implementation status. It does NOT claim live registration on MCP :8020.
Core :8000 remains the authorization authority; caller-supplied identity is
never treated as proof of authority.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

CATALOG_VERSION = "54.0.0-draft1"
IMPLEMENTED = "IMPLEMENTED"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

GROUP_ROOM = "room"
GROUP_SANDBOX = "sandbox"
GROUP_COMPUTER = "computer"
GROUP_BROWSER = "browser"

class ToolCallError(RuntimeError):
    """Stable typed error raised by handlers; wrapped into the result envelope."""
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

@dataclass(frozen=True)
class ToolSpec:
    name: str
    group: str
    status: str
    description: str
    input_schema: dict[str, Any]

def _schema(properties: dict[str, Any], required: tuple[str, ...] = ()) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": list(required), "additionalProperties": False}

S = {"type": "string"}
NS = {"type": ["string", "null"]}
INT_LIMIT = {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}
INT_OFFSET = {"type": "integer", "minimum": 0, "default": 0}
STR_ARRAY = {"type": "array", "items": {"type": "string"}, "default": []}
WORK_ID = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"}
UP_DOWN = {"type": "string", "enum": ["up", "down"]}

TOOL_SPECS: tuple[ToolSpec, ...] = (
    # ---- ROOM / meeting / task group (10) ----
    ToolSpec("room_get_context", GROUP_ROOM, IMPLEMENTED, "Read the current authorized ROOM context.", _schema({"selector": NS})),
    ToolSpec("room_get_structure", GROUP_ROOM, IMPLEMENTED, "Read the ROOM hierarchy/structure for an optional scope.", _schema({"scope": NS})),
    ToolSpec("room_list_meetings", GROUP_ROOM, IMPLEMENTED, "List meeting summaries with bounded pagination.", _schema({"status_filter": NS, "limit": INT_LIMIT, "offset": INT_OFFSET})),
    ToolSpec("room_get_meeting", GROUP_ROOM, IMPLEMENTED, "Read one meeting record by ID.", _schema({"meeting_id": S}, ("meeting_id",))),
    ToolSpec("room_get_transcript", GROUP_ROOM, IMPLEMENTED, "Read transcript segments for one meeting with a bounded range.", _schema({"meeting_id": S, "offset": INT_OFFSET, "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 100}}, ("meeting_id",))),
    ToolSpec("room_start_meeting", GROUP_ROOM, IMPLEMENTED, "Start a meeting with a title and explicit starter identity.", _schema({"title": S, "identity_id": S, "participants": STR_ARRAY}, ("title", "identity_id"))),
    ToolSpec("room_join_meeting", GROUP_ROOM, IMPLEMENTED, "Join a meeting as a validated participant identity.", _schema({"meeting_id": S, "identity_id": S}, ("meeting_id", "identity_id"))),
    ToolSpec("room_append_meeting_message", GROUP_ROOM, IMPLEMENTED, "Append a message to an active meeting transcript.", _schema({"meeting_id": S, "content": S, "speaker": NS}, ("meeting_id", "content"))),
    ToolSpec("room_get_pending_tasks", GROUP_ROOM, IMPLEMENTED, "List pending tasks with optional owner/status filters.", _schema({"owner": NS, "status_filter": NS, "limit": INT_LIMIT, "offset": INT_OFFSET})),
    ToolSpec("room_submit_proposal", GROUP_ROOM, IMPLEMENTED, "Submit a proposal and create a pending review task.", _schema({"identity_id": S, "content": S, "scope": NS, "evidence_refs": STR_ARRAY}, ("identity_id", "content"))),
    # ---- Sandbox / file / execution / evidence group (21) ----
    ToolSpec("sandbox_list_works", GROUP_SANDBOX, IMPLEMENTED, "List accessible Work IDs with bounded pagination.", _schema({"limit": INT_LIMIT, "offset": INT_OFFSET})),
    ToolSpec("sandbox_create_work", GROUP_SANDBOX, IMPLEMENTED, "Create a Work Sandbox with a validated work ID.", _schema({"work_id": WORK_ID, "work_name": S, "identity_id": NS}, ("work_id", "work_name"))),
    ToolSpec("sandbox_list", GROUP_SANDBOX, IMPLEMENTED, "List entries inside an authorized Work Sandbox path.", _schema({"work_id": S, "path": {"type": "string", "default": ""}}, ("work_id",))),
    ToolSpec("sandbox_read", GROUP_SANDBOX, IMPLEMENTED, "Read a bounded UTF-8 byte range from a Work Sandbox file.", _schema({"work_id": S, "path": S, "offset": INT_OFFSET, "length": {"type": "integer", "minimum": 1, "maximum": 65536, "default": 16384}}, ("work_id", "path"))),
    ToolSpec("sandbox_write", GROUP_SANDBOX, IMPLEMENTED, "Create or overwrite a Work Sandbox text file; returns the content hash.", _schema({"work_id": S, "path": S, "content": S, "overwrite": {"type": "boolean", "default": False}}, ("work_id", "path", "content"))),
    ToolSpec("sandbox_append", GROUP_SANDBOX, IMPLEMENTED, "Append text to an existing Work Sandbox file; returns the content hash.", _schema({"work_id": S, "path": S, "content": S}, ("work_id", "path", "content"))),
    ToolSpec("sandbox_delete", GROUP_SANDBOX, IMPLEMENTED, "Delete a Work Sandbox file behind an explicit confirmation guard.", _schema({"work_id": S, "path": S, "confirm_delete": {"type": "boolean", "default": False}}, ("work_id", "path", "confirm_delete"))),
    ToolSpec("sandbox_search", GROUP_SANDBOX, IMPLEMENTED, "Search filenames and text content inside one Work Sandbox with a bounded result count.", _schema({"work_id": S, "query": S, "path": {"type": "string", "default": ""}, "glob": {"type": "string", "default": "*"}, "limit": INT_LIMIT}, ("work_id", "query"))),
    ToolSpec("sandbox_read_file_metadata", GROUP_SANDBOX, IMPLEMENTED, "Read size/hash/timestamps for a Work Sandbox file.", _schema({"work_id": S, "path": S}, ("work_id", "path"))),
    ToolSpec("sandbox_create_directory", GROUP_SANDBOX, IMPLEMENTED, "Create a directory inside a Work Sandbox.", _schema({"work_id": S, "path": S}, ("work_id", "path"))),
    ToolSpec("sandbox_copy_file", GROUP_SANDBOX, IMPLEMENTED, "Copy a file within one Work Sandbox.", _schema({"work_id": S, "source_path": S, "destination_path": S}, ("work_id", "source_path", "destination_path"))),
    ToolSpec("sandbox_move_file", GROUP_SANDBOX, IMPLEMENTED, "Move or rename a file within one Work Sandbox.", _schema({"work_id": S, "source_path": S, "destination_path": S}, ("work_id", "source_path", "destination_path"))),
    ToolSpec("sandbox_get_manifest", GROUP_SANDBOX, IMPLEMENTED, "Read the Work manifest with provenance metadata and file inventory.", _schema({"work_id": S, "path": {"type": "string", "default": ""}}, ("work_id",))),
    ToolSpec("sandbox_validate_path", GROUP_SANDBOX, IMPLEMENTED, "Normalize a Work-relative path and return an allow/deny decision for an operation.", _schema({"work_id": S, "path": S, "operation": {"type": "string", "enum": ["READ", "WRITE", "DELETE"]}}, ("work_id", "path", "operation"))),
    ToolSpec("sandbox_run_python", GROUP_SANDBOX, NOT_IMPLEMENTED, "Run a bounded Python entrypoint through the approved Core/W12-W13 runtime. Requires the authorized execution path; not available in this build.", _schema({"work_id": S, "script": S, "args": STR_ARRAY, "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 300, "default": 30}}, ("work_id", "script"))),
    ToolSpec("sandbox_run_command", GROUP_SANDBOX, NOT_IMPLEMENTED, "Run an allowlisted command through the approved runtime. Requires the authorized execution path; not available in this build.", _schema({"work_id": S, "command": S, "args": STR_ARRAY, "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 300, "default": 30}}, ("work_id", "command"))),
    ToolSpec("sandbox_get_execution_status", GROUP_SANDBOX, NOT_IMPLEMENTED, "Read the status of one execution run. Requires the authorized execution path; not available in this build.", _schema({"run_id": S}, ("run_id",))),
    ToolSpec("sandbox_get_execution_result", GROUP_SANDBOX, NOT_IMPLEMENTED, "Read the captured result of one execution run. Requires the authorized execution path; not available in this build.", _schema({"run_id": S}, ("run_id",))),
    ToolSpec("sandbox_collect_artifact", GROUP_SANDBOX, NOT_IMPLEMENTED, "Collect one artifact of an execution run. Requires the authorized execution path; not available in this build.", _schema({"run_id": S, "artifact_path": S}, ("run_id", "artifact_path"))),
    ToolSpec("sandbox_generate_evidence", GROUP_SANDBOX, NOT_IMPLEMENTED, "Generate an evidence record for a run. Requires the authorized execution path; not available in this build.", _schema({"run_id": S, "evidence_type": S, "refs": STR_ARRAY}, ("run_id", "evidence_type"))),
    ToolSpec("sandbox_create_handoff", GROUP_SANDBOX, NOT_IMPLEMENTED, "Create a handoff record. Requires verified execution evidence; not available in this build.", _schema({"work_id": S, "status": S, "evidence_refs": STR_ARRAY, "next_action": S}, ("work_id", "status", "next_action"))),
    # ---- Computer Agent group (6) ----
    ToolSpec("computer_screenshot", GROUP_COMPUTER, NOT_IMPLEMENTED, "Capture a screenshot. Requires the W14 computer runtime; not available in this build.", _schema({"display": NS, "region": NS})),
    ToolSpec("computer_click", GROUP_COMPUTER, NOT_IMPLEMENTED, "Click at coordinates or a target. Requires the W14 computer runtime; not available in this build.", _schema({"x": {"type": "integer"}, "y": {"type": "integer"}, "target": NS}, ("x", "y"))),
    ToolSpec("computer_type", GROUP_COMPUTER, NOT_IMPLEMENTED, "Type text into a focused target. Requires the W14 computer runtime; not available in this build.", _schema({"text": S, "target": NS}, ("text",))),
    ToolSpec("computer_keypress", GROUP_COMPUTER, NOT_IMPLEMENTED, "Press an allowlisted key or chord. Requires the W14 computer runtime; not available in this build.", _schema({"keys": STR_ARRAY}, ("keys",))),
    ToolSpec("computer_scroll", GROUP_COMPUTER, NOT_IMPLEMENTED, "Scroll a direction and bounded amount. Requires the W14 computer runtime; not available in this build.", _schema({"direction": UP_DOWN, "amount": {"type": "integer", "minimum": 1, "maximum": 100, "default": 3}, "target": NS}, ("direction",))),
    ToolSpec("computer_get_screen_state", GROUP_COMPUTER, NOT_IMPLEMENTED, "Read the current screen state. Requires the W14 computer runtime; not available in this build.", _schema({"capture": NS})),
    # ---- Browser Agent and OCR group (13) ----
    ToolSpec("browser_open", GROUP_BROWSER, NOT_IMPLEMENTED, "Open a URL under a navigation policy. Requires the W14 browser runtime; not available in this build.", _schema({"url": S, "policy": NS}, ("url",))),
    ToolSpec("browser_get_text", GROUP_BROWSER, NOT_IMPLEMENTED, "Read visible text of a page scope. Requires the W14 browser runtime; not available in this build.", _schema({"selector": NS})),
    ToolSpec("browser_screenshot", GROUP_BROWSER, NOT_IMPLEMENTED, "Capture a page/viewport screenshot. Requires the W14 browser runtime; not available in this build.", _schema({"viewport": NS})),
    ToolSpec("browser_click", GROUP_BROWSER, NOT_IMPLEMENTED, "Click a locator with a bounded timeout. Requires the W14 browser runtime; not available in this build.", _schema({"selector": S, "timeout_ms": {"type": "integer", "minimum": 100, "maximum": 30000, "default": 5000}}, ("selector",))),
    ToolSpec("browser_fill", GROUP_BROWSER, NOT_IMPLEMENTED, "Fill a locator with a value; secrets are guarded. Requires the W14 browser runtime; not available in this build.", _schema({"selector": S, "value": S}, ("selector", "value"))),
    ToolSpec("browser_find", GROUP_BROWSER, NOT_IMPLEMENTED, "Find text matches on the current page. Requires the W14 browser runtime; not available in this build.", _schema({"query": S}, ("query",))),
    ToolSpec("browser_get_state", GROUP_BROWSER, NOT_IMPLEMENTED, "Read URL/title/loading state of the current tab. Requires the W14 browser runtime; not available in this build.", _schema({})),
    ToolSpec("computer_find_text", GROUP_BROWSER, NOT_IMPLEMENTED, "OCR text search on a screen region. Requires the W14 computer runtime; not available in this build.", _schema({"query": S, "region": NS}, ("query",))),
    ToolSpec("browser_wait", GROUP_BROWSER, NOT_IMPLEMENTED, "Wait for a condition with a bounded timeout. Requires the W14 browser runtime; not available in this build.", _schema({"condition": S, "timeout_ms": {"type": "integer", "minimum": 100, "maximum": 60000, "default": 5000}}, ("condition",))),
    ToolSpec("browser_press_key", GROUP_BROWSER, NOT_IMPLEMENTED, "Press a key or chord on the current page. Requires the W14 browser runtime; not available in this build.", _schema({"keys": STR_ARRAY}, ("keys",))),
    ToolSpec("browser_scroll", GROUP_BROWSER, NOT_IMPLEMENTED, "Scroll the page a bounded amount. Requires the W14 browser runtime; not available in this build.", _schema({"direction": UP_DOWN, "amount": {"type": "integer", "minimum": 1, "maximum": 100, "default": 3}, "target": NS}, ("direction",))),
    ToolSpec("browser_back_forward", GROUP_BROWSER, NOT_IMPLEMENTED, "Navigate back/forward a bounded number of steps. Requires the W14 browser runtime; not available in this build.", _schema({"direction": {"type": "string", "enum": ["back", "forward"]}, "steps": {"type": "integer", "minimum": 1, "maximum": 10, "default": 1}}, ("direction",))),
    ToolSpec("browser_get_tabs", GROUP_BROWSER, NOT_IMPLEMENTED, "Read tab IDs, titles, URLs, and active state. Requires the W14 browser runtime; not available in this build.", _schema({})),
    # ---- Additional browser/computer support group (4) ----
    ToolSpec("browser_get_accessibility_tree", GROUP_BROWSER, NOT_IMPLEMENTED, "Read a bounded accessibility tree subset. Requires the W14 browser runtime; not available in this build.", _schema({"scope": NS})),
    ToolSpec("browser_upload_download", GROUP_BROWSER, NOT_IMPLEMENTED, "Transfer a file under an allowlist policy. Requires the W14 browser runtime; not available in this build.", _schema({"direction": {"type": "string", "enum": ["upload", "download"]}, "file_ref": S, "target": S, "policy": NS}, ("direction", "file_ref", "target"))),
    ToolSpec("browser_drag_drop", GROUP_BROWSER, NOT_IMPLEMENTED, "Drag from a source to a target. Requires the W14 browser runtime; not available in this build.", _schema({"source": S, "target": S}, ("source", "target"))),
    ToolSpec("browser_wait_for_change", GROUP_BROWSER, NOT_IMPLEMENTED, "Wait for a change from a baseline state with before/after evidence. Requires the W14 browser runtime; not available in this build.", _schema({"baseline": S, "timeout_ms": {"type": "integer", "minimum": 100, "maximum": 60000, "default": 5000}}, ("baseline",))),
)

ROOM_TOOLS = tuple(s.name for s in TOOL_SPECS if s.group == GROUP_ROOM)
SANDBOX_TOOLS = tuple(s.name for s in TOOL_SPECS if s.group == GROUP_SANDBOX)
COMPUTER_TOOLS = tuple(s.name for s in TOOL_SPECS if s.group == GROUP_COMPUTER)
BROWSER_TOOLS = tuple(s.name for s in TOOL_SPECS if s.group == GROUP_BROWSER)
EXPECTED_GROUP_COUNTS = {GROUP_ROOM: 10, GROUP_SANDBOX: 21, GROUP_COMPUTER: 6, GROUP_BROWSER: 17}
EXPECTED_TOTAL = 54

def validate_catalog() -> None:
    names = tuple(spec.name for spec in TOOL_SPECS)
    if len(names) != EXPECTED_TOTAL or len(set(names)) != EXPECTED_TOTAL:
        raise ValueError("catalog must contain exactly 54 unique ordered tool names")
    counts: dict[str, int] = {}
    for spec in TOOL_SPECS:
        if spec.status not in (IMPLEMENTED, NOT_IMPLEMENTED):
            raise ValueError("invalid status: " + spec.name)
        if spec.group not in EXPECTED_GROUP_COUNTS:
            raise ValueError("invalid group: " + spec.name)
        counts[spec.group] = counts.get(spec.group, 0) + 1
        schema = spec.input_schema
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            raise ValueError("invalid tool schema envelope: " + spec.name)
        for key in schema.get("required", []):
            if key not in schema.get("properties", {}):
                raise ValueError("required key missing from properties: " + spec.name + "." + key)
    if counts != EXPECTED_GROUP_COUNTS:
        raise ValueError("group counts do not match the 54-tool catalog: " + repr(counts))

def export_mcp_tools() -> list[dict[str, Any]]:
    validate_catalog()
    return [{"name": s.name, "description": s.description, "inputSchema": s.input_schema} for s in TOOL_SPECS]

def implemented_tool_names() -> tuple[str, ...]:
    return tuple(s.name for s in TOOL_SPECS if s.status == IMPLEMENTED)

def not_implemented_tool_names() -> tuple[str, ...]:
    return tuple(s.name for s in TOOL_SPECS if s.status == NOT_IMPLEMENTED)

def tool_status(name: str) -> dict[str, Any]:
    """Return the declared status for one catalog tool; unknown names fail closed."""
    for spec in TOOL_SPECS:
        if spec.name == name:
            return {
                "name": spec.name,
                "group": spec.group,
                "status": spec.status,
                "catalog_version": CATALOG_VERSION,
            }
    return {
        "name": name,
        "group": None,
        "status": "UNKNOWN_TOOL",
        "catalog_version": CATALOG_VERSION,
    }
