import pytest
from unittest.mock import patch, MagicMock
import urllib.error
from core.gemini_provider_adapter import (
    GeminiProviderAdapter,
    GeminiInvalidModeError,
    GeminiAuthError,
    GeminiRateLimitError,
    GeminiTimeoutError,
    GeminiInvalidResponseError,
    GeminiAdapterError
)


def test_mode_validation():
    with pytest.raises(GeminiInvalidModeError):
        GeminiProviderAdapter(mode="INVALID_MODE")


def test_missing_api_key_real():
    with pytest.raises(GeminiAuthError):
        GeminiProviderAdapter(mode="REAL_API", api_key="")


def test_mock_token_labeling():
    adapter = GeminiProviderAdapter(mode="MOCK")
    res = adapter.generate_content("Xin chào Gemini, hãy giới thiệu ngắn gọn về ROOM-HOP.")
    assert res["status"] == "SUCCESS"
    assert res["gate"] == "GATE_A_MOCK"
    assert res["usage"]["is_estimated"] is True
    assert "estimated_prompt_tokens" in res["usage"]


def test_empty_prompt_validation():
    adapter = GeminiProviderAdapter(mode="MOCK")
    with pytest.raises(GeminiInvalidResponseError):
        adapter.generate_content("   ")


def test_mock_execution_flow():
    adapter = GeminiProviderAdapter(mode="MOCK", model_name="gemini-1.5-flash")
    res = adapter.generate_content("Test prompt")
    assert res["model"] == "gemini-1.5-flash"
    assert "[MOCK_GEMINI_RESPONSE]" in res["content"]
    assert res["latency_ms"] >= 0


def test_auth_error_no_retry():
    with pytest.raises(GeminiAuthError):
        GeminiProviderAdapter(mode="REAL_API", api_key="")


def test_rate_limit_retry_policy():
    err = GeminiRateLimitError("Rate limit exceeded", retry_after_sec=5)
    assert err.retry_after_sec == 5


@patch("urllib.request.urlopen")
def test_real_api_success_mocked(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"candidates":[{"content":{"parts":[{"text":"Hello from Real Gemini API"}]}}],"usageMetadata":{"promptTokenCount":10,"candidatesTokenCount":5,"totalTokenCount":15}}'
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    adapter = GeminiProviderAdapter(mode="REAL_API", api_key="test_fake_api_key")
    res = adapter.generate_content("Hello")

    assert res["status"] == "SUCCESS"
    assert res["gate"] == "GATE_B_REAL_API"
    assert res["content"] == "Hello from Real Gemini API"
    assert res["usage"]["is_estimated"] is False
    assert res["usage"]["total_token_count"] == 15


@patch("urllib.request.urlopen")
def test_real_api_auth_error_no_retry(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://test", code=401, msg="Unauthorized", hdrs={},
        fp=MagicMock(read=lambda: b"Invalid API Key")
    )

    adapter = GeminiProviderAdapter(mode="REAL_API", api_key="bad_key")
    with pytest.raises(GeminiAuthError) as excinfo:
        adapter.generate_content("Test")
    assert "HTTP 401" in str(excinfo.value)


@patch("urllib.request.urlopen")
def test_real_api_rate_limit_retry(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://test", code=429, msg="Too Many Requests",
        hdrs={"Retry-After": "1"},
        fp=MagicMock(read=lambda: b"Quota exceeded")
    )

    adapter = GeminiProviderAdapter(mode="REAL_API", api_key="test_key", max_retries=1)
    with pytest.raises(GeminiRateLimitError):
        adapter.generate_content("Test")


