from pathlib import Path
import json
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\ROOM-HOP-CLEAN\room-meeting-ai\.ai-workspace\sessions\AI-BUILD-GATEWAY-V1\workspace\14\AUTONOMOUS-E2E-BUILDER")
EVIDENCE = ROOT / "06_EVIDENCE" / "W14-W13-BROWSER-E2E-001"
EVIDENCE.mkdir(parents=True, exist_ok=True)

result = {
    "execution_id": "W14-W13-BROWSER-E2E-001",
    "work_id": "14",
    "provider": "W13_W12_REAL_EXECUTION_HOST",
    "browser": "chromium",
    "status": "FAIL",
    "started_at": datetime.now(timezone.utc).isoformat(),
}

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        page.goto("https://example.com", wait_until="domcontentloaded")

        title = page.title()
        url = page.url

        screenshot = EVIDENCE / "browser.png"
        page.screenshot(path=str(screenshot), full_page=True)

        assert title == "Example Domain"
        assert url == "https://example.com/"

        result.update({
            "status": "PASS",
            "navigation": "PASS",
            "title": title,
            "url": url,
            "screenshot": str(screenshot),
            "chromium_executable": p.chromium.executable_path,
        })

        browser.close()

except Exception as exc:
    result.update({
        "status": "FAIL",
        "error": str(exc),
    })

result["finished_at"] = datetime.now(timezone.utc).isoformat()

final = EVIDENCE / "FINAL_RESULT.json"
final.write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

print(json.dumps(result, indent=2, ensure_ascii=False))

if result["status"] != "PASS":
    raise SystemExit(1)
