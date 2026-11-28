import sys
import pytest
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_mock import Core
from work05_google_adapter import FakeGoogleProvider, GoogleWorkspaceAdapter
from work05_reconcile import FakeChangeFeed, Reconciler
from work05_real_provider import GoogleWorkspaceProvider
class Call:
    def __init__(self, value): self.value=value
    def execute(self): return self.value
class Changes:
    def __init__(self): self.calls=[]
    def getStartPageToken(self, **kwargs): self.calls.append(('start',kwargs)); return Call({'startPageToken':'t0'})
    def list(self, **kwargs): self.calls.append(('list',kwargs)); return Call({'changes':[{'id':'c1','fileId':'g-1','time':'now'}], 'nextPageToken':'t1', 'newStartPageToken':'t2'})
    def watch(self, **kwargs): self.calls.append(('watch',kwargs)); return Call({'id':'ch-1','resourceId':'res-1','expiration':'999'})
class Channels:
    def __init__(self): self.calls=[]
    def stop(self, **kwargs): self.calls.append(('stop',kwargs)); return Call({})
class Drive:
    def __init__(self): self.changes_service=Changes(); self.channels_service=Channels()
    def changes(self): return self.changes_service
    def channels(self): return self.channels_service
def test_g09_offline_change_fetch_reconcile_duplicate_and_audit():
    provider=FakeGoogleProvider(); adapter=GoogleWorkspaceAdapter(provider, 'folder'); core=Core(adapter); core.create('runner','core-1','Doc'); provider_id=adapter.core_to_provider['core-1']; provider.docs[provider_id].content='edited externally'; provider.docs[provider_id].revision=1
    feed=FakeChangeFeed({'t0':{'changes':[{'id':'change-1','fileId':provider_id,'time':'now'}], 'newStartPageToken':'t1'}}); reconciler=Reconciler(core, adapter, feed, drive_id='drive-1'); assert reconciler.initial_token()=='token-0'; first=reconciler.poll_once('t0'); second=reconciler.poll_once('t0')
    assert first['results'][0]['status']=='applied' and second['results'][0]['status']=='duplicate'; assert core.canonical['core-1']['content']=='edited externally'; assert [x for x in core.audit if x[0]=='reconcile']
def test_g09_offline_deleted_change_and_page_token():
    provider=FakeGoogleProvider(); adapter=GoogleWorkspaceAdapter(provider, 'folder'); core=Core(adapter); core.create('runner','core-1','Doc'); provider_id=adapter.core_to_provider['core-1']; feed=FakeChangeFeed({'t0':{'changes':[{'id':'delete-1','fileId':provider_id,'removed':True}], 'nextPageToken':'t1'}}); result=Reconciler(core, adapter, feed).poll_once('t0')
    assert result['next_page_token']=='t1' and result['results'][0]['status']=='applied' and 'core-1' not in core.canonical; assert any(x[0]=='reconcile_delete' for x in core.audit)
def test_real_provider_changes_and_watch_boundary_with_injected_drive():
    drive=Drive(); provider=GoogleWorkspaceProvider(None, drive, 'folder', drive_id='drive-1'); assert provider.get_start_page_token()=='t0'; listing=provider.list_changes('t0'); assert listing['nextPageToken']=='t1' and listing['newStartPageToken']=='t2'; watched=provider.watch_changes('t0','ch-1','https://example.invalid/hook','opaque','drive-1'); assert watched['resourceId']=='res-1'; provider.stop_channel('ch-1','res-1'); assert drive.changes_service.calls[0][0]=='start' and drive.channels_service.calls[0][0]=='stop'
