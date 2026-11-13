from __future__ import annotations

import ipaddress
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from .core_authority_client import AuthorityClientError, CoreAuthorityClient
from .granted_host import GrantedExecutionHost


_LOOPBACK_HOSTNAMES = {"127.0.0.1", "localhost", "::1"}


def _loopback_authority(value: str | None, expected_port: int) -> bool:
    if not value or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit("//" + value)
        return (
            parsed.hostname is not None
            and parsed.hostname.lower() in _LOOPBACK_HOSTNAMES
            and parsed.port == expected_port
            and parsed.username is None
            and parsed.password is None
            and not parsed.path
            and not parsed.query
            and not parsed.fragment
        )
    except ValueError:
        return False


def _request_origin_allowed(headers, expected_port: int) -> bool:
    if not _loopback_authority(headers.get("Host"), expected_port):
        return False
    origin = headers.get("Origin")
    if origin is not None:
        try:
            parsed = urlsplit(origin)
            if (
                parsed.scheme != "http"
                or parsed.hostname is None
                or parsed.hostname.lower() not in _LOOPBACK_HOSTNAMES
                or parsed.port != expected_port
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path not in ("",)
                or parsed.query
                or parsed.fragment
            ):
                return False
        except ValueError:
            return False
    fetch_site = (headers.get("Sec-Fetch-Site") or "").lower()
    if fetch_site and fetch_site not in {"same-origin", "none"}:
        return False
    return True


class Handler(BaseHTTPRequestHandler):
    host: GrantedExecutionHost | None = None
    expected_port: int = 8031

    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/health":
            if not _request_origin_allowed(self.headers, self.expected_port):
                self._send(403, {"status": "BLOCKED", "reason": "loopback_host_origin_required"})
                return
            if self.host is None:
                self._send(503, {
                    "status": "BLOCKED",
                    "reason": "core_authority_client_not_configured",
                })
                return
            self._send(200, {
                "status": "PASS",
                "service": "execution-host",
                **self.host.identity(),
            })
            return
        self._send(404, {"status": "NOT_FOUND"})

    def do_POST(self) -> None:
        if urlsplit(self.path).path != "/execute-granted":
            # The former caller-supplied /execute + WorkContext contract is
            # intentionally retired from the HTTP surface.
            self._send(404, {"status": "NOT_FOUND"})
            return
        if not _request_origin_allowed(self.headers, self.expected_port):
            self._send(403, {"status": "BLOCKED", "reason": "loopback_host_origin_required"})
            return
        if self.host is None:
            self._send(503, {
                "status": "BLOCKED",
                "reason": "core_authority_client_not_configured",
            })
            return
        if self.headers.get_content_type() != "application/json":
            self._send(415, {"status": "BLOCKED", "reason": "application_json_required"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(400, {"status": "BLOCKED", "reason": "invalid_content_length"})
            return
        if length < 1 or length > 16384:
            self._send(413, {"status": "BLOCKED", "reason": "request_body_size_invalid"})
            return
        try:
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict) or set(body) != {"work_id", "grant_id", "grant_token"}:
                raise ValueError("request_schema_invalid")
            if not all(isinstance(body[key], str) and body[key] for key in body):
                raise ValueError("request_schema_invalid")
            result = self.host.execute_for_work(
                body["work_id"], body["grant_id"], body["grant_token"]
            )
            status = result.get("status", "BLOCKED")
            code = 200 if status in {"PASS", "FAILED", "TIMEOUT"} else 403
            self._send(code, result)
        except (UnicodeError, json.JSONDecodeError, ValueError):
            self._send(400, {"status": "BLOCKED", "reason": "request_schema_invalid"})
        except AuthorityClientError as exc:
            self._send(exc.status_code, {"status": "BLOCKED", "reason": exc.code})
        except Exception as exc:
            self._send(500, {
                "status": "BLOCKED",
                "reason": "execution_host_internal_error:" + type(exc).__name__,
            })

    def log_message(self, *_args) -> None:
        # Do not log request bodies, bearer grants or service credentials.
        return


def _loopback_host(value: str) -> str:
    host = value.strip()
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        if host.lower() == "localhost":
            return "127.0.0.1"
        raise RuntimeError("Execution Host must bind to a loopback IP.") from None
    if not address.is_loopback:
        raise RuntimeError(
            "Execution Host remote bind is disabled until TLS and authenticated transport are implemented."
        )
    return host


def serve(host: str | None = None, port: int | None = None) -> None:
    bind_host = _loopback_host(
        host or os.getenv("ROOM_HOP_EXECUTION_HOST_BIND", "127.0.0.1")
    )
    bind_port = port or int(os.getenv("ROOM_HOP_EXECUTION_HOST_PORT", "8031"))
    Handler.expected_port = bind_port
    try:
        authority_client = CoreAuthorityClient()
        Handler.host = GrantedExecutionHost(authority_client)
    except AuthorityClientError:
        Handler.host = None
    ThreadingHTTPServer((bind_host, bind_port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
