from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
APP = ROOT / "browser_ui_app.py"
URL = os.environ.get("W14_E2E_URL", "http://127.0.0.1:8766/")
OUT = Path(tempfile.gettempdir()) / "work14-browser-ui-e2e"
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("W14_E2E_KEY") or f"ui-phase4-full-e2e-{int(time.time())}"  # unique per run: a reused key is (correctly) replayed by the ledger
W13_URL = os.environ.get("W13_EXECUTION_HOST_URL", "http://127.0.0.1:8031")


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False


def ensure_w14_runtime() -> subprocess.Popen | None:
    """Start the canonical local W14 UI only when :8766 is not already resident."""
    parsed_host = "127.0.0.1"
    parsed_port = 8766
    if port_open(parsed_host, parsed_port):
        return None
    if not APP.exists():
        raise RuntimeError(f"W14 app source missing: {APP}")
    env = os.environ.copy()
    env["PORT"] = str(parsed_port)
    proc = subprocess.Popen(
        [sys.executable, str(APP)],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        if port_open(parsed_host, parsed_port):
            return proc
        if proc.poll() is not None:
            raise RuntimeError(f"W14 UI exited before binding :{parsed_port} (code={proc.returncode})")
        time.sleep(0.25)
    proc.terminate()
    raise RuntimeError(f"W14 UI did not bind :{parsed_port} within 15 seconds")


def get_json(url: str):
    from urllib.request import urlopen
    with urlopen(url, timeout=5) as response:
        return json.loads(response.read())


def launch_chromium(pw):
    args = ["--no-sandbox"]
    try:
        return pw.chromium.launch(headless=True, args=args)
    except Exception as first_error:
        candidates = [
            os.environ.get("CHROME_PATH"),
            os.environ.get("GOOGLE_CHROME_PATH"),
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            str(Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe"),
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return pw.chromium.launch(headless=True, executable_path=candidate, args=args)
        raise RuntimeError(
            "Chromium is unavailable. Install Playwright Chromium or set CHROME_PATH."
        ) from first_error


def fixture_frame(page):
    locator = page.locator("#page")
    locator.wait_for(state="attached")
    frame = locator.content_frame
    if frame is None:
        raise RuntimeError("W14 real-browser iframe has no content frame")
    frame.locator("body").wait_for(state="visible")
    return frame


def assert_fixture(frame):
    assert frame.locator("#q").is_visible()
    assert frame.locator("#action").is_visible()
    assert frame.locator("#result").inner_text() == "browser-result-good"


w14_proc = ensure_w14_runtime()

try:
    w13_health = get_json(W13_URL + "/health")
    if w13_health.get("status") != "PASS":
        raise RuntimeError(f"W13 /health not PASS: {w13_health}")
    required = ["instance_id", "build_hash", "started_at", "pid", "platform", "bind_address"]
    identity = w13_health.get("runtime_identity") or {}  # W13 /health nests the identity
    missing = [k for k in required if not identity.get(k)]
    if missing:
        raise RuntimeError(f"W13 runtime identity incomplete: missing={missing}")

    with sync_playwright() as pw:
        browser = launch_chromium(pw)
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(URL, wait_until="domcontentloaded")
            page.wait_for_timeout(300)

            frame = fixture_frame(page)
            assert_fixture(frame)

            frame.locator("#q").fill("human-e2e")
            frame.locator("#action").click()
            assert frame.locator("#result").inner_text() == "clicked-result-good"

            frame.locator("a").click()
            page.wait_for_timeout(300)
            frame = fixture_frame(page)
            assert frame.locator("#result").inner_text() == "navigation-good"
            assert frame.locator("#result").inner_text() == "navigation-good"

            page.locator("#back").click()
            page.wait_for_timeout(300)
            frame = fixture_frame(page)
            assert frame.locator("#q").count() == 1
            assert_fixture(frame)

            page.locator("#forward").click()
            page.wait_for_timeout(300)
            frame = fixture_frame(page)
            assert frame.locator("#result").inner_text() == "navigation-good"

            page.locator("#reload").click()
            page.wait_for_timeout(300)
            frame = fixture_frame(page)
            assert frame.locator("#result").inner_text() == "navigation-good"

            page.locator("#key").fill(KEY)
            page.locator("#execute").click()
            page.wait_for_function("() => !/Running/.test(document.querySelector('#execState').textContent)", timeout=180000)
            assert "Completed" in page.locator("#execState").inner_text(), page.locator("#output").inner_text()
            log_text = page.locator("#output").inner_text()
            assert "retest_pass" in log_text and "final_evidence_verification" in log_text, log_text
            state = get_json(URL.rstrip("/") + "/api/state")
            fev = state.get("final_evidence_verification") or {}
            assert fev.get("status") == "PASS", json.dumps(fev)
            assert fev.get("w13_instance_id") == identity["instance_id"], (fev, identity)

            page.get_by_text("DIFF", exact=True).click()
            assert "ui autonomous artifact" in page.locator("#output").inner_text()

            page.get_by_text("PREVIEW", exact=True).click()
            assert "browser-result-good" in page.locator("#output").inner_text()

            page.screenshot(path=str(OUT / "desktop-full.png"), full_page=True)

            page.locator("#execute").click()
            page.wait_for_timeout(800)
            assert "Replayed idempotently" in page.locator("#execState").inner_text()

            mobile = browser.new_page(viewport={"width": 375, "height": 812})
            mobile.goto(URL, wait_until="domcontentloaded")
            mobile.wait_for_timeout(300)
            assert mobile.locator("#command").is_visible()
            assert mobile.get_by_text("DIFF", exact=True).is_visible()
            assert mobile.get_by_text("PREVIEW", exact=True).is_visible()
            mobile.screenshot(path=str(OUT / "mobile.png"), full_page=True)

            result = {
                "status": "PASS",
                "url": URL,
                "w13_health": w13_health,
                "idempotency_key": KEY,
                "w13_identity": identity,
                "final_evidence_verification": fev,
                "human_mode": ["click", "type", "navigate", "back", "forward", "reload"],
                "ai_mode": ["execute", "real_browser_agent", "artifact"],
                "panels": ["diff", "log", "preview"],
                "replay": "REPLAYED_IDEMPOTENTLY",
                "responsive": ["desktop", "mobile"],
                "screenshots": [str(OUT / "desktop-full.png"), str(OUT / "mobile.png")],
            }
            (OUT / "UI_E2E_RESULT.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(json.dumps(result, indent=2))
        finally:
            browser.close()
finally:
    if w14_proc is not None and w14_proc.poll() is None:
        w14_proc.terminate()
        try:
            w14_proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            w14_proc.kill()



