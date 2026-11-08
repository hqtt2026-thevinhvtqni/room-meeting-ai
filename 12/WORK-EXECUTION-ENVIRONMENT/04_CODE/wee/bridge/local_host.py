from __future__ import annotations
import importlib.util, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path
from .contracts import ExecutionResult
from ..models import WorkContext

class LocalExecutionHost:
    provider_type='LOCAL'
    def __init__(self, evidence_root='06_EVIDENCE'): self.evidence_root=Path(evidence_root)
    def _probe_exe(self,names):
        for name in names:
            path=shutil.which(name)
            if path: return {'status':'AVAILABLE','path':path}
        return {'status':'NOT_CONFIGURED','expected':names}
    def discover(self, context: WorkContext):
        browser=self._probe_exe(['chromium','chromium-browser','google-chrome'])
        playwright={'status':'AVAILABLE' if importlib.util.find_spec('playwright') else 'NOT_CONFIGURED'}
        return {'provider_type':self.provider_type,'work_id':context.work_id,'execution_id':context.execution_id,'capabilities':[
            {'name':'filesystem','status':'AVAILABLE'}, {'name':'shell','status':self._probe_exe(['sh'])['status']},
            {'name':'git','status':self._probe_exe(['git'])['status']}, {'name':'runtime','status':'AVAILABLE' if shutil.which('python3') or shutil.which('node') else 'NOT_CONFIGURED'},
            {'name':'browser','status':browser['status'],'evidence':browser}, {'name':'chromium','status':browser['status'],'evidence':browser},
            {'name':'playwright','status':playwright['status'],'evidence':playwright}, {'name':'test','status':'AVAILABLE' if shutil.which('python3') else 'NOT_CONFIGURED'}]}
    def execute(self, command, context: WorkContext):
        started=datetime.now(timezone.utc).isoformat(); base=self.evidence_root/context.execution_id/'runtime'; base.mkdir(parents=True, exist_ok=True)
        out,err=base/'stdout.log',base/'stderr.log'
        try:
            p=subprocess.run(command,cwd=context.execution_workspace,text=True,capture_output=True)
            out.write_text(p.stdout,encoding='utf-8'); err.write_text(p.stderr,encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,context.execution_workspace,command,started,datetime.now(timezone.utc).isoformat(),p.returncode,str(out),str(err),[str(out),str(err)],'PASS' if p.returncode==0 else 'FAILED',self.provider_type)
        except OSError as exc:
            err.write_text(str(exc),encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,context.execution_workspace,command,started,datetime.now(timezone.utc).isoformat(),None,None,str(err),[str(err)],'FAILED',self.provider_type)
    def runtime_info(self, context): return {'execution_id':context.execution_id,'provider_type':self.provider_type,'python':shutil.which('python3'),'node':shutil.which('node')}
    def browser_info(self, context): return {'execution_id':context.execution_id,'provider_type':self.provider_type,**self._probe_exe(['chromium','chromium-browser','google-chrome'])}
    def workspace_info(self, context): return {'workspace':context.execution_workspace,'exists':Path(context.execution_workspace).exists(),'is_dir':Path(context.execution_workspace).is_dir()}
    def collect_artifact(self,path,execution_id): return str(Path(path))
    def cleanup(self): return None
