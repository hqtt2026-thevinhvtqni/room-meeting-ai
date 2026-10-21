"""Work 28 unified MCP :8020 registry: 18 legacy operations + 3 read-only GitHub tools.

Prepared contract only; this does not prove live registration. Core remains the
authorization authority. Caller-supplied identity fields are not proof of authority.
"""
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
EXTENSION_9 = (
    "execution_submit", "execution_status", "execution_output_read",
    "sandbox_search", "sandbox_stat", "sandbox_read_range",
    "github_create_branch", "github_create_file", "github_update_file",
)
EXPECTED_TOOL_NAMES = LEGACY_18 + GITHUB_3 + EXTENSION_9

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
    ToolSpec("list_meetings", "List meetings available through ROOM-HOP.", "core", "list_meetings", _schema({})),
    ToolSpec("get_meeting", "Read a detached DTO for one meeting.", "core", "get_meeting", _schema(MEETING, ("meeting_id",))),
    ToolSpec("get_transcript", "Read transcript evidence for one meeting.", "core", "get_transcript", _schema(MEETING, ("meeting_id",))),
    ToolSpec("join_meeting", "Join a meeting as an identity validated by the trusted service.", "core", "join_meeting", _schema({"meeting_id": S, "identity_id": S}, ("meeting_id", "identity_id"))),
    ToolSpec("start_meeting", "Start a meeting as an explicit starter identity.", "core", "start_meeting", _schema({"meeting_id": S, "starter": S}, ("meeting_id", "starter"))),
    ToolSpec("add_paste_to_meeting", "Append raw text to an active meeting.", "core", "add_paste_to_meeting", _schema({"meeting_id": S, "text": S, "identity_id": {"type": ["string", "null"]}}, ("meeting_id", "text"))),
    ToolSpec("sandbox_create_work", "Create a Work Sandbox after caller identity validation.", "sandbox", "sandbox_create_work", _schema({"work_id": S, "work_name": S, "identity_id": S}, ("work_id", "work_name", "identity_id"))),
    ToolSpec("sandbox_list_works", "Discover Work Sandboxes and manifest metadata.", "sandbox", "sandbox_list_works", _schema({})),
    ToolSpec("sandbox_list", "List files and directories inside a Work Sandbox.", "sandbox", "sandbox_list", _schema({"work_id": S}, ("work_id",))),
    ToolSpec("get_room_structure", "Read the published MAIN SOURCE structure for orientation.", "core", "get_room_structure", _schema({})),
    ToolSpec("get_room_context", "Read current architecture and build rules for orientation.", "core", "get_room_context", _schema({})),
    ToolSpec("sandbox_read", "Read a UTF-8 text file inside the specified Work Sandbox.", "sandbox", "sandbox_read", _schema(WORK_PATH, ("work_id", "relative_path"))),
    ToolSpec("sandbox_create", "Create a text file inside a Work Sandbox; content defaults to empty.", "sandbox", "sandbox_create", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path"))),
    ToolSpec("sandbox_write", "Create or overwrite a text file inside a Work Sandbox.", "sandbox", "sandbox_write", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path", "content"))),
    ToolSpec("sandbox_append", "Append text to a Work artifact.", "sandbox", "sandbox_append", _schema({**WORK_PATH, "content": S}, ("work_id", "relative_path", "content"))),
    ToolSpec("sandbox_delete", "Delete a file inside a Work Sandbox after policy checks.", "sandbox", "sandbox_delete", _schema(WORK_PATH, ("work_id", "relative_path"))),
    ToolSpec("get_pending_tasks", "List pending tasks for one identity; default limit is 20.", "core", "get_pending_tasks", _schema({"identity_id": S, "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}}, ("identity_id",))),
    ToolSpec("submit_proposal", "Submit a task reply through Proposal Gate and Core Message Gate.", "proposal", "submit_proposal", _schema({"identity_id": S, "meeting_id": S, "trigger_message_id": S, "agent_id": S, "proposal_id": S, "content": S}, ("identity_id", "meeting_id", "trigger_message_id", "agent_id", "proposal_id", "content"))),
    ToolSpec("github_repository", "Read repository metadata through the authenticated GitHub provider.", "github", "github_repository", _schema({"repository": S}, ("repository",))),
    ToolSpec("github_read_file", "Read a repository file at an explicit branch, tag, or commit ref.", "github", "github_read_file", _schema({"repository": S, "path": S, "ref": S}, ("repository", "path", "ref"))),
    ToolSpec("github_search_files", "Search repository files at an explicit ref with a bounded result limit; default limit is 20.", "github", "github_search_files", _schema({"repository": S, "query": S, "ref": S, "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}}, ("repository", "query", "ref"))),
    ToolSpec("execution_submit", "Submit a bounded RUN_TESTS or RUN_SCRIPT request through authenticated Core; never accepts shell commands.", "runtime", "execution_submit", _schema({"request": {"type": "object", "properties": {"work_id": S, "operation": {"type": "string", "enum": ["RUN_TESTS", "RUN_SCRIPT"]}, "source_sha256": {"type": "string", "minLength": 64, "maxLength": 64}, "profile_id": S, "request_id": S}, "required": ["work_id", "operation", "source_sha256", "profile_id", "request_id"], "additionalProperties": False}}, ("request",))),
    ToolSpec("execution_status", "Read execution status through authenticated Core using a run ID.", "runtime", "execution_status", _schema({"run_id": S}, ("run_id",))),
    ToolSpec("execution_output_read", "Read bounded stdout, stderr, or combined output for a run through authenticated Core.", "runtime", "execution_output_read", _schema({"run_id": S, "stream": {"type": "string", "enum": ["stdout", "stderr", "combined"], "default": "combined"}, "max_bytes": {"type": "integer", "minimum": 1, "maximum": 16384, "default": 16384}}, ("run_id",))),
    ToolSpec("sandbox_search", "Search filenames/content within one authorized Work Sandbox with a bounded result count.", "sandbox_extension", "sandbox_search", _schema({"work_id": S, "query": S, "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}}, ("work_id", "query"))),
    ToolSpec("sandbox_stat", "Read metadata for a Work-relative Sandbox path.", "sandbox_extension", "sandbox_stat", _schema({"work_id": S, "path": S}, ("work_id", "path"))),
    ToolSpec("sandbox_read_range", "Read a bounded byte range from a text artifact in an authorized Work Sandbox.", "sandbox_extension", "sandbox_read_range", _schema({"work_id": S, "path": S, "offset": {"type": "integer", "minimum": 0, "default": 0}, "length": {"type": "integer", "minimum": 1, "maximum": 65536, "default": 16384}}, ("work_id", "path"))),
    ToolSpec("github_create_branch", "Create a non-default GitHub branch from an explicit base ref.", "github", "github_create_branch", _schema({"repository": S, "branch": S, "base_ref": {"type": "string", "default": "main"}}, ("repository", "branch"))),
    ToolSpec("github_create_file", "Create a new file on a non-default branch; fails if the path already exists.", "github", "github_create_file", _schema({"repository": S, "branch": S, "path": S, "content": S, "message": S}, ("repository", "branch", "path", "content", "message"))),
    ToolSpec("github_update_file", "Update an existing file on a non-default branch using an expected blob SHA to prevent stale writes.", "github", "github_update_file", _schema({"repository": S, "branch": S, "path": S, "content": S, "message": S, "expected_blob_sha": {"type": "string", "pattern": "^[0-9a-fA-F]{40}$"}}, ("repository", "branch", "path", "content", "message", "expected_blob_sha"))),
)

def validate_registry() -> None:
    names = tuple(spec.name for spec in TOOL_SPECS)
    if names != EXPECTED_TOOL_NAMES or len(set(names)) != len(names):
        raise ValueError("unified registry must contain the exact 30 unique ordered tool names")
    for spec in TOOL_SPECS:
        if spec.boundary not in {"core", "sandbox", "sandbox_extension", "proposal", "github", "runtime"} or spec.input_schema.get("type") != "object":
            raise ValueError(f"invalid tool contract: {spec.name}")

def export_mcp_tools() -> list[dict[str, Any]]:
    validate_registry()
    return [{"name": s.name, "description": s.description, "inputSchema": s.input_schema} for s in TOOL_SPECS]
