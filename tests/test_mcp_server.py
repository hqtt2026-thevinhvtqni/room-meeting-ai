import asyncio

from mcp import types

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService
from room_hop_mcp.adapter.server import create_server


def _get_tools(server):
    """Call the registered MCP ListTools handler."""
    handler = server.request_handlers[types.ListToolsRequest]
    request = types.ListToolsRequest(method="tools/list")
    return asyncio.run(handler(request))


def _get_call_tool_handler(server):
    """Get the registered MCP CallTool handler."""
    return server.request_handlers[types.CallToolRequest]


def test_add_paste_to_meeting_tool_is_registered(tmp_path):
    """Verify that the MCP write tool is exposed."""
    manager = MeetingManager(tmp_path)
    service = MeetingService(manager)
    server = create_server(service)

    assert types.ListToolsRequest in server.request_handlers


def test_add_paste_to_meeting_tool_schema(tmp_path):
    """Verify the input contract of the MCP write tool."""
    manager = MeetingManager(tmp_path)
    service = MeetingService(manager)
    server = create_server(service)

    result = _get_tools(server)

    tool = next(
        tool
        for tool in result.root.tools
        if tool.name == "add_paste_to_meeting"
    )

    schema = tool.inputSchema

    assert schema["type"] == "object"
    assert schema["properties"]["meeting_id"]["type"] == "string"
    assert schema["properties"]["meeting_id"]["minLength"] == 1
    assert schema["properties"]["text"]["type"] == "string"
    assert schema["required"] == ["meeting_id", "text"]
    assert schema["additionalProperties"] is False


def test_add_paste_delegates_to_service(tmp_path):
    """Verify delegation to MeetingService.add_paste()."""

    class FakeService:
        def __init__(self):
            self.calls = []

        def add_paste(self, meeting_id, raw_text):
            self.calls.append((meeting_id, raw_text))
            return {"accepted": True}

    service = FakeService()
    server = create_server(service)

    handler = _get_call_tool_handler(server)

    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="add_paste_to_meeting",
            arguments={
                "meeting_id": "MEETING-TEST-001",
                "text": "Hello ROOM HOP",
            },
        ),
    )

    result = asyncio.run(handler(request))

    assert service.calls == [
        ("MEETING-TEST-001", "Hello ROOM HOP")
    ]

    assert result.root.structuredContent == {
        "paste": {
            "accepted": True
        }
    }


def test_add_paste_rejects_missing_meeting_id(tmp_path):
    """Verify missing meeting_id is rejected by MCP input validation."""
    manager = MeetingManager(tmp_path)
    service = MeetingService(manager)
    server = create_server(service)

    handler = _get_call_tool_handler(server)

    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="add_paste_to_meeting",
            arguments={
                "text": "Hello ROOM HOP",
            },
        ),
    )

    result = asyncio.run(handler(request))

    assert result.root.isError is True
    assert "meeting_id" in result.root.content[0].text


def test_add_paste_rejects_missing_text(tmp_path):
    """Verify missing text is rejected by MCP input validation."""
    manager = MeetingManager(tmp_path)
    service = MeetingService(manager)
    server = create_server(service)

    handler = _get_call_tool_handler(server)

    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="add_paste_to_meeting",
            arguments={
                "meeting_id": "MEETING-TEST-001",
            },
        ),
    )

    result = asyncio.run(handler(request))

    assert result.root.isError is True
    assert "text" in result.root.content[0].text


def test_add_paste_returns_service_result(tmp_path):
    """Verify the MCP adapter returns the service result."""

    class FakeService:
        def add_paste(self, meeting_id, raw_text):
            return {
                "meeting_id": meeting_id,
                "accepted": True,
                "bytes": len(raw_text.encode("utf-8")),
            }

    service = FakeService()
    server = create_server(service)

    handler = _get_call_tool_handler(server)

    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="add_paste_to_meeting",
            arguments={
                "meeting_id": "MEETING-TEST-001",
                "text": "Hello ROOM HOP",
            },
        ),
    )

    result = asyncio.run(handler(request))

    assert result.root.isError is False
    assert result.root.structuredContent == {
        "paste": {
            "meeting_id": "MEETING-TEST-001",
            "accepted": True,
            "bytes": len("Hello ROOM HOP".encode("utf-8")),
        }
    }


def test_add_paste_handles_core_error(tmp_path):
    """Verify Core/service errors are handled at the MCP boundary."""

    class FakeService:
        def add_paste(self, meeting_id, raw_text):
            raise RuntimeError("meeting is not active")

    service = FakeService()
    server = create_server(service)

    handler = _get_call_tool_handler(server)

    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="add_paste_to_meeting",
            arguments={
                "meeting_id": "MEETING-TEST-001",
                "text": "Hello ROOM HOP",
            },
        ),
    )

    result = asyncio.run(handler(request))

    assert result.root.isError is True
    assert len(result.root.content) > 0
    assert "meeting is not active" in result.root.content[0].text
