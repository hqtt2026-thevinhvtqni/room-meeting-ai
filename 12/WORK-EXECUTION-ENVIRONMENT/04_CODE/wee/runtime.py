from __future__ import annotations
import subprocess, time
class RuntimeManager:
    def __init__(self): self.processes = {}
    def discover(self): return {'python': True, 'node': bool(__import__('shutil').which('node')), 'processes': list(self.processes)}
    def start(self, name, command):
        if name in self.processes and self.processes[name].poll() is None: return {'status':'PASS','pid':self.processes[name].pid,'already_running':True}
        try:
            self.processes[name] = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return {'status':'PASS','pid':self.processes[name].pid}
        except OSError as e: return {'status':'BLOCKED','reason':str(e)}
    def health_check(self, name, timeout=5):
        p=self.processes.get(name)
        if not p: return {'status':'BLOCKED','reason':'process_not_started'}
        time.sleep(min(timeout, .1)); return {'status':'PASS' if p.poll() is None else 'FAILED','returncode':p.poll()}
    def stop(self, name):
        p=self.processes.pop(name, None)
        if p and p.poll() is None: p.terminate(); return {'status':'PASS'}
        return {'status':'BLOCKED','reason':'process_not_found'}
    def status(self): return {n: ('running' if p.poll() is None else 'exited') for n,p in self.processes.items()}
