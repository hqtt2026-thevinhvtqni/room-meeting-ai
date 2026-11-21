"""Validate Work/Task/Issue linkage for task-scoped GitHub source changes.

A legacy aggregate Work branch is reported as UNBOUND_LEGACY_BRANCH, never
silently mapped to a Task. A task-scoped push must bind the branch and every
commit message to the same Work ID, Task ID and GitHub Issue number.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


BRANCH_RE = re.compile(
    r"^work/(?P<work_id>W[0-9]{3,4})/task-(?P<task_id>W[0-9]{3,4}-TASK-[0-9]{3,6})$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TRAILER_PATTERNS = {
    "work_id": re.compile(r"^Work-ID:\s*(\S+)\s*$", re.IGNORECASE),
    "task_id": re.compile(r"^Task-ID:\s*(\S+)\s*$", re.IGNORECASE),
    "issue_id": re.compile(r"^Issue:\s*#?([1-9][0-9]*)\s*$", re.IGNORECASE),
}


class SourceBindingError(ValueError):
    """Source change is missing or contradicts its Task binding."""


def parse_task_branch(branch: str) -> dict[str, str] | None:
    if not isinstance(branch, str) or not branch:
        raise SourceBindingError("branch must be a non-empty string")
    match = BRANCH_RE.fullmatch(branch)
    if not match:
        if branch.startswith(("work/W", "work/w")):
            raise SourceBindingError("task-scoped branch does not match the canonical naming contract")
        return None
    binding = match.groupdict()
    if binding["work_id"] != binding["task_id"].split("-TASK-", 1)[0]:
        raise SourceBindingError("branch Work ID and Task ID prefix do not match")
    return binding


def parse_commit_trailers(message: str) -> dict[str, str]:
    if not isinstance(message, str) or not message.strip():
        raise SourceBindingError("commit message must be non-empty")
    found: dict[str, list[str]] = {key: [] for key in TRAILER_PATTERNS}
    for line in message.splitlines():
        for key, pattern in TRAILER_PATTERNS.items():
            match = pattern.fullmatch(line.strip())
            if match:
                found[key].append(match.group(1))
    for key, values in found.items():
        if len(values) != 1:
            raise SourceBindingError(f"commit requires exactly one {key} trailer")
    return {key: values[0] for key, values in found.items()}


def validate_commit_binding(
    message: str, *, work_id: str, task_id: str, issue_id: int
) -> dict[str, str]:
    trailers = parse_commit_trailers(message)
    expected = {"work_id": work_id, "task_id": task_id, "issue_id": str(issue_id)}
    for key, value in expected.items():
        if trailers[key] != value:
            raise SourceBindingError(
                f"commit {key} mismatch: expected {value}, got {trailers[key]}"
            )
    return trailers


def validate_push_payload(
    payload: Mapping[str, Any], *, expected_repository: str
) -> dict[str, Any]:
    """Validate a trusted GitHub push event payload without mutating Task state."""
    if not isinstance(payload, Mapping):
        raise SourceBindingError("push payload must be an object")
    repository = payload.get("repository")
    if not isinstance(repository, Mapping) or not repository.get("full_name"):
        raise SourceBindingError("push payload requires repository.full_name")
    ref = payload.get("ref")
    if not isinstance(ref, str) or not ref.startswith("refs/heads/"):
        raise SourceBindingError("push ref must identify a branch")
    branch = ref.removeprefix("refs/heads/")
    branch_binding = parse_task_branch(branch)
    if branch_binding is None:
        return {
            "status": "UNBOUND_LEGACY_BRANCH",
            "enforcement": "NOT_APPLICABLE",
            "repository": repository["full_name"],
            "branch": branch,
            "reason": "aggregate/legacy branch has no Task-level binding; no Task state may be inferred",
        }

    after = payload.get("after")
    if not isinstance(after, str) or not SHA_RE.fullmatch(after):
        raise SourceBindingError("push after must be a full 40-character commit SHA")
    if payload.get("deleted") is True:
        raise SourceBindingError("task branch deletion cannot be accepted as a source push")
    if payload.get("forced") is True:
        raise SourceBindingError("force-push is not allowed for task-scoped source branches")
    commits = payload.get("commits")
    if not isinstance(commits, list) or not commits:
        raise SourceBindingError("task-scoped push must include commit messages")
    head_commit = payload.get("head_commit")
    if not isinstance(head_commit, Mapping) or head_commit.get("id") != after:
        raise SourceBindingError("head_commit.id must match push after SHA")

    if not any(
        isinstance(commit, Mapping) and commit.get("id") == after for commit in commits
    ):
        raise SourceBindingError("push after SHA must be present in the commits list")

    issue_ids: set[int] = set()
    checked = []
    for commit in commits:
        if not isinstance(commit, Mapping):
            raise SourceBindingError("each push commit must be an object")
        sha = commit.get("id")
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            raise SourceBindingError("each pushed commit requires a full SHA")
        trailers = parse_commit_trailers(commit.get("message", ""))
        if trailers["work_id"] != branch_binding["work_id"]:
            raise SourceBindingError("commit Work-ID does not match branch Work ID")
        if trailers["task_id"] != branch_binding["task_id"]:
            raise SourceBindingError("commit Task-ID does not match branch Task ID")
        issue_ids.add(int(trailers["issue_id"]))
        checked.append({"commit_sha": sha, **trailers})

    if len(issue_ids) != 1:
        raise SourceBindingError("all commits in one Task push must reference the same Issue")
    return {
        "status": "BOUND",
        "enforcement": "PASS",
        "repository": repository["full_name"],
        "branch": branch,
        "work_id": branch_binding["work_id"],
        "task_id": branch_binding["task_id"],
        "issue_id": next(iter(issue_ids)),
        "head_sha": after,
        "commits": checked,
        "state_effect": "EVIDENCE_ONLY_NO_TASK_TRANSITION",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, help="Path to a trusted GitHub push event JSON file")
    args = parser.parse_args()
    payload = json.loads(Path(args.event).read_text(encoding="utf-8"))
    try:
        result = validate_push_payload(payload)
    except (SourceBindingError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
