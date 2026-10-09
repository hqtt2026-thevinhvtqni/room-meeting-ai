from __future__ import annotations
import subprocess
class TestRunner:
    def run(self, stage: str, command: list[str] | None):
        if not command: return {'stage':stage,'status':'BLOCKED','reason':'command_not_configured'}
        p=subprocess.run(command, text=True, capture_output=True)
        return {'stage':stage,'status':'PASS' if p.returncode==0 else 'FAILED','returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
