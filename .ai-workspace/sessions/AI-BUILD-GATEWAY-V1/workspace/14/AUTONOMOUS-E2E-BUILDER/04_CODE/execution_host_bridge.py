from __future__ import annotations
import json, os, shutil, uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
RUNNER = HERE / 'host_command_runner.py'  # W14 in-host capability script, shipped next to this bridge
WORKSPACE = HERE.parents[2]               # .../AI-BUILD-GATEWAY-V1/workspace (explicit, from this file's own location)
W09_1_CODE = Path(os.getenv('W09_1_CODE_DIR') or WORKSPACE / '091' / 'ROOM-HOP-BROWSER-WORKFLOW-ENGINE' / '04_CODE')
W09_PYTHON = Path(os.getenv('W09_PYTHON') or WORKSPACE / '09' / 'ROOM-HOP-BROWSER-AGENT-ADAPTER' / '04_CODE' / '.venv' / 'Scripts' / 'python.exe')
# The W12 execution adapter only accepts timeout_seconds == 30.0 (anything else => BLOCKED w12_timeout_control_not_supported).
W13_TIMEOUT_SECONDS = 30
ENVELOPE_KEYS = ('execution_id', 'work_id', 'status', 'exit_code', 'evidence_ref', 'blocker', 'runtime_instance_id', 'runtime_build_hash', 'runtime_pid', 'runtime_platform', 'runtime_bind_address')


class ExecutionHostBridge:
    def __init__(self, endpoint: str | None = None, timeout: float = 180):
        self.endpoint = (endpoint or os.getenv('EXECUTION_HOST_URL', 'http://127.0.0.1:8031')).rstrip('/')
        self.timeout = timeout

    # ---- transport -------------------------------------------------------------------
    def _post(self, path: str, body: dict) -> dict:
        req = Request(self.endpoint + path, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urlopen(req, timeout=self.timeout + 10) as r:
            return json.loads(r.read())

    def health(self) -> dict:
        """W13 runtime identity as exposed by GET /health (nested under runtime_identity)."""
        with urlopen(self.endpoint + '/health', timeout=10) as r:
            data = json.loads(r.read())
        return data.get('runtime_identity') or {}

    @staticmethod
    def _read(ref) -> str:
        try:
            return Path(ref).read_text(encoding='utf-8') if ref and Path(ref).is_file() else ''
        except OSError:
            return ''

    def capabilities(self, ctx) -> dict:
        return {'w09_1_code': str(W09_1_CODE), 'w09_python': str(W09_PYTHON) if W09_PYTHON.is_file() else None,
                'evidence_dir': str(Path(ctx['evidence_root']) / 'w09_1')}

    # ---- one W13 /execute round trip ---------------------------------------------------
    def _execute(self, ctx, payload):
        root = Path(ctx['execution_workspace']); root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RUNNER, root / 'host_command_runner.py')
        request_id = f'W14-REQ-{uuid.uuid4().hex[:12]}'
        payload = {**payload, 'request_id': request_id, 'capabilities': self.capabilities(ctx)}
        (root / 'host_request.json').write_text(json.dumps(payload), encoding='utf-8')
        body = {'work_context': ctx, 'execution_request': {'command': ['python', 'host_command_runner.py', 'host_request.json'], 'timeout_seconds': W13_TIMEOUT_SECONDS}}
        corr = {'w14_request_id': request_id}
        try:
            envelope = self._post('/execute', body)
        except HTTPError as exc:  # keep the W13 error body: it names the exact contract violation
            return {'status': 'BLOCKED', 'reason': f'w13_http_{exc.code}', 'w13_body': exc.read().decode('utf-8', 'replace'), 'correlation': corr}
        except (URLError, OSError) as exc:
            return {'status': 'BLOCKED', 'reason': 'w13_unreachable:' + type(exc).__name__, 'correlation': corr}
        corr['w13_execution_id'] = envelope.get('execution_id')
        w13 = {k: envelope.get(k) for k in ENVELOPE_KEYS}
        w13.update({'stdout_ref': envelope.get('stdout'), 'stderr_ref': envelope.get('stderr'), 'provider_type': envelope.get('provider_type')})
        if envelope.get('status') != 'PASS':
            return {'status': envelope.get('status', 'BLOCKED'), 'reason': envelope.get('blocker') or envelope.get('reason'), 'w13': w13,
                    'stderr_tail': self._read(envelope.get('stderr'))[-1500:], 'correlation': corr}
        # W13 returns stdout as a reference to runtime/stdout.log (same PC); accept inline content too.
        raw = envelope.get('stdout_summary')
        if raw is None:
            ref = envelope.get('stdout') or ''
            raw = self._read(ref) or ref
        lines = [x for x in str(raw).strip().splitlines() if x.strip()]
        try:
            result = json.loads(lines[-1])
        except (IndexError, ValueError):
            return {'status': 'BLOCKED', 'reason': 'w13_stdout_missing_child_result', 'w13': w13, 'stderr_tail': self._read(envelope.get('stderr'))[-1500:], 'correlation': corr}
        if result.get('request_id') not in (None, request_id):
            return {'status': 'BLOCKED', 'reason': 'w13_child_result_request_mismatch', 'w13': w13, 'correlation': corr}
        result['w13_envelope'] = w13
        result.setdefault('correlation', {}).update(corr)
        return result

    # ---- capabilities (all go through W13 /execute) ------------------------------------
    def context(self, root: Path, repo: Path, evidence: Path, expected_head: str | None = None):
        root = root.resolve(); contained_evidence = (root / 'evidence').resolve(); contained_evidence.mkdir(parents=True, exist_ok=True)
        return {'work_id': '14', 'work_name': 'ROOM-HOP Browser + Autonomous Execution UI', 'workspace_root': str(root), 'execution_workspace': str(root),
                'evidence_root': str(contained_evidence), 'authorized': True, 'repository': 'work14-ui', 'repository_root': str(repo.resolve()),
                'branch': 'main', 'expected_head': expected_head}

    def browser_execute(self, ctx, workflow): return self._execute(ctx, {'kind': 'browser', 'workflow': workflow})
    def git_init(self, ctx): return self._execute(ctx, {'kind': 'git', 'action': 'init', 'repo': ctx['repository_root'], 'branch': ctx['branch']})
    def git_validate(self, ctx): return self._execute(ctx, {'kind': 'git', 'action': 'validate', 'repo': ctx['repository_root'], 'branch': ctx['branch'], 'expected_head': ctx.get('expected_head')})
    def git_commit(self, ctx, message): return self._execute(ctx, {'kind': 'git', 'action': 'commit', 'repo': ctx['repository_root'], 'branch': ctx['branch'], 'message': message})
    def git_diff(self, ctx): return self._execute(ctx, {'kind': 'git', 'action': 'diff', 'repo': ctx['repository_root'], 'branch': ctx['branch'], 'path': 'artifact.txt'})
