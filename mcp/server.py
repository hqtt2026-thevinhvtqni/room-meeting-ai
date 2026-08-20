"""ROOM HOP MCP Server — stdio transport for POC."""
import logging
import os
from mcp.server.fastmcp import FastMCP

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo MCP Server
mcp = FastMCP("ROOM_HOP_MCP_Server")

# Identity propagation: lấy từ env, không hard-code
MCP_REQUESTER_IDENTITY = os.getenv("MCP_REQUESTER_IDENTITY", "vinh")
# Trong production, env var này sẽ được set bởi deployment config
# POC dùng "vinh" làm fallback, nhưng không hard-code trong Service

# Khởi tạo Core components
manager = MeetingManager()
service = MeetingService(
    manager=manager,
    requester_identity=MCP_REQUESTER_IDENTITY,
)

# Register tools
from .tools.meetings import register_meeting_tools
register_meeting_tools(mcp, service)

if __name__ == "__main__":
    mcp.run(transport='stdio')
