import os
import time
import re
import socket
import urllib.request
import urllib.error
import json
from typing import Dict, Any, Optional


class GeminiAdapterError(Exception):
    """Base exception class for Gemini Provider Adapter"""
    pass


class GeminiInvalidModeError(GeminiAdapterError):
    pass


class GeminiAuthError(GeminiAdapterError):
    """HTTP 401/403: Permanent error - DO NOT RETRY"""
    pass


class GeminiRateLimitError(GeminiAdapterError):
    """HTTP 429: Rate limit or quota exceeded - RETRY WITH BACKOFF"""

    def __init__(self, message: str, retry_after_sec: Optional[int] = None):
        super().__init__(message)
        self.retry_after_sec = retry_after_sec


class GeminiTimeoutError(GeminiAdapterError):
    """Network or execution timeout - RETRYABLE"""
    pass


class GeminiInvalidResponseError(GeminiAdapterError):
    """Malformed or invalid structure in response"""
    pass


class GeminiProviderAdapter:
    VALID_MODES = {"MOCK", "REAL_API"}
    # Default model. Override with model_name= or the GEMINI_MODEL_NAME environment variable.
    DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
    # Upper bound for a server-supplied Retry-After value.
    MAX_RETRY_AFTER_SEC = 60

    def __init__(
        self,
        mode: str = "MOCK",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout_sec: float = 30.0,
        max_retries: int = 3
    ):
        if mode not in self.VALID_MODES:
            raise GeminiInvalidModeError(
                f"Invalid mode '{mode}'. Allowed modes are: {sorted(list(self.VALID_MODES))}"
            )
        self.mode = mode
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries
        self.model_name = model_name or os.getenv("GEMINI_MODEL_NAME", self.DEFAULT_GEMINI_MODEL)

        # Explicit api_key is authoritative. Fall back to the environment only when
        # api_key was not provided at all (None); a blank explicit key fails closed.
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        self.api_key = api_key.strip() if isinstance(api_key, str) else None
        if self.mode == "REAL_API" and not self.api_key:
            raise GeminiAuthError("GEMINI_API_KEY is missing while mode is set to REAL_API.")

    def _redact(self, text: Any) -> str:
        """Remove the API key from any text that may reach an exception message."""
        text = str(text)
        if self.api_key:
            text = text.replace(self.api_key, "[REDACTED_API_KEY]")
        return text

    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ) -> Dict[str, Any]:
        if not prompt or not prompt.strip():
            raise GeminiInvalidResponseError("Prompt cannot be empty.")

        start_time = time.time()

        if self.mode == "MOCK":
            return self._execute_mock(prompt, start_time)
        else:
            return self._execute_real_api(prompt, system_instruction, temperature, max_output_tokens, start_time)

    def _execute_mock(self, prompt: str, start_time: float) -> Dict[str, Any]:
        words = len(re.findall(r'\w+', prompt))
        est_prompt_tokens = int(words * 1.3)
        mock_reply = f"[MOCK_GEMINI_RESPONSE] Processed prompt: '{prompt[:40]}...'"
        est_completion_tokens = int(len(re.findall(r'\w+', mock_reply)) * 1.3)

        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "status": "SUCCESS",
            "gate": "GATE_A_MOCK",
            "provider": "gemini",
            "model": self.model_name,
            "content": mock_reply,
            "usage": {
                "estimated_prompt_tokens": est_prompt_tokens,
                "estimated_completion_tokens": est_completion_tokens,
                "estimated_total_tokens": est_prompt_tokens + est_completion_tokens,
                "is_estimated": True
            },
            "latency_ms": latency_ms
        }

    def _execute_real_api(
        self,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float,
        max_output_tokens: int,
        start_time: float
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise GeminiAuthError("API key is required for REAL_API execution.")

        # The API key is sent in the x-goog-api-key header, never in the URL.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        attempts = 0
        while attempts <= self.max_retries:
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_sec) as response:
                    res_body = response.read().decode("utf-8")
                    data = json.loads(res_body)

                    usage_meta = data.get("usageMetadata", {})
                    prompt_tokens = usage_meta.get("promptTokenCount", 0)
                    candidates_tokens = usage_meta.get("candidatesTokenCount", 0)
                    total_tokens = usage_meta.get("totalTokenCount", prompt_tokens + candidates_tokens)
                    # Thinking models spend part of maxOutputTokens on internal "thoughts";
                    # report it when the API provides it (diagnostics for MAX_TOKENS failures).
                    thoughts_tokens = usage_meta.get("thoughtsTokenCount")

                    # Aggregate the textual parts of the first candidate. An HTTP 200 without
                    # candidate text is not a successful generation.
                    candidates = data.get("candidates", [])
                    content_text = ""
                    finish_reason = None
                    if candidates and isinstance(candidates[0], dict):
                        candidate = candidates[0]
                        finish_reason = candidate.get("finishReason")
                        parts = candidate.get("content", {}).get("parts", [])
                        if isinstance(parts, list):
                            content_text = "".join(
                                part.get("text", "")
                                for part in parts
                                if isinstance(part, dict) and isinstance(part.get("text"), str)
                            )

                    if not content_text.strip():
                        block_reason = data.get("promptFeedback", {}).get("blockReason")
                        detail = f" (prompt blocked: {block_reason})" if block_reason else (
                            f" (finish reason: {finish_reason})" if finish_reason else ""
                        )
                        # Only provider-supplied values are passed through _redact.
                        usage_detail = (
                            f" [prompt_tokens={self._redact(prompt_tokens)}, "
                            f"thoughts_tokens={self._redact(thoughts_tokens)}, "
                            f"candidates_tokens={self._redact(candidates_tokens)}, "
                            f"max_output_tokens={max_output_tokens}]"
                        )
                        raise GeminiInvalidResponseError(
                            "Gemini API returned no textual candidate content" + detail + usage_detail
                        )

                    latency_ms = int((time.time() - start_time) * 1000)

                    usage = {
                        "prompt_token_count": prompt_tokens,
                        "candidates_token_count": candidates_tokens,
                        "total_token_count": total_tokens,
                        "is_estimated": False
                    }
                    if thoughts_tokens is not None:
                        usage["thoughts_token_count"] = thoughts_tokens

                    return {
                        "status": "SUCCESS",
                        "gate": "GATE_B_REAL_API",
                        "provider": "gemini",
                        "model": self.model_name,
                        "content": content_text,
                        # Lets callers detect truncation (e.g. "MAX_TOKENS") instead of treating
                        # partial text as a complete answer.
                        "finish_reason": finish_reason,
                        "usage": usage,
                        "latency_ms": latency_ms
                    }

            except urllib.error.HTTPError as e:
                code = e.code
                err_msg = e.read().decode("utf-8", errors="ignore")
                sanitized_msg = self._redact(err_msg)

                if code in (401, 403):
                    raise GeminiAuthError(f"Authentication/Authorization failed (HTTP {code}): {sanitized_msg}")
                elif code == 429:
                    retry_after = e.headers.get("Retry-After")
                    sec = int(retry_after) if retry_after and retry_after.isdigit() else 5
                    sec = min(sec, self.MAX_RETRY_AFTER_SEC)
                    attempts += 1
                    if attempts > self.max_retries:
                        raise GeminiRateLimitError(f"Rate limit exceeded (HTTP 429) after {self.max_retries} retries.", retry_after_sec=sec)
                    time.sleep(sec)
                    continue
                else:
                    raise GeminiAdapterError(f"Gemini API HTTP Error {code}: {sanitized_msg}")

            except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
                # HTTPError (a URLError subclass) is handled above; raw socket timeouts are not
                # wrapped in URLError, so they are caught here too.
                attempts += 1
                if attempts > self.max_retries:
                    reason = getattr(e, "reason", None) or e
                    raise GeminiTimeoutError(f"Network timeout or unreachable endpoint after {self.max_retries} retries: {self._redact(reason)}")
                time.sleep(2 ** attempts)
                continue
            except json.JSONDecodeError as e:
                raise GeminiInvalidResponseError(f"Failed to parse JSON response from Gemini API: {self._redact(e)}")

        raise GeminiTimeoutError("Max retries exceeded for Gemini API request.")
