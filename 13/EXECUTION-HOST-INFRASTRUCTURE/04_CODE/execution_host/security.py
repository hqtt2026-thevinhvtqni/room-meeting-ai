from __future__ import annotations
import os, re, shutil
from pathlib import Path
from typing import Iterable

class HostError(ValueError): pass
_SECRET = re.compile(r'(?i)(token|secret|password|api[_-]?key|authorization)\s*[=:]\s*[^\s,;]+')
_ALLOWED = {'python','python3','pytest','node','npm','npx','git','bash','sh'}

def redact(value: str) -> str:
    value = _SECRET.sub(lambda m: m.group(1)+'=<REDACTED>', value)
    for key, val in os.environ.items():
        if len(val) >= 12 and key.lower() in {'openai_api_key','github_token','git_token','api_key'}:
            value = value.replace(val, '<REDACTED>')
    return value

def validate_context(ctx):
    if not ctx.work_id or not ctx.work_name or not ctx.workspace_root or not ctx.execution_workspace: raise HostError('invalid_work_context')
    if not ctx.authorized: raise HostError('execution_not_authorized')
    root = Path(ctx.workspace_root).resolve(); workspace = Path(ctx.execution_workspace).resolve(); evidence = Path(ctx.evidence_root).resolve()
    for child, parent in ((workspace, root), (evidence, root)):
        try: child.relative_to(parent)
        except ValueError: raise HostError('workspace_escape')
    if not root.exists() or not root.is_dir(): raise HostError('workspace_root_missing')
    return root, workspace, evidence

def validate_command(command: Iterable[str]) -> list[str]:
    args = list(command)
    if not args or any(not isinstance(x, str) or not x or '\x00' in x for x in args): raise HostError('invalid_command_arguments')
    exe = Path(args[0]).name
    if exe not in _ALLOWED: raise HostError('forbidden_executable')
    if any(x in args for x in ('&&','||',';','|','>','<','`')): raise HostError('command_injection_rejected')
    if any(os.path.isabs(x) for x in args[1:]): raise HostError('absolute_argument_rejected')
    return args

def validate_cwd(cwd: Path, workspace: Path) -> Path:
    resolved = cwd.resolve()
    try: resolved.relative_to(workspace.resolve())
    except ValueError: raise HostError('cwd_escape')
    return resolved

def safe_env() -> dict[str,str]:
    keep = {'PATH','HOME','LANG','LC_ALL','SYSTEMROOT','WINDIR','TMP','TEMP'}
    return {k:v for k,v in os.environ.items() if k in keep}

def executable_capabilities():
    return {name: bool(shutil.which(name)) for name in sorted(_ALLOWED)}
