from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class JobState(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    GENERATING = "GENERATING"
    RENDERING = "RENDERING"
    QC_PENDING = "QC_PENDING"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    EXPORTED = "EXPORTED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

@dataclass
class VideoBrief:
    title: str
    goal: str
    duration_seconds: int = 30
    aspect_ratio: str = "9:16"
    language: str = "vi-VN"
    audience: str = "general"
    brand_name: str | None = None
    spend_limit_credits: float = 0
    allow_paid_generation: bool = False

    def validate(self) -> None:
        if not self.title.strip() or not self.goal.strip():
            raise ValueError("title and goal are required")
        if not 5 <= self.duration_seconds <= 180:
            raise ValueError("duration_seconds must be between 5 and 180")
        if self.aspect_ratio not in {"9:16", "16:9", "1:1", "4:5"}:
            raise ValueError("unsupported aspect_ratio")
        if self.spend_limit_credits < 0:
            raise ValueError("spend_limit_credits cannot be negative")
        if self.allow_paid_generation and self.spend_limit_credits <= 0:
            raise ValueError("paid generation requires a positive spend limit")

@dataclass
class Shot:
    shot_id: str
    duration_seconds: int
    visual_prompt: str
    narration: str
    asset_refs: list[str] = field(default_factory=list)

@dataclass
class VideoProject:
    project_id: str
    brief: VideoBrief
    state: JobState = JobState.DRAFT
    shots: list[Shot] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
