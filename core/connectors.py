"""
Agent Connector — ROOM HOP v0.2

Interface chung để Meeting Manager gọi AI thật (hoặc Mock để test) mà không
cần biết bên trong là Anthropic hay OpenAI. Đúng tinh thần "AI API nằm
ngoài Core" đã chốt từ đầu.

🔒 Không đổi 4 lõi v0.1 (Meeting Manager, Agent Registry, Context Loader,
Meeting Log). Connector chỉ CUNG CẤP nội dung message — Discussion Engine
(discussion.py) mới là chỗ quyết định luồng hội thoại.
"""

from __future__ import annotations

import os
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

import requests

from core.agent_registry import Agent
from core.usage_ledger import extract_usage, new_usage_event, record_usage_event, sha256_text


class TurnStatus(str, Enum):
    REPLY = "REPLY"
    PASS = "PASS"
    FINAL = "FINAL"


@dataclass
class MeetingContextForAgent:
    """Gói dữ liệu gửi cho một agent trong một lượt cụ thể."""

    topic: str
    context_text: str                     # nội dung context files đã ghép
    history: list[dict]                   # [{"speaker": str, "content": str}, ...]
    agent: Agent


@dataclass
class AgentResponse:
    status: TurnStatus
    content: str                          # rỗng nếu PASS
    raw: str = field(default="", repr=False)   # response gốc chưa parse, để debug


class ConnectorError(Exception):
    """Lỗi khi gọi API thật — Discussion Engine bắt lỗi này để không sập cả cuộc họp."""


# ---------------------------------------------------------------------------
# Prompt / parsing helpers dùng chung cho mọi connector
# ---------------------------------------------------------------------------

STATUS_LINE_RE = re.compile(r"^\s*STATUS:\s*(REPLY|PASS|FINAL)\s*$", re.IGNORECASE | re.MULTILINE)


def build_system_prompt(agent: Agent, topic: str, context_text: str) -> str:
    return f"""Bạn là {agent.name}, vai trò {agent.role} trong một cuộc họp nội bộ (ROOM HOP).

Chủ đề cuộc họp: {topic}

--- CONTEXT ĐƯỢC CẤP ---
{context_text}
--- HẾT CONTEXT ---

QUY TẮC BẮT BUỘC khi trả lời:
Dòng đầu tiên PHẢI là một trong ba trạng thái sau (viết đúng định dạng):
STATUS: REPLY   -> bạn có điều cần bổ sung/phản biện/trả lời
STATUS: PASS    -> bạn không có gì cần bổ sung ở lượt này
STATUS: FINAL   -> bạn cho rằng cuộc thảo luận đã đủ để tổng hợp thành quyết định

Nếu STATUS là PASS, không cần viết gì thêm sau dòng đó.
Nếu STATUS là REPLY hoặc FINAL, các dòng tiếp theo là nội dung bạn muốn nói,
ngắn gọn, đúng trọng tâm — đây là một cuộc họp thật, không phải bài luận."""


def build_user_message(history: list[dict]) -> str:
    if not history:
        return "(Cuộc họp vừa mở, chưa có ai phát biểu.)"
    lines = []
    for m in history:
        lines.append(f"{m['speaker']}: {m['content']}")
    return "\n\n".join(lines)


def parse_agent_output(raw_text: str) -> AgentResponse:
    """
    Parse output thô của model thành AgentResponse.
    Nếu không tìm được dòng STATUS hợp lệ, fallback về REPLY với toàn bộ
    nội dung — AN TOÀN HƠN là raise lỗi làm sập cuộc họp vì model lỡ quên
    format.
    """
    match = STATUS_LINE_RE.search(raw_text)
    if not match:
        return AgentResponse(status=TurnStatus.REPLY, content=raw_text.strip(), raw=raw_text)

    status = TurnStatus(match.group(1).upper())
    content = raw_text[match.end():].strip()
    if status == TurnStatus.PASS:
        content = ""
    return AgentResponse(status=status, content=content, raw=raw_text)


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------


