from __future__ import annotations
import shutil
from dataclasses import dataclass, asdict
from enum import Enum

class CapabilityStatus(str, Enum):
    AVAILABLE='AVAILABLE'; BLOCKED='BLOCKED'; NOT_CONFIGURED='NOT_CONFIGURED'; FAILED='FAILED'

@dataclass
class Capability:
    name: str
    status: CapabilityStatus
    reason: str = ''
    evidence: dict = None
    def as_dict(self):
        return {'name':self.name,'status':self.status.value,'reason':self.reason,'evidence':self.evidence or {}}

class CapabilityDiscovery:
    REQUIRED=('filesystem','shell','git','runtime','browser','chromium','playwright','github','commit','push','ci','evidence')
    def _executable(self, names):
        found=next((shutil.which(x) for x in names if shutil.which(x)),None)
        return CapabilityStatus.AVAILABLE if found else CapabilityStatus.NOT_CONFIGURED, {'executables':list(names),'resolved':found}
    def discover(self):
        out=[]
        status,ev=self._executable(['sh']); out.append(Capability('shell',status,'shell executable not configured' if status!=CapabilityStatus.AVAILABLE else '',ev))
        status,ev=self._executable(['git']); out.append(Capability('git',status,'git executable not configured' if status!=CapabilityStatus.AVAILABLE else '',ev))
        status,ev=self._executable(['python3','node']); out.append(Capability('runtime',status,'Python/Node runtime not configured' if status!=CapabilityStatus.AVAILABLE else '',ev))
        browser_status,browser_ev=self._executable(['chromium','chromium-browser','google-chrome']); out += [Capability('browser',browser_status,'browser runtime not configured' if browser_status!=CapabilityStatus.AVAILABLE else '',browser_ev), Capability('chromium',browser_status,'Chromium not configured' if browser_status!=CapabilityStatus.AVAILABLE else '',browser_ev)]
        try: __import__('playwright'); out.append(Capability('playwright',CapabilityStatus.AVAILABLE,'',{'import':'ok'}))
        except ImportError: out.append(Capability('playwright',CapabilityStatus.NOT_CONFIGURED,'Playwright package not configured',{'import':'missing'}))
        out += [
            Capability('filesystem',CapabilityStatus.AVAILABLE,'',{'probe':'Work Sandbox write/read boundary'}),
            Capability('evidence',CapabilityStatus.AVAILABLE,'',{'probe':'EvidenceStore contract'}),
            Capability('github',CapabilityStatus.NOT_CONFIGURED,'GitHub gateway/credential not configured',{'adapter':'missing'}),
            Capability('ci',CapabilityStatus.NOT_CONFIGURED,'CI provider adapter not configured',{'adapter':'missing'}),
            Capability('commit',CapabilityStatus.BLOCKED,'ROOM-HOP governance does not grant AI commit authority',{'policy':'AI cannot commit/merge/push'}),
            Capability('push',CapabilityStatus.BLOCKED,'ROOM-HOP governance does not grant AI push authority',{'policy':'AI cannot commit/merge/push'}),
        ]
        return out
    def report(self):
        caps=[c.as_dict() for c in self.discover()]
        blockers=[c for c in caps if c['status'] in ('BLOCKED','NOT_CONFIGURED','FAILED')]
        return {'capabilities':caps,'required_blockers':blockers,'status':'BLOCKED' if blockers else 'AVAILABLE'}
