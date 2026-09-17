"""
ROOM HOP Integration â€” Contract #1 (Option C: MCP Client Session).

Scope, per Contract #1 (LOCKED):
    Integration
        -> MCP Client Session
        -> stdio
        -> ROOM HOP MCP Server (Public V1, room_hop_mcp/adapter/server.py)
        -> MeetingService
        -> Core

This module is the ONLY thing in the stack allowed to speak the MCP
protocol on behalf of a Dashboard. It does not import anything from
core.* or room_hop_mcp.adapter.* directly â€” it only talks to the
already-running Public V1 boundary as a client, over stdio, exactly the
same way any other MCP client would.

Hard boundary (do not cross without a new Gate):
    - No import of core.meeting_manager / core.meeting_service / any
      Core module. Integration does not know Core exists.
    - No filesystem access to meetings/*.yaml, transcript.txt, etc.
    - No new capability beyond the 4 locked in Contract #1:
          list_meetings, get_meeting, get_transcript, add_paste_to_meeting
    - No business logic: no retries with domain meaning, no caching that
      changes what a caller sees, no inference of meeting state, no
      default values invented for missing fields. This module's only job
      is session/transport management and DTO passthrough/translation of
      what Public V1 already returns.
    - Errors from Public V1 (tool-level `isError`) are surfaced as
      IntegrationError with the server's own message, unchanged. This
      module does not invent new error semantics.
"""

from __future__ import annotations

import json
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

LIST_MEETINGS = "list_meetings"
GET_MEETING = "get_meeting"
GET_TRANSCRIPT = "get_transcript"
JOIN_MEETING = "join_meeting"
ADD_PASTE_TO_MEETING = "add_paste_to_meeting"

_REQUIRED_TOOLS = {LIST_MEETINGS, GET_MEETING, GET_TRANSCRIPT, JOIN_MEETING, ADD_PASTE_TO_MEETING}


class IntegrationError(RuntimeError):
    """
    Raised when the Public V1 MCP boundary returns a tool-level error, or
    when the MCP transport itself fails (session/process/protocol level).

    The message is passed through unchanged from Public V1 where possible
    â€” Integration does not reclassify or reword domain errors from Core.
    """


@dataclass(frozen=True)
class RoomHopIntegrationConfig:
    """Connection config for the Public V1 stdio MCP server."""

    python_executable: str = sys.executable
    module: str = "room_hop_mcp"
    cwd: str | None = None  # must be the room-meeting-ai project root
    env: dict[str, str] | None = None


