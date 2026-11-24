"""Fail-closed bounded raw-byte Sandbox upload engine.

Core authorization is injected and checked for every operation. No local grant
fallback exists. This is an engine component, not a deployed MCP registration.
"""
from __future__ import annotations
import hashlib, os, re, secrets, sqlite3, threading, time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

MAX_FILE_BYTES = 100 * 1024 * 1024
MAX_CHUNK_BYTES = 1024 * 1024
MAX_CHUNKS = 256
MAX_ACTIVE_PER_WORK = 2
_SHA = re.compile(r"^[0-9a-f]{64}$")
_WORK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")

class UploadError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message); self.code = code

@dataclass(frozen=True)
class UploadGrant:
    grant_id: str
    principal_id: str
    session_id: str
    canonical_work_id: str
    sandbox_work_id: str
    mapping_id: str
    mapping_version: int
    audience: str
    capability: str
    operations: frozenset[str]
    normalized_path: str
    max_file_bytes: int
    max_chunk_bytes: int
    max_chunks: int
    max_reserved_work_bytes: int
    max_active_uploads: int
    expires_at: float
    policy_version: str
    revocation_epoch: int

class CoreUploadAuthorizer(Protocol):
    def authorize_upload_operation(self, *, trusted_context: Any, operation: str,
        upload_id: str | None, destination: str | None,
        requested_bytes: int | None) -> UploadGrant: ...

