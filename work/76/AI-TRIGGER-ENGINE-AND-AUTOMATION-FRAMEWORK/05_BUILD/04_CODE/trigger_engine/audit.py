"""Audit record contract and fail-closed writer; sink durability is external."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Protocol,Any
from .models import canonical_json

class AuditUnavailable(RuntimeError): pass

@dataclass(frozen=True)
class AuditRecord:
    record_id:str; work_id:str; actor_ref:str; action:str; outcome:str; correlation_id:str
    occurred_at:datetime; payload_digest:str; previous_hash:str=""; record_hash:str=""

class AppendOnlyAuditSink(Protocol):
    def append(self,record:AuditRecord)->None: ...

class AuditWriter:
    def __init__(self,sink:AppendOnlyAuditSink|None):
        self._sink=sink
        self._head=""

    def write(self,*,record_id:str,work_id:str,actor_ref:str,action:str,outcome:str,correlation_id:str,payload:Any)->AuditRecord:
        if self._sink is None:
            raise AuditUnavailable("audit persistence unavailable; protected operation fails closed")
        if not all(isinstance(v,str) and v.strip() for v in (record_id,work_id,actor_ref,action,outcome,correlation_id)):
            raise ValueError("audit identity/scope/action/outcome/correlation required")

        # Reuse the engine's strict canonical JSON: sorted keys, compact UTF-8,
        # and rejection of NaN/Infinity. Non-canonical payloads must not enter
        # the audit chain with implementation-dependent digests.
        payload_json=canonical_json(payload)
        digest=hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        occurred=datetime.now(timezone.utc)
        base={"record_id":record_id,"work_id":work_id,"actor_ref":actor_ref,"action":action,"outcome":outcome,
              "correlation_id":correlation_id,"occurred_at":occurred.isoformat(),"payload_digest":digest,"previous_hash":self._head}
        record_hash=hashlib.sha256(canonical_json(base).encode("utf-8")).hexdigest()
        record=AuditRecord(record_id,work_id,actor_ref,action,outcome,correlation_id,occurred,digest,self._head,record_hash)
        try:
            self._sink.append(record)
        except Exception as exc:
            raise AuditUnavailable("audit append failed; protected operation fails closed") from exc
        self._head=record_hash
        return record