class AgentConnector(ABC):
    """Mỗi provider (Anthropic, OpenAI, Mock...) implement interface này."""

    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        ...


# ---------------------------------------------------------------------------
# Mock — dùng cho test và cho demo khi chưa có API key thật
# ---------------------------------------------------------------------------


class MockConnector(AgentConnector):
    """
    Trả lời theo kịch bản định trước (danh sách AgentResponse). Dùng để:
      - Test Discussion Engine (Room Stop Guard) mà không cần gọi API thật.
      - Demo luồng v0.2 khi Vinh chưa gắn API key.
    Không gọi mạng, không tốn phí.
    """

    def __init__(self, agent: Agent, scripted_responses: list[AgentResponse]):
        super().__init__(agent)
        self._script = list(scripted_responses)
        self._idx = 0

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        usage_event = new_usage_event(
            provider="internal", model=self.agent.model or None, ai_id=self.agent.id,
            ai_role=self.agent.role, caller="meeting_turn",
        )
        if self._idx >= len(self._script):
            # Hết kịch bản mà vẫn bị gọi tiếp -> PASS an toàn, không raise
            response = AgentResponse(status=TurnStatus.PASS, content="", raw="(mock: hết kịch bản)")
        else:
            response = self._script[self._idx]
            self._idx += 1
        usage_event.update(usage_source="unavailable", content_hash=sha256_text(response.content))
        record_usage_event(usage_event)
        return response


# ---------------------------------------------------------------------------
# Anthropic — gọi API thật. CẦN Vinh tự set ANTHROPIC_API_KEY trên PC.
# ---------------------------------------------------------------------------


class AnthropicConnector(AgentConnector):
    API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, agent: Agent, api_key: str | None = None):
        super().__init__(agent)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ConnectorError(
                "Thiếu ANTHROPIC_API_KEY. Set biến môi trường trên PC trước khi chạy, "
                "ví dụ: export ANTHROPIC_API_KEY=sk-ant-..."
            )
        if not agent.model:
            raise ConnectorError(
                f"Agent '{agent.id}' chưa khai báo 'model' trong agents/{agent.id}.yaml. "
                f"Điền tên model Anthropic thật (xem docs.claude.com) trước khi dùng AnthropicConnector."
            )

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        system_prompt = build_system_prompt(self.agent, context.topic, context.context_text)
        user_message = build_user_message(context.history)
        started = time.monotonic()
        usage_event = new_usage_event(
            provider="anthropic", model=self.agent.model, ai_id=self.agent.id,
            ai_role=self.agent.role, caller="meeting_turn",
        )

        try:
            resp = requests.post(
                self.API_URL,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.agent.model,
                    "max_tokens": 800,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_message}],
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            raw_text = "\n".join(text_blocks)
            usage_event.update(extract_usage("anthropic", data.get("usage")))
            usage_event["provider_request_id"] = data.get("id") or resp.headers.get("request-id")
            usage_event["latency_ms"] = round((time.monotonic() - started) * 1000)
            usage_event["content_hash"] = sha256_text(raw_text)
            record_usage_event(usage_event)
        except requests.RequestException as e:
            error_response = getattr(e, "response", None)
            error_data = {}
            if error_response is not None:
                try:
                    error_data = error_response.json()
                except Exception:
                    error_data = {}
            usage = error_data.get("usage") if isinstance(error_data, dict) else None
            usage_event.update(extract_usage("anthropic", usage))
            usage_event.update(status="error", error_class=type(e).__name__,
                               latency_ms=round((time.monotonic() - started) * 1000))
            if error_response is not None:
                usage_event["provider_request_id"] = error_response.headers.get("request-id")
            record_usage_event(usage_event)
            raise ConnectorError(f"Anthropic API call thất bại cho agent '{self.agent.id}': {e}") from e

        return parse_agent_output(raw_text)


