"""WP18 — Core grant fetch boundary (fail-closed).

Core is the only runtime grant authority. FileGrantSource is an explicit
offline/test adapter and is never selected automatically.
Client body never supplies grants.
"""
from __future__ import annotations

import ipaddress
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Protocol

from .work28_grant import ExecutionGrant, GrantError
from .work28_grant_registry import load_grant_registry

CORE_GRANT_URL_ENV = "ROOM_HOP_CORE_GRANT_URL"
CORE_GRANT_TOKEN_ENV = "ROOM_HOP_CORE_GRANT_TOKEN"


def validate_core_grant_url(url: str) -> str:
    """Allow HTTPS remotely and HTTP only for loopback development endpoints."""
    if not isinstance(url, str) or not url.strip():
        raise GrantError("core_grant_url_required")
    try:
        parsed = urllib.parse.urlsplit(url.strip())
        hostname = parsed.hostname
        parsed.port  # Validate malformed and out-of-range ports.
    except ValueError as exc:
        raise GrantError("core_grant_url_invalid") from exc
    if (
        parsed.scheme not in ("https", "http")
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise GrantError("core_grant_url_invalid")
    if parsed.scheme == "http":
        host = hostname.rstrip(".").lower()
        is_loopback = host == "localhost"
        if not is_loopback:
            try:
                is_loopback = ipaddress.ip_address(host).is_loopback
            except ValueError:
                is_loopback = False
        if not is_loopback:
            raise GrantError("core_grant_https_required")
    return url.strip()


class RejectRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Never forward a Core bearer token to a redirect destination."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class CoreGrantSource(Protocol):
    def fetch_grants(self) -> dict[str, ExecutionGrant]:
        ...


class FileGrantSource:
    def __init__(self, path: str | None = None) -> None:
        self._path = path

    def fetch_grants(self) -> dict[str, ExecutionGrant]:
        return load_grant_registry(path=self._path)


class HttpCoreGrantSource:
    def __init__(self, url: str, token: str | None = None, timeout: float = 5.0) -> None:
        self.url = validate_core_grant_url(url)
        self.token = token
        self.timeout = timeout

    def fetch_grants(self) -> dict[str, ExecutionGrant]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        req = urllib.request.Request(self.url, headers=headers, method="GET")
        try:
            opener = urllib.request.build_opener(RejectRedirectHandler())
            with opener.open(req, timeout=self.timeout) as resp:
                if resp.status != 200:
                    raise GrantError("core_grant_http_" + str(resp.status))
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise GrantError("core_grant_http_" + str(exc.code)) from exc
        except Exception as exc:
            raise GrantError("core_grant_unreachable") from exc
        data = json.loads(raw)
        if not isinstance(data, list):
            raise GrantError("core_grant_payload_invalid")
        out: dict[str, ExecutionGrant] = {}
        for item in data:
            if not isinstance(item, dict):
                raise GrantError("core_grant_entry_invalid")
            gid = item.get("grant_id")
            if not isinstance(gid, str) or not gid:
                raise GrantError("core_grant_entry_missing_id")
            out[gid] = ExecutionGrant(
                grant_id=gid,
                work_id=str(item["work_id"]),
                entry_path=str(item["entry_path"]),
                operation=str(item["operation"]),
                expected_source_sha256=str(item["expected_source_sha256"]),
                expires_at_unix=item.get("expires_at_unix"),
            )
        return out


def build_grant_source(environ=None) -> CoreGrantSource:
    env = os.environ if environ is None else environ
    url = env.get(CORE_GRANT_URL_ENV)
    if not isinstance(url, str) or not url.strip():
        raise GrantError("core_grant_url_required")
    return HttpCoreGrantSource(url.strip(), token=env.get(CORE_GRANT_TOKEN_ENV))


__all__ = [
    "CORE_GRANT_URL_ENV",
    "CORE_GRANT_TOKEN_ENV",
    "CoreGrantSource",
    "FileGrantSource",
    "HttpCoreGrantSource",
    "RejectRedirectHandler",
    "validate_core_grant_url",
    "build_grant_source",
]
