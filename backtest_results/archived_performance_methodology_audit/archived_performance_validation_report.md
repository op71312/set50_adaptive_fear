# Archived Performance Methodology Audit — Validation Report

## Result

The deliverables document the retained archive and its limits. Structural accounting checks pass, but the archived performance methodology remains **BLOCKED / NOT_VALIDATED** because initial-equity treatment, metric formulas, and historical code/run identity cannot be linked to the saved metric CSV. No replacement performance values were calculated.

## Required checks

| # | Check | Result | Evidence / limitation |
|---:|---|---|---|
| 1 | Verify the six archived artifacts and hashes. | PASS | Hash table below; archive artifacts read only. |
| 2 | Validate the 63 strategy/allocation rows. | PASS | Performance, daily, and prediction files cover the full 9 × 7 label set. |
| 3 | Validate 209 daily rows per pair. | PASS | Every pair has exactly 209 daily rows. |
| 4 | Validate date coverage. | PASS | Decision dates: 2026-01-05–2026-11-12; execution dates: 2026-01-06–2026-11-13. |
| 5 | Inspect stored equity, cash, holdings, and valuation consistency. | PASS | Zero mismatches for Portfolio_Value = Cash + Market_Value; daily Market_Value vs valuation sum; Shares × Valuation_Price; Holdings_Count vs valuation rows; stale-count and stale-age propagation. |
| 6 | Investigate initial-equity baseline. | PASS_WITH_LIMITATIONS | Archive manifest states Total Return/CAGR omitted the baseline; exact denominator and historical implementation are unknown. |
| 7 | Inspect all six performance metric definitions. | PASS_WITH_LIMITATIONS | Archived formulas are not linked to the output; current Notebook 05/06 formulas are static references only. |
| 8 | Inspect stale valuation including BANPU. | PASS_WITH_LIMITATIONS | 378 stale BANPU rows; maximum 93 calendar days. Historical acceptance rule and exact metric effect remain unknown. |
| 9 | Inspect transaction costs and historical code. | PASS_WITH_LIMITATIONS | Cost/Gross is 0.0026799 for all 3,125 records; separate fee/slippage treatment and archived cash application are unverified. |
| 10 | Evaluate all 63 combinations independently. | PASS_WITH_LIMITATIONS | Pair-level CSV has one row per combination. Same date coverage is verified; comparable metric policy is not. |
| 11 | Distinguish current code from historical code. | PASS | Current notebook hashes/cells and saved blocked state are separated from the archive; no run linkage was inferred. |
| 12 | Verify no protected input was modified. | PASS | Pre-audit inventory covered 20,086 existing repository files. After creation: zero hash mismatches, missing files, or unexpected paths outside the new audit directory. |
| 13 | Verify no external download or yfinance call occurred. | PASS | No call was made; existing run-status artifacts also record no redownload. |
| 14 | Verify no model, prediction, optimizer, or backtest execution occurred. | PASS | Audit scripts only read files and checked record-level identities; no notebook code was executed. |
| 15 | Verify all ten deliverables and their hashes. | PASS | Manifest includes the nine other outputs; each recorded size and SHA-256 was checked. |

**Counts:** PASS = 10; PASS_WITH_LIMITATIONS = 5; FAIL = 0.  
**Audit validation:** PASS_WITH_LIMITATIONS.  
**Archived performance methodology:** BLOCKED / NOT_VALIDATED.

## Archived artifact SHA-256

| Artifact | SHA-256 |
|---|---|
| `backtest_results/superseded_20261115_pre_integrity_fixes/archive_manifest.json` | `514b6b968444b4c7363e8f606bf73f690b41a997ab2a311e6953f29de59c898e` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/daily_portfolio_results.csv` | `62ee4eb8c8ae65fc8505cf8bff985201ee472b31f9556ca41b3500b72c07d8d9` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/daily_predictions_audit.csv` | `6f8ee45ffeba1325e715c7a30c5bab3fcab1e54c321bbde91fff39702e28d657` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/performance_summary.csv` | `b72cac4dae5d904befcfd1b59e8353efa5eadc430302f6488af83109cd8d0351` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/portfolio_valuation_audit.csv` | `529395642379dcdd716a10f9019103724e67bd6a77f157cd993f185d397d87d8` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/transactions.csv` | `68630934bd6ead91cc9a0c89cc3f2bc3d7ea6fd71d119949ba41d300318c0879` |

## Key structural results

- 13,167 daily rows, 67,633 position-valuation rows, 3,125 transaction rows, and 63 performance rows.
- 35 pairs have recorded positions and transactions; 28 are zero-holdings/all-cash for the full period.
- All 28 all-cash pairs record Cash and Portfolio_Value of 1,000,000 throughout. No explicit initial-equity baseline row exists.
- 378 stale valuation rows across six pairs are BANPU; maximum recorded age is 93 calendar days.
- For the 35 pairs with transactions, nonblank performance-summary transaction count, cost, and turnover fields reconcile to transaction records. For the 28 no-trade pairs those fields are blank.
- The archived performance summary has blank Sharpe, Sortino, Calmar, transaction, and stale-summary fields for the 28 all-cash pairs.

## Protected hash verification

The pre-audit baseline was captured before creating the new audit directory and covered 20,086 existing files under the repository (excluding `.git`). The final comparison excludes only the new audit directory and found all 20,086 hashes unchanged; there were zero mismatches, missing baseline files, or unexpected paths outside the new directory. The temporary baseline was removed after comparison.

## Prohibited-operation compliance

No market data was downloaded; no yfinance or other external data service was called. No source notebook or existing data/model/result file was edited. No metric, return, equity curve, or replacement performance result was calculated. No model, prediction, optimizer, or backtest was run. The Research Backtest Gate was not changed and Phase F was not started.

## Final status

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
