"""GitHub Issue mirror adapter for Core :8000 Task snapshots.

This module has no Task database. The caller must supply a normalized Core
Task projection and a Core-issued per-Task mirror lock lease. Core remains the
only runtime Task/Assignment/Event authority.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Mapping

from .marker_safety import has_exact_standalone_marker

from .core_task_adapter import (
    CoreTaskProjection,
    core_task_issue_marker,
    project_core_task_to_issue,
)


class GitHubIssueError(RuntimeError):
    """GitHub Issue API operation failed or returned inconsistent data."""


class IssueLookupIncomplete(GitHubIssueError):
    """The adapter cannot prove that no matching Issue already exists."""


class IssueLookupDuplicate(GitHubIssueError):
    """More than one GitHub Issue carries the same Core Task marker."""


_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9_-])?$")


def _valid_repository(value: object) -> bool:
    return isinstance(value, str) and _REPOSITORY_RE.fullmatch(value) is not None


class GitHubIssueAdapter:
    def __init__(
        self,
        transport: Callable[..., tuple[int, Mapping[str, str], Any]],
        *,
        repository: str,
        max_issue_pages: int = 20,
        lease_validator: Callable[[str, CoreTaskProjection], bool] | None = None,
    ) -> None:
        if not _valid_repository(repository):
            raise ValueError("repository must contain valid non-empty owner/name components")
        if type(max_issue_pages) is not int or max_issue_pages < 1:
            raise ValueError("max_issue_pages must be a positive integer")
        self.transport = transport
        self.repository = repository
        self.max_issue_pages = max_issue_pages
        # Integration port only; no local lease authority is implemented.
        # Production writes stay disabled until Core supplies its validator.
        self.lease_validator = lease_validator

    def _request(self, method: str, path: str, payload: Mapping[str, Any] | None = None) -> tuple[int, Mapping[str, str], Any]:
        status, headers, body = self.transport(method, path, payload)
        if status == 403 or status == 429:
            raise GitHubIssueError("GitHub API rate/permission limit; retry only after policy/Retry-After")
        if status >= 500:
            raise GitHubIssueError("GitHub API server error")
        if status >= 400:
            raise GitHubIssueError(f"GitHub API returned HTTP {status}")
        return status, headers, body

    def _find_task_issues(self, marker: str) -> list[Mapping[str, Any]]:
        """Return all matching Issues after a complete bounded scan.

        Pull Requests are excluded. A full final page is not proof that the
        scan is complete, so reaching the page ceiling fails closed.
        """
        matches: list[Mapping[str, Any]] = []
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
                body = issue.get("body") or ""
                if not isinstance(body, str):
                    raise IssueLookupDuplicate("Issue body is not text; refusing ambiguous Task marker lookup")
                if marker in body:
                    if not has_exact_standalone_marker(body, marker):
                        raise IssueLookupDuplicate("embedded, quoted, fenced or repeated Task marker; refusing mutation")
                    matches.append(issue)
            if len(issues) < 100:
                return matches
        raise IssueLookupIncomplete(
            "Issue scan reached max_issue_pages; refusing mutation because duplicates may exist"
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
        if self.lease_validator is None:
            raise GitHubIssueError(
                "authoritative Core lease validator is not configured; refusing GitHub mutation"
            )
        try:
            lease_valid = self.lease_validator(lock_lease_id, task)
        except Exception as exc:
            raise GitHubIssueError("Core lease validation failed; refusing GitHub mutation") from exc
        if lease_valid is not True:
            raise GitHubIssueError("Core lease was not authoritatively validated; refusing GitHub mutation")

        projection = project_core_task_to_issue(task)
        title, body, labels = projection["title"], projection["body"], projection["labels"]
        marker = core_task_issue_marker(task.task_id)
        matches = self._find_task_issues(marker)
        if len(matches) > 1:
            raise IssueLookupDuplicate(
                f"multiple GitHub Issues carry Core Task marker for {task.task_id}; refusing mutation"
            )
        existing = matches[0] if matches else None
        if task.issue_id is not None:
            if existing is None:
                raise GitHubIssueError(
                    "Core has a persisted issue_id but no matching Task-marker Issue was found; refusing create"
                )
            if existing.get("number") != task.issue_id:
                raise GitHubIssueError(
                    "GitHub Task-marker Issue number does not match Core's persisted issue_id; refusing mutation"
                )
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
