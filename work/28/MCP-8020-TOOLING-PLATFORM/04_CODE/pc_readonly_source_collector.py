#!/usr/bin/env python3
"""Read-only allowlisted source collector draft; never run under current policy."""
from __future__ import annotations
import argparse, hashlib, json, os, stat, subprocess, sys, zipfile
from pathlib import Path
from datetime import datetime, timezone
from source_snapshot_contract import HARD_MAX_EXCLUDED_ITEM_CHARS, HARD_MAX_EXCLUDED_ITEMS, HARD_MAX_MANIFEST_BYTES, HARD_MAX_STATUS_ITEM_CHARS, HARD_MAX_STATUS_ITEMS
COLLECTOR_VERSION = "pc-readonly-collector/0.4.0"
SCHEMA_VERSION = "0.1.1"; PROVENANCE_STATUS = "UNAUTHENTICATED_LOCAL_OBSERVATION"
MAX_FILES = 20000; MAX_FILE_BYTES = 8 * 1024 * 1024; MAX_TOTAL_BYTES = 128 * 1024 * 1024; MAX_GIT_OUTPUT = 256 * 1024
ALLOWED_ROOTS = ("room_hop_mcp", "core", "integration", "tests")
ALLOWED_ROOT_FILES = {"pyproject.toml", "setup.cfg", "tox.ini", "pytest.ini", "requirements.txt", "requirements-dev.txt", "requirements-test.txt"}
ALLOWED_SUFFIXES = {".py", ".toml", ".txt", ".ini", ".yaml", ".yml", ".ps1"}
DENIED_DIRS = {".git", ".ssh", ".aws", ".azure", ".gnupg", ".kube", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".venv", "venv", "dist", "build", "coverage", "htmlcov"}
DENIED_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".git-credentials", ".npmrc", ".netrc", ".pypirc", "id_rsa", "id_ed25519", "known_hosts", "credentials", "secrets.json"}
DENIED_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".keystore", ".sqlite", ".sqlite3", ".db", ".log", ".bak", ".dump")
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
def fail(message: str) -> "NoReturn": print(f"ERROR: {message}", file=sys.stderr) or (_ for _ in ()).throw(SystemExit(2))
def git(repo: Path, *args: str) -> str:
    env = {"PATH": os.environ.get("PATH", ""), "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    if os.name == "nt" and os.environ.get("SystemRoot"): env["SystemRoot"] = os.environ["SystemRoot"]
    try: proc = subprocess.run(["git", "-C", str(repo), "--no-optional-locks", "-c", "core.fsmonitor=false", *args], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=False, timeout=15, cwd=str(repo), env=env)
    except (OSError, subprocess.SubprocessError) as exc: fail(f"Git query failed ({type(exc).__name__})")
    if len(proc.stdout) > MAX_GIT_OUTPUT or len(proc.stderr) > MAX_GIT_OUTPUT: fail("Git output exceeds bounded limit")
    return proc.stdout.strip()
def is_reparse_or_symlink(path: Path) -> bool:
    try: info = path.lstat()
    except OSError: return True
    return path.is_symlink() or bool(getattr(info, "st_file_attributes", 0) & REPARSE_POINT)
def assert_safe_components(repo: Path, rel: str) -> None:
    current = repo
    for component in Path(rel).parts:
        current = current / component
        if is_reparse_or_symlink(current): fail(f"link/reparse component detected: {rel}")
def is_denied_rel(rel: str) -> bool:
    parts = [part.lower() for part in rel.split("/")]
    return any(part in DENIED_DIRS for part in parts) or any(part in DENIED_NAMES or part.startswith(".env.") for part in parts) or any(part.endswith(DENIED_SUFFIXES) for part in parts)
def append_excluded(excluded: list[str], value: str) -> None:
    if len(value) > HARD_MAX_EXCLUDED_ITEM_CHARS: fail("excluded-path item exceeds contract limit during enumeration")
    if len(excluded) >= HARD_MAX_EXCLUDED_ITEMS: fail("excluded-path count exceeds contract limit during enumeration")
    excluded.append(value)
def selected_path(rel: str) -> bool:
    if is_denied_rel(rel): return False
    path = Path(rel)
    return rel in ALLOWED_ROOT_FILES if len(path.parts) == 1 else path.parts[0] in ALLOWED_ROOTS and path.suffix.lower() in ALLOWED_SUFFIXES
def enumerate_files(repo: Path) -> tuple[list[tuple[str, Path]], list[str]]:
    selected, excluded = [], []
    for root, dirs, files in os.walk(repo, topdown=True, followlinks=False):
        current = Path(root); kept = []
        for dirname in sorted(dirs):
            item = current / dirname; rel = item.relative_to(repo).as_posix()
            if is_reparse_or_symlink(item) or is_denied_rel(rel): append_excluded(excluded, rel + "/")
            elif rel.split("/")[0] in ALLOWED_ROOTS: kept.append(dirname)
            else: append_excluded(excluded, rel + "/")
        dirs[:] = kept
        for filename in sorted(files):
            item = current / filename; rel = item.relative_to(repo).as_posix()
            if not selected_path(rel) or is_reparse_or_symlink(item) or not item.is_file(): append_excluded(excluded, rel + " [link-or-nonfile]")
            else: selected.append((rel, item))
    return sorted(selected), sorted(excluded)
def parse_status(status_text: str) -> list[str]:
    result = []
    for item in status_text.splitlines():
        if len(item) > HARD_MAX_STATUS_ITEM_CHARS: fail("Git status item exceeds contract limit")
        if len(result) >= HARD_MAX_STATUS_ITEMS: fail("Git status count exceeds contract limit")
        result.append(item)
    return result
def safe_read(repo: Path, rel: str, path: Path) -> bytes:
    if not path.resolve(strict=True).is_relative_to(repo): fail(f"path escaped repository root: {rel}")
    assert_safe_components(repo, rel); before_path = path.lstat()
    try: fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc: fail(f"safe open failed ({type(exc).__name__}): {rel}")
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode): fail(f"not a regular file: {rel}")
        if before.st_ino and before_path.st_ino and (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (before_path.st_dev, before_path.st_ino, before_path.st_size, before_path.st_mtime_ns): fail(f"file identity changed before read: {rel}")
        chunks, remaining = [], MAX_FILE_BYTES + 1
        while remaining:
            chunk = os.read(fd, min(1024 * 1024, remaining))
            if not chunk: break
            chunks.append(chunk); remaining -= len(chunk)
        data = b"".join(chunks); after = os.fstat(fd)
        if len(data) > MAX_FILE_BYTES or len(data) != after.st_size: fail(f"file size limit or short read: {rel}")
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns): fail(f"file changed while reading: {rel}")
        if not path.resolve(strict=True).is_relative_to(repo): fail(f"path escaped repository root after read: {rel}")
        return data
    finally: os.close(fd)
