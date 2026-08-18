# core/file_ops_agent.py - V2 - Soft Delete + Audit
import os
import shutil
import time
from pathlib import Path
from.governance import GOV, MissionContext

class FileOpsAgent:
    def __init__(self, identity="vinh", mission: MissionContext = None):
        self.identity = identity
        self.mission = mission or MissionContext(name="default_research", allow_delete=False)
        self.trash_dir = Path("trash")
        self.trash_dir.mkdir(exist_ok=True)

    def set_mission(self, mission: MissionContext):
        self.mission = mission

    def create_folder(self, path: str):
        ok, msg = GOV.check(self.identity, "CREATE", path, self.mission)
        if not ok:
            raise PermissionError(msg)
        os.makedirs(path, exist_ok=True)
        GOV.audit(self.identity, "CREATE_FOLDER", path, "OK", self.mission)
        return f"OK: {msg}"

    def create_file(self, path: str, content: str = ""):
        ok, msg = GOV.check(self.identity, "CREATE", path, self.mission)
        if not ok:
            raise PermissionError(msg)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if os.path.exists(path):
            raise FileExistsError(f"File {path} da ton tai, dung EDIT thay vi CREATE")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        GOV.audit(self.identity, "CREATE", path, "OK", self.mission)
        return f"OK: {msg}"

    def edit_file(self, path: str, content: str):
        ok, msg = GOV.check(self.identity, "EDIT", path, self.mission)
        if not ok:
            raise PermissionError(msg)
        # Backup ban cu truoc khi sua
        if os.path.exists(path):
            backup_name = f"{self.trash_dir}/{int(time.time())}_{Path(path).name}.bak"
            shutil.copy2(path, backup_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        GOV.audit(self.identity, "EDIT", path, "OK", self.mission)
        return f"OK: {msg} | Da backup ban cu vao trash/"

    def read_file(self, path: str):
        ok, msg = GOV.check(self.identity, "READ", path, self.mission)
        if not ok:
            raise PermissionError(msg)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def list_dir(self, path: str):
        ok, msg = GOV.check(self.identity, "READ", path, self.mission)
        if not ok:
            raise PermissionError(msg)
        return os.listdir(path)

    def delete_file(self, path: str):
        # DAY LA DIEM QUAN TRONG - Soft Delete
        ok, msg = GOV.check(self.identity, "DELETE", path, self.mission)
        if not ok:
            raise PermissionError(msg)

        if not os.path.exists(path):
            return f"File {path} khong ton tai"

        # Soft delete: move vao trash/ chu khong xoa han
        dest = self.trash_dir / f"{int(time.time())}_{Path(path).name}"
        shutil.move(path, dest)
        GOV.audit(self.identity, "DELETE_SOFT", path, f"Moved to {dest}", self.mission)
        return f"OK: {msg} | Da Soft-Delete: {path} -> {dest} (co the phuc hoi)"

    def delete_file_hard(self, path: str):
        # Chi XU moi duoc goi ham nay, khong expose cho Agent
        if self.identity!= "vinh":
            raise PermissionError("Hard Delete chi XU (vinh) moi duoc thuc hien")
        os.remove(path)
        return "Hard Deleted"