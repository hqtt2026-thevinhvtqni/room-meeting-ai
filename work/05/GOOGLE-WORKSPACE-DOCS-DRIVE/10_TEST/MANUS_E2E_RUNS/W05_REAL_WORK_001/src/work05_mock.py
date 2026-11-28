"""Work 05 mock vertical slice: interface -> Core -> adapter -> local store.
No Google credentials or external calls are used.
"""
from dataclasses import dataclass, field
from threading import Lock
from typing import Dict
class DomainError(Exception): pass
class NotFound(DomainError): pass
class Conflict(DomainError): pass
class Unauthorized(DomainError): pass
class AdapterFailure(DomainError): pass
@dataclass
class Document:
    doc_id: str
    title: str
    content: str = ""
    revision: int = 0
    operations: set = field(default_factory=set)
class LocalWorkspaceAdapter:
    def __init__(self): self.docs: Dict[str, Document] = {}; self.fail_next = False
    def create(self, doc_id, title):
        if self.fail_next: self.fail_next=False; raise AdapterFailure('injected adapter failure')
        self.docs[doc_id] = Document(doc_id, title); return self.docs[doc_id]
    def read(self, doc_id):
        if doc_id not in self.docs: raise NotFound(doc_id)
        return self.docs[doc_id]
    def write(self, doc_id, expected_revision, op_id, mode, text):
        if self.fail_next: self.fail_next=False; raise AdapterFailure('injected adapter failure')
        d=self.read(doc_id)
        if op_id in d.operations: return d
        if expected_revision != d.revision: raise Conflict(f'expected {expected_revision}, actual {d.revision}')
        if mode == 'append': d.content += text
        elif mode == 'section_update':
            marker='[SECTION]'
            if marker not in d.content: raise DomainError('section marker missing')
            before, _, _after = d.content.partition(marker)
            d.content = before + marker + text
        else: raise DomainError('unsupported mode')
        d.revision += 1; d.operations.add(op_id); return d
class Core:
    def __init__(self, adapter): self.adapter=adapter; self.audit=[]; self.lock=Lock()
    def _auth(self, actor):
        if actor not in {'runner','editor'}: raise Unauthorized(actor)
    def create(self, actor, doc_id, title):
        self._auth(actor); d=self.adapter.create(doc_id,title); self.audit.append(('create',actor,doc_id,d.revision)); return self._view(d)
    def read(self, actor, doc_id):
        self._auth(actor); return self._view(self.adapter.read(doc_id))
    def write(self, actor, doc_id, expected_revision, op_id, mode, text):
        self._auth(actor)
        with self.lock:
            d=self.adapter.write(doc_id,expected_revision,op_id,mode,text)
            self.audit.append((mode,actor,doc_id,d.revision,op_id)); return self._view(d)
    @staticmethod
    def _view(d): return {'id':d.doc_id,'title':d.title,'content':d.content,'revision':d.revision}
class MCPInterface:
    def __init__(self, core): self.core=core
    def request(self, action, **p):
        if action == 'create': return self.core.create(**p)
        if action == 'read': return self.core.read(**p)
        if action in {'append','section_update'}:
            p['mode']=action; return self.core.write(**p)
        raise DomainError('invalid action')
