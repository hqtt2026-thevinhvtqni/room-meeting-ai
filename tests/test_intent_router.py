"""
Tests for core/intent_router.py — dùng mock requests, KHÔNG gọi API thật,
không cần ANTHROPIC_API_KEY để chạy trong CI/pytest.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from core.intent_router import IntentRouter, IntentRouterError, ALLOWED_ACTIONS


def _fake_response(json_text: str):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"content": [{"type": "text", "text": json_text}]}
    return resp


class TestAvailability:
    def test_not_available_without_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        router = IntentRouter(api_key=None)
        assert router.available is False

    def test_available_with_key(self):
        router = IntentRouter(api_key="sk-ant-fake-key")
        assert router.available is True

    def test_route_without_key_raises(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        router = IntentRouter(api_key=None)
        with pytest.raises(IntentRouterError, match="ANTHROPIC_API_KEY"):
            router.route("tao file test.md")


class TestRouting:
    @patch("core.intent_router.requests.post")
    def test_parses_valid_json_action(self, mock_post):
        mock_post.return_value = _fake_response(
            json.dumps({"action": "tao_file", "params": {"path": "docs/test.md", "content": "hello"}})
        )
        router = IntentRouter(api_key="sk-ant-fake")
        result = router.route("tao file docs/test.md noi dung hello")
        assert result["action"] == "tao_file"
        assert result["params"]["path"] == "docs/test.md"

    @patch("core.intent_router.requests.post")
    def test_strips_markdown_fence(self, mock_post):
        mock_post.return_value = _fake_response(
            "```json\n" + json.dumps({"action": "tro_chuyen", "params": {"reply": "chao anh"}}) + "\n```"
        )
        router = IntentRouter(api_key="sk-ant-fake")
        result = router.route("chao")
        assert result["action"] == "tro_chuyen"
        assert result["params"]["reply"] == "chao anh"

    @patch("core.intent_router.requests.post")
    def test_free_form_conversation_never_says_khong_hieu(self, mock_post):
        mock_post.return_value = _fake_response(
            json.dumps({"action": "tro_chuyen", "params": {"reply": "Da hieu, minh se dong vai thu ky."}})
        )
        router = IntentRouter(api_key="sk-ant-fake")
        result = router.route("ban la thu ky cua phong")
        assert result["action"] == "tro_chuyen"
        assert "chua hieu" not in result["params"]["reply"].lower()

    @patch("core.intent_router.requests.post")
    def test_unknown_action_falls_back_to_tro_chuyen(self, mock_post):
        # Nếu model "sáng tạo" 1 action ngoài whitelist, phải ép về tro_chuyen
        # thay vì để ChatBot thực thi hành động không xác định.
        mock_post.return_value = _fake_response(
            json.dumps({"action": "format_o_cung", "params": {"path": "C:/"}})
        )
        router = IntentRouter(api_key="sk-ant-fake")
        result = router.route("xoa het o C")
        assert result["action"] == "tro_chuyen"

    @patch("core.intent_router.requests.post")
    def test_invalid_json_raises_router_error(self, mock_post):
        mock_post.return_value = _fake_response("khong phai json dau")
        router = IntentRouter(api_key="sk-ant-fake")
        with pytest.raises(IntentRouterError, match="JSON khong hop le"):
            router.route("abc")

    @patch("core.intent_router.requests.post")
    def test_network_error_raises_router_error(self, mock_post):
        import requests
        mock_post.side_effect = requests.ConnectionError("no network")
        router = IntentRouter(api_key="sk-ant-fake")
        with pytest.raises(IntentRouterError, match="Loi goi Anthropic API"):
            router.route("abc")


class TestAllowedActionsWhitelist:
    def test_all_expected_actions_present(self):
        assert ALLOWED_ACTIONS == {
            "tao_file", "mo_file", "tao_thu_muc", "doc_file", "xoa_file", "tro_chuyen",
        }
