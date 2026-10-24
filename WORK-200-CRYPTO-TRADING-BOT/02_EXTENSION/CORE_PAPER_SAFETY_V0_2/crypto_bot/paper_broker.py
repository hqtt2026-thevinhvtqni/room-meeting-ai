"""Deterministic SPOT-only paper broker. No network, credentials, or live orders.

Owns simulated cash, holdings and realized PnL. SELLs can only reduce owned
holdings; there is no spot short. This is not a complete account ledger.
"""
from decimal import Decimal
from .models import Fill, OrderRequest, Side
from .risk import RiskManager


class PaperBroker:
    def __init__(self, risk: RiskManager, fee_rate: Decimal = Decimal("0.001"),
                 slippage_rate: Decimal = Decimal("0.0005"),
                 starting_cash: Decimal = Decimal("10000")) -> None:
        vals = (fee_rate, slippage_rate, starting_cash)
        if any(not isinstance(v, Decimal) or not v.is_finite() for v in vals):
            raise ValueError("configuration requires finite Decimal values")
        if fee_rate < 0 or slippage_rate < 0 or slippage_rate >= 1 or starting_cash < 0:
            raise ValueError("invalid fee, slippage, or starting cash")
        self.risk = risk
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate
        self.cash = starting_cash
        self.positions: dict[str, Decimal] = {}
        self.cost_basis: dict[str, Decimal] = {}  # includes entry commissions
        self.realized_pnl = Decimal("0")           # lifetime, not daily roll-over
        self.fills: list[Fill] = []
        self.pending: dict[str, tuple[OrderRequest, Decimal]] = {}
        self.risk.register_cancel_handler(self.cancel_all_pending)

    def cancel_all_pending(self) -> None:
        self.pending.clear()

    def _price(self, order: OrderRequest, reference_price: Decimal) -> Decimal:
        if not isinstance(reference_price, Decimal) or not reference_price.is_finite() or reference_price <= 0:
            raise ValueError("reference price must be a finite positive Decimal")
        direction = Decimal("1") if order.side is Side.BUY else Decimal("-1")
        return reference_price * (Decimal("1") + direction * self.slippage_rate)

    def submit(self, order: OrderRequest, reference_price: Decimal) -> Fill:
        px = self._price(order, reference_price)
        qty = self.positions.get(order.symbol, Decimal("0"))
        # Reject any attempt to short physical spot, including opening with SELL.
        if order.side is Side.SELL and order.quantity > qty:
            raise PermissionError("spot SELL may only reduce existing holdings")
        value = order.quantity * px
        fee = value * self.fee_rate
        current_notional = qty * px
        close = order.side is Side.SELL
        if not self.risk.approve(order, px, current_notional,
                                 self.realized_pnl, reduce_only=close):
            raise PermissionError("order rejected by risk controls")
        if order.side is Side.BUY:
            spend = value + fee
            if spend > self.cash:
                raise PermissionError("insufficient paper cash")
            self.cash -= spend
            self.positions[order.symbol] = qty + order.quantity
            self.cost_basis[order.symbol] = self.cost_basis.get(order.symbol, Decimal("0")) + spend
        else:
            basis = self.cost_basis[order.symbol]
            relieved = basis * order.quantity / qty
            self.cash += value - fee
            self.positions[order.symbol] = qty - order.quantity
            self.cost_basis[order.symbol] = basis - relieved
            self.realized_pnl += value - fee - relieved
            if not self.positions[order.symbol]:
                del self.positions[order.symbol]
                del self.cost_basis[order.symbol]
            self.risk.enforce_loss_limit(self.realized_pnl)
        fill = Fill(order.symbol, order.side, order.quantity, px, fee, simulated=True)
        self.fills.append(fill)
        return fill

    def queue_paper(self, event_id: str, order: OrderRequest, reference_price: Decimal) -> None:
        if not event_id or event_id in self.pending:
            raise ValueError("pending event id must be unique and nonempty")
        px = self._price(order, reference_price)
        qty = self.positions.get(order.symbol, Decimal("0"))
        if order.side is Side.SELL and order.quantity > qty:
            raise PermissionError("spot SELL requires holdings")
        if not self.risk.approve(order, px, qty * px, self.realized_pnl,
                                 reduce_only=order.side is Side.SELL):
            raise PermissionError("pending proposal blocked by risk")
        self.pending[event_id] = (order, reference_price)

    def execute_paper(self, event_id: str) -> Fill:
        order, price = self.pending.pop(event_id)
        return self.submit(order, price)