"""Work 76 — WP-76-04: Typed condition evaluator.

Evaluates a *typed expression tree* (DOC-003 FR-04, DOC-004 §Condition
Evaluator). The evaluator deliberately supports only the node kinds listed in
``NODE_KINDS`` and refuses everything else — there is **no eval(), no exec(),
no attribute traversal, no import machinery and no user-supplied callables**.
This satisfies DOC-006 test group 4 ("reject arbitrary code") and risk R-76-01
(event payload is data, never instruction).

Expression grammar (JSON-friendly dicts)::

    {"op": "and"|"or", "args": [<expr>, ...]}
    {"op": "not", "arg": <expr>}
    {"op": "=="|"!="|"<"|"<="|">"|">=", "left": <value>, "right": <value>}
    {"op": "in", "left": <value>, "right": [<value>, ...]}
    {"op": "exists", "path": "a.b.c"}
    {"op": "const", "value": <literal>}
    {"var": "a.b.c"}                      # resolved from the event context
    {"window": {...}, "arg": <expr>}      # time-window wrapper

Values are typed: scalars (int/float/str/bool/None) and lists of scalars.
Mixed-type comparisons that have no safe ordering (e.g. ``"2" > 1``) raise
:class:`ConditionEvaluationError` instead of silently returning False —
fail closed, per DOC-004 §Security boundaries.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

from .errors import ConditionEvaluationError
from .models import iso, parse_iso, utcnow

NODE_KINDS = frozenset(
    {"and", "or", "not", "==", "!=", "<", "<=", ">", ">=", "in", "exists", "const", "var", "window"}
)

_COMPARISONS = ("<", "<=", ">", ">=")

_SCALAR_TYPES = (int, float, str, bool, type(None))


def _is_scalar(value: Any) -> bool:
    return isinstance(value, _SCALAR_TYPES)


def _resolve_path(path: str, context: dict[str, Any]) -> tuple[bool, Any]:
    """Walk a dotted path through *dicts only*. Returns (found, value).

    Lists are not indexed by path segments; attribute access is impossible by
    construction, so an injected payload cannot reach engine internals.
    """
    if not isinstance(path, str) or not path:
        raise ConditionEvaluationError(f"invalid variable path: {path!r}")
    current: Any = context
    for segment in path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            return False, None
    return True, current


def _coerce_datetime(value: Any, field_name: str) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        try:
            dt = parse_iso(value)
        except ValueError as exc:
            raise ConditionEvaluationError(f"{field_name} is not ISO-8601: {exc}") from exc
    else:
        raise ConditionEvaluationError(f"{field_name} must be an ISO-8601 string or datetime")
    if dt.tzinfo is None:
        raise ConditionEvaluationError(f"{field_name} must be timezone-aware")
    return dt.astimezone(timezone.utc)


class ConditionEvaluator:
    """Pure, side-effect-free evaluator over a typed expression tree."""

    def evaluate(self, expression: Any, context: dict[str, Any]) -> bool:
        result = self._evaluate(expression, context)
        if not isinstance(result, bool):
            raise ConditionEvaluationError(
                f"expression did not reduce to a bool (got {type(result).__name__})"
            )
        return result

    # ------------------------------------------------------------------

    def _evaluate(self, node: Any, context: dict[str, Any]) -> Any:
        if isinstance(node, bool):
            return node
        if not isinstance(node, dict):
            raise ConditionEvaluationError(
                f"expression nodes must be objects, got {type(node).__name__}"
            )

        if "window" in node:
            return self._eval_window(node, context)

        op = node.get("op")
        if op is None and "var" in node:
            found, value = _resolve_path(node["var"], context)
            if not found:
                raise ConditionEvaluationError(f"unknown variable {node['var']!r}")
            return value
        if op is None:
            raise ConditionEvaluationError("expression node missing 'op'")
        if op not in NODE_KINDS:
            raise ConditionEvaluationError(f"unsupported operator {op!r}")

        if op == "const":
            value = node.get("value")
            if not _is_scalar(value) and not (
                isinstance(value, list) and all(_is_scalar(v) for v in value)
            ):
                raise ConditionEvaluationError("const value must be scalar or list of scalars")
            return value

        if op in ("and", "or"):
            args = node.get("args")
            if not isinstance(args, list) or not args:
                raise ConditionEvaluationError(f"{op!r} requires a non-empty 'args' list")
            results = [self._as_bool(self._evaluate_inner(a, context), op) for a in args]
            return all(results) if op == "and" else any(results)

        if op == "not":
            if "arg" not in node:
                raise ConditionEvaluationError("'not' requires 'arg'")
            return not self._as_bool(self._evaluate_inner(node["arg"], context), "not")

        if op == "exists":
            found, _ = _resolve_path(node.get("path", ""), context)
            return found

        if op == "in":
            left = self._value_of(node.get("left"), context)
            right = self._value_of(node.get("right"), context)
            if not isinstance(right, list):
                raise ConditionEvaluationError("'in' requires a list on the right side")
            if not _is_scalar(left):
                raise ConditionEvaluationError("'in' requires a scalar on the left side")
            return left in right

        # comparisons
        left = self._value_of(node.get("left"), context)
        right = self._value_of(node.get("right"), context)
        return self._compare(op, left, right)

    def _evaluate_inner(self, node: Any, context: dict[str, Any]) -> Any:
        return self._evaluate(node, context)

    @staticmethod
    def _as_bool(value: Any, op: str) -> bool:
        if isinstance(value, bool):
            return value
        raise ConditionEvaluationError(
            f"operator {op!r} expects boolean operands, got {type(value).__name__}"
        )

    def _value_of(self, operand: Any, context: dict[str, Any]) -> Any:
        """Operand position accepts a literal scalar/list or an expression node."""
        if _is_scalar(operand):
            return operand
        if isinstance(operand, list) and all(_is_scalar(v) for v in operand):
            return operand
        if isinstance(operand, dict):
            return self._evaluate(operand, context)
        raise ConditionEvaluationError(f"unsupported operand {operand!r}")

    @staticmethod
    def _compare(op: str, left: Any, right: Any) -> bool:
        if op in ("==", "!="):
            equal = _strictly_equal(left, right)
            return equal if op == "==" else not equal
        if op not in _COMPARISONS:
            raise ConditionEvaluationError(f"unsupported comparison {op!r}")
        # Ordering is only allowed between compatible numeric/temporal types.
        if isinstance(left, bool) or isinstance(right, bool):
            raise ConditionEvaluationError("booleans are not orderable in conditions")
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            pass
        elif isinstance(left, str) and isinstance(right, str):
            # allow lexicographic compare only when both look like timestamps?
            # No implicit timestamp parsing: strings compare as strings.
            pass
        elif isinstance(left, datetime) or isinstance(right, datetime):
            left = _coerce_datetime(left, "left")
            right = _coerce_datetime(right, "right")
        else:
            raise ConditionEvaluationError(
                f"cannot order {type(left).__name__} vs {type(right).__name__}"
            )
        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        return left >= right

    # ------------------------------------------------------------------

    def _eval_window(self, node: dict[str, Any], context: dict[str, Any]) -> bool:
        """Restrict an inner expression to a time window.

        window spec::

            {"field": "occurred_at",          # defaults to now()
             "last_seconds": 300}             # or explicit since/until
        """
        spec = node.get("window") or {}
        if not isinstance(spec, dict):
            raise ConditionEvaluationError("window must be an object")
        if "arg" not in node:
            raise ConditionEvaluationError("window node requires 'arg'")

        now = utcnow()
        field = spec.get("field")
        if field:
            found, raw = _resolve_path(field, context)
            if not found:
                raise ConditionEvaluationError(f"window field {field!r} missing from context")
            anchor = _coerce_datetime(raw, field)
        else:
            anchor = now

        last = spec.get("last_seconds")
        if last is not None:
            if not isinstance(last, (int, float)) or isinstance(last, bool) or last < 0:
                raise ConditionEvaluationError("window.last_seconds must be a non-negative number")
            since = anchor - timedelta(seconds=float(last))
            until = anchor
        else:
            since = _coerce_datetime(spec.get("since"), "window.since") if spec.get("since") else None
            until = _coerce_datetime(spec.get("until"), "window.until") if spec.get("until") else None
            if since is None and until is None:
                raise ConditionEvaluationError("window requires last_seconds, since or until")

        if since is not None and anchor < since:
            return False
        if until is not None and anchor > until:
            return False
        return self._as_bool(self._evaluate(node["arg"], context), "window")


def _strictly_equal(left: Any, right: Any) -> bool:
    """Type-strict equality: 1 != True, 1 != "1"."""
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return float(left) == float(right)
    if type(left) is not type(right):
        return False
    return bool(left == right)


#: Module-level convenience used by the orchestrator.
_default_evaluator = ConditionEvaluator()


def evaluate_condition(expression: Any, context: dict[str, Any]) -> bool:
    return _default_evaluator.evaluate(expression, context)


__all__ = [
    "ConditionEvaluator",
    "evaluate_condition",
    "NODE_KINDS",
    "iso",
]
