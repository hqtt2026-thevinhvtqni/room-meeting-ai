"""Work 28 v54 Sandbox file-operation handlers.

Real file operations inside a provider-rooted sandbox with path-escape and
symlink protection. Execution/evidence tools are NOT implemented here on
purpose: they must delegate to the approved Core/W12-W13 runtime, and this
build does not fake them.
"""
from __future__ import annotations
import fnmatch
import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from mcp8020_catalog_v54 import ToolCallError

WORK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
MAX_SEARCH_FILE_BYTES = 1_000_000

def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class SandboxProvider:
    def __init__(self, root: str | os.PathLike) -> None:
        self._root = Path(root)
        os.makedirs(self._root, exist_ok=True)
        self._works: dict[str, dict[str, Any]] = {}

    def _require_work(self, work_id: str) -> dict[str, Any]:
        work = self._works.get(work_id)
        if work is None:
            raise ToolCallError("NOT_FOUND", "work sandbox not found: " + work_id)
        return work

    def _resolve(self, work_id: str, rel: str) -> tuple[Path, Path, str]:
        self._require_work(work_id)
        rel = rel or ""
        if rel.startswith("/") or rel.startswith("\\") or ":" in rel:
            raise ToolCallError("INVALID_PATH", "absolute or drive paths are not allowed")
        work_root = os.path.realpath(self._root / work_id)
        target_real = os.path.realpath(self._root / work_id / rel)
        if target_real != work_root and not target_real.startswith(work_root + os.sep):
            raise ToolCallError("PATH_ESCAPE", "path escapes the work sandbox boundary")
        rel_norm = os.path.relpath(target_real, work_root)
        return Path(target_real), Path(work_root), rel_norm

    def sandbox_list_works(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        items = sorted(self._works.values(), key=lambda w: w["work_id"])
        return {"works": items[offset:offset + limit], "total": len(items)}

    def sandbox_create_work(self, work_id: str, work_name: str, identity_id: str | None = None) -> dict[str, Any]:
        if not WORK_ID_RE.match(work_id):
            raise ToolCallError("INVALID_INPUT", "work_id does not match the required pattern")
        if work_id in self._works:
            raise ToolCallError("ALREADY_EXISTS", "work already exists: " + work_id)
        os.makedirs(self._root / work_id, exist_ok=False)
        record = {"work_id": work_id, "work_name": work_name, "identity_id": identity_id, "created_at": datetime.now(timezone.utc).isoformat()}
        self._works[work_id] = record
        return {"work_id": work_id, "created": True}

    def _list_entries(self, work_id: str, path: str) -> dict[str, Any]:
        target, work_root, rel_norm = self._resolve(work_id, path)
        if not target.exists():
            raise ToolCallError("NOT_FOUND", "path not found: " + path)
        if target.is_file():
            raise ToolCallError("INVALID_PATH", "path is a file, not a directory")
        entries = []
        for child in sorted(os.listdir(target)):
            child_path = target / child
            entries.append({"name": child, "type": "directory" if child_path.is_dir() else "file", "size": child_path.stat().st_size if child_path.is_file() else None})
        return {"work_id": work_id, "path": rel_norm, "entries": entries}

    def sandbox_list(self, work_id: str, path: str = "") -> dict[str, Any]:
        return self._list_entries(work_id, path)

    def _require_file(self, work_id: str, path: str) -> tuple[Path, Path, str]:
        target, work_root, rel_norm = self._resolve(work_id, path)
        if not target.exists():
            raise ToolCallError("NOT_FOUND", "file not found: " + path)
        if target.is_dir():
            raise ToolCallError("INVALID_PATH", "path is a directory, not a file")
        return target, work_root, rel_norm

    def sandbox_read(self, work_id: str, path: str, offset: int = 0, length: int = 16384) -> dict[str, Any]:
        target, _, rel_norm = self._require_file(work_id, path)
        data = target.read_bytes()
        window = data[offset:offset + length]
        try:
            text = window.decode("utf-8")
        except UnicodeDecodeError:
            raise ToolCallError("DECODE_ERROR", "range does not decode as UTF-8")
        return {"path": rel_norm, "content": text, "offset": offset, "length": len(window), "total_bytes": len(data), "sha256": _sha256_bytes(data)}

    def sandbox_write(self, work_id: str, path: str, content: str, overwrite: bool = False) -> dict[str, Any]:
        target, _, rel_norm = self._resolve(work_id, path)
        if target.exists():
            if target.is_dir():
                raise ToolCallError("INVALID_PATH", "path is a directory")
            if not overwrite:
                raise ToolCallError("ALREADY_EXISTS", "file exists and overwrite is False: " + path)
        os.makedirs(target.parent, exist_ok=True)
        data = content.encode("utf-8")
        target.write_bytes(data)
        return {"path": rel_norm, "sha256": _sha256_bytes(data), "bytes": len(data), "overwritten": target.exists()}

    def sandbox_append(self, work_id: str, path: str, content: str) -> dict[str, Any]:
        target, _, rel_norm = self._require_file(work_id, path)
        with open(target, "ab") as handle:
            handle.write(content.encode("utf-8"))
        data = target.read_bytes()
        return {"path": rel_norm, "sha256": _sha256_bytes(data), "bytes": len(data)}

    def sandbox_delete(self, work_id: str, path: str, confirm_delete: bool = False) -> dict[str, Any]:
        if not confirm_delete:
            raise ToolCallError("POLICY_REFUSED", "delete requires confirm_delete=true")
        target, _, rel_norm = self._require_file(work_id, path)
        target.unlink()
        return {"path": rel_norm, "deleted": True}

    def sandbox_search(self, work_id: str, query: str, path: str = "", glob: str = "*", limit: int = 20) -> dict[str, Any]:
        base, _, _ = self._resolve(work_id, path)
        if not base.exists():
            raise ToolCallError("NOT_FOUND", "search path not found: " + path)
        if base.is_file():
            raise ToolCallError("INVALID_PATH", "search path must be a directory")
        needle = query.lower()
        matches: list[dict[str, Any]] = []
        for root, _dirs, files in os.walk(base):
            for fname in sorted(files):
                if len(matches) >= limit:
                    break
                full = Path(root) / fname
                if not fnmatch.fnmatch(fname, glob):
                    continue
                rel = os.path.relpath(full, base)
                if needle in fname.lower():
                    matches.append({"path": rel, "match": "filename"})
                    continue
                if full.stat().st_size > MAX_SEARCH_FILE_BYTES:
                    continue
                try:
                    text = full.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                for line_no, line in enumerate(text.splitlines(), start=1):
                    if needle in line.lower():
                        matches.append({"path": rel, "line_number": line_no, "line": line.strip()[:200]})
                        break
            if len(matches) >= limit:
                break
        return {"query": query, "matches": matches[:limit]}

    def sandbox_read_file_metadata(self, work_id: str, path: str) -> dict[str, Any]:
        target, _, rel_norm = self._require_file(work_id, path)
        stat = target.stat()
        return {"path": rel_norm, "size": stat.st_size, "sha256": _sha256_bytes(target.read_bytes()), "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()}

    def sandbox_create_directory(self, work_id: str, path: str) -> dict[str, Any]:
        target, _, rel_norm = self._resolve(work_id, path)
        if target.exists():
            raise ToolCallError("ALREADY_EXISTS", "path already exists: " + path)
        try:
            os.makedirs(target, exist_ok=False)
        except FileNotFoundError:
            raise ToolCallError("NOT_FOUND", "parent directory does not exist")
        return {"path": rel_norm, "created": True}

    def sandbox_copy_file(self, work_id: str, source_path: str, destination_path: str) -> dict[str, Any]:
        source, _, src_rel = self._require_file(work_id, source_path)
        destination, _, dst_rel = self._resolve(work_id, destination_path)
        if destination.exists():
            raise ToolCallError("ALREADY_EXISTS", "destination already exists: " + destination_path)
        if not destination.parent.exists():
            raise ToolCallError("NOT_FOUND", "destination parent directory does not exist")
        data = source.read_bytes()
        destination.write_bytes(data)
        return {"source": src_rel, "destination": dst_rel, "sha256": _sha256_bytes(data), "bytes": len(data)}

    def sandbox_move_file(self, work_id: str, source_path: str, destination_path: str) -> dict[str, Any]:
        source, _, src_rel = self._require_file(work_id, source_path)
        destination, _, dst_rel = self._resolve(work_id, destination_path)
        if destination.exists():
            raise ToolCallError("ALREADY_EXISTS", "destination already exists: " + destination_path)
        if not destination.parent.exists():
            raise ToolCallError("NOT_FOUND", "destination parent directory does not exist")
        data = source.read_bytes()
        destination.write_bytes(data)
        source.unlink()
        return {"source": src_rel, "destination": dst_rel, "sha256": _sha256_bytes(data), "moved": True}

    def sandbox_get_manifest(self, work_id: str, path: str = "") -> dict[str, Any]:
        self._require_work(work_id)
        base, _, _ = self._resolve(work_id, path)
        if not base.exists() or base.is_file():
            raise ToolCallError("INVALID_PATH", "manifest path must be an existing directory")
        files = []
        for root, _dirs, fnames in os.walk(base):
            for fname in sorted(fnames):
                full = Path(root) / fname
                files.append({"path": os.path.relpath(full, base), "size": full.stat().st_size, "sha256": _sha256_bytes(full.read_bytes())})
        return {"work": dict(self._works[work_id]), "base_path": path, "files": files}

    def sandbox_validate_path(self, work_id: str, path: str, operation: str) -> dict[str, Any]:
        target, _, rel_norm = self._resolve(work_id, path)
        if operation not in ("READ", "WRITE", "DELETE"):
            raise ToolCallError("INVALID_INPUT", "operation must be READ, WRITE, or DELETE")
        return {"path": path, "normalized_path": rel_norm, "operation": operation, "allowed": True, "exists": target.exists()}
