"""Provider adapter contract — no credentials in source; paid calls opt-in only."""
from __future__ import annotations
from pathlib import Path
from typing import Protocol
from .models import VideoProject

class VideoProvider(Protocol):
    name: str
    def generate_shot(self, project: VideoProject, shot_id: str, output_dir: Path) -> Path:
        """Return path to a shot artifact (fixture JSON or media file)."""
        ...

class ProviderError(RuntimeError):
    """Stable provider failure; pipeline must map to FAILED/BLOCKED, not PASS."""
