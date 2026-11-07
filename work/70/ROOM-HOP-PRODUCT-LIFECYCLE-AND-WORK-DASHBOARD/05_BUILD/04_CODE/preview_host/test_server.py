"""Black-box tests for the read-only Preview Host."""
import json
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

SERVER = Path(__file__).with_name("server.py")

class PreviewHostTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        dash = self.root / "dash"
        (dash / "execution").mkdir(parents=True)
        (dash / "execution" / "index.html").write_text("<html><body><h1>EXECUTION</h1></body></html>", encoding="utf-8")
        (dash / "execution" / "status.json").write_text('{"state":"RECORDED"}', encoding="utf-8")
        registry = {"schema_version":"1.0","works":[{
            "work_id":"70","display_name":"Work 70","enabled":True,
            "dashboard_root":"dash","views":{"execution":"execution/index.html"}
        }]}
        self.registry = self.root / "registry.json"
        self.registry.write_text(json.dumps(registry), encoding="utf-8")
        self.port = self._free_port()
        self.proc = subprocess.Popen(
            [sys.executable,str(SERVER),"--registry",str(self.registry),
             "--repo-root",str(self.root),"--host","127.0.0.1","--port",str(self.port)],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.base = f"http://127.0.0.1:{self.port}"
        for _ in range(40):
            if self.proc.poll() is not None:
                self.fail("Preview Host exited during startup")
            try:
                urllib.request.urlopen(self.base + "/", timeout=0.2)
                break
            except Exception:
                time.sleep(0.05)
        else:
            self.fail("Preview Host did not become ready")

    def tearDown(self):
        self.proc.terminate()
        try: self.proc.wait(timeout=3)
        except subprocess.TimeoutExpired: self.proc.kill()
        self.tmp.cleanup()

    @staticmethod
    def _free_port():
        import socket
        with socket.socket() as sock:
            sock.bind(("127.0.0.1",0))
            return sock.getsockname()[1]

    def request(self,path,method="GET"):
        req=urllib.request.Request(self.base+path,method=method)
        try:
            with urllib.request.urlopen(req,timeout=2) as r: return r.status,r.read(),r.headers
        except urllib.error.HTTPError as e: return e.code,e.read(),e.headers

    def test_work_route_serves_html(self):
        status,body,_=self.request("/work/70/execution/")
        self.assertEqual(status,200); self.assertIn(b"EXECUTION",body)
        self.assertIn(b"PREVIEW / READ-ONLY",body)
        self.assertIn(b"Freshness UNKNOWN",body)

    def test_relative_json_asset_served(self):
        status,body,_=self.request("/work/70/execution/status.json")
        self.assertEqual(status,200); self.assertIn(b"RECORDED",body)

    def test_health_endpoint(self):
        status,body,headers=self.request("/healthz")
        self.assertEqual(status,200)
        self.assertIn(b'"status": "ok"',body)
        self.assertIn("application/json",headers.get("Content-Type",""))

    def test_work_without_trailing_slash_redirects(self):
        status,_,headers=self.request("/work/70")
        self.assertEqual(status,308)
        self.assertEqual(headers.get("Location"),"/work/70/")

    def test_view_without_trailing_slash_redirects(self):
        status,_,headers=self.request("/work/70/execution")
        self.assertEqual(status,308)
        self.assertEqual(headers.get("Location"),"/work/70/execution/")

    def test_unknown_work_is_404(self):
        self.assertEqual(self.request("/work/999/")[0],404)

    def test_write_method_is_405(self):
        self.assertEqual(self.request("/work/70/execution/","POST")[0],405)

    def test_unknown_method_is_405(self):
        self.assertEqual(self.request("/work/70/execution/","TRACE")[0],405)

    def test_head_is_supported_without_body(self):
        status,body,_=self.request("/work/70/execution/","HEAD")
        self.assertEqual(status,200)
        self.assertEqual(body,b"")

    def test_path_traversal_is_rejected(self):
        self.assertEqual(self.request("/work/70/execution/%2e%2e/%2e%2e/registry.json")[0],400)

    def test_security_headers_present(self):
        status,_,headers=self.request("/work/70/execution/")
        self.assertEqual(status,200)
        self.assertEqual(headers.get("X-Content-Type-Options"),"nosniff")
        self.assertEqual(headers.get("Cache-Control"),"no-store")

if __name__ == "__main__":
    unittest.main()
