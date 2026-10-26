import json
from pathlib import Path
import pytest
from video_studio.models import JobState, VideoBrief
from video_studio.pipeline import (
    FailingProvider, create_project, plan_project, run_mock_generation,
    run_offline_e2e, run_quality_gate, run_render,
)
from video_studio.renderer import ffmpeg_available

def brief(**kwargs):
    values = {"title": "Demo", "goal": "Introduce a product", "duration_seconds": 30}
    values.update(kwargs)
    return VideoBrief(**values)

def test_plan_and_mock_generation_e2e(tmp_path: Path):
    project = create_project("test-001", brief())
    plan_project(project)
    assert project.state == JobState.PLANNED
    assert sum(s.duration_seconds for s in project.shots) == 30
    run_mock_generation(project, tmp_path)
    assert project.state == JobState.QC_PENDING
    assert len(project.artifacts) == len(project.shots)
    for artifact in project.artifacts.values():
        payload = json.loads(Path(artifact).read_text(encoding="utf-8"))
        assert payload["provider"] == "mock"

def test_invalid_duration_rejected():
    with pytest.raises(ValueError):
        create_project("bad", brief(duration_seconds=2))

def test_invalid_aspect_rejected():
    with pytest.raises(ValueError):
        create_project("bad", brief(aspect_ratio="2:3"))

def test_paid_generation_requires_positive_ceiling():
    with pytest.raises(ValueError):
        create_project("paid", brief(allow_paid_generation=True))

def test_mock_runner_does_not_call_paid_provider(tmp_path: Path):
    project = create_project("test-paid", brief(allow_paid_generation=True, spend_limit_credits=10))
    plan_project(project)
    with pytest.raises(RuntimeError, match="refuses to enable paid"):
        run_mock_generation(project, tmp_path)
    assert project.state == JobState.PLANNED

def test_provider_error_marks_failed(tmp_path: Path):
    project = create_project("fail-prov", brief())
    plan_project(project)
    with pytest.raises(RuntimeError, match="simulated"):
        run_mock_generation(project, tmp_path, provider=FailingProvider())
    assert project.state == JobState.FAILED
    assert any(e.get("event") == "generation_failed" for e in project.evidence)

def test_cannot_plan_twice():
    project = create_project("twice", brief())
    plan_project(project)
    with pytest.raises(ValueError):
        plan_project(project)

@pytest.mark.skipif(not ffmpeg_available(), reason="ffmpeg/ffprobe not installed")
def test_offline_e2e_render_and_qc(tmp_path: Path):
    project = run_offline_e2e("e2e-001", brief(duration_seconds=6), tmp_path)
    assert project.state == JobState.READY_FOR_REVIEW
    final = Path(project.artifacts["final_video"])
    assert final.is_file() and final.stat().st_size > 1000
    assert any(e.get("event") == "qc_result" and e.get("pass") is True for e in project.evidence)
    assert any(e.get("sha256") for e in project.evidence if e.get("event") == "render_complete")

@pytest.mark.skipif(not ffmpeg_available(), reason="ffmpeg/ffprobe not installed")
def test_qc_fails_without_final(tmp_path: Path):
    project = create_project("no-final", brief(duration_seconds=6))
    plan_project(project)
    run_mock_generation(project, tmp_path)
    with pytest.raises(RuntimeError, match="no final_video"):
        run_quality_gate(project)
    assert project.state == JobState.BLOCKED
