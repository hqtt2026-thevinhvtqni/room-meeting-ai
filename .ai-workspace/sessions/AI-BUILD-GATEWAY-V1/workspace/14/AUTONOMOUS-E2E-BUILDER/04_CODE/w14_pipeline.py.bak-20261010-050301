#!/usr/bin/env python
"""W14 AUTONOMOUS E2E BUILDER - pipeline orchestrator.

DISCOVER -> BUILD -> START -> E2E -> VERIFY -> (REPAIR LOOP) -> PACKAGE -> RELEASE VERIFY -> FINAL

Architecture is fixed and not re-decided here:
    W14 UI -> W14 ExecutionHostBridge -> W13 PC Execution Host :8031 -> W12 contract -> real execution
No provider, no mock, no sandbox runtime, no /browser_execute, no /git_*.

Rules this file enforces
  * Evidence first: every stage writes <evidence>/<run_id>/NN_<stage>[_aK].json; nothing is PASS without a check.
  * Fail closed: any unexplained failure is BLOCKED with a diagnosis bundle, never a softer status.
  * Repair loop = allowlisted, deterministic environment/runtime repairs only (REPAIRS below).
    A failure that needs a SOURCE change is BLOCKED with `needs=source_patch`; this tool never edits source to get a PASS.
  * Release (push + Work 99 lock) happens only with --release and only after stage 8 PASS.
Exit code: 0 = DONE_*, 2 = BLOCKED.
"""
from __future__ import annotations

import argparse, dataclasses, hashlib, importlib.util, json, os, py_compile, re, shutil, socket, subprocess, sys, tempfile, time, traceback, zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent                   # .../14/AUTONOMOUS-E2E-BUILDER/04_CODE
W14 = HERE.parent
WORKSPACE = HERE.parents[2]                               # .../AI-BUILD-GATEWAY-V1/workspace
W12_CODE = WORKSPACE / "12" / "WORK-EXECUTION-ENVIRONMENT" / "04_CODE"
W12_CONTRACT = WORKSPACE / "12" / "WORK-EXECUTION-ENVIRONMENT" / "03_ARCHITECTURE" / "INFRASTRUCTURE_HANDOFF_CONTRACT.md"
W13_CODE = WORKSPACE / "13" / "EXECUTION-HOST-INFRASTRUCTURE" / "04_CODE"
W09_1_CODE = WORKSPACE / "091" / "ROOM-HOP-BROWSER-WORKFLOW-ENGINE" / "04_CODE"
WORK_INDEX = WORKSPACE / "99" / "WORK_INDEX.md"
HOST_PORT, UI_PORT = 8031, 8766                           # UI port is fixed by the canonical E2E script
HOST_URL, UI_URL = f"http://127.0.0.1:{HOST_PORT}", f"http://127.0.0.1:{UI_PORT}/"
E2E_OUT = Path(tempfile.gettempdir()) / "work14-browser-ui-e2e"
EXEC_PATH_FILES = ["execution_host_bridge.py", "browser_ui_app.py", "command_workflow_interpreter.py", "host_command_runner.py", "run_browser_ui_full_e2e.py"]
FORBIDDEN = ["/home/ubuntu", "/browser_execute", "/git_", "python3'", 'python3"']
RELEASE_EXCLUDE = {".browser_ui_runtime", "__pycache__", ".venv", "desktop.ini"}
SECRET_RE = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|(?i:bearer\s+[A-Za-z0-9._-]{20,}))")
IS_WIN = os.name == "nt"


def iso() -> str: return datetime.now(timezone.utc).isoformat()
def sha_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha_file(p: Path) -> str: return sha_bytes(Path(p).read_bytes())


class Blocker(Exception):
    def __init__(self, code: str, detail: str = "", **data):
        super().__init__(f"{code}: {detail}"); self.code, self.detail, self.data = code, detail, data


class StageFailed(Exception):
    def __init__(self, rec: dict): super().__init__(rec.get("code")); self.rec = rec


# ------------------------------------------------------------------ platform helpers (no third-party deps)
def http(method: str, url: str, body: dict | None = None, timeout: float = 15):
    req = Request(url, method=method, data=None if body is None else json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=timeout) as r:
            raw = r.read(); status = r.status
    except HTTPError as e:
        raw = e.read(); status = e.code
    except (URLError, OSError) as e:
        return 0, {"error": type(e).__name__ + ":" + str(e)}
    try: return status, json.loads(raw)
    except ValueError: return status, {"raw": raw.decode("utf-8", "replace")[:500]}


def port_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1): return True
    except OSError: return False


def _linux_listener(port: int):
    """No external tools: /proc/net/tcp{,6} (LISTEN=0A) -> socket inode -> owning pid via /proc/<pid>/fd."""
    hexport = f"{port:04X}"
    for fn in ("/proc/net/tcp", "/proc/net/tcp6"):
        try: rows = Path(fn).read_text().splitlines()[1:]
        except OSError: continue
        for ln in rows:
            f = ln.split()
            if f[3] != "0A" or f[1].rsplit(":", 1)[1] != hexport: continue
            ah, inode = f[1].rsplit(":", 1)[0], f[9]
            addr = {"0100007F": "127.0.0.1", "00000000": "0.0.0.0", "00000000000000000000000001000000": "::1"}.get(ah, ah)
            for pd in Path("/proc").iterdir():
                if not pd.name.isdigit(): continue
                try:
                    if any(os.readlink(fd) == f"socket:[{inode}]" for fd in (pd / "fd").iterdir()): return addr, int(pd.name)
                except OSError: continue
    return None


