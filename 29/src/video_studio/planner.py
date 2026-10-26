from .models import Shot, VideoBrief

def plan_shots(brief: VideoBrief) -> list[Shot]:
    """Create a deterministic, provider-free storyboard for the MVP."""
    brief.validate()
    count = 3 if brief.duration_seconds < 45 else 5
    base, remainder = divmod(brief.duration_seconds, count)
    shots: list[Shot] = []
    for index in range(count):
        duration = base + (1 if index < remainder else 0)
        if index == 0:
            beat = "Hook: introduce the problem or attention-grabbing idea"
        elif index == count - 1:
            beat = "Closing: clear call to action and brand-safe ending"
        else:
            beat = f"Main message beat {index}"
        brand = f" Brand context: {brief.brand_name}." if brief.brand_name else ""
        shots.append(Shot(
            shot_id=f"shot-{index + 1:02d}",
            duration_seconds=duration,
            visual_prompt=f"{beat}. Goal: {brief.goal}.{brand} Aspect ratio {brief.aspect_ratio}. No generated text; add captions in renderer.",
            narration=f"{beat}. {brief.goal}" if index in (0, count - 1) else brief.goal,
        ))
    return shots
