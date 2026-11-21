"""Idempotent Sandbox-to-GitHub Issue mirror adapter for W118 Tasks.

Sandbox remains the Task authority. GitHub Issues are collaboration mirrors.
This adapter never assigns GitHub users, closes Issues, or changes Task state.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Mapping


class GitHubIssueError(RuntimeError):
    """GitHub API operation failed or returned an unverifiable result."""


class IssueLookupIncomplete(GitHubIssueError):
    """The Issue scan was incomplete; creating another Issue would be unsafe."""


Transport = Callable[[str, str, Mapping[str, Any] | None], tuple[int, Mapping[str, str], Any]]


def task_issue_marker(task_id: str) -> str:
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", task_id):
        raise ValueError("task_id is invalid")
    return f"<!-- room-hop-task-id:{task_id} -->"


def build_task_issue_body(task: Mapping[str, Any]) -> str:
    required = ("work_id", "wp_id", "task_id", "title", "objective")
    for field in required:
        if not isinstance(task.get(field), str) or not task[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    marker = task_issue_marker(task["task_id"])
    criteria = task.get("acceptance_criteria", [])
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("acceptance_criteria must be a non-empty list")
    criterion_lines = []
    for item in criteria:
        if not isinstance(item, Mapping):
            raise ValueError("each acceptance criterion must be an object")
        criterion_lines.append(
            f"- **{item.get('id', 'AC')}** — {item.get('description', '')} "
            f"(Verify: {item.get('verification_method', '')})"
        )
    scope_in = task.get("scope_in", [])
    scope_out = task.get("scope_out", [])
    priority = task.get("priority", "P2")
    return "\n".join([
        marker,
        f"<!-- Work-ID: {task['work_id']} WP-ID: {task['wp_id']} Task-ID: {task['task_id']} -->",
        "## Sandbox Task mirror",
        f"- **Work:** {task['work_id']}",
        f"- **Work Package:** {task['wp_id']}",
        f"- **Task:** {task['task_id']}",
        f"- **Priority:** {priority}",
        f"- **Sandbox owner:** {task.get('owner_principal', 'UNASSIGNED')}",
        "",
        "## Objective",
        task["objective"].strip(),
        "",
        "## Scope in",
        *([f"- {item}" for item in scope_in] if scope_in else ["- Not specified"]),
        "",
        "## Scope out",
        *([f"- {item}" for item in scope_out] if scope_out else ["- None specified"]),
        "",
        "## Acceptance criteria",
        *criterion_lines,
        "",
        "---",
        "This Issue mirrors a Task whose lifecycle authority remains in Sandbox. "
        "GitHub Assignee is not proof of AI assignment or ACK. CI success does not "
        "constitute Task acceptance. Do not close this Issue until Sandbox confirms "
        "Owner acceptance and successful Issue-state readback.",
    ])


class GitHubIssueAdapter:
    """Create/update and read back a Task Issue using an injected GitHub token."""

    def __init__(
        self,
        repository: str,
        token: str,
        *,
        transport: Transport | None = None,
        api_base: str = "https://api.github.com",
        max_issue_pages: int = 50,
    ) -> None:
        if not isinstance(repository, str) or not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
        ):
            raise ValueError("repository must use owner/name format")
        if not isinstance(token, str) or not token.strip():
            raise ValueError("GitHub token is required")
        if type(max_issue_pages) is not int or max_issue_pages < 1 or max_issue_pages > 100:
            raise ValueError("max_issue_pages must be between 1 and 100")
        self.repository = repository
        self._token = token.strip()
        self._transport = transport or self._urllib_transport
        self._api_base = api_base.rstrip("/")
        self._max_issue_pages = max_issue_pages

    def _urllib_transport(
        self, method: str, path: str, body: Mapping[str, Any] | None
    ) -> tuple[int, Mapping[str, str], Any]:
        url = f"{self._api_base}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
                "User-Agent": "ROOM-HOP-W118-Issue-Adapter",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read()
                payload = json.loads(raw.decode("utf-8")) if raw else None
                return response.status, dict(response.headers.items()), payload
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            detail = raw.decode("utf-8", errors="replace")
            raise GitHubIssueError(f"GitHub API {method} {path} returned HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise GitHubIssueError(f"GitHub API transport failed: {exc}") from exc

    def _request(
        self, method: str, path: str, body: Mapping[str, Any] | None = None
    ) -> tuple[int, Mapping[str, str], Any]:
        status, headers, payload = self._transport(method, path, body)
        if status < 200 or status >= 300:
            raise GitHubIssueError(f"GitHub API {method} {path} returned HTTP {status}")
        return status, headers, payload

    def _find_task_issue(self, marker: str) -> Mapping[str, Any] | None:
        for page in range(1, self._max_issue_pages + 1):
            query = urllib.parse.urlencode({"state": "all", "per_page": 100, "page": page})
            _, _, issues = self._request(
                "GET", f"/repos/{self.repository}/issues?{query}"
            )
            if not isinstance(issues, list):
                raise GitHubIssueError("GitHub Issue listing did not return an array")
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
            raise GitHubIssueError("Task mirror resolved to a Pull Request, not an Issue")
        return issue

    def mirror_task(self, task: Mapping[str, Any]) -> dict[str, Any]:
        """Create or update the Task Issue mirror and verify exact readback."""
        title = f"[{task.get('work_id', 'W?')}] {task.get('title', '')}"
        body = build_task_issue_body(task)
        marker = task_issue_marker(task["task_id"])
        existing = self._find_task_issue(marker)
        if existing:
            number = existing.get("number")
            if type(number) is not int or number < 1:
                raise GitHubIssueError("existing Task Issue has an invalid number")
            if existing.get("title") != title or existing.get("body") != body:
                self._request(
                    "PATCH",
                    f"/repos/{self.repository}/issues/{number}",
                    {"title": title, "body": body},
                )
                action = "UPDATED"
            else:
                action = "UNCHANGED"
        else:
            _, _, created = self._request(
                "POST",
                f"/repos/{self.repository}/issues",
                {"title": title, "body": body},
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
            "work_id": task["work_id"],
            "wp_id": task["wp_id"],
            "task_id": task["task_id"],
            "readback_verified": True,
            "authority": "GITHUB_ISSUE_MIRROR_SANDBOX_TASK_AUTHORITY",
            "assignees_mutated": False,
            "issue_state_mutated": False,
        }
