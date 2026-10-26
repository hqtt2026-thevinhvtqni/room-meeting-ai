"""Connector factory + GeminiConnector tests (Work 23).

Deterministic: no network, no real key, no real sleeps.
 - Autouse fixture clears GEMINI_* env, blocks urllib.request.urlopen and time.sleep.
 - Tests that exercise the real adapter's REAL_API path install a fake urlopen explicitly.
"""
import email.message
import io
import json
import traceback
import urllib.error

import pytest

from core.agent_registry import Agent, AgentRegistry
from core.connector_factory import ConnectorFactory
from core.connectors import (
    AgentResponse,
    AnthropicConnector,
    ConnectorError,
    InternalConnector,
    MeetingContextForAgent,
    MockConnector,
    OpenAIConnector,
    TurnStatus,
)
from core.gemini_connector import GeminiConnector
from core.gemini_provider_adapter import (
    GeminiProviderAdapter,
    GeminiRateLimitError,
)
from core.groq_connector import GroqConnector

FAKE_KEY = "fake-gemini-key-0123456789"


# --------------------------------------------------------------------------- helpers


def make_agent(provider: str, model: str = "test-model") -> Agent:
    return Agent(
        id=f"test_{provider}",
        name=f"Test {provider}",
        role="Test",
        provider=provider,
        model=model,
        capabilities=[],
    )


def make_context(agent: Agent, history=None) -> MeetingContextForAgent:
    if history is None:
        history = [{"speaker": "Vinh", "content": "STATUS: REPLY\nXin chào"}]
    return MeetingContextForAgent(
        topic="test topic",
        context_text="synthetic test context",
        history=history,
        agent=agent,
    )


def full_traceback(exc: BaseException) -> str:
    return "".join(traceback.format_exception(exc))


class FakeAdapter:
    """Injected adapter: records calls, returns/raises what the test configures."""

    def __init__(self, result=None, exc=None):
        self.result = result
        self.exc = exc
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.exc is not None:
            raise self.exc
        return self.result


class FakeHTTPResponse:
    def __init__(self, body: bytes):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False


def gemini_json(text="STATUS: REPLY\nXin chào từ Gemini", finish="STOP"):
    return json.dumps(
        {
            "candidates": [
                {"content": {"parts": [{"text": text}]}, "finishReason": finish}
            ],
            "usageMetadata": {"promptTokenCount": 3, "candidatesTokenCount": 4},
        }
    ).encode("utf-8")


def http_error(code: int, body: str) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://example.invalid", code, "err", email.message.Message(), io.BytesIO(body.encode())
    )


@pytest.fixture(autouse=True)
def isolate_environment(monkeypatch):
    for name in ("GEMINI_API_KEY", "GEMINI_PROVIDER_MODE", "GEMINI_MODEL_NAME"):
        monkeypatch.delenv(name, raising=False)

    def _blocked(*args, **kwargs):
        raise AssertionError("network access attempted in a deterministic test")

    monkeypatch.setattr("urllib.request.urlopen", _blocked)
    monkeypatch.setattr("time.sleep", lambda *_: None)


@pytest.fixture
def urlopen_calls(monkeypatch):
    """Install a recording fake urlopen. Set `.handler` to a callable(req) -> bytes | raise."""

    class Recorder:
        def __init__(self):
            self.requests = []
            self.handler = lambda req: gemini_json()

    rec = Recorder()

    def fake_urlopen(req, timeout=None):
        rec.requests.append(req)
        return FakeHTTPResponse(rec.handler(req))

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    return rec


# --------------------------------------------------------------------------- existing factory behavior (kept)


