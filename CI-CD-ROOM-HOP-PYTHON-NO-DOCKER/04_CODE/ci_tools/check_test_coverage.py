"""Report tests/test_*.py files that no CI job runs.

Reads the whitelists from the UNIT_TESTS and E2E_TESTS environment variables
(whitespace-separated paths, as used by the workflow). Optional EXCLUDED_TESTS
lists files intentionally left out. Default mode is report-only (exit 0);
set CHECK_STRICT=1 to exit 1 when any test file is unaccounted for.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _names(var: str) -> set[str]:
    return {Path(p).as_posix() for p in os.environ.get(var, "").split() if p}


def find_unaccounted(repo_root: Path, tests_dir: str = "tests") -> list[str]:
    known = _names("UNIT_TESTS") | _names("E2E_TESTS") | _names("EXCLUDED_TESTS")
    found = {
        p.relative_to(repo_root).as_posix()
        for p in (repo_root / tests_dir).glob("test_*.py")
    }
    return sorted(found - known)


def find_missing(repo_root: Path) -> list[str]:
    """Whitelisted paths that do not exist (a typo would otherwise hide a gap)."""
    listed = _names("UNIT_TESTS") | _names("E2E_TESTS")
    return sorted(p for p in listed if not (repo_root / p).is_file())


def main() -> int:
    root = Path(os.environ.get("REPO_ROOT", ".")).resolve()
    unaccounted = find_unaccounted(root)
    missing = find_missing(root)
    print(f"unaccounted_test_files={len(unaccounted)}")
    for p in unaccounted:
        print(f"  NOT RUN BY CI: {p}")
    print(f"missing_whitelisted_files={len(missing)}")
    for p in missing:
        print(f"  MISSING: {p}")
    strict = os.environ.get("CHECK_STRICT") == "1"
    if missing:
        return 1  # a listed-but-absent file always fails: pytest would error anyway
    if unaccounted and strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
