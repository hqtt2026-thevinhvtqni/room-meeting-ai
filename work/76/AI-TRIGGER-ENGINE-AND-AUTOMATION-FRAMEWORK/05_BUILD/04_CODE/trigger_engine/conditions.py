"""Work 76 typed condition evaluator (deterministic, no arbitrary code).

Implements the DOC-004 typed AST contract:
- fixed operator allow-list, strict node validation (unknown keys, arity,
  depth/node limits, non-finite numbers rejected),
- missing is distinct from explicit null (regression W76-CE-002),
- timezone-aware normalization to UTC (W76-CE-001),
- relative window uses a documented UTC reference clock with inclusive
  bounds (W76-CE-003),
- explicit since/until window requires aware timestamps and a non-inverted
  range (W76-CE-004).

Evaluation result is a typed outcome: MATCH / NO_MATCH / INVALID / ERROR,
never a bare boolean.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

from .errors import ConditionEvaluationError, ConditionValidationError

MAX_DEPTH = 20
MAX_NODES = 200
COMPARE_OPS = ("EQ", "NE", "LT", "LTE", "GT", "GTE")

MISSING = object()  # sentinel: field absent from the evaluation scope


@dataclass(frozen=True)
class ConditionResult:
    outcome: str  # MATCH | NO_MATCH | INVALID | ERROR
    reason_code: str
    evaluated_at: datetime
    evaluator_version: str = "w76-cond-1.0.0"


def normalize_utc(value: datetime) -> datetime:
    """Normalize an aware datetime to UTC; reject naive datetimes (W76-CE-001)."""
    if not isinstance(value, datetime):
        raise ConditionValidationError("expected a datetime value")
    if value.tzinfo is None:
        raise ConditionValidationError(
            "naive datetime is not allowed; supply an explicit UTC offset"
        )
    return value.astimezone(timezone.utc)


def _parse_iso(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise ConditionValidationError(f"{field} must be an ISO 8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ConditionValidationError(f"{field} is not a valid ISO 8601 timestamp") from exc
    return normalize_utc(parsed)


def _validate_node(node: Any, depth: int, counter: list) -> None:
    if depth > MAX_DEPTH:
        raise ConditionValidationError("condition AST exceeds maximum depth")
    counter[0] += 1
    if counter[0] > MAX_NODES:
        raise ConditionValidationError("condition AST exceeds maximum node count")
    if not isinstance(node, Mapping):
        raise ConditionValidationError("condition node must be an object")
    ntype = node.get("type")
    if not isinstance(ntype, str):
        raise ConditionValidationError("condition node requires a string 'type'")

    if ntype == "literal":
        if set(node.keys()) - {"type", "value", "value_type"}:
            raise ConditionValidationError("literal node has unknown keys")
        value = node.get("value", MISSING)
        if value is MISSING:
            raise ConditionValidationError("literal node requires 'value'")
        if isinstance(value, float) and not math.isfinite(value):
            raise ConditionValidationError("literal numeric value must be finite")
        return
    if ntype == "field":
        if set(node.keys()) - {"type", "path"}:
            raise ConditionValidationError("field node has unknown keys")
        path = node.get("path")
        if not isinstance(path, str) or not path.strip():
            raise ConditionValidationError("field node requires a non-empty 'path'")
        return
    if ntype == "compare":
        if set(node.keys()) - {"type", "op", "left", "right"}:
            raise ConditionValidationError("compare node has unknown keys")
        # Missing operands are malformed AST, never null literals (W76-CE-002).
        if "left" not in node or "right" not in node:
            raise ConditionValidationError("compare node requires 'left' and 'right' operands")
        if node.get("op") not in COMPARE_OPS:
            raise ConditionValidationError(f"compare op must be one of {COMPARE_OPS}")
        _validate_node(node["left"], depth + 1, counter)
        _validate_node(node["right"], depth + 1, counter)
        return
    if ntype in ("and", "or"):
        if set(node.keys()) - {"type", "operands"}:
            raise ConditionValidationError(f"{ntype} node has unknown keys")
        operands = node.get("operands")
        if "operands" not in node or not isinstance(operands, list) or len(operands) < 2:
            raise ConditionValidationError(f"{ntype} node requires at least two operands")
        for operand in operands:
            _validate_node(operand, depth + 1, counter)
        return
    if ntype == "not":
        if set(node.keys()) - {"type", "operand"}:
            raise ConditionValidationError("not node has unknown keys")
        if "operand" not in node:
            raise ConditionValidationError("not node requires 'operand'")
        _validate_node(node["operand"], depth + 1, counter)
        return
    if ntype == "exists":
        if set(node.keys()) - {"type", "path"}:
            raise ConditionValidationError("exists node has unknown keys")
        if not isinstance(node.get("path"), str):
            raise ConditionValidationError("exists node requires a string 'path'")
        return
    if ntype == "in":
        if set(node.keys()) - {"type", "left", "values"}:
            raise ConditionValidationError("in node has unknown keys")
        if "left" not in node or "values" not in node:
            raise ConditionValidationError("in node requires 'left' and 'values'")
        if not isinstance(node.get("values"), list) or not node["values"]:
            raise ConditionValidationError("in node requires a non-empty 'values' list")
        _validate_node(node["left"], depth + 1, counter)
        return
    if ntype == "time_window":
        if set(node.keys()) - {"type", "last_seconds", "since", "until", "path"}:
            raise ConditionValidationError("time_window node has unknown keys")
        if "last_seconds" in node:
            last = node["last_seconds"]
            if isinstance(last, bool) or not isinstance(last, (int, float)) or not math.isfinite(last) or last <= 0:
                raise ConditionValidationError("last_seconds must be a positive finite number")
            return
        if "since" in node or "until" in node:
            if "since" not in node or "until" not in node:
                raise ConditionValidationError("explicit time_window requires both 'since' and 'until'")
            return
        raise ConditionValidationError("time_window requires 'last_seconds' or 'since'/'until'")
    raise ConditionValidationError(f"unknown condition node type: {ntype}")


def _resolve_path(scope: Mapping[str, Any], path: str) -> Any:
    current: Any = scope
    for part in path.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        else:
            return MISSING
    return current


def _coerce_pair(left: Any, right: Any) -> tuple:
    """Coerce ISO strings to datetimes when compared against datetimes."""
    if isinstance(left, datetime) and isinstance(right, str):
        return left, _parse_iso(right, "comparison operand")
    if isinstance(right, datetime) and isinstance(left, str):
        return _parse_iso(left, "comparison operand"), right
    return left, right


def _compare(op: str, left: Any, right: Any) -> bool:
    left, right = _coerce_pair(left, right)
    if left is MISSING or right is MISSING:
        # A missing operand can never satisfy a comparison (missing != null).
        return False
    both_datetime = isinstance(left, datetime) and isinstance(right, datetime)
    if both_datetime:
        left = normalize_utc(left)
        right = normalize_utc(right)
    numeric = (int, float)
    left_is_num = isinstance(left, numeric) and not isinstance(left, bool)
    right_is_num = isinstance(right, numeric) and not isinstance(right, bool)
    if left_is_num != right_is_num and not (left is None or right is None):
        if op == "EQ":
            return False
        if op == "NE":
            return True
        raise ConditionEvaluationError("ordered comparison between mismatched types")
    if isinstance(left, bool) != isinstance(right, bool) and not both_datetime:
        if op == "EQ":
            return False
        if op == "NE":
            return True
        raise ConditionEvaluationError("ordered comparison between mismatched types")
    if op == "EQ":
        return left == right
    if op == "NE":
        return left != right
    try:
        if op == "LT":
            return left < right
        if op == "LTE":
            return left <= right
        if op == "GT":
            return left > right
        if op == "GTE":
            return left >= right
    except TypeError as exc:
        raise ConditionEvaluationError("ordered comparison failed") from exc
    raise ConditionEvaluationError(f"unsupported operator: {op}")


def _eval_node(node: Mapping[str, Any], scope: Mapping[str, Any], event_time: datetime, now: datetime) -> Any:
    ntype = node["type"]
    if ntype == "literal":
        return node["value"]
    if ntype == "field":
        return _resolve_path(scope, node["path"])
    if ntype == "compare":
        return _compare(
            node["op"],
            _eval_node(node["left"], scope, event_time, now),
            _eval_node(node["right"], scope, event_time, now),
        )
    if ntype == "and":
        return all(bool(_eval_node(o, scope, event_time, now)) for o in node["operands"])
    if ntype == "or":
        return any(bool(_eval_node(o, scope, event_time, now)) for o in node["operands"])
    if ntype == "not":
        return not bool(_eval_node(node["operand"], scope, event_time, now))
    if ntype == "exists":
        return _resolve_path(scope, node["path"]) is not MISSING
    if ntype == "in":
        left = _eval_node(node["left"], scope, event_time, now)
        if left is MISSING:
            return False
        return any(_compare("EQ", left, v) for v in node["values"])
    if ntype == "time_window":
        return _eval_time_window(node, event_time, now)
    raise ConditionEvaluationError(f"unknown node type: {ntype}")


def _eval_time_window(node: Mapping[str, Any], event_time: datetime, now: datetime) -> bool:
    """Time-window semantics (documented for W76-CE-003/004).

    Reference clock is the injected 'now' (UTC), never the event timestamp:
    a relative window is [now - last_seconds, now], inclusive on both ends.
    Stale (older than the window) and future (later than 'now') events are
    rejected. Explicit windows are [since, until] inclusive; both bounds are
    required, must be timezone-aware and since <= until.
    """
    event_utc = normalize_utc(event_time)
    if "last_seconds" in node:
        seconds = float(node["last_seconds"])
        if not math.isfinite(seconds) or seconds <= 0:
            raise ConditionValidationError("last_seconds must be a positive finite number")
        since = now - timedelta(seconds=seconds)
        return since <= event_utc <= now
    since = _parse_iso(node["since"], "since")
    until = _parse_iso(node["until"], "until")
    if since > until:
        raise ConditionValidationError("time_window 'since' must not be later than 'until'")
    return since <= event_utc <= until


def evaluate(
    condition: Any,
    scope: Mapping[str, Any],
    event_time: datetime,
    now: datetime | None = None,
) -> ConditionResult:
    """Validate and evaluate a condition AST against a field scope.

    Returns a typed ConditionResult. Malformed AST yields INVALID (never a
    silent match); runtime failures yield ERROR.
    """
    evaluated_at = normalize_utc(now) if now is not None else datetime.now(timezone.utc)
    try:
        _validate_node(condition, 0, [0])
        event_utc = normalize_utc(event_time)
        result = bool(_eval_node(condition, scope, event_utc, evaluated_at))
        return ConditionResult(
            outcome="MATCH" if result else "NO_MATCH",
            reason_code="OK",
            evaluated_at=evaluated_at,
        )
    except ConditionValidationError as exc:
        return ConditionResult(outcome="INVALID", reason_code=str(exc), evaluated_at=evaluated_at)
    except ConditionEvaluationError as exc:
        return ConditionResult(outcome="ERROR", reason_code=str(exc), evaluated_at=evaluated_at)
