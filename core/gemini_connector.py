from __future__ import annotations

import os
from typing import Any

from core.agent_registry import Agent
from core.connectors import (
    AgentConnector,
    AgentResponse,
    ConnectorError,
    MeetingContextForAgent,
    build_system_prompt,
    build_user_message,
    parse_agent_output,
)
from core.gemini_provider_adapter import GeminiAdapterError, GeminiProviderAdapter

# Agent configs use a generic model label ("gemini"/"google"); in that case the adapter's
# own default (or GEMINI_MODEL_NAME) decides the concrete model.
_GENERIC_MODEL_LABELS = {"", "gemini", "google"}


class GeminiConnector(AgentConnector):
    """Bridge GeminiProviderAdapter into ROOM-HOP's existing AgentConnector contract.

    - No network access in the constructor.
    - Key comes from `api_key` or server-side GEMINI_API_KEY (resolved by the adapter);
      a blank explicit key fails closed in REAL_API mode.
    - `adapter` is an injection seam for tests (fake adapter, no network, no key).
    """

    def __init__(
        self,
        agent: Agent,
        api_key: str | None = None,
        *,
        mode: str | None = None,
        adapter: Any | None = None,
    ):
        super().__init__(agent)
        resolved_mode = (mode or os.getenv("GEMINI_PROVIDER_MODE") or "").strip().upper()
        self.mode = resolved_mode or "REAL_API"  # fail closed: real mode needs a key

        configured_model = (agent.model or "").strip()
        model_name = None if configured_model.lower() in _GENERIC_MODEL_LABELS else configured_model

        if adapter is not None:
            self.adapter = adapter
            return
        try:
            self.adapter = GeminiProviderAdapter(
                mode=self.mode,
                api_key=api_key,
                model_name=model_name,
            )
        except GeminiAdapterError as exc:
            # Construction errors are raised directly by the adapter with static text
            # (no key, no transport context), so chaining is safe here.
            raise ConnectorError(
                f"Không thể khởi tạo Gemini connector cho agent '{agent.id}' "
                f"(lỗi cấu hình/xác thực: {type(exc).__name__})."
            ) from exc

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        system_prompt = build_system_prompt(
            self.agent, context.topic, context.context_text
        )
        user_message = build_user_message(context.history)

        failure_type: str | None = None
        try:
            result = self.adapter.generate_content(
                prompt=user_message,
                system_instruction=system_prompt,
            )
        except Exception as exc:  # noqa: BLE001 - adapter, transport or injected-fake failure
            # Record only the exception class. Do NOT chain (`from exc`) and do NOT raise
            # inside this block: exception text/args and the implicit __context__ (e.g. the
            # raw URLError the adapter was handling) may contain secrets and would surface
            # in tracebacks and logs even when str(exc) is clean.
            failure_type = type(exc).__name__

        if failure_type is not None:
            raise ConnectorError(
                f"Gemini connector thất bại cho agent '{self.agent.id}' "
                f"({failure_type})."
            )

        if not isinstance(result, dict):
            raise ConnectorError("Gemini trả về cấu trúc response không hợp lệ.")
        content = result.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ConnectorError("Gemini trả về nội dung rỗng hoặc không hợp lệ.")

        return parse_agent_output(content)
