#!/usr/bin/env python3
"""Read-only detector for desktop.ini files inside a ROOM-HOP Git checkout."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TARGET = "desktop.ini"

def find_desktop_ini(root: Path) -> list[str]:
    """Find case-insensitive matches, skip .git, and never follow symlinks."""
    matches: list[str] = []
    root = root.resolve()
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        here = Path(current)
        dirs[:] = [d for d in dirs if d.casefold() != ".git" and not (here / d).is_symlink()]
        for name in files:
            candidate = here / name
            if name.casefold() == TARGET and not candidate.is_symlink():
                matches.append(candidate.relative_to(root).as_posix())
    return sorted(set(matches), key=str.casefold)

def git_output(root: Path, *args: str) -> tuple[int, str, str]:
    try:
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=15, check=False)
        return p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, "", str(exc)

def make_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    matches = find_desktop_ini(root)
    code, tracked_raw, tracked_err = git_output(root, "ls-files", "-z")
    git_available = code == 0
    tracked = {x.replace("\\", "/") for x in tracked_raw.split("\0")
               if x and Path(x).name.casefold() == TARGET} if git_available else set()
    findings = []
    for rel in matches:
        ignored, rule, _ = git_output(root, "check-ignore", "-v", "--no-index", "--", rel)
        findings.append({"path": rel, "tracked_in_index": rel in tracked,
            "ignored_by_git": ignored == 0, "ignore_rule": rule.strip() if ignored == 0 else None,
            "action_taken": "none"})
    probe, probe_out, _ = git_output(root, "check-ignore", "-v", "--no-index", "--", TARGET)
    status, status_out, status_err = git_output(root, "status", "--porcelain=v1", "--untracked-files=all")
    return {
        "schema": "room-drive-isolation-report/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root), "git_available": git_available,
        "git_error": tracked_err.strip() if not git_available else None,
        "desktop_ini_count": len(matches),
        "tracked_desktop_ini_count": sum(1 for x in findings if x["tracked_in_index"]),
        "findings": findings,
        "ignore_probe": {"sample": TARGET, "matched": probe == 0,
                         "rule": probe_out.strip() if probe == 0 else None},
        "git_status_available": status == 0,
        "git_status_porcelain": status_out.splitlines() if status == 0 else [],
        "git_status_error": status_err.strip() if status != 0 else None,
        "remediation": "No files were changed. Review provenance and impact before quarantine or removal."
    }

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=float, default=30.0)
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir(): ap.error(f"root is not a directory: {root}")
    if args.watch and args.interval < 2: ap.error("--interval must be at least 2 seconds")
    try:
        while True:
            report = make_report(root)
            if args.json:
                print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
            else:
                state = "ALERT" if report["desktop_ini_count"] else "CLEAN"
                print(f"{state}: {report['desktop_ini_count']} desktop.ini file(s); "
                      f"tracked={report['tracked_desktop_ini_count']}; git={report['git_available']}")
                for item in report["findings"]:
                    print(f"  - {item['path']} | tracked={item['tracked_in_index']} "
                          f"| ignored={item['ignored_by_git']} | action=none")
                if not report["ignore_probe"]["matched"]:
                    print("  WARNING: .gitignore does not match desktop.ini at repository root.")
            if not args.watch:
                if not report["git_available"]: return 3
                return 2 if report["desktop_ini_count"] else 0
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 130

if __name__ == "__main__":
    sys.exit(main())
