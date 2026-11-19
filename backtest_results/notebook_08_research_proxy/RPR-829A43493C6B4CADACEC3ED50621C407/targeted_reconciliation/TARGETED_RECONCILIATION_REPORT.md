# Targeted Reconciliation Report

## Objective
Read-only reconciliation of existing RESEARCH_PROXY run `RPR-829A43493C6B4CADACEC3ED50621C407` using only artifacts from that run. No backtest, prediction, model fitting, external data access, or source/notebook modification was performed. Only the six requested audit deliverables were created in `targeted_reconciliation/`.

## Run and source hashes
- Run ID: `RPR-829A43493C6B4CADACEC3ED50621C407`; mode: `RESEARCH_PROXY`.
- Notebook 07 SHA256 recorded by run: `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070`.
- Notebook 08 SHA256 recorded by run: `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081`.
- Frozen model SHA256 recorded by run: `8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7`.
- Frozen run-source hashes (as recorded in the run manifest; source files were not reopened) are in `reconciliation_manifest.json`.
- Input artifact SHA256 values and checksum verification results are in `reconciliation_manifest.json`.

## Status summary
| Check | Status | Evidence | Impact |
|---|---|---|---|
| Transaction cost vs turnover | **NOT_VERIFIABLE**; transaction ledger math **PASS** | Fees, slippage, and reported total costs reconcile; turnover equals filled gross notional / mean daily portfolio equity for 54/54 completed combinations. The nominal combined-rate notional basis is not recorded. | No cost-ledger arithmetic error found; exact interpretation of nominal combined rate is unresolved. |
| No-buy strategies | **NOT_VERIFIABLE**; executed output checks **PASS** | 24/24 executed S5/S6/S8/S9 combinations have no transaction rows, constant cash of 1,000,000, zero market value/open positions, and constant equity. Four CVaR combinations were not run; action logs are absent. | Zero fills are consistent with cash-only output behavior, not an automatic error. |
| Equity curve & metrics | **NOT_VERIFIABLE**; daily arithmetic **PASS** | 54/54 completed curves reconcile cash, market value, cash flows, total return, and max drawdown. Position-valuation rows lack combination identifiers; source-level look-ahead cannot be tested. | No arithmetic mismatch found, but independent holdings repricing and causal implementation are unverified. |
| Stale valuation | **NOT_VERIFIABLE**; observed-calendar check **PASS** | Daily stale-holding count and reported stale count are zero; 145,952 valuation rows have max observed-session age 0. | E-005/E-006 verified exchange-session compliance cannot be tested without an official calendar. |

## 1. Transaction cost vs turnover
Method: for all 63 combinations, recomputed filled raw/fill notionals, fee, slippage, total cost, and cash delta from `transactions.csv`; compared costs and turnover with the run's combination summary. `NO_FILL` and `BLOCKED` rows are not treated as executions.

- Run-approved component rates: fee `0.0016799` and slippage `0.001` per side; nominal sum `0.0026799`.
- Filled rows: 6,019 (5,048 BUY, 971 SELL); also 7,210 `NO_FILL` and 54 `BLOCKED` rows.
- Fee = fee rate × fill `Gross_Notional`; slippage = quantity × absolute(fill price − raw Open). Fill prices match raw Open ± `0.001` exactly.
- Cash delta matches `-(fill gross + fee)` on BUY and `(fill gross − fee)` on SELL. Slippage is reflected in the fill price; the separate slippage figure is used in cost reporting and is not an extra cash deduction.
- Recomputed fees + slippage match reported `Total_Transaction_Cost` for 54/54 completed combinations; maximum absolute per-combination difference is `7.27595761418e-12`.
- Reported turnover exactly matches sum of filled `Gross_Notional` divided by the combination's arithmetic mean daily `Portfolio_Equity` for 54/54 completed combinations; it does not match an initial-equity denominator. The run output does not document this formula as a declared policy.
- Because fee is charged on fill notional, effective combined cost against raw-open notional is `0.0026815799` for BUY and `0.0026782201` for SELL. Run outputs do not specify the basis for the nominal `0.0026799` combined rate, so exact policy-basis conformance is `NOT_VERIFIABLE`.

Requested combinations (notional pairs are BUY/SELL; fees and slippage likewise):
| Combination | Filled count B/S | Raw-open notional B/S | Fee B/S | Slippage B/S | Recomputed/reported cost | Reported/recomputed turnover | Ledger |
|---|---:|---:|---:|---:|---:|---:|---|
| S2_PanicBuy_FOMOSell/EW | 114/78 | 9,859,087.25/8,933,239.25 | 16,578.84/14,991.94 | 9,859.09/8,933.24 | 50,363.11/50,363.11 | 16.916984/16.916984 | PASS |
| S7_PanicHold_FOMOBuy/MPT | 285/4 | 997,325.59/0.00 | 1,677.08/0.00 | 997.33/0.00 | 2,674.41/2,674.41 | 0.852563/0.852563 | PASS |
| S4_PanicSell_FOMOBuy/EW | 470/90 | 3,629,808.03/2,646,629.90 | 6,103.81/4,441.63 | 3,629.81/2,646.63 | 16,821.88/16,821.88 | 5.612375/5.612375 | PASS |

