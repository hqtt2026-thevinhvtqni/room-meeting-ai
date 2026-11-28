"""Lazy real Google Docs/Drive provider boundary for Work 05.

The module does not authenticate or call Google at import time. It validates
configuration first, accepts injected services for offline tests, and only
constructs Google clients when explicitly requested by the caller.
"""
from dataclasses import dataclass
import os
from pathlib import Path
from work05_google_adapter import ProviderError
@dataclass(frozen=True)
class GoogleConfig:
    credentials_file: str
    scopes: tuple[str, ...]
    parent_id: str
    project_mode: str = 'test'
    drive_id: str = ''
    @classmethod
    def from_env(cls, environ=None):
        env = environ or os.environ; scopes=tuple(x.strip() for x in env.get('W05_GOOGLE_SCOPES','').split(',') if x.strip()); return cls(env.get('W05_GOOGLE_CREDENTIALS_FILE',''), scopes, env.get('W05_GOOGLE_PARENT_ID',''), env.get('W05_GOOGLE_MODE','test'), env.get('W05_GOOGLE_DRIVE_ID',''))
def validate_config(config: GoogleConfig):
    errors=[]
    if not config.credentials_file: errors.append('W05_GOOGLE_CREDENTIALS_FILE missing')
    elif not Path(config.credentials_file).is_file(): errors.append('credentials file does not exist')
    if not config.scopes: errors.append('W05_GOOGLE_SCOPES missing')
    if not config.parent_id: errors.append('W05_GOOGLE_PARENT_ID missing')
    if config.project_mode not in {'test','development','production'}: errors.append('W05_GOOGLE_MODE invalid')
    return {'ready':not errors,'errors':errors,'credentials_present':bool(config.credentials_file and Path(config.credentials_file).is_file()),'scope_count':len(config.scopes),'parent_configured':bool(config.parent_id),'drive_id_configured':bool(config.drive_id)}
def build_google_services(config: GoogleConfig):
    result=validate_config(config)
    if not result['ready']: raise ProviderError('CONFIG_INVALID','; '.join(result['errors']))
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc: raise ProviderError('DEPENDENCY_MISSING','google-auth/google-api-python-client required') from exc
    credentials=Credentials.from_service_account_file(config.credentials_file, scopes=list(config.scopes)); return build('docs','v1',credentials=credentials), build('drive','v3',credentials=credentials)
def _text_and_end(document):
    parts=[]
    for item in document.get('body',{}).get('content',[]):
        for elem in item.get('paragraph',{}).get('elements',[]):
            content=elem.get('textRun',{}).get('content')
            if content: parts.append(content)
    text=''.join(parts); return text, max(1, document.get('body',{}).get('content',[{}])[-1].get('endIndex',1)-1)
class GoogleWorkspaceProvider:
    """WorkspaceProvider plus explicit Drive change/watch boundary."""
    def __init__(self, docs_service, drive_service, parent_id, drive_id=''): self.docs=docs_service; self.drive=drive_service; self.parent_id=parent_id; self.drive_id=drive_id
    def create_document(self, title, parent_id=None):
        created=self.docs.documents().create(body={'title':title}).execute(); document_id=created['documentId']; target=parent_id or self.parent_id
        if target: self.drive.files().update(fileId=document_id, addParents=target, fields='id,parents').execute()
        return self.get_document(document_id)
    def get_document(self, document_id):
        raw=self.docs.documents().get(documentId=document_id).execute(); text,_=_text_and_end(raw); return {'documentId':document_id,'title':raw.get('title',''),'content':text,'revision':raw.get('revisionId','')}
    def batch_update(self, document_id, requests, required_revision):
        current=self.docs.documents().get(documentId=document_id).execute(); text,end_index=_text_and_end(current); converted=[]
        for req in requests:
            mode,value=req['mode'],req['text']
            if mode=='append': converted.append({'insertText':{'location':{'index':end_index},'text':value}})
            elif mode=='section_update':
                marker='[SECTION]'; marker_index=text.find(marker)
                if marker_index<0: raise ProviderError('INVALID_ARGUMENT','section marker missing')
                start=marker_index+len(marker); end=len(text.rstrip('\n')); converted.extend([{'deleteContentRange':{'range':{'startIndex':start+1,'endIndex':end+1}}},{'insertText':{'location':{'index':start+1},'text':value}}])
            else: raise ProviderError('INVALID_ARGUMENT',mode)
        try: self.docs.documents().batchUpdate(documentId=document_id,body={'requests':converted,'writeControl':{'requiredRevisionId':required_revision}}).execute()
        except Exception as exc: raise ProviderError('API_ERROR',str(exc)) from exc
        return self.get_document(document_id)
    def get_change_state(self, document_id):
        raw=self.docs.documents().get(documentId=document_id,fields='documentId,revisionId').execute(); return {'documentId':document_id,'revision':raw.get('revisionId','')}
    def get_start_page_token(self, drive_id=None):
        try: return self.drive.changes().getStartPageToken(driveId=drive_id or self.drive_id, supportsAllDrives=True).execute()['startPageToken']
        except Exception as exc: raise ProviderError('API_ERROR',str(exc)) from exc
    def list_changes(self, page_token, drive_id=None):
        try: return self.drive.changes().list(pageToken=page_token, driveId=drive_id or self.drive_id, spaces='drive', includeItemsFromAllDrives=True, supportsAllDrives=True, fields='changes(id,fileId,removed,time,file(id,name,mimeType,trashed,modifiedTime,driveId)),nextPageToken,newStartPageToken').execute()
        except Exception as exc: raise ProviderError('API_ERROR',str(exc)) from exc
    def watch_changes(self, page_token, channel_id, webhook_address, token=None, drive_id=None):
        body={'id':channel_id,'type':'web_hook','address':webhook_address}
        if token: body['token']=token
        try: return self.drive.changes().watch(pageToken=page_token,driveId=drive_id or self.drive_id,supportsAllDrives=True,body=body).execute()
        except Exception as exc: raise ProviderError('API_ERROR',str(exc)) from exc
    def stop_channel(self, channel_id, resource_id):
        try: return self.drive.channels().stop(body={'id':channel_id,'resourceId':resource_id}).execute()
        except Exception as exc: raise ProviderError('API_ERROR',str(exc)) from exc