class SQLiteUploadLedger:
    """Transactional durable session, chunk, quota and append-only audit store."""
    def __init__(self, path: str | os.PathLike):
        self.path=str(path); Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock()
        with self.db() as c:
            c.executescript("""
            PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;
            CREATE TABLE IF NOT EXISTS sessions(
              upload_id TEXT PRIMARY KEY, grant_id TEXT NOT NULL, principal_id TEXT NOT NULL,
              session_id TEXT NOT NULL, canonical_work_id TEXT NOT NULL, sandbox_work_id TEXT NOT NULL,
              mapping_id TEXT NOT NULL, mapping_version INTEGER NOT NULL, destination TEXT NOT NULL,
              expected_bytes INTEGER NOT NULL, expected_sha256 TEXT NOT NULL, chunk_size INTEGER NOT NULL,
              chunk_count INTEGER NOT NULL, received_bytes INTEGER NOT NULL DEFAULT 0,
              next_index INTEGER NOT NULL DEFAULT 0, state TEXT NOT NULL, staging_path TEXT NOT NULL,
              final_path TEXT NOT NULL, expires_at REAL NOT NULL, policy_version TEXT NOT NULL,
              revocation_epoch INTEGER NOT NULL, idempotency_key TEXT NOT NULL, created_at REAL NOT NULL,
              completed_sha256 TEXT);
            CREATE UNIQUE INDEX IF NOT EXISTS upload_idempotency
              ON sessions(principal_id,canonical_work_id,idempotency_key);
            CREATE TABLE IF NOT EXISTS chunks(
              upload_id TEXT NOT NULL, chunk_index INTEGER NOT NULL, byte_offset INTEGER NOT NULL,
              byte_length INTEGER NOT NULL, sha256 TEXT NOT NULL, PRIMARY KEY(upload_id,chunk_index));
            CREATE TABLE IF NOT EXISTS quota(
              canonical_work_id TEXT PRIMARY KEY, reserved_bytes INTEGER NOT NULL,
              active_uploads INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS audit(
              seq INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL, upload_id TEXT,
              work_id TEXT, principal_ref TEXT, destination TEXT, byte_count INTEGER,
              sha256 TEXT, outcome TEXT NOT NULL, at REAL NOT NULL);
            """)
    def db(self):
        c=sqlite3.connect(self.path,timeout=15,isolation_level=None)
        c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
    def by_key(self, principal: str, work: str, key: str):
        with self.db() as c:
            r=c.execute("SELECT * FROM sessions WHERE principal_id=? AND canonical_work_id=? AND idempotency_key=?",(principal,work,key)).fetchone()
            return dict(r) if r else None
    def begin(self,row:dict,max_bytes:int,max_active:int):
        with self.lock,self.db() as c:
            c.execute("BEGIN IMMEDIATE")
            q=c.execute("SELECT reserved_bytes,active_uploads FROM quota WHERE canonical_work_id=?",(row["canonical_work_id"],)).fetchone()
            reserved,active=(q[0],q[1]) if q else (0,0)
            if active>=max_active or reserved+row["expected_bytes"]>max_bytes:
                c.rollback(); raise UploadError("QUOTA_EXCEEDED","Work quota or concurrent upload limit exceeded")
            c.execute("INSERT INTO quota VALUES(?,?,?) ON CONFLICT(canonical_work_id) DO UPDATE SET reserved_bytes=excluded.reserved_bytes,active_uploads=excluded.active_uploads",
                (row["canonical_work_id"],reserved+row["expected_bytes"],active+1))
            c.execute("INSERT INTO sessions("+",".join(row)+") VALUES("+",".join("?" for _ in row)+")",tuple(row.values()))
            self.audit(c,"BEGIN_ACCEPTED",row,"PASS",0,row["expected_sha256"]); c.commit()
    @staticmethod
    def audit(c,event,row,outcome,count,digest):
        c.execute("INSERT INTO audit(event,upload_id,work_id,principal_ref,destination,byte_count,sha256,outcome,at) VALUES(?,?,?,?,?,?,?,?,?)",
            (event,row["upload_id"],row["canonical_work_id"],row["principal_id"],row["destination"],count,digest,outcome,time.time()))
    def get(self,uid):
        with self.db() as c:
            r=c.execute("SELECT * FROM sessions WHERE upload_id=?",(uid,)).fetchone()
            return dict(r) if r else None
    def get_chunk(self,uid,index):
        with self.db() as c:
            r=c.execute("SELECT byte_offset,byte_length,sha256 FROM chunks WHERE upload_id=? AND chunk_index=?",(uid,index)).fetchone()
            return tuple(r) if r else None
    def accept_chunk(self,uid,index,offset,length,digest):
        with self.lock,self.db() as c:
            c.execute("BEGIN IMMEDIATE"); row=c.execute("SELECT * FROM sessions WHERE upload_id=?",(uid,)).fetchone()
            if not row: c.rollback(); raise UploadError("NOT_FOUND","upload session not found")
            old=c.execute("SELECT * FROM chunks WHERE upload_id=? AND chunk_index=?",(uid,index)).fetchone()
            if old:
                same=(old["byte_offset"],old["byte_length"],old["sha256"])==(offset,length,digest)
                c.rollback()
                if same: return "REPLAY_IDENTICAL"
                raise UploadError("REPLAY_MISMATCH","chunk replay changed bytes or offset")
            if row["state"]!="UPLOADING" or index!=row["next_index"] or offset!=row["received_bytes"]:
                c.rollback(); raise UploadError("CHUNK_SEQUENCE","chunk must be the exact next contiguous range")
            if row["received_bytes"]+length>row["expected_bytes"]:
                c.rollback(); raise UploadError("SIZE_EXCEEDED","chunk exceeds declared file size")
            c.execute("INSERT INTO chunks VALUES(?,?,?,?,?)",(uid,index,offset,length,digest))
            c.execute("UPDATE sessions SET received_bytes=received_bytes+?,next_index=next_index+1 WHERE upload_id=?",(length,uid))
            self.audit(c,"CHUNK_ACCEPTED",dict(row),"PASS",length,digest); c.commit(); return "ACCEPTED"
    def transition(self,uid,old,new,outcome,digest=None):
        with self.lock,self.db() as c:
            c.execute("BEGIN IMMEDIATE"); r=c.execute("SELECT * FROM sessions WHERE upload_id=?",(uid,)).fetchone()
            if not r: c.rollback(); raise UploadError("NOT_FOUND","upload session not found")
            if r["state"]!=old: c.rollback(); raise UploadError("INVALID_STATE","upload state is not "+old)
            c.execute("UPDATE sessions SET state=?,completed_sha256=? WHERE upload_id=?",(new,digest,uid))
            self.audit(c,new,dict(r),outcome,r["received_bytes"],digest or r["expected_sha256"])
            if new in {"COMPLETED","ABORTED"}:
                c.execute("UPDATE quota SET reserved_bytes=MAX(0,reserved_bytes-?),active_uploads=MAX(0,active_uploads-1) WHERE canonical_work_id=?",(r["expected_bytes"],r["canonical_work_id"]))
            c.commit(); return self.get(uid)

