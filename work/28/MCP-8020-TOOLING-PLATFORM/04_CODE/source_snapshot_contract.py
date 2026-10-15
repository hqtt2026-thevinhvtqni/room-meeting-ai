"""Pure source-snapshot manifest validation; no filesystem or transfer side effects."""
from __future__ import annotations
import hashlib, json, re, unicodedata
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

CONTRACT_VERSION = "0.1.1"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_HEAD = re.compile(r"^[0-9a-f]{7,64}$")
_DENIED_DIRS = {".git", ".ssh", ".aws", ".azure", ".gnupg", ".kube", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".venv", "venv", "dist", "build"}
_DENIED_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".git-credentials", ".npmrc", ".netrc", ".pypirc", "id_rsa", "id_ed25519", "known_hosts", "credentials"}
_DENIED_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".keystore", ".sqlite", ".sqlite3", ".db", ".log", ".bak", ".dump")
HARD_MAX_FILES = 20_000
HARD_MAX_FILE_BYTES = 8 * 1024 * 1024
HARD_MAX_TOTAL_BYTES = 128 * 1024 * 1024
HARD_MAX_PATH_CHARS = 512
HARD_MAX_MANIFEST_BYTES = 2 * 1024 * 1024
HARD_MAX_STATUS_ITEMS = 2_000
HARD_MAX_STATUS_ITEM_CHARS = 2_048
HARD_MAX_EXCLUDED_ITEMS = 20_000
HARD_MAX_EXCLUDED_ITEM_CHARS = 1_024
_ALLOWED_TOP_LEVEL = {"schema_version", "collector_version", "provenance_status", "created_at_utc", "repo_root", "branch", "head", "dirty", "status_short", "included_files", "excluded_paths", "file_count", "total_bytes", "archive_sha256"}

class SnapshotValidationError(ValueError):
    pass

@dataclass(frozen=True)
class SnapshotLimits:
    max_files: int = HARD_MAX_FILES
    max_file_bytes: int = HARD_MAX_FILE_BYTES
    max_total_bytes: int = HARD_MAX_TOTAL_BYTES
    max_path_chars: int = HARD_MAX_PATH_CHARS
    def __post_init__(self):
        for name, hard_max in {"max_files": HARD_MAX_FILES, "max_file_bytes": HARD_MAX_FILE_BYTES, "max_total_bytes": HARD_MAX_TOTAL_BYTES, "max_path_chars": HARD_MAX_PATH_CHARS}.items():
            value = getattr(self, name)
            if type(value) is not int or value < 1 or value > hard_max:
                raise SnapshotValidationError(f"{name} must be an integer from 1 to {hard_max}")

def _string(value: Any, field: str, max_len: int = 4096) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or len(value) > max_len:
        raise SnapshotValidationError(f"{field} must be a bounded non-empty trimmed string")
    if any(unicodedata.category(ch) in {"Cc", "Cf", "Cs", "Co", "Cn", "Zl", "Zp"} for ch in value):
        raise SnapshotValidationError(f"{field} contains control/invisible characters")
    return value

def casefold_path_key(path: str) -> str:
    """Collision key for Windows-like case-insensitive destinations."""
    return unicodedata.normalize("NFKC", unicodedata.normalize("NFC", path)).casefold()

def validate_relative_path(path: Any, *, allowlist: Iterable[str], max_chars: int = HARD_MAX_PATH_CHARS) -> str:
    if type(max_chars) is not int or not 1 <= max_chars <= HARD_MAX_PATH_CHARS:
        raise SnapshotValidationError("max_chars exceeds hard policy bounds")
    path = _string(path, "path", max_chars)
    if unicodedata.normalize("NFC", path) != path or unicodedata.normalize("NFKC", path) != path:
        raise SnapshotValidationError("path must be NFC/NFKC stable")
    if "\\" in path or path.startswith("/") or re.match(r"^[A-Za-z]:", path):
        raise SnapshotValidationError("absolute, drive-qualified, or backslash paths forbidden")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts) or any(part.endswith((".", " ")) for part in parts):
        raise SnapshotValidationError("ambiguous or traversal path component")
    forbidden = ':<>|"?*%$' + chr(96)
    if any(any(ch in part for ch in forbidden) for part in parts):
        raise SnapshotValidationError("forbidden path character")
    lower = [part.lower() for part in parts]
    if any(part in _DENIED_DIRS for part in lower) or any(part in _DENIED_NAMES or part.startswith(".env.") for part in lower) or any(part.endswith(_DENIED_SUFFIXES) for part in lower):
        raise SnapshotValidationError("denied secret/runtime path")
    if any(re.match(r"^(con|prn|aux|nul|com[1-9¹²³]|lpt[1-9¹²³])(?:\..*)?$", p, re.I) for p in parts):
        raise SnapshotValidationError("Windows reserved device name denied")
    roots = tuple(_string(root, "allowlist entry", HARD_MAX_PATH_CHARS).rstrip("/") for root in allowlist)
    if not roots or not any(path == root or path.startswith(root + "/") for root in roots):
        raise SnapshotValidationError("path outside explicit allowlist")
    return path

