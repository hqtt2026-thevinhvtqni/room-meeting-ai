"""Opt-in live Browser Adapter E2E against a job-owned disposable meeting."""

import os

import pytest
import requests


REQUIRED_ENV = (
    "ROOMHOP_TEST_MEETINGS_DIR",
    "ROOMHOP_TEST_MODE",
    "ROOMHOP_TEST_MEETING_ID",
    "ROOMHOP_TEST_IDENTITY_ID",
    "ROOMHOP_BROWSER_ADAPTER_PORT",
)

pytestmark = pytest.mark.skipif(
    os.getenv("ROOMHOP_TEST_MODE") != "1"
    or any(not os.getenv(name) for name in REQUIRED_ENV),
    reason="requires an explicitly configured job-owned disposable ROOM-HOP target",
)

PORT = int(os.getenv("ROOMHOP_BROWSER_ADAPTER_PORT", "0"))
BASE = f"http://127.0.0.1:{PORT}"


def test_browser_workflow_handoff_and_readback():
    """Run only against the explicitly provisioned disposable fixture."""
    assert 1 <= PORT <= 65535
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

    response = requests.post(
        BASE + "/browser/execute_workflow",
        json=req,
        timeout=60,
    )
    assert response.ok, response.text
    data = response.json()
    assert data["ok"] is True
    assert "wikipedia.org/wiki/Headless_browser" in data["final_url"]
    assert data["page_title"].endswith(" - Wikipedia")

    submission = data["roomhop_submission"]
    assert submission["status"] == "pass", submission
    assert submission["read_back"] is True
    assert submission["transport"] == "stdio"
    assert submission["meeting_id"] == os.environ["ROOMHOP_TEST_MEETING_ID"]
    assert submission["identity_id"] == os.environ["ROOMHOP_TEST_IDENTITY_ID"]
