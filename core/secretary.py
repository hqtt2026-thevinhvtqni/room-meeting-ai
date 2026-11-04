from __future__ import annotations

from pathlib import Path

from core.paste_rate_limiter import MAX_PASTE_REQUESTS_PER_WINDOW

MAX_TEXT_BYTES = 1 * 1024 * 1024

class Secretary:
    """
    ROOM HOP Secretary v0.3 — Raw Transcript Record Keeper.

    Nhiem vu duy nhat:
    - append(text): ghi nguyen van mot block text vao transcript.txt
    - read(): doc lai toan bo transcript.txt
    - export(): xuat transcript (hien tai == read())

    Secretary KHONG:
    - nhan dien speaker
    - parse cau lenh
    - sua whitespace
    - doi CRLF thanh LF
    - them timestamp vao transcript
    - them metadata vao transcript
    - tu tao summary
    - giu reference toi Meeting
    - import MeetingManager/Governance/Discussion/IdentityResolution/IntentRouter
    """

    def __init__(self, transcript_path: str | Path = "docs/transcript.txt"):
        self._transcript_path = Path(transcript_path)

    @staticmethod
    def validate_text(text: str) -> str:
        """Normalize and validate the authoritative UTF-8 byte ceiling."""
        text = "" if text is None else str(text)
        text_bytes = len(text.encode("utf-8"))
        if text_bytes > MAX_TEXT_BYTES:
            raise ValueError(
                f"Transcript input exceeds {MAX_TEXT_BYTES} UTF-8 bytes"
            )
        return text

    def append(self, text: str) -> dict:
        # Validate before opening the transcript to prevent partial writes.
        text = self.validate_text(text)
        self._transcript_path.parent.mkdir(parents=True, exist_ok=True)

        # newline="" : khong de Python tu dich CRLF<->LF (universal newline
        # translation). Ban ghi phai giu nguyen dung byte/ky tu xuong dong
        # nhu block dau vao.
        with open(self._transcript_path, "a", encoding="utf-8", newline="") as f:
            f.write(text)

        return {"status": "READY"}

    def read(self) -> str:
        if not self._transcript_path.exists():
            return ""

        with open(self._transcript_path, "r", encoding="utf-8", newline="") as f:
            return f.read()

    def export(self) -> str:
        return self.read()
