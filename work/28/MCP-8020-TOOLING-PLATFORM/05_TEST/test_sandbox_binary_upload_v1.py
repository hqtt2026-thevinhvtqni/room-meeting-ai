"""Component tests for the Work 28 binary upload engine; Fake Core is not live evidence."""
import hashlib, tempfile, unittest, zipfile, threading
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from sandbox_binary_upload_v1 import UploadError, UploadGrant, SQLiteUploadLedger, SandboxBinaryUploadService

class FakeCore:
    def __init__(self):
        self.calls=[]; self.path="images/photo.png"
    def authorize_upload_operation(self, *, trusted_context, operation, upload_id, destination, requested_bytes):
        if trusted_context!="trusted-test-context": raise PermissionError("untrusted context")
        self.calls.append(operation)
        return UploadGrant(
          grant_id="G-TEST",principal_id="agent-test",session_id="S-TEST",
          canonical_work_id="W119",sandbox_work_id="119",mapping_id="MAP-TEST",mapping_version=1,
          audience="build-sandbox-test",capability="sandbox.file.upload",
          operations=frozenset({"begin","chunk","finalize","abort"}),normalized_path=self.path,
          max_file_bytes=100_000_000,max_chunk_bytes=1_048_576,max_chunks=256,
          max_reserved_work_bytes=500_000_000,max_active_uploads=2,
          expires_at=4_000_000_000,policy_version="test-policy-v1",revocation_epoch=1)

class BinaryUploadTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)/"sandbox"
        self.ledger=SQLiteUploadLedger(Path(self.tmp.name)/"ledger.sqlite3"); self.core=FakeCore()
        self.service=SandboxBinaryUploadService(sandbox_root=self.root,ledger=self.ledger,authorizer=self.core,audience="build-sandbox-test")
        self.ctx="trusted-test-context"; (self.root/"119"/"images").mkdir(parents=True)
    def tearDown(self): self.tmp.cleanup()
    def roundtrip(self,data):
        digest=hashlib.sha256(data).hexdigest()
        started=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",
          destination="images/photo.png",expected_bytes=len(data),expected_sha256=digest,chunk_size=4096,idempotency_key="idempotency-key-0001")
        uid=started["upload_id"]
        for i,off in enumerate(range(0,len(data),4096)):
            self.service.chunk(trusted_context=self.ctx,upload_id=uid,index=i,offset=off,data=data[off:off+4096])
        result=self.service.finalize(trusted_context=self.ctx,upload_id=uid)
        self.assertEqual((self.root/"119"/"images"/"photo.png").read_bytes(),data)
        self.assertEqual(result["sha256"],digest); self.assertTrue(result["readback_verified"])
        self.assertEqual(self.ledger.get(uid)["state"],"COMPLETED")
    def test_png_and_arbitrary_binary_roundtrip(self): self.roundtrip(b"\x89PNG\r\n\x1a\n"+bytes(range(256))*80)
    def test_invalid_utf8_roundtrip(self): self.roundtrip(bytes([0,255,254,128,192,193])*700)
    def test_zip_roundtrip(self):
        b=BytesIO()
        with zipfile.ZipFile(b,"w") as z: z.writestr("hello.txt","ROOM-HOP binary")
        self.roundtrip(b.getvalue())
    def test_zero_byte_roundtrip(self): self.roundtrip(b"")
    def test_missing_core_authority_fails_closed(self):
        s=SandboxBinaryUploadService(sandbox_root=self.root,ledger=self.ledger,authorizer=None,audience="build-sandbox-test")
        with self.assertRaises(UploadError) as e:
            s.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/x",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0002")
        self.assertEqual(e.exception.code,"AUTHORITY_UNAVAILABLE")
    def test_untrusted_context_denied(self):
        with self.assertRaises(UploadError):
            self.service.begin(trusted_context="caller-spoof",canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0003")
    def test_wrong_work_mapping_denied(self):
        with self.assertRaises(UploadError) as e:
            self.service.begin(trusted_context=self.ctx,canonical_work_id="W28",sandbox_work_id="28",destination="images/photo.png",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0004")
        self.assertEqual(e.exception.code,"GRANT_SCOPE_MISMATCH")
    def test_path_traversal_denied(self):
        with self.assertRaises(UploadError):
            self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="../escape",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0005")
    def test_symlink_escape_denied(self):
        outside=Path(self.tmp.name)/"outside"; outside.mkdir()
        (self.root/"119"/"images"/"link").symlink_to(outside,target_is_directory=True); self.core.path="images/link/file"
        with self.assertRaises(UploadError) as e:
            self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/link/file",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0006")
        self.assertEqual(e.exception.code,"SYMLINK_DENIED")
    def test_chunk_gap_denied(self):
        data=b"abcdefgh"; r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=8,expected_sha256=hashlib.sha256(data).hexdigest(),chunk_size=4,idempotency_key="idempotency-key-0007")
        with self.assertRaises(UploadError) as e: self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=1,offset=4,data=b"efgh")
        self.assertEqual(e.exception.code,"CHUNK_SEQUENCE")
    def test_checksum_mismatch_never_promotes(self):
        r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=3,expected_sha256=hashlib.sha256(b"abc").hexdigest(),chunk_size=3,idempotency_key="idempotency-key-0008")
        self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=b"xyz")
        with self.assertRaises(UploadError) as e: self.service.finalize(trusted_context=self.ctx,upload_id=r["upload_id"])
        self.assertEqual(e.exception.code,"CHECKSUM_MISMATCH")
        self.assertFalse((self.root/"119"/"images"/"photo.png").exists())
    def test_existing_destination_not_overwritten(self):
        p=self.root/"119"/"images"/"photo.png"; p.write_bytes(b"original")
        with self.assertRaises(UploadError) as e:
            self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
              expected_bytes=1,expected_sha256=hashlib.sha256(b"x").hexdigest(),chunk_size=1,idempotency_key="idempotency-key-0009")
        self.assertEqual(e.exception.code,"ALREADY_EXISTS"); self.assertEqual(p.read_bytes(),b"original")
    def test_chunk_retry_is_idempotent(self):
        data=b"retry-safe"
        r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=len(data),expected_sha256=hashlib.sha256(data).hexdigest(),chunk_size=64,idempotency_key="idempotency-key-0010")
        first=self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=data)
        second=self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=data)
        self.assertEqual(first["status"],"ACCEPTED"); self.assertEqual(second["status"],"ALREADY_ACCEPTED")
    def test_two_service_instances_serialize_conflicting_chunk_writes(self):
        expected=b"good"
        r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=4,expected_sha256=hashlib.sha256(expected).hexdigest(),chunk_size=4,idempotency_key="idempotency-key-0016")
        other=SandboxBinaryUploadService(sandbox_root=self.root,ledger=self.ledger,authorizer=self.core,audience="build-sandbox-test")
        barrier=threading.Barrier(2)
        def send(service,payload):
            barrier.wait()
            try: return service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=payload)["status"]
            except UploadError as e: return e.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes=list(pool.map(lambda args:send(*args),[(self.service,b"good"),(other,b"evil")]))
        self.assertCountEqual(outcomes,["ACCEPTED","REPLAY_MISMATCH"])
        row=self.ledger.get(r["upload_id"]); staging=Path(row["staging_path"])
        accepted=self.ledger.get_chunk(r["upload_id"],0)
        self.assertIn(staging.read_bytes(),(b"good",b"evil"))
        self.assertEqual(accepted[2],hashlib.sha256(staging.read_bytes()).hexdigest())
        self.assertEqual(accepted[1],4)
    def test_concurrent_finalize_calls_are_serialized_and_idempotent(self):
        data=b"concurrent-finalize"
        r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=len(data),expected_sha256=hashlib.sha256(data).hexdigest(),chunk_size=64,idempotency_key="idempotency-key-0017")
        self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=data)
        barrier=threading.Barrier(2)
        def finish():
            barrier.wait()
            return self.service.finalize(trusted_context=self.ctx,upload_id=r["upload_id"])
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:finish(),range(2)))
        self.assertEqual(results[0],results[1])
        self.assertEqual(results[0]["status"],"COMPLETED")
        self.assertEqual((self.root/"119"/"images"/"photo.png").read_bytes(),data)
        self.assertEqual(self.ledger.get(r["upload_id"])["state"],"COMPLETED")
    def test_finalize_retry_is_idempotent_and_readback_checked(self):
        data=b"finalize-retry"
        r=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          expected_bytes=len(data),expected_sha256=hashlib.sha256(data).hexdigest(),chunk_size=64,idempotency_key="idempotency-key-0011")
        self.service.chunk(trusted_context=self.ctx,upload_id=r["upload_id"],index=0,offset=0,data=data)
        one=self.service.finalize(trusted_context=self.ctx,upload_id=r["upload_id"])
        two=self.service.finalize(trusted_context=self.ctx,upload_id=r["upload_id"])
        self.assertEqual(one,two)
    def test_idempotency_key_cannot_change_content(self):
        args=dict(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",destination="images/photo.png",
          chunk_size=64,idempotency_key="idempotency-key-0012")
        self.service.begin(expected_bytes=1,expected_sha256=hashlib.sha256(b"a").hexdigest(),**args)
        with self.assertRaises(UploadError) as e:
            self.service.begin(expected_bytes=1,expected_sha256=hashlib.sha256(b"b").hexdigest(),**args)
        self.assertEqual(e.exception.code,"IDEMPOTENCY_CONFLICT")
    def _prepare_finalizing_crash(self,data,key):
        digest=hashlib.sha256(data).hexdigest()
        started=self.service.begin(trusted_context=self.ctx,canonical_work_id="W119",sandbox_work_id="119",
          destination="images/photo.png",expected_bytes=len(data),expected_sha256=digest,chunk_size=4096,idempotency_key=key)
        uid=started["upload_id"]
        for i,off in enumerate(range(0,len(data),4096)):
            self.service.chunk(trusted_context=self.ctx,upload_id=uid,index=i,offset=off,data=data[off:off+4096])
        row=self.ledger.get(uid)
        self.ledger.transition(uid,"UPLOADING","FINALIZING","SIMULATED_PROCESS_CRASH",digest)
        return uid,Path(row["staging_path"]),Path(row["final_path"]),digest
    def test_finalize_recovers_crash_before_promotion(self):
        data=b"crash-before-promotion"
        uid,staging,final,digest=self._prepare_finalizing_crash(data,"idempotency-key-0013")
        self.assertTrue(staging.exists()); self.assertFalse(final.exists())
        result=self.service.finalize(trusted_context=self.ctx,upload_id=uid)
        self.assertEqual(result["status"],"COMPLETED"); self.assertTrue(result["recovered"])
        self.assertEqual(final.read_bytes(),data); self.assertFalse(staging.exists())
        self.assertEqual(result["sha256"],digest); self.assertEqual(self.ledger.get(uid)["state"],"COMPLETED")
    def test_finalize_recovers_crash_after_promotion_before_cleanup(self):
        data=b"crash-after-promotion"
        uid,staging,final,digest=self._prepare_finalizing_crash(data,"idempotency-key-0014")
        final.parent.mkdir(parents=True,exist_ok=True); __import__("os").link(staging,final)
        self.assertTrue(staging.exists()); self.assertEqual(final.read_bytes(),data)
        result=self.service.finalize(trusted_context=self.ctx,upload_id=uid)
        self.assertEqual(result["status"],"COMPLETED"); self.assertTrue(result["recovered"])
        self.assertFalse(staging.exists()); self.assertEqual(result["sha256"],digest)
        self.assertEqual(self.ledger.get(uid)["state"],"COMPLETED")
    def test_finalize_recovery_refuses_conflicting_destination(self):
        data=b"expected-finalizing-content"
        uid,staging,final,_=self._prepare_finalizing_crash(data,"idempotency-key-0015")
        final.write_bytes(b"attacker-or-unrelated-file")
        with self.assertRaises(UploadError) as e:
            self.service.finalize(trusted_context=self.ctx,upload_id=uid)
        self.assertEqual(e.exception.code,"RECOVERY_CONFLICT")
        self.assertEqual(self.ledger.get(uid)["state"],"FINALIZING")
        self.assertTrue(staging.exists())
    def test_core_checked_for_each_operation(self):
        self.roundtrip(b"binary-data")
        self.assertEqual(self.core.calls,["begin","chunk","chunk","finalize"])

if __name__=="__main__": unittest.main(verbosity=2)
