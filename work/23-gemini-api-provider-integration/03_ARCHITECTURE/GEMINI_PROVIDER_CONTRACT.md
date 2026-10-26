# Gemini Provider Contract — Work 23
Date: 2026-10-10
Status: DRAFT — adapter implemented; prior 40-test suite and live API calls passed before the latest response-validation patch. Regression suite and adapter live-call must be rerun after that patch; MCP/Core E2E remains NOT VERIFIED.

## Method
`GeminiProviderAdapter(mode="MOCK"|"REAL_API", api_key=None, model_name=None, timeout_sec=30.0, max_retries=3)`

`generate_content(prompt, system_instruction=None, temperature=0.7, max_output_tokens=2048)`

## Modes
- `MOCK`: no network, no key needed. Returns status SUCCESS, gate `GATE_A_MOCK`, provider gemini, configured model, clearly labeled mock content, estimated usage (`is_estimated=true`), `latency_ms`.
- `REAL_API`: calls `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`. Returns gate `GATE_B_REAL_API` with usage taken from `usageMetadata` (`is_estimated=false`).

## API key handling (fail closed)
- An explicit `api_key` argument is authoritative. `GEMINI_API_KEY` is read from the environment ONLY when `api_key is None`.
- An empty or blank explicit key never falls back to the environment; in `REAL_API` it raises `GeminiAuthError` at construction.
- The key is sent only in the `x-goog-api-key` header. It must never appear in the URL, query string, logs, exceptions or evidence. All error text passes through `_redact()` (`[REDACTED_API_KEY]`).

## Model
- Default: `gemini-3.8-flash`. Override with `model_name=` or `GEMINI_MODEL_NAME`.
- The previous default `gemini-1.5-flash` is shut down on the Gemini API; `gemini-2.0-flash` and `gemini-2.0-flash-lite` shut down on 2026-06-01. Source: Google "Gemini deprecations" page, last updated 2026-10-09.
- Model availability for a given API key/project has NOT been confirmed by a live call. Re-check the deprecations page before release.

## Error mapping
| Condition | Exception | Retried? |
|---|---|---|
| Invalid mode | `GeminiInvalidModeError` | no |
| Missing/blank key in REAL_API | `GeminiAuthError` | no |
| HTTP 401 / 403 | `GeminiAuthError` (message contains `HTTP <code>`) | **never** (exactly 1 attempt) |
| HTTP 429 | `GeminiRateLimitError(retry_after_sec)` after retries | yes, up to `max_retries`, sleeping `Retry-After` (non-numeric → 5s; capped at `MAX_RETRY_AFTER_SEC` = 60s) |
| `URLError`, `TimeoutError`, `socket.timeout` (incl. during `read()`) | `GeminiTimeoutError` after retries | yes, up to `max_retries`, backoff `2**attempt` s |
| Other HTTP status (e.g. 400, 404, 500) | `GeminiAdapterError` | no |
| Non-JSON response body | `GeminiInvalidResponseError` | no |
| Empty prompt | `GeminiInvalidResponseError` | no |

Total attempts = 1 + `max_retries`. Per-attempt timeout = `timeout_sec` (passed to `urlopen`).

## Response parsing
Text = concatenate all textual parts in the first candidate. If no non-empty textual content is returned, raise `GeminiInvalidResponseError` rather than returning `status=SUCCESS` with empty content. Usage: `prompt_token_count`, `candidates_token_count`, `total_token_count` (computed as prompt + candidates if the total is absent), `is_estimated=false`.

## Known gaps (still open)
- Caller, purpose, data classification and correlation ID are not in the method contract.
- Policy gate, model registry, budget guard and audit integration are not wired.
- No live API verification; no MCP/Core integration test.
- Only the first candidate is considered; multi-candidate selection and provider safety-block response taxonomy still need explicit handling. Empty/missing textual content is rejected.

## Compatibility
Inspect the authorized repository and preserve the existing Core/MCP contract. Do not create a parallel Core or bypass policy. Fail closed when policy/classification is unknown.
