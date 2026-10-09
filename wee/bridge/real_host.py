from __future__ import annotations
import os, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .contracts import ExecutionResult
from .local_host import LocalExecutionHost
from ..models import WorkContext

class WorkIsolationError(RuntimeError): pass

class RealExecutionHost(LocalExecutionHost):
    provider_type='REAL'
    def __init__(self, evidence_root='06_EVIDENCE', *, enabled=False, allow_processes=False, browser=None, github=None, ci=None):
        if not enabled: raise RuntimeError('REAL execution host is not enabled/configured')
        super().__init__(evidence_root); self.allow_processes=allow_processes; self.browser=browser; self.github=github; self.ci=ci; self.processes={}
    def _workspace(self, context: WorkContext) -> Path:
        root=Path(context.execution_workspace).resolve()
        if not root.exists() or not root.is_dir(): raise WorkIsolationError('execution_workspace_missing')
        allowed=Path(context.evidence_root).resolve().parent
        try: root.relative_to(allowed)
        except ValueError: raise WorkIsolationError('execution_workspace_outside_work_sandbox')
        return root
    def workspace_info(self, context):
        root=self._workspace(context)
        return {'status':'PASS','workspace':str(root),'work_id':context.work_id,'execution_id':context.execution_id}
    def discover(self, context):
        report=super().discover(context); report.update({'provider_type':'REAL','execution_id':context.execution_id,'work_id':context.work_id,'workspace':self.workspace_info(context)})
        report['capabilities'] += [
            {'name':'process_lifecycle','status':'AVAILABLE' if self.allow_processes else 'BLOCKED','reason':'explicit_process_permission_required'},
            {'name':'github','status':'AVAILABLE' if self.github else 'NOT_CONFIGURED','reason':'gateway adapter not supplied' if not self.github else ''},
            {'name':'ci','status':'AVAILABLE' if self.ci else 'NOT_CONFIGURED','reason':'CI adapter not supplied' if not self.ci else ''}]
        return report
    def execute(self, command, context: WorkContext):
        workspace=self._workspace(context); started=datetime.now(timezone.utc).isoformat(); base=self.evidence_root/context.execution_id/'runtime'; base.mkdir(parents=True,exist_ok=True); out,err=base/'stdout.log',base/'stderr.log'
        try:
            p=subprocess.run(command,cwd=workspace,text=True,capture_output=True,env={**os.environ,'ROOM_HOP_EXECUTION_ID':context.execution_id,'ROOM_HOP_WORK_ID':context.work_id})
            out.write_text(p.stdout,encoding='utf-8'); err.write_text(p.stderr,encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),p.returncode,str(out),str(err),[str(out),str(err)],'PASS' if p.returncode==0 else 'FAILED',self.provider_type)
        except (OSError,WorkIsolationError) as exc:
            err.write_text(str(exc),encoding='utf-8'); return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),None,None,str(err),[str(err)],'BLOCKED',self.provider_type)
    def start_service(self,name,command,context):
        workspace=self._workspace(context)
        if not self.allow_processes: return {'status':'BLOCKED','reason':'process_permission_not_granted','execution_id':context.execution_id}
        if name in self.processes and self.processes[name].poll() is None: return {'status':'PASS','pid':self.processes[name].pid,'already_running':True,'execution_id':context.execution_id}
        self.processes[name]=subprocess.Popen(command,cwd=workspace,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True); return {'status':'PASS','pid':self.processes[name].pid,'execution_id':context.execution_id}
    def service_status(self,name,context):
        p=self.processes.get(name); return {'status':'PASS' if p and p.poll() is None else 'FAILED','name':name,'returncode':None if not p else p.poll(),'execution_id':context.execution_id}
    def stop_service(self,name,context):
        p=self.processes.pop(name,None)
        if not p: return {'status':'BLOCKED','reason':'service_not_found','execution_id':context.execution_id}
        if p.poll() is None: p.terminate()
        return {'status':'PASS','execution_id':context.execution_id}
    def run_test(self,context):
        if not context.test_entrypoint: return {'status':'BLOCKED','reason':'test_entrypoint_not_bound','execution_id':context.execution_id}
        return self.execute(context.test_entrypoint,context).as_dict()
    def browser_execute(self,context,action):
        if not self.browser: return {'status':'NOT_CONFIGURED','reason':'browser_adapter_not_supplied','execution_id':context.execution_id}
        return self.browser.execute(context,action)
    def git_validate(self,context):
        if not context.repository_root or not context.branch or not context.expected_head: return {'status':'BLOCKED','reason':'git_binding_incomplete','execution_id':context.execution_id}
        from ..git_gateway import GitGateway
        return GitGateway(context.repository_root,context.repository,context.branch,context.expected_head).validate_target()
    def github_verify(self,context):
        if not self.github: return {'status':'NOT_CONFIGURED','reason':'github_gateway_not_supplied','execution_id':context.execution_id}
        return self.github.verify_head(context,context.expected_head)
    def ci_verify(self,context,commit_sha):
        if not self.ci: return {'status':'NOT_CONFIGURED','reason':'ci_adapter_not_supplied','execution_id':context.execution_id}
        return self.ci.verify(context,commit_sha)
    def collect_artifact(self,path,execution_id):
        source=Path(path).resolve(); target=self.evidence_root/execution_id/'artifacts'/source.name; target.parent.mkdir(parents=True,exist_ok=True)
        if source.exists(): shutil.copy2(source,target); return str(target)
        return ''
    def cleanup(self):
        for name,p in list(self.processes.items()):
            if p.poll() is None: p.terminate()
            self.processes.pop(name,None)
