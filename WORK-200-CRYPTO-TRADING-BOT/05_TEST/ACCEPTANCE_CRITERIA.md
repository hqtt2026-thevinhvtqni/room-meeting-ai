# Acceptance Criteria — Work 200 (Initial Gate)

A milestone may be marked PASS only when evidence exists for all applicable items.

- [ ] Project manifest and architecture plan exist.
- [ ] Market data validation rejects malformed, duplicate, out-of-order, and missing-required-field inputs.
- [ ] Strategy output is deterministic for fixed input and configuration.
- [ ] Backtest uses only information available at each simulated decision time.
- [ ] Fees and slippage are applied and covered by tests.
- [ ] Risk limits prevent order proposals that exceed configured exposure/loss bounds.
- [ ] Kill switch blocks further paper orders.
- [ ] Paper broker cannot submit live orders.
- [ ] Unit and integration tests run in the actual Sandbox environment; results and commands are recorded.
- [ ] Reports include drawdown, costs, exposure, and benchmark comparison.
- [ ] No secrets are committed to source or logs.
- [ ] Limitations and unresolved risks are documented.

No PASS is implied by the existence of plans or files alone.
