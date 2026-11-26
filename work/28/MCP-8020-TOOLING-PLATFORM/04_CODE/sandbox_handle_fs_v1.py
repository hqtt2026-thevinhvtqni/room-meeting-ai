"""Handle-anchored filesystem primitives for Work 28 uploads.

Linux implementation only. Windows intentionally fails closed until a reviewed
native handle-relative implementation is available. No pathname fallback.
"""
from __future__ import annotations

import hashlib
import os
import stat
from contextlib import contextmanager
from dataclasses import dataclass


class HandleFilesystemError(RuntimeError):
    """A filesystem operation could not be proven to stay under pinned handles."""


@dataclass
class PinnedDirectory:
    fd: int

    def close(self) -> None:
        if self.fd >= 0:
            fd, self.fd = self.fd, -1
            os.close(fd)

    def __enter__(self):
        if self.fd < 0:
            raise HandleFilesystemError("DIRECTORY_HANDLE_CLOSED")
        return self

    def __exit__(self, *_):
        self.close()


@dataclass
class PinnedFile:
    fd: int

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class LinuxHandleFilesystem:
    """All mutations are relative to retained directory/file descriptors.

    The configured Sandbox root is opened by walking from '/' one component at
    a time with O_NOFOLLOW. Every descendant is opened relative to its pinned
    parent descriptor. Callers must retain returned handles for each operation.
    """

    def __init__(self, sandbox_root: str | os.PathLike):
        if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
            raise HandleFilesystemError("HANDLE_BACKEND_UNAVAILABLE")
        if not all(hasattr(os, name) for name in ("open", "mkdir", "link", "unlink")):
            raise HandleFilesystemError("HANDLE_BACKEND_UNAVAILABLE")
        self._root_fd = self._open_absolute_directory(sandbox_root)

    @staticmethod
    def _directory_flags() -> int:
        return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)

    @classmethod
    def _open_absolute_directory(cls, value: str | os.PathLike) -> int:
        raw = os.fspath(value)
        if not isinstance(raw, str) or not raw or "\x00" in raw:
            raise HandleFilesystemError("INVALID_SANDBOX_ROOT")
        absolute = os.path.abspath(raw)
        parts = [p for p in absolute.split(os.sep) if p]
        fd = os.open(os.sep, cls._directory_flags())
        try:
            for part in parts:
                next_fd = os.open(part, cls._directory_flags(), dir_fd=fd)
                os.close(fd)
                fd = next_fd
            if not stat.S_ISDIR(os.fstat(fd).st_mode):
                raise HandleFilesystemError("SANDBOX_ROOT_NOT_DIRECTORY")
            return fd
        except Exception:
            os.close(fd)
            raise

    def close(self) -> None:
        if self._root_fd >= 0:
            os.close(self._root_fd)
            self._root_fd = -1

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    @staticmethod
    def _parts(relative: str) -> tuple[str, ...]:
        if not isinstance(relative, str) or not relative or "\x00" in relative or relative.startswith("/") or "\\" in relative:
            raise HandleFilesystemError("INVALID_RELATIVE_PATH")
        parts = tuple(relative.split("/"))
        if any(p in ("", ".", "..") or ":" in p for p in parts):
            raise HandleFilesystemError("INVALID_RELATIVE_PATH")
        return parts

    @staticmethod
    def _open_child_dir(parent_fd: int, name: str, *, create: bool) -> int:
        flags = LinuxHandleFilesystem._directory_flags()
        try:
            return os.open(name, flags, dir_fd=parent_fd)
        except FileNotFoundError:
            if not create:
                raise
            try:
                os.mkdir(name, mode=0o700, dir_fd=parent_fd)
            except FileExistsError:
                pass
            return os.open(name, flags, dir_fd=parent_fd)

    @contextmanager
    def work(self, work_id: str, *, create: bool = False):
        if not isinstance(work_id, str) or not work_id or "/" in work_id or work_id in (".", ".."):
            raise HandleFilesystemError("INVALID_WORK_ID")
        handle = PinnedDirectory(self._open_child_dir(self._root_fd, work_id, create=create))
        try:
            yield handle
        finally:
            handle.close()

    @contextmanager
    def directory(self, parent_fd: int, relative: str, *, create: bool = False):
        parts = self._parts(relative)
        fd = os.dup(parent_fd)
        try:
            for part in parts:
                next_fd = self._open_child_dir(fd, part, create=create)
                os.close(fd)
                fd = next_fd
            handle = PinnedDirectory(fd)
            fd = -1
            try:
                yield handle
            finally:
                handle.close()
        finally:
            if fd >= 0:
                os.close(fd)

    @staticmethod
    def create_exclusive(parent_fd: int, name: str, mode: int = 0o600) -> PinnedFile:
        if not name or name in (".", "..") or "/" in name or "\\" in name:
            raise HandleFilesystemError("INVALID_LEAF_NAME")
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(name, flags, mode, dir_fd=parent_fd)
        return PinnedFile(fd)

    @staticmethod
    def open_file(parent_fd: int, name: str, *, writable: bool = False) -> PinnedFile:
        if not name or name in (".", "..") or "/" in name or "\\" in name:
            raise HandleFilesystemError("INVALID_LEAF_NAME")
        flags = (os.O_RDWR if writable else os.O_RDONLY) | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(name, flags, dir_fd=parent_fd)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            raise HandleFilesystemError("NOT_REGULAR_FILE")
        return PinnedFile(fd)

    @staticmethod
    def write_at(file_fd: int, offset: int, payload: bytes) -> None:
        if offset < 0 or not isinstance(payload, bytes):
            raise HandleFilesystemError("INVALID_WRITE")
        view = memoryview(payload)
        written = 0
        while written < len(view):
            count = os.pwrite(file_fd, view[written:], offset + written)
            if count <= 0:
                raise HandleFilesystemError("SHORT_WRITE")
            written += count
        os.fsync(file_fd)

    @staticmethod
    def truncate(file_fd: int, length: int) -> None:
        if length < 0:
            raise HandleFilesystemError("INVALID_TRUNCATE")
        os.ftruncate(file_fd, length)
        os.fsync(file_fd)

    @staticmethod
    def digest(file_fd: int) -> tuple[int, str]:
        h = hashlib.sha256()
        size = 0
        offset = 0
        while True:
            block = os.pread(file_fd, 1024 * 1024, offset)
            if not block:
                break
            size += len(block)
            offset += len(block)
            h.update(block)
        return size, h.hexdigest()

    @staticmethod
    def promote_no_replace(source_dir_fd: int, source_name: str,
                           destination_dir_fd: int, destination_name: str) -> None:
        """Atomic no-replace publication using linkat semantics on pinned dirs."""
        try:
            os.link(source_name, destination_name,
                    src_dir_fd=source_dir_fd, dst_dir_fd=destination_dir_fd,
                    follow_symlinks=False)
        except FileExistsError:
            raise
        except (NotImplementedError, TypeError) as exc:
            raise HandleFilesystemError("ATOMIC_NO_REPLACE_UNAVAILABLE") from exc
        os.fsync(destination_dir_fd)

    @staticmethod
    def unlink(parent_fd: int, name: str, *, missing_ok: bool = False) -> None:
        try:
            os.unlink(name, dir_fd=parent_fd)
        except FileNotFoundError:
            if not missing_ok:
                raise
        os.fsync(parent_fd)
