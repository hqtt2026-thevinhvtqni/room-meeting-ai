"""Validated domain models for the initial paper-trading engine."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class Candle:
    symbol: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")
        prices = (self.open, self.high, self.low, self.close)
        if any(not isinstance(x, Decimal) or not x.is_finite() or x <= 0 for x in prices):
            raise ValueError("OHLC prices must be finite and positive")
        if not isinstance(self.volume, Decimal) or not self.volume.is_finite() or self.volume < 0:
            raise ValueError("volume must be finite and non-negative")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must be >= open, close, and low")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be <= open, close, and high")


@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: Side
    quantity: Decimal

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")
        if not isinstance(self.side, Side):
            raise ValueError("side must be Side")
        if not isinstance(self.quantity, Decimal) or not self.quantity.is_finite() or self.quantity <= 0:
            raise ValueError("quantity must be finite and positive")


@dataclass(frozen=True)
class Fill:
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    fee: Decimal
    simulated: bool = True