Complete 63-row evidence is in `01_transaction_cost_reconciliation.csv`. CVaR rows are `INSUFFICIENT_HISTORY`; their cost/turnover as an executed allocation is `NOT_VERIFIABLE`.

## 2. No-buy strategies
Checked transaction rows and combination-keyed daily cash, market value, equity, and open-position count for S5 (Sell/Sell/Hold), S6 (Sell/Hold/Hold), S8 (Hold/Sell/Hold), and S9 (Hold/Hold/Hold).

- For the 24 executed no-buy combinations, transaction, BUY, and SELL row counts are zero; cash remains `1,000,000`, market value and open positions remain zero, and equity remains `1,000,000` on every exported session.
- The four no-buy CVaR combinations were not run due insufficient history.
- The run has no strategy-action/signal log by strategy, therefore action generation cannot be confirmed from these exports; this is `NOT_VERIFIABLE`. Output-level no-trade accounting passes for executed combinations.
- A zero transaction count is consistent with cash-only initialization and does not by itself indicate an error.

All 28 combinations are detailed in `02_no_buy_strategy_validation.csv`.

## 3. Equity curve and performance metrics
For each completed combination, recomputed `Portfolio_Equity = Cash + Market_Value`, daily cash using previous daily cash plus that day's transaction `Cash_Delta`, total return from initial and final equity, and max drawdown from the exported equity curve.

- Initial equity is `1,000,000`; the first recorded equity is exactly this amount in all 54 completed combinations.
- Maximum absolute daily equity-identity residual: `2.32830643654e-10`; maximum cash-bridge residual: `1.38243194669e-10`.
- Maximum absolute total-return difference: `0`; maximum absolute max-drawdown difference: `0`. All 54/54 executed curves pass these numerical checks.
- All 13,283 transaction rows have predictor date before execution date: `True`; execution date is the next observed-vendor date for all rows: `True`. `predictions.csv` contains no realized future-return field. These output facts cannot prove the implementation did not use future information internally; that remains `NOT_VERIFIABLE`.
- `position_valuation.csv` does not contain `Strategy_ID` or `Allocation_Method`, so holding marks/quantities cannot be joined to each strategy × allocation combination. Daily `Cash + Market_Value = Portfolio_Equity` passes, but per-combination repricing from position rows is `NOT_VERIFIABLE`.
- All exported performance is unannualized `PRICE_RETURN`; this report does not recalculate or validate a trading strategy.

All 63 combinations, including S7/MPT, S4/EW, and S1/MPT, are in `03_equity_curve_reconciliation.csv`.

## 4. Stale valuation policy
- Run calendar is `OBSERVED_VENDOR_CALENDAR`; official SET calendar verified: `False`.
- Maximum daily `Stale_Holding_Count` across 8,100 daily rows is 0; all zero: `True`.
- Position-valuation rows: 145,952; observed-session age distribution `{"0": 145952}`; maximum age `0`; valuation statuses `{"PORTFOLIO_VALUE_VALID": 145952}`.
- Reported stale valuation counts are zero for the executed combinations and agree with daily observed-calendar stale counts. Position-valuation rows cannot be attributed per combination because combination IDs are absent.
- E-005/E-006 are defined in verified exchange sessions. Since the run uses `OBSERVED_VENDOR_CALENDAR`, compliance measured in verified SET sessions is `NOT_VERIFIABLE`; vendor sessions are not described as exchange sessions.

All 63 rows are in `04_stale_valuation_reconciliation.csv`.

## Conclusions
1. **Are the 54 completed combinations mathematically/accounting consistent?** Exported transaction-to-cost, cash-flow, daily equity identity, total return, and drawdown arithmetic are consistent within floating-point tolerance. This is output-level reconciliation only.
2. **Is an error proven to affect Total Return or Max Drawdown?** No arithmetic mismatch was found. However, missing strategy/method identifiers in position valuation prevent independent per-combination repricing, and output-only evidence cannot rule out implementation-level look-ahead. It is not justified to claim that all possible errors are absent.
3. **Suitability as a Research Proxy baseline:** provisional and exploratory only; not a verified or execution-ready baseline. Before promotion, preserve strategy/method IDs in valuation output, explicitly record turnover and fee notional bases, and export strategy-action provenance for no-buy assertions.

## Gate status (unchanged)
- `RESEARCH_BACKTEST_GATE = CONDITIONAL_OPEN`
- `EXECUTION_VALIDATION_GATE = BLOCKED`
- `Canonical_Historical_Gate = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`

No gate was changed. This is not a Verified Tradable Backtest.
