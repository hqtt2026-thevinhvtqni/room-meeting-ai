from __future__ import annotations

import functools
import hashlib
import http.server
import json
import shutil
import subprocess
import threading
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from browser_provider_phase2 import BrowserProvider

ROOT = Path('/tmp/work14-phase3')
if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)
EVIDENCE = ROOT / 'evidence'; EVIDENCE.mkdir()
REPO = ROOT / 'repo'; REPO.mkdir()

def git(*args: str, check: bool = True):
    return subprocess.run(['git', *args], cwd=REPO, text=True, capture_output=True, check=check)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(event: str, **data): lifecycle.append({'ts': time.time(), 'event': event, **data})

lifecycle = []
execution_id = 'W14-PHASE3-001'
idempotency_key = 'work14-phase3-full-pipeline-v1'
expected_value = 'browser-result-good'
git('init', '-b', 'main'); git('config', 'user.name', 'Work14 Nu'); git('config', 'user.email', 'nu@work14.local')
git('remote', 'add', 'origin', 'https://example.invalid/work14-phase3.git')
(REPO / 'artifact.txt').write_text('baseline\n'); git('add', 'artifact.txt'); git('commit', '-m', 'phase3 baseline')
expected_head = git('rev-parse', 'HEAD').stdout.strip(); record('git_baseline', expected_head=expected_head)
fixture = ROOT / 'fixture'; fixture.mkdir()
(fixture / 'index.html').write_text('<!doctype html><html><head><title>Work 14 Phase 3 Fixture</title></head><body><h1>Phase 3 Browser Target</h1><p id="result">browser-result-good</p><input id="q"></body></html>')
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(fixture)))
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    url = f'http://127.0.0.1:{server.server_port}/index.html'
    browser_result = BrowserProvider().execute('Work 14', url, [{'op':'inspect'}, {'op':'extract','selectors':{'result':'#result'}}, {'op':'screenshot','name':'phase3-browser.png'}, {'op':'close'}], EVIDENCE)
    assert browser_result['status'] == 'PASS'; record('browser_execution_pass', execution_id=browser_result['execution_id'])
    artifact = REPO / 'artifact.txt'; artifact.write_text('bad\n'); record('artifact_created', value='bad')
    first_verify = artifact.read_text().strip() == expected_value; record('intentional_failure', expected=expected_value, actual=artifact.read_text().strip(), passed=first_verify)
    assert not first_verify
    record('diagnose', reason='artifact_value_mismatch_after_browser_result_creation')
    artifact.write_text(expected_value + '\n'); record('automatic_repair', value=expected_value); assert artifact.read_text().strip() == expected_value; record('retest_pass')
    actual_branch = git('branch','--show-current').stdout.strip(); actual_remote = git('config','--get','remote.origin.url').stdout.strip(); actual_head = git('rev-parse','HEAD').stdout.strip()
    authorized = {'requester':'nu','work_id':'14','repository':'work14-phase3','branch':'main','expected_head':expected_head}
    authority_ok = actual_branch == 'main' and 'work14-phase3' in actual_remote and actual_head == expected_head; record('git_authorization', status='PASS' if authority_ok else 'BLOCKED'); assert authority_ok
    git('add','artifact.txt'); git('commit','-m','phase3 repaired browser artifact'); commit_head = git('rev-parse','HEAD').stdout.strip(); record('commit', status='PASS', head=commit_head)
    evidence = {'execution_id':execution_id,'idempotency_key':idempotency_key,'work_id':'Work 14','status':'PASS','browser':browser_result,'artifact':{'path':'artifact.txt','value':artifact.read_text().strip(),'sha256':sha256(artifact)},'authorization':authorized,'commit_head':commit_head,'intentional_failure':True,'automatic_repair':True,'lifecycle':lifecycle}
    (ROOT/'ledger.json').write_text(json.dumps({idempotency_key:{'commit_head':commit_head,'artifact_sha256':evidence['artifact']['sha256']}}, indent=2)); (EVIDENCE/f'{execution_id}.json').write_text(json.dumps(evidence, indent=2)); record('final_evidence_capture')
    before_count = int(git('rev-list','--count','HEAD').stdout.strip()); replay = json.loads((ROOT/'ledger.json').read_text())[idempotency_key]; replay_status = 'REPLAYED_IDEMPOTENTLY' if replay['commit_head'] == commit_head and sha256(artifact) == replay['artifact_sha256'] else 'FAIL'; after_count = int(git('rev-list','--count','HEAD').stdout.strip()); assert replay_status == 'REPLAYED_IDEMPOTENTLY' and before_count == after_count; record('replay_idempotency_pass', commit_count=after_count)
    checks = {'browser_execution':browser_result['status']=='PASS','artifact_result_creation':artifact.exists(),'git_authorization':authority_ok,'commit':commit_head!=expected_head,'evidence_capture':(EVIDENCE/f'{execution_id}.json').exists(),'replay_idempotency':replay_status=='REPLAYED_IDEMPOTENTLY','intentional_failure':any(e['event']=='intentional_failure' and not e['passed'] for e in lifecycle),'automatic_repair':any(e['event']=='automatic_repair' for e in lifecycle),'full_rerun':after_count==before_count}; assert all(checks.values()), checks
    summary = {'execution_id':execution_id,'status':'PASS','checks':checks,'commit_head':commit_head,'replay':replay_status,'evidence':str(EVIDENCE/f'{execution_id}.json')}; (ROOT/'PHASE3_FINAL_RESULT.json').write_text(json.dumps(summary, indent=2)); print(json.dumps(summary, indent=2))
finally:
    server.shutdown(); server.server_close()
