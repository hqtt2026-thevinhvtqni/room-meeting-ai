from __future__ import annotations
from pathlib import Path
from typing import Any
from .models import WorkContext, EvidenceStore, LIFECYCLE
from .bridge.local_host import LocalExecutionHost

class LifecycleController:
    """Generic work_e2e lifecycle. It never invents targets and never fake-passes."""
    def __init__(self, context: WorkContext, evidence: EvidenceStore, host=None, max_repair_cycles: int = 2):
        self.ctx, self.ev = context, evidence
        self.host = host or LocalExecutionHost(context.evidence_root)
        self.max_repair_cycles = max_repair_cycles
        self.states: list[dict[str, Any]] = []
    def stage(self, name: str, status: str, **data: Any) -> None:
        item = {'stage': name, 'status': status, 'execution_id': self.ctx.execution_id, **data}
        self.states.append(item); self.ev.record(name, status, **data)
    def run(self) -> dict[str, Any]:
        self.ev.write('authority.json', {'work_id': self.ctx.work_id, 'work_name': self.ctx.work_name, 'source': 'canonical authority'})
        self.stage('RESOLVE', 'PASS', work_id=self.ctx.work_id, work_name=self.ctx.work_name)
        self.ev.write('context.json', self.ctx.as_dict())
        self.stage('BIND', 'PASS', context=self.ctx.as_dict())
        blockers = self._validate_binding()
        if blockers:
            self.stage('VALIDATE', 'BLOCKED', blockers=blockers)
            return self._finish('BLOCKED', blockers[0]['reason'], blockers)
        self.stage('VALIDATE', 'PASS')
        self.stage('PREPARE', 'PASS', workspace=self.ctx.execution_workspace)
        report = self.host.discover(self.ctx)
        self.ev.write('runtime/discovery.json', report)
        self.stage('EXECUTE', 'PASS', host=report)
        if not self.ctx.test_entrypoint:
            blocker = {'reason':'test_entrypoint_missing'}
            self.stage('TEST', 'BLOCKED', blockers=[blocker]); return self._finish('BLOCKED', blocker['reason'], [blocker])
        self.stage('TEST', 'BLOCKED', reason='execution adapter must run the bound entrypoint')
        return self._finish('BLOCKED', 'test_execution_not_available_in_sandbox_boundary', [])
    def _validate_binding(self):
        required = {'repository': self.ctx.repository, 'repository_root': self.ctx.repository_root, 'branch': self.ctx.branch, 'expected_head': self.ctx.expected_head}
        return [{'field': key, 'reason': f'authority_field_not_configured:{key}'} for key, value in required.items() if not value]
    def _finish(self, status: str, reason: str, blockers: list[dict[str, Any]]) -> dict[str, Any]:
        gates = {name: 'PASS' if any(x['stage'] == name and x['status'] == 'PASS' for x in self.states) else 'BLOCKED' for name in ('RESOLVE','BIND','VALIDATE','PREPARE','EXECUTE','TEST','COMMIT','PUSH','CI','VERIFY')}
        payload = {'work_id': self.ctx.work_id, 'execution_id': self.ctx.execution_id, 'status': status, 'initial_head': self.ctx.expected_head, 'final_head': None, 'github_head': None, 'tests': gates['TEST'], 'ci': gates['CI'], 'evidence_root': str(self.ev.path), 'failure_reason': reason, 'gates': gates, 'lifecycle': self.states, 'blockers': blockers, 'no_fake_pass': True}
        self.ev.write('FINAL_RESULT.json', payload)
        return {'status': status, 'work_id': self.ctx.work_id, 'execution_id': self.ctx.execution_id, 'evidence': str(self.ev.path), 'blocker': reason}