def listener(port: int):
    """(local_address, pid) of the LISTEN socket on `port`, or None."""
    try:
        if IS_WIN:
            out = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True).stdout
            for ln in out.splitlines():
                p = ln.split()
                if len(p) >= 5 and p[0] == "TCP" and p[3] == "LISTENING" and p[1].rsplit(":", 1)[-1] == str(port):
                    return p[1].rsplit(":", 1)[0].strip("[]"), int(p[4])
        else:
            return _linux_listener(port)
    except OSError: pass
    return None


def proc_name(pid: int) -> str:
    try:
        if IS_WIN:
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout
            return out.split(",")[0].strip('"').lower() if out.strip().startswith('"') else ""
        return Path(f"/proc/{pid}/comm").read_text().strip().lower()
    except OSError: return ""


def pid_alive(pid: int) -> bool:
    return bool(proc_name(pid))


def kill_tree(pid: int):
    if IS_WIN: subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
    else:
        try: os.kill(pid, 15)
        except OSError: pass


def source_build_hash() -> str:
    spec = importlib.util.spec_from_file_location("w13_identity_src", W13_CODE / "execution_host" / "identity.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.canonical_build_hash()


def tail(path: Path, n: int = 1500) -> str:
    try: return Path(path).read_text(encoding="utf-8", errors="replace")[-n:]
    except OSError: return ""


# ------------------------------------------------------------------ repair registry (environment/runtime only)
def repair_install_chromium(p: "Pipeline", f: dict) -> dict:
    r = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], capture_output=True, text=True, timeout=900)
    return {"action": "playwright install chromium", "exit_code": r.returncode, "tail": (r.stdout + r.stderr)[-600:]}


def repair_restart_host(p: "Pipeline", f: dict) -> dict:
    return {"action": "restart owned W13 host + W14 UI on next cycle (state is stopped now)"}


def repair_replace_stale(p: "Pipeline", f: dict) -> dict:
    if not p.args.replace_stale:
        raise Blocker("stale_process_needs_operator", "re-run with --replace-stale to let the pipeline stop the stale python process", **f.get("data", {}))
    pid = f.get("pid"); name = proc_name(pid) if pid else ""
    if not re.match(r"^pythonw?(\.exe)?$|^python3", name): raise Blocker("refuse_to_kill_non_python", f"pid={pid} name={name!r}")
    kill_tree(pid); time.sleep(1)
    return {"action": "stopped stale python process", "pid": pid, "name": name}


REPAIRS = {"chromium_missing": repair_install_chromium, "host_unreachable": repair_restart_host, "host_died": repair_restart_host,
           "stale_host": repair_replace_stale, "ui_port_busy": repair_replace_stale}


def diagnose_e2e(out: str, err: str, host_log: Path) -> tuple[str, str, dict]:
    t = out + "\n" + err
    rules = [(r"Executable doesn't exist|playwright install", "chromium_missing", "Playwright browser binary not installed"),
             (r"Connection refused|W13 /health not PASS|urlopen error.*8031", "host_unreachable", "W13 host not answering"),
             (r"W13 runtime identity incomplete", "w13_health_contract_mismatch", "W13 /health identity shape != E2E expectation (source patch)"),
             (r"w13_http_4\d\d|unexpected keyword argument|execution_workspace_outside_work_sandbox|forbidden_executable", "w13_contract_mismatch", "W13/W12 rejected the W14 request (source patch)"),
             (r"w13_stdout_missing_child_result|w09_dependency_missing|w09_1_code_missing", "runner_failure", "in-host runner failed (see stderr_tail)")]
    for pat, code, why in rules:
        if re.search(pat, t): return code, why, {"host_log_tail": tail(host_log, 800)}
    return "e2e_failed", "unclassified E2E failure", {"host_log_tail": tail(host_log, 800)}


