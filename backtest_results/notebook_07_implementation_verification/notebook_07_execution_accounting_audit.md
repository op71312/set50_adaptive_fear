# Notebook 07 execution accounting audit

## Scope
This review inspected the actual code in the notebook implementation and checked whether the accounting and execution behavior is coherent and fail-closed for synthetic inputs only. No historical backtest, live market data source, or historical price ingestion was used.

## Verified accounting and execution behavior

### 1. Cash accounting
The order-execution logic in `execute_orders` calculates cash delta from trade notional and fees, preserves cash when no fill occurs, and stores `Cash_After` per transaction. The synthetic test `26_buy_lot_fee_and_cash_accounting` asserts:
- `Quantity % board_lot_multiple == 0`
- `Cash_Delta + Gross_Notional + Fee == 0`
- `Cash >= 0`
- `Slippage_Cost > 0` when the benchmark Open is used and fill price exceeds raw Open

This is consistent with a valid accounting identity for order execution.

### 2. Share accounting and board-lot enforcement
`_lot_rule_for`, `_sell_quantity`, and `_buy_quantity` are actual enforcement functions. They block unsupported order sizes and enforce minimum order quantities. The synthetic tests `27_missing_open_preserves_cash`, `28_minimum_order_size_enforced`, and `31_unverified_board_lot_blocks_sizing` demonstrate the fail-closed behavior: no Open quote, no valid lot rule, or minimum order violation yields blocked or `NO_FILL` outcomes without inventing fills.

### 3. Buy/sell ordering
`execute_orders` sorts sell transactions before buy transactions and applies forced exits before new buys. The synthetic test `30_sell_orders_precede_buy_orders` asserts the exact order list `["SELL", "BUY"]` in the output transaction frame.

### 4. Corporate actions
`apply_corporate_actions` validates `Reconciliation_Status` and applies a verified split only once. The code stores `Applied_Event_IDs` and returns an idempotent result on repeated processing. Tests `32_unreconciled_corporate_action_blocked` and `33_verified_corporate_action_applied_once` confirm this guardrail.

### 5. Daily valuation and stale-price handling
`mark_portfolio` updates the last valid marks and tracks `Portfolio_Equity_Status`. The synthetic tests `34_stale_marks_capped_at_three_sessions`, `35_missing_close_without_prior_mark`, and `36_calendar_required_for_daily_valuation` confirm that stale marks degrade to `PORTFOLIO_VALUE_STALE` and then `PORTFOLIO_VALUE_UNAVAILABLE` when price evidence is missing or calendars are unverified.

## Algebraic conclusion
The notebook logic enforces arithmetic consistency and fail-closed conditions for synthetic inputs. It does not claim historical valuation accuracy, and it does not run a historical backtest. The code therefore validates the accounting model under synthetic conditions, not real historical portfolio reconciliation.

## Final verdict
`IMPLEMENTED_WITH_LIMITATIONS`
