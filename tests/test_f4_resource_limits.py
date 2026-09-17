"""
F4 Resource Limits — Dedicated Design/Baseline Tests.

IMPORTANT
---------
These tests inspect the current resource-boundary behavior.

They do NOT modify production code.

F4 policy under test:
    MAX_TEXT_BYTES = 1 MiB

Expected at this stage:
    Some tests SHOULD FAIL because the resource limits have not been
    implemented yet.

That FAIL is evidence for the F4 implementation round.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.meeting_manager import MeetingError, MeetingManager
from core.meeting_service import MeetingService
from core.secretary import Secretary


MAX_TEXT_BYTES = 1 * 1024 * 1024


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def make_secretary(tmp_path: Path) -> Secretary:
    return Secretary(
        transcript_path=tmp_path / "transcript.txt",
    )


def make_service(tmp_path: Path) -> tuple[MeetingService, str]:
    """
    Build a real Core MeetingService and move a meeting to ACTIVE.
    """
    # MeetingManager expects meetings_dir as keyword argument
    manager = MeetingManager(meetings_dir=tmp_path / "meetings")
    service = MeetingService(manager)

    meeting_id = "F4-RESOURCE-001"

    # Create meeting with 3 participants.
    # Vinh is included because Vinh is the STARTER.
    service.create_meeting(
        meeting_id=meeting_id,
        topic="F4 Resource Limits",
        participants=["vinh", "xu", "claude"],
        context_files=[],
        created_by="vinh",
    )

    # Open session
    service.open_meeting(meeting_id)

    # All participants must JOIN_ACCEPTED before START.
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, "xu")
    service.join_meeting(meeting_id, "claude")

    # START with vinh as starter.
    service.start_meeting(meeting_id, "vinh")

    return service, meeting_id


# ---------------------------------------------------------------------------
# F4.1 Secretary input-size boundary
# ---------------------------------------------------------------------------


class TestF4SecretaryInputLimit:
    def test_exact_limit_is_accepted(self, tmp_path):
        secretary = make_secretary(tmp_path)

        text = "A" * MAX_TEXT_BYTES

        result = secretary.append(text)

        assert result["status"] == "READY"
        assert secretary.read() == text

    def test_over_limit_is_rejected(self, tmp_path):
        secretary = make_secretary(tmp_path)

        oversized = "A" * (MAX_TEXT_BYTES + 1)

        with pytest.raises(
            (ValueError, OverflowError, MemoryError)
        ):
            secretary.append(oversized)

        assert secretary.read() == ""

    def test_over_limit_is_rejected_by_utf8_bytes(self, tmp_path):
        secretary = make_secretary(tmp_path)

        character = "😀"
        character_bytes = len(character.encode("utf-8"))

        repetitions = (MAX_TEXT_BYTES // character_bytes) + 1
        oversized = character * repetitions

        assert len(oversized.encode("utf-8")) > MAX_TEXT_BYTES

        with pytest.raises(
            (ValueError, OverflowError, MemoryError)
        ):
            secretary.append(oversized)

        assert secretary.read() == ""

    def test_oversized_input_does_not_partially_write(
        self,
        tmp_path,
    ):
        secretary = make_secretary(tmp_path)

        valid = "VALID\n"
        oversized = "B" * (MAX_TEXT_BYTES + 1)

        secretary.append(valid)

        with pytest.raises(
            (ValueError, OverflowError, MemoryError)
        ):
            secretary.append(oversized)

        assert secretary.read() == valid


# ---------------------------------------------------------------------------
# F4.2 MeetingService / Core public boundary
# ---------------------------------------------------------------------------


class TestF4MeetingServiceInputLimit:
    def test_service_rejects_oversized_paste(self, tmp_path):
        service, meeting_id = make_service(tmp_path)

        oversized = "X" * (MAX_TEXT_BYTES + 1)

        with pytest.raises(
            (
                ValueError,
                OverflowError,
                MemoryError,
                MeetingError,
            )
        ):
            service.add_paste(
                meeting_id,
                oversized,
            )

    def test_service_does_not_partially_write_oversized_paste(
        self,
        tmp_path,
    ):
        service, meeting_id = make_service(tmp_path)

        before = service.get_transcript(meeting_id)

        oversized = "Y" * (MAX_TEXT_BYTES + 1)

        with pytest.raises(
            (
                ValueError,
                OverflowError,
                MemoryError,
                MeetingError,
            )
        ):
            service.add_paste(
                meeting_id,
                oversized,
            )

        after = service.get_transcript(meeting_id)

        assert after == before


# ---------------------------------------------------------------------------
# F4.3 MCP schema/resource-boundary inspection
# ---------------------------------------------------------------------------


class TestF4MCPBoundary:
    def test_add_paste_schema_declares_maximum_length(
        self,
        tmp_path,
    ):
        """
        MCP public schema should expose a maximum text length.

        This is a DESIGN test. It is expected to FAIL until maxLength is
        deliberately added to the public MCP schema.
        """
        from room_hop_mcp.adapter.server import (
            ADD_PASTE_TO_MEETING,
            create_server,
        )

        service, _ = make_service(tmp_path)
        server = create_server(service)

        from mcp import types

        handler = server.request_handlers[types.ListToolsRequest]
        request = types.ListToolsRequest(method="tools/list")

        import asyncio
        result = asyncio.run(handler(request))

        tool = next(
            tool
            for tool in result.root.tools
            if tool.name == ADD_PASTE_TO_MEETING
        )

        text_schema = tool.inputSchema["properties"]["text"]

        assert text_schema.get("maxLength") is not None
        assert text_schema["maxLength"] > 0

    def test_add_paste_schema_limit_matches_f4_policy(
        self,
        tmp_path,
    ):
        """
        Once declared, MCP maxLength must equal the F4 policy.

        NOTE:
        JSON Schema maxLength is character-based, while F4 runtime policy
        is byte-based. Therefore this test is primarily a declaration check,
        not the final UTF-8 enforcement mechanism.
        """
        from room_hop_mcp.adapter.server import (
            ADD_PASTE_TO_MEETING,
            create_server,
        )

        service, _ = make_service(tmp_path)
        server = create_server(service)

        from mcp import types

        handler = server.request_handlers[types.ListToolsRequest]
        request = types.ListToolsRequest(method="tools/list")

        import asyncio
        result = asyncio.run(handler(request))

        tool = next(
            tool
            for tool in result.root.tools
            if tool.name == ADD_PASTE_TO_MEETING
        )

        text_schema = tool.inputSchema["properties"]["text"]

        assert text_schema.get("maxLength") == MAX_TEXT_BYTES


# ---------------------------------------------------------------------------
# F4.4 Repeated-request / rate policy
# ---------------------------------------------------------------------------


class TestF4RatePolicy:
    def test_rate_policy_is_explicitly_declared(self):
        """
        F4 requires an explicit repeated-request policy.

        This intentionally fails until the project declares a real policy.

        No production behavior is assumed here.
        """
        candidates = (
            "MAX_PASTE_REQUESTS",
            "MAX_PASTE_REQUESTS_PER_WINDOW",
            "PASTE_RATE_LIMIT",
            "RATE_LIMIT",
        )

        modules = (
            "core.secretary",
            "core.meeting_manager",
            "core.meeting_service",
            "room_hop_mcp.adapter.server",
        )

        found = []

        for module_name in modules:
            try:
                module = __import__(
                    module_name,
                    fromlist=["*"],
                )
            except Exception:
                continue

            for candidate in candidates:
                if hasattr(module, candidate):
                    found.append(
                        f"{module_name}.{candidate}"
                    )

        assert found, (
            "No explicit F4 rate/repeated-request policy is declared yet."
        )

    def test_repeated_valid_appends_are_exact(self, tmp_path):
        """
        Baseline integrity only.

        This does NOT claim rate limiting.
        """
        secretary = make_secretary(tmp_path)

        blocks = [
            "A\n",
            "B\n",
            "C\n",
            "D\n",
            "E\n",
        ]

        for block in blocks:
            result = secretary.append(block)
            assert result["status"] == "READY"

        assert secretary.read() == "".join(blocks)

    def test_many_small_appends_do_not_duplicate_content(
        self,
        tmp_path,
    ):
        """
        Baseline resource-integrity test.

        This does NOT prove a rate guard.
        """
        secretary = make_secretary(tmp_path)

        block = "ROOM-HOP-F4\n"
        repetitions = 100

        for _ in range(repetitions):
            secretary.append(block)

        assert secretary.read() == block * repetitions


# ---------------------------------------------------------------------------
# F4.5 Explicit policy sanity
# ---------------------------------------------------------------------------


class TestF4PolicyDefinition:
    def test_policy_is_positive(self):
        assert isinstance(MAX_TEXT_BYTES, int)
        assert MAX_TEXT_BYTES > 0

    def test_policy_is_one_megabyte(self):
        assert MAX_TEXT_BYTES == 1024 * 1024

    def test_utf8_is_measured_in_bytes(self):
        text = "😀"

        assert len(text) == 1
        assert len(text.encode("utf-8")) == 4