"""
Tests for core/llama_intent_router.py — mock Groq client, KHÔNG gọi API
thật, không cần GROQ_API_KEY để chạy trong CI/pytest.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from core.llama_intent_router import LlamaIntentRouter
from core.intent_router import IntentRouterError, ALLOWED_ACTIONS


def _fake_tool_call_response(name: str, arguments: dict):
    resp = MagicMock()
    tool_call = MagicMock()
    tool_call.function.name = name
    tool_call.function.arguments = json.dumps(arguments)
    resp.choices = [MagicMock(message=MagicMock(tool_calls=[tool_call]))]
    return resp


def _fake_text_response(text: str):
    resp = MagicMock()
    resp.choices = [MagicMock(message=MagicMock(tool_calls=None, content=text))]
    return resp


class TestAvailability:
    def test_not_available_without_key(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        router = LlamaIntentRouter(api_key=None)
        assert router.available is False

    def test_available_with_key(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        assert router.available is True

    def test_route_without_key_raises(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        router = LlamaIntentRouter(api_key=None)
        with pytest.raises(IntentRouterError, match="GROQ_API_KEY"):
            router.route("tao file test.md")


class TestRoutingWithToolCalls:
    def test_tool_call_maps_to_action(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = _fake_tool_call_response(
            "tao_file", {"path": "docs/test.md", "content": "hello"}
        )
        router._client = fake_client

        result = router.route("tao file docs/test.md noi dung hello")
        assert result["action"] == "tao_file"
        assert result["params"]["path"] == "docs/test.md"
        assert result["params"]["content"] == "hello"

    def test_no_tool_call_means_tro_chuyen(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = _fake_text_response(
            "Da hieu, minh se dong vai thu ky phong."
        )
        router._client = fake_client

        result = router.route("ban la thu ky cua phong")
        assert result["action"] == "tro_chuyen"
        assert "chua hieu" not in result["params"]["reply"].lower()

    def test_unknown_tool_name_falls_back_to_tro_chuyen(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = _fake_tool_call_response(
            "format_o_cung", {"path": "C:/"}
        )
        router._client = fake_client

        result = router.route("xoa het o C")
        assert result["action"] == "tro_chuyen"

    def test_invalid_arguments_json_raises(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        resp = MagicMock()
        tool_call = MagicMock()
        tool_call.function.name = "tao_file"
        tool_call.function.arguments = "khong phai json"
        resp.choices = [MagicMock(message=MagicMock(tool_calls=[tool_call]))]
        fake_client.chat.completions.create.return_value = resp
        router._client = fake_client

        with pytest.raises(IntentRouterError, match="tham so khong hop le"):
            router.route("abc")

    def test_api_error_raises_router_error(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        fake_client.chat.completions.create.side_effect = RuntimeError("rate limit")
        router._client = fake_client

        with pytest.raises(IntentRouterError, match="Loi goi Groq API"):
            router.route("abc")


class TestHistoryConversion:
    def test_history_lines_converted_to_roles(self):
        router = LlamaIntentRouter(api_key="gsk_fake")
        fake_client = MagicMock()
        fake_client.chat.completions.create.return_value = _fake_text_response("ok")
        router._client = fake_client

        router.route("cau moi", history=["Vinh: cau cu", "Agent: tra loi cu"])

        sent_messages = fake_client.chat.completions.create.call_args.kwargs["messages"]
        roles = [m["role"] for m in sent_messages]
        assert "system" in roles
        assert "user" in roles
        assert "assistant" in roles


class TestToolsWhitelist:
    def test_all_tools_are_allowed_actions(self):
        from core.llama_intent_router import TOOLS
        tool_names = {t["function"]["name"] for t in TOOLS}
        assert tool_names.issubset(ALLOWED_ACTIONS)
