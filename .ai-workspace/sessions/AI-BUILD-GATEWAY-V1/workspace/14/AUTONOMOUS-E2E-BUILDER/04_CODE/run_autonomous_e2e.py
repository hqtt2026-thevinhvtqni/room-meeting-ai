import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from autonomous_builder import AutonomousBuilder, WorkRequest

root = Path('/tmp/work14-autonomous-e2e')
if root.exists(): shutil.rmtree(root)
workspace = root / 'workspace'; workspace.mkdir(parents=True)
request = WorkRequest('W14-E2E-001', 'Work 14', 'nu', str(workspace), [sys.executable, '-c', "from pathlib import Path; Path('artifact.txt').write_text('bad')"], [sys.executable, '-c', "from pathlib import Path; import sys; sys.exit(0 if Path('artifact.txt').read_text() == 'good' else 1)"], [sys.executable, '-c', "from pathlib import Path; Path('artifact.txt').write_text('good')"])
result = AutonomousBuilder(root / 'evidence').build(request)
assert result['status'] == 'PASS', result
assert (workspace / 'artifact.txt').read_text() == 'good'
assert any(x['stage'] == 'DETECT' for x in result['lifecycle'])
summary = {'status': 'PASS', 'result': result, 'artifact': str(workspace / 'artifact.txt'), 'artifact_value': (workspace / 'artifact.txt').read_text()}
(root / 'E2E_SUMMARY.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