class SandboxBinaryUploadService:
    """Upload raw bytes in bounded chunks; Core must authorize begin/chunk/finalize/abort."""
    def __init__(self, *, sandbox_root, ledger:SQLiteUploadLedger,
                 authorizer:CoreUploadAuthorizer|None, audience:str):
        self.root=Path(sandbox_root).resolve(); self.root.mkdir(parents=True,exist_ok=True)
        self.ledger=ledger; self.authorizer=authorizer; self.audience=audience
        self.lock=threading.RLock()
    def grant(self,ctx,op,uid,path,size):
        if self.authorizer is None: raise UploadError("AUTHORITY_UNAVAILABLE","Core upload authority is not configured")
        try: g=self.authorizer.authorize_upload_operation(trusted_context=ctx,operation=op,upload_id=uid,destination=path,requested_bytes=size)
        except Exception as e: raise UploadError("AUTHORITY_BLOCKED","Core authorization failed closed") from e
        if not isinstance(g,UploadGrant) or g.audience!=self.audience or g.capability!="sandbox.file.upload" or op not in g.operations or g.expires_at<=time.time():
            raise UploadError("INVALID_GRANT","Core returned an invalid, expired or out-of-scope grant")
        if (not g.grant_id or not g.principal_id or not g.session_id or not g.mapping_id or g.mapping_version<1
            or not g.canonical_work_id.startswith("W") or not _WORK.fullmatch(g.sandbox_work_id)
            or not g.policy_version or not 0<g.max_file_bytes<=MAX_FILE_BYTES
            or not 0<g.max_chunk_bytes<=MAX_CHUNK_BYTES or not 0<g.max_chunks<=MAX_CHUNKS
            or g.max_reserved_work_bytes<=0 or not 0<g.max_active_uploads<=MAX_ACTIVE_PER_WORK):
            raise UploadError("INVALID_GRANT","Core grant violates the versioned upload limits")
        return g
    @staticmethod
    def path(value):
        if not isinstance(value,str) or not value or len(value)>1024 or "\0" in value or "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:",value):
            raise UploadError("INVALID_PATH","destination must be a relative POSIX path")
        parts=value.split("/")
        if any(p in {"",".",".."} or ":" in p for p in parts): raise UploadError("INVALID_PATH","invalid destination segment")
        return "/".join(parts)
    def work_root(self,work):
        if not _WORK.fullmatch(work): raise UploadError("INVALID_WORK","invalid Sandbox Work ID")
        p=(self.root/work).resolve()
        if p.parent!=self.root: raise UploadError("PATH_ESCAPE","Work root escaped Sandbox root")
        p.mkdir(parents=True,exist_ok=True); return p
    @staticmethod
    def no_symlinks(root,target):
        for part in target.relative_to(root).parts:
            root=root/part
            if root.is_symlink(): raise UploadError("SYMLINK_DENIED","symlink path component denied")
    def begin(self,*,trusted_context,canonical_work_id,sandbox_work_id,destination,expected_bytes,expected_sha256,chunk_size,idempotency_key):
        path=self.path(destination)
        if isinstance(expected_bytes,bool) or not isinstance(expected_bytes,int) or not 0<=expected_bytes<=MAX_FILE_BYTES: raise UploadError("INVALID_SIZE","file size outside bound")
        if not isinstance(expected_sha256,str) or not _SHA.fullmatch(expected_sha256): raise UploadError("INVALID_DIGEST","expected SHA-256 must be lowercase hex")
        if isinstance(chunk_size,bool) or not isinstance(chunk_size,int) or not 1<=chunk_size<=MAX_CHUNK_BYTES: raise UploadError("INVALID_CHUNK_SIZE","chunk size outside bound")
        if not isinstance(idempotency_key,str) or not 16<=len(idempotency_key)<=128: raise UploadError("INVALID_IDEMPOTENCY_KEY","idempotency key must be 16-128 chars")
        g=self.grant(trusted_context,"begin",None,path,expected_bytes)
        if (g.canonical_work_id!=canonical_work_id or g.sandbox_work_id!=sandbox_work_id or g.normalized_path!=path
            or expected_bytes>g.max_file_bytes or chunk_size>g.max_chunk_bytes): raise UploadError("GRANT_SCOPE_MISMATCH","request exceeds Core grant scope")
        old=self.ledger.by_key(g.principal_id,g.canonical_work_id,idempotency_key)
        if old:
            same=(old["destination"],old["expected_bytes"],old["expected_sha256"])==(path,expected_bytes,expected_sha256)
            if not same: raise UploadError("IDEMPOTENCY_CONFLICT","idempotency key reused with different content or scope")
            return {"upload_id":old["upload_id"],"state":old["state"],"chunk_size":old["chunk_size"],"chunk_count":old["chunk_count"]}
        chunks=0 if expected_bytes==0 else (expected_bytes+chunk_size-1)//chunk_size
        if chunks>g.max_chunks: raise UploadError("CHUNK_LIMIT","too many chunks")
        root=self.work_root(g.sandbox_work_id); final=root/path; self.no_symlinks(root,final)
        if final.exists(): raise UploadError("ALREADY_EXISTS","destination exists; overwrite denied")
        staging_dir=root/".upload-staging"; staging_dir.mkdir(mode=0o700,exist_ok=True)
        uid="UP-"+secrets.token_urlsafe(18); staging=staging_dir/(uid+".part")
        fd=os.open(staging,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600); os.close(fd)
        row={"upload_id":uid,"grant_id":g.grant_id,"principal_id":g.principal_id,"session_id":g.session_id,
          "canonical_work_id":g.canonical_work_id,"sandbox_work_id":g.sandbox_work_id,"mapping_id":g.mapping_id,
          "mapping_version":g.mapping_version,"destination":path,"expected_bytes":expected_bytes,"expected_sha256":expected_sha256,
          "chunk_size":chunk_size,"chunk_count":chunks,"state":"UPLOADING","staging_path":str(staging),"final_path":str(final),
          "expires_at":g.expires_at,"policy_version":g.policy_version,"revocation_epoch":g.revocation_epoch,
          "idempotency_key":idempotency_key,"created_at":time.time()}
        try: self.ledger.begin(row,max_bytes=g.max_reserved_work_bytes,max_active=g.max_active_uploads)
        except Exception:
            try: staging.unlink()
            except OSError: pass
            raise
        return {"upload_id":uid,"state":"UPLOADING","chunk_size":chunk_size,"chunk_count":chunks}
    @staticmethod
    def match(g,row):
        pairs=((g.grant_id,row["grant_id"]),(g.principal_id,row["principal_id"]),(g.session_id,row["session_id"]),
          (g.canonical_work_id,row["canonical_work_id"]),(g.sandbox_work_id,row["sandbox_work_id"]),
          (g.mapping_id,row["mapping_id"]),(g.mapping_version,row["mapping_version"]),
          (g.normalized_path,row["destination"]),(g.policy_version,row["policy_version"]),(g.revocation_epoch,row["revocation_epoch"]))
        if any(a!=b for a,b in pairs) or row["expires_at"]<=time.time(): raise UploadError("SESSION_BINDING_MISMATCH","Core grant no longer matches upload session")
    def chunk(self,*,trusted_context,upload_id,index,offset,data:bytes):
        if not isinstance(data,bytes) or not data or len(data)>MAX_CHUNK_BYTES: raise UploadError("INVALID_CHUNK","chunk must be 1..1MiB raw bytes")
        if isinstance(index,bool) or not isinstance(index,int) or index<0 or isinstance(offset,bool) or not isinstance(offset,int) or offset<0: raise UploadError("INVALID_OFFSET","chunk index and offset must be non-negative integers")
        row=self.ledger.get(upload_id)
        if not row: raise UploadError("NOT_FOUND","upload session not found")
        g=self.grant(trusted_context,"chunk",upload_id,row["destination"],row["expected_bytes"]); self.match(g,row)
        if len(data)>g.max_chunk_bytes or index>=g.max_chunks: raise UploadError("CHUNK_LIMIT","chunk exceeds Core grant")
        digest=hashlib.sha256(data).hexdigest()
        if index<row["next_index"]:
            old=self.ledger.get_chunk(upload_id,index)
            if old==(offset,len(data),digest):
                return {"upload_id":upload_id,"index":index,"status":"ALREADY_ACCEPTED","sha256":digest}
            raise UploadError("REPLAY_MISMATCH","chunk retry does not match the accepted bytes")
        if row["state"]!="UPLOADING" or index!=row["next_index"] or offset!=row["received_bytes"]:
            raise UploadError("CHUNK_SEQUENCE","chunk must be the exact next contiguous range")
        if offset+len(data)>row["expected_bytes"]:
            raise UploadError("SIZE_EXCEEDED","chunk exceeds declared file size")
        path=Path(row["staging_path"])
        with self.lock:
            with open(path,"r+b",buffering=0) as f:
                f.seek(offset); f.write(data); f.flush(); os.fsync(f.fileno())
            self.ledger.accept_chunk(upload_id,index,offset,len(data),digest)
        return {"upload_id":upload_id,"index":index,"status":"ACCEPTED","bytes":len(data),"sha256":digest}
    def finalize(self,*,trusted_context,upload_id):
        row=self.ledger.get(upload_id)
        if not row: raise UploadError("NOT_FOUND","upload session not found")
        g=self.grant(trusted_context,"finalize",upload_id,row["destination"],row["expected_bytes"]); self.match(g,row)
        if row["state"]=="COMPLETED":
            final=Path(row["final_path"]); h=hashlib.sha256(); size=0
            with open(final,"rb") as f:
                for b in iter(lambda:f.read(1024*1024),b""): size+=len(b); h.update(b)
            if size!=row["expected_bytes"] or h.hexdigest()!=row["completed_sha256"]:
                raise UploadError("READBACK_MISMATCH","completed upload no longer matches its durable receipt")
            return {"upload_id":upload_id,"status":"COMPLETED","path":row["destination"],"bytes":size,"sha256":h.hexdigest(),"readback_verified":True}
        if row["received_bytes"]!=row["expected_bytes"] or row["next_index"]!=row["chunk_count"]: raise UploadError("INCOMPLETE_UPLOAD","byte coverage is incomplete")
        root=self.work_root(row["sandbox_work_id"]); staging=Path(row["staging_path"]); final=Path(row["final_path"])
        self.no_symlinks(root,final); h=hashlib.sha256()
        with open(staging,"rb") as f:
            for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
        digest=h.hexdigest()
        if digest!=row["expected_sha256"]: raise UploadError("CHECKSUM_MISMATCH","full-file SHA-256 mismatch")
        self.ledger.transition(upload_id,"UPLOADING","FINALIZING","FINALIZE_STARTED",digest)
        final.parent.mkdir(parents=True,exist_ok=True); self.no_symlinks(root,final)
        try: os.link(staging,final)
        except FileExistsError: raise UploadError("ALREADY_EXISTS","destination appeared during upload")
        except OSError as e: raise UploadError("PROMOTION_BLOCKED","atomic no-replace promotion unavailable") from e
        h=hashlib.sha256(); size=0
        with open(final,"rb") as f:
            for b in iter(lambda:f.read(1024*1024),b""): size+=len(b); h.update(b)
        if size!=row["expected_bytes"] or h.hexdigest()!=digest:
            try: final.unlink()
            except OSError: pass
            raise UploadError("READBACK_MISMATCH","final file readback mismatch")
        try: staging.unlink()
        except OSError as e:
            try: final.unlink()
            except OSError: pass
            raise UploadError("CLEANUP_BLOCKED","staging cleanup could not be verified") from e
        try:
            self.ledger.transition(upload_id,"FINALIZING","COMPLETED","PASS",digest)
        except Exception as e:
            try: final.unlink()
            except OSError: pass
            raise UploadError("AUDIT_BLOCKED","completion audit could not be committed") from e
        return {"upload_id":upload_id,"status":"COMPLETED","path":row["destination"],"bytes":size,"sha256":digest,"readback_verified":True}
    def abort(self,*,trusted_context,upload_id):
        row=self.ledger.get(upload_id)
        if not row: raise UploadError("NOT_FOUND","upload session not found")
        g=self.grant(trusted_context,"abort",upload_id,row["destination"],row["expected_bytes"]); self.match(g,row)
        if row["state"]=="ABORTED": return {"upload_id":upload_id,"status":"ABORTED","cleanup_verified":True}
        try: Path(row["staging_path"]).unlink(missing_ok=True)
        except OSError as e: raise UploadError("CLEANUP_BLOCKED","staging cleanup not verified") from e
        self.ledger.transition(upload_id,"UPLOADING","ABORTED","PASS")
        return {"upload_id":upload_id,"status":"ABORTED","cleanup_verified":True}
