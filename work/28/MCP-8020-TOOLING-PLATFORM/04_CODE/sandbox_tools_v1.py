"""Work 28 bounded sandbox tools v1. Provider must route through authorized Sandbox/Core."""
from __future__ import annotations
import re
from typing import Any, Mapping, Protocol

class SandboxBlocked(RuntimeError):
    pass
class InvalidSandboxRequest(ValueError):
    pass

MAX_READ_BYTES = 64 * 1024
MAX_SEARCH_RESULTS = 100
MAX_SEARCH_QUERY = 256
_DRIVE = re.compile(r"^[A-Za-z]:")

def normalize_work_path(path: str) -> str:
    if not isinstance(path, str) or not path or len(path) > 1024:
        raise InvalidSandboxRequest("path must be non-empty text <= 1024 chars")
    if "\x00" in path or "\\" in path or path.startswith("/") or _DRIVE.match(path):
        raise InvalidSandboxRequest("path must be a Work-relative POSIX path")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise InvalidSandboxRequest("path contains an invalid segment")
    if any(":" in part for part in parts):
        raise InvalidSandboxRequest("alternate data stream syntax is not allowed")
    return "/".join(parts)

class SandboxProvider(Protocol):
    def search(self, work_id: str, query: str, limit: int) -> Mapping[str, Any]: ...
    def stat(self, work_id: str, path: str) -> Mapping[str, Any]: ...
    def read_range(self, work_id: str, path: str, offset: int, length: int) -> Mapping[str, Any]: ...
    def write(self, work_id: str, path: str, content: str, expected_sha256: str | None) -> Mapping[str, Any]: ...

class SandboxToolsV1:
    def __init__(self, provider: SandboxProvider | None):
        self._provider = provider
    def _ready(self) -> SandboxProvider:
        if self._provider is None:
            raise SandboxBlocked("authorized Sandbox/Core provider is not configured")
        return self._provider
    @staticmethod
    def _work_id(work_id: str) -> str:
        if not isinstance(work_id, str) or not work_id.strip() or len(work_id) > 64:
            raise InvalidSandboxRequest("invalid work_id")
        return work_id.strip()
    def sandbox_search(self, work_id: str, query: str, limit: int = 20) -> dict[str, Any]:
        if not isinstance(query, str) or not query.strip() or len(query) > MAX_SEARCH_QUERY:
            raise InvalidSandboxRequest("query must be 1-256 characters")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_SEARCH_RESULTS:
            raise InvalidSandboxRequest("limit must be an integer between 1 and 100")
        result = self._ready().search(self._work_id(work_id), query.strip(), limit)
        if not isinstance(result, Mapping):
            raise SandboxBlocked("Sandbox provider returned malformed search result")
        return dict(result)
    def sandbox_stat(self, work_id: str, path: str) -> dict[str, Any]:
        result = self._ready().stat(self._work_id(work_id), normalize_work_path(path))
        if not isinstance(result, Mapping):
            raise SandboxBlocked("Sandbox provider returned malformed stat result")
        return dict(result)
    def sandbox_read_range(self, work_id: str, path: str, offset: int = 0,
                           length: int = 16_384) -> dict[str, Any]:
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise InvalidSandboxRequest("offset must be a non-negative integer")
        if isinstance(length, bool) or not isinstance(length, int) or not 1 <= length <= MAX_READ_BYTES:
            raise InvalidSandboxRequest("length must be an integer between 1 and 65536")
        result = self._ready().read_range(
            self._work_id(work_id), normalize_work_path(path), offset, length)
        if not isinstance(result, Mapping):
            raise SandboxBlocked("Sandbox provider returned malformed read result")
        return dict(result)
    def sandbox_write(self, work_id: str, path: str, content: str,
                      expected_sha256: str | None = None) -> dict[str, Any]:
        if not isinstance(content, str) or len(content.encode("utf-8")) > MAX_READ_BYTES:
            raise InvalidSandboxRequest("content must be UTF-8 text <= 65536 bytes")
        if expected_sha256 is not None and (
            not isinstance(expected_sha256, str) or len(expected_sha256) != 64
            or any(c not in "0123456789abcdefABCDEF" for c in expected_sha256)):
            raise InvalidSandboxRequest("expected_sha256 must be a SHA-256 hex digest")
        result = self._ready().write(
            self._work_id(work_id), normalize_work_path(path), content, expected_sha256)
        if not isinstance(result, Mapping) or result.get("readback_verified") is not True:
            raise SandboxBlocked("write not accepted: provider did not verify readback")
        return dict(result)