# ------------------------------------------------------------------ pipeline
class Pipeline:
    def __init__(self, args):
        self.args = args
        self.run_id = args.run_id or "W14-PIPELINE-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.ev = W14 / "06_EVIDENCE" / self.run_id; self.ev.mkdir(parents=True, exist_ok=True)
        self.n = 0; self.attempt = 0
        self.timeline: list[dict] = []; self.repairs: list[dict] = []
        self.host: dict = {}; self.ui: dict = {}; self.e2e: dict = {}; self.final: dict = {}; self.pkg: dict = {}
        self.owned: dict[str, dict] = {}  # name -> {"proc": Popen, "pid": int}

    # ---- stage runner
    def stage(self, name: str, fn):
        self.n += 1; t0 = time.time()
        try: data = fn() or {}; status = "PASS"
        except Blocker as b: data = {"code": b.code, "detail": b.detail, **b.data}; status = "BLOCKED"
        except Exception as e: data = {"code": "unhandled_" + type(e).__name__, "detail": str(e), "trace": traceback.format_exc()[-1800:]}; status = "BLOCKED"
        rec = {"stage": name, "attempt": self.attempt, "status": status, "seconds": round(time.time() - t0, 2), "at": iso(), **data}
        (self.ev / f"{self.n:02d}_{name.lower()}_a{self.attempt}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
        self.timeline.append({k: rec[k] for k in ("stage", "attempt", "status", "seconds") + (("code",) if "code" in rec else ())})
        print(f"[{name:<14}] {status}" + (f"  {rec.get('code')}: {rec.get('detail', '')}" if status != "PASS" else ""), flush=True)
        if status != "PASS": raise StageFailed(rec)
        return data

    # ---- 1. DISCOVER
    def s_discover(self):
        need = {"w12_authority": W12_CODE / "wee" / "authority.py", "w12_contract": W12_CONTRACT, "w13_server": W13_CODE / "execution_host" / "server.py",
                "w13_identity": W13_CODE / "execution_host" / "identity.py", "w09_1_engine": W09_1_CODE / "workflow_engine.py", "w09_1_adapter": W09_1_CODE / "adapter.py",
                "work_index": WORK_INDEX, **{f"w14_{f}": HERE / f for f in EXEC_PATH_FILES}}
        missing = [k for k, p in need.items() if not p.is_file()]
        if missing: raise Blocker("source_boundary_incomplete", "required source missing", missing=missing)
        required = re.findall(r"'(\w+)'", re.search(r"REQUIRED\s*=\s*\(([^)]*)\)", (W12_CODE / "wee" / "authority.py").read_text(encoding="utf-8-sig")).group(1))
        spec = importlib.util.spec_from_file_location("w13_models_src", W13_CODE / "execution_host" / "models.py")
        m = importlib.util.module_from_spec(spec); sys.modules["w13_models_src"] = m; spec.loader.exec_module(m)
        fields = {f.name for f in dataclasses.fields(m.WorkContext)}
        lacking = [k for k in required if k not in fields]
        if lacking: raise Blocker("w13_workcontext_lacks_w12_required_fields", "W13 cannot accept the canonical W12 WorkContext (source patch)", fields=lacking, needs="source_patch")
        legacy = []
        for f in EXEC_PATH_FILES:
            txt = (HERE / f).read_text(encoding="utf-8-sig")
            legacy += [f"{f}: {pat}" for pat in FORBIDDEN if pat in txt]
        if legacy: raise Blocker("legacy_runtime_assumption", "forbidden legacy pattern on the execution path", findings=legacy, needs="source_patch")
        return {"w12_required_fields": required, "w13_source_build_hash": source_build_hash(), "w12_authority_sha256": sha_file(W12_CODE / "wee" / "authority.py"),
                "w12_contract_sha256": sha_file(W12_CONTRACT), "execution_path": "W14 UI -> bridge -> W13 :8031 /execute -> W12 -> real execution",
                "legacy_scan": "clean", "files_checked": len(need)}

    # ---- 2. BUILD
    def s_build(self):
        tmp = Path(tempfile.mkdtemp(prefix="w14build_")); compiled = 0
        try:
            for root in (HERE, W13_CODE / "execution_host", W12_CODE / "wee", W09_1_CODE):
                for p in root.rglob("*.py"):
                    if RELEASE_EXCLUDE & set(p.parts): continue
                    try: py_compile.compile(str(p), cfile=str(tmp / f"{compiled}.pyc"), doraise=True); compiled += 1
                    except py_compile.PyCompileError as e: raise Blocker("compile_failed", str(e)[:300], file=str(p), needs="source_patch")
        finally: shutil.rmtree(tmp, ignore_errors=True)
        r = subprocess.run([sys.executable, "-c", "import playwright, fastapi, pydantic, requests"], capture_output=True, text=True)
        if r.returncode: raise Blocker("python_dependencies_missing", r.stderr.strip()[-300:], python=sys.executable)
        g = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if g.returncode: raise Blocker("git_missing", g.stderr.strip())
        snippet = ("from playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n b=p.chromium.launch(headless=True%s)\n pg=b.new_page(); pg.set_content('<h1>ok</h1>')\n"
                   " print(pg.locator('h1').inner_text(), b.version); b.close()\n") % ("" if IS_WIN else ",args=['--no-sandbox']")
        c = subprocess.run([sys.executable, "-c", snippet], capture_output=True, text=True, timeout=120)
        if c.returncode:
            code = "chromium_missing" if re.search(r"Executable doesn't exist|playwright install", c.stderr) else "chromium_launch_failed"
            raise Blocker(code, c.stderr.strip()[-400:])
        (HERE / ".browser_ui_runtime").mkdir(exist_ok=True)
        return {"py_files_compiled": compiled, "python": sys.executable, "git": g.stdout.strip(), "chromium": c.stdout.strip()}

    # ---- 3. START
    def _spawn(self, name: str, argv: list[str], cwd: Path, env: dict, port: int):
        log = self.ev / f"{name}.log"
        proc = subprocess.Popen(argv, cwd=str(cwd), env=env, stdout=open(log, "ab"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        deadline = time.time() + 30
        while time.time() < deadline:
            if proc.poll() is not None: raise Blocker(f"{name}_start_failed", f"exited code={proc.returncode}", log_tail=tail(log))
            if port_open(port): break
            time.sleep(0.3)
        else:
            proc.terminate(); raise Blocker(f"{name}_start_failed", f"did not bind :{port} in 30s", log_tail=tail(log))
        lp = listener(port)
        self.owned[name] = {"proc": proc, "pid": lp[1] if lp else proc.pid, "popen_pid": proc.pid}
        return log

    def s_start(self):
        src_hash = source_build_hash()
        st, h = http("GET", HOST_URL + "/health")
        if st == 200:
            ident = h.get("runtime_identity") or {}
            if ident.get("build_hash") != src_hash:
                lp = listener(HOST_PORT)
                raise Blocker("stale_host", "a W13 host is running whose build_hash != source on disk (restart needed)", pid=lp[1] if lp else None,
                              data={"running": ident.get("build_hash"), "source": src_hash})
            adopted = True
        else:
            if port_open(HOST_PORT):
                lp = listener(HOST_PORT); raise Blocker("stale_host", "port 8031 is occupied by a non-W13 process", pid=lp[1] if lp else None)
            env = dict(os.environ, PYTHONUNBUFFERED="1", PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
            self._spawn("w13_host", [sys.executable, "-m", "execution_host.server"], W13_CODE, env, HOST_PORT)
            st, h = http("GET", HOST_URL + "/health"); adopted = False
            if st != 200: raise Blocker("host_unreachable", f"health {st}: {h}")
        ident = h["runtime_identity"]
        need = ["instance_id", "build_hash", "started_at", "pid", "platform", "bind_address"]
        if h.get("status") != "PASS" or [k for k in need if not ident.get(k)]: raise Blocker("host_identity_incomplete", json.dumps(h)[:300])
        self.host = {"instance_id": ident["instance_id"], "build_hash": ident["build_hash"], "pid": ident["pid"], "adopted": adopted, "platform": ident["platform"]}
        # W14 UI (the canonical E2E reuses an already-bound :8766)
        if port_open(UI_PORT):
            lp = listener(UI_PORT); raise Blocker("ui_port_busy", f"{UI_URL} already bound by pid={lp[1] if lp else '?'} (stale W14 UI)", pid=lp[1] if lp else None)
        self._spawn("w14_ui", [sys.executable, str(HERE / "browser_ui_app.py")], HERE, dict(os.environ, PORT=str(UI_PORT), PYTHONUNBUFFERED="1"), UI_PORT)
        s, _ = http("GET", UI_URL)
        if s != 200: raise Blocker("ui_unhealthy", f"GET {UI_URL} -> {s}")
        self.ui = {"pid": self.owned["w14_ui"]["pid"]}
        return {"host": self.host, "ui": self.ui, "browser": "Playwright Chromium verified in BUILD; launched per-run by the W09.1 adapter inside the W13 host"}

    # ---- 4. E2E
    def s_e2e(self):
        self.key = f"{self.run_id}-a{self.attempt}"
        shutil.rmtree(E2E_OUT, ignore_errors=True)
        env = dict(os.environ, W13_EXECUTION_HOST_URL=HOST_URL, W14_E2E_URL=UI_URL, W14_E2E_KEY=self.key, PYTHONUNBUFFERED="1")
        try: p = subprocess.run([sys.executable, str(HERE / "run_browser_ui_full_e2e.py")], cwd=str(HERE), env=env, capture_output=True, text=True, timeout=self.args.e2e_timeout)
        except subprocess.TimeoutExpired as e: raise Blocker("e2e_timeout", f"no result in {self.args.e2e_timeout}s (W12 host does not enforce timeouts)", out=(e.stdout or b"")[-500:] if isinstance(e.stdout, bytes) else (e.stdout or "")[-500:])
        (self.ev / f"e2e_a{self.attempt}.out.txt").write_text(p.stdout, encoding="utf-8"); (self.ev / f"e2e_a{self.attempt}.err.txt").write_text(p.stderr, encoding="utf-8")
        for name in ("w13_host", "w14_ui"):
            o = self.owned.get(name)
            if o and o["proc"].poll() is not None: raise Blocker("host_died" if name == "w13_host" else "ui_died", f"{name} exited during E2E code={o['proc'].returncode}")
        if p.returncode:
            code, why, extra = diagnose_e2e(p.stdout, p.stderr, self.ev / "w13_host.log")
            raise Blocker(code, why, exit_code=p.returncode, stderr_tail=p.stderr[-1500:], stdout_tail=p.stdout[-800:], **extra, needs="source_patch" if code not in REPAIRS else "repair")
        res_file = E2E_OUT / "UI_E2E_RESULT.json"
        if not res_file.is_file(): raise Blocker("e2e_result_missing", str(res_file))
        res = json.loads(res_file.read_text(encoding="utf-8"))
        shutil.copytree(E2E_OUT, self.ev / f"e2e_output_a{self.attempt}", dirs_exist_ok=True)
        if res.get("status") != "PASS" or res.get("idempotency_key") != self.key: raise Blocker("e2e_result_not_pass", json.dumps({k: res.get(k) for k in ("status", "idempotency_key")}))
        self.e2e = res
        return {"exit_code": 0, "idempotency_key": self.key, "replay": res.get("replay"), "responsive": res.get("responsive"), "result_sha256": sha_file(res_file)}

    # ---- 5. VERIFY
    def _probe_ctx(self, tag: str, **over):
        root = self.ev / "security_probe" / tag; (root / "evidence").mkdir(parents=True, exist_ok=True)
        ctx = {"work_id": "14", "work_name": "w14-security-probe", "workspace_root": str(root), "execution_workspace": str(root), "repository": "probe",
               "repository_root": str(root), "branch": "main", "evidence_root": str(root / "evidence"), "authorized": True}
        ctx.update(over); return ctx

    def _blocked(self, ctx, command) -> tuple[bool, str]:
        st, body = http("POST", HOST_URL + "/execute", {"work_context": ctx, "execution_request": {"command": command, "timeout_seconds": 30}}, timeout=30)
        not_pass = st != 200 or body.get("status") != "PASS"
        return not_pass, f"http={st} status={body.get('status')} reason={body.get('blocker') or body.get('reason')}"

    def s_verify(self):
        checks: dict[str, object] = {}
        def chk(name, ok, detail=""): checks[name] = {"ok": bool(ok), "detail": str(detail)[:300]}
        # runtime health + identity
        st, h = http("GET", HOST_URL + "/health"); ident = (h.get("runtime_identity") or {}) if st == 200 else {}
        chk("runtime_health", st == 200 and h.get("status") == "PASS" and h.get("runtime_provider") == "REAL", f"http={st}")
        chk("identity_stable_since_start", ident.get("instance_id") == self.host["instance_id"] and ident.get("build_hash") == self.host["build_hash"], ident.get("instance_id"))
        chk("identity_matches_source_on_disk", ident.get("build_hash") == source_build_hash(), ident.get("build_hash"))
        # process lifecycle
        lp = listener(HOST_PORT)
        chk("listener_pid_equals_health_pid", lp and lp[1] == ident.get("pid"), f"listener={lp} health_pid={ident.get('pid')}")
        chk("listener_loopback_only", lp and lp[0] in ("127.0.0.1", "::1"), lp)
        chk("host_process_is_python", lp and re.match(r"^pythonw?(\.exe)?$|^python3", proc_name(lp[1])), proc_name(lp[1]) if lp else "")
        chk("host_process_alive", lp and pid_alive(lp[1]))
        # evidence produced by this run (matched by idempotency key)
        finals = [json.loads(p.read_text(encoding="utf-8")) for p in (HERE / ".browser_ui_runtime" / "host_evidence").glob("*/FINAL_RESULT.json")]
        fin = next((f for f in finals if f.get("idempotency_key") == self.key), None)
        chk("final_result_for_this_run", fin, f"key={self.key}")
        fin = fin or {"browser": {}, "git": {}, "artifact": {}, "final_evidence_verification": {}}
        fev = fin.get("final_evidence_verification", {})
        chk("w14_final_evidence_verification", fev.get("status") == "PASS" and all(c for c in fev.get("checks", {}).values()), f"{sum(bool(c) for c in fev.get('checks', {}).values())}/{len(fev.get('checks', {}))}")
        chk("identity_correlated_in_evidence", fev.get("w13_instance_id") == ident.get("instance_id"), fev.get("w13_instance_id"))
        # browser evidence
        b = fin["browser"]; steps = b.get("steps", [])
        chk("browser_steps_pass", steps and all(s.get("status") == "PASS" for s in steps) and {"inspect", "type", "extract", "screenshot"} <= {s.get("op") for s in steps}, [s.get("op") for s in steps])
        shots = [Path(a) for a in b.get("artifacts", [])]
        chk("browser_screenshot_is_png", shots and all(s.is_file() and s.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" and s.stat().st_size > 1000 for s in shots), [str(s) for s in shots])
        chk("browser_workflow_evidence_file", b.get("evidence_json") and Path(b["evidence_json"]).is_file(), b.get("evidence_json"))
        # artifact + git
        art = Path(fin["artifact"].get("path", "")); payload = fin["artifact"].get("payload", "")
        chk("artifact_on_disk_sha", art.is_file() and sha_bytes(art.read_text(encoding="utf-8").rstrip().encode() + b"\n") == fin["artifact"].get("sha256"), str(art))
        repo = art.parent; head = fin.get("git", {}).get("commit", {}).get("head")
        def git(*a): return subprocess.run(["git", "-c", "safe.directory=*", *a], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if repo.is_dir() and (repo / ".git").exists():
            chk("git_head_is_recorded_commit", head and git("rev-parse", "HEAD").stdout.strip() == head, head)
            chk("git_branch_main", git("branch", "--show-current").stdout.strip() == "main")
            chk("git_tree_clean", git("status", "--porcelain").stdout.strip() == "", git("status", "--porcelain").stdout[:100])
            chk("git_object_is_commit", git("cat-file", "-t", "HEAD").stdout.strip() == "commit")
            chk("git_committed_blob_equals_artifact", git("show", "HEAD:artifact.txt").stdout.replace("\r\n", "\n").rstrip() == payload.rstrip())
            chk("git_fsck", git("fsck", "--no-progress").returncode == 0)
        else: chk("git_repository_present", False, str(repo))
        # security boundary (live probes against the real host)
        for ep in ("/browser_execute", "/git_commit", "/git_init"):
            s, _ = http("POST", HOST_URL + ep, {}); chk(f"legacy_endpoint_absent{ep}", s in (404, 405), f"http={s}")
        ok, d = self._blocked(self._probe_ctx("unauth", authorized=False), ["python", "--version"]); chk("rejects_unauthorized_context", ok, d)
        ok, d = self._blocked(self._probe_ctx("exe"), ["whoami"]); chk("rejects_non_allowlisted_executable", ok, d)
        ok, d = self._blocked(self._probe_ctx("inj"), ["python", "-c", "print(1)", "&&", "whoami"]); chk("rejects_command_injection_tokens", ok, d)
        ok, d = self._blocked(self._probe_ctx("abs"), ["python", str(Path(tempfile.gettempdir()) / "x.py")]); chk("rejects_absolute_path_argument", ok, d)
        pr = self._probe_ctx("wsesc"); ok, d = self._blocked({**pr, "execution_workspace": str(Path(pr["workspace_root"]).parent)}, ["python", "--version"]); chk("rejects_workspace_escape", ok, d)
        pr = self._probe_ctx("evesc"); ok, d = self._blocked({**pr, "evidence_root": str(Path(tempfile.gettempdir()) / "w14_outside_evidence")}, ["python", "--version"]); chk("rejects_evidence_root_escape", ok, d)
        sys.path.insert(0, str(HERE)); import execution_host_bridge as bridge_mod
        br = bridge_mod.ExecutionHostBridge(HOST_URL); pr = self._probe_ctx("repoesc"); outside = Path(tempfile.mkdtemp(prefix="w14_outside_repo_"))
        res = br._execute(pr, {"kind": "git", "action": "init", "repo": str(outside)}); chk("runner_rejects_repository_escape", res.get("status") == "BLOCKED" and res.get("reason") == "repository_escape", f"{res.get('status')} {res.get('reason')}")
        chk("runner_did_not_touch_outside_repo", not (outside / ".git").exists()); shutil.rmtree(outside, ignore_errors=True)
        leaks = [str(p) for p in self.ev.rglob("*") if p.is_file() and p.stat().st_size < 5_000_000 and SECRET_RE.search(p.read_text(encoding="utf-8", errors="ignore"))]
        chk("no_secrets_in_evidence", not leaks, leaks[:3])
        failed = [k for k, v in checks.items() if not v["ok"]]
        data = {"checks": checks, "passed": len(checks) - len(failed), "total": len(checks), "failed": failed}
        self.final = fin
        if failed:
            code = ("w13_command_allowlist_not_enforced" if "rejects_non_allowlisted_executable" in failed
                    else "host_died" if "runtime_health" in failed else "verify_failed")
            raise Blocker(code, f"{len(failed)} verification check(s) failed: {failed}", **data, needs="repair" if code == "host_died" else "source_patch_or_operator")
        return data

    # ---- 7. PACKAGE
    def s_package(self):
        rel = W14 / "07_RELEASE" / self.run_id; rel.mkdir(parents=True, exist_ok=True)
        files = sorted(p for p in HERE.rglob("*") if p.is_file() and not (RELEASE_EXCLUDE & set(p.relative_to(HERE).parts)) and p.suffix != ".pyc")
        entries = [{"path": p.relative_to(HERE).as_posix(), "sha256": sha_file(p), "bytes": p.stat().st_size} for p in files]
        verify_json = next(self.ev.glob("*_verify_a%d.json" % self.attempt)); e2e_json = E2E_OUT / "UI_E2E_RESULT.json"
        manifest = {"work_id": "14", "run_id": self.run_id, "created_at": iso(), "files": entries,
                    "dependencies": {"w13_build_hash": source_build_hash(), "w12_authority_sha256": sha_file(W12_CODE / "wee" / "authority.py"), "w12_contract_sha256": sha_file(W12_CONTRACT),
                                     "w09_1": {p.name: sha_file(p) for p in (W09_1_CODE / "adapter.py", W09_1_CODE / "workflow_engine.py")}},
                    "runtime": {"w13_instance_id": self.host["instance_id"], "w13_pid": self.host["pid"], "platform": self.host["platform"]},
                    "evidence": {"e2e_result_sha256": sha_file(self.ev / f"e2e_output_a{self.attempt}" / "UI_E2E_RESULT.json"), "verify_sha256": sha_file(verify_json),
                                 "final_result_sha256": sha_bytes(json.dumps(self.final, sort_keys=True).encode())},
                    "tests": {"py_compile": "PASS", "e2e": "PASS", "verify": "PASS", "e2e_idempotency_key": self.key}}
        mf = rel / "ARTIFACT_MANIFEST.json"; mf.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        zp = rel / f"W14_RELEASE_{self.run_id}.zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for p in files: z.write(p, "04_CODE/" + p.relative_to(HERE).as_posix())
            z.write(mf, "ARTIFACT_MANIFEST.json")
        self.pkg = {"manifest": str(mf), "zip": str(zp), "zip_sha256": sha_file(zp), "manifest_sha256": sha_file(mf), "files": len(entries), "release_dir": str(rel)}
        return self.pkg

    # ---- 8. RELEASE VERIFY
    def s_release_verify(self):
        mf = json.loads(Path(self.pkg["manifest"]).read_text(encoding="utf-8")); problems = []
        tmp = Path(tempfile.mkdtemp(prefix="w14rel_"))
        try:
            with zipfile.ZipFile(self.pkg["zip"]) as z: z.extractall(tmp)
            for e in mf["files"]:
                x, d = tmp / "04_CODE" / e["path"], HERE / e["path"]
                if not x.is_file() or sha_file(x) != e["sha256"]: problems.append("zip_mismatch:" + e["path"])
                if not d.is_file() or sha_file(d) != e["sha256"]: problems.append("source_changed_since_package:" + e["path"])
            for py in (tmp / "04_CODE").rglob("*.py"):
                try: py_compile.compile(str(py), cfile=str(tmp / "x.pyc"), doraise=True)
                except py_compile.PyCompileError as ex: problems.append("release_compile_failed:" + py.name + str(ex)[:80])
        finally: shutil.rmtree(tmp, ignore_errors=True)
        st, h = http("GET", HOST_URL + "/health"); ident = h.get("runtime_identity", {}) if st == 200 else {}
        if ident.get("instance_id") != mf["runtime"]["w13_instance_id"]: problems.append("runtime_instance_changed")
        if not (ident.get("build_hash") == mf["dependencies"]["w13_build_hash"] == source_build_hash()): problems.append("runtime_source_hash_mismatch")
        for label, rel in (("e2e_result", self.ev / f"e2e_output_a{self.attempt}" / "UI_E2E_RESULT.json"), ("verify", next(self.ev.glob("*_verify_a%d.json" % self.attempt)))):
            if sha_file(rel) != mf["evidence"][label + "_sha256"]: problems.append("evidence_changed:" + label)
        if sha_file(Path(self.pkg["zip"])) != self.pkg["zip_sha256"]: problems.append("zip_changed")
        reg = self._registry_row()
        if problems: raise Blocker("release_verify_failed", "; ".join(problems[:6]), problems=problems)
        return {"files_verified": len(mf["files"]), "zip_sha256": self.pkg["zip_sha256"], "runtime_instance": ident.get("instance_id"), "registry_row_14": reg or "ABSENT (will be registered at lock time)"}

    # ---- registry / release helpers
    def _registry_row(self):
        for ln in WORK_INDEX.read_text(encoding="utf-8-sig").splitlines():
            if re.match(r"^\|\s*14\s*\|", ln): return ln.strip()
        return None

    def _stop_owned(self) -> dict:
        report = {}
        for name, o in list(self.owned.items()):
            pid = o["pid"]; kill_tree(pid)
            try: o["proc"].wait(timeout=10)
            except Exception: o["proc"].kill()
            port = HOST_PORT if name == "w13_host" else UI_PORT; t = time.time()
            while time.time() - t < 8 and (port_open(port) or pid_alive(pid)): time.sleep(0.3)
            report[name] = {"pid": pid, "port_released": not port_open(port), "process_gone": not pid_alive(pid)}
            self.owned.pop(name)
        return report

    def _git(self, repo: Path, *a, env=None, check=True):
        r = subprocess.run(["git", "-c", "safe.directory=*", *a], cwd=str(repo), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        if check and r.returncode: raise Blocker("git_failed", f"git {' '.join(a[:2])}: {(r.stderr or r.stdout).strip()[-300:]}")
        return r.stdout.strip()

    def _publish(self, repo: Path, paths: list[str], parent: str, ref: str, message: str) -> str:
        """Commit exactly `paths` on top of `parent` via a private index: working tree, index and branch are never touched."""
        idx = self.ev / f"release_{int(time.time()*1000)}.index"
        env = dict(os.environ, GIT_INDEX_FILE=str(idx), GIT_AUTHOR_NAME="ROOM-HOP W14 Builder", GIT_AUTHOR_EMAIL="w14@room-hop.local",
                   GIT_COMMITTER_NAME="ROOM-HOP W14 Builder", GIT_COMMITTER_EMAIL="w14@room-hop.local")
        try:
            self._git(repo, "read-tree", parent, env=env)
            for i in range(0, len(paths), 200): self._git(repo, "add", "-f", "--", *paths[i:i + 200], env=env)
            tree = self._git(repo, "write-tree", env=env)
            commit = self._git(repo, "commit-tree", tree, "-p", parent, "-m", message, env=env)
        finally: idx.unlink(missing_ok=True)
        self._git(repo, "update-ref", ref, commit)
        out = subprocess.run(["git", "-c", "safe.directory=*", "push", "origin", f"{ref}:{ref}"], cwd=str(repo), capture_output=True, text=True)
        if out.returncode: raise Blocker("push_failed", out.stderr.strip()[-300:], ref=ref, commit=commit)
        remote = self._git(repo, "ls-remote", "origin", ref).split()
        if not remote or remote[0] != commit: raise Blocker("push_unverified", f"remote ref != {commit}", remote=remote)
        return commit

    # ---- 9. FINAL
    def s_final(self):
        lifecycle = self._stop_owned()
        (self.ev / "LIFECYCLE.json").write_text(json.dumps({"owned_processes_closed": lifecycle, "adopted_host_left_running": self.host.get("adopted")}, indent=2), encoding="utf-8")
        if any(not (v["port_released"] and v["process_gone"]) for v in lifecycle.values()): raise Blocker("process_not_terminated", json.dumps(lifecycle))
        if not self.args.release:
            return {"outcome": "DONE_RELEASE_READY", "lifecycle": lifecycle, "release": "not requested (--release). Package + verify PASS; nothing pushed, registry untouched.",
                    "to_release": "re-run with --release (or push the zip/manifest yourself)"}
        repo = Path(self._git(HERE, "rev-parse", "--show-toplevel"))
        head = self._git(repo, "rev-parse", "HEAD"); ref = "refs/heads/release/work14-" + re.sub(r"[^a-z0-9-]", "-", self.run_id.lower())
        rel = lambda p: Path(p).resolve().relative_to(repo.resolve()).as_posix()
        mf = json.loads(Path(self.pkg["manifest"]).read_text(encoding="utf-8"))
        paths = [rel(HERE / e["path"]) for e in mf["files"]] + [rel(self.pkg["manifest"]), rel(self.pkg["zip"])]
        paths += [rel(p) for p in self.ev.rglob("*") if p.is_file() and not p.name.endswith(".index") and "security_probe" not in p.parts and p.stat().st_size < 5_000_000]
        c1 = self._publish(repo, sorted(set(paths)), head, ref, f"W14 release {self.run_id}: autonomous E2E PASS (manifest {self.pkg['manifest_sha256'][:12]})")
        # Work 99 registry: COMPLETED + LOCKED only after the release commit is verified on the remote
        original = WORK_INDEX.read_bytes(); text = original.decode("utf-8"); nl = "\r\n" if "\r\n" in text else "\n"
        row = "| 14 | AUTONOMOUS-E2E-BUILDER | 14 - AUTONOMOUS-E2E-BUILDER | COMPLETED | LOCKED | W14 Browser + Autonomous Execution UI via W13 canonical host; release " + c1[:12] + " |"
        lines = text.split(nl)
        if any(re.match(r"^\|\s*14\s*\|", l) for l in lines): lines = [row if re.match(r"^\|\s*14\s*\|", l) else l for l in lines]
        else:
            i = next((k for k, l in enumerate(lines) if re.match(r"^\|\s*13\s*\|", l)), None)
            if i is None: raise Blocker("WORK_REGISTRY_DRIFT", "cannot locate row 13 to register Work 14")
            lines.insert(i + 1, row)
        WORK_INDEX.write_bytes(nl.join(lines).encode("utf-8"))
        lock = {"work_id": "14", "state": "COMPLETED+LOCKED", "locked_at": iso(), "release_commit": c1, "release_ref": ref, "manifest_sha256": self.pkg["manifest_sha256"], "zip_sha256": self.pkg["zip_sha256"]}
        lockf = self.ev / "LOCK.json"; lockf.write_text(json.dumps(lock, indent=2), encoding="utf-8")
        try: c2 = self._publish(repo, [rel(WORK_INDEX), rel(lockf)], c1, ref, f"Work 99: register Work 14 COMPLETED+LOCKED ({c1[:12]})")
        except Blocker as b:
            WORK_INDEX.write_bytes(original)  # never leave a local LOCKED that was not published
            raise Blocker("registry_lock_unpublished", f"release {c1} is pushed but the registry lock was not: {b.code}", release_commit=c1)
        return {"outcome": "DONE_RELEASED_LOCKED", "release_ref": ref, "release_commit": c1, "registry_commit": c2, "lifecycle": lifecycle, "registered_row_14": row}

    # ---- orchestration with repair loop
    def run(self) -> int:
        final_status, blocker, release = "BLOCKED", None, {}
        try:
            self.attempt = 0
            self.stage("DISCOVER", self.s_discover)
            while True:
                self.attempt += 1
                try:
                    self.stage("BUILD", self.s_build); self.stage("START", self.s_start); self.stage("E2E", self.s_e2e); self.stage("VERIFY", self.s_verify)
                    break
                except StageFailed as sf:
                    rec = sf.rec; code = rec.get("code"); fix = REPAIRS.get(code)
                    if not fix or self.attempt > self.args.max_repair_cycles:
                        raise
                    cyc = {"cycle": self.attempt, "failed_stage": rec["stage"], "diagnosis": {"code": code, "detail": rec.get("detail")}, "repair": code, "at": iso()}
                    cyc["stopped_for_restart"] = self._stop_owned()
                    try: cyc["result"] = fix(self, {"pid": rec.get("pid"), "data": rec.get("data", {})})
                    except Blocker as b:
                        cyc["result"] = {"blocked": b.code, "detail": b.detail}; self.repairs.append(cyc)
                        (self.ev / f"repair_cycle_{self.attempt}.json").write_text(json.dumps(cyc, indent=2, default=str), encoding="utf-8"); raise StageFailed({**rec, "code": b.code, "detail": b.detail})
                    self.repairs.append(cyc); (self.ev / f"repair_cycle_{self.attempt}.json").write_text(json.dumps(cyc, indent=2, default=str), encoding="utf-8")
                    print(f"[REPAIR #{self.attempt}   ] {code} -> {cyc['result'].get('action')}; restarting stages BUILD..VERIFY", flush=True)
            self.stage("PACKAGE", self.s_package); self.stage("RELEASE_VERIFY", self.s_release_verify)
            release = self.stage("FINAL", self.s_final); final_status = release["outcome"]
        except StageFailed as sf:
            blocker = {"run_id": self.run_id, "stage": sf.rec["stage"], "code": sf.rec.get("code"), "detail": sf.rec.get("detail"), "needs": sf.rec.get("needs", "operator_or_source_patch"),
                       "attempt": sf.rec.get("attempt"), "diagnosis": {k: v for k, v in sf.rec.items() if k in ("stderr_tail", "stdout_tail", "host_log_tail", "log_tail", "failed", "findings", "missing", "fields", "problems")},
                       "evidence_dir": str(self.ev), "at": iso(), "registry": "Work 14 NOT locked (BLOCKED never locks)"}
        finally:
            try: self._stop_owned()
            except Exception: pass
        result = {"run_id": self.run_id, "status": final_status, "timeline": self.timeline, "repair_cycles": self.repairs, "release": release, "package": self.pkg or None,
                  "w13_identity": self.host or None, "finished_at": iso(), "evidence_dir": str(self.ev)}
        if blocker:
            result["blocker"] = blocker; (self.ev / "BLOCKER.json").write_text(json.dumps(blocker, indent=2, default=str), encoding="utf-8")
            (W14 / "06_EVIDENCE" / "LATEST_BLOCKER.json").write_text(json.dumps(blocker, indent=2, default=str), encoding="utf-8")
        (self.ev / "PIPELINE_RESULT.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
        print(f"\n=== W14 PIPELINE {final_status} ===\nEVIDENCE={self.ev}" + (f"\nBLOCKER={blocker['code']} @ {blocker['stage']}: {blocker['detail']}" if blocker else ""), flush=True)
        return 0 if final_status.startswith("DONE") else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="W14 autonomous E2E builder pipeline")
    ap.add_argument("--release", action="store_true", help="after stage 8 PASS: push release ref to origin and mark Work 14 COMPLETED+LOCKED in Work 99")
    ap.add_argument("--replace-stale", action="store_true", help="allow stopping a stale python W13 host / W14 UI that blocks the ports")
    ap.add_argument("--max-repair-cycles", type=int, default=2)
    ap.add_argument("--e2e-timeout", type=int, default=420)
    ap.add_argument("--run-id", default=None)
    return Pipeline(ap.parse_args(argv)).run()


if __name__ == "__main__":
    sys.exit(main())
