"""Provider-neutral Google Docs/Drive adapter contract for Work 05.

No Google SDK calls are made here. GoogleWorkspaceAdapter translates Core
operations to a narrow provider contract; FakeGoogleProvider supplies a
fully deterministic local implementation for contract and recovery tests.
"""
from dataclasses import dataclass, field
from typing import Dict, Protocol, Optional
from work05_mock import Conflict, NotFound, AdapterFailure
class ProviderError(Exception):
    def __init__(self, code: str, message: str): super().__init__(message); self.code = code
class WorkspaceProvider(Protocol):
    def create_document(self, title: str, parent_id: Optional[str] = None) -> dict: ...
    def get_document(self, document_id: str) -> dict: ...
    def batch_update(self, document_id: str, requests: list, required_revision: int) -> dict: ...
    def get_change_state(self, document_id: str) -> dict: ...
@dataclass
class FakeDoc:
    document_id: str
    title: str
    content: str = ""
    revision: int = 0
    applied_operations: set = field(default_factory=set)
class FakeGoogleProvider:
    """Local provider with Google-like document/revision semantics."""
    def __init__(self): self.docs: Dict[str, FakeDoc] = {}; self.next_id = 1; self.fail_next = None; self.calls = []
    def _maybe_fail(self):
        if self.fail_next:
            code = self.fail_next; self.fail_next = None; raise ProviderError(code, f'injected provider failure: {code}')
    def create_document(self, title, parent_id=None):
        self._maybe_fail(); doc_id = f'fake-doc-{self.next_id}'; self.next_id += 1; self.docs[doc_id] = FakeDoc(doc_id, title); self.calls.append(('create_document', doc_id, parent_id)); return self.get_document(doc_id)
    def get_document(self, document_id):
        self._maybe_fail()
        if document_id not in self.docs: raise ProviderError('NOT_FOUND', document_id)
        d = self.docs[document_id]; self.calls.append(('get_document', document_id)); return {'documentId': d.document_id, 'title': d.title, 'content': d.content, 'revision': d.revision}
    def batch_update(self, document_id, requests, required_revision):
        self._maybe_fail()
        if document_id not in self.docs: raise ProviderError('NOT_FOUND', document_id)
        d = self.docs[document_id]
        if all(req['operationId'] in d.applied_operations for req in requests): return self.get_document(document_id)
        if required_revision != d.revision: raise ProviderError('ABORTED', f'expected {required_revision}, actual {d.revision}')
        for req in requests:
            op_id = req['operationId']
            if op_id in d.applied_operations: continue
            mode, text = req['mode'], req['text']
            if mode == 'append': d.content += text
            elif mode == 'section_update':
                marker = '[SECTION]'
                if marker not in d.content: raise ProviderError('INVALID_ARGUMENT', 'section marker missing')
                before, _, _ = d.content.partition(marker); d.content = before + marker + text
            else: raise ProviderError('INVALID_ARGUMENT', mode)
            d.applied_operations.add(op_id); d.revision += 1
        self.calls.append(('batch_update', document_id, required_revision, len(requests))); return self.get_document(document_id)
    def get_change_state(self, document_id):
        if document_id not in self.docs: raise ProviderError('NOT_FOUND', document_id)
        d = self.docs[document_id]; return {'documentId': document_id, 'revision': d.revision}
class GoogleWorkspaceAdapter:
    """Narrow adapter translating Core IDs and semantics to WorkspaceProvider."""
    def __init__(self, provider: WorkspaceProvider, parent_id: Optional[str] = None): self.provider = provider; self.parent_id = parent_id; self.core_to_provider = {}; self.provider_to_core = {}
    @staticmethod
    def _normalize(raw): return {'id': raw['documentId'], 'title': raw['title'], 'content': raw['content'], 'revision': raw['revision']}
    def _provider_id(self, core_id): return self.core_to_provider.get(core_id, core_id)
    def create(self, doc_id, title):
        try:
            result = self._normalize(self.provider.create_document(title, self.parent_id)); self.core_to_provider[doc_id] = result['id']; self.provider_to_core[result['id']] = doc_id; return {**result, 'id': doc_id}
        except ProviderError as exc: raise AdapterFailure(f'{exc.code}: {exc}') from exc
    def core_id_for_provider(self, provider_id): return self.provider_to_core.get(provider_id, provider_id)
    def read(self, doc_id):
        try:
            raw = self.provider.get_document(self._provider_id(doc_id)); result = self._normalize(raw); return {**result, 'id': doc_id}
        except ProviderError as exc:
            if exc.code == 'NOT_FOUND': raise NotFound(doc_id) from exc
            raise AdapterFailure(f'{exc.code}: {exc}') from exc
    def write(self, doc_id, expected_revision, op_id, mode, text):
        try:
            raw = self.provider.batch_update(self._provider_id(doc_id), [{'operationId': op_id, 'mode': mode, 'text': text}], expected_revision); result = self._normalize(raw); return {**result, 'id': doc_id}
        except ProviderError as exc:
            if exc.code == 'ABORTED': raise Conflict(str(exc)) from exc
            if exc.code == 'NOT_FOUND': raise NotFound(doc_id) from exc
            raise AdapterFailure(f'{exc.code}: {exc}') from exc
    def change_state(self, doc_id):
        try: return self.provider.get_change_state(self._provider_id(doc_id))
        except ProviderError as exc:
            if exc.code == 'NOT_FOUND': raise NotFound(doc_id) from exc
            raise AdapterFailure(f'{exc.code}: {exc}') from exc
