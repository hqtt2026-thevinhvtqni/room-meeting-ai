"""Authorization for isolated W118 diagnostics fault-injection trigger only.

This allowlist is not a ROOM-HOP identity, Agent, Assignment, ACK, review,
acceptance, merge or release authority. Core/W01/W02/W22 remain authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def authorize(config_path: str, login: str) -> tuple[bool, str]:
    if not isinstance(login, str) or not login.strip():
        return False, "missing GitHub actor login"
    try:
        config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"controlled-test allowlist unavailable: {exc}"
    if config.get("scope") != "CONTROLLED_TEST_TRIGGER_ONLY":
        return False, "allowlist scope is not controlled-test-only"
    allowed = config.get("authorized_github_logins")
    if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
        return False, "controlled-test allowlist is invalid"
    if login not in allowed:
        return False, "actor is not authorized to trigger isolated diagnostics test"
    return True, "authorized for isolated W118 diagnostics test only"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/w118/controlled-test-allowlist.json")
    parser.add_argument("--login", required=True)
    args = parser.parse_args()
    allowed, reason = authorize(args.config, args.login)
    print(json.dumps({"authorized": allowed, "reason": reason, "login": args.login,
                      "scope": "CONTROLLED_TEST_TRIGGER_ONLY"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
