from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Iterable


class HostError(ValueError):
    pass


_SECRET = re.compile(
    r"(?i)(token|secret|password|api[_-]?key|authorization)"
    r"\s*[=:]\s*[^\s,;]+"
)

_ALLOWED = {
    "python",
    "python3",
    "pytest",
    "node",
    "npm",
    "npx",
    "git",
    "bash",
    "sh",
}


def redact(value: str) -> str:
    value = _SECRET.sub(
        lambda m: m.group(1) + "=<REDACTED>",
        value,
    )

    for key, val in os.environ.items():
        if (
            len(val) >= 12
            and key.lower()
            in {
                "openai_api_key",
                "github_token",
                "git_token",
                "api_key",
            }
        ):
            value = value.replace(val, "<REDACTED>")

    return value


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_context(ctx):
    if (
        not ctx.work_id
        or not ctx.work_name
        or not ctx.workspace_root
        or not ctx.execution_workspace
        or not ctx.evidence_root
    ):
        raise HostError("invalid_work_context")

    if not ctx.authorized:
        raise HostError("execution_not_authorized")

    root = Path(ctx.workspace_root).resolve()
    workspace = Path(ctx.execution_workspace).resolve()
    evidence = Path(ctx.evidence_root).resolve()

    if not root.exists() or not root.is_dir():
        raise HostError("workspace_root_missing")

    # Canonical execution workspace must be inside:
    # <workspace_root>/workspace
    canonical_workspace = (root / "workspace").resolve()

    if not _is_relative_to(workspace, canonical_workspace):
        raise HostError("workspace_escape")

    if not _is_relative_to(evidence, root):
        raise HostError("workspace_escape")

    if not workspace.exists() or not workspace.is_dir():
        raise HostError("execution_workspace_missing")

    return root, workspace, evidence


def validate_cwd(cwd: str | Path, workspace: str | Path) -> Path:
    cwd_path = Path(cwd).resolve()
    workspace_path = Path(workspace).resolve()

    if not workspace_path.exists() or not workspace_path.is_dir():
        raise HostError("execution_workspace_missing")

    if not _is_relative_to(cwd_path, workspace_path):
        raise HostError("cwd_escape")

    return cwd_path


def validate_command(command: Iterable[str]) -> list[str]:
    args = list(command)

    if not args:
        raise HostError("invalid_command_arguments")

    if any(
        not isinstance(x, str) or not x or "\x00" in x
        for x in args
    ):
        raise HostError("invalid_command_arguments")

    executable = Path(args[0]).stem.lower()

    if executable not in _ALLOWED:
        raise HostError("forbidden_executable")

    # Never allow absolute executable/argument paths.
    if any(Path(x).is_absolute() for x in args[1:]):
        raise HostError("absolute_argument_rejected")

    # Shell metacharacters are forbidden as standalone command tokens.
    if any(
        x in args
        for x in (
            "&&",
            "||",
            ";",
            "|",
            ">",
            "<",
            "`",
        )
    ):
        raise HostError("command_injection_rejected")

    # Python -c receives exactly one code argument.
    #
    # This still permits legitimate Python code such as:
    #   python3 -c "import time; time.sleep(2)"
    #
    # but rejects:
    #   python3 -c "print(1);" rm
    if executable in {"python", "python3"}:
        if "-c" in args:
            index = args.index("-c")

            if index != 1:
                raise HostError("invalid_python_command")

            if len(args) != 3:
                raise HostError("command_injection_rejected")

        # Python's -m form also gets a strict argument boundary.
        if "-m" in args:
            index = args.index("-m")

            if index != 1:
                raise HostError("invalid_python_command")

    # Reject shell chaining embedded in non-Python arguments.
    for arg in args[1:]:
        if any(token in arg for token in ("&&", "||", "`")):
            raise HostError("command_injection_rejected")

    return args


def safe_env() -> dict[str, str]:
    keep = {
        "PATH",
        "HOME",
        "LANG",
        "LC_ALL",
        "SYSTEMROOT",
        "WINDIR",
        "TMP",
        "TEMP",
    }

    return {
        key: value
        for key, value in os.environ.items()
        if key in keep
    }


def executable_capabilities():
    return {
        name: bool(shutil.which(name))
        for name in sorted(_ALLOWED)
    }