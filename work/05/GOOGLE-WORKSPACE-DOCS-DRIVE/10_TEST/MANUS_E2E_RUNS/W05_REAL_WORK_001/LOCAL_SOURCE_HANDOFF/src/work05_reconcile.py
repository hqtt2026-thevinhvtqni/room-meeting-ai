"""Change detection and reconciliation for Work 05.

Drive Changes reports resource changes, not character-level edits. For each
changed file this flow fetches current Docs state through the adapter, then
updates Core's canonical state and audit trail. It is provider-neutral and
safe to exercise offline with an injected change-feed stub.
"""
from typing import Protocol
from work05_mock import NotFound, AdapterFailure
class ChangeFeed(Protocol):
    def get_start_page_token(self, drive_id=None) -> str: ...
    def list_changes(self, page_token: str, drive_id=None) -> dict: ...
class Reconciler:
    def __init__(self, core, adapter, feed, drive_id=None): self.core=core; self.adapter=adapter; self.feed=feed; self.drive_id=drive_id
    def initial_token(self): return self.feed.get_start_page_token(self.drive_id)
    def poll_once(self, page_token):
        response=self.feed.list_changes(page_token, self.drive_id); results=[]
        for change in response.get('changes', []):
            event_id=str(change.get('id') or change.get('changeId') or f"{change.get('fileId')}:{change.get('time')}"); provider_id=change.get('fileId') or change.get('file',{}).get('id')
            if not provider_id: continue
            file_id=getattr(self.adapter, 'core_id_for_provider', lambda x: x)(provider_id)
            if change.get('removed') or change.get('file',{}).get('trashed'): results.append(self.core.reconcile_deleted(event_id, file_id)); continue
            try: view=self.adapter.read(file_id)
            except NotFound: results.append(self.core.reconcile_deleted(event_id, file_id)); continue
            results.append(self.core.reconcile_external(event_id, file_id, view))
        return {'results':results, 'next_page_token':response.get('nextPageToken'), 'new_start_page_token':response.get('newStartPageToken')}
class FakeChangeFeed:
    """Deterministic local feed used only for offline reconcile tests."""
    def __init__(self, pages): self.pages=dict(pages); self.calls=[]
    def get_start_page_token(self, drive_id=None): self.calls.append(('start',drive_id)); return 'token-0'
    def list_changes(self, page_token, drive_id=None): self.calls.append(('list',page_token,drive_id)); return self.pages.get(page_token, {'changes':[], 'newStartPageToken':page_token})
