"""Paper-only broker. This module has no exchange/network order submission."""
from decimal import Decimal
from .models import Fill, OrderRequest
from .risk import RiskManager


class PaperBroker:
    def __init__(self, risk: RiskManager, fee_rate: Decimal = Decimal("0.001"),
                 slippage_rate: Decimal = Decimal("0.0005")) -> None:
        if fee_rate < 0 or slippage_rate < 0 or slippage_rate >= 1:
            raise ValueError("invalid fee or slippage rate")
        self.risk = risk
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate
        self.fills: list[Fill] = []

    def submit(self, order: OrderRequest, reference_price: Decimal,
               current_position_notional: Decimal = Decimal("0"),
               daily_pnl: Decimal = Decimal("0")) -> Fill:
        if not self.risk.approve(order, reference_price, current_position_notional, daily_pnl):
            raise PermissionError("order rejected by risk controls")
        direction = Decimal("1") if order.side.value == "BUY" else Decimal("-1")
        fill_price = reference_price * (Decimal("1") + direction * self.slippage_rate)
        notional = order.quantity * fill_price
        fill = Fill(order.symbol, order.side, order.quantity, fill_price,
                    notional * self.fee_rate, simulated=True)
        self.fills.append(fill)
        return fill
