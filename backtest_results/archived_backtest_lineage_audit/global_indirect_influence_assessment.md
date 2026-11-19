# GLOBAL indirect-influence assessment

## Summary
GLOBAL's absence from 2026 prediction, valuation, and transaction rows does **not** establish zero upstream influence. The available feature build has a confirmed historical cross-sectional data path from GLOBAL to other member features during periods when GLOBAL was a SET50 constituent. Whether the exact archived model used that feature build, or whether GLOBAL entered archived risk matrices/weights, is `UNKNOWN_INSUFFICIENT_EVIDENCE`.

| Pathway | Classification | Evidence and limit |
|---|---|---|
| 2026 eligibility / predictions | `NO_PATH_IDENTIFIED_WITHIN_INSPECTED_SCOPE` | Local 2026_H1/H2 lists each contain 50 members and exclude GLOBAL. Archived prediction rows contain 54-symbol union, no non-members, exact full H1 member coverage, and 63 missing H2 BANPU rows; no GLOBAL rows. Archive does not hash-pin membership inputs or code. |
| Direct portfolio execution / valuation | `NO_PATH_IDENTIFIED_WITHIN_INSPECTED_SCOPE` | GLOBAL has 0 rows in archived transactions and valuation, and is absent from the archived prediction rows. This rules out an observed GLOBAL position in these CSVs, not upstream effects. |
| Historical feature ranks / market proxy | `INDIRECT_INFLUENCE_CONFIRMED` | Local membership file includes GLOBAL from 2017_H1 through 2025_H1; stored feature Master has 2,061 GLOBAL rows with all three rank columns present. Notebook 03 cell 32 forms member-period market returns and ranks across the active member set. GLOBAL returns enter other members' proxy/rank groups when it is a member. This confirms a feature-generation path, not the magnitude of rank changes. |
| Frozen model / archived predictions | `UNKNOWN_INSUFFICIENT_EVIDENCE` | Notebook 04 reads the fixed Master, filters member rows, and trains on Target_Date 2016-2024; GLOBAL is a member in much of that window. But frozen model metadata and archived prediction CSV do not pin the training feature hash/model hash. |
| Risk return matrix, volatility, covariance/correlation | `UNKNOWN_INSUFFICIENT_EVIDENCE` | Archive has no risk matrix, estimation dates, cutoff, source hash, or risk universe. Current Notebook 05 code forms history from symbols passed by the allocation function; current execution path passes Buy names. The historical archived code version is not hash-linked, so that behavior cannot be projected onto the archive. |
| ERC/HRP/MinVar/CVaR/MPT weights and hierarchy | `UNKNOWN_INSUFFICIENT_EVIDENCE` | No raw/final weights, covariance, correlation, cluster tree, solver diagnostics, or weight audit is archived. Current code is only static evidence and is not tied to the historical run. |
| Candidate-specific influence | `UNKNOWN_INSUFFICIENT_EVIDENCE` | No archived input hash or name points to `execution_ohlcv_corrected_v2.parquet`. The local feature Master is separately built from `auto_adjust=True` source files and its stored GLOBAL values differ from the candidate. Missing run hashes prevent a definitive non-use claim. |

## Direct vs indirect interpretation
The 2026 point-in-time membership evidence offers no identified path for GLOBAL to be a 2026 eligible signal or held security. Separately, GLOBAL historical member data can influence cross-sectional training features: VolRank, CorrRank, LiquidityRank, and the member-period market proxy. Since the model's training period is 2016-2024, that feature path overlaps the stated training window. The existing model hash is known, but its training dataset hash is not; therefore the feature path cannot be promoted to confirmed contamination of the archived predictions or allocation results.

No counterfactual ranks, predictions, risk estimates, weights, or backtests were calculated.
