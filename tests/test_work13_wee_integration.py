import json
import sys
from pathlib import Path

from wee.authority import CanonicalWorkAuthority
from wee.models import WorkContext, EvidenceStore
from wee.controller import LifecycleController
from wee_work13_adapter import Work13ExecutionHostAdapter

def test_work13_real_host_e2e(tmp_path):
    authority_file=tmp_path/"authority.json"
    workspace=tmp_path/"workspace"
    evidence=tmp_path/"evidence"
    workspace.mkdir()

    authority_file.write_text(json.dumps({
        "work_id":"W13-E2E",
        "work_name":"EXECUTION-HOST-INFRASTRUCTURE",
        "repository":"local/test",
        "repository_root":str(tmp_path),
        "branch":"main",
        "execution_workspace":str(workspace),
        "expected_head":"test-head",
        "runtime":{},
        "browser":{},
        "test_entrypoint":[
            sys.executable,"-c",
            "print('W13_WEE_TEST_PASS')"
        ],
        "ci_target":{},
        "evidence_root":str(evidence)
    }))

    binding=CanonicalWorkAuthority(authority_file).resolve("W13-E2E")
    context=WorkContext.from_binding(binding,"W13-WEE-E2E")
    host=Work13ExecutionHostAdapter(context)

    result=host.execute(context.test_entrypoint,context)

    assert result.status=="PASS"
    assert result.exit_code==0

    final=evidence/"W13-WEE-E2E"/"FINAL_RESULT.json"
    assert final.exists()

    payload=json.loads(final.read_text())
    assert payload["execution_id"]=="W13-WEE-E2E"
    assert payload["work_id"]=="W13-E2E"
    assert payload["status"]=="PASS"

    stdout=evidence/"W13-WEE-E2E"/"runtime"/"stdout.log"
    assert "W13_WEE_TEST_PASS" in stdout.read_text()
