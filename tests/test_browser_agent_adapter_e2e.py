import json
import requests

BASE = "http://127.0.0.1:8787"

req = {
    "url": "https://en.wikipedia.org/wiki/Headless_browser",
    "work_id": "wikipedia-browser-e2e",
    "steps": [
        {"op": "inspect"},
        {
            "op": "extract",
            "selectors": {
                "headings": "h1,h2",
                "summary": "#mw-content-text p",
            },
        },
        {"op": "wait", "ms": 500},
        {"op": "screenshot", "name": "wikipedia-browser-e2e.png"},
    ],
}

r = requests.post(
    BASE + "/browser/execute_workflow",
    json=req,
    timeout=60,
)

print(r.status_code)

data = r.json()

print(
    json.dumps(
        {
            k: data.get(k)
            for k in [
                "ok",
                "final_url",
                "page_title",
                "evidence_json",
                "roomhop_submission",
            ]
        },
        indent=2,
        ensure_ascii=False,
    )
)

assert r.ok and data["ok"]
assert "wikipedia.org/wiki/Headless_browser" in data["final_url"]
assert data["page_title"].endswith(" - Wikipedia")

submission = data["roomhop_submission"]

assert submission["status"] == "pass"
assert submission["read_back"] is True
assert submission["meeting_id"] == "MEETING-MCP-LIFECYCLE-001"

print("ROOM-HOP MCP HANDOFF + READ-BACK PASS")
print(
    "BROWSER E2E PASS: "
    "real Chromium navigation, inspect, extraction, wait, screenshot"
)