# ---------------------------------------------------------------------------
# Internal — agent chạy local trong tiến trình Python, không gọi API mạng.
# Dùng cho agent như MeAgent (me_meta): logic nằm trong chính class agent,
# không phải kịch bản cứng (khác MockConnector) và không tốn phí API (khác
# AnthropicConnector/OpenAIConnector).
# ---------------------------------------------------------------------------


class InternalConnector(AgentConnector):
    """
    Bọc một local agent object (có method execute(task, history)) thành
    AgentConnector chuẩn. Output của agent phải theo giao thức STATUS
    (dùng chung parse_agent_output như các connector khác).
    """

    def __init__(self, agent: Agent, local_agent):
        super().__init__(agent)
        if not hasattr(local_agent, "execute"):
            raise ConnectorError(
                f"Local agent cho '{agent.id}' phải có method execute(task, history)."
            )
        self.local_agent = local_agent

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        usage_event = new_usage_event(
            provider="internal", model=self.agent.model or None, ai_id=self.agent.id,
            ai_role=self.agent.role, caller="meeting_turn",
        )
        try:
            raw_text = self.local_agent.execute(
                task=context.topic,
                history=context.history,
            )
        except Exception as e:
            usage_event.update(status="error", error_class=type(e).__name__)
            record_usage_event(usage_event)
            raise ConnectorError(
                f"Internal agent '{self.agent.id}' lỗi khi execute: {e}"
            ) from e
        usage_event.update(usage_source="unavailable", content_hash=sha256_text(raw_text))
        record_usage_event(usage_event)
        return parse_agent_output(raw_text)


# ---------------------------------------------------------------------------
# OpenAI — gọi API thật cho Xu. CẦN Vinh tự set OPENAI_API_KEY trên PC.
# ---------------------------------------------------------------------------


class OpenAIConnector(AgentConnector):
    API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, agent: Agent, api_key: str | None = None):
        super().__init__(agent)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ConnectorError(
                "Thiếu OPENAI_API_KEY. Set biến môi trường trên PC trước khi chạy, "
                "ví dụ: export OPENAI_API_KEY=sk-..."
            )
        if not agent.model:
            raise ConnectorError(
                f"Agent '{agent.id}' chưa khai báo 'model' trong agents/{agent.id}.yaml. "
                f"Điền tên model OpenAI thật (xem platform.openai.com/docs) trước khi dùng OpenAIConnector."
            )

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        system_prompt = build_system_prompt(self.agent, context.topic, context.context_text)
        user_message = build_user_message(context.history)
        started = time.monotonic()
        usage_event = new_usage_event(
            provider="openai", model=self.agent.model, ai_id=self.agent.id,
            ai_role=self.agent.role, caller="meeting_turn",
        )

        try:
            resp = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "content-type": "application/json",
                },
                json={
                    "model": self.agent.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    "max_tokens": 800,
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]
            usage_event.update(extract_usage("openai", data.get("usage")))
            usage_event["provider_request_id"] = data.get("id") or resp.headers.get("x-request-id")
            usage_event["latency_ms"] = round((time.monotonic() - started) * 1000)
            usage_event["content_hash"] = sha256_text(raw_text)
            record_usage_event(usage_event)
        except requests.RequestException as e:
            error_response = getattr(e, "response", None)
            error_data = {}
            if error_response is not None:
                try:
                    error_data = error_response.json()
                except Exception:
                    error_data = {}
            usage = error_data.get("usage") if isinstance(error_data, dict) else None
            usage_event.update(extract_usage("openai", usage))
            usage_event.update(status="error", error_class=type(e).__name__,
                               latency_ms=round((time.monotonic() - started) * 1000))
            if error_response is not None:
                usage_event["provider_request_id"] = error_response.headers.get("x-request-id")
            record_usage_event(usage_event)
            raise ConnectorError(f"OpenAI API call thất bại cho agent '{self.agent.id}': {e}") from e

        return parse_agent_output(raw_text)