def _metadata(value: Any, field: str, max_items: int, max_chars: int) -> list[str]:
    if not isinstance(value, list) or len(value) > max_items:
        raise SnapshotValidationError(f"{field} exceeds metadata limit")
    for index, item in enumerate(value):
        _string(item, f"{field}[{index}]", max_chars)
    return value

def validate_manifest(manifest: Any, *, allowlist: Iterable[str], limits: SnapshotLimits = SnapshotLimits()) -> dict[str, Any]:
    if not isinstance(manifest, Mapping): raise SnapshotValidationError("manifest must be an object")
    keys = set(manifest); missing = sorted(_ALLOWED_TOP_LEVEL - keys); unknown = sorted(keys - _ALLOWED_TOP_LEVEL)
    if missing: raise SnapshotValidationError("missing fields: " + ", ".join(missing))
    if unknown: raise SnapshotValidationError("unknown fields: " + ", ".join(str(k) for k in unknown))
    if manifest["schema_version"] != CONTRACT_VERSION: raise SnapshotValidationError("unsupported schema_version")
    _string(manifest["collector_version"], "collector_version", 128)
    if manifest["provenance_status"] != "UNAUTHENTICATED_LOCAL_OBSERVATION": raise SnapshotValidationError("provenance must remain unauthenticated until external receipt verification")
    stamp = _string(manifest["created_at_utc"], "created_at_utc", 40)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", stamp): raise SnapshotValidationError("invalid UTC timestamp")
    _string(manifest["repo_root"], "repo_root", 1024); _string(manifest["branch"], "branch", 256)
    if not isinstance(manifest["head"], str) or not _HEAD.fullmatch(manifest["head"]): raise SnapshotValidationError("head must be lowercase Git SHA")
    if type(manifest["dirty"]) is not bool: raise SnapshotValidationError("dirty must be bool")
    status = _metadata(manifest["status_short"], "status_short", HARD_MAX_STATUS_ITEMS, HARD_MAX_STATUS_ITEM_CHARS)
    _metadata(manifest["excluded_paths"], "excluded_paths", HARD_MAX_EXCLUDED_ITEMS, HARD_MAX_EXCLUDED_ITEM_CHARS)
    files = manifest["included_files"]
    if not isinstance(files, list) or not 1 <= len(files) <= limits.max_files: raise SnapshotValidationError("included_files must be non-empty and bounded")
    seen, collision_keys, total = set(), set(), 0
    for index, item in enumerate(files):
        if not isinstance(item, Mapping) or set(item) != {"path", "size_bytes", "sha256"}: raise SnapshotValidationError(f"included_files[{index}] shape invalid")
        path = validate_relative_path(item["path"], allowlist=allowlist, max_chars=limits.max_path_chars)
        collision_key = casefold_path_key(path)
        if path in seen: raise SnapshotValidationError("duplicate included path")
        if collision_key in collision_keys: raise SnapshotValidationError("case-fold/NFKC path collision")
        seen.add(path); collision_keys.add(collision_key)
        size = item["size_bytes"]
        if type(size) is not int or size < 0 or size > limits.max_file_bytes: raise SnapshotValidationError("invalid file size")
        if not isinstance(item["sha256"], str) or not _SHA256.fullmatch(item["sha256"]): raise SnapshotValidationError("invalid file SHA-256")
        total += size
        if total > limits.max_total_bytes: raise SnapshotValidationError("total bytes exceed limit")
    if type(manifest["file_count"]) is not int or manifest["file_count"] != len(seen): raise SnapshotValidationError("file_count mismatch")
    if type(manifest["total_bytes"]) is not int or manifest["total_bytes"] != total: raise SnapshotValidationError("total_bytes mismatch")
    if not isinstance(manifest["archive_sha256"], str) or not _SHA256.fullmatch(manifest["archive_sha256"]): raise SnapshotValidationError("invalid archive SHA-256")
    if manifest["dirty"] is False and status: raise SnapshotValidationError("clean snapshot must have empty status")
    if manifest["dirty"] is True and not status: raise SnapshotValidationError("dirty snapshot must preserve status")
    return dict(manifest)

def canonical_manifest_bytes(manifest: Mapping[str, Any]) -> bytes:
    return (json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    if not isinstance(data, bytes): raise TypeError("data must be bytes")
    return hashlib.sha256(data).hexdigest()
