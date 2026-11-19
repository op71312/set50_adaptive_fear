# BANPU Impact Isolation — Phase C

## Execution data

- BANPU remains excluded for all of 2026 with the unchanged reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`.
- The original snapshot still contains 253 missing OHLC cells across 64 BANPU rows (2026-08-13 through 2026-11-13); no prices were filled.
- Those execution OHLC values are not used by the Master feature rank or market-proxy formulas. The missing execution bars therefore do not directly enter shared feature calculations.

## Shared feature effects

- The pinned Master has 147 BANPU feature rows in 2026 ({'2026_H1': 118, '2026_H2': 29}); the last BANPU feature observation before the execution-missing interval is 2026-08-11. There is one late BANPU feature row on 2026-11-13, which has no next observed execution date and is not an eligible predictor row.
- Notebook 03 computes same-date cross-sectional VolRank/LiquidityRank and a SET50 market proxy. For each other member, the leave-one-out proxy includes BANPU's return when present; `Corr_60d` then uses a 60-observation rolling window.
- The first predictor date whose current and trailing 60 observed feature dates contain no BANPU row is 2026-11-09. The Phase C universe excludes earlier dates; this is a date-bounded restriction, not a rebuild of the Master.

## Propagation through Notebook 06

- The edited `generate_predictions` function applies the approved exclusion policy before the frozen model's `predict` and `predict_proba` calls.
- The targeted test confirms BANPU is removed from model input. The full synthetic regression cell passed 18/18 tests.
- The saved notebook output block contains 18 passing rows and matches the fresh run result; the fresh run result is also preserved in `notebook_06_synthetic_regression_results.csv`.
- Downstream runner guards still filter predictions/execution data before signals and contain order/holding exclusion checks. No actual allocation, order, holding, or valuation outputs were produced because no backtest was run.

## Classification

`PASS_WITH_LIMITATIONS` for the BANPU missing-execution issue within the eligible Phase C candidate sample: BANPU is excluded, its execution gaps are not feature inputs, its precomputed feature influence is excluded by a 60-observation date washout, and its own late feature row cannot be executed. The historical Master remains unchanged; no claim is made that BANPU never influenced features outside the eligible date window.
