"""Offline tests for the Work 23 smoke classifier. No network, no key."""
import importlib.util
from pathlib import Path

import pytest

_smoke_path = Path(__file__).with_name("work23_gemini_smoke.py")
_spec = importlib.util.spec_from_file_location("work23_gemini_smoke", _smoke_path)
smoke = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(smoke)

SECRET = "AIzaSyFAKEFAKEFAKEFAKEFAKEFAKEFAKE12345"


class Adapter:
    def __init__(self, result=None, exc=None):
        self.result, self.exc, self.kwargs = result, exc, None

    def generate_content(self, **kwargs):
        self.kwargs = kwargs
        if self.exc:
            raise self.exc
        return self.result


def good(**over):
    r = {"status": "SUCCESS", "gate": "GATE_B_REAL_API", "provider": "gemini", "model": "m",
         "content": "WORK23_OK", "finish_reason": "STOP", "usage": {"is_estimated": False}, "latency_ms": 5}
    r.update(over)
    return r


def run(adapter, key=None):
    lines = []
    code = smoke.run(adapter, key=key, out=lines.append)
    return code, "\n".join(lines)


def test_pass_and_budget_is_256_not_32():
    a = Adapter(good())
    code, out = run(a)
    assert code == smoke.EXIT_OK and "REAL_API_ADAPTER=PASS" in out
    assert a.kwargs["max_output_tokens"] == 256 and a.kwargs["temperature"] == 0
    assert a.kwargs["prompt"].endswith("WORK23_OK")


def test_pass_accepts_missing_finish_reason():
    assert run(Adapter(good(finish_reason=None)))[0] == smoke.EXIT_OK


@pytest.mark.parametrize("content", ["", "   ", None, 5])
def test_empty_or_non_text_content_fails(content):
    assert run(Adapter(good(content=content)))[0] == smoke.EXIT_EMPTY


def test_wrong_text_fails_even_with_http_success():
    assert run(Adapter(good(content="hello")))[0] == smoke.EXIT_MISMATCH


def test_truncated_text_fails():
    code, out = run(Adapter(good(content="WORK23_", finish_reason="MAX_TOKENS")))
    assert code == smoke.EXIT_TRUNCATED and "MAX_TOKENS" in out


@pytest.mark.parametrize("bad", [None, "x", {"status": "FAIL"}, good(gate="GATE_A_MOCK")])
def test_malformed_or_mock_result_fails(bad):
    assert run(Adapter(bad))[0] == smoke.EXIT_BAD_RESULT


def test_adapter_error_keeps_traceback_and_redacts_key():
    code, out = run(Adapter(exc=RuntimeError("boom with " + SECRET)), key=SECRET)
    assert code == smoke.EXIT_ADAPTER_ERROR
    assert "RuntimeError" in out and "TRACE|" in out
    assert SECRET not in out and "[REDACTED_API_KEY]" in out


def test_key_like_strings_are_redacted_even_without_known_key():
    code, out = run(Adapter(exc=RuntimeError("leak " + SECRET)), key=None)
    assert SECRET not in out


def test_max_tokens_error_gets_diagnosis_and_no_retry():
    a = Adapter(exc=RuntimeError("no textual candidate content (finish reason: MAX_TOKENS) [thoughts_tokens=256]"))
    code, out = run(a)
    assert code == smoke.EXIT_ADAPTER_ERROR and "OUTPUT_BUDGET_EXHAUSTED" in out
