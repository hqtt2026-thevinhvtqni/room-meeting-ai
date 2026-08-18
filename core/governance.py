# core/governance.py - V2 - Capability + Vung + Authority
import os
import time
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MissionContext:
    name: str = "default"
    allow_delete: bool = False
    allow_edit_protected: bool = False
    allowed_scopes: list = None # vd: ["research/RC007/*"]
    def __post_init__(self):
        if self.allowed_scopes is None:
            self.allowed_scopes = ["research/*", "docs/*", "tmp/*"]

class Governance:
    # Vung cam tuyet doi - bat ke Mission nao
    PROTECTED = [
        "core/governance.py",
        "core/vscode_agent.py",
        "core/file_ops_agent.py",
        "XU_CORE.md",
        "audit.log",
        "meetings/",
        ".git/",
        "trash/"
    ]

    # Capability Matrix theo Identity
    CAPABILITIES = {
        "vinh": {
            "READ": ["*"],
            "CREATE": ["*"],
            "EDIT": ["*"],
            "DELETE": ["*"],
            "MOVE": ["*"]
        },
        "agent_llama": {
            "READ": ["research/*", "docs/*", "notes/*", "tmp/*"],
            "CREATE": ["research/*", "tmp/*", "docs/*"],
            "EDIT": ["research/*", "tmp/*", "docs/*"],
            "DELETE": ["tmp/*", "research/draft/*", "research/RC007/tmp/*"], # Chi vung rac moi duoc xoa
            "MOVE": ["research/*", "tmp/*"]
        },
        # XU (CEO) va QUAN_GIA (Operations) can quyen EDIT tren meetings/*
        # de dong (close) meeting - dung boi meeting_manager.py::Meeting.close().
        # Khong dung "*" nhu vinh de tranh cap quyen ngoai y muon; chi mo rong
        # dung pham vi can cho vong doi meeting + cac vung lam viec thong thuong.
        "xu": {
            "READ": ["*"],
            "CREATE": ["meetings/*", "research/*", "docs/*", "tmp/*"],
            "EDIT": ["meetings/*", "research/*", "docs/*", "tmp/*"],
            "DELETE": ["tmp/*"],
            "MOVE": ["meetings/*", "research/*", "tmp/*"]
        },
        "quan_gia": {
            "READ": ["*"],
            "CREATE": ["meetings/*", "research/*", "docs/*", "tmp/*"],
            "EDIT": ["meetings/*", "research/*", "docs/*", "tmp/*"],
            "DELETE": ["tmp/*"],
            "MOVE": ["meetings/*", "research/*", "tmp/*"]
        }
    }

    def _is_protected(self, path: str) -> bool:
        path = path.replace("\\", "/")
        for p in self.PROTECTED:
            if path == p.rstrip("/") or path.startswith(p):
                return True
        return False

    def _match_scope(self, path: str, scopes: list) -> bool:
        path = path.replace("\\", "/")
        for scope in scopes:
            if scope == "*" or scope == "*/*":
                return True
            if scope.endswith("/*"):
                prefix = scope[:-2]
                if path.startswith(prefix + "/") or path == prefix:
                    return True
            elif scope == path or scope in path:
                return True
        return False

    def check(self, identity: str, capability: str, path: str, mission: MissionContext):
        identity = identity or "agent_llama"
        caps = self.CAPABILITIES.get(identity, self.CAPABILITIES["agent_llama"])

        # 1. Kiem tra protected
        if self._is_protected(path):
            if not mission.allow_edit_protected:
                return False, f"DENY: {path} la Protected Artifact (core/governance, XU_CORE, meetings/). Can Authority XU."

        # 2. Kiem tra capability co ton tai khong
        allowed_scopes = caps.get(capability, [])
        if not allowed_scopes:
            return False, f"DENY: Identity {identity} khong co quyen {capability}"

        # 3. Kiem tra path co nam trong scope duoc phep khong
        if not self._match_scope(path, allowed_scopes):
            # Ngoai le: neu mission mo rong scope
            if not self._match_scope(path, mission.allowed_scopes):
                return False, f"DENY: {path} nam ngoai vung {capability} cho phep cua {identity}. Vung cho phep: {allowed_scopes}"

        # 4. Dieu kien dac biet cho DELETE
        if capability == "DELETE":
            if not mission.allow_delete:
                return False, f"DENY: DELETE can Mission co allow_delete=True. Mission hien tai: {mission.name}"
            return True, f"ALLOW (CONDITIONAL): {capability} {path} -> se Soft-Delete vao trash/ + ghi Audit"

        return True, f"ALLOW: {capability} {path}"

    def audit(self, identity, capability, path, result, mission: MissionContext):
        os.makedirs("audit", exist_ok=True)
        log_path = "audit/audit.log"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Identity={identity} | Mission={mission.name} | {capability} | {path} | {result}\n")

# Singleton
GOV = Governance()