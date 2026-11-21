"""Deterministic adapter double used by the offline and HTTP tests.

Test-only: it never touches a browser. It records lifecycle calls so the HTTP
tests can prove the adapter is released even when a workflow fails.
"""
from __future__ import annotations

import os
import threading
import time

LOG_ENV = "COMPUTER_AGENT_FAKE_LOG"
TEXT = "Work 10 REAL E2E\nSUBMITTED\nresult: Work 10 REAL E2E"
URL = "http://127.0.0.1/fake"


def _log(line: str) -> None:
    path = os.getenv(LOG_ENV)
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


class FakeAdapter:
    def __init__(self):
        self.calls = []
        self.closed = False

    def start(self):
        self.calls.append("start")
        _log("start")
        _log(f"start-thread:{threading.get_ident()}")
        return {"started": True, "url": "about:blank"}

    def observe(self):
        self.calls.append("observe")
        return {"url": URL, "title": "Fake", "text": TEXT}

    def navigate(self, url):
        self.calls.append(("navigate", url))
        return {"url": url, "title": "Fake", "text": TEXT}

    def click(self, target):
        self.calls.append(("click", target))
        if target == "slow":
            _log("click-start:slow")
            _log(f"click-start-thread:{threading.get_ident()}")
            time.sleep(float(os.getenv("COMPUTER_AGENT_FAKE_SLOW_CLICK_SECONDS", "0.3")))
            _log("click-end:slow")
            _log(f"click-end-thread:{threading.get_ident()}")
        return {"clicked": target, "url": URL}

    def type(self, target, text):
        self.calls.append(("type", target, text))
        return {"typed": text, "target": target}

    def key_press(self, key):
        self.calls.append(("key", key))
        return {"key": key}

    def scroll(self, amount=700):
        self.calls.append(("scroll", amount))
        return {"scrolled": amount}

    def wait(self, seconds=1):
        self.calls.append(("wait", seconds))
        return {"waited_seconds": seconds}

    def extract(self, target=None):
        self.calls.append(("extract", target))
        return {"target": target, "text": TEXT}

    def screenshot(self, path=None):
        self.calls.append(("screenshot", path))
        return {"path": path or "06_EVIDENCE/fake.png"}

    def download(self, target):
        self.calls.append(("download", target))
        return {"suggested_filename": "evidence.txt", "path": "06_EVIDENCE/fake-evidence.txt"}

    def close(self):
        self.closed = True
        self.calls.append("close")
        _log("close")
        _log(f"close-thread:{threading.get_ident()}")
