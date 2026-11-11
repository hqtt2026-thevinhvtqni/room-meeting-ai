from __future__ import annotations

import json
import os
from urllib import error, request
from urllib.parse import quote, urlsplit
from typing import Any


class AuthorityClientError(RuntimeError):
    def __init__(self, code: str, status_code: int = 503):
        super().__init__(code)
        self.code = code
        self.status_code = status_code


class CoreAuthorityClient:
    """Execution Host client. Every authorization decision is fetched online."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        service_id: str | None = None,
        credential: str | None = None,
        timeout: float = 5.0,
        transport=None,
    ):
        self.base_url = (
            base_url or os.getenv("ROOM_HOP_CORE_AUTHORITY_URL", "")
        ).rstrip("/")
        parsed = urlsplit(self.base_url)
        loopback_http = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
        if not self.base_url or parsed.username or parsed.password or parsed.query or parsed.fragment or not (parsed.scheme == "https" or loopback_http):
            raise AuthorityClientError("core_authority_url_must_use_https_or_loopback_http", 503)
        self.service_id = (
            service_id or os.getenv("ROOM_HOP_EXECUTION_HOST_ID", "")
        )
        self.credential = (
            credential or os.getenv("ROOM_HOP_EXECUTION_HOST_CREDENTIAL", "")
        )
        self.timeout = timeout
        self.transport = transport or self._http_transport
        if not self.base_url or not self.service_id or not self.credential:
            raise AuthorityClientError("core_authority_client_not_configured", 503)

    @staticmethod
    def _http_transport(url: str, method: str, body: bytes | None, headers: dict, timeout: float):
        req = request.Request(url, data=body, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=timeout) as response:
                return response.status, response.read()
        except error.HTTPError as exc:
            return exc.code, exc.read()
        except (error.URLError, TimeoutError, OSError):
            raise AuthorityClientError("core_authority_unreachable", 503) from None

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        grant_token: str | None = None,
    ) -> dict[str, Any]:
        headers = {
            "Accept": "application/json",
            "X-ROOM-HOP-SERVICE-ID": self.service_id,
            "X-ROOM-HOP-SERVICE-CREDENTIAL": self.credential,
        }
        body = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if grant_token:
            headers["Authorization"] = "Bearer " + grant_token
        status, raw = self.transport(
            self.base_url + path, method, body, headers, self.timeout
        )
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeError, json.JSONDecodeError):
            raise AuthorityClientError("core_authority_invalid_response", 503) from None
        if status < 200 or status >= 300:
            detail = data.get("detail", "core_authority_request_failed") if isinstance(data, dict) else "core_authority_request_failed"
            raise AuthorityClientError(str(detail), status)
        if not isinstance(data, dict):
            raise AuthorityClientError("core_authority_invalid_response", 503)
        return data

    def validate_grant(self, work_id: str, grant_id: str, token: str) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/works/{quote(work_id, safe='')}/execution-grants/{quote(grant_id, safe='')}/validate",
            grant_token=token,
        )

    def start_run(
        self,
        work_id: str,
        grant_id: str,
        token: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/works/{quote(work_id, safe='')}/execution-grants/{quote(grant_id, safe='')}/runs",
            payload=record,
            grant_token=token,
        )

    def complete_run(
        self,
        work_id: str,
        grant_id: str,
        token: str,
        run_id: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/works/{quote(work_id, safe='')}/execution-grants/{quote(grant_id, safe='')}/runs/{quote(run_id, safe='')}/complete",
            payload=record,
            grant_token=token,
        )

    def record_run(
        self,
        work_id: str,
        grant_id: str,
        token: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        """Compatibility alias; callers must have created the Run Record first."""
        return self.complete_run(
            work_id, grant_id, token, str(record["run_id"]), record
        )
