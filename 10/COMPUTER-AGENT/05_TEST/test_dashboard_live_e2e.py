from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "08_DASHBOARD"
API_SCRIPT = ROOT / "04_CODE" / "agent_api.py"
API_URL = "http://127.0.0.1:8787"
DASH_URL = "http://127.0.0.1:3010"
TOKEN = "w10-dashboard-live-test-token"


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"  PASS  {label}")


def wait_for_api(process: subprocess.Popen, timeout: float = 20.0) -> dict:
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Agent API exited early with code {process.returncode}")
        try:
            with urllib.request.urlopen(f"{API_URL}/health", timeout=1) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if response.status == 200 and payload.get("work_id") == "10":
                    return payload
        except Exception as exc:  # bounded startup retry
            last_error = exc
        time.sleep(0.1)
    raise TimeoutError(f"Agent API health did not become ready: {last_error}")


def stop_process(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> None:
    env = os.environ.copy()
    env.update({
        "COMPUTER_AGENT_API_TOKEN": TOKEN,
        "COMPUTER_AGENT_ALLOWED_ORIGINS": "http://127.0.0.1:3010",
        "COMPUTER_AGENT_WORK_ID": "10",
        "COMPUTER_AGENT_HOST_WRITABLE_ROOTS": "",
        "COMPUTER_AGENT_HOST_POWERSHELL_ROOTS": "",
    })
    api = dashboard = None
    try:
        api = subprocess.Popen(
            [sys.executable, str(API_SCRIPT)],
            cwd=str(ROOT), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        health = wait_for_api(api)
        check("local Agent API health identifies Work 10", str(health.get("work_id")) == "10")

        dashboard = subprocess.Popen(
            [sys.executable, "-m", "http.server", "3010", "--bind", "127.0.0.1", "--directory", str(DASHBOARD)],
            cwd=str(ROOT), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(DASH_URL, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_function(
                    "() => document.querySelector('#healthLabel')?.textContent.includes('CONNECTED')",
                    timeout=15000,
                )
                check("Dashboard live health fetch connects cross-origin to Agent API", "CONNECTED" in page.locator("#healthLabel").inner_text())
                check("Dashboard renders the correct Work ID", page.locator("#workId").inner_text().strip() == "10")

                page.locator("#apiToken").fill(TOKEN)
                page.locator("#task").fill("Dashboard live health and consent smoke test")
                page.locator("#actions").fill('[{"type":"observe"}]')
                page.locator("#verification").fill('{"checks":[{"field":"text","contains":"Work 10"}]}')
                check("Execute remains disabled before explicit consent", page.locator("#run").is_disabled())
                page.locator("#confirmReal").check()
                check("Execute enables only after health, token and explicit consent", not page.locator("#run").is_disabled())

                page.locator("#clear").click()
                check("Clear removes the in-memory bearer token", page.locator("#apiToken").input_value() == "")
                check("Clear resets explicit consent and disables Execute", not page.locator("#confirmReal").is_checked() and page.locator("#run").is_disabled())
                print("Dashboard live E2E: 6 checks passed")
            finally:
                browser.close()
    finally:
        stop_process(dashboard)
        stop_process(api)


if __name__ == "__main__":
    main()
