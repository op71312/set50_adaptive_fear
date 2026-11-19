# GLOBAL adjusted execution candidate: origin and transformation

## Finding
Notebook 05's saved execution records show the original execution snapshot was loaded, GLOBAL OHLC before 2026-02-24 was multiplied by `28/27` (`1.037037037037037`), and a corrected candidate was written. The lineage record reports 36 changed rows; Volume and Adj Close were unchanged. This confirms candidate creation and use for Notebook 05 diagnostics, not the adjustment's correctness or approval for historical execution.

## Artifact identity
- Candidate: `backtest_results/execution_data_v2/execution_ohlcv_corrected_v2.parquet`
- Candidate SHA-256: `4d35f215ce3a0243b13ef3eb582fc7904b0de8920ad85c78ee14497ff1fc5428`; size 324462 bytes.
- Filesystem mtime: `2026-11-15T20:57:16+07:00` (supporting evidence only; not proof of actual creation/use time).
- Source snapshot: `dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`; SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
- Immutable copy SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
- Recorded evidence status: `USER_PROVIDED_TERMS; OFFICIAL_SOURCE_URL_NOT_ATTACHED`; `exchange_verified=false`.

## Notebook evidence (static inspection of saved cells and outputs)
- Notebook 05 cell 20 (execution count 139): creates candidate from original snapshot and records lineage; saved output reports 36 changed rows and no Yahoo redownload.
- Cell 21 (count 140): loads candidate and derives eligibility/returns; saved output reports shape `(17430, 13)` and 17,332 bars eligible.
- Cell 22 (count 141): consumes candidate for tick-basis and execution-quality diagnostics.
- Notebook 05's saved later output states the 63 experiments were skipped. Current `backtest_run_status.json` records no new result files and no verified execution dataset.
- Notebook 06 cell 7 (execution count 16) loads the original snapshot, not the candidate; saved output reports `(17430, 10)`.

## Interpretation
Candidate use is confirmed for Notebook 05 diagnostics and candidate-derived diagnostic output. It is not confirmed for any portfolio-result package. An archived package exists; its exact historical input hashes are incomplete, so the exact candidate's involvement remains `UNKNOWN_INSUFFICIENT_EVIDENCE`. Candidate validity is unverified and is separate from the question of use.

This audit was read-only: no data download, yfinance call, notebook/pipeline execution, model fit, prediction generation, or backtest occurred.
