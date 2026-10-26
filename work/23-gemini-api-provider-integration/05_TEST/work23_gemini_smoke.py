"""Work 23 - Gemini REAL_API adapter smoke (synthetic prompt only, one call, no retries).

Run from the repository root:  python <path>\\work23_gemini_smoke.py
Reads GEMINI_API_KEY from the environment; the key is never printed (all output is redacted).

Exit codes: 0 PASS | 20 BLOCKED_NO_KEY | 21 empty content | 22 unexpected content
            23 truncated / abnormal finish_reason | 24 adapter error | 25 malformed result
PASS requires real text containing WORK23_OK, status SUCCESS, gate GATE_B_REAL_API and
finish_reason STOP (when the API reports one). HTTP 200 alone is never a PASS.
"""
import os
import re
import sys
import traceback

EXPECTED = "WORK23_OK"
# Gemini "thinking" models spend part of maxOutputTokens on internal thoughts, so 32 tokens can be
# exhausted before any text is produced (finishReason=MAX_TOKENS). 256 leaves headroom for a
# one-word answer; this is a budget choice, the adapter logic is unchanged.
MAX_OUTPUT_TOKENS = 256
PROMPT = "Reply with exactly: " + EXPECTED
SYSTEM = "This is a synthetic integration smoke test. Do not include anything else."

EXIT_OK, EXIT_NO_KEY, EXIT_EMPTY, EXIT_MISMATCH = 0, 20, 21, 22
EXIT_TRUNCATED, EXIT_ADAPTER_ERROR, EXIT_BAD_RESULT = 23, 24, 25

_KEY_LIKE = re.compile(r"AIza[0-9A-Za-z_\-]{20,}")


def redact(text, key=None):
    text = str(text)
    if key:
        text = text.replace(key, "[REDACTED_API_KEY]")
    return _KEY_LIKE.sub("[REDACTED_API_KEY]", text)


def run(adapter, key=None, out=print):
    """Execute one adapter call and classify it. Returns the exit code."""

    def emit(line):
        out(redact(line, key))

    try:
        result = adapter.generate_content(
            prompt=PROMPT,
            system_instruction=SYSTEM,
            temperature=0,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as exc:  # noqa: BLE001 - classify every failure, keep traceback (redacted)
        emit("REAL_API_ADAPTER=FAIL; ERROR_TYPE=" + type(exc).__name__)
        emit("ERROR_MESSAGE=" + str(exc))
        for line in traceback.format_exception(exc):
            for sub in line.rstrip().splitlines():
                emit("TRACE| " + sub)
        if "MAX_TOKENS" in str(exc):
            emit(
                "DIAGNOSIS=OUTPUT_BUDGET_EXHAUSTED at max_output_tokens=%d; see token breakdown in "
                "ERROR_MESSAGE (thoughts_tokens). Not retried." % MAX_OUTPUT_TOKENS
            )
        else:
            emit("DIAGNOSIS=ROOT_CAUSE_UNCONFIRMED; not retried.")
        return EXIT_ADAPTER_ERROR

    if not isinstance(result, dict):
        emit("REAL_API_ADAPTER=FAIL; MALFORMED_RESULT_TYPE=" + type(result).__name__)
        return EXIT_BAD_RESULT
    if result.get("status") != "SUCCESS" or result.get("gate") != "GATE_B_REAL_API":
        emit("REAL_API_ADAPTER=FAIL; STATUS=%r; GATE=%r" % (result.get("status"), result.get("gate")))
        return EXIT_BAD_RESULT

    content = result.get("content")
    if not isinstance(content, str) or not content.strip():
        emit("REAL_API_ADAPTER=FAIL; EMPTY_CONTENT")
        return EXIT_EMPTY

    finish = result.get("finish_reason")
    emit("FINISH_REASON=" + str(finish))
    emit("USAGE=" + repr(result.get("usage", {})))
    if finish is not None and finish != "STOP":
        emit("REAL_API_ADAPTER=FAIL; TRUNCATED_OR_ABNORMAL_FINISH=" + str(finish))
        return EXIT_TRUNCATED
    if EXPECTED not in content:
        emit("REAL_API_ADAPTER=FAIL; UNEXPECTED_CONTENT_LEN=%d" % len(content))
        emit("CONTENT_HEAD=" + content[:80].replace("\n", " "))
        return EXIT_MISMATCH

    emit("REAL_API_ADAPTER=PASS")
    emit("PROVIDER=" + str(result.get("provider")))
    emit("MODEL=" + str(result.get("model")))
    emit("CONTENT_NONEMPTY=True; CONTAINS_%s=True" % EXPECTED)
    emit("LATENCY_MS=" + str(result.get("latency_ms", "unavailable")))
    return EXIT_OK


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key or not key.strip():
        print("BLOCKED_NO_KEY (key not printed or requested)")
        return EXIT_NO_KEY
    sys.path.insert(0, os.getcwd())
    from core.gemini_provider_adapter import GeminiProviderAdapter

    adapter = GeminiProviderAdapter(mode="REAL_API", api_key=key, timeout_sec=20, max_retries=0)
    return run(adapter, key=key)


if __name__ == "__main__":
    sys.exit(main())
