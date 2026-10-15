"""Work 28 guarded GitHub tools v1. Authenticated API calls are injected via provider."""
from __future__ import annotations
import re
from typing import Any, Mapping, Protocol

class GitHubBlocked(RuntimeError):
    pass
class InvalidGitHubRequest(ValueError):
    pass

_BLOB_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
_MAX_FILE_BYTES = 128 * 1024
_MAX_SEARCH = 100

class GitHubProvider(Protocol):
    def repository(self, repository: str) -> Mapping[str, Any]: ...
    def read_file(self, repository: str, path: str, ref: str) -> Mapping[str, Any]: ...
    def search_files(self, repository: str, query: str, ref: str, limit: int) -> Mapping[str, Any]: ...
    def create_branch(self, repository: str, branch: str, base_ref: str) -> Mapping[str, Any]: ...
    def create_file(self, repository: str, branch: str, path: str, content: str, message: str) -> Mapping[str, Any]: ...
    def update_file(self, repository: str, branch: str, path: str, content: str,
                    message: str, expected_blob_sha: str) -> Mapping[str, Any]: ...

def _text(value: Any, field: str, limit: int = 512) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise InvalidGitHubRequest(f"{field} must be non-empty text <= {limit} chars")
    return value.strip()
def _path(path: str) -> str:
    path = _text(path, "path", 1024)
    if path.startswith("/") or "\\" in path or any(p in {"", ".", ".."} for p in path.split("/")):
        raise InvalidGitHubRequest("path must be a repository-relative POSIX path")
    return path
def _branch(branch: str) -> str:
    branch = _text(branch, "branch", 255)
    if branch.casefold() in {"main", "master"}:
        raise InvalidGitHubRequest("direct writes to default branch names are forbidden")
    if branch.startswith("-") or ".." in branch or " " in branch or branch.endswith(("/", ".")):
        raise InvalidGitHubRequest("invalid branch name")
    return branch

class GitHubToolsV1:
    def __init__(self, provider: GitHubProvider | None):
        self._provider = provider
    def _ready(self) -> GitHubProvider:
        if self._provider is None:
            raise GitHubBlocked("authenticated GitHub provider is not configured")
        return self._provider
    def github_repository(self, repository: str) -> dict[str, Any]:
        repository = _text(repository, "repository", 200)
        if repository.count("/") != 1 or any(not p for p in repository.split("/")):
            raise InvalidGitHubRequest("repository must be owner/name")
        result = self._ready().repository(repository)
        if not isinstance(result, Mapping):
            raise GitHubBlocked("GitHub provider returned malformed repository metadata")
        return dict(result)
    def github_read_file(self, repository: str, path: str, ref: str) -> dict[str, Any]:
        result = self._ready().read_file(
            _text(repository, "repository", 200), _path(path), _text(ref, "ref", 255))
        if not isinstance(result, Mapping):
            raise GitHubBlocked("GitHub provider returned malformed file result")
        return dict(result)
    def github_search_files(self, repository: str, query: str, ref: str,
                            limit: int = 20) -> dict[str, Any]:
        query = _text(query, "query", 256)
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= _MAX_SEARCH:
            raise InvalidGitHubRequest("limit must be an integer between 1 and 100")
        result = self._ready().search_files(
            _text(repository, "repository", 200), query, _text(ref, "ref", 255), limit)
        if not isinstance(result, Mapping):
            raise GitHubBlocked("GitHub provider returned malformed search result")
        return dict(result)
    def github_create_branch(self, repository: str, branch: str,
                             base_ref: str = "main") -> dict[str, Any]:
        result = self._ready().create_branch(
            _text(repository, "repository", 200), _branch(branch), _text(base_ref, "base_ref", 255))
        if not isinstance(result, Mapping):
            raise GitHubBlocked("GitHub provider returned malformed branch result")
        return dict(result)
    def github_create_file(self, repository: str, branch: str, path: str,
                           content: str, message: str) -> dict[str, Any]:
        if not isinstance(content, str) or len(content.encode("utf-8")) > _MAX_FILE_BYTES:
            raise InvalidGitHubRequest("content must be UTF-8 text <= 131072 bytes")
        result = self._ready().create_file(
            _text(repository, "repository", 200), _branch(branch), _path(path),
            content, _text(message, "message", 200))
        if not isinstance(result, Mapping) or not result.get("commit_sha"):
            raise GitHubBlocked("GitHub create did not return a commit SHA")
        return dict(result)
    def github_update_file(self, repository: str, branch: str, path: str,
                           content: str, message: str, expected_blob_sha: str) -> dict[str, Any]:
        if not isinstance(content, str) or len(content.encode("utf-8")) > _MAX_FILE_BYTES:
            raise InvalidGitHubRequest("content must be UTF-8 text <= 131072 bytes")
        expected_blob_sha = _text(expected_blob_sha, "expected_blob_sha", 40)
        if not _BLOB_SHA.fullmatch(expected_blob_sha):
            raise InvalidGitHubRequest("expected_blob_sha must be a 40-character Git blob SHA")
        result = self._ready().update_file(
            _text(repository, "repository", 200), _branch(branch), _path(path),
            content, _text(message, "message", 200), expected_blob_sha)
        if not isinstance(result, Mapping) or not result.get("commit_sha"):
            raise GitHubBlocked("GitHub update did not return a commit SHA")
        return dict(result)
