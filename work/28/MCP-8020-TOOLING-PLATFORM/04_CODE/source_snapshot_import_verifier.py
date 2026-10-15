"""In-memory source snapshot verification; never extracts or imports files."""
from __future__ import annotations
import hashlib, io, json, re, stat, zipfile
from datetime import datetime
from typing import Any, Iterable, Mapping
from source_snapshot_contract import HARD_MAX_FILE_BYTES, HARD_MAX_MANIFEST_BYTES, HARD_MAX_TOTAL_BYTES, SnapshotLimits, SnapshotValidationError, canonical_manifest_bytes, casefold_path_key, validate_manifest, validate_relative_path
VERIFIER_VERSION = "source-snapshot-verifier/0.3.0"
MAX_ARCHIVE_BYTES = 160 * 1024 * 1024; MAX_COMPRESSION_RATIO = 200
DOS_DIRECTORY = 0x10; DOS_DEVICE = 0x40; DOS_VOLUME = 0x08; DOS_REPARSE = 0x400
_RECEIPT_FIELDS = {"receipt_version", "source_identity", "approved_channel", "archive_sha256", "manifest_sha256", "destination_work_id", "transferred_at_utc", "nonce", "issuer", "issuer_signature", "verifier_result"}
_SHA256 = re.compile(r"^[0-9a-f]{64}$"); _NONCE = re.compile(r"^[A-Za-z0-9._:-]{16,128}$")
class ImportVerificationError(ValueError): pass
def _text(value: Any, field: str, max_len: int = 1024) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or len(value) > max_len or any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value): raise ImportVerificationError(f"{field} must be a bounded safe string")
    return value
def validate_transfer_receipt(receipt: Any, *, destination_work_id: str) -> dict[str, Any]:
    if not isinstance(receipt, Mapping) or set(receipt) != _RECEIPT_FIELDS: raise ImportVerificationError("receipt fields are incomplete or unknown")
    if receipt["receipt_version"] != "0.1.0": raise ImportVerificationError("unsupported receipt version")
    for field in ("source_identity", "approved_channel", "destination_work_id", "issuer", "issuer_signature", "verifier_result"): _text(receipt[field], field)
    if receipt["destination_work_id"] != destination_work_id: raise ImportVerificationError("receipt destination Work mismatch")
    for field in ("archive_sha256", "manifest_sha256"):
        if not isinstance(receipt[field], str) or not _SHA256.fullmatch(receipt[field]): raise ImportVerificationError(f"invalid {field}")
    if not isinstance(receipt["nonce"], str) or not _NONCE.fullmatch(receipt["nonce"]): raise ImportVerificationError("invalid receipt nonce")
    stamp = _text(receipt["transferred_at_utc"], "transferred_at_utc", 40)
    try: datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc: raise ImportVerificationError("invalid transfer timestamp") from exc
    if receipt["verifier_result"] != "TRUSTED_RECEIPT_PENDING_EXTERNAL_AUTH": raise ImportVerificationError("receipt must remain pending external authentication")
    return dict(receipt)
def _sha256_stream(stream: Any, *, limit: int) -> tuple[str, int]:
    digest = hashlib.sha256(); total = 0
    while True:
        chunk = stream.read(1024 * 1024)
        if not chunk: break
        total += len(chunk)
        if total > limit: raise ImportVerificationError("stream exceeds configured limit")
        digest.update(chunk)
    return digest.hexdigest(), total
def validate_zip_member_type(info: zipfile.ZipInfo) -> None:
    """Accept only Unix regular files or DOS normal files with safe attrs.

    Unix creator (3): mode must be present and regular; symlink/FIFO/device/socket
    and all other special modes are rejected. DOS creator (0): Unix mode must be
    zero/absent and DOS directory/device/volume/reparse bits are rejected; normal,
    readonly, hidden, system and archive bits are permitted. Other creators or
    mixed DOS/Unix metadata are rejected as ambiguous.
    """
    creator = info.create_system; mode = (info.external_attr >> 16) & 0xFFFF; dos_attr = info.external_attr & 0xFFFF
    if creator not in (0, 3): raise ImportVerificationError("unsupported ZIP creator platform")
    if dos_attr & (DOS_DIRECTORY | DOS_DEVICE | DOS_VOLUME | DOS_REPARSE): raise ImportVerificationError("ZIP DOS member has directory/device/volume/reparse attribute")
    if creator == 0:
        if mode != 0: raise ImportVerificationError("ambiguous DOS member with Unix mode")
    else:
        if mode == 0 or stat.S_IFMT(mode) != stat.S_IFREG or stat.S_ISLNK(mode): raise ImportVerificationError("ZIP Unix member is not a regular non-link file")
