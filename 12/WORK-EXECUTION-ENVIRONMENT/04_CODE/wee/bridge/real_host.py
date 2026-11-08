from __future__ import annotations
import os, shutil, subprocess, threading, time
import psutil
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
    def execute(self, command, context: WorkContext, timeout_seconds: float = 30.0):
        workspace=self._workspace(context); started=datetime.now(timezone.utc).isoformat(); base=self.evidence_root/context.execution_id/'runtime'; base.mkdir(parents=True,exist_ok=True); out,err=base/'stdout.log',base/'stderr.log'
        if not self.allow_processes:
            err.write_text('process_permission_not_granted',encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),None,None,str(err),[str(err)],'BLOCKED',self.provider_type,blocker='process_permission_not_granted')
        if not isinstance(timeout_seconds,(int,float)) or timeout_seconds <= 0 or timeout_seconds > 3600:
            err.write_text('invalid_timeout',encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),None,None,str(err),[str(err)],'BLOCKED',self.provider_type,blocker='invalid_timeout')
        keep={'PATH','HOME','LANG','LC_ALL','SYSTEMROOT','WINDIR','TMP','TEMP','PATHEXT','COMSPEC','HOMEDRIVE','HOMEPATH','USERPROFILE'}
        child_env={k:v for k,v in os.environ.items() if k in keep}
        child_env.update({'ROOM_HOP_EXECUTION_ID':context.execution_id,'ROOM_HOP_WORK_ID':context.work_id})
        process=None; observed={}; observer_errors=[]; stop=threading.Event()
        try:
            process=psutil.Popen(command,cwd=workspace,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=child_env)
            def watch_children():
                while not stop.is_set():
                    try:
                        for child in process.children(recursive=True):
                            observed[child.pid]=child
                    except psutil.AccessDenied:
                        observer_errors.append("process_tree_access_denied")
                    except (psutil.NoSuchProcess,psutil.ZombieProcess):
                        pass
                    time.sleep(0.02)
            watcher=threading.Thread(target=watch_children,daemon=True)
            watcher.start()
            timed_out=False
            try:
                stdout,stderr=process.communicate(timeout=float(timeout_seconds))
            except subprocess.TimeoutExpired:
                timed_out=True
                try: process.kill()
                except (psutil.NoSuchProcess,psutil.AccessDenied): pass
                try: stdout,stderr=process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    stdout,stderr="","process_reap_timeout"
            finally:
                stop.set(); watcher.join(timeout=1)
            # Reap every descendant observed while the command was alive.
            descendants=list(observed.values())
            for child in reversed(descendants):
                try:
                    if child.is_running(): child.kill()
                except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
                    pass
            _,alive=psutil.wait_procs(descendants,timeout=5)
            process_reaped=process.poll() is not None
            cleanup_verified=process_reaped and not alive and not observer_errors
            out.write_text(stdout or '',encoding='utf-8')
            err_text=stderr or ''
            if timed_out: err_text=(err_text+'\nexecution_timeout').strip()
            if observer_errors: err_text=(err_text+'\n'+','.join(sorted(set(observer_errors)))).strip()
            err.write_text(err_text,encoding='utf-8')
            if not cleanup_verified:
                status='BLOCKED'; blocker='process_tree_cleanup_unverified'
            elif timed_out:
                status='FAILED'; blocker='execution_timeout'
            else:
                status='PASS' if process.returncode==0 else 'FAILED'; blocker=None
            return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),process.returncode,str(out),str(err),[str(out),str(err)],status,self.provider_type,blocker=blocker,timed_out=timed_out,process_tree_cleanup_verified=cleanup_verified)
        except (OSError,WorkIsolationError,psutil.Error) as exc:
            err.write_text(str(exc),encoding='utf-8')
            return ExecutionResult(context.execution_id,context.work_id,str(workspace),list(command),started,datetime.now(timezone.utc).isoformat(),None,None,str(err),[str(err)],'BLOCKED',self.provider_type,blocker=type(exc).__name__)

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
