"""WP17 — Work id equivalence for grant ↔ HTTP allow-list binding.

Canonical HTTP allow-list uses W<number>. Contract/grant payloads may use
either W28 or 28. Equivalence is explicit and fail-closed on ambiguity.
"""
from __future__ import annotations

import re

_W = re.compile(r"^W(\d+)$", re.IGNORECASE)
_DIGITS = re.compile(r"^(\d+)$")


def work_ids_equivalent(left: object, right: object) -> bool:
    if not isinstance(left, str) or not isinstance(right, str):
        return False
    a, b = left.strip(), right.strip()
    if not a or not b:
        return False
    if a == b:
        return True
    if a.upper() == b.upper():
        return True
    ma, mb = _W.fullmatch(a), _W.fullmatch(b)
    da, db = _DIGITS.fullmatch(a), _DIGITS.fullmatch(b)
    if ma and db and ma.group(1) == db.group(1):
        return True
    if mb and da and mb.group(1) == da.group(1):
        return True
    if ma and mb and ma.group(1) == mb.group(1):
        return True
    return False


__all__ = ["work_ids_equivalent"]
