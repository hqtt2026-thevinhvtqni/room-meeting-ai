"""Opt-in PC integration test. Never runs against an unspecified meeting."""

import os

import pytest
import requests


REQUIRED_ENV = (
    "ROOMHOP_MCP_URL",
    "ROOMHOP_TEST_MODE",
    "ROOMHOP_TEST_MEETING_ID",
    "ROOMHOP_TEST_IDENTITY_ID",
)

pytestmark = pytest.mark.skipif(
    os.getenv("ROOMHOP_TEST_MODE") != "1"
    or any(not os.getenv(name) for name in REQUIRED_ENV),
    reason="requires an explicitly configured disposable ROOM-HOP test target",
)

BASE = "http://127.0.0.1:8787"


def test_browser_workflow_handoff_and_readback():
    """Run only on a PC with an explicit disposable meeting and test identity."""
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
    assert submission["meeting_id"] == os.environ["ROOMHOP_TEST_MEETING_ID"]
    assert submission["identity_id"] == os.environ["ROOMHOP_TEST_IDENTITY_ID"]
