from __future__ import annotations

import os

import requests

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


class GroqConnector(AgentConnector):
    """Connector cho các model chạy qua Groq API."""

    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, agent: Agent, api_key: str | None = None):
        super().__init__(agent)
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")

        if not self.api_key:
            raise ConnectorError(
                "Thiếu GROQ_API_KEY trước khi dùng GroqConnector."
            )

        if not self.agent.model:
            raise ConnectorError(
                f"Agent '{self.agent.id}' chưa có model cho Groq."
            )

    def send_turn(self, context: MeetingContextForAgent) -> AgentResponse:
        system_prompt = build_system_prompt(
            self.agent,
            context.topic,
            context.context_text,
        )
        user_message = build_user_message(context.history)

        try:
            resp = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.agent.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        },
                    ],
                    "max_completion_tokens": 800,
                },
                timeout=60,
            )
            resp.raise_for_status()

            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            raise ConnectorError(
                f"Groq API call thất bại cho agent "
                f"'{self.agent.id}': {e}"
            ) from e
        except (KeyError, TypeError, IndexError) as e:
            raise ConnectorError(
                f"Groq trả response không hợp lệ cho agent "
                f"'{self.agent.id}': {e}"
            ) from e

        return parse_agent_output(raw_text)
