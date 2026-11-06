"""ROOM HOP — read-only Work Dashboard scanner.

Supports:
1. A single Work checked out directly at the repository root.
2. A multi-Work repository using work/<sandbox>/<work>/.

Partial mirrors are deliberately excluded from discovery and aggregate counts.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_ROOT = REPO_ROOT / "work"
VN_TZ = timezone(timedelta(hours=7))

CORE_RECORDS = {
    "BIEN_BAN": ("BIEN_BAN.md",),
    "KE_HOACH": ("KE_HOACH_THI_CONG_XU.md",),
    "NHAT_KY": ("NHAT_KY_HOP_THI_CONG.md", "NHAT_KY_THI_CONG.md"),
}
MANIFEST_NAMES = ("WORK_MANIFEST.md", "DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md")
PHASE_PREFIXES = ("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_")
EXCLUDED_ROOT_DIRS = {".git", ".github", "work", "work_dashboard", "__pycache__"}

STATUS_RE = re.compile(
    r"\b(PASS|DONE|BLOCKED|FAILED|DECISION|CH\s?ƯA\s?XÁC\s?MINH|PENDING|DESIGN|"
    r"SURVEY|IN[- ]?PROGRESS|WIP|SUPERSEDED)\b",
    re.IGNORECASE,
)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _manifest_path(directory: Path) -> Path | None:
    for name in MANIFEST_NAMES:
        direct = directory / name
        if direct.is_file():
            return direct
    root_dir = directory / "00_ROOT"
    for name in MANIFEST_NAMES:
        candidate = root_dir / name
        if candidate.is_file():
            return candidate
    return None


def _phase_dirs(directory: Path) -> list[Path]:
    try:
        return sorted(
            p for p in directory.iterdir()
            if p.is_dir() and p.name.upper().startswith(PHASE_PREFIXES)
        )
    except OSError:
        return []


def _looks_like_work(directory: Path) -> bool:
    # Require both a manifest and a meaningful lifecycle footprint.
    return _manifest_path(directory) is not None and len(_phase_dirs(directory)) >= 3


def _find_record(work_dir: Path, filenames: tuple[str, ...]) -> Path | None:
    # Prefer canonical locations; never search the partial work/ mirror.
    preferred_dirs = [work_dir, work_dir / "00_ROOT", work_dir / "01_PLAN", work_dir / "04_PLAN"]
    for filename in filenames:
        for directory in preferred_dirs:
            candidate = directory / filename
            if candidate.is_file():
                return candidate
    for filename in filenames:
        try:
            for candidate in sorted(work_dir.rglob(filename)):
                relative_parts = {part.lower() for part in candidate.relative_to(work_dir).parts}
                if relative_parts.isdisjoint({"work", "work_dashboard", ".git", "__pycache__"}):
                    return candidate
        except OSError:
            pass
    return None


def _extract_status(text: str) -> str | None:
    match = re.search(
        r"(?im)^\s*[-*#]*\s*(?:status|trạng\s*thái)\s*[:\-–]\s*(.+)$", text
    )
    if match:
        raw = match.group(1).strip().splitlines()[0]
        found = STATUS_RE.search(raw)
        if found:
            return found.group(1).upper().replace(" ", "_")
        return raw[:40].upper()
    found = STATUS_RE.search(text)
    return found.group(1).upper().replace(" ", "_") if found else None


def _count_nhat_ky_entries(text: str) -> int:
    headings = len(re.findall(r"(?m)^##\s+\S", text))
    bullets = len(re.findall(r"(?m)^\s*[-*]\s*\*\*", text))
    return max(headings, bullets) or (1 if text.strip() else 0)


def _last_modified(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, VN_TZ).isoformat(timespec="seconds")
    except OSError:
        return None


def _iter_files(directory: Path, *, exclude_partial_mirror: bool = False) -> list[Path]:
    excluded = EXCLUDED_ROOT_DIRS if exclude_partial_mirror else {".git", "__pycache__"}
    result: list[Path] = []
    try:
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(directory)
            except ValueError:
                continue
            if any(part in excluded for part in relative.parts):
                continue
            result.append(path)
    except OSError:
        return result
    return result


def scan_work(work_dir: Path, sandbox_id: str, work_name: str, *, single_root: bool = False) -> dict[str, Any]:
    records: dict[str, Any] = {}
    statuses: list[str] = []
    manifest_path = _manifest_path(work_dir)
    if manifest_path:
        manifest_text = _read_text(manifest_path)
        status = _extract_status(manifest_text)
        if status:
            statuses.append(status)
        records["MANIFEST"] = {
            "exists": True,
            "path": str(manifest_path.relative_to(REPO_ROOT)),
            "modified": _last_modified(manifest_path),
        }

    for key, filenames in CORE_RECORDS.items():
        path = _find_record(work_dir, filenames)
        entry: dict[str, Any] = {"exists": path is not None}
        if path is not None:
            content = _read_text(path)
            entry.update({
                "path": str(path.relative_to(REPO_ROOT)),
                "modified": _last_modified(path),
                "size": path.stat().st_size,
            })
            if key == "NHAT_KY":
                entry["entries"] = _count_nhat_ky_entries(content)
            status = _extract_status(content)
            if status:
                entry["status"] = status
                statuses.append(status)
        records[key] = entry

    folders: list[dict[str, Any]] = []
    candidates = _phase_dirs(work_dir)
    if single_root:
        root_records = work_dir / "00_ROOT"
        if root_records.is_dir():
            candidates = [root_records] + candidates
    evidence_files = 0
    md_files = 0
    for folder in candidates:
        files = _iter_files(folder)
        markdown_files = [p for p in files if p.suffix.lower() == ".md"]
        md_files += len(markdown_files)
        if folder.name.upper().startswith(("05_TEST", "06_EVIDENCE", "07_RELEASE")):
            evidence_files += len(files)
        folders.append({
            "name": folder.name,
            "files": len(files),
            "md": len(markdown_files),
            "last_modified": max((_last_modified(p) for p in files), default=None),
        })

    overall = next((s for s in ("BLOCKED", "FAILED") if s in statuses), None)
    if overall is None:
        overall = statuses[0] if statuses else "CHUA_XAC_MINH"

    all_paths = _iter_files(work_dir, exclude_partial_mirror=single_root)
    latest = max(all_paths, key=lambda p: p.stat().st_mtime) if all_paths else None
    return {
        "sandbox_id": sandbox_id,
        "work_name": work_name,
        "path": str(work_dir.relative_to(REPO_ROOT)) if work_dir != REPO_ROOT else ".",
        "status": overall,
        "statuses_found": statuses,
        "records": records,
        "folders": folders,
        "total_files": len(all_paths),
        "md_files": md_files,
        "evidence_files": evidence_files,
        "last_activity": _last_modified(latest) if latest else None,
    }


def scan_all() -> dict[str, Any]:
    works: list[dict[str, Any]] = []
    root_is_single_work = (
        (REPO_ROOT / "00_ROOT").is_dir()
        and _manifest_path(REPO_ROOT) is not None
        and len(_phase_dirs(REPO_ROOT)) >= 3
    )

    if root_is_single_work:
        works.append(scan_work(REPO_ROOT, REPO_ROOT.name, "Work 32", single_root=True))
    elif WORK_ROOT.is_dir():
        for sandbox in sorted(p for p in WORK_ROOT.iterdir() if p.is_dir()):
            candidates = sorted(p for p in sandbox.iterdir() if p.is_dir() and _looks_like_work(p))
            for work_dir in candidates:
                works.append(scan_work(work_dir, sandbox.name, work_dir.name))

    return {
        "generated_at": datetime.now(VN_TZ).isoformat(timespec="seconds"),
        "repo_root": str(REPO_ROOT),
        "works": works,
        "discovery_mode": "single-work-root" if root_is_single_work else "multi-work",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(scan_all(), indent=2, ensure_ascii=False))