def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024): digest.update(chunk)
    return digest.hexdigest()
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--repo", required=True); parser.add_argument("--out-dir", required=True); args = parser.parse_args()
    repo = Path(args.repo).resolve(strict=True); out_dir = Path(args.out_dir).expanduser().resolve()
    if not repo.is_dir() or not (repo / ".git").exists(): fail("repo must be a Git working tree root")
    if out_dir == repo or repo in out_dir.parents or out_dir in repo.parents: fail("output directory must be outside repository")
    if out_dir.exists(): fail("output directory must not pre-exist; collector owns only a newly-created directory")
    if is_reparse_or_symlink(repo): fail("repository root may not be a symlink/reparse point")
    if git(repo, "rev-parse", "--show-toplevel") != str(repo): fail("Git root does not match --repo")
    branch = git(repo, "branch", "--show-current") or "(detached HEAD)"; head = git(repo, "rev-parse", "HEAD"); status_short = parse_status(git(repo, "status", "--short", "--untracked-files=all"))
    files, excluded = enumerate_files(repo)
    if not files or len(files) > MAX_FILES: fail("selected file set is empty or exceeds maximum")
    payloads, total = [], 0
    for rel, path in files:
        data = safe_read(repo, rel, path); total += len(data)
        if total > MAX_TOTAL_BYTES: fail("selected source bytes exceed total maximum")
        payloads.append((rel, data, hashlib.sha256(data).hexdigest()))
    owned = False; archive_path = out_dir / "room-hop-source-snapshot.zip"; manifest_path = out_dir / "room-hop-source-snapshot.manifest.json"
    try:
        out_dir.mkdir(parents=True, exist_ok=False); owned = True
        with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for rel, data, _digest in payloads:
                info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.create_system = 3; info.external_attr = (0o100644 & 0xFFFF) << 16; zf.writestr(info, data)
        archive_hash = hash_file(archive_path)
        manifest = {"schema_version": SCHEMA_VERSION, "collector_version": COLLECTOR_VERSION, "provenance_status": PROVENANCE_STATUS, "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "repo_root": str(repo), "branch": branch, "head": head, "dirty": bool(status_short), "status_short": status_short, "included_files": [{"path": rel, "size_bytes": len(data), "sha256": digest} for rel, data, digest in payloads], "excluded_paths": excluded, "file_count": len(payloads), "total_bytes": total, "archive_sha256": archive_hash}
        manifest_bytes = (json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
        if len(manifest_bytes) > HARD_MAX_MANIFEST_BYTES: fail("manifest exceeds shared hard byte limit")
        with manifest_path.open("xb") as stream: stream.write(manifest_bytes)
    except BaseException as exc:
        if owned:
            for candidate in (archive_path, manifest_path):
                try: candidate.unlink(missing_ok=True)
                except OSError: pass
            try: out_dir.rmdir()
            except OSError: pass
        if isinstance(exc, SystemExit): raise
        fail(f"snapshot creation failed ({type(exc).__name__}); owned partial outputs removed")
    print(json.dumps({"status": "COLLECTED_READ_ONLY_UNAUTHENTICATED", "repo_root": str(repo), "branch": branch, "head": head, "dirty": bool(status_short), "file_count": len(payloads), "total_bytes": total, "archive": str(archive_path), "archive_sha256": archive_hash, "manifest": str(manifest_path), "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(), "provenance_status": PROVENANCE_STATUS}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
