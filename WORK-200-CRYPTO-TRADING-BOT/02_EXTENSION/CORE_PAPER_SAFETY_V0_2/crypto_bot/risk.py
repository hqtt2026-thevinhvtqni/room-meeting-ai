"""Paper-only exposure and loss guard (v0.2); never grants live order authority.

The PaperBroker owns the account snapshot; calling approve with fabricated account
numbers is not an authentication or live trading interface.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Callable
from .models import OrderRequest, Side


def _finite(value: Decimal) -> bool:
    return isinstance(value, Decimal) and value.is_finite()


@dataclass(frozen=True)
class RiskLimits:
    max_order_notional: Decimal
    max_position_notional: Decimal
    max_daily_loss: Decimal

    def __post_init__(self) -> None:
        limits = (self.max_order_notional, self.max_position_notional, self.max_daily_loss)
        if any(not _finite(x) or x <= 0 for x in limits):
            raise ValueError("risk limits must be finite positive decimals")


class RiskManager:
    """Rejects increased exposure when halted; permits strictly reduce-only exits.

    IMPORTANT: daily_pnl has NO date roll-over yet. The owning PaperBroker feeds
    realized lifetime PnL; a calendar-day loss engine is a future requirement.
    """
    def __init__(self, limits: RiskLimits) -> None:
        self.limits = limits
        self._halted = False
        self._cancel_handlers: list[Callable[[], None]] = []

    @property
    def halted(self) -> bool:
        return self._halted

    def register_cancel_handler(self, fn: Callable[[], None]) -> None:
        self._cancel_handlers.append(fn)
        if self._halted:
            fn()

    def activate_kill_switch(self) -> None:
        self._halted = True
        for fn in tuple(self._cancel_handlers):
            fn()

    def reset_kill_switch(self) -> None:
        # Not safe for remote control: human review and authenticated release required.
        self._halted = False

    def enforce_loss_limit(self, pnl: Decimal) -> None:
        if not _finite(pnl) or pnl <= -self.limits.max_daily_loss:
            self.activate_kill_switch()

    def approve(self, order: OrderRequest, reference_price: Decimal,
                current_position_notional: Decimal = Decimal("0"),
                daily_pnl: Decimal = Decimal("0"), *, reduce_only: bool = False) -> bool:
        # Check loss FIRST so an oversized order cannot mask a breached loss limit.
        self.enforce_loss_limit(daily_pnl)
        if not (_finite(reference_price) and reference_price > 0 and
                _finite(current_position_notional)):
            return False
        notional = order.quantity * reference_price
        if not _finite(notional):
            return False
        delta = notional if order.side is Side.BUY else -notional
        projected = current_position_notional + delta
        # Reductions must not cross zero or create a new position in the opposite direction.
        is_reduction = (current_position_notional != 0 and
                        abs(projected) < abs(current_position_notional) and
                        (projected == 0 or (projected > 0) == (current_position_notional > 0)))
        if reduce_only:
            return is_reduction
        if self._halted:
            return False
        if notional > self.limits.max_order_notional:
            return False
        if abs(projected) > self.limits.max_position_notional:
            return False
        return True