@patch("urllib.request.urlopen")
def test_real_api_timeout(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError(reason="timed out")

    adapter = GeminiProviderAdapter(mode="REAL_API", api_key="test_key", max_retries=1)
    with pytest.raises(GeminiTimeoutError):
        adapter.generate_content("Test")


# =====================================================================
# Work 23 — additional tests (added after fixing the 2 failures).
# Existing tests above are unchanged. All tests here are hermetic:
# no real Gemini API call, no dependence on the developer's environment.
# =====================================================================
import io
import json
import socket


@pytest.fixture(autouse=True)
def _no_real_network(monkeypatch):
    """Guard: any attempt to open a real socket fails the test loudly."""
    def _blocked(*a, **k):
        raise AssertionError("Real network access attempted in unit test")
    monkeypatch.setattr(socket.socket, "connect", _blocked)


@pytest.fixture
def no_sleep(monkeypatch):
    calls = []
    monkeypatch.setattr("time.sleep", lambda s: calls.append(s))
    return calls


def _http_error(code, body=b"err", headers=None):
    return urllib.error.HTTPError(
        url="https://example.invalid", code=code, msg=str(code),
        hdrs=headers or {}, fp=io.BytesIO(body),
    )


def _ok_response(body: bytes):
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__.return_value = resp
    return resp


# ---- missing / invalid key: must not depend on the machine environment ----

def test_empty_key_does_not_fall_back_to_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key_from_environment")
    with pytest.raises(GeminiAuthError):
        GeminiProviderAdapter(mode="REAL_API", api_key="")


def test_whitespace_key_rejected(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key_from_environment")
    with pytest.raises(GeminiAuthError):
        GeminiProviderAdapter(mode="REAL_API", api_key="   ")


def test_no_key_anywhere_real_api_raises(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(GeminiAuthError):
        GeminiProviderAdapter(mode="REAL_API")


def test_none_key_uses_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key_from_environment")
    adapter = GeminiProviderAdapter(mode="REAL_API")
    assert adapter.api_key == "key_from_environment"


def test_mock_mode_needs_no_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert GeminiProviderAdapter(mode="MOCK").api_key is None


# ---- security: key in header only, never in URL / exceptions ----

@patch("urllib.request.urlopen")
def test_key_sent_in_header_not_in_url(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}')
    GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123").generate_content("hi")
    req = mock_urlopen.call_args[0][0]
    assert "SECRET123" not in req.full_url
    assert "key=" not in req.full_url
    assert req.get_header("X-goog-api-key") == "SECRET123"


@patch("urllib.request.urlopen")
def test_timeout_value_passed_to_urlopen(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}')
    GeminiProviderAdapter(mode="REAL_API", api_key="k", timeout_sec=7.5).generate_content("hi")
    assert mock_urlopen.call_args.kwargs["timeout"] == 7.5


@patch("urllib.request.urlopen")
def test_key_redacted_in_auth_error(mock_urlopen):
    mock_urlopen.side_effect = _http_error(403, b"API key SECRET123 is not allowed")
    with pytest.raises(GeminiAuthError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123").generate_content("x")
    assert "SECRET123" not in str(exc.value)
    assert "[REDACTED_API_KEY]" in str(exc.value)


@patch("urllib.request.urlopen")
def test_key_redacted_in_network_error(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = urllib.error.URLError(reason="cannot reach host with SECRET123")
    with pytest.raises(GeminiTimeoutError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123", max_retries=1).generate_content("x")
    assert "SECRET123" not in str(exc.value)


@patch("urllib.request.urlopen")
def test_key_redacted_in_other_http_error(mock_urlopen):
    mock_urlopen.side_effect = _http_error(500, b"server saw SECRET123")
    with pytest.raises(GeminiAdapterError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123").generate_content("x")
    assert "SECRET123" not in str(exc.value)


# ---- 401/403: GeminiAuthError, exactly one attempt ----

@pytest.mark.parametrize("code", [401, 403])
@patch("urllib.request.urlopen")
def test_auth_codes_map_to_auth_error_single_attempt(mock_urlopen, code, no_sleep):
    mock_urlopen.side_effect = _http_error(code, b"denied")
    with pytest.raises(GeminiAuthError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=3).generate_content("x")
    assert f"HTTP {code}" in str(exc.value)
    assert mock_urlopen.call_count == 1
    assert no_sleep == []


# ---- 429: bounded retry; timeout: bounded retry; other errors: no retry ----

@patch("urllib.request.urlopen")
def test_429_retries_exactly_max_retries_then_raises(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = lambda *a, **k: (_ for _ in ()).throw(
        _http_error(429, b"quota", {"Retry-After": "2"}))
    with pytest.raises(GeminiRateLimitError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=3).generate_content("x")
    assert mock_urlopen.call_count == 4  # 1 initial + 3 retries
    assert exc.value.retry_after_sec == 2
    assert no_sleep == [2, 2, 2]


@patch("urllib.request.urlopen")
def test_429_then_success_recovers(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = [
        _http_error(429, b"quota", {"Retry-After": "1"}),
        _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}'),
    ]
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=3).generate_content("x")
    assert res["content"] == "ok"
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_network_error_retries_bounded(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = lambda *a, **k: (_ for _ in ()).throw(urllib.error.URLError("timed out"))
    with pytest.raises(GeminiTimeoutError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=2).generate_content("x")
    assert mock_urlopen.call_count == 3  # 1 initial + 2 retries


@patch("urllib.request.urlopen")
def test_http_500_not_retried(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = _http_error(500, b"boom")
    with pytest.raises(GeminiAdapterError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=3).generate_content("x")
    assert mock_urlopen.call_count == 1


# ---- response parsing / usage metadata ----

@patch("urllib.request.urlopen")
def test_usage_metadata_parsed(mock_urlopen):
    body = {"candidates": [{"content": {"parts": [{"text": "hi"}]}}],
            "usageMetadata": {"promptTokenCount": 3, "candidatesTokenCount": 4, "totalTokenCount": 7}}
    mock_urlopen.return_value = _ok_response(json.dumps(body).encode())
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")
    assert res["usage"] == {"prompt_token_count": 3, "candidates_token_count": 4,
                            "total_token_count": 7, "is_estimated": False}


@patch("urllib.request.urlopen")
def test_total_tokens_computed_when_missing(mock_urlopen):
    body = {"candidates": [{"content": {"parts": [{"text": "ok"}]}}],
            "usageMetadata": {"promptTokenCount": 3, "candidatesTokenCount": 4}}
    mock_urlopen.return_value = _ok_response(json.dumps(body).encode())
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")
    assert res["usage"]["total_token_count"] == 7
    assert res["content"] == "ok"


@patch("urllib.request.urlopen")
def test_invalid_json_response(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b"<html>not json</html>")
    with pytest.raises(GeminiInvalidResponseError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")


@patch("urllib.request.urlopen")
def test_system_instruction_and_generation_config_in_payload(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}')
    GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content(
        "x", system_instruction="be brief", temperature=0.1, max_output_tokens=64)
    sent = json.loads(mock_urlopen.call_args[0][0].data.decode())
    assert sent["systemInstruction"]["parts"][0]["text"] == "be brief"
    assert sent["generationConfig"] == {"temperature": 0.1, "maxOutputTokens": 64}


# =====================================================================
# Work 23 — round 2: raw timeouts, Retry-After cap, default model.
# =====================================================================

# ---- raw TimeoutError / socket.timeout (not wrapped in URLError) ----

@patch("urllib.request.urlopen")
def test_raw_timeout_error_retries_bounded_then_maps(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = lambda *a, **k: (_ for _ in ()).throw(TimeoutError("timed out"))
    with pytest.raises(GeminiTimeoutError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=2).generate_content("x")
    assert mock_urlopen.call_count == 3  # 1 initial + 2 retries


@patch("urllib.request.urlopen")
def test_socket_timeout_during_read_is_mapped(mock_urlopen, no_sleep):
    resp = MagicMock()
    resp.read.side_effect = socket.timeout("read timed out")
    resp.__enter__.return_value = resp
    mock_urlopen.return_value = resp
    with pytest.raises(GeminiTimeoutError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=1).generate_content("x")
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_raw_timeout_then_success_recovers(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = [
        TimeoutError("timed out"),
        _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}'),
    ]
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=2).generate_content("x")
    assert res["content"] == "ok"
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_key_redacted_in_raw_timeout_error(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = TimeoutError("stalled while sending SECRET123")
    with pytest.raises(GeminiTimeoutError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123", max_retries=1).generate_content("x")
    assert "SECRET123" not in str(exc.value)


# ---- Retry-After handling ----

@patch("urllib.request.urlopen")
def test_retry_after_is_capped(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = lambda *a, **k: (_ for _ in ()).throw(
        _http_error(429, b"quota", {"Retry-After": "99999"}))
    with pytest.raises(GeminiRateLimitError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=2).generate_content("x")
    cap = GeminiProviderAdapter.MAX_RETRY_AFTER_SEC
    assert no_sleep == [cap, cap]
    assert exc.value.retry_after_sec == cap
    assert mock_urlopen.call_count == 3


@patch("urllib.request.urlopen")
def test_retry_after_non_numeric_uses_default(mock_urlopen, no_sleep):
    mock_urlopen.side_effect = lambda *a, **k: (_ for _ in ()).throw(
        _http_error(429, b"quota", {"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}))
    with pytest.raises(GeminiRateLimitError):
        GeminiProviderAdapter(mode="REAL_API", api_key="k", max_retries=1).generate_content("x")
    assert no_sleep == [5]


# ---- default model ----

SHUTDOWN_MODELS = {"gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-8b",
                   "gemini-2.0-flash", "gemini-2.0-flash-lite"}


def test_default_model_is_not_a_known_shutdown_model(monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL_NAME", raising=False)
    adapter = GeminiProviderAdapter(mode="MOCK")
    assert adapter.model_name == GeminiProviderAdapter.DEFAULT_GEMINI_MODEL
    assert adapter.model_name not in SHUTDOWN_MODELS


def test_model_name_env_and_argument_override(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL_NAME", "model-from-env")
    assert GeminiProviderAdapter(mode="MOCK").model_name == "model-from-env"
    assert GeminiProviderAdapter(mode="MOCK", model_name="explicit").model_name == "explicit"


@patch("urllib.request.urlopen")
def test_request_url_uses_model_and_has_no_query(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}],"usageMetadata":{}}')
    GeminiProviderAdapter(mode="REAL_API", api_key="k", model_name="m-x").generate_content("x")
    url = mock_urlopen.call_args[0][0].full_url
    assert url.endswith("/models/m-x:generateContent")
    assert "?" not in url


@patch("urllib.request.urlopen")
def test_empty_candidate_content_is_not_reported_as_success(mock_urlopen):
    mock_urlopen.return_value = _ok_response(b'{"candidates":[],"usageMetadata":{}}')
    with pytest.raises(GeminiInvalidResponseError, match="no textual candidate content"):
        GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")


@patch("urllib.request.urlopen")
def test_multiple_text_parts_are_aggregated(mock_urlopen):
    body = {"candidates": [{"content": {"parts": [{"text": "Hello "}, {"text": "world"}]}}],
            "usageMetadata": {}}
    mock_urlopen.return_value = _ok_response(json.dumps(body).encode())
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")
    assert res["content"] == "Hello world"



# =====================================================================
# Work 23 — round 3: MAX_TOKENS diagnostics and truncation visibility.
# Additive behaviour only: existing keys/values are unchanged.
# =====================================================================

def _body(parts, finish=None, usage=None):
    cand = {"content": {"parts": parts}}
    if finish is not None:
        cand["finishReason"] = finish
    return json.dumps({"candidates": [cand], "usageMetadata": usage or {}}).encode()


@patch("urllib.request.urlopen")
def test_max_tokens_without_text_reports_budget_diagnostics(mock_urlopen):
    mock_urlopen.return_value = _ok_response(
        _body([], "MAX_TOKENS", {"promptTokenCount": 17, "thoughtsTokenCount": 32}))
    with pytest.raises(GeminiInvalidResponseError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123", max_retries=0).generate_content(
            "x", max_output_tokens=32)
    msg = str(exc.value)
    assert "no textual candidate content" in msg and "MAX_TOKENS" in msg
    assert "thoughts_tokens=32" in msg and "max_output_tokens=32" in msg
    assert "SECRET123" not in msg
    assert mock_urlopen.call_count == 1  # not retried


@patch("urllib.request.urlopen")
def test_provider_values_in_diagnostics_are_redacted(mock_urlopen):
    mock_urlopen.return_value = _ok_response(
        _body([], "MAX_TOKENS", {"thoughtsTokenCount": "leak-SECRET123"}))
    with pytest.raises(GeminiInvalidResponseError) as exc:
        GeminiProviderAdapter(mode="REAL_API", api_key="SECRET123").generate_content("x")
    assert "SECRET123" not in str(exc.value)


@patch("urllib.request.urlopen")
def test_finish_reason_is_returned_on_success(mock_urlopen):
    mock_urlopen.return_value = _ok_response(_body([{"text": "ok"}], "STOP"))
    assert GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")["finish_reason"] == "STOP"


@patch("urllib.request.urlopen")
def test_truncated_partial_text_is_visible_via_finish_reason(mock_urlopen):
    mock_urlopen.return_value = _ok_response(_body([{"text": "WORK23_"}], "MAX_TOKENS"))
    res = GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")
    assert res["content"] == "WORK23_" and res["finish_reason"] == "MAX_TOKENS"


@patch("urllib.request.urlopen")
def test_finish_reason_none_when_api_omits_it(mock_urlopen):
    mock_urlopen.return_value = _ok_response(_body([{"text": "ok"}]))
    assert GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")["finish_reason"] is None


@patch("urllib.request.urlopen")
def test_thoughts_token_count_only_when_provided(mock_urlopen):
    mock_urlopen.return_value = _ok_response(
        _body([{"text": "ok"}], "STOP", {"promptTokenCount": 1, "candidatesTokenCount": 2, "thoughtsTokenCount": 9}))
    usage = GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")["usage"]
    assert usage["thoughts_token_count"] == 9 and usage["is_estimated"] is False
    mock_urlopen.return_value = _ok_response(_body([{"text": "ok"}], "STOP", {"promptTokenCount": 1}))
    assert "thoughts_token_count" not in GeminiProviderAdapter(mode="REAL_API", api_key="k").generate_content("x")["usage"]
