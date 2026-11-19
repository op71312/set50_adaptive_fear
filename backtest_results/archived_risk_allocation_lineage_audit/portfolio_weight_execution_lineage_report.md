# Portfolio Weight and Execution Lineage Report

## Trace result

The archived outputs can be linked structurally by strategy/allocation identifiers and dates, but the historical allocation chain cannot be traced to weights or risk inputs:

`Archived predictions → historical strategy action → Sell / forced exit → Buy Universe → risk inputs → raw weights → final weights → Open execution → Close valuation`

The first transitions are not fully represented in the archive, the risk and weight artifacts are absent, and the final output tables have no run/input identifiers. No missing allocation values were reconstructed.

## Evidence at each stage

| Stage | What is retained | What is not established |
|---|---|---|
| Prediction | 654,381 prediction rows; 63 pairs; 209 decision dates; class and probability fields. | Model/run identity is not part of this audit's scope; prediction rows do not contain per-symbol Action or allocator Buy input. |
| Strategy action | Strategy and allocation IDs accompany prediction rows. | Archive lacks an action column or run-linked strategy mapping/output. Do not recompute actions from current rules. |
| Sell / forced exit / Hold | Transactions record `Side`, `Shares`, `Price`, `Gross`, `Cost`; valuation records shares. | No sell reason, forced-exit flag, blocked order file, state-transition log, or proof of sell/forced-exit/Buy ordering for the historical engine. |
| Buy Universe | None as a dated per-method artifact. | Exact eligible symbols and whether selection used predictor date or execution date are unknown. |
| Risk inputs | None. | Risk dates/cutoff, symbol order, return price basis, estimator, matrix hashes, and missing-data behavior are unknown. |
| Raw / final weights | None. The transaction schema has no `Budget`, `Raw_Weight`, `Final_Weight`, or allocation status; daily/valuation schemas contain no per-method allocation weights. | Raw weights, cap adjustments, redistribution, and solver result are unknown. |
| Execution | Transactions contain Date, Symbol, Side, Shares, Price, Gross, Cost, Strategy, Allocation. | No input-price ID, run ID, per-side slippage/fee components, allocation budget, or order/fill linkage. Archive metadata only says adjusted Master OHLC execution prices. |
| Daily portfolio | 13,167 rows; 209 per pair; includes Cash, Market_Value, Portfolio_Value, Holdings_Count, and stale indicators. | Daily Cash is a post-execution output field; it does not identify allocation-budget residual cash or method weights. |
| Valuation | 67,633 rows across 35 pairs; contains shares, Valuation_Price, Price_Date, stale age, market value, date, strategy, allocation. | No verified price source ID, risk-input relation, or hash-pinned valuation process. |

## Structural checks

- Performance, daily portfolio, and predictions each contain the full 63-pair Cartesian set (nine strategy IDs by seven allocation labels).
- Predictions' 209 dates equal daily Decision_Date coverage; daily execution dates cover 2026-01-06–2026-11-13 while decision dates cover 2026-01-05–2026-11-12.
- Transactions and valuation records cover the same 35 pairs; 28 other pairs have zero holdings throughout.
- No GLOBAL symbol appears in prediction, transaction, or valuation rows.
- These checks establish row/key alignment only. They do not prove the allocator generated the records or that a historical Open/Close source matches them.

## Current code comparison only

The current Notebook 05 code describes Sell/forced exit before Buy, builds `buy_names` from action, execution-date membership, and available Open, and passes those names to the allocator. It applies the 25% cap and stores allocation audit rows only inside `run_backtest`. The saved current run state has `BACKTEST_GATE_OPEN=False`; cell 53 reports all 63 experiments skipped and no portfolio-result CSVs written.

Notebook 06's saved fail-closed state is also blocked and reports only EW and IV as implemented. Neither notebook's saved state is proven to be the archived execution. The archived manifest separately records a single-asset cap bypass in some methods, so the archive must not be presumed to satisfy the later cap policy.

## Lineage status

Archived output-to-output structure is `METADATA_REFERENCE_ONLY` / structurally verified. Historical risk-to-weight, weight-to-order, and input-price-to-fill lineage remain `UNKNOWN_INSUFFICIENT_EVIDENCE`.

`ALLOCATION_WEIGHT_LINEAGE = UNKNOWN`  
`PORTFOLIO_EXECUTION_LINEAGE = PARTIALLY_VERIFIED`
