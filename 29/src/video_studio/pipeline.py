from __future__ import annotations
import json
from pathlib import Path
from .models import JobState, VideoBrief, VideoProject
from .planner import plan_shots
from .renderer import render_project
from .qc import run_qc

class MockProvider:
    """Deterministic test provider. Never spends credits or calls external services."""
    name = "mock"

    def generate_shot(self, project: VideoProject, shot_id: str, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{shot_id}.mock.json"
        path.write_text(json.dumps({
            "provider": self.name,
            "project_id": project.project_id,
            "shot_id": shot_id,
            "note": "fixture only; not a video file"
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

class FailingProvider:
    name = "failing"
    def generate_shot(self, project: VideoProject, shot_id: str, output_dir: Path) -> Path:
        raise RuntimeError("simulated provider error")

def create_project(project_id: str, brief: VideoBrief) -> VideoProject:
    brief.validate()
    if brief.allow_paid_generation and brief.spend_limit_credits <= 0:
        raise ValueError("paid generation blocked: spend ceiling required")
    return VideoProject(project_id=project_id, brief=brief)

def plan_project(project: VideoProject) -> VideoProject:
    if project.state != JobState.DRAFT:
        raise ValueError(f"cannot plan project from state {project.state.value}")
    project.shots = plan_shots(project.brief)
    if sum(s.duration_seconds for s in project.shots) != project.brief.duration_seconds:
        raise RuntimeError("storyboard duration does not match brief")
    project.state = JobState.PLANNED
    project.evidence.append({"event": "planned", "shot_count": len(project.shots), "provider": "none"})
    return project

def run_mock_generation(project: VideoProject, output_dir: Path, provider=None) -> VideoProject:
    if project.state != JobState.PLANNED:
        raise ValueError(f"generation requires PLANNED state, got {project.state.value}")
    if project.brief.allow_paid_generation:
        raise RuntimeError("MVP mock runner refuses to enable paid provider calls")
    provider = provider or MockProvider()
    project.state = JobState.GENERATING
    try:
        for shot in project.shots:
            artifact = provider.generate_shot(project, shot.shot_id, output_dir)
            project.artifacts[shot.shot_id] = str(artifact)
        project.state = JobState.QC_PENDING
        project.evidence.append({"event": "mock_generation_complete", "artifact_count": len(project.artifacts)})
    except Exception as exc:
        project.state = JobState.FAILED
        project.evidence.append({"event": "generation_failed", "error_type": type(exc).__name__})
        raise
    return project

def run_render(project: VideoProject, output_dir: Path) -> VideoProject:
    render_project(project, output_dir)
    return project

def run_quality_gate(project: VideoProject) -> VideoProject:
    return run_qc(project)

def run_offline_e2e(project_id: str, brief: VideoBrief, output_dir: Path) -> VideoProject:
    """Brief -> plan -> mock gen -> ffmpeg render -> QC. No paid providers."""
    project = create_project(project_id, brief)
    plan_project(project)
    run_mock_generation(project, output_dir / "shots")
    run_render(project, output_dir / "render")
    run_quality_gate(project)
    return project
