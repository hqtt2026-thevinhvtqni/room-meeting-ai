from __future__ import annotations

import functools
import http.server
import json
import shutil
import threading
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from browser_provider_phase2 import BrowserProvider

ROOT = Path('/tmp/work14-browser-phase2')
if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)
fixture = ROOT / 'fixture'; fixture.mkdir()
(fixture / 'index.html').write_text('''<!doctype html><html><head><title>Work 14 Browser Fixture</title></head><body><h1>Browser Provider Fixture</h1><h2>Phase 2</h2><p id="summary">Real Chromium provider verification.</p><label>Query <input id="q"></label></body></html>''', encoding='utf-8')
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(fixture))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
try:
    url = f'http://127.0.0.1:{server.server_port}/index.html'
    result = BrowserProvider().execute('Work 14', url, [
        {'op': 'inspect'},
        {'op': 'type', 'selector': '#q', 'text': 'provider-e2e'},
        {'op': 'extract', 'selectors': {'heading': 'h1', 'summary': '#summary'}},
        {'op': 'screenshot', 'name': 'phase2-browser.png'},
        {'op': 'close'},
    ], ROOT / 'evidence')
    assert result['status'] == 'PASS', result
    assert result['page_title'] == 'Work 14 Browser Fixture'
    assert any(step['op'] == 'screenshot' and step['result']['bytes'] > 0 for step in result['steps'])
    assert any(step['op'] == 'extract' and step['result']['heading'] == ['Browser Provider Fixture'] for step in result['steps'])
    summary = {'status': 'PASS', 'provider': result['provider'], 'execution_id': result['execution_id'], 'target': url, 'final_url': result['final_url'], 'page_title': result['page_title'], 'steps': result['steps'], 'evidence_dir': str(ROOT / 'evidence' / result['execution_id'])}
    (ROOT / 'PHASE2_SUMMARY.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
finally:
    server.shutdown(); server.server_close()
