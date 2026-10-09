import json
from pathlib import Path

from wee.models import WorkContext
from wee_work13_adapter import Work13ExecutionHostAdapter

ROOT = Path.cwd()

WORKSPACE = (
ROOT
/ ".ai-workspace"
/ "sessions"
/ "AI-BUILD-GATEWAY-V1"
/ "workspace"
/ "14"
/ "AUTONOMOUS-E2E-BUILDER"
)

EVIDENCE = WORKSPACE / "06_EVIDENCE"
EVIDENCE.mkdir(parents=True, exist_ok=True)

context = WorkContext(
work_id="14",
work_name="AUTONOMOUS-E2E-BUILDER",
repository=str(ROOT),
repository_root=str(ROOT),
branch=None,
execution_workspace=str(WORKSPACE),
expected_head=None,
runtime={"python": "3.12"},
browser={"provider": "chromium"},
test_entrypoint=None,
ci_target={},
evidence_root=str(EVIDENCE),
execution_id="W14-W13-REAL-EXECUTION-001",
)

adapter = Work13ExecutionHostAdapter(context)

print("=== CONTEXT ===")
print("repository       =", context.repository)
print("execution_workspace =", context.execution_workspace)
print("evidence_root    =", context.evidence_root)

print("\n=== DISCOVER ===")
print(json.dumps(adapter.discover(context), indent=2, default=str))

print("\n=== RUNTIME ===")
print(json.dumps(adapter.runtime_info(context), indent=2, default=str))

print("\n=== WORKSPACE ===")
print(json.dumps(adapter.workspace_info(context), indent=2, default=str))

print("\n=== BROWSER ===")
print(json.dumps(adapter.browser_info(context), indent=2, default=str))

print("\n=== EXECUTE ===")
result = adapter.execute(["python", "--version"], context)
print(json.dumps(result, indent=2, default=str))

print("\n=== DONE ===")
