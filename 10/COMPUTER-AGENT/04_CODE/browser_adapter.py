from __future__ import annotations
from pathlib import Path
from typing import Any

class BrowserAdapter:
    def start(self) -> None: raise NotImplementedError
    def observe(self) -> dict: raise NotImplementedError
    def navigate(self, url: str) -> dict: raise NotImplementedError
    def click(self, target: str) -> dict: raise NotImplementedError
    def type(self, target: str, text: str) -> dict: raise NotImplementedError
    def key_press(self, key: str) -> dict: raise NotImplementedError
    def scroll(self, amount: int = 700) -> dict: raise NotImplementedError
    def wait(self, seconds: float = 1) -> dict: raise NotImplementedError
    def extract(self, target: str | None = None) -> dict: raise NotImplementedError
    def screenshot(self, path: str | None = None) -> dict: raise NotImplementedError
    def download(self, target: str) -> dict: raise NotImplementedError
    def close(self) -> None: raise NotImplementedError


class PlaywrightBrowserAdapter(BrowserAdapter):
    _KEY_ALIASES = {
        "TAB": "Tab",
        "ENTER": "Enter",
        "RETURN": "Enter",
        "ESC": "Escape",
        "ESCAPE": "Escape",
        "SPACE": " ",
        "BACKSPACE": "Backspace",
        "DELETE": "Delete",
        "ARROWUP": "ArrowUp",
        "ARROWDOWN": "ArrowDown",
        "ARROWLEFT": "ArrowLeft",
        "ARROWRIGHT": "ArrowRight",
        "HOME": "Home",
        "END": "End",
        "PAGEUP": "PageUp",
        "PAGEDOWN": "PageDown",
    }

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page(accept_downloads=True)
        return {"started": True, "url": self.page.url}

    def _ensure(self):
        if self.page is None:
            self.start()
        return self.page

    def _default_evidence_dir(self) -> Path:
        # Anchor to Work 10 evidence dir regardless of current working directory.
        return Path(__file__).resolve().parents[1] / "06_EVIDENCE"

    def observe(self):
        p = self._ensure()
        return {"url": p.url, "title": p.title(), "text": p.locator("body").inner_text(timeout=3000)[:12000]}

    def navigate(self, url):
        p = self._ensure()
        p.goto(url, wait_until="domcontentloaded")
        return self.observe()

    def _locator(self, target):
        p = self._ensure()
        # Explicit selector first; accessible role/text fallback is deliberately limited.
        if target.startswith(("css=", "xpath=", "text=")):
            return p.locator(target)
        return p.get_by_role("button", name=target).or_(p.get_by_text(target, exact=True))

    def click(self, target):
        loc = self._locator(target)
        loc.first.click()
        return {"clicked": target, "url": self.page.url}

    def type(self, target, text):
        p = self._ensure()
        if target.startswith(("css=", "xpath=")):
            loc = p.locator(target)
        else:
            # Label-first resolution. Never pass raw label text through locator():
            # labels with special characters (e.g. "Task #1") are invalid CSS and
            # would raise even when get_by_label matches.
            loc = (p.get_by_label(target)
                   .or_(p.get_by_placeholder(target))
                   .or_(p.get_by_role("textbox", name=target)))
        loc.first.fill(text)
        return {"typed": text, "target": target}

    def key_press(self, key):
        p = self._ensure()
        normalized = self._KEY_ALIASES.get(str(key).upper(), key)
        p.keyboard.press(normalized)
        return {"key": key, "normalized_key": normalized}

    def scroll(self, amount=700):
        self._ensure().mouse.wheel(0, amount)
        return {"scrolled": amount}

    def wait(self, seconds=1):
        self._ensure().wait_for_timeout(int(seconds * 1000))
        return {"waited_seconds": seconds}

    def extract(self, target=None):
        p = self._ensure()
        loc = p.locator(target) if target else p.locator("body")
        return {"target": target, "text": loc.first.inner_text(timeout=3000)[:12000]}

    def screenshot(self, path=None):
        p = self._ensure()
        if path:
            out = Path(path)
            if not out.is_absolute():
                out = self._default_evidence_dir() / out
        else:
            out = self._default_evidence_dir() / "latest.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        p.screenshot(path=str(out), full_page=True)
        return {"path": str(out)}

    def download(self, target):
        p = self._ensure()
        with p.expect_download() as info:
            self.click(target)
        d = info.value
        path = d.path()
        return {"suggested_filename": d.suggested_filename, "temp_path": str(path)}

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.browser = self.playwright = self.page = None
