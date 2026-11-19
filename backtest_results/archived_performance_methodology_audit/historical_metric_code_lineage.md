# Historical Metric Code Lineage

## Archived artifacts

The archive directory `backtest_results/superseded_20261115_pre_integrity_fixes/` contains the manifest and five output CSVs. The manifest identifies the archive as `superseded_not_for_strategy_selection`, dated 2026-11-15, and records the known initial-equity, stale BANPU, adjusted-price, and cap issues. It records file sizes but no run ID, Notebook 05 hash, metric-code hash, input hashes, formula configuration, or link from a saved cell to `performance_summary.csv`.

The 63-row performance file is an archived output. The current notebook code and its saved output are separate evidence. A matching filename, metric label, or formula is not a run link.

## Current saved Notebook 05 reference

- Current Notebook 05 SHA-256: `b249fdc28ace8c546b15ca2e6ec25371fa9bfa84af201fcc9762c3fc6077be41`.
- Cell index 43; execution count 151: defines `run_backtest`, with an explicit `BACKTEST_GATE_OPEN` guard.
- Cell index 45; execution count 152; input timestamp `2026-11-15T12:00:27.301575Z`: defines `calculate_performance`. It inserts an initial row, uses `final_value / initial_equity - 1`, computes CAGR from calendar days / 365.25, annualizes sample daily standard deviation and Sharpe with sqrt(252), assumes a zero risk-free rate implicitly, computes Sortino from negative returns only, calculates drawdown from a running peak, and computes Calmar as CAGR / abs(Max Drawdown) for a negative drawdown.
- Cell index 46; execution count 153: saved synthetic regression fixture output tests a supplied two-point equity fixture and initial-capital/drawdown behavior. It is not a historical backtest result.
- Cell index 53; execution count 156; input timestamp `2026-11-15T12:00:27.325958Z`: saved output states the gate is closed, all 63 experiments were skipped, and no portfolio result CSVs were written.

The current code sets `INITIAL_CASH = 1,000,000`, `INITIAL_DATE = 2026-01-05`, cost rates and a five-calendar-day stale threshold. Its saved metric function and fixture do not prove that it generated the archived summary. The archived BANPU age of 93 calendar days is incompatible with the current saved five-day mark-to-market guard.

## Current saved Notebook 06 reference

- Current Notebook 06 SHA-256: `4b390d06306f74bd9360768fa2ce9ac86a86429fcf6cac66f1bc7800748a1a1c`.
- Cell index 20; execution count 22: a separate current `calculate_performance_metrics` function inserts an initial equity point, uses calendar-day / 365.25 CAGR, sample daily standard deviation, sqrt(252) annualization, and a configured daily risk-free rate of 0.0 for Sharpe. It defines Sortino as RMS of negative-clipped returns.
- Cell index 22; execution count 23: current single-run harness calls this function. It is not linked to the archived output.
- Cell index 26; execution count 25 and cell index 28; execution count 26: saved audit output is BLOCKED and records `63 combinations executed: False`.

## Linkage conclusion

| Evidence layer | Available? | Finding |
|---|---|---|
| Current metric code | Yes | Static code references in Notebooks 05 and 06. |
| Saved notebook code and execution counts | Yes | Current saved cells, not historical archive identity. |
| Saved metric-related output | Yes | Synthetic regression fixture in Notebook 05; blocked audit in Notebook 06. |
| Archived metric CSV | Yes | 63 summary rows with metric values and some blank fields. |
| Code/run identity linking formulas to archive | No | No run ID, code hash, formula log, or metric input hash in archive. |

`HISTORICAL_METRIC_CODE_LINK = UNKNOWN_INSUFFICIENT_EVIDENCE`  
`CONSUMPTION_CONFIRMED = NOT ESTABLISHED`
