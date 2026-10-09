from __future__ import annotations
import json, os
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Callable
from urllib import error, request

@dataclass(frozen=True)
class BridgeResult:
    execution_id: str | None
    work_id: str | None
    status: str
    evidence_ref: str | None = None
    exit_code: int | None = None
    stdout_ref: str | None = None
    stderr_ref: str | None = None
    artifacts: list[str] | None = None
    blocker: str | None = None
    cleanup: dict[str, Any] | None = None
    provider_type: str = 'HTTP_EXECUTION_HOST'
    runtime_instance_id: str | None = None
    runtime_build_hash: str | None = None
    runtime_started_at: str | None = None
    runtime_pid: int | None = None
    runtime_platform: str | None = None
    runtime_bind_address: str | None = None
    raw: dict[str, Any] | None = None
    def as_dict(self): return asdict(self)

class ExecutionHostBridge:
    """Reusable WEE boundary adapter; it never invents WorkContext authority."""
    def __init__(self, endpoint: str | None = None, timeout: float = 30.0, transport: Callable[[str, bytes, float], tuple[int, bytes]] | None = None):
        self.endpoint=(endpoint or os.getenv('EXECUTION_HOST_URL','http://127.0.0.1:8031')).rstrip('/'); self.timeout=timeout; self.transport=transport or self._http_transport
    @staticmethod
    def _http_transport(url: str, body: bytes, timeout: float) -> tuple[int, bytes]:
        req=request.Request(url,data=body,headers={'Content-Type':'application/json','Accept':'application/json'},method='POST')
        with request.urlopen(req,timeout=timeout) as response: return response.status,response.read()
    @staticmethod
    def _to_dict(value: Any) -> dict[str, Any]:
        if isinstance(value,dict): return dict(value)
        if hasattr(value,'as_dict'): return value.as_dict()
        if is_dataclass(value): return asdict(value)
        raise TypeError('work_context_must_be_mapping_or_dataclass')
    def invoke(self,work_context: Any,execution_request: Any) -> BridgeResult:
        context=self._to_dict(work_context); run=self._to_dict(execution_request); required=('work_id','work_name','workspace_root','execution_workspace','evidence_root','authorized'); missing=[key for key in required if key not in context or context[key] in (None,'')]
        if missing: return BridgeResult(None,context.get('work_id'),'BLOCKED',blocker='missing_authoritative_context:'+','.join(missing))
        if context.get('authorized') is not True: return BridgeResult(None,context.get('work_id'),'BLOCKED',blocker='execution_not_authorized')
        body=json.dumps({'work_context':context,'execution_request':run},ensure_ascii=False,separators=(',',':')).encode()
        try:
            code,payload=self.transport(self.endpoint+'/execute',body,self.timeout); data=json.loads(payload.decode('utf-8'))
            if not isinstance(data,dict): return BridgeResult(None,context.get('work_id'),'BLOCKED',blocker='invalid_execution_host_response')
            result=data.get('result') if isinstance(data.get('result'),dict) else data; status=result.get('status','BLOCKED'); status='BLOCKED' if code < 200 or code >= 300 else status
            return BridgeResult(result.get('execution_id') or context.get('execution_id'),result.get('work_id') or context.get('work_id'),status,result.get('evidence_ref'),result.get('exit_code'),result.get('stdout_ref'),result.get('stderr_ref'),result.get('artifacts') or [],result.get('blocker') or (None if code < 300 else 'execution_host_http_'+str(code)),result.get('cleanup') or {},result.get('provider_type','HTTP_EXECUTION_HOST'),result.get('runtime_instance_id'),result.get('runtime_build_hash'),result.get('runtime_started_at'),result.get('runtime_pid'),result.get('runtime_platform'),result.get('runtime_bind_address'),data)
        except (TimeoutError,error.URLError,OSError) as exc: return BridgeResult(context.get('execution_id'),context.get('work_id'),'BLOCKED',blocker='execution_host_unreachable:'+type(exc).__name__,cleanup={'process_reaped':False})
        except (ValueError,UnicodeError) as exc: return BridgeResult(context.get('execution_id'),context.get('work_id'),'BLOCKED',blocker='invalid_execution_host_json:'+type(exc).__name__,cleanup={'process_reaped':False})

def execute_work(work_context: Any,execution_request: Any,*,endpoint: str|None=None,timeout: float=30.0,transport=None)->BridgeResult: return ExecutionHostBridge(endpoint,timeout,transport).invoke(work_context,execution_request)
