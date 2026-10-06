"""ROOM HOP MCP Server — stdio transport for POC."""
import logging
import os
from mcp.server.fastmcp import FastMCP

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("ROOM_HOP_MCP_Server")

# Identity propagation: deployment MUST provide the requester identity.
# Never silently authenticate an MCP caller as Vinh.
MCP_REQUESTER_IDENTITY = os.getenv("MCP_REQUESTER_IDENTITY")
if not MCP_REQUESTER_IDENTITY:
    raise RuntimeError(
        "MCP_REQUESTER_IDENTITY is required; refusing to start without caller identity."
    )

manager = MeetingManager()
service = MeetingService(
    manager=manager,
    requester_identity=MCP_REQUESTER_IDENTITY,
)

from .tools.meetings import register_meeting_tools
register_meeting_tools(mcp, service)

if __name__ == "__main__":
    mcp.run(transport="stdio")
