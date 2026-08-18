"""
Discussion Engine — ROOM HOP v0.2

Chốt của Xu:
  - Agent TỰ QUYẾT ĐỊNH mỗi lượt: REPLY / PASS / FINAL.
  - Room (không phải agent) giữ quyền DỪNG cuộc thảo luận:
      MAX_ROUNDS           — chặn thảo luận vô hạn
      MAX_CONSECUTIVE_PASS — chặn hai bên im lặng nhìn nhau
  - FINAL từ agent -> dừng ngay, chuyển sang tổng hợp.
  - Agent có quyền ĐỀ NGHỊ dừng (FINAL). Room có quyền ÉP dừng (guard).

Không đổi Meeting Manager / Agent Registry / Context Loader / Meeting Log.
Discussion Engine chỉ ĐIỀU PHỐI, gọi các module đó qua interface có sẵn.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.agent_registry import AgentRegistry
from core.connectors import (
    AgentConnector,
    ConnectorError,
    MeetingContextForAgent,
    TurnStatus,
)
from core.meeting_manager import Meeting

DEFAULT_MAX_ROUNDS = 10
DEFAULT_MAX_CONSECUTIVE_PASS = 2


@dataclass
class DiscussionResult:
    stop_reason: str          # "final" | "consecutive_pass" | "max_rounds" | "connector_error"
    rounds_used: int


def _read_context_text(meeting: Meeting) -> str:
    """Ghép nội dung mọi file context đã đóng gói cho meeting này thành 1 khối text."""
    context_dir = meeting.meeting_dir / "context"
    parts = []
    for path in sorted(context_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        parts.append(f"### {path.name}\n{content or '(file rỗng)'}")
    return "\n\n".join(parts)


def _build_history(meeting: Meeting) -> list[dict]:
    return [
        {"speaker": m["speaker"], "content": m["content"]}
        for m in meeting.log.read_all_messages()
    ]


def run_discussion(
    meeting: Meeting,
    connectors: dict[str, AgentConnector],
    max_rounds: int = DEFAULT_MAX_ROUNDS,
    max_consecutive_pass: int = DEFAULT_MAX_CONSECUTIVE_PASS,
) -> DiscussionResult:
    """
    Chạy vòng lặp thảo luận giữa các participant của meeting.

    connectors: map agent_id -> AgentConnector đã khởi tạo sẵn
                (MockConnector để test, AnthropicConnector/OpenAIConnector cho API thật).

    Thứ tự lượt nói xoay vòng theo participants[] trong meeting.yaml, nhưng
    NỘI DUNG và việc có nói hay không hoàn toàn do agent quyết định qua status.
    """
    data = meeting.data

    if data.get("status") != "active":
        raise ValueError(
            f"Discussion chỉ được chạy khi Meeting ACTIVE, "
            f"hiện tại là '{data.get('status')}'."
        )

    participants = data.get("participants", [])

    if len(participants) < 2:
        raise ValueError(
            "Discussion yêu cầu ít nhất 2 participants đã JOIN_ACCEPTED."
        )

    context_text = _read_context_text(meeting)
    topic = data["topic"]

    missing = [p for p in participants if p not in connectors]
    if missing:
        raise ValueError(f"Thiếu connector cho participant: {missing}")

    consecutive_pass = 0
    round_num = 0
    stop_reason = "max_rounds"

    while round_num < max_rounds:
        speaker_id = participants[round_num % len(participants)]
        connector = connectors[speaker_id]

        context = MeetingContextForAgent(
            topic=topic,
            context_text=context_text,
            history=_build_history(meeting),
            agent=connector.agent,
        )

        try:
            response = connector.send_turn(context)
        except ConnectorError as e:
            meeting.log.log_event("connector_error", detail=f"{speaker_id}: {e}")
            stop_reason = "connector_error"
            break

        round_num += 1

        if response.status == TurnStatus.PASS:
            meeting.log.log_event("agent_pass", detail=speaker_id)
            consecutive_pass += 1
        else:
            meeting.add_message(speaker_id, response.content)
            consecutive_pass = 0

        if response.status == TurnStatus.FINAL:
            stop_reason = "final"
            break

        if consecutive_pass >= max_consecutive_pass:
            stop_reason = "consecutive_pass"
            break
    else:
        stop_reason = "max_rounds"

    meeting.log.log_event(
        "discussion_stopped",
        detail=f"reason={stop_reason}, rounds_used={round_num}",
    )
    return DiscussionResult(stop_reason=stop_reason, rounds_used=round_num)


def request_synthesis(
    meeting: Meeting,
    synthesizer_id: str,
    connectors: dict[str, AgentConnector],
) -> str:
    """
    Sau khi thảo luận dừng, yêu cầu MỘT agent (mặc định: Xu) tổng hợp thành
    summary. v0.2 chỉ lấy nội dung tổng hợp dạng text tự do — parse
    decisions/action_items có cấu trúc từ AI output là việc của v0.3+
    (chưa cần, tránh over-engineering).
    """
    if synthesizer_id not in connectors:
        raise ValueError(f"Không có connector cho synthesizer '{synthesizer_id}'")

    connector = connectors[synthesizer_id]
    context = MeetingContextForAgent(
        topic=meeting.data["topic"] + " — YÊU CẦU TỔNG HỢP CUỐI CUỘC HỌP",
        context_text=_read_context_text(meeting),
        history=_build_history(meeting),
        agent=connector.agent,
    )
    response = connector.send_turn(context)
    return response.content or "(không có nội dung tổng hợp)"
