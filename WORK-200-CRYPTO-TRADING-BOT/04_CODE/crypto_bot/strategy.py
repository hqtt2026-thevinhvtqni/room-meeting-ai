"""A simple moving-average crossover baseline for research, not investment advice."""
from decimal import Decimal
from .models import Candle, Side


class MovingAverageCross:
    def __init__(self, fast_window: int = 5, slow_window: int = 20) -> None:
        if fast_window < 1 or slow_window <= fast_window:
            raise ValueError("require 1 <= fast_window < slow_window")
        self.fast_window = fast_window
        self.slow_window = slow_window
        self._previous_relation: int | None = None

    def on_candle(self, history: list[Candle]) -> Side | None:
        if len(history) < self.slow_window:
            return None
        closes = [c.close for c in history]
        fast = sum(closes[-self.fast_window:], Decimal("0")) / self.fast_window
        slow = sum(closes[-self.slow_window:], Decimal("0")) / self.slow_window
        relation = 1 if fast > slow else (-1 if fast < slow else 0)
        signal = None
        if self._previous_relation is not None:
            if self._previous_relation <= 0 and relation > 0:
                signal = Side.BUY
            elif self._previous_relation >= 0 and relation < 0:
                signal = Side.SELL
        self._previous_relation = relation
        return signal
