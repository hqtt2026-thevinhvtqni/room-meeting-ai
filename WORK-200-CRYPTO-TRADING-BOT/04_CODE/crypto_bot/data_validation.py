"""Chronological OHLCV data validation."""
from .models import Candle


def validate_candles(candles: list[Candle]) -> list[Candle]:
    if not candles:
        raise ValueError("candles must not be empty")
    symbol = candles[0].symbol
    previous = None
    for candle in candles:
        if candle.symbol != symbol:
            raise ValueError("one symbol per series is required")
        if previous is not None and candle.timestamp <= previous:
            raise ValueError("timestamps must be strictly increasing; duplicates/out-of-order rejected")
        previous = candle.timestamp
    return candles
