"""Reproducible file:// UI smoke; not Browser Runtime or agent E2E evidence."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "index.html").as_uri()
external_requests = []
checks = []


def check(name, condition, detail=""):
    if not condition:
        raise AssertionError(f"FAIL {name}: {detail}")
    checks.append({"name": name, "status": "PASS", "detail": detail})


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1365, "height": 900})
    page.on("request", lambda request: external_requests.append(request.url) if request.url.startswith(("http://", "https://")) else None)
    page.goto(URL, wait_until="load")

    check("file-based page loads", page.title().endswith("TEST_ONLY"), page.title())
    check("runtime stays disconnected", page.locator("#runtimeBadge").inner_text() == "DISCONNECTED" and page.locator("#runtimeConnection").inner_text() == "DISCONNECTED")
    check("network boundary banner", "NO NETWORK" in page.locator(".chrome-mode").inner_text())
    tabs = page.get_by_role("tab", name="Select TEST_ONLY tab: Local fixture")
    check("initial browser tab selected", tabs.get_attribute("aria-selected") == "true")

    # New tab, arrow-key selection/focus, close selected tab and focus restoration.
    page.get_by_role("button", name="Open TEST_ONLY tab").click()
    check("new local tab created", page.locator("#tabs [role='tab']").count() == 2)
    check("tablist contains only role=tab children", page.locator("#tabs > [role='tab']").count() == 2 and page.locator("#tabs > button:not([role='tab'])").count() == 0)
    second = page.get_by_role("tab", name="Select TEST_ONLY tab: Test tab 2")
    check("new tab receives focus", page.evaluate("document.activeElement.id") == "mock-tab-2")
    second.press("ArrowLeft")
    check("ArrowLeft selects and focuses previous tab", page.evaluate("document.activeElement.id") == "mock-tab-1" and page.locator("#mock-tab-1").get_attribute("aria-selected") == "true")
    page.locator("#mock-tab-1").press("ArrowRight")
    check("ArrowRight selects and focuses the next tab", page.evaluate("document.activeElement.id") == "mock-tab-2" and page.locator("#mock-tab-2").get_attribute("aria-selected") == "true")
    page.get_by_role("button", name="Close current TEST_ONLY tab: Test tab 2").click()
    check("closing active tab restores focus to fallback", page.evaluate("document.activeElement.id") == "mock-tab-1" and page.locator("#tabs [role='tab']").count() == 1)
    check("last tab cannot be closed", page.get_by_role("button", name="Close current TEST_ONLY tab: Local fixture").is_disabled())

    # Address entry and navigation buttons modify only local fixture state.
    address = page.locator("#urlInput")
    address.fill("https://example.test/search?q=local-fixture")
    address.press("Enter")
    check("address entry changes only the local fixture URL", address.input_value() == "https://example.test/search?q=local-fixture" and "Sample fixture cards" in page.locator("#browserContent").inner_text())
    page.get_by_role("button", name="Back in TEST_ONLY mock state").click()
    check("Back restores the local root fixture", address.input_value() == "https://wikipedia.org" and "Local browser-view fixture" in page.locator("#browserContent").inner_text())
    page.get_by_role("button", name="Forward in TEST_ONLY mock state").click()
    check("Forward restores a local search fixture", "Special:Search" in address.input_value() and "Sample fixture cards" in page.locator("#browserContent").inner_text())
    page.get_by_role("button", name="Reload TEST_ONLY mock view").click()
    check("Reload exposes local loading state", page.locator("#browserContent").get_attribute("aria-busy") == "true" and "LOCAL UPDATE" in page.locator("#pageState").inner_text())
    page.locator("#browserContent[aria-busy='false']").wait_for(timeout=5000)
    check("Reload returns to disconnected local ready state", page.locator("#runtimeBadge").inner_text() == "DISCONNECTED" and "DISCONNECTED" in page.locator("#pageState").inner_text())

    # Secondary tablist keyboard/panel behavior.
    architecture = page.get_by_role("tab", name="Architecture limits")
    architecture.click()
    check("secondary tab reveals matching panel", page.locator("#architecturePanel").is_visible() and page.locator("#demoPanel").is_hidden())
    architecture.press("ArrowLeft")
    check("secondary ArrowLeft updates panel and focus", page.evaluate("document.activeElement.id") == "demoTab" and page.locator("#demoPanel").is_visible())

    # Permission gate and held-state behavior.
    page.get_by_role("button", name="Run TEST_ONLY demo").click()
    check("permission gate reports missing permissions", page.locator("#permissionFeedback").inner_text().startswith("Chưa bật quyền TEST_ONLY"))
    check("permission gate moves focus to required test flag", page.evaluate("document.activeElement.dataset.permission") == "readPage")
    page.get_by_role("button", name="Hold TEST_ONLY demo").click()
    check("local hold disables demo run", page.get_by_role("button", name="Run TEST_ONLY demo").is_disabled())
    page.get_by_role("button", name="Resume TEST_ONLY demo").click()
    check("local resume re-enables demo run", not page.get_by_role("button", name="Run TEST_ONLY demo").is_disabled())

    # Enable only local TEST_ONLY flags; this never grants browser permissions.
    for button in page.locator(".permission-toggle").all():
        if button.get_attribute("aria-pressed") != "true":
            button.click()
    check("permission flags are local and pressed", page.locator(".permission-toggle[aria-pressed='true']").count() == 7)
    page.get_by_role("button", name="Run TEST_ONLY demo").click()
    page.locator("#passBox").wait_for(state="visible", timeout=10000)
    check("fixture flow completes as TEST_ONLY", "TEST_ONLY DEMO COMPLETE" in page.locator("#passBox").inner_text())
    check("runtime remains disconnected after fixture", page.locator("#runtimeBadge").inner_text() == "DISCONNECTED" and "No real-world task" in page.locator("#sessionSubstate").inner_text())
    check("evidence explicitly has no artifact", "artifact: none" in page.locator("#evidence").inner_text() and "No screenshot file was created" in page.locator("#evidence").inner_text())
    check("progress semantics reach complete", page.locator(".progress-track").get_attribute("aria-valuenow") == "6")

    # Reset clears local state and permissions.
    page.get_by_role("button", name="Reset TEST_ONLY state").click()
    check("reset clears simulated state", page.locator("#timeline").inner_text().strip() == "No simulated events" and page.locator("#passBox").is_hidden())
    check("reset clears all permission flags", page.locator(".permission-toggle[aria-pressed='true']").count() == 0)

    # Responsive overflow checks at mobile and compact desktop widths.
    for width, height in [(390, 844), (360, 800), (768, 900)]:
        page.set_viewport_size({"width": width, "height": height})
        page.wait_for_timeout(100)
        dimensions = page.evaluate("({inner: window.innerWidth, doc: document.documentElement.scrollWidth, body: document.body.scrollWidth})")
        check(f"no horizontal overflow at {width}px", dimensions["doc"] <= dimensions["inner"] and dimensions["body"] <= dimensions["inner"], json.dumps(dimensions))

    page.wait_for_timeout(100)
    check("no HTTP(S) request was made", not external_requests, json.dumps(external_requests))
    browser.close()

print(json.dumps({"kind": "file_based_ui_smoke", "runtime_integration": False, "tests": len(checks), "passed": len(checks), "failed": 0, "checks": checks, "external_requests": external_requests}, ensure_ascii=False, indent=2))


# Preserve the local UI-only result separately from Browser Runtime/E2E evidence.
from datetime import datetime, timezone

smoke_report = {
    "work_id": "092",
    "kind": "file_url_test_only_browser_ui_smoke",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "environment": {"browser": "system Chromium", "executable": "/usr/bin/chromium", "runner": "Playwright Python", "runtime_integration": False},
    "summary": {"checks": len(checks), "passed": len(checks), "failed": 0},
    "checks": checks,
    "external_http_requests": external_requests,
    "screenshots_captured": False,
    "limits": [
        "This is local file:// UI interaction evidence only, not Browser Runtime or real-agent E2E.",
        "The prototype did not connect to an external website or API.",
    ],
    "status": "PASS",
}
smoke_report_path = ROOT.parents[1] / "02_EVIDENCE" / "test-results" / "browser-ui-smoke.json"
smoke_report_path.parent.mkdir(parents=True, exist_ok=True)
smoke_report_path.write_text(json.dumps(smoke_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
