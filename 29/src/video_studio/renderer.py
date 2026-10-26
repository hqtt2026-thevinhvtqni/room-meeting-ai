"""FFmpeg renderer for MVP fixtures — deterministic color clips + concat."""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from .models import JobState, VideoProject

ASPECT = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
}

def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr[-800:]}")

def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

def render_project(project: VideoProject, output_dir: Path) -> Path:
    if project.state not in (JobState.QC_PENDING, JobState.GENERATING, JobState.PLANNED):
        # allow render after mock gen (QC_PENDING) or after plan with fixtures
        if project.state not in (JobState.QC_PENDING,):
            raise ValueError(f"render requires QC_PENDING after generation, got {project.state.value}")
    if not ffmpeg_available():
        project.state = JobState.BLOCKED
        project.evidence.append({"event": "render_blocked", "reason": "ffmpeg/ffprobe not available"})
        raise RuntimeError("ffmpeg/ffprobe not available")
    if not project.shots:
        raise ValueError("no shots to render")
    output_dir.mkdir(parents=True, exist_ok=True)
    project.state = JobState.RENDERING
    w, h = ASPECT.get(project.brief.aspect_ratio, (1080, 1920))
    clip_paths: list[Path] = []
    colors = ["blue", "green", "red", "orange", "purple"]
    try:
        for i, shot in enumerate(project.shots):
            clip = output_dir / f"{shot.shot_id}.mp4"
            color = colors[i % len(colors)]
            _run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"color=c={color}:s={w}x{h}:d={max(shot.duration_seconds, 1)}",
                "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
                "-t", str(max(shot.duration_seconds, 1)),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                "-shortest", str(clip),
            ])
            clip_paths.append(clip)
        # concat
        list_file = output_dir / "concat.txt"
        list_file.write_text("".join(f"file '{p.name}'\n" for p in clip_paths), encoding="utf-8")
        final = output_dir / f"{project.project_id}_final.mp4"
        _run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c", "copy", str(final),
        ])
        digest = hashlib.sha256(final.read_bytes()).hexdigest()
        project.artifacts["final_video"] = str(final)
        project.evidence.append({
            "event": "render_complete",
            "path": str(final),
            "sha256": digest,
            "bytes": final.stat().st_size,
        })
        project.state = JobState.QC_PENDING
        return final
    except Exception as exc:
        project.state = JobState.FAILED
        project.evidence.append({"event": "render_failed", "error_type": type(exc).__name__})
        raise
