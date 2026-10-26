"""Quality gate — fail closed; never invent PASS."""
from __future__ import annotations
import json
import shutil
import subprocess
from pathlib import Path
from .models import JobState, VideoProject

def ffprobe_json(path: Path) -> dict:
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe not available")
    proc = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {proc.stderr[-400:]}")
    return json.loads(proc.stdout)

def run_qc(project: VideoProject, tolerance_seconds: float = 1.5) -> VideoProject:
    if project.state != JobState.QC_PENDING:
        raise ValueError(f"QC requires QC_PENDING, got {project.state.value}")
    final = project.artifacts.get("final_video")
    if not final:
        project.state = JobState.BLOCKED
        project.evidence.append({"event": "qc_blocked", "reason": "missing final_video artifact"})
        raise RuntimeError("QC blocked: no final_video")
    path = Path(final)
    if not path.is_file() or path.stat().st_size < 100:
        project.state = JobState.FAILED
        project.evidence.append({"event": "qc_failed", "reason": "artifact missing or too small"})
        raise RuntimeError("QC failed: artifact invalid")
    try:
        meta = ffprobe_json(path)
    except Exception as exc:
        project.state = JobState.FAILED
        project.evidence.append({"event": "qc_failed", "reason": "ffprobe_error", "error_type": type(exc).__name__})
        raise
    duration = float(meta.get("format", {}).get("duration") or 0)
    expected = float(project.brief.duration_seconds)
    streams = meta.get("streams") or []
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    ok = has_video and abs(duration - expected) <= tolerance_seconds
    project.evidence.append({
        "event": "qc_result",
        "duration": duration,
        "expected": expected,
        "has_video": has_video,
        "has_audio": has_audio,
        "pass": ok,
    })
    if not ok:
        project.state = JobState.FAILED
        raise RuntimeError(f"QC failed: duration={duration} expected={expected} video={has_video}")
    project.state = JobState.READY_FOR_REVIEW
    return project