def test_factory_routes_groq_to_groq_connector(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-groq-key")
    agent = AgentRegistry().get("quan_gia_gpt")
    connector = ConnectorFactory.create(agent)
    assert isinstance(connector, GroqConnector)
    assert connector.agent.id == "quan_gia_gpt"
    assert connector.agent.provider == "groq"
    assert connector.agent.model == "openai/gpt-oss-120b"


def test_factory_routes_qwen_to_groq_connector(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "fake-groq-key")
    agent = AgentRegistry().get("quan_gia_qwen")
    connector = ConnectorFactory.create(agent)
    assert isinstance(connector, GroqConnector)
    assert connector.agent.id == "quan_gia_qwen"
    assert connector.agent.model == "qwen/qwen3.8-27b"


def test_factory_routes_anthropic():
    assert isinstance(
        ConnectorFactory.create(make_agent("anthropic"), api_key="fake-anthropic-key"),
        AnthropicConnector,
    )


def test_factory_routes_openai():
    assert isinstance(
        ConnectorFactory.create(make_agent("openai"), api_key="fake-openai-key"),
        OpenAIConnector,
    )


def test_factory_routes_mock():
    assert isinstance(
        ConnectorFactory.create(make_agent("mock"), scripted_responses=[]),
        MockConnector,
    )


def test_factory_requires_local_agent_for_internal():
    with pytest.raises(ConnectorError, match="local_agent"):
        ConnectorFactory.create(make_agent("internal"))


def test_factory_routes_internal_with_local_agent():
    class Local:
        def execute(self, task, history):
            return "STATUS: PASS"

    assert isinstance(
        ConnectorFactory.create(make_agent("internal"), local_agent=Local()),
        InternalConnector,
    )


def test_factory_rejects_unknown_provider():
    with pytest.raises(ConnectorError, match="unknown-provider"):
        ConnectorFactory.create(make_agent("unknown-provider"))


# --------------------------------------------------------------------------- Google routing + config


def test_factory_routes_google_to_gemini_connector(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    connector = ConnectorFactory.create(make_agent("google", model="gemini"))
    assert isinstance(connector, GeminiConnector)  # constructing must not hit the network


def test_factory_provider_match_ignores_case_and_whitespace(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    assert isinstance(
        ConnectorFactory.create(make_agent("  Google ", model="gemini")), GeminiConnector
    )


def test_factory_routes_registry_quan_gia_gemini(monkeypatch):
    # Replaces the obsolete "quan_gia_gemini is unsupported" expectation: with the
    # connector present, provider google must route to GeminiConnector.
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    agent = AgentRegistry().get("quan_gia_gemini")
    assert agent.provider == "google"
    connector = ConnectorFactory.create(agent)
    assert isinstance(connector, GeminiConnector)
    assert connector.adapter.model_name == GeminiProviderAdapter.DEFAULT_GEMINI_MODEL


def test_kha_gemini_stays_internal_and_is_not_routed_to_gemini_connector():
    agent = AgentRegistry().get("kha_gemini")
    assert agent.provider == "internal"
    with pytest.raises(ConnectorError, match="local_agent"):
        ConnectorFactory.create(agent)


def test_factory_missing_gemini_key_fails_closed():
    with pytest.raises(ConnectorError, match="cấu hình/xác thực") as exc:
        ConnectorFactory.create(make_agent("google", model="gemini"))
    assert "GeminiAuthError" in str(exc.value)


@pytest.mark.parametrize("blank_key", ["", "   "])
def test_blank_explicit_key_does_not_fall_back_to_env(monkeypatch, blank_key):
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    with pytest.raises(ConnectorError, match="cấu hình/xác thực"):
        ConnectorFactory.create(make_agent("google", model="gemini"), api_key=blank_key)


def test_invalid_provider_mode_is_rejected(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    monkeypatch.setenv("GEMINI_PROVIDER_MODE", "LIVE")
    with pytest.raises(ConnectorError, match="GeminiInvalidModeError"):
        ConnectorFactory.create(make_agent("google", model="gemini"))


def test_blank_provider_mode_defaults_to_real_api_and_fails_closed(monkeypatch):
    monkeypatch.setenv("GEMINI_PROVIDER_MODE", "")
    with pytest.raises(ConnectorError, match="GeminiAuthError"):
        ConnectorFactory.create(make_agent("google", model="gemini"))


def test_generic_model_label_uses_adapter_default_and_custom_model_is_kept():
    generic = GeminiConnector(make_agent("google", model="gemini"), mode="MOCK")
    assert generic.adapter.model_name == GeminiProviderAdapter.DEFAULT_GEMINI_MODEL
    custom = GeminiConnector(make_agent("google", model="gemini-custom-x"), mode="MOCK")
    assert custom.adapter.model_name == "gemini-custom-x"


# --------------------------------------------------------------------------- send_turn with fake adapter


def test_gemini_connector_parses_fake_adapter_response():
    fake = FakeAdapter(
        result={"status": "SUCCESS", "content": "STATUS: REPLY\nGemini trả lời.", "gate": "GATE_A_MOCK"}
    )
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, mode="MOCK", adapter=fake)

    result = connector.send_turn(make_context(agent))

    assert isinstance(result, AgentResponse)
    assert result.status == TurnStatus.REPLY
    assert result.content == "Gemini trả lời."
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert "Xin chào" in call["prompt"]
    assert "test topic" in call["system_instruction"]
    assert agent.name in call["system_instruction"]


@pytest.mark.parametrize(
    "raw, status, content",
    [
        ("STATUS: PASS\nignored text", TurnStatus.PASS, ""),
        ("STATUS: FINAL\nChốt phương án A.", TurnStatus.FINAL, "Chốt phương án A."),
        ("Không có dòng STATUS", TurnStatus.REPLY, "Không có dòng STATUS"),
    ],
)
def test_gemini_connector_status_protocol(raw, status, content):
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, mode="MOCK", adapter=FakeAdapter(result={"content": raw}))
    result = connector.send_turn(make_context(agent))
    assert (result.status, result.content) == (status, content)


def test_gemini_connector_handles_empty_history():
    fake = FakeAdapter(result={"content": "STATUS: REPLY\nok"})
    agent = make_agent("google", model="gemini")
    GeminiConnector(agent, mode="MOCK", adapter=fake).send_turn(make_context(agent, history=[]))
    assert fake.calls[0]["prompt"].strip()  # adapter rejects empty prompts


@pytest.mark.parametrize(
    "bad_result",
    [
        {"status": "SUCCESS", "content": "  "},
        {"status": "SUCCESS", "content": ""},
        {"status": "SUCCESS", "content": None},
        {"status": "SUCCESS", "content": 123},
        {"status": "SUCCESS"},
        None,
        "just a string",
        ["content"],
    ],
)
def test_gemini_connector_rejects_empty_or_malformed_adapter_result(bad_result):
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, mode="MOCK", adapter=FakeAdapter(result=bad_result))
    with pytest.raises(ConnectorError, match="Gemini trả về"):
        connector.send_turn(make_context(agent))


def test_gemini_connector_redacts_adapter_exception_text_everywhere():
    secret = "do-not-leak-this-secret"
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, mode="MOCK", adapter=FakeAdapter(exc=RuntimeError(secret)))

    with pytest.raises(ConnectorError) as exc:
        connector.send_turn(make_context(agent))

    assert secret not in str(exc.value)
    assert secret not in repr(exc.value)
    assert secret not in full_traceback(exc.value)  # no leak through __cause__/__context__
    assert exc.value.__cause__ is None
    assert "RuntimeError" in str(exc.value)


