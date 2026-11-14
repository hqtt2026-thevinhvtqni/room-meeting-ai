"""Compare the active GitHub workflow with its Work 32 mirror copy.

Usage:
    python check_workflow_mirror.py [ACTIVE_PATH] [MIRROR_PATH]

Defaults: ACTIVE_PATH=.github/workflows/ci-validation.yml and
MIRROR_PATH=$W32_DIR/04_CODE/ci-validation.yml (W32_DIR defaults to
work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER). Paths are resolved from REPO_ROOT
(default: current directory).

Line endings are normalized (CRLF/CR -> LF) before comparing. Report-only by
default (exit 0 on drift); set CHECK_STRICT=1 to exit 1 when files differ.
A missing file always exits 2.
"""
from __future__ import annotations

import difflib
import os
import sys
from pathlib import Path

DEFAULT_ACTIVE = ".github/workflows/ci-validation.yml"
DEFAULT_W32_DIR = "work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER"


def normalize(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n").split("\n")


def diff_workflows(active: Path, mirror: Path) -> list[str]:
    """Return unified-diff lines (empty list when the files are equivalent)."""
    return list(
        difflib.unified_diff(
            normalize(active.read_text(encoding="utf-8")),
            normalize(mirror.read_text(encoding="utf-8")),
            fromfile=f"active:{active.as_posix()}",
            tofile=f"mirror:{mirror.as_posix()}",
            lineterm="",
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(os.environ.get("REPO_ROOT", ".")).resolve()
    w32 = os.environ.get("W32_DIR", DEFAULT_W32_DIR)
    active = root / (args[0] if len(args) > 0 else DEFAULT_ACTIVE)
    mirror = root / (args[1] if len(args) > 1 else f"{w32}/04_CODE/ci-validation.yml")

    for path in (active, mirror):
        if not path.is_file():
            print(f"MISSING: {path.as_posix()}")
            return 2

    diff = diff_workflows(active, mirror)
    if not diff:
        print("workflow_mirror=IN_SYNC")
        return 0
    print("workflow_mirror=DRIFT")
    print("\n".join(diff))
    return 1 if os.environ.get("CHECK_STRICT") == "1" else 0


if __name__ == "__main__":
    sys.exit(main())
