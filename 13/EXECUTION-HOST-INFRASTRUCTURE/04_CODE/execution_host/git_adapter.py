from __future__ import annotations
import subprocess
from pathlib import Path
from .security import redact

class GitAdapter:
    def __init__(self, ctx): self.ctx = ctx
    def _bound(self):
        if not self.ctx.repository_root or not self.ctx.repository or not self.ctx.branch or not self.ctx.expected_head: return {'status':'BLOCKED','reason':'missing_git_authority'}
        root=Path(self.ctx.repository_root).resolve()
        try: root.relative_to(Path(self.ctx.workspace_root).resolve())
        except ValueError: return {'status':'BLOCKED','reason':'repository_escape'}
        return None
    def _run(self,*args):
        p=subprocess.run(['git',*args],cwd=self.ctx.repository_root,text=True,capture_output=True,env={'PATH':__import__('os').environ.get('PATH','')})
        return {'exit_code':p.returncode,'stdout':redact(p.stdout),'stderr':redact(p.stderr)}
    def validate(self):
        if (blocked:=self._bound()): return blocked
        branch=self._run('branch','--show-current'); head=self._run('rev-parse','HEAD'); remote=self._run('config','--get','remote.origin.url')
        if branch['stdout'].strip()!=self.ctx.branch: return {'status':'BLOCKED','reason':'wrong_branch','actual':branch['stdout'].strip()}
        if self.ctx.repository not in remote['stdout']: return {'status':'BLOCKED','reason':'wrong_repository'}
        if head['stdout'].strip()!=self.ctx.expected_head: return {'status':'BLOCKED','reason':'unexpected_head','actual':head['stdout'].strip()}
        return {'status':'PASS','branch':self.ctx.branch,'repository':self.ctx.repository,'head':self.ctx.expected_head}
    def status(self): return self._run('status','--short','--branch') if not self._bound() else self._bound()
    def commit(self,message,authorized=False):
        if not authorized: return {'status':'BLOCKED','reason':'commit_not_authorized'}
        v=self.validate(); return v if v.get('status')!='PASS' else dict(self._run('commit','-am',message),status='PASS')
    def push(self,authorized=False):
        if not authorized: return {'status':'BLOCKED','reason':'push_not_authorized'}
        v=self.validate(); return v if v.get('status')!='PASS' else dict(self._run('push'),status='PASS')
