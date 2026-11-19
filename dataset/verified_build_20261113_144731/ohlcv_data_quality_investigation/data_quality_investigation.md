# OHLCV Data Quality Investigation

Generated: 2026-11-13T15:24:46

## Executive Summary
Read-only audit of `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_144731`. 175 input/reference files were inventoried; every size and SHA-256 hash is unchanged. Baseline Master has 198,532 rows x 17 columns. No OHLCV was modified, no rows were deleted/filled, and no feature, target, or rank was recomputed.

Staged OHLCV has 205,152 rows across 83 symbols. Material Close/High/Low boundary violations (>1e-6): 193; >0.01: 179. Current Yahoo unadjusted bars confirm 193 listed anomaly rows. The Yahoo union-calendar proxy has 67 absent symbol/date rows (BANPU 63, SCB 4); this is not an official exchange calendar. Expected symbols without files: 8.

There are 117,663 common Date+Symbol pairs between the prior current Parquets and refreshed Yahoo data. 48,080 have at least one OHLC change above tolerance; 52 Volume values changed.

## Findings
- Strict and tolerance-based anomaly counts are in the symbol integrity summary and row-level `ohlc_anomalies.csv`.
- Yahoo action history coincides on 3 anomaly rows and is within five calendar days on 14. Timing is correlation, not proof of cause.
- Missing rows in combined calendar: BANPU 63, SCB 4. Other Yahoo symbols have data on those dates; official SET trading dates/suspensions were not checked.
- Many refreshed-only keys may reflect that prior Parquets were membership-filtered, not OHLCV revisions on common keys.
- Recent revision-window action lookup: TRUE 2026-11-13 dividend=0.16 split=0

## Root Cause Analysis
- Current Yahoo unadjusted responses reproduce some impossible bar relationships. This verifies the returned bars, not that Yahoo caused all anomalies; no independent official OHLCV source was queried.
- Corporate actions coincide with only some anomaly dates. Older action/adjustment snapshots are unavailable; action timing cannot explain all anomalies or revisions.
- Source-row absence for BANPU/SCB is verified. Whether each gap is a true trading day is unresolved without official exchange calendar or symbol-level suspension data.
- OHLC changes on common keys; coherent OHLC rescaling can be consistent with adjusted-history restatement but does not prove it. Volume changes confirm snapshot disagreement, not its cause.

## Evidence
- `source_file_inventory.csv`: names, sizes, row/column metadata and before/after hashes for originals, staging and Master.
- `historical_data_integrity.csv`: one record per staged symbol with first/last dates, row counts, missing OHLCV, anomaly counts and union-calendar coverage.
- `ohlc_anomalies.csv`: OHLCV, Period, deviation, adjacent observed dates, Yahoo unadjusted confirmation and action proximity.
- `missing_data_report.csv`: per-symbol date gaps and separate missing expected files.
- `yfinance_revision_report.csv` (summary) and `yfinance_revision_details.csv` (changed keys):
- Open: 48,039/117,663 changed (40.8276%); mean absolute difference=0.0016311638; max=0.17635458 on TRUE 2026-07-31.
- High: 48,080/117,663 changed (40.8625%); mean absolute difference=0.0016530348; max=0.17944873 on TRUE 2026-05-08.
- Low: 47,990/117,663 changed (40.7860%); mean absolute difference=0.0016080823; max=0.17393819 on TRUE 2026-05-20.
- Close: 47,990/117,663 changed (40.7860%); mean absolute difference=0.0016299371; max=0.17705631 on TRUE 2026-05-14.
- Volume: 52/117,663 changed (0.0442%); mean absolute difference=134.26567; max=3172917 on MINT 2026-11-11.
- Baseline Master duplicate Date+Symbol keys=0; rank-range violations=0.

## Potential Impact on Machine Learning
- OHLC anomalies may affect daily_return and dependent momentum_20d, volatility_ret, Corr_60d, VolRank, CorrRank and the next-return component of target. No such value was recomputed.
- Volume revisions may affect vol_z, its target input, and LiquidityRank through rolling trading value. No feature or rank was recomputed.
- Missing observations can make row-based windows span longer calendar intervals; the next observed return may bridge multiple sessions. Missing member dates also reduce the available rank cross-section.
- No look-ahead was introduced by this audit. Retrospective adjusted-price revisions remain a point-in-time concern; the prior adjustment snapshot is unavailable.

## Recommended Actions
- **Keep:** preserve originals, staging, and Master unchanged; retain hashes and source snapshots.
- **Flag:** mark OHLC boundary violations, BANPU/SCB gaps, and revised values. Keep them visible; do not impute.
- **Exclude:** do not delete rows during this investigation. Consider excluding flagged training examples only after review and a documented modeling decision.
- **Investigate Further:** compare anomalies/gaps with official SET price, trading-status and corporate-action records; retrieve archived vendor snapshots/adjustment factors; independently verify BANPU 2026-11-11 and recent volume revisions.

## Remaining Uncertainties
- The combined calendar is Yahoo-derived, not an official SET calendar.
- Root cause of each bar inconsistency and historical vendor revision remains unresolved.
- Current action history does not prove what the prior Yahoo snapshot contained or which adjustment factors were applied.
- No source data was corrected, forward-filled, interpolated, excluded, or re-ranked.

## Data Quality Classification
- Level 1 Verified: source hashes unchanged; baseline master key/rank-range checks recorded.
- Level 2 Suspicious: adjusted-price revisions and action associations whose exact mechanism is unproven.
- Level 3 Confirmed Issue: observed source bar constraints violated; expected file coverage is incomplete; source snapshots disagree on values/rows.
- Level 4 Unresolved: whether each proxy gap is an official trading day, why Yahoo omitted/revised particular values, and whether adjusted history creates point-in-time leakage.
