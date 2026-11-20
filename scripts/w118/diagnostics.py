"""Deterministic idempotency planning for W118 CI diagnostics."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{7,64}$")


def diagnostic_key(workflow_id: str | int, sha: str) -> str:
    value = str(workflow_id).strip()
    if not value.isdigit():
        raise ValueError("workflow_id must be numeric")
    normalized_sha = sha.strip().lower()
    if not SHA_RE.fullmatch(normalized_sha):
        raise ValueError("sha must be a 7-64 character hexadecimal commit SHA")
    return f"w118-diagnostic:{value}:{normalized_sha}"


def update_marker(run_id: str | int, attempt: str | int) -> str:
    run = str(run_id).strip()
    try:
        run_number = int(run)
        attempt_number = int(attempt)
    except ValueError as exc:
        raise ValueError("run_id and attempt must be positive integers") from exc
    if run_number < 1 or attempt_number < 1:
        raise ValueError("run_id and attempt must be positive integers")
    return f"<!-- w118-diagnostic-update:{run_number}:{attempt_number} -->"


def find_existing_open_issue(issues: list[dict[str, Any]], key: str) -> str:
    marker = f"<!-- {key} -->"
    for issue in issues:
        body = issue.get("body") or ""
        number = issue.get("number")
        if marker in body and number is not None:
            return str(number)
    return ""


def build_plan(issues: list[dict[str, Any]], workflow_id: str | int, sha: str,
               run_id: str | int, attempt: str | int) -> dict[str, Any]:
    key = diagnostic_key(workflow_id, sha)
    marker = update_marker(run_id, attempt)
    return {
        "idempotency_key": key,
        "update_marker": marker,
        "existing_issue": find_existing_open_issue(issues, key),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issues-json", required=True)
    parser.add_argument("--workflow-id", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    issues = json.loads(Path(args.issues_json).read_text(encoding="utf-8"))
    if not isinstance(issues, list):
        raise ValueError("issues-json must contain a JSON array")
    print(json.dumps(build_plan(issues, args.workflow_id, args.sha, args.run_id, args.attempt),
                     ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