class RoomHopIntegration:
    """
    Thin MCP client wrapper over Public V1's 4 locked tools.

    Usage:

        integration = RoomHopIntegration(RoomHopIntegrationConfig(cwd="."))

        async with integration.session() as session:
            meetings = await integration.list_meetings(session)
            meeting = await integration.get_meeting(session, meetings[0]["id"])

    Each method is a 1:1 passthrough to one Public V1 tool call. No method
    combines multiple tool calls or adds interpretation on top of what
    Public V1 returns.
    """

    def __init__(self, config: RoomHopIntegrationConfig | None = None) -> None:
        self._config = config or RoomHopIntegrationConfig()

    def _server_params(self) -> StdioServerParameters:
        return StdioServerParameters(
            command=self._config.python_executable,
            args=["-m", self._config.module],
            env=self._config.env,
            cwd=self._config.cwd,
        )

    @staticmethod
    def _first_leaf(exc: BaseException) -> BaseException:
        """
        anyio's TaskGroup (used internally by both stdio_client and
        ClientSession) wraps any exception raised during teardown in a
        BaseExceptionGroup â€” and does so again at each nested `async with`
        boundary it passes through. Drill down to the original leaf
        exception so callers see the real message, not a nesting artifact.
        """
        seen = exc
        while isinstance(seen, BaseExceptionGroup) and seen.exceptions:
            seen = seen.exceptions[0]
        return seen

    @asynccontextmanager
    async def session(self) -> AsyncIterator[ClientSession]:
        """
        Open one MCP client session against Public V1 over stdio.

        Spawns `python -m room_hop_mcp` as a subprocess (the same
        entrypoint room_hop_mcp/__main__.py already defines) and performs
        the MCP initialize handshake. The caller is responsible for
        issuing tool calls within the `async with` block; the session
        (and subprocess) is torn down on exit.

        Error evidence: an IntegrationError raised by caller code inside
        the `async with` block (e.g. from _unwrap on a tool-level error)
        must surface with its original message unchanged â€” even though
        the underlying anyio TaskGroups used by ClientSession/stdio_client
        wrap it in a BaseExceptionGroup at every nested boundary during
        teardown. Only a genuine transport/session failure (subprocess
        spawn, handshake, protocol) gets the generic "MCP transport
        failure" wrapping.
        """
        try:
            async with stdio_client(self._server_params()) as (read, write):
                async with ClientSession(read, write) as mcp_session:
                    await mcp_session.initialize()
                    yield mcp_session
        except IntegrationError:
            raise
        except BaseExceptionGroup as eg:
            leaf = self._first_leaf(eg)
            if isinstance(leaf, IntegrationError):
                raise leaf from None
            raise IntegrationError(
                f"MCP transport failure: {type(leaf).__name__}: {leaf}"
            ) from leaf
        except Exception as exc:  # noqa: BLE001
            raise IntegrationError(
                f"MCP transport failure: {type(exc).__name__}: {exc}"
            ) from exc

    async def verify_capabilities(self, mcp_session: ClientSession) -> None:
        """
        Confirm the connected Public V1 server exposes exactly the 4
        Contract #1 tools this Integration depends on. Raises
        IntegrationError if the boundary has drifted from what was
        proven in Gate #3-VERIFY. Does not check for absence of extra
        tools â€” only that the required 4 are present.
        """
        tools_result = await mcp_session.list_tools()
        names = {t.name for t in tools_result.tools}
        missing = _REQUIRED_TOOLS - names
        if missing:
            raise IntegrationError(
                f"Public V1 is missing required Contract #1 tool(s): {sorted(missing)}"
            )

    @staticmethod
    def _unwrap(result: Any, key: str) -> Any:
        """
        Parse a CallToolResult's text content as JSON and return the
        Public V1 DTO under `key`, unchanged. Raises IntegrationError on
        tool-level errors or malformed responses â€” never silently
        returns a default.
        """
        if getattr(result, "isError", False):
            detail = ""
            if result.content:
                first = result.content[0]
                detail = getattr(first, "text", "") or ""
            raise IntegrationError(detail or "Public V1 returned an error")

        if not result.content:
            raise IntegrationError("Public V1 returned an empty result")

        text = getattr(result.content[0], "text", None)
        if text is None:
            raise IntegrationError("Public V1 returned a non-text result")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise IntegrationError(
                f"Public V1 returned malformed JSON: {exc}"
            ) from exc

        if key not in data:
            raise IntegrationError(
                f"Public V1 response missing expected key '{key}': {data}"
            )

        return data[key]

    # -- Contract #1 capabilities -------------------------------------

    async def list_meetings(self, mcp_session: ClientSession) -> list[dict[str, Any]]:
        """READ. Returns Public V1's list_meetings DTO, unchanged."""
        result = await mcp_session.call_tool(LIST_MEETINGS, {})
        return self._unwrap(result, "meetings")

    async def get_meeting(
        self, mcp_session: ClientSession, meeting_id: str
    ) -> dict[str, Any]:
        """READ. Returns Public V1's get_meeting DTO, unchanged."""
        result = await mcp_session.call_tool(
            GET_MEETING, {"meeting_id": meeting_id}
        )
        return self._unwrap(result, "meeting")

    async def get_transcript(
        self, mcp_session: ClientSession, meeting_id: str
    ) -> list[dict[str, Any]]:
        """READ. Returns Public V1's get_transcript DTO, unchanged."""
        result = await mcp_session.call_tool(
            GET_TRANSCRIPT, {"meeting_id": meeting_id}
        )
        return self._unwrap(result, "transcript")

    async def join_meeting(
        self,
        mcp_session: ClientSession,
        meeting_id: str,
        identity_id: str,
    ) -> dict[str, Any]:
        """PARTICIPATE. Returns Public V1's join_meeting DTO, unchanged."""
        result = await mcp_session.call_tool(
            JOIN_MEETING,
            {"meeting_id": meeting_id, "identity_id": identity_id},
        )
        return self._unwrap(result, "meeting")
    async def add_paste_to_meeting(
        self, mcp_session: ClientSession, meeting_id: str, text: str, identity_id: str | None = None
    ) -> dict[str, Any]:
        """
        RECORDING. Returns Public V1's add_paste_to_meeting DTO, unchanged.

        Core's own validation (meeting must be 'active', etc.) is what
        decides success/failure here â€” Integration does not pre-check or
        second-guess meeting state before calling.
        """
        result = await mcp_session.call_tool(
            ADD_PASTE_TO_MEETING,
            {"meeting_id": meeting_id, "text": text, **({"identity_id": identity_id} if identity_id is not None else {})},
        )
        return self._unwrap(result, "paste")


__all__ = [
    "RoomHopIntegration",
    "RoomHopIntegrationConfig",
    "IntegrationError",
]