def test_gemini_connector_wraps_adapter_errors_without_provider_text():
    agent = make_agent("google", model="gemini")
    err = GeminiRateLimitError("quota text from provider", retry_after_sec=7)
    connector = GeminiConnector(agent, mode="MOCK", adapter=FakeAdapter(exc=err))
    with pytest.raises(ConnectorError) as exc:
        connector.send_turn(make_context(agent))
    assert "GeminiRateLimitError" in str(exc.value)
    assert "quota text" not in str(exc.value)


# --------------------------------------------------------------------------- real adapter wiring, still offline


def test_gemini_connector_with_real_adapter_in_mock_mode():
    agent = make_agent("google", model="gemini")
    result = GeminiConnector(agent, mode="MOCK").send_turn(make_context(agent))
    assert result.status == TurnStatus.REPLY
    assert result.content.startswith("[MOCK_GEMINI_RESPONSE]")


def test_real_api_path_success_via_simulated_http(urlopen_calls, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    agent = make_agent("google", model="gemini")
    connector = ConnectorFactory.create(agent)

    result = connector.send_turn(make_context(agent))

    assert result.status == TurnStatus.REPLY
    assert result.content == "Xin chào từ Gemini"
    (req,) = urlopen_calls.requests
    assert req.get_header("X-goog-api-key") == FAKE_KEY
    assert FAKE_KEY not in req.full_url
    assert GeminiProviderAdapter.DEFAULT_GEMINI_MODEL in req.full_url


def test_real_api_path_uses_agent_specific_model(urlopen_calls):
    agent = make_agent("google", model="gemini-custom-x")
    GeminiConnector(agent, api_key=FAKE_KEY).send_turn(make_context(agent))
    assert "models/gemini-custom-x:generateContent" in urlopen_calls.requests[0].full_url


def test_real_api_auth_error_is_not_retried_and_does_not_leak_key(urlopen_calls):
    def handler(req):
        raise http_error(401, f"bad credentials for {FAKE_KEY}")

    urlopen_calls.handler = handler
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, api_key=FAKE_KEY)

    with pytest.raises(ConnectorError) as exc:
        connector.send_turn(make_context(agent))

    assert len(urlopen_calls.requests) == 1  # permanent error: exactly one attempt
    assert "GeminiAuthError" in str(exc.value)
    assert FAKE_KEY not in full_traceback(exc.value)


def test_real_api_timeout_retries_then_fails_without_leaking_key(urlopen_calls):
    def handler(req):
        raise urllib.error.URLError(f"unreachable while using {FAKE_KEY}")

    urlopen_calls.handler = handler
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, api_key=FAKE_KEY)

    with pytest.raises(ConnectorError) as exc:
        connector.send_turn(make_context(agent))

    assert len(urlopen_calls.requests) == 1 + connector.adapter.max_retries
    assert "GeminiTimeoutError" in str(exc.value)
    assert FAKE_KEY not in full_traceback(exc.value)


@pytest.mark.parametrize(
    "body",
    [
        b'{"candidates": []}',
        b'{"candidates": [{"content": {"parts": []}, "finishReason": "SAFETY"}]}',
        b"<html>not json</html>",
    ],
)
def test_real_api_empty_or_malformed_provider_body_is_rejected(urlopen_calls, body):
    urlopen_calls.handler = lambda req: body
    agent = make_agent("google", model="gemini")
    connector = GeminiConnector(agent, api_key=FAKE_KEY)
    with pytest.raises(ConnectorError) as exc:
        connector.send_turn(make_context(agent))
    assert "GeminiInvalidResponseError" in str(exc.value)
