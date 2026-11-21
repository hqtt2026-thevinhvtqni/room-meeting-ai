"""Static UI-contract checks for the Work 10 operational dashboard.

These checks do not start an Agent API, browser adapter, or real workflow.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "08_DASHBOARD" / "index.html"


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.textareas = 0
        self.textarea_text = []
        self.in_textarea = False
        self.current_textarea = ""
        self.buttons: dict[str, dict[str, str | None]] = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "textarea":
            self.textareas += 1
            self.in_textarea = True
            self.current_textarea = ""
        if tag == "button" and attrs.get("id"):
            self.buttons[attrs["id"]] = attrs

    def handle_data(self, data):
        if self.in_textarea:
            self.current_textarea += data

    def handle_endtag(self, tag):
        if tag == "textarea" and self.in_textarea:
            self.textarea_text.append(self.current_textarea)
            self.in_textarea = False


def check(condition: bool, label: str):
    if not condition:
        raise AssertionError(label)
    print(f"PASS  {label}")


def main():
    html = DASH.read_text(encoding="utf-8")
    parser = Inventory()
    parser.feed(html)
    script_blocks = re.findall(r"<script>(.*?)</script>", html, re.S | re.I)
    script = "\n".join(script_blocks)

    required_ids = {
        "healthPill", "refreshHealth", "workId", "serviceVersion", "leaseState",
        "apiToken", "task", "actions", "verification", "confirmReal", "run",
        "resultPill", "trace", "evidenceTable", "observation", "rawResponse",
    }
    check(required_ids.issubset(parser.ids), "required live-health, input, and evidence UI hooks exist")
    check("const EXPECTED_WORK_ID = '10'" in script, "client pins health check to Work 10")
    check("data.service !== 'computer-agent'" in script and "String(data.work_id) !== EXPECTED_WORK_ID" in script,
          "health rejects wrong service or Work ID")
    check("/health" in script and "/agent/execute" in script, "UI calls the documented live API endpoints")
    check("$('confirmReal').checked" in script, "execution requires explicit real-action confirmation")
    check("!state.health.execution_busy" in script, "execution is blocked while the runtime lease is busy")
    check("verification.checks.length === 0" in script, "workflow requires explicit post-condition checks")
    check("const finalObservation = verifyEvidence?.observation" in script,
          "final observation prefers the runtime verification evidence")
    check("localStorage" not in script and "sessionStorage" not in script, "token is not persisted in browser storage")
    check("Bearer ${token}" in script, "bearer token is sent in the authorization header")
    check("Work 10 REAL E2E" not in html and "PREVIEW_ONLY" not in html, "operational page has no seeded demo result")
    check("setInterval" in script and "15000" in script, "health refreshes periodically")
    check("AbortController" in script, "network calls have bounded timeout handling")
    check(parser.textareas == 2 and all(not text.strip() for text in parser.textarea_text),
          "actions and verification start blank, not with sample execution payload")
    check("disabled" in parser.buttons.get("run", {}), "Execute starts disabled until runtime/consent guards pass")

    node = shutil.which("node")
    if node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
            f.write(script)
            js_path = f.name
        result = subprocess.run([node, "--check", js_path], capture_output=True, text=True)
        Path(js_path).unlink(missing_ok=True)
        check(result.returncode == 0, f"inline JavaScript parses with node --check: {result.stderr.strip()}")
    else:
        print("SKIP  node unavailable; inline JavaScript syntax was not checked")

    print("Static Dashboard contract checks complete. No API/browser workflow was executed.")


if __name__ == "__main__":
    main()


# Final compatibility assertion (kept outside main to avoid rewriting prior checks).
_dashboard_source = DASH.read_text(encoding="utf-8")
if "String(state.health.work_id) === EXPECTED_WORK_ID" not in _dashboard_source:
    raise AssertionError("execution guard must normalize Work ID type")
print("PASS  execution guard normalizes Work ID type")
