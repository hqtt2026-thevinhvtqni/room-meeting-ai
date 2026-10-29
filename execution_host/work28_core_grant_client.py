"""WP18 — Core grant fetch boundary (fail-closed).

When ROOM_HOP_CORE_GRANT_URL is unset, falls back to file registry.
Client body never supplies grants.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Protocol

from .work28_grant import ExecutionGrant, GrantError
from .work28_grant_registry import load_grant_registry

CORE_GRANT_URL_ENV = "ROOM_HOP_CORE_GRANT_URL"
CORE_GRANT_TOKEN_ENV = "ROOM_HOP_CORE_GRANT_TOKEN"


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
        if not url:
            raise GrantError("core_grant_url_required")
        self.url = url
        self.token = token
        self.timeout = timeout

    def fetch_grants(self) -> dict[str, ExecutionGrant]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        req = urllib.request.Request(self.url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
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
    if url:
        return HttpCoreGrantSource(url, token=env.get(CORE_GRANT_TOKEN_ENV))
    return FileGrantSource()


__all__ = [
    "CORE_GRANT_URL_ENV",
    "CORE_GRANT_TOKEN_ENV",
    "CoreGrantSource",
    "FileGrantSource",
    "HttpCoreGrantSource",
    "build_grant_source",
]
