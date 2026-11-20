"""Fail-closed GitHub actor authorization for Work 118.

This module deliberately separates execution ACK, independent-review and
project-owner final-acceptance permissions. An owner account is not an
independent reviewer or execution actor merely because it owns the project.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ACK_RE = re.compile(r"^ACKED-([a-z][a-z0-9_-]*)\s+([1-9][0-9]*)$")


def load_role_map(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.1":
        raise ValueError("unsupported role-map schema_version")
    if data.get("policy") != "deny-by-default":
        raise ValueError("role-map must use deny-by-default")
    principals = data.get("principals")
    if not isinstance(principals, dict):
        raise ValueError("principals must be an object")
    for login, entry in principals.items():
        if not isinstance(login, str) or not login or not isinstance(entry, dict):
            raise ValueError("invalid principal entry")
        if not isinstance(entry.get("principal"), str) or not entry.get("principal"):
            raise ValueError(f"{login}: principal must be a non-empty string")
        if not isinstance(entry.get("roles", []), list) or not all(isinstance(x, str) and x for x in entry.get("roles", [])):
            raise ValueError(f"{login}: roles must be a list of non-empty strings")
        if not isinstance(entry.get("ack_roles", []), list) or not all(isinstance(x, str) and x for x in entry.get("ack_roles", [])):
            raise ValueError(f"{login}: ack_roles must be a list of non-empty strings")
        if not isinstance(entry.get("active"), bool):
            raise ValueError(f"{login}: active must be boolean")
        if not isinstance(entry.get("can_accept"), bool):
            raise ValueError(f"{login}: can_accept must be boolean")
        if not isinstance(entry.get("can_independently_review"), bool):
            raise ValueError(f"{login}: can_independently_review must be boolean")
        if not isinstance(entry.get("can_trigger_controlled_test"), bool):
            raise ValueError(f"{login}: can_trigger_controlled_test must be boolean")
        if not set(entry.get("ack_roles", [])).issubset(set(entry.get("roles", []))):
            raise ValueError(f"{login}: ack_roles must be a subset of roles")
    return data


def parse_ack(body: str) -> tuple[str, int] | None:
    match = ACK_RE.fullmatch(body.strip())
    if not match:
        return None
    return match.group(1), int(match.group(2))


def authorize_ack(role_map: dict[str, Any], login: str, role: str) -> tuple[bool, str, str | None]:
    entry = role_map.get("principals", {}).get(login)
    if not entry or not entry.get("active", False):
        return False, "actor is not mapped as an active principal", None
    if role not in entry.get("ack_roles", []):
        return False, f"actor is not authorized to ACK role '{role}'", entry.get("principal")
    return True, "authorized", entry.get("principal")


def authorize_independent_review(role_map: dict[str, Any], login: str, pull_request_author: str) -> tuple[bool, str, str | None]:
    principals = role_map.get("principals", {})
    entry = principals.get(login)
    if not entry or not entry.get("active", False) or not entry.get("can_independently_review", False):
        return False, "actor is not mapped as an active independent reviewer", None
    author_entry = principals.get(pull_request_author)
    if not author_entry or not author_entry.get("active", False):
        return False, "PR author principal is not mapped; reviewer independence cannot be verified", None
    if entry.get("principal") == author_entry.get("principal"):
        return False, "reviewer and PR author resolve to the same HQTT principal", None
    return True, "authorized independent reviewer", entry.get("principal")


def authorize_controlled_test(role_map: dict[str, Any], login: str) -> tuple[bool, str]:
    entry = role_map.get("principals", {}).get(login)
    if not entry or not entry.get("active", False):
        return False, "actor is not mapped as an active principal"
    if not entry.get("can_trigger_controlled_test", False):
        return False, "actor is not authorized to trigger controlled diagnostics tests"
    return True, "authorized controlled diagnostics test"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/w118/role-map.json")
    parser.add_argument("--login", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--issue", required=True, type=int)
    args = parser.parse_args()

    role_map = load_role_map(args.config)
    parsed = parse_ack(args.body)
    if not parsed:
        result = {"authorized": False, "reason": "ACK syntax invalid", "login": args.login, "issue": args.issue}
    else:
        role, issue_number = parsed
        if issue_number != args.issue:
            result = {"authorized": False, "reason": "ACK issue number does not match event issue", "login": args.login, "role": role, "issue": args.issue}
        else:
            allowed, reason, principal = authorize_ack(role_map, args.login, role)
            result = {"authorized": allowed, "reason": reason, "login": args.login, "principal": principal, "role": role, "issue": args.issue}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
