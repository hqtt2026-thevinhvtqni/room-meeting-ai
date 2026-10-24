"""Independent risk checks; fail closed when limits are exceeded."""
from dataclasses import dataclass
from decimal import Decimal
from .models import OrderRequest


@dataclass(frozen=True)
class RiskLimits:
    max_order_notional: Decimal
    max_position_notional: Decimal
    max_daily_loss: Decimal

    def __post_init__(self) -> None:
        if min(self.max_order_notional, self.max_position_notional, self.max_daily_loss) <= 0:
            raise ValueError("all risk limits must be positive")


class RiskManager:
    def __init__(self, limits: RiskLimits) -> None:
        self.limits = limits
        self._halted = False

    @property
    def halted(self) -> bool:
        return self._halted

    def activate_kill_switch(self) -> None:
        self._halted = True

    def reset_kill_switch(self) -> None:
        # Reset is explicit and should be performed only after a human review.
        self._halted = False

    def approve(self, order: OrderRequest, reference_price: Decimal,
                current_position_notional: Decimal = Decimal("0"),
                daily_pnl: Decimal = Decimal("0")) -> bool:
        if self._halted or reference_price <= 0:
            return False
        notional = order.quantity * reference_price
        if notional > self.limits.max_order_notional:
            return False
        if abs(current_position_notional) + notional > self.limits.max_position_notional:
            return False
        if daily_pnl <= -self.limits.max_daily_loss:
            self.activate_kill_switch()
            return False
        return True
