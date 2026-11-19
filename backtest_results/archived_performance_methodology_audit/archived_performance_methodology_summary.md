# Archived Performance Methodology Audit

## Executive summary

The archived performance summary is **NOT_VALIDATED as a research result**. Its accompanying manifest explicitly records that Total Return and CAGR omitted the initial-equity baseline. The archived package has no run ID, source-code hash, metric formula log, or input hash tying a historical metric implementation to `performance_summary.csv`. Therefore the precise return denominator and the formulas used for CAGR, Sharpe, Sortino, Maximum Drawdown, and Calmar cannot be established.

The stored accounting tables are internally consistent at the row level: across all 13,167 daily rows, `Portfolio_Value = Cash + Market_Value`; every daily Market_Value equals the sum of recorded position values; each position value equals Shares × Valuation_Price; and Holdings_Count matches the valuation-row count. This confirms consistency of retained output fields, not correctness of the source prices or metric methodology.

Material limitations:

- The archive manifest says the run used adjusted Master OHLC as execution prices but provides no exact source path or hash.
- Initial capital is not a recorded baseline row. Twenty-eight no-position pairs show $1,000,000 cash and equity throughout; this does not establish the denominator for the other 35 pairs.
- BANPU is carried at a stale Close up to 93 **calendar days** in six pairs. The stale marks are included in stored position and portfolio values.
- All 3,125 transactions have `Cost / Gross = 0.0026799`, numerically equal to the later fee plus slippage assumptions. The transaction schema does not separate fee and slippage or identify the raw price/fill-price basis.
- All pairs cover 209 dates, but 28 are all-cash/no-trade cases; performance summaries leave several fields blank for those cases. Uniform dates do not establish comparable measurement.

## Metrics and trust assessment

| Metric / evidence | Assessment |
|---|---|
| Total Return | Archive metadata says the initial-equity baseline was omitted. Exact denominator and archived formula remain unknown; do not rely on the stored value. |
| CAGR | Same baseline issue; historical period and annualization formula are not linked to the archived output. |
| Sharpe / Sortino / Max Drawdown / Calmar | Values exist for most pairs, but no archived formula, run linkage, or metric-input series is present. Zero-holdings pairs have blank Sharpe, Sortino, and Calmar fields. Not validated. |
| Daily equity construction | Recorded cash-plus-market-value identity and position valuation reconcile across the archived output. This is structural consistency only. |
| Stale marks | 378 stale valuation rows across six pairs are all BANPU; maximum recorded age is 93 calendar days. Their inclusion in stored portfolio values is directly observable. |
| Transaction cost fields | Cost and gross sums reconcile to nonblank performance-summary totals. Component rates and cash application are not proven by a run-linked source. |

No replacement metric, equity curve, return series, or performance result was calculated. The metric formula table and pair-level table document evidence and coverage only.

## Final decision table

| Question | Finding | Evidence classification |
|---|---|---|
| Initial equity verified? | Partially observed: $1,000,000 all-cash daily values for 28 pairs; no explicit starting-equity row for the portfolio series. | `METADATA_REFERENCE_ONLY` |
| First-day return treatment verified? | No; first archived daily record is the execution-date Close mark. No return series or run-linked formula is present. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Daily equity construction verified? | Stored cash + market value equals equity; positions reconcile to valuation rows. Historical price source remains unverified. | `HASH_VERIFIED` |
| Return formula verified? | No; archive manifest states the initial-equity baseline was omitted but the denominator is unknown. | `METADATA_REFERENCE_ONLY` |
| CAGR methodology verified? | No; baseline issue is recorded, annualization formula is not linked. | `METADATA_REFERENCE_ONLY` |
| Sharpe methodology verified? | No; frequency, risk-free rate, and estimator are unknown for the archived result. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Sortino methodology verified? | No; target and downside formula are unknown for the archived result. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Maximum Drawdown methodology verified? | No; archived curve construction and peak initialization are not linked. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Calmar methodology verified? | No; compatibility of archived CAGR and drawdown inputs is unknown. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Cash treatment verified? | Cash is included in recorded Portfolio_Value identity; historical transaction-to-cash application is not linked. | `HASH_VERIFIED` / `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Stale valuation policy verified? | Calendar-day stale ages and inclusion are visible; historical rule/configuration is not linked. | `METADATA_REFERENCE_ONLY` |
| BANPU valuation impact understood? | BANPU stale marks enter stored equity; metric impact direction/magnitude was not calculated. | `DERIVATION_CONFIRMED` for exposure only |
| Buy transaction costs verified? | Cost is separate from Gross; per-order Cost/Gross matches 0.0026799. Cash application is unknown. | `DERIVATION_CONFIRMED` for recorded ratio |
| Sell transaction costs verified? | Same recorded ratio; cash proceeds net of cost are not separately recorded. | `DERIVATION_CONFIRMED` for recorded ratio |
| Slippage verified? | No separate slippage field or archived settings; ratio matches the later combined assumptions but does not identify component treatment. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| All 63 pairs comparable? | Same stored date coverage, but zero-holdings cases, stale exposure, missing summary fields, and methodology lineage prevent validation. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Historical metric code linked to archive? | No run ID or code/input hash link. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Archived performance suitable as validated research result? | No. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |

`ARCHIVED_PERFORMANCE_AUDIT = COMPLETED / BLOCKED`  
`INITIAL_EQUITY_METHODOLOGY = PARTIALLY_VERIFIED`  
`RETURN_METHODOLOGY = PARTIALLY_VERIFIED`  
`PERFORMANCE_METRIC_METHODOLOGY = UNKNOWN`  
`STALE_VALUATION_METHODOLOGY = PARTIALLY_VERIFIED`  
`TRANSACTION_COST_METHODOLOGY = PARTIALLY_VERIFIED`  
`CROSS_STRATEGY_COMPARABILITY = UNKNOWN`  
`ARCHIVED_PERFORMANCE_TRUST = NOT_VALIDATED`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`

No subsequent workstream was started.