def verify_archive_in_memory(archive_bytes: bytes, manifest_bytes: bytes, *, allowlist: Iterable[str], destination_work_id: str, receipt: Mapping[str, Any] | None = None, limits: SnapshotLimits = SnapshotLimits()) -> dict[str, Any]:
    if not isinstance(archive_bytes, bytes) or not isinstance(manifest_bytes, bytes): raise ImportVerificationError("archive and manifest must be bytes")
    if not 1 <= len(archive_bytes) <= MAX_ARCHIVE_BYTES: raise ImportVerificationError("archive size outside hard bounds")
    if not 1 <= len(manifest_bytes) <= HARD_MAX_MANIFEST_BYTES: raise ImportVerificationError("manifest exceeds hard byte limit")
    archive_hash = hashlib.sha256(archive_bytes).hexdigest(); manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    if receipt is not None:
        checked_receipt = validate_transfer_receipt(receipt, destination_work_id=destination_work_id)
        if checked_receipt["archive_sha256"] != archive_hash or checked_receipt["manifest_sha256"] != manifest_hash: raise ImportVerificationError("receipt hash mismatch")
    try: manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise ImportVerificationError("manifest is not canonical UTF-8 JSON") from exc
    if canonical_manifest_bytes(manifest) != manifest_bytes: raise ImportVerificationError("manifest bytes are not canonical")
    try: checked = validate_manifest(manifest, allowlist=allowlist, limits=limits)
    except SnapshotValidationError as exc: raise ImportVerificationError(str(exc)) from exc
    if checked["archive_sha256"] != archive_hash: raise ImportVerificationError("manifest archive hash mismatch")
    expected = {item["path"]: item for item in checked["included_files"]}; expected_keys = {casefold_path_key(path) for path in expected}
    if len(expected_keys) != len(expected): raise ImportVerificationError("manifest contains case-fold path collision")
    seen, seen_keys, total = set(), set(), 0
    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes), "r") as archive:
            infos = archive.infolist()
            if len(infos) != len(expected): raise ImportVerificationError("archive entry count mismatch")
            for info in infos:
                if info.filename in seen: raise ImportVerificationError("duplicate archive entry")
                seen.add(info.filename); collision_key = casefold_path_key(info.filename)
                if collision_key in seen_keys: raise ImportVerificationError("case-fold archive path collision")
                seen_keys.add(collision_key)
                if info.is_dir() or info.filename.endswith("/"): raise ImportVerificationError("directory entries are forbidden")
                if info.flag_bits & 0x1: raise ImportVerificationError("encrypted ZIP entries are forbidden")
                if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED): raise ImportVerificationError("unsupported ZIP compression")
                validate_zip_member_type(info); validate_relative_path(info.filename, allowlist=allowlist, max_chars=limits.max_path_chars)
                if info.filename not in expected: raise ImportVerificationError("unexpected archive path")
                if info.file_size > HARD_MAX_FILE_BYTES or info.file_size > limits.max_file_bytes: raise ImportVerificationError("archive member exceeds file limit")
                if info.compress_size == 0 and info.file_size: raise ImportVerificationError("invalid compressed size")
                if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO: raise ImportVerificationError("compression ratio exceeds limit")
                with archive.open(info, "r") as stream: digest, size = _sha256_stream(stream, limit=limits.max_file_bytes)
                claim = expected[info.filename]
                if size != claim["size_bytes"] or digest != claim["sha256"]: raise ImportVerificationError(f"archive member hash/size mismatch: {info.filename}")
                total += size
                if total > HARD_MAX_TOTAL_BYTES or total > limits.max_total_bytes: raise ImportVerificationError("archive total exceeds limit")
    except zipfile.BadZipFile as exc: raise ImportVerificationError("invalid or truncated ZIP archive") from exc
    if seen != set(expected) or seen_keys != expected_keys: raise ImportVerificationError("archive path set mismatch")
    return {"status": "VERIFIED_IN_MEMORY_NOT_IMPORTED", "verifier_version": VERIFIER_VERSION, "archive_sha256": archive_hash, "manifest_sha256": manifest_hash, "destination_work_id": destination_work_id, "file_count": len(seen), "total_bytes": total, "receipt_authentication": "NOT_PERFORMED_BY_PURE_VERIFIER", "imported": False}
