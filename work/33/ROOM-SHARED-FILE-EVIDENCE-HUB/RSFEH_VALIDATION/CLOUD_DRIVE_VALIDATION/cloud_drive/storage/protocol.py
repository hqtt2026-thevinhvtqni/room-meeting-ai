"""Provider-neutral storage contracts for ROOM-HOP Cloud Drive.

This module intentionally contains no identity or authorization logic. Callers
must authorize every operation before invoking a storage adapter.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Protocol


@dataclass(frozen=True)
class ObjectRef:
    key: str


@dataclass(frozen=True)
class StoredObject:
    ref: ObjectRef
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class ProviderCapabilities:
    streaming_write: bool
    streaming_read: bool
    multipart_resume: bool
    signed_urls: bool
    server_side_copy: bool


class StorageAdapter(Protocol):
    def put_stream(self, key: str, source: BinaryIO, *, max_bytes: int) -> StoredObject: ...
    def open_read(self, ref: ObjectRef) -> BinaryIO: ...
    def head(self, ref: ObjectRef) -> StoredObject: ...
    def delete(self, ref: ObjectRef) -> None: ...
    def capabilities(self) -> ProviderCapabilities: ...
