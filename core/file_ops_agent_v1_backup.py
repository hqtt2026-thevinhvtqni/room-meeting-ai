"""
FileOpsAgent — ROOM HOP v0.2

Agent có quyền tạo / sửa / xóa file và thư mục TRONG phạm vi dự án
room_hop, thông qua AuthorizationEngine (core/governance.py) — không tự
quyết định quyền của chính mình.

An toàn theo nhiều lớp (defense in depth), không chỉ dựa vào 1 chỗ:

1. SANDBOX: mọi path đều bị resolve() và ép phải nằm trong PROJECT_ROOT.
   Path traversal (../..) ra ngoài dự án sẽ bị chặn ngay, agent nào
   gọi cũng vậy — không liên quan tới quyền hạn.
2. CLASSIFY: mỗi path được phân loại vào đúng ResourceType đã có sẵn
   (CORE/GOVERNANCE/CONTEXT/PROJECT_STATE/SESSION) TRƯỚC khi cho phép
   rơi vào nhánh WORKSPACE (file thường). Nghĩa là dù agent có quyền
   WORKSPACE:WRITE cũng không đụng được XU_CORE.md — nó không được
   phân loại là WORKSPACE ngay từ đầu.
3. HARD_BLOCK: một số path bị khóa cứng tuyệt đối, không agent nào kể
   cả VINH-as-agent-id được thao tác qua tool này (chính engine phân
   quyền, và schema — sửa qua đây là tự ý leo quyền). Muốn sửa các file
   này phải làm thủ công ngoài agent.
4. AUDIT: mọi thao tác WRITE (tạo/sửa/xóa) đều append vào audit log
   JSONL, không xóa/sửa được ngược (append-only), tương tự triết lý
   Meeting Log (core/meeting_log.py).
5. MEETINGS EXCLUDED: thư mục meetings/ hoàn toàn nằm ngoài phạm vi
   agent này — đó là evidence, có MeetingManager/MeetingLog riêng quản
   lý vòng đời + checksum, trộn vào đây sẽ phá tính toàn vẹn.

Không đổi 4 lõi v0.1 (Meeting Manager, Agent Registry, Context Loader,
Meeting Log) và không đổi Discussion Engine.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from core.governance import (
    Action,
    AuthorizationResult,
    ResourceType,
    get_authorization_engine,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG_PATH = PROJECT_ROOT / "core" / "file_ops_audit.jsonl"

# Path tuyệt đối bị khóa — không qua FileOpsAgent được, bất kể agent_id nào.
# So khớp theo path tương đối (posix, lowercase) tính từ PROJECT_ROOT.
HARD_BLOCKED_RELATIVE_PATHS = {
    "core/governance.py",       # chính authorization engine — cấm tự sửa luật
    "core/file_ops_agent.py",   # chính module này — cấm tự sửa quyền của mình
    "core/file_ops_audit.jsonl",  # audit log — append-only, không cho ghi đè qua tool
}
HARD_BLOCKED_RELATIVE_PREFIXES = (
    "meetings/",   # evidence bất biến, có MeetingManager/MeetingLog riêng
    ".git/",
)

# Map path tương đối -> ResourceType đã định nghĩa sẵn trong governance.py.
# Khớp theo exact path hoặc theo thư mục cha.
_EXACT_RESOURCE_MAP = {
    "context/XU_CORE.md": ResourceType.CORE,
    "context/XU_MEMORY.md": ResourceType.CORE,
    "context/PROJECT_STATE.md": ResourceType.PROJECT_STATE,
    "context/XU_SESSION.md": ResourceType.SESSION,
    "AGENTS.md": ResourceType.GOVERNANCE,
}
_PREFIX_RESOURCE_MAP = {
    "context/": ResourceType.CONTEXT,   # các file context/ khác (đọc-only)
    "schemas/": ResourceType.GOVERNANCE,  # schema là hợp đồng cấu trúc, khóa như governance
    "agents/": ResourceType.GOVERNANCE,   # hồ sơ agent — coi như governance, chỉ VINH sửa qua tool này
}


class FileOpsError(Exception):
    """Lỗi chung của FileOpsAgent — bao gồm cả DENY quyền và path không hợp lệ."""


@dataclass
class FileOpsResult:
    ok: bool
    action: str
    path: str
    reason: str = ""


def classify_path(rel_posix: str) -> ResourceType:
    """Phân loại 1 path tương đối vào đúng ResourceType đã có trong governance.py."""
    if rel_posix in _EXACT_RESOURCE_MAP:
        return _EXACT_RESOURCE_MAP[rel_posix]
    for prefix, rtype in _PREFIX_RESOURCE_MAP.items():
        if rel_posix.startswith(prefix):
            return rtype
    return ResourceType.WORKSPACE


class FileOpsAgent:
    """
    id: dùng làm agent_id khi check quyền qua AuthorizationEngine, ví dụ
    "xu", "claude", "quan_gia", "vinh". Agent lạ mặc định OTHER (chỉ đọc).
    """

    ROLE = "FILE-OPS"

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._auth = get_authorization_engine()

    # -- helpers ------------------------------------------------------

    def _resolve(self, rel_path: str) -> tuple[Path, str]:
        """
        Resolve path tương đối thành path tuyệt đối, ép nằm trong
        PROJECT_ROOT. Trả về (abs_path, rel_posix). Raise FileOpsError
        nếu path thoát ra ngoài sandbox.
        """
        candidate = (PROJECT_ROOT / rel_path).resolve()
        try:
            rel = candidate.relative_to(PROJECT_ROOT)
        except ValueError:
            raise FileOpsError(
                f"SANDBOX VIOLATION: '{rel_path}' thoát ra ngoài project root — từ chối."
            )
        rel_posix = rel.as_posix()
        return candidate, rel_posix

    def _check_hard_block(self, rel_posix: str) -> None:
        if rel_posix in HARD_BLOCKED_RELATIVE_PATHS:
            raise FileOpsError(f"HARD BLOCKED: '{rel_posix}' không thể thao tác qua FileOpsAgent.")
        if rel_posix.startswith(HARD_BLOCKED_RELATIVE_PREFIXES):
            raise FileOpsError(f"HARD BLOCKED: '{rel_posix}' nằm trong vùng cấm (meetings/.git).")

    def _authorize(self, rel_posix: str, action: Action) -> AuthorizationResult:
        resource_type = classify_path(rel_posix)
        return self._auth.check(self.agent_id, resource_type, action)

    def _audit(self, result: FileOpsResult) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_id": self.agent_id,
            "action": result.action,
            "path": result.path,
            "ok": result.ok,
            "reason": result.reason,
        }
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _guard(self, rel_path: str, action: Action, op_name: str) -> str:
        """Chạy đủ 3 lớp bảo vệ (sandbox -> hard block -> authorization). Trả về rel_posix nếu PASS."""
        _, rel_posix = self._resolve(rel_path)
        try:
            self._check_hard_block(rel_posix)
            auth = self._authorize(rel_posix, action)
            if not auth.allowed:
                raise FileOpsError(f"DENY: {auth.reason}")
        except FileOpsError as e:
            self._audit(FileOpsResult(ok=False, action=op_name, path=rel_posix, reason=str(e)))
            raise
        return rel_posix

    # -- read (không cần audit, không cần ghi) -------------------------

    def read_file(self, rel_path: str) -> str:
        abs_path, rel_posix = self._resolve(rel_path)
        self._check_hard_block(rel_posix)
        auth = self._authorize(rel_posix, Action.READ)
        if not auth.allowed:
            raise FileOpsError(f"DENY: {auth.reason}")
        return abs_path.read_text(encoding="utf-8")

    def list_dir(self, rel_path: str = ".") -> list[str]:
        abs_path, rel_posix = self._resolve(rel_path)
        self._check_hard_block(rel_posix if rel_posix != "." else "")
        if not abs_path.is_dir():
            raise FileOpsError(f"'{rel_path}' không phải thư mục.")
        return sorted(p.name for p in abs_path.iterdir())

    # -- write ----------------------------------------------------------

    def create_file(self, rel_path: str, content: str = "") -> FileOpsResult:
        rel_posix = self._guard(rel_path, Action.WRITE, "create_file")
        abs_path = PROJECT_ROOT / rel_posix
        if abs_path.exists():
            result = FileOpsResult(False, "create_file", rel_posix, "File đã tồn tại — dùng edit_file để sửa.")
            self._audit(result)
            raise FileOpsError(result.reason)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(content, encoding="utf-8")
        result = FileOpsResult(True, "create_file", rel_posix, "OK")
        self._audit(result)
        return result

    def edit_file(self, rel_path: str, content: str, mode: str = "overwrite") -> FileOpsResult:
        if mode not in ("overwrite", "append"):
            raise FileOpsError("mode phải là 'overwrite' hoặc 'append'.")
        rel_posix = self._guard(rel_path, Action.WRITE, "edit_file")
        abs_path = PROJECT_ROOT / rel_posix
        if not abs_path.exists():
            result = FileOpsResult(False, "edit_file", rel_posix, "File chưa tồn tại — dùng create_file trước.")
            self._audit(result)
            raise FileOpsError(result.reason)
        if mode == "overwrite":
            abs_path.write_text(content, encoding="utf-8")
        else:
            with open(abs_path, "a", encoding="utf-8") as f:
                f.write(content)
        result = FileOpsResult(True, "edit_file", rel_posix, f"OK ({mode})")
        self._audit(result)
        return result

    def delete_file(self, rel_path: str) -> FileOpsResult:
        rel_posix = self._guard(rel_path, Action.WRITE, "delete_file")
        abs_path = PROJECT_ROOT / rel_posix
        if not abs_path.exists() or not abs_path.is_file():
            result = FileOpsResult(False, "delete_file", rel_posix, "File không tồn tại.")
            self._audit(result)
            raise FileOpsError(result.reason)
        abs_path.unlink()
        result = FileOpsResult(True, "delete_file", rel_posix, "OK")
        self._audit(result)
        return result

    def create_folder(self, rel_path: str) -> FileOpsResult:
        rel_posix = self._guard(rel_path, Action.WRITE, "create_folder")
        abs_path = PROJECT_ROOT / rel_posix
        abs_path.mkdir(parents=True, exist_ok=True)
        result = FileOpsResult(True, "create_folder", rel_posix, "OK")
        self._audit(result)
        return result

    def delete_folder(self, rel_path: str, recursive: bool = False) -> FileOpsResult:
        rel_posix = self._guard(rel_path, Action.WRITE, "delete_folder")
        abs_path = PROJECT_ROOT / rel_posix
        if not abs_path.exists() or not abs_path.is_dir():
            result = FileOpsResult(False, "delete_folder", rel_posix, "Thư mục không tồn tại.")
            self._audit(result)
            raise FileOpsError(result.reason)
        if any(abs_path.iterdir()) and not recursive:
            result = FileOpsResult(False, "delete_folder", rel_posix, "Thư mục không rỗng — cần recursive=True.")
            self._audit(result)
            raise FileOpsError(result.reason)
        shutil.rmtree(abs_path)
        result = FileOpsResult(True, "delete_folder", rel_posix, f"OK (recursive={recursive})")
        self._audit(result)
        return result
