#!/usr/bin/env python3
"""File-based accessibility/responsive audit for the TEST_ONLY UI; not Runtime E2E."""
from datetime import datetime, timezone
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT.parents[1]
URL = (ROOT / "index.html").as_uri()
EVIDENCE = WORK_ROOT / "02_EVIDENCE"
SCREENSHOTS = EVIDENCE / "screenshots"
REPORT = EVIDENCE / "test-results" / "accessibility-audit.json"
CHECKS = []
NETWORK_REQUESTS = []
CONSOLE_ERRORS = []
PAGE_ERRORS = []


def check(name, passed, detail=""):
    CHECKS.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": str(detail)})
    if not passed:
        print(f"FAIL {name}: {detail}")


def rgb(value):
    if value.startswith("#"):
        h = value.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    match = re.fullmatch(r"rgba?\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)(?:,\s*[\d.]+)?\)", value)
    if not match:
        raise ValueError(f"Unsupported computed color: {value}")
    return tuple(round(float(match.group(i))) for i in (1, 2, 3))


def luminance(color):
    channels = []
    for value in rgb(color):
        value /= 255
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(foreground, background):
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def color_of(page, selector, prop="color"):
    return page.locator(selector).first.evaluate("(el, prop) => getComputedStyle(el)[prop]", prop)


def contrast_check(page, name, selector, background_selector=None, background_color=None, minimum=4.5):
    foreground = color_of(page, selector)
    if background_color:
        background = background_color
    else:
        background = color_of(page, background_selector, "backgroundColor")
    measured = contrast(foreground, background)
    check(f"contrast: {name}", measured >= minimum, f"{measured:.2f}:1; minimum {minimum:.1f}:1; fg={foreground}; bg={background}")


