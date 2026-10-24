"""Stateless, closed-history moving-average cross for deterministic research."""
from decimal import Decimal
from .models import Candle, Side


class MovingAverageCross:
    def __init__(self, fast_window: int = 5, slow_window: int = 20) -> None:
        if fast_window < 1 or slow_window <= fast_window:
            raise ValueError("require 1 <= fast_window < slow_window")
        self.fast_window = fast_window
        self.slow_window = slow_window

    def _relation(self, closes: list[Decimal]) -> int:
        fast = sum(closes[-self.fast_window:], Decimal("0")) / self.fast_window
        slow = sum(closes[-self.slow_window:], Decimal("0")) / self.slow_window
        return 1 if fast > slow else -1 if fast < slow else 0

    def on_candle(self, history: list[Candle]) -> Side | None:
        if len(history) < self.slow_window + 1:
            return None
        closes = [c.close for c in history]
        previous, current = self._relation(closes[:-1]), self._relation(closes)
        if previous <= 0 and current > 0:
            return Side.BUY
        if previous >= 0 and current < 0:
            return Side.SELL
        return None