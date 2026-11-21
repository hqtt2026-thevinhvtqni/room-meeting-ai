from __future__ import annotations

from pathlib import Path
from typing import Any
import uuid


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

    def observe(self):
        p = self._ensure()
        return {
            "url": p.url,
            "title": p.title(),
            "text": p.locator("body").inner_text(timeout=3000)[:12000],
        }

    def navigate(self, url):
        p = self._ensure()
        p.goto(url, wait_until="domcontentloaded")
        return self.observe()

    def _selector_locator(self, target):
        p = self._ensure()
        return p.locator(target)

    def _locator(self, target):
        """Resolve a click target deterministically: explicit selector first,
        then button role, then link role, then exact text."""
        p = self._ensure()
        if target.startswith(("css=", "xpath=", "text=", "#", ".", "[")):
            return self._selector_locator(target)
        return (
            p.get_by_role("button", name=target)
            .or_(p.get_by_role("link", name=target))
            .or_(p.get_by_text(target, exact=True))
        )

    def click(self, target):
        loc = self._locator(target)
        loc.first.click()
        return {"clicked": target, "url": self.page.url}

    def type(self, target, text):
        p = self._ensure()
        if target.startswith(("css=", "xpath=", "#", ".", "[")):
            loc = p.locator(target)
        else:
            loc = p.get_by_label(target).or_(p.get_by_placeholder(target)).or_(p.locator(target))
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
        self._ensure().wait_for_timeout(int(float(seconds) * 1000))
        return {"waited_seconds": seconds}

    def extract(self, target=None):
        p = self._ensure()
        loc = p.locator(target) if target else p.locator("body")
        return {"target": target, "text": loc.first.inner_text(timeout=3000)[:12000]}

    def _evidence_path(self, path=None) -> Path:
        """Resolve a screenshot destination strictly inside Work/06_EVIDENCE."""
        evidence_root = (Path(__file__).resolve().parents[1] / "06_EVIDENCE").resolve()
        if path is None:
            candidate = evidence_root / "latest.png"
        else:
            raw = Path(str(path)).expanduser()
            if raw.is_absolute():
                candidate = raw.resolve()
            elif raw.parts and raw.parts[0].casefold() == "06_evidence":
                candidate = (evidence_root.parent / raw).resolve()
            elif len(raw.parts) == 1:
                # Bare filenames default into Evidence. Nested relative paths
                # are Work-relative and must explicitly start with 06_EVIDENCE/.
                candidate = (evidence_root / raw).resolve()
            else:
                candidate = (evidence_root.parent / raw).resolve()
        try:
            candidate.relative_to(evidence_root)
        except ValueError:
            raise ValueError("screenshot path must remain inside Work/06_EVIDENCE") from None
        if candidate == evidence_root:
            raise ValueError("screenshot path must name a file inside Work/06_EVIDENCE")
        return candidate

    def screenshot(self, path=None):
        p = self._ensure()
        destination = self._evidence_path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        p.screenshot(path=str(destination), full_page=True)
        return {"path": str(destination)}

    def _download_destination(self, suggested_filename: str | None) -> Path:
        # Treat provider-supplied filenames as untrusted labels, never as paths.
        filename = str(suggested_filename or "download.bin").replace("\\", "/").split("/")[-1]
        # Colon enables NTFS alternate data streams; reject it before sanitizing.
        if ":" in filename or "\x00" in filename:
            raise ValueError("download filename is invalid")
        filename = filename.rstrip(" .")
        filename = "".join("_" if ord(ch) < 32 or ch in '<>|?*' else ch for ch in filename)[:180]
        if not filename or filename in {".", ".."}:
            raise ValueError("download filename is invalid")
        destination = self._evidence_path(f"06_EVIDENCE/{uuid.uuid4().hex}_{filename}")
        return destination

    def download(self, target):
        p = self._ensure()
        with p.expect_download() as info:
            self._locator(target).first.click()
        download = info.value
        destination = self._download_destination(download.suggested_filename)
        destination.parent.mkdir(parents=True, exist_ok=True)
        download.save_as(str(destination))
        return {
            "suggested_filename": download.suggested_filename,
            "path": str(destination),
        }

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.browser = self.playwright = self.page = None
