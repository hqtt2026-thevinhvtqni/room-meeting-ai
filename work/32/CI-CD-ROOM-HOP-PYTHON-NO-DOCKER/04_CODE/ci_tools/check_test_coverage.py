"""Report test files not assigned to a CI lane.

UNIT_TESTS and E2E_TESTS are executed by the hosted Linux jobs.
WINDOWS_LANE_TESTS is an explicit accounting bucket for opt-in PC-only tests;
it does not claim those tests have run. EXCLUDED_TESTS is a reviewed exclusion
list. Discovery is recursive and honors pytest.ini norecursedirs.
"""
from __future__ import annotations

import fnmatch
import os
import re
import sys
from pathlib import Path


def _names(var: str) -> set[str]:
    return {Path(p).as_posix() for p in os.environ.get(var, "").split() if p}


def _norecursedirs(repo_root: Path) -> list[str]:
    config = repo_root / "pytest.ini"
    if not config.is_file():
        return []
    text = config.read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^\s*norecursedirs\s*=\s*(.*?)(?=^\S|\Z)", text
    )
    if not match:
        return []
    return match.group(1).replace("\\", " ").split()


def _is_pytest_excluded(directory: Path, repo_root: Path, patterns: list[str]) -> bool:
    current = directory
    while current != repo_root and repo_root in current.parents:
        rel = current.relative_to(repo_root).as_posix()
        if any(
            fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(current.name, pattern)
            for pattern in patterns
        ):
            return True
        current = current.parent
    return False


def find_unaccounted(repo_root: Path, tests_dir: str = "tests") -> list[str]:
    known = (
        _names("UNIT_TESTS")
        | _names("E2E_TESTS")
        | _names("WINDOWS_LANE_TESTS")
        | _names("EXCLUDED_TESTS")
    )
    tests_root = repo_root / tests_dir
    if not tests_root.is_dir():
        return []
    patterns = _norecursedirs(repo_root)
    found = {
        p.relative_to(repo_root).as_posix()
        for p in tests_root.rglob("test_*.py")
        if not _is_pytest_excluded(p.parent, repo_root, patterns)
    }
    return sorted(found - known)


def find_missing(repo_root: Path) -> list[str]:
    """Whitelisted paths that do not exist (a typo would otherwise hide a gap)."""
    listed = (
        _names("UNIT_TESTS")
        | _names("E2E_TESTS")
        | _names("WINDOWS_LANE_TESTS")
    )
    return sorted(p for p in listed if not (repo_root / p).is_file())


def main() -> int:
    root = Path(os.environ.get("REPO_ROOT", ".")).resolve()
    unaccounted = find_unaccounted(root)
    missing = find_missing(root)
    windows = sorted(_names("WINDOWS_LANE_TESTS"))
    print(f"windows_lane_tests={len(windows)}")
    for p in windows:
        print(f"  WINDOWS-ONLY (not run by Linux jobs): {p}")
    print(f"unaccounted_test_files={len(unaccounted)}")
    for p in unaccounted:
        print(f"  NOT RUN BY CI: {p}")
    print(f"missing_whitelisted_files={len(missing)}")
    for p in missing:
        print(f"  MISSING: {p}")
    strict = os.environ.get("CHECK_STRICT") == "1"
    if missing:
        return 1
    if unaccounted and strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
