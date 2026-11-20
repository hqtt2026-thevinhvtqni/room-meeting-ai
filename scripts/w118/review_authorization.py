"""Authorization checks for independent Work 118 acceptance reviews."""
from __future__ import annotations

import argparse
import json

from scripts.w118.authorization import load_role_map, authorize_independent_review


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/w118/role-map.json")
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--pr-author", required=True)
    args = parser.parse_args()

    role_map = load_role_map(args.config)
    allowed, reason, principal = authorize_independent_review(role_map, args.reviewer, args.pr_author)
    print(json.dumps({
        "authorized": allowed,
        "reason": reason,
        "reviewer": args.reviewer,
        "pr_author": args.pr_author,
        "principal": principal,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
