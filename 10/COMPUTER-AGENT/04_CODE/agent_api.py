from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, os
from agent_runtime import AgentRuntime
from browser_adapter import PlaywrightBrowserAdapter
from models import Action

PORT = int(os.getenv("COMPUTER_AGENT_PORT", "8787"))
HEADLESS = os.getenv("COMPUTER_AGENT_HEADLESS", "0") == "1"

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers(); self.wfile.write(raw)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status":"ok","service":"computer-agent","port":PORT})
        self._send(404, {"status":"FAIL","error":"not_found"})

    def do_POST(self):
        if self.path != "/agent/execute":
            return self._send(404, {"status":"FAIL","error":"not_found"})
        try:
            n=int(self.headers.get("Content-Length","0"))
            body=json.loads(self.rfile.read(n) or b"{}")
            task=body["task"]
            actions=[Action(**a) for a in body.get("actions",[])]
            result=AgentRuntime(PlaywrightBrowserAdapter(HEADLESS)).execute(
                task, actions, body.get("verification"))
            code=200 if result.status=="PASS" else 409
            return self._send(code, result.__dict__)
        except Exception as exc:
            self._send(400, {"status":"FAIL","error":f"{type(exc).__name__}: {exc}"})

if __name__=="__main__":
    print(f"Computer Agent API listening on 127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