def visible_width_check(page, label, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.wait_for_timeout(80)
    dims = page.evaluate("({viewport: innerWidth, doc: document.documentElement.scrollWidth, body: document.body.scrollWidth})")
    check(f"{label} has no horizontal overflow", dims["doc"] <= dims["viewport"] and dims["body"] <= dims["viewport"], dims)
    return dims


def check_names_and_roles(page):
    result = page.evaluate("""() => {
      const visible = (el) => !!(el.getClientRects().length) && !el.closest('[hidden]');
      const name = (el) => {
        const labelledby = el.getAttribute('aria-labelledby');
        if (labelledby) return labelledby.split(/\\s+/).map(id => document.getElementById(id)?.innerText || '').join(' ').trim();
        const aria = el.getAttribute('aria-label'); if (aria) return aria.trim();
        if (el.labels?.length) return [...el.labels].map(x => x.innerText).join(' ').trim();
        return (el.innerText || el.getAttribute('title') || el.getAttribute('alt') || '').trim();
      };
      const controls = [...document.querySelectorAll('button,input:not([type=hidden]),textarea,select,[role=progressbar]')]
        .filter(visible).map(el => ({tag: el.tagName, id: el.id, role: el.getAttribute('role'), name: name(el)}));
      const tabs = [...document.querySelectorAll('#tabs [role=tab]')];
      const selected = tabs.filter(t => t.getAttribute('aria-selected') === 'true');
      const tabsOnly = [...document.querySelector('#tabs').children].every(el => el.getAttribute('role') === 'tab');
      const active = selected[0];
      return {controls, unnamed: controls.filter(c => !c.name), tabCount: tabs.length,
        selectedCount: selected.length, tabsOnly, roving: tabs.every(t => t.tabIndex === (t === active ? 0 : -1)),
        panelLinked: !!active && document.querySelector('#browserContent').getAttribute('aria-labelledby') === active.id,
        describedbyExists: [...document.querySelectorAll('[aria-describedby]')].every(el => el.getAttribute('aria-describedby').split(/\\s+/).every(id => document.getElementById(id)))
      };
    }""")
    check("all visible controls/status widgets have a name source (automated heuristic)", not result["unnamed"], result["unnamed"])
    check("browser tablist contains only tabs and follows roving-tabindex semantics", result["tabCount"] == 1 and result["selectedCount"] == 1 and result["tabsOnly"] and result["roving"], result)
    check("selected browser tab labels the browser panel", result["panelLinked"], result["panelLinked"])
    check("all aria-describedby IDs resolve", result["describedbyExists"], result["describedbyExists"])


def audit_scenario(page, task, name, expected_actions):
    page.locator("#taskInput").fill(task)
    for button in page.locator(".permission-toggle").all():
        if button.get_attribute("aria-pressed") != "true":
            button.click()
    page.get_by_role("button", name="Run TEST_ONLY demo").click()
    running = page.locator("#actionState").inner_text()
    runtime = page.locator("#runtimeBadge").inner_text()
    check(f"{name}: TEST_ONLY running transition", running == "TEST_ONLY_RUNNING" and runtime == "DISCONNECTED", {"activity": running, "runtime": runtime})
    check(f"{name}: current action has readable description", bool(page.locator("#currentHumanAction").inner_text().strip()))
    page.locator("#passBox").wait_for(state="visible", timeout=15000)
    final = page.locator("#actionState").inner_text()
    final_runtime = page.locator("#runtimeBadge").inner_text()
    action_names = page.locator("#timeline li strong").all_inner_texts()
    descriptions = page.locator("#timeline li small").all_inner_texts()
    check(f"{name}: expected ordered action sequence", len(action_names) == len(expected_actions) and all(action in title for action, title in zip(expected_actions, action_names)), action_names)
    check(f"{name}: every timeline item has a human-readable description", len(descriptions) == len(expected_actions) and all(" · " in item and item.split(" · ", 1)[1].strip() for item in descriptions), descriptions)
    check(f"{name}: completion remains TEST_ONLY and disconnected", final == "TEST_ONLY_COMPLETE" and final_runtime == "DISCONNECTED" and "TEST_ONLY DEMO COMPLETE" in page.locator("#passBox").inner_text(), {"activity": final, "runtime": final_runtime})
    check(f"{name}: progress reaches all fixture steps", page.locator(".progress-track").get_attribute("aria-valuenow") == str(len(expected_actions)), page.locator("#progressValue").inner_text())
    if name == "Browse":
        contrast_check(page, "timeline timestamp/description", "#timeline li small", background_color="#0d141c")
        contrast_check(page, "evidence detail/provenance", ".evidence-list li small", background_color="#0d141c")
    page.get_by_role("button", name="Reset TEST_ONLY state").click()
    check(f"{name}: reset returns to TEST_ONLY_READY and clears grants", page.locator("#actionState").inner_text() == "TEST_ONLY_READY" and page.locator(".permission-toggle[aria-pressed='true']").count() == 0)


def main():
    EVIDENCE.joinpath("test-results").mkdir(parents=True, exist_ok=True)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("request", lambda request: NETWORK_REQUESTS.append(request.url) if request.url.startswith(("http://", "https://", "ws://", "wss://")) else None)
        page.on("console", lambda message: CONSOLE_ERRORS.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: PAGE_ERRORS.append(str(error)))
        page.goto(URL, wait_until="load")
        page.screenshot(path=str(SCREENSHOTS / "ui-only-desktop-1920x1080.png"), full_page=True)
        check("file:// prototype loads with explicit disconnected boundary", page.title().endswith("TEST_ONLY") and page.locator("#runtimeBadge").inner_text() == "DISCONNECTED" and "NO NETWORK" in page.locator(".chrome-mode").inner_text())
        check("initial activity is TEST_ONLY_READY, not agent connected", page.locator("#actionState").inner_text() == "TEST_ONLY_READY" and page.locator("#agentStateLabel").inner_text() == "DISCONNECTED")
        check_names_and_roles(page)
        contrast_check(page, "chrome mode", ".chrome-mode", background_color="#121a23")
        contrast_check(page, "brand subtitle", ".brand small", background_color="#0a0f15")
        contrast_check(page, "top bar status text", ".top-right", background_color="#0a0f15")
        contrast_check(page, "selected browser tab text", ".tab", background_color="#10161e")
        contrast_check(page, "URL bar text", ".urlbar", background_color="#0a1016")
        contrast_check(page, "browser page status", ".page-status", background_color="#111922")
        contrast_check(page, "muted browser fixture text", ".wiki-side", background_color="#ffffff")
        contrast_check(page, "task helper text", ".task-help", background_color="#0d141c")
        contrast_check(page, "task label", ".task-box label", background_color="#0d141c")
        contrast_check(page, "section counter", ".section-head span", background_color="#0d141c")
        contrast_check(page, "empty timeline text", ".empty-timeline", background_color="#0d141c")
        contrast_check(page, "permission status", ".permission-item > [data-permission-status]", background_color="#111d25")
        contrast_check(page, "permission button label", ".permission-toggle", background_color="#17252d")
        contrast_check(page, "runtime banner body", ".runtime-banner", background_color="#211b13")
        contrast_check(page, "runtime banner title", ".runtime-banner strong", background_color="#211b13")
        contrast_check(page, "session substate", ".session-state small", background_color="#111a23")
        contrast_check(page, "footer on darkest body gradient stop", "footer", background_color="#080b10")
        contrast_check(page, "footer on lightest body gradient stop", "footer", background_color="#101c24")
        check("task starts aria-valid and becomes announced invalid on blank input", page.locator("#taskInput").get_attribute("aria-invalid") == "false")
        page.keyboard.press("Tab")
        focus = page.evaluate("document.activeElement.id")
        outline = page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
        check("keyboard Tab reaches a control and visible focus indicator appears", page.evaluate("document.activeElement.tagName") in ("BUTTON", "INPUT", "TEXTAREA") and float(outline.removesuffix("px")) >= 2, {"focus": focus, "outline": outline})

        # Tabs: keyboard selection, panel relationships, active/non-active close focus restoration.
        page.get_by_role("button", name="Open TEST_ONLY tab").click()
        contrast_check(page, "blank fixture helper text", ".blank-fixture p", background_color="#edf0f2")
        contrast_check(page, "inactive browser tab text", "#mock-tab-1", background_color="#19232d")
        page.get_by_role("tab", name="Select TEST_ONLY tab: Test tab 2").press("ArrowLeft")
        check("ArrowLeft moves selection/focus to previous browser tab", page.evaluate("document.activeElement.id") == "mock-tab-1" and page.locator("#mock-tab-1").get_attribute("aria-selected") == "true")
        page.locator("#mock-tab-1").press("ArrowRight")
        check("ArrowRight returns selection/focus to the next browser tab", page.evaluate("document.activeElement.id") == "mock-tab-2" and page.locator("#mock-tab-2").get_attribute("aria-selected") == "true")
        page.get_by_role("button", name="Close current TEST_ONLY tab: Test tab 2").click()
        check("closing active tab restores focus to remaining tab", page.evaluate("document.activeElement.id") == "mock-tab-1" and page.locator("#tabs [role=tab]").count() == 1)
        check("final browser tab close is disabled", page.get_by_role("button", name="Close current TEST_ONLY tab: Local fixture").is_disabled())
        page.get_by_role("tab", name="Architecture limits").press("ArrowRight")
        check("secondary keyboard tab updates ARIA selection and panel", page.locator("#demoTab").get_attribute("aria-selected") == "true" and page.locator("#demoPanel").is_visible() and page.locator("#architecturePanel").is_hidden())

        # Trigger form error and local hold gates; neither may imply a runtime action.
        page.locator("#taskInput").fill("")
        page.get_by_role("button", name="Run TEST_ONLY demo").click()
        check("empty task error is visible, announced, invalid and focused", page.locator("#taskError").is_visible() and page.locator("#taskInput").get_attribute("aria-invalid") == "true" and page.evaluate("document.activeElement.id") == "taskInput")
        check("task error text contrast meets WCAG AA", contrast(color_of(page, "#taskError"), color_of(page, ".agent-rail", "backgroundColor")) >= 4.5)
        page.locator("#taskInput").fill("Mở Wikipedia và tìm ROOM-HOP")
        page.get_by_role("button", name="Hold TEST_ONLY demo").click()
        check("hold gate is TEST_ONLY_HELD and run is blocked", page.locator("#actionState").inner_text() == "TEST_ONLY_HELD" and page.get_by_role("button", name="Run TEST_ONLY demo").is_disabled())
        page.get_by_role("button", name="Resume TEST_ONLY demo").click()
        check("resume returns to TEST_ONLY_READY", page.locator("#actionState").inner_text() == "TEST_ONLY_READY")
        check("permission flags start ungranted and expose aria-pressed state", page.locator(".permission-toggle[aria-pressed='true']").count() == 0 and page.locator(".permission-toggle[aria-pressed='false']").count() == 7)

        # Scenario acceptance and T6/T8 fixture boundaries.
        audit_scenario(page, "Mở trang mẫu để duyệt", "Browse", ["Navigate", "Inspect", "Screenshot"])
        audit_scenario(page, "Tìm kiếm khí hậu trên Wikipedia", "Search", ["Navigate", "Inspect", "Type", "Click", "Extract", "Screenshot"])
        audit_scenario(page, "Chạy agent workflow demo", "Workflow", ["Navigate", "Inspect", "Type", "Click", "Extract", "Screenshot", "Wait", "DONE"])

        # Loading/ready transition and reduced-motion preference.
        page.emulate_media(reduced_motion="reduce")
        page.get_by_role("button", name="Reload TEST_ONLY mock view").click()
        check("reload exposes loading state and aria-busy", page.locator("#browserContent").get_attribute("aria-busy") == "true" and "LOCAL UPDATE" in page.locator("#pageState").inner_text())
        duration = page.locator(".spinner").evaluate("el => getComputedStyle(el).animationDuration")
        duration_value = float(duration[:-1]) if duration.endswith("s") else float(duration[:-2]) / 1000
        check("reduced-motion limits spinner animation", duration_value <= 0.0001, duration)
        page.locator("#browserContent[aria-busy='false']").wait_for(timeout=5000)
        check("loading returns to ready while runtime remains disconnected", "DISCONNECTED" in page.locator("#pageState").inner_text() and page.locator("#runtimeBadge").inner_text() == "DISCONNECTED")

        # Wide desktop and tablet screen checks.
        visible_width_check(page, "desktop 1920x1080", 1920, 1080)
        page.screenshot(path=str(SCREENSHOTS / "ui-only-desktop-1920x1080.png"), full_page=True)
        visible_width_check(page, "tablet 768x1024", 768, 1024)
        page.screenshot(path=str(SCREENSHOTS / "ui-only-tablet-768x1024.png"), full_page=True)

        # Android-like mobile emulation only; this is not a physical-device test.
        device = dict(p.devices.get("Pixel 7", {}))
        device.update({"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True})
        mobile_context = browser.new_context(**device)
        mobile = mobile_context.new_page()
        mobile.on("request", lambda request: NETWORK_REQUESTS.append(request.url) if request.url.startswith(("http://", "https://", "ws://", "wss://")) else None)
        mobile.goto(URL, wait_until="load")
        mobile.screenshot(path=str(SCREENSHOTS / "ui-only-android-emulation-390x844.png"), full_page=True, scale="css")
        dims = mobile.evaluate("({viewport: innerWidth, doc: document.documentElement.scrollWidth, body: document.body.scrollWidth, touch: navigator.maxTouchPoints, mobile: matchMedia('(pointer: coarse)').matches, ua: navigator.userAgent})")
        check("Android mobile emulation 390x844 has no overflow and touch input", dims["doc"] <= dims["viewport"] and dims["body"] <= dims["viewport"] and dims["touch"] > 0 and dims["mobile"], {**dims, "ua": "Android-like emulated browser"})
        mobile.locator(".permission-toggle").first.tap()
        check("mobile touch toggles only local TEST_ONLY permission", mobile.locator(".permission-toggle").first.get_attribute("aria-pressed") == "true" and mobile.locator("#runtimeBadge").inner_text() == "DISCONNECTED")
        mobile_context.close()

        check("no HTTP(S)/WebSocket requests were made", not NETWORK_REQUESTS, NETWORK_REQUESTS)
        check("no browser console errors or uncaught page errors", not CONSOLE_ERRORS and not PAGE_ERRORS, {"console": CONSOLE_ERRORS, "page": PAGE_ERRORS})
        browser.close()

    report = {
        "work_id": "092",
        "kind": "file_url_test_only_accessibility_responsive_audit",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(ROOT),
        "environment": {"browser": "system Chromium", "executable": "/usr/bin/chromium", "runner": "Playwright Python", "runtime_integration": False},
        "viewports_css_pixels": {"desktop": "1920x1080", "tablet": "768x1024", "android_emulation": "390x844"},
        "summary": {"checks": len(CHECKS), "passed": sum(c["status"] == "PASS" for c in CHECKS), "failed": sum(c["status"] == "FAIL" for c in CHECKS)},
        "checks": CHECKS,
        "network_requests": NETWORK_REQUESTS,
        "console_errors": CONSOLE_ERRORS,
        "page_errors": PAGE_ERRORS,
        "screenshot_files": [
            "02_EVIDENCE/screenshots/ui-only-desktop-1920x1080.png",
            "02_EVIDENCE/screenshots/ui-only-tablet-768x1024.png",
            "02_EVIDENCE/screenshots/ui-only-android-emulation-390x844.png",
        ],
        "limits": [
            "Screenshots show only the local TEST_ONLY UI opened from file://; they are not evidence of Browser Runtime, an external website, or a real agent.",
            "Android coverage is Playwright device emulation, not a physical Android device.",
            "This automated audit is not a screen-reader/assistive-technology certification or independent Xu review.",
            "The optional HTTP preview server was not started; its HTTP health route/backend isolation were not exercised.",
        ],
    }
    report["status"] = "PASS" if report["summary"]["failed"] == 0 else "FAIL"
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["summary"]["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
