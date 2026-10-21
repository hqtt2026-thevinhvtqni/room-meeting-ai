"""Work 28 unified MCP :8020 registry: 18 legacy operations + 3 read-only GitHub tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

CONTRACT_VERSION = "1.0.0"
LEGACY_18 = (
    "list_meetings", "get_meeting", "get_transcript", "join_meeting",
    "start_meeting", "add_paste_to_meeting", "sandbox_create_work",
    "sandbox_list_works", "sandbox_list", "get_room_structure",
    "get_room_context", "sandbox_read", "sandbox_create", "sandbox_write",
    "sandbox_append", "sandbox_delete", "get_pending_tasks", "submit_proposal",
)
GITHUB_3 = ("github_repository", "github_read_file", "github_search_files")
EXPECTED_TOOL_NAMES = LEGACY_18 + GITHUB_3

@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    boundary: str
    handler: str
    input_schema: dict[str, Any]

def _schema(properties: dict[str, Any], required: tuple[str, ...] = ()) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": list(required), "additionalProperties": False}

S = {"type": "string"}
MEETING = {"meeting_id": S}
WORK_PATH = {"work_id": S, "relative_path": S}
TOOL_SPECS = (
    ToolSpec("list_meetings", "List meetings visible to the authenticated principal.", "core", "list_meetings", _schema({})),
    ToolSpec("get_meeting", "Read one authorized meeting.", "core", "get_meeting", _schema(MEETING, ("meeting_id",))),
    ToolSpec("get_transcript", "Read transcript for one authorized meeting.", "core", "get_transcript", _schema(MEETING, ("meeting_id",))),
    ToolSpec("join_meeting", "Join a meeting using a server-validated identity.", "core", "join_meeting", _schema({"meeting_id": S, "identity_id": S}, ("meeting_id", "identity_id"))),
    ToolSpec("start_meeting", "Start a meeting using a server-validated starter identity.", "core", "start_meeting", _schema({"meeting_id": S, "starter": S}, ("meeting_id", "starter"))),
    ToolSpec("add_paste_to_meeting", "Add supplied text to an authorized meeting.", "core", "add_paste_to_meeting", _schema({"meeting_id": S, "content": S}, ("meeting_id", "content"))),
    ToolSpec("sandbox_create_work", "Create a Work Sandbox after Core authorization.", "sandbox", "sandbox_create_work", _schema({"work_id": S, "work_name": S}, ("work_id", "work_name"))),
    ToolSpec("sandbox_list_works", "List Work Sandboxes visible to the authenticated principal.", "sandbox", "sandbox_list_works", _schema({})),
    ToolSpec("sandbox_list", "List entries inside an authorized Work-relative directory.", "sandbox", "sandbox_list", _schema({"work_id": S, "relative_path": S}, ("work_id", "relative_path"))),
    ToolSpec("get_room_structure", "Read the published ROOM-HOP structure.", "core", "get_room_structure", _schema({})),
    ToolSpec("get_room_context", "Read the authorized room context.", "core", "get_room_context", _schema({})),
    ToolSpec("sandbox_read", "Read a UTF-8 text file within the specified Work Sandbox.", "sandbox", "sandbox_read", _schema(WORK_PATH, ("work_id", "relative_path"))),
    ToolSpec("sandbox_create", "Create a new text file within the specified Work Sandbox.", "sandbox", "sandbox_create", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path"))),
    ToolSpec("sandbox_write", "Write a text file within the specified Work Sandbox.", "sandbox", "sandbox_write", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path", "content"))),
    ToolSpec("sandbox_append", "Append text to an authorized Work artifact.", "sandbox", "sandbox_append", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path", "content"))),
    ToolSpec("sandbox_delete", "Delete an authorized Work-relative artifact after Core policy checks.", "sandbox", "sandbox_delete", _schema(WORK_PATH, ("work_id", "relative_path"))),
    ToolSpec("get_pending_tasks", "Read pending tasks for the authenticated agent.", "core", "get_pending_tasks", _schema({"identity_id": S, "limit": {"type": "integer", "minimum": 1, "maximum": 100}}, ("identity_id",))),
    ToolSpec("submit_proposal", "Submit a proposal through the authorized proposal gate.", "proposal", "submit_proposal", _schema({"identity_id": S, "meeting_id": S, "trigger_message_id": S, "agent_id": S, "proposal_id": S, "content": S}, ("identity_id", "meeting_id", "trigger_message_id", "agent_id", "proposal_id", "content"))),
    ToolSpec("github_repository", "Read repository metadata through the authenticated GitHub provider.", "github", "github_repository", _schema({"repository": S}, ("repository",))),
    ToolSpec("github_read_file", "Read a repository file at an explicit branch, tag, or commit ref.", "github", "github_read_file", _schema({"repository": S, "path": S, "ref": S}, ("repository", "path", "ref"))),
    ToolSpec("github_search_files", "Search repository files at an explicit ref with a bounded result limit.", "github", "github_search_files", _schema({"repository": S, "query": S, "ref": S, "limit": {"type": "integer", "minimum": 1, "maximum": 100}}, ("repository", "query", "ref"))),
)

def validate_registry() -> None:
    names = tuple(spec.name for spec in TOOL_SPECS)
    if names != EXPECTED_TOOL_NAMES or len(set(names)) != len(names):
        raise ValueError("unified registry must contain the exact 21 unique ordered tool names")
    for spec in TOOL_SPECS:
        if spec.boundary not in {"core", "sandbox", "proposal", "github"} or spec.input_schema.get("type") != "object":
            raise ValueError(f"invalid tool contract: {spec.name}")

def export_mcp_tools() -> list[dict[str, Any]]:
    validate_registry()
    return [{"name": s.name, "description": s.description, "inputSchema": s.input_schema} for s in TOOL_SPECS]
