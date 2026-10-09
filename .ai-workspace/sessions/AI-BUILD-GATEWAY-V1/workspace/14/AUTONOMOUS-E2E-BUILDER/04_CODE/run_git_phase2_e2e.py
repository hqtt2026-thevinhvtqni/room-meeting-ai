from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from git_provider_phase2 import LocalGitProvider

ROOT = Path('/tmp/work14-git-phase2')
if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)
repo = ROOT / 'repo'; repo.mkdir()
def run(*args): return subprocess.run(args, cwd=repo, text=True, capture_output=True, check=True)
run('git','init','-b','main')
run('git','config','user.name','Work14 Nu')
run('git','config','user.email','nu@work14.local')
run('git','remote','add','origin','https://example.invalid/local-phase2.git')
(repo/'artifact.txt').write_text('initial\n', encoding='utf-8')
run('git','add','artifact.txt'); run('git','commit','-m','initial fixture')
expected_head = run('git','rev-parse','HEAD').stdout.strip()
(repo/'artifact.txt').write_text('provider-integrated\n', encoding='utf-8')
provider = LocalGitProvider()
validation = provider.validate(repo, 'local-phase2', 'main', expected_head)
assert validation['status'] == 'PASS', validation
blocked = provider.commit(repo, 'unauthorized should not happen', authorized=False)
assert blocked['status'] == 'BLOCKED'
commit = provider.commit(repo, 'provider integration phase 2', authorized=True)
assert commit['status'] == 'PASS', commit
new_head = run('git','rev-parse','HEAD').stdout.strip()
result = {'status':'PASS','provider':provider.name,'repository':'local-phase2','branch':'main','expected_head':expected_head,'new_head':new_head,'validation':validation,'unauthorized_commit':blocked,'authorized_commit':commit,'artifact':(repo/'artifact.txt').read_text().strip()}
(ROOT/'GIT_PHASE2_SUMMARY.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
