"""Fail-closed authorization for controlled W118 diagnostics fault injection."""
from __future__ import annotations

import argparse
import json

from scripts.w118.authorization import load_role_map, authorize_controlled_test


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/w118/role-map.json")
    parser.add_argument("--login", required=True)
    args = parser.parse_args()
    role_map = load_role_map(args.config)
    allowed, reason = authorize_controlled_test(role_map, args.login)
    print(json.dumps({"authorized": allowed, "reason": reason, "login": args.login},
                     ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
