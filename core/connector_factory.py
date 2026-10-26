from __future__ import annotations

from typing import Mapping, Sequence

from core.agent_registry import Agent
from core.connectors import (
    AgentConnector,
    AnthropicConnector,
    ConnectorError,
    InternalConnector,
    MockConnector,
    OpenAIConnector,
)
from core.groq_connector import GroqConnector


class ConnectorFactory:
    """Create the correct connector from an agent provider."""

    @staticmethod
    def create(
        agent: Agent,
        *,
        api_key: str | None = None,
        local_agent=None,
        scripted_responses: Sequence | None = None,
    ) -> AgentConnector:
        provider = (agent.provider or "").strip().lower()

        if provider == "groq":
            return GroqConnector(agent, api_key=api_key)
        if provider == "google":
            from core.gemini_connector import GeminiConnector
            return GeminiConnector(agent, api_key=api_key)
        if provider == "anthropic":
            return AnthropicConnector(agent, api_key=api_key)
        if provider == "openai":
            return OpenAIConnector(agent, api_key=api_key)
        if provider == "internal":
            if local_agent is None:
                raise ConnectorError(
                    f"Agent '{agent.id}' dùng internal nhưng chưa cung cấp local_agent."
                )
            return InternalConnector(agent, local_agent)
        if provider == "mock":
            return MockConnector(agent, list(scripted_responses or []))

        raise ConnectorError(
            f"Chưa có connector cho provider '{agent.provider}' "
            f"của agent '{agent.id}'."
        )
