"""Work 28 contract primitives.

Pure contract code only: no network, filesystem, subprocess, Core, or runtime side effects.
This module does not grant authorization and is not an execution adapter.
Server-side principal, WorkContext, filesystem containment and runtime isolation
are enforced by adapters/Core; this module only provides typed validation boundaries.

CONTRACT_VERSION 1.3.0 — Trust Boundary + Authorization surface + Resource Limits.
TrustedPrincipal and WorkContext are DATA CONTRACTS only. They do not prove that a
principal is authentic or authorized. Adapters/Core MUST derive principal from a
trusted transport source and MUST reject caller-supplied identity_id as authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
import math
import re
import secrets
import unicodedata
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Mapping

CONTRACT_VERSION = "1.3.0"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_RUN_ID_RE = re.compile(r"^run-[0-9a-f]{32}$")
_PRINCIPAL_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_WORK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_WINDOWS_RESERVED = re.compile(
    r"^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?$",
    re.IGNORECASE,
)
_PROTECTED_COMPONENTS = {
    ".git", ".env", ".env.local", ".envrc", ".ssh", ".aws", ".azure", ".gnupg", ".kube",
    ".git-credentials", ".npmrc", ".netrc", ".pypirc", "id_rsa", "credentials",
    "desktop.ini", "thumbs.db",
}

_ALLOWED_SUMMARY_SCALARS = (type(None), bool, int, float, str)

# Resource limit defaults (bytes / counts)
DEFAULT_MAX_READ_BYTES = 1_048_576       # 1 MiB
DEFAULT_MAX_WRITE_BYTES = 1_048_576      # 1 MiB
DEFAULT_MAX_LIST_ENTRIES = 1_000
DEFAULT_MAX_APPEND_BYTES = 262_144       # 256 KiB
HARD_MAX_READ_BYTES = 16_777_216         # 16 MiB
HARD_MAX_WRITE_BYTES = 16_777_216
HARD_MAX_LIST_ENTRIES = 10_000
HARD_MAX_APPEND_BYTES = 4_194_304        # 4 MiB


class ToolStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    DENIED = "DENIED"
    TIMEOUT = "TIMEOUT"
    NOT_FOUND = "NOT_FOUND"
    INVALID_REQUEST = "INVALID_REQUEST"
    CANCELLED = "CANCELLED"


class OperationKind(str, Enum):
    READ = "READ"
    MUTATION = "MUTATION"
    EXECUTION = "EXECUTION"
    DIAGNOSTIC = "DIAGNOSTIC"


class ExecutionOperation(str, Enum):
    RUN_SCRIPT = "RUN_SCRIPT"
    RUN_TESTS = "RUN_TESTS"


class SandboxOperation(str, Enum):
    """Sandbox file operations that require authorization."""
    LIST = "LIST"
    READ = "READ"
    CREATE = "CREATE"
    WRITE = "WRITE"
    APPEND = "APPEND"
    DELETE = "DELETE"


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, _ALLOWED_SUMMARY_SCALARS):
        # Reject NaN / ±Infinity (KA-AUDIT-28-07)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            raise ValueError("NaN and ±Infinity are not allowed in test_summary")
        return value
    if isinstance(value, Mapping):
        # Keys must be strings (KA-AUDIT-28-07)
        frozen_items = {}
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError(f"test_summary keys must be strings, got {type(k).__name__}")
            frozen_items[k] = _deep_freeze(v)
        return MappingProxyType(frozen_items)
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(v) for v in value)
    raise ValueError(
        f"test_summary contains non-JSON-compatible type: {type(value).__name__}"
    )


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_thaw(v) for v in value]
    return value


# ---------------------------------------------------------------------------
# Trust Boundary — DATA CONTRACTS ONLY
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TrustedPrincipal:
    """Server-derived principal identity.

    This is a DATA CONTRACT. Creating an instance does NOT prove authenticity.
    Adapters/Core MUST populate this from a trusted transport source
    (e.g. authenticated session, mTLS identity, Core-issued token).
    Caller-supplied identity_id MUST NEVER be treated as authoritative.
    """
    principal_id: str
    source: str  # e.g. "core-session", "mtls", "adapter-derived" — never "caller"

    def __post_init__(self) -> None:
        if not isinstance(self.principal_id, str) or not _PRINCIPAL_ID_RE.fullmatch(self.principal_id):
            raise ValueError("principal_id must match 1-128 ASCII letters/digits or . _ : -")
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("source must be a non-empty string")
        if self.source.strip().lower() in {"caller", "client", "user-supplied", "identity_id"}:
            raise ValueError(
                "TrustedPrincipal.source must not be caller-supplied; "
                "principal must be derived from a trusted transport boundary"
            )


@dataclass(frozen=True)
class WorkContext:
    """Authorized Work scope.

    DATA CONTRACT only. Does not prove the principal is authorized for this work.
    Core MUST resolve and bind WorkContext server-side after authenticating the principal.
    """
    work_id: str
    principal: TrustedPrincipal
    allowed_operations: tuple[str, ...]  # e.g. ("READ", "LIST") or full set

    def __post_init__(self) -> None:
        if not isinstance(self.work_id, str) or not _WORK_ID_RE.fullmatch(self.work_id):
            raise ValueError("work_id must match 1-64 ASCII letters/digits or . _ -")
        if not isinstance(self.principal, TrustedPrincipal):
            raise ValueError("principal must be a TrustedPrincipal instance")
        if not isinstance(self.allowed_operations, tuple) or not self.allowed_operations:
            raise ValueError("allowed_operations must be a non-empty tuple of operation names")
        for op in self.allowed_operations:
            if not isinstance(op, str) or not op.strip():
                raise ValueError("each allowed_operation must be a non-empty string")

    def permits(self, operation: str) -> bool:
        """Shape-level check only. Real authorization is Core/adapter responsibility."""
        return operation in self.allowed_operations


# ---------------------------------------------------------------------------
# Authorization request surface (fail-closed)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AuthorizedSandboxRequest:
    """Request shape for any Sandbox file operation.

    Fail-closed: missing principal, missing WorkContext, or operation not in
    allowed_operations raises at construction time. This is still only shape
    validation; the adapter must still enforce the principal against the real
    Core-derived context.
    """
    request_id: str
    work_context: WorkContext
    operation: SandboxOperation
    relative_path: str | None = None  # required for most ops except LIST at root
    content: str | None = None        # for CREATE/WRITE/APPEND
    max_read_bytes: int = DEFAULT_MAX_READ_BYTES
    max_list_entries: int = DEFAULT_MAX_LIST_ENTRIES
    max_write_bytes: int = DEFAULT_MAX_WRITE_BYTES
    max_append_bytes: int = DEFAULT_MAX_APPEND_BYTES

    def __post_init__(self) -> None:
        validate_request_id(self.request_id)
        if not isinstance(self.work_context, WorkContext):
            raise ValueError("work_context must be a WorkContext instance")
        if not isinstance(self.operation, SandboxOperation):
            raise ValueError("operation must be a SandboxOperation")

        # Fail-closed: operation must be permitted by the context
        if not self.work_context.permits(self.operation.value):
            raise ValueError(
                f"operation {self.operation.value} is not in allowed_operations "
                f"for work_id={self.work_context.work_id}"
            )

        # Path required for non-LIST (or LIST with sub-path)
        if self.operation != SandboxOperation.LIST and self.relative_path is None:
            raise ValueError(f"relative_path is required for {self.operation.value}")
        if self.relative_path is not None:
            object.__setattr__(self, "relative_path", validate_relative_work_path(self.relative_path))

        # Content required for write-like ops
        if self.operation in (SandboxOperation.CREATE, SandboxOperation.WRITE, SandboxOperation.APPEND):
            if self.content is None:
                raise ValueError(f"content is required for {self.operation.value}")
            if not isinstance(self.content, str):
                raise ValueError("content must be a string")

        # Resource limits
        object.__setattr__(self, "max_read_bytes", bounded_limit(
            self.max_read_bytes, default=DEFAULT_MAX_READ_BYTES, maximum=HARD_MAX_READ_BYTES))
        object.__setattr__(self, "max_list_entries", bounded_limit(
            self.max_list_entries, default=DEFAULT_MAX_LIST_ENTRIES, maximum=HARD_MAX_LIST_ENTRIES))
        object.__setattr__(self, "max_write_bytes", bounded_limit(
            self.max_write_bytes, default=DEFAULT_MAX_WRITE_BYTES, maximum=HARD_MAX_WRITE_BYTES))
        object.__setattr__(self, "max_append_bytes", bounded_limit(
            self.max_append_bytes, default=DEFAULT_MAX_APPEND_BYTES, maximum=HARD_MAX_APPEND_BYTES))

        # Enforce content size against the chosen limit
        if self.content is not None:
            content_bytes = len(self.content.encode("utf-8"))
            if self.operation == SandboxOperation.APPEND and content_bytes > self.max_append_bytes:
                raise ValueError(f"append content exceeds max_append_bytes ({self.max_append_bytes})")
            if self.operation in (SandboxOperation.CREATE, SandboxOperation.WRITE) and content_bytes > self.max_write_bytes:
                raise ValueError(f"write content exceeds max_write_bytes ({self.max_write_bytes})")


# ---------------------------------------------------------------------------
# ToolResult (unchanged behaviour from 1.2.1 + version bump)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolResult:
    request_id: str
    status: ToolStatus
    message: str
    result: Any = None
    evidence_ref: str | None = None
    operation_kind: OperationKind = OperationKind.READ
    run_id: str | None = None
    exit_code: int | None = None
    source_sha256: str | None = None
    test_summary: Mapping[str, Any] | None = None
    execution_operation: ExecutionOperation | None = None
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        validate_request_id(self.request_id)
        if not isinstance(self.status, ToolStatus):
            raise ValueError("status must be a ToolStatus")
        if not isinstance(self.operation_kind, OperationKind):
            raise ValueError("operation_kind must be an OperationKind")
        if self.execution_operation is not None and not isinstance(
            self.execution_operation, ExecutionOperation
        ):
            raise ValueError("execution_operation must be an ExecutionOperation")

        if self.execution_operation is not None and self.operation_kind != OperationKind.EXECUTION:
            raise ValueError("execution_operation is only valid when operation_kind=EXECUTION")
        if self.operation_kind == OperationKind.EXECUTION and self.execution_operation is None:
            raise ValueError("execution results must identify RUN_SCRIPT or RUN_TESTS")

        if self.operation_kind != OperationKind.EXECUTION:
            if self.run_id is not None:
                raise ValueError("run_id is only valid for EXECUTION results")
            if self.exit_code is not None:
                raise ValueError("exit_code is only valid for EXECUTION results")
            if self.source_sha256 is not None:
                raise ValueError("source_sha256 is only valid for EXECUTION results")
            if self.test_summary is not None:
                raise ValueError("test_summary is only valid for EXECUTION results")

        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("message must be non-empty")

        if self.test_summary is not None:
            if not isinstance(self.test_summary, Mapping):
                raise ValueError("test_summary must be a mapping")
            frozen = _deep_freeze(dict(self.test_summary))
            object.__setattr__(self, "test_summary", frozen)

        if self.status == ToolStatus.PASS and self.operation_kind == OperationKind.EXECUTION:
            missing: list[str] = []
            if not isinstance(self.run_id, str) or not _RUN_ID_RE.fullmatch(self.run_id):
                missing.append("run_id=run-<32hex>")
            if type(self.exit_code) is not int or self.exit_code != 0:
                missing.append("exit_code=0 (int)")
            if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
                missing.append("evidence_ref")
            if not isinstance(self.source_sha256, str) or not _SHA256_RE.fullmatch(self.source_sha256):
                missing.append("source_sha256")
            if self.test_summary is None:
                missing.append("test_summary")
            elif self.execution_operation == ExecutionOperation.RUN_TESTS:
                required_counters = ("tests_run", "failures", "errors", "skipped")
                counters: dict[str, int] = {}
                for counter in required_counters:
                    count = self.test_summary.get(counter)
                    if type(count) is not int:
                        missing.append(f"{counter}=explicit_integer")
                    else:
                        counters[counter] = count
                if "tests_run" in counters and counters["tests_run"] < 1:
                    missing.append("tests_run>=1")
                for counter in ("failures", "errors", "skipped"):
                    if counter in counters and counters[counter] != 0:
                        missing.append(f"{counter}=0")
            if missing:
                raise ValueError(
                    "execution PASS missing authoritative evidence: " + ", ".join(missing)
                )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "request_id": self.request_id,
            "status": self.status.value,
            "message": self.message,
            "result": self.result,
            "evidence_ref": self.evidence_ref,
            "operation_kind": self.operation_kind.value,
            "run_id": self.run_id,
            "exit_code": self.exit_code,
            "source_sha256": self.source_sha256,
            "contract_version": self.contract_version,
        }
        if self.execution_operation is not None:
            data["execution_operation"] = self.execution_operation.value
        if self.test_summary is not None:
            data["test_summary"] = _thaw(self.test_summary)
        else:
            data["test_summary"] = None
        return data


def new_request_id() -> str:
    return "req-" + secrets.token_hex(16)


def new_run_id() -> str:
    return "run-" + secrets.token_hex(16)


def validate_request_id(value: object) -> str:
    if not isinstance(value, str) or not _REQUEST_ID_RE.fullmatch(value):
        raise ValueError("request_id must be 1-128 ASCII letters/digits or . _ : -")
    return value


def validate_run_id(value: object) -> str:
    if not isinstance(value, str) or not _RUN_ID_RE.fullmatch(value):
        raise ValueError("run_id must match run-<32 lowercase hex>")
    return value


def validate_sha256(value: object, *, field_name: str = "sha256") -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise ValueError(f"{field_name} must be a lowercase 64-character SHA-256 hex digest")
    return value


def validate_relative_work_path(value: object) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("relative_path must be a non-empty, trimmed string")
    if len(value) > 1024:
        raise ValueError("relative_path exceeds 1024 characters")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError("relative_path must use NFC Unicode normalization")
    if unicodedata.normalize("NFKC", value) != value:
        raise ValueError("relative_path contains compatibility/confusable characters")
    for ch in value:
        cat = unicodedata.category(ch)
        if cat in {"Cc", "Cf", "Cs", "Co", "Cn", "Zl", "Zp"}:
            raise ValueError(
                "relative_path contains control, format, private-use, unassigned or line/paragraph separator"
            )
        if ch in {"\u2044", "\u2215", "\uff0f", "\uff3c", "\u1680"}:
            raise ValueError("relative_path contains a separator confusable")
        if ord(ch) == 0x7F or 0x80 <= ord(ch) <= 0x9F:
            raise ValueError("relative_path contains DEL/C1 control characters")
    if "\\" in value:
        raise ValueError("literal backslash is not allowed; use forward slash")
    if value.startswith(("/", "\\")) or PurePosixPath(value).is_absolute():
        raise ValueError("absolute paths are not allowed")
    win = PureWindowsPath(value)
    if win.is_absolute() or win.drive or win.root:
        raise ValueError("drive-qualified, rooted, or UNC paths are not allowed")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("empty, dot, or traversal path components are not allowed")
    forbidden_chars = set(':<>|"?*%$') | {chr(96)}
    for part in parts:
        if part.startswith("-"):
            raise ValueError("option-like path components are not allowed")
        if part.endswith((".", " ")):
            raise ValueError("Windows path components may not end in dot or space")
        if any(ch in forbidden_chars for ch in part):
            raise ValueError("path contains a forbidden or expansion character")
        if _WINDOWS_RESERVED.fullmatch(part):
            raise ValueError("Windows reserved device names are not allowed")
        if part.lower() in _PROTECTED_COMPONENTS:
            raise ValueError("protected metadata/secret path component is not allowed")
        if "~" in part:
            raise ValueError("short-name or home-expansion ambiguity is not allowed")
    return "/".join(parts)


def bounded_limit(value: object, *, default: int = 100, maximum: int = 1000) -> int:
    if isinstance(default, bool) or not isinstance(default, int) or default < 1 or default > maximum:
        raise ValueError("default must be an integer within the allowed limit range")
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("limit must be an integer")
    if value < 1 or value > maximum:
        raise ValueError(f"limit must be between 1 and {maximum}")
    return value


def normalize_status(value: object) -> ToolStatus:
    if not isinstance(value, str):
        return ToolStatus.INVALID_REQUEST
    try:
        return ToolStatus(value.upper())
    except ValueError:
        return ToolStatus.FAIL


def result_from_exception(request_id: str, exc: Exception) -> ToolResult:
    safe_id = validate_request_id(request_id)
    if isinstance(exc, TimeoutError):
        status = ToolStatus.TIMEOUT
    elif isinstance(exc, ValueError):
        status = ToolStatus.INVALID_REQUEST
    elif isinstance(exc, (PermissionError, FileNotFoundError)):
        status = ToolStatus.NOT_FOUND
    else:
        status = ToolStatus.FAIL
    return ToolResult(
        request_id=safe_id,
        status=status,
        message=f"Operation failed ({type(exc).__name__})",
    )
