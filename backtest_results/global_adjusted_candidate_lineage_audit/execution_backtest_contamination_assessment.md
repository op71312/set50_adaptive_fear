# Execution and backtest contamination assessment

## Conclusion
- **Confirmed:** candidate loaded and consumed by Notebook 05 for eligibility and diagnostic calculations; candidate-derived diagnostic output exists.
- **Not confirmed:** any portfolio/backtest result package used this exact candidate.
- **Important:** an archived prior package exists. Its exact link to the candidate is `UNKNOWN_INSUFFICIENT_EVIDENCE`; do not claim no historical backtest ever occurred.
- **Current saved run:** Notebook 05 says 63 experiments were skipped; current status says no new result files and no verified execution dataset.

## Archived package facts
`backtest_results/superseded_20261115_pre_integrity_fixes/` contains:
- Performance summary: 63 rows, 63 distinct strategy/allocation pairs.
- Daily portfolio rows: 13167; transaction rows: 3125; valuation rows: 67633; prediction rows: 654381.
- GLOBAL rows in archived predictions / valuation / transactions: 0 / 0 / 0.
- Archive manifest expressly says the prior run used **adjusted Master OHLC as execution prices**. This names a different declared source than the exact corrected snapshot candidate.
- Archived output mtimes are around 2026-11-15 17:56 +07:00; candidate mtime is 2026-11-15T20:57:16+07:00. Timestamps are supporting evidence only.

The archive lacks a complete per-run source hash/configuration chain. Adjusted Master prices may overlap in basis, but that is not proof of exact candidate use. The absent GLOBAL symbol rows reduce evidence of direct GLOBAL trading/valuation in the result outputs, but do not rule out upstream risk/allocator influence.

This audit did not execute notebooks/pipelines, download data/call yfinance, train a model, generate predictions, or run a backtest/63 combinations. Existing archive outputs were not regenerated or modified. Gate remains `BLOCKED`; Phase F remains `DO_NOT_BEGIN`.
