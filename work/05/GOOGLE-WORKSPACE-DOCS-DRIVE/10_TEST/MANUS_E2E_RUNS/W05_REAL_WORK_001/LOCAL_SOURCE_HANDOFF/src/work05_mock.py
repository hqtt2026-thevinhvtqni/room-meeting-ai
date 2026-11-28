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
    """Adapter contract standing in for Google Docs/Drive; persistence is local."""
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
            before, _, _after = d.content.partition(marker); d.content = before + marker + text
        else: raise DomainError('unsupported mode')
        d.revision += 1; d.operations.add(op_id); return d
class Core:
    """Single source of truth for business semantics and reconciled canonical state."""
    def __init__(self, adapter): self.adapter=adapter; self.audit=[]; self.canonical={}; self.reconciled_events=set(); self.lock=Lock()
    def _auth(self, actor):
        if actor not in {'runner','editor'}: raise Unauthorized(actor)
    def create(self, actor, doc_id, title):
        self._auth(actor); d=self.adapter.create(doc_id,title); view=self._view(d, doc_id); self.canonical[doc_id]=view; self.audit.append(('create',actor,doc_id,self._revision(d))); return view
    def read(self, actor, doc_id):
        self._auth(actor); return self._view(self.adapter.read(doc_id), doc_id)
    def write(self, actor, doc_id, expected_revision, op_id, mode, text):
        self._auth(actor)
        with self.lock:
            d=self.adapter.write(doc_id,expected_revision,op_id,mode,text); view=self._view(d, doc_id); self.canonical[doc_id]=view
            self.audit.append((mode,actor,doc_id,self._revision(d),op_id)); return view
    def reconcile_external(self, event_id, doc_id, view, source='google_changes'):
        """Apply one externally observed projection into canonical state idempotently."""
        with self.lock:
            if event_id in self.reconciled_events: return {'status':'duplicate','event_id':event_id,'document':self.canonical.get(doc_id, view)}
            self.reconciled_events.add(event_id); self.canonical[doc_id]=dict(view)
            self.audit.append(('reconcile',source,doc_id,view.get('revision'),event_id)); return {'status':'applied','event_id':event_id,'document':self.canonical[doc_id]}
    def reconcile_deleted(self, event_id, doc_id, source='google_changes'):
        with self.lock:
            if event_id in self.reconciled_events: return {'status':'duplicate','event_id':event_id,'document':self.canonical.get(doc_id)}
            self.reconciled_events.add(event_id); self.canonical.pop(doc_id,None); self.audit.append(('reconcile_delete',source,doc_id,event_id)); return {'status':'applied','event_id':event_id,'document':None}
    @staticmethod
    def _get(d, name, fallback=None): return d.get(name, fallback) if isinstance(d, dict) else getattr(d, name, fallback)
    @classmethod
    def _revision(cls, d): return cls._get(d, 'revision', 0)
    @classmethod
    def _view(cls, d, fallback_id=None):
        return {'id':cls._get(d,'id',cls._get(d,'doc_id',fallback_id)), 'title':cls._get(d,'title'), 'content':cls._get(d,'content',''), 'revision':cls._revision(d)}
class MCPInterface:
    """Thin interface layer: validates request and delegates to Core; no storage access."""
    def __init__(self, core): self.core=core
    def request(self, action, **p):
        if action == 'create': return self.core.create(**p)
        if action == 'read': return self.core.read(**p)
        if action in {'append','section_update'}:
            p['mode']=action; return self.core.write(**p)
        raise DomainError('invalid action')
