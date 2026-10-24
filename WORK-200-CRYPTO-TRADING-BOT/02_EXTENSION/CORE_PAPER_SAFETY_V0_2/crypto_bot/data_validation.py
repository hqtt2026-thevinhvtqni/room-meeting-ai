"""Chronological OHLCV series validation with optional fixed candle interval."""
from datetime import timedelta
from .models import Candle


def validate_candles(candles: list[Candle], timeframe: timedelta | None = None) -> list[Candle]:
    if not candles:
        raise ValueError("candles must not be empty")
    if timeframe is not None and timeframe <= timedelta(0):
        raise ValueError("timeframe must be positive")
    symbol = candles[0].symbol
    previous = None
    for candle in candles:
        if candle.symbol != symbol:
            raise ValueError("one symbol per series is required")
        if previous is not None:
            if candle.timestamp <= previous:
                raise ValueError("timestamps must be strictly increasing; duplicates/out-of-order rejected")
            if timeframe is not None and candle.timestamp - previous != timeframe:
                raise ValueError("missing or irregular candle interval")
        previous = candle.timestamp
    return candles