"""Provider-neutral object references used by Cloud Drive recovery validation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ObjectRef:
    key: str

@dataclass(frozen=True)
class StoredObject:
    ref: ObjectRef
    size_bytes: int
    sha256: str
