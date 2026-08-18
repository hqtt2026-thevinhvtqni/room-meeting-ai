# core/vscode_agent.py
# VSCodeAgent - Cánh tay điều khiển VSCode có kiểm soát, giống hệt FileOpsAgent
import subprocess
import os
from pathlib import Path
from core.file_ops_agent import FileOpsAgent

class VSCodeAgent:
    def __init__(self, identity: str):
        self.identity = identity
        self.file_agent = FileOpsAgent(identity) # Dùng lại để check quyền

    def _try_open_vscode(self, target_path: str):
        """Thử mở bằng lệnh 'code', nếu máy anh chưa có thì bỏ qua, không lỗi"""
        try:
            # Dùng shell=True để nó tự tìm code.cmd trên Windows
            subprocess.Popen(f'code "{target_path}"', shell=True)
            return True
        except Exception:
            return False

    # 1. Mở file
    def open_file(self, file_path: str):
        content = self.file_agent.read_file(file_path) # Check quyền + file tồn tại qua FileOpsAgent
        opened = self._try_open_vscode(file_path)
        if opened:
            return f"OPENED in VSCode: {file_path}"
        else:
            return f"READ OK (VSCode CLI chưa cài, nhưng quyền đã check): {file_path} | {len(content)} chars"

    # 2. Mở thư mục
    def open_folder(self, folder_path: str):
        self.file_agent.list_dir(folder_path) # Check quyền đọc folder
        self._try_open_vscode(folder_path)
        return f"OPENED FOLDER: {folder_path}"

    # 3. Tạo file và mở luôn
    def create_and_open(self, file_path: str, content: str = ""):
        result = self.file_agent.create_file(file_path, content) # Đã có check quyền + không ghi đè
        self._try_open_vscode(file_path)
        return f"CREATED & OPENED: {file_path}"

    # 4. Tạo thư mục
    def create_folder(self, folder_path: str):
        return self.file_agent.create_folder(folder_path)

    # 5. So sánh 2 file
    def diff(self, file_a: str, file_b: str):
        self.file_agent.read_file(file_a)
        self.file_agent.read_file(file_b)
        try:
            subprocess.Popen(f'code --diff "{file_a}" "{file_b}"', shell=True)
            return f"DIFF OPENED: {file_a} vs {file_b}"
        except Exception as e:
            return f"DIFF CHECK OK, lỗi mở VSCode: {e}"