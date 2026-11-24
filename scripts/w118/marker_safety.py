"""Conservative Markdown fenced-code detection for canonical marker lines.

This parser intentionally fails closed on an unclosed fence. A closing fence
must use the same character as its opener, contain at least as many fence
characters, and have no trailing non-whitespace content.
"""
from __future__ import annotations

import re

_OPEN_FENCE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
_CLOSING_CANDIDATE = re.compile(r"^( {0,3})([`~]+)[ \t]*$")


def has_exact_standalone_marker(body: str, marker: str) -> bool:
    """True only for one exact marker line outside all Markdown code fences."""
    if not isinstance(body, str) or not isinstance(marker, str) or not marker:
        return False
    if body.count(marker) != 1:
        return False

    fence_char: str | None = None
    fence_length = 0
    found = 0

    for line in body.splitlines():
        if fence_char is not None:
            closing = _CLOSING_CANDIDATE.fullmatch(line)
            if closing:
                run = closing.group(2)
                if set(run) == {fence_char} and len(run) >= fence_length:
                    fence_char = None
                    fence_length = 0
                    continue
            # Fence-like lines inside a fence are content unless they satisfy
            # the exact closing-fence rule above.
            if line == marker:
                return False
            continue

        opening = _OPEN_FENCE.fullmatch(line)
        if opening:
            run = opening.group(2)
            info = opening.group(3)
            # CommonMark disallows backticks in a backtick-fence info string.
            # Treat this malformed opener conservatively as a fence anyway.
            fence_char = run[0]
            fence_length = len(run)
            continue

        if line == marker:
            found += 1

    # An unmatched opener makes the remainder ambiguous; fail closed.
    return found == 1 and fence_char is None
