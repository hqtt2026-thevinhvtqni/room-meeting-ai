"""GitHub Issue mirror adapter for Core :8000 Task snapshots.

This module has no Task database. The caller must supply a normalized Core
Task projection and a Core-issued per-Task mirror lock lease. Core remains the
only runtime Task/Assignment/Event authority.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping

from .core_task_adapter import (
    CoreTaskProjection,
    core_task_issue_marker,
    project_core_task_to_issue,
)


class GitHubIssueError(RuntimeError):
    """GitHub Issue API operation failed or returned inconsistent data."""


class IssueLookupIncomplete(GitHubIssueError):
    """The adapter cannot prove that no matching Issue already exists."""


class GitHubIssueAdapter:
    def __init__(
        self,
        transport: Callable[..., tuple[int, Mapping[str, str], Any]],
        *,
        repository: str,
        max_issue_pages: int = 20,
    ) -> None:
        if not isinstance(repository, str) or repository.count("/") != 1:
            raise ValueError("repository must be owner/name")
        if type(max_issue_pages) is not int or max_issue_pages < 1:
            raise ValueError("max_issue_pages must be a positive integer")
        self.transport = transport
        self.repository = repository
        self.max_issue_pages = max_issue_pages

    def _request(self, method: str, path: str, payload: Mapping[str, Any] | None = None) -> tuple[int, Mapping[str, str], Any]:
        status, headers, body = self.transport(method, path, payload)
        if status == 403 or status == 429:
            raise GitHubIssueError("GitHub API rate/permission limit; retry only after policy/Retry-After")
        if status >= 500:
            raise GitHubIssueError("GitHub API server error")
        if status >= 400:
            raise GitHubIssueError(f"GitHub API returned HTTP {status}")
        return status, headers, body

    def _find_task_issue(self, marker: str) -> Mapping[str, Any] | None:
        for page in range(1, self.max_issue_pages + 1):
            _, _, issues = self._request(
                "GET",
                f"/repos/{self.repository}/issues?state=all&per_page=100&page={page}",
            )
            if not isinstance(issues, list):
                raise GitHubIssueError("Issue list response is not a list")
            for issue in issues:
                if not isinstance(issue, Mapping) or "pull_request" in issue:
                    continue
                if marker in str(issue.get("body") or ""):
                    return issue
            if len(issues) < 100:
                return None
        raise IssueLookupIncomplete(
            "Issue scan reached max_issue_pages; refusing to create a possible duplicate"
        )

    def _readback(self, number: int, expected_title: str, expected_body: str) -> Mapping[str, Any]:
        _, _, issue = self._request("GET", f"/repos/{self.repository}/issues/{number}")
        if not isinstance(issue, Mapping):
            raise GitHubIssueError("Issue readback did not return an object")
        if issue.get("number") != number or issue.get("title") != expected_title:
            raise GitHubIssueError("Issue readback identity/title mismatch")
        if issue.get("body") != expected_body:
            raise GitHubIssueError("Issue readback body mismatch")
        if "pull_request" in issue:
            raise GitHubIssueError("Core Task mirror resolved to a Pull Request, not an Issue")
        return issue

    def mirror_core_task(
        self,
        task: CoreTaskProjection,
        *,
        lock_lease_id: str,
    ) -> dict[str, Any]:
        """Create/update an Issue from a Core snapshot under a Core-issued lock."""
        if not isinstance(task, CoreTaskProjection):
            raise GitHubIssueError("task must be a normalized CoreTaskProjection")
        if not isinstance(lock_lease_id, str) or not lock_lease_id.strip():
            raise GitHubIssueError("Core per-Task lock lease is required; no local lock is created")
        projection = project_core_task_to_issue(task)
        title, body, labels = projection["title"], projection["body"], projection["labels"]
        marker = core_task_issue_marker(task.task_id)
        existing = self._find_task_issue(marker)
        if existing:
            number = existing.get("number")
            if type(number) is not int or number < 1:
                raise GitHubIssueError("existing Core Task Issue has an invalid number")
            if existing.get("title") != title or existing.get("body") != body:
                self._request(
                    "PATCH",
                    f"/repos/{self.repository}/issues/{number}",
                    {"title": title, "body": body, "labels": labels},
                )
                action = "UPDATED"
            else:
                action = "UNCHANGED"
        else:
            _, _, created = self._request(
                "POST",
                f"/repos/{self.repository}/issues",
                {"title": title, "body": body, "labels": labels},
            )
            if not isinstance(created, Mapping) or type(created.get("number")) is not int:
                raise GitHubIssueError("GitHub Issue creation returned no valid issue number")
            number = created["number"]
            action = "CREATED"

        issue = self._readback(number, title, body)
        return {
            "action": action,
            "issue_id": number,
            "issue_url": issue.get("html_url"),
            "repository": self.repository,
            "work_id": task.work_id,
            "task_id": task.task_id,
            "correlation_id": task.correlation_id,
            "core_source_revision": task.source_revision,
            "readback_verified": True,
            "authority": "CORE_8000_TASK_AUTHORITY_GITHUB_ISSUE_MIRROR",
            "lock_lease_id": lock_lease_id,
            "assignees_mutated": False,
            "issue_state_mutated": False,
        }
