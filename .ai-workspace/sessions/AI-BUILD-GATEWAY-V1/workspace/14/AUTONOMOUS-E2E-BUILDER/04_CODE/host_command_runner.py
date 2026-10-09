"""W14 in-host capability runner.

Executed BY the W13 canonical execution host (POST /execute) with cwd = the bound
execution workspace:

    python host_command_runner.py host_request.json

It is not a provider. Browser work is delegated to the canonical Work 09.1
WorkflowEngine + Adapter (imported, never re-implemented); git work uses the git CLI
inside the bound repository only. The LAST stdout line is exactly one JSON object
(ASCII-only, so Windows pipe encodings cannot corrupt it).

Request: {"kind": "browser"|"git", ...}; the caller passes every path explicitly
(capabilities.*), nothing is discovered from the ambient process.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

INNER_MARK = "W14_RUNNER_INNER"
_SECRET = re.compile(r"(?i)(token|secret|password|api[_-]?key|authorization)\s*[=:]\s*[^\s,;]+")
GIT_IDENTITY = ["-c", "user.name=ROOM-HOP W14", "-c", "user.email=w14@room-hop.local"]


def emit(result: dict) -> None:
    sys.stdout.write("\n" + json.dumps(result, ensure_ascii=True) + "\n")
    sys.stdout.flush()


def redact(text: str) -> str:
    return _SECRET.sub(lambda m: m.group(1) + "=<REDACTED>", text or "")


# ------------------------------------------------------------------ browser (W09.1)
def run_browser(req: dict) -> dict:
    caps = req.get("capabilities", {})
    code_dir = Path(caps.get("w09_1_code", ""))
    if not (code_dir / "workflow_engine.py").is_file() or not (code_dir / "adapter.py").is_file():
        return {"status": "BLOCKED", "reason": "w09_1_code_missing:" + str(code_dir)}
    sys.path.insert(0, str(code_dir))
    try:
        import adapter as w09  # canonical Work 09.1 Adapter (Playwright owner)
        from workflow_engine import WorkflowEngine
    except ImportError as exc:
        venv_py = caps.get("w09_python")
        if venv_py and Path(venv_py).is_file() and not os.environ.get(INNER_MARK):
            # Same canonical W09 dependency set: run this runner under the W09 venv python.
            env = dict(os.environ, **{INNER_MARK: "1"})
            p = subprocess.run([venv_py, str(Path(__file__).resolve()), sys.argv[1]],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            lines = [x for x in p.stdout.splitlines() if x.strip()]
            if lines:
                try:
                    return json.loads(lines[-1])
                except ValueError:
                    pass
            return {"status": "BLOCKED", "reason": "w09_venv_runner_failed", "stderr": redact(p.stderr)[-1500:]}
        return {"status": "BLOCKED", "reason": "w09_dependency_missing:" + str(exc)}

    evidence_dir = Path(caps.get("evidence_dir") or "evidence/w09_1")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = WorkflowEngine(w09.adapter, evidence_dir).execute(req["workflow"])
    finally:
        try:
            w09.adapter.close()
        except Exception:
            pass

    logs, artifacts = [], []
    for step in result.get("steps", []):
        logs.append({"event": "browser_" + str(step.get("op")), "status": step.get("status"),
                     "attempts": step.get("attempts"), "duration_ms": step.get("duration_ms"),
                     "error": step.get("error")})
        out = step.get("result")
        if step.get("status") == "PASS" and isinstance(out, dict) and out.get("path"):
            src = Path(out["path"])
            if src.is_file():  # W09.1 writes shots into its own tree; keep a copy with the W14 evidence
                dst = evidence_dir / src.name
                shutil.copy2(src, dst)
                artifacts.append(str(dst))
    return {"status": result["status"], "provider": "work09.1-browser-agent", "w09_1_execution_id": result["execution_id"],
            "start_url": result["start_url"], "final_url": result["final_url"], "page_title": result["page_title"],
            "steps": result["steps"], "logs": logs, "artifacts": artifacts,
            "evidence_json": result.get("evidence_json"), "failure_screenshot": result.get("failure_screenshot")}


# ------------------------------------------------------------------ git (bound repository only)
def git(repo: Path, *args: str) -> dict:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    p = subprocess.run(["git", *GIT_IDENTITY, *args], cwd=str(repo), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return {"exit_code": p.returncode, "stdout": redact(p.stdout), "stderr": redact(p.stderr)}


SHELL_NOISE = ("desktop.ini",)  # Google Drive / Explorer metadata that appears inside synced work folders; never part of an artifact


def ignore_shell_noise(repo: Path) -> None:
    """Keep shell metadata out of this repository: local-only exclude (not tracked) + untrack anything already committed."""
    exclude = repo / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    text = exclude.read_text(encoding="utf-8", errors="replace") if exclude.exists() else ""
    have = set(text.splitlines())
    missing = [n for n in SHELL_NOISE if n not in have]
    if missing:
        with exclude.open("a", encoding="utf-8", newline="\n") as f:
            f.write(("" if not text or text.endswith("\n") else "\n") + "\n".join(missing) + "\n")


def head_of(repo: Path):
    r = git(repo, "rev-parse", "HEAD")
    return r["stdout"].strip() if r["exit_code"] == 0 else None


def run_git(req: dict) -> dict:
    repo = Path(req.get("repo", "")).resolve()
    try:
        repo.relative_to(Path.cwd().resolve())
    except ValueError:
        return {"status": "BLOCKED", "reason": "repository_escape"}
    action = req.get("action")
    branch = req.get("branch") or "main"
    if action == "init":
        repo.mkdir(parents=True, exist_ok=True)
        created = not (repo / ".git").exists()
        if created:
            r = git(repo, "init", "-b", branch)
            if r["exit_code"] != 0:  # git < 2.28
                r = git(repo, "init")
                git(repo, "symbolic-ref", "HEAD", "refs/heads/" + branch)
            if r["exit_code"] != 0:
                return {"status": "BLOCKED", "reason": "git_init_failed", "stderr": r["stderr"]}
        ignore_shell_noise(repo)
        return {"status": "PASS", "action": action, "initialized": created, "head": head_of(repo)}
    if not (repo / ".git").exists():
        return {"status": "BLOCKED", "reason": "not_a_git_repository"}
    if action == "commit":
        ignore_shell_noise(repo)
        for noise in SHELL_NOISE:
            git(repo, "rm", "--cached", "-q", "--ignore-unmatch", "--", noise)
        add = git(repo, "add", "-A")
        if add["exit_code"] != 0:
            return {"status": "FAIL", "reason": "git_add_failed", "stderr": add["stderr"]}
        c = git(repo, "commit", "--allow-empty", "-m", str(req.get("message") or "w14 commit"))
        head = head_of(repo)
        return {"status": "PASS" if c["exit_code"] == 0 and head else "FAIL", "action": action, "head": head,
                "stdout": c["stdout"][-1500:], "stderr": c["stderr"][-1500:]}
    if action == "validate":
        cur = git(repo, "branch", "--show-current")["stdout"].strip()
        head = head_of(repo)
        if cur != branch:
            return {"status": "BLOCKED", "reason": "wrong_branch", "actual": cur}
        if not req.get("expected_head") or head != req["expected_head"]:
            return {"status": "BLOCKED", "reason": "unexpected_head", "actual": head}
        return {"status": "PASS", "action": action, "branch": cur, "head": head}
    if action == "diff":
        d = git(repo, "show", "--no-color", "--patch", "HEAD")
        blob = git(repo, "show", "HEAD:" + str(req.get("path") or "artifact.txt"))  # committed content, even when the patch is empty
        return {"status": "PASS" if d["exit_code"] == 0 else "FAIL", "action": action, "head": head_of(repo), "diff": d["stdout"],
                "head_blob": blob["stdout"] if blob["exit_code"] == 0 else None}
    return {"status": "BLOCKED", "reason": "unsupported_git_action:" + str(action)}


def main() -> int:
    try:
        req = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        kind = req.get("kind")
        if kind == "browser":
            result = run_browser(req)
        elif kind == "git":
            result = run_git(req)
        else:
            result = {"status": "BLOCKED", "reason": "unsupported_kind:" + str(kind)}
    except Exception as exc:  # always return one JSON result so W13 evidence shows the real cause
        result = {"status": "FAIL", "reason": type(exc).__name__ + ":" + str(exc)}
    result["request_id"] = req.get("request_id") if isinstance(locals().get("req"), dict) else None
    emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
