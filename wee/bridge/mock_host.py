from datetime import datetime, timezone
from .contracts import ExecutionResult
class MockExecutionHost:
    provider_type='MOCK'
    def __init__(self, fail_command=False, fail_browser=False): self.fail_command=fail_command; self.fail_browser=fail_browser
    def discover(self, context):
        status='FAILED' if self.fail_browser else 'AVAILABLE'
        return {'provider_type':'MOCK','work_id':context.work_id,'execution_id':context.execution_id,'capabilities':[{'name':n,'status':status if n in ('browser','chromium','playwright') else 'AVAILABLE','evidence':{'mock':True}} for n in ('filesystem','shell','git','runtime','browser','chromium','playwright','test')]}
    def execute(self,command,context):
        now=datetime.now(timezone.utc).isoformat(); ok=not self.fail_command
        return ExecutionResult(context.execution_id,context.work_id,context.execution_workspace,command,now,now,0 if ok else 1,None,None,[],'PASS' if ok else 'FAILED','MOCK')
    def runtime_info(self, context): return {'provider_type':'MOCK','execution_id':context.execution_id,'mock':True}
    def browser_info(self, context): return {'provider_type':'MOCK','execution_id':context.execution_id,'mock':True,'launch':'FAILED' if self.fail_browser else 'AVAILABLE'}
    def workspace_info(self, context): return {'provider_type':'MOCK','workspace':context.execution_workspace}
    def collect_artifact(self,path,execution_id): return path
    def cleanup(self): return None
