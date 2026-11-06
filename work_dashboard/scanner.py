"""ROOM HOP — Work Dashboard Scanner.

Quét cây thư mục `work/` và các hồ sơ điều hành chính thức theo
AGENTS.md §06 (BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md, NHAT_KY_HOP_THI_CONG.md)
cộng thêm WORK_MANIFEST.md / README.md để dựng dữ liệu dashboard.

Chỉ đọc (read-only) — không sửa bất kỳ hồ sơ nào.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_ROOT = REPO_ROOT / "work"

VN_TZ = timezone(timedelta(hours=7))

# Tên chuẩn 3 hồ sơ điều hành (AGENTS.md 06.1) + manifest
CORE_RECORDS = {
    "BIEN_BAN": "BIEN_BAN.md",
    "KE_HOACH": "KE_HOACH_THI_CONG_XU.md",
    "NHAT_KY": "NHAT_KY_HOP_THI_CONG.md",
}
MANIFEST_NAME = "WORK_MANIFEST.md"

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


def _find_record(work_dir: Path, filename: str) -> Path | None:
    """Tìm hồ sơ ở gốc Work hoặc trong 00_ROOT, ưu tiên gốc."""
    direct = work_dir / filename
    if direct.is_file():
        return direct
    for sub in sorted(work_dir.glob("*/" + filename)):
        return sub
    # fallback: tìm sâu
    for p in sorted(work_dir.rglob(filename)):
        return p
    return None


def _extract_status(text: str) -> str | None:
    """Lấy trạng thái khai báo gần nhất dạng `- Status: XXX` hoặc keyword đầu tiên."""
    m = re.search(r"(?im)^\s*[-*#]*\s*(?:status|trạng\s*thái)\s*[:\-–]\s*(.+)$", text)
    if m:
        raw = m.group(1).strip().splitlines()[0]
        s = STATUS_RE.search(raw)
        if s:
            return s.group(1).upper().replace(" ", "_")
        return raw[:40].upper()
    s = STATUS_RE.search(text)
    if s:
        return s.group(1).upper().replace(" ", "_")
    return None


def _count_nhat_ky_entries(text: str) -> int:
    """Đếm số mục ghi trong Nhật ký (heading ## hoặc bullet có in đậm)."""
    headings = len(re.findall(r"(?m)^##\s+\S", text))
    bullets = len(re.findall(r"(?m)^\s*[-*]\s*\*\*", text))
    return max(headings, bullets) or (1 if text.strip() else 0)


def _last_modified(path: Path) -> str | None:
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts, VN_TZ).isoformat(timespec="seconds")
    except OSError:
        return None


def scan_work(work_dir: Path, sandbox_id: str, work_name: str) -> dict[str, Any]:
    records: dict[str, Any] = {}
    statuses: list[str] = []
    evidence_files = 0
    md_files = 0

    manifest_path = _find_record(work_dir, MANIFEST_NAME)
    manifest_text = _read_text(manifest_path) if manifest_path else ""
    if manifest_path:
        st = _extract_status(manifest_text)
        if st:
            statuses.append(st)
        records["MANIFEST"] = {
            "exists": True,
            "path": str(manifest_path.relative_to(REPO_ROOT)),
            "modified": _last_modified(manifest_path),
        }

    for key, fname in CORE_RECORDS.items():
        p = _find_record(work_dir, fname)
        exists = p is not None
        entry: dict[str, Any] = {"exists": exists}
        if exists and p is not None:
            text = _read_text(p)
            entry["path"] = str(p.relative_to(REPO_ROOT))
            entry["modified"] = _last_modified(p)
            entry["size"] = p.stat().st_size
            if key == "NHAT_KY":
                entry["entries"] = _count_nhat_ky_entries(text)
            st = _extract_status(text)
            if st:
                entry["status"] = st
                statuses.append(st)
        records[key] = entry

    folders: list[dict[str, Any]] = []
    for sub in sorted(p for p in work_dir.iterdir() if p.is_dir()):
        files = [f for f in sub.rglob("*") if f.is_file()]
        mds = [f for f in files if f.suffix.lower() == ".md"]
        md_files += len(mds)
        up = sub.name.upper()
        if up.startswith(("05_TEST", "06_EVIDENCE", "07_RELEASE")) or up in ("EVIDENCE", "TEST", "RELEASE"):
            evidence_files += len(files)
        folders.append({
            "name": sub.name,
            "files": len(files),
            "md": len(mds),
            "last_modified": max(
                (datetime.fromtimestamp(f.stat().st_mtime, VN_TZ).isoformat(timespec="seconds")
                 for f in files), default=None),
        })

    # Trạng thái tổng hợp: BLOCKED/FAILED thắng; nếu không lấy status của manifest
    overall = None
    for prio in ("BLOCKED", "FAILED"):
        if prio in statuses:
            overall = prio
            break
    if overall is None:
        overall = statuses[0] if statuses else "CHUA_XAC_MINH"

    all_paths = [p for p in work_dir.rglob("*") if p.is_file()]
    latest = max(all_paths, key=lambda p: p.stat().st_mtime) if all_paths else None

    return {
        "sandbox_id": sandbox_id,
        "work_name": work_name,
        "path": str(work_dir.relative_to(REPO_ROOT)),
        "status": overall,
        "statuses_found": statuses,
        "records": records,
        "folders": folders,
        "total_files": len(all_paths),
        "md_files": md_files,
        "evidence_files": evidence_files,
        "last_activity": (_last_modified(latest) if latest else None),
    }


def scan_all() -> dict[str, Any]:
    works: list[dict[str, Any]] = []
    if WORK_ROOT.is_dir():
        for sandbox in sorted(p for p in WORK_ROOT.iterdir() if p.is_dir()):
            children = [p for p in sandbox.iterdir() if p.is_dir()]
            if children:
                for wd in children:
                    works.append(scan_work(wd, sandbox.name, wd.name))
            else:
                works.append({
                    "sandbox_id": sandbox.name,
                    "work_name": "(rỗng)",
                    "path": str(sandbox.relative_to(REPO_ROOT)),
                    "status": "CHUA_XAC_MINH",
                    "statuses_found": [],
                    "records": {},
                    "folders": [],
                    "total_files": 0,
                    "md_files": 0,
                    "evidence_files": 0,
                    "last_activity": None,
                })
    return {
        "generated_at": datetime.now(VN_TZ).isoformat(timespec="seconds"),
        "repo_root": str(REPO_ROOT),
        "works": works,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(scan_all(), indent=2, ensure_ascii=False))
