from __future__ import annotations
import subprocess
from pathlib import Path

class GitGateway:
    def __init__(self, root: str, expected_repo: str|None, expected_branch: str|None, expected_head: str|None=None):
        self.root, self.expected_repo, self.expected_branch, self.expected_head = Path(root), expected_repo, expected_branch, expected_head
    def _run(self, *args):
        p=subprocess.run(['git',*args],cwd=self.root,text=True,capture_output=True)
        return {'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
    def status(self): return self._run('status','--short','--branch')
    def head(self): return self._run('rev-parse','HEAD')
    def branch(self): return self._run('branch','--show-current')
    def resolve_repo(self): return self._run('config','--get','remote.origin.url')
    def validate_target(self):
        if not self.root.exists(): return {'status':'BLOCKED','reason':'workspace_root_missing'}
        if not self.expected_repo or not self.expected_branch or not self.expected_head: return {'status':'BLOCKED','reason':'canonical_git_binding_incomplete'}
        b,r,h=self.branch(),self.resolve_repo(),self.head()
        if b['stdout']!=self.expected_branch: return {'status':'BLOCKED','reason':'wrong_branch','actual':b['stdout'],'expected':self.expected_branch}
        if self.expected_repo not in r['stdout']: return {'status':'BLOCKED','reason':'wrong_repo','actual':r['stdout'],'expected':self.expected_repo}
        if h['stdout']!=self.expected_head: return {'status':'BLOCKED','reason':'unexpected_initial_head','actual':h['stdout'],'expected':self.expected_head}
        return {'status':'PASS','branch':b['stdout'],'repository':r['stdout'],'head':h['stdout']}
    def commit(self,message,validation_status):
        if validation_status!='PASS': return {'status':'BLOCKED','reason':'validation_not_pass'}
        return self._run('commit','-am',message)
    def push(self,validation_status):
        if validation_status!='PASS': return {'status':'BLOCKED','reason':'commit_validation_not_pass'}
        return self._run('push')
