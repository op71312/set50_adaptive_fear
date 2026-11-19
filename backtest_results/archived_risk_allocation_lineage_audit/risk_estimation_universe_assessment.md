# Risk Estimation Universe Assessment

## Historical result

`RISK_UNIVERSE_UNKNOWN`.

The archived package contains no risk-input symbol list, return panel, covariance matrix, correlation matrix, expected-return vector, CVaR scenario matrix, HRP cluster tree, input hash, estimation cutoff, or per-date risk log. Its manifest describes “adjusted Master OHLC as execution prices” but does not identify an exact file/hash and does not state whether that file also supplied risk inputs.

No evidence establishes whether the historical risk estimator used Buy candidates only, all active SET50 members, held securities plus new buys, all available historical securities, or another universe. The universe cannot be reconstructed from current predictions or source code.

## Universe distinctions

| Universe | Meaning | Archived evidence / status |
|---|---|---|
| Buy Universe | Eligible securities with a Buy action for a strategy/date, before allocation. | Not separately recorded; unknown. |
| Held Portfolio Universe | Securities with nonzero shares in the portfolio at a date. | Reflected in valuation records for 35 pairs; not evidence of risk inputs. |
| Historical Risk Estimation Universe | Securities whose historical returns entered volatility, covariance, correlation, expected returns, or CVaR scenarios. | No risk panel or risk-universe log; `RISK_UNIVERSE_UNKNOWN`. |
| Active SET50 Membership Universe | Point-in-time constituents by membership effective date. | Local files exist, but archive has no membership snapshot/hash or run linkage. |
| Entire available historical price universe | Securities present in a candidate historical dataset. | Multiple candidate data artifacts exist; none is hash-linked as the archive's risk input. |

These sets are not interchangeable. In particular, no presence in predictions, transactions, valuation rows, or a current Master file proves inclusion or exclusion from the archived risk panel.

## Source and price-basis evidence

- Archive manifest SHA-256: `514b6b968444b4c7363e8f606bf73f690b41a997ab2a311e6953f29de59c898e`. It declares adjusted Master OHLC execution prices but lists no source path/hash, run ID, or risk-input metadata.
- `daily_predictions_audit.csv` has no model or feature source hash; `transactions.csv` and valuation records have no price-source ID or risk-input link.
- No standalone risk, covariance, correlation, return-matrix, weight, or solver-result artifact was found in the inspected `dataset/` or `backtest_results/` files. Existing Phase E policy documents and unresolved-risk reports are specifications/audits, not historical risk inputs.

## Current Notebook 05 code reference (not historical evidence)

Saved Notebook 05 cells 21, 25, 27, 29, and 31 (execution counts 141–145) construct daily returns from the currently loaded execution-price candidate's Close values and `pct_change(fill_method=None)`. `get_complete_history(symbols, ...)` selects the named columns and common rows, then requires at least 50 short-window or 200 CVaR observations. In the current `execute_one_day` code, the supplied symbols are `buy_names` formed from action and execution-date eligibility.

This path is a static/current-code observation only. Notebook 05's saved gate was closed; cell 53 (execution count 156) says all 63 experiments were skipped and no portfolio result CSVs were written. Notebook 06's saved harness reports only EW and IV as implemented and keeps the gate blocked. Neither saved notebook state is linked to the archived run.

## Approved Phase E comparison (specification only)

The approved specification requires the complete eligible Buy Universe for risk columns and common complete observations: 60 for IV/ERC/HRP/MinVar/MPT and 252 for CVaR, with centered sample covariance where applicable, no silent security removal, and no partial-window fallback. These rules do not reveal what the archive historically consumed. The current Notebook 05's 50/200 thresholds, Ledoit-Wolf code, and automatic EW fallbacks are current implementation facts, not approved historical behavior.

`HISTORICAL_RISK_UNIVERSE = UNKNOWN`  
`RISK_INPUT_LINEAGE = UNKNOWN`
