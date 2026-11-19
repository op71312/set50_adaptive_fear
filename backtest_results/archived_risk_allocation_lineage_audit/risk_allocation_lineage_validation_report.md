# Risk and Allocation Lineage Audit — Validation Report

## Result

Audit deliverables and structural checks are complete. Historical risk/allocation lineage remains **BLOCKED** because the archived package has no risk inputs, dated Buy Universe, allocation weights, or solver diagnostics. A successful evidence-inventory check does not imply historical readiness.

## Minimum checks

| # | Check | Result | Evidence / limitation |
|---:|---|---|---|
| 1 | Six expected archived artifacts exist and SHA-256 digests were recorded. | PASS | Hash table below; archive files were read only. |
| 2 | Five archived output CSV sizes match `archive_manifest.json`. | PASS | Manifest `files` size metadata agrees with the inspected CSV byte sizes. |
| 3 | Prediction, daily, and performance outputs contain all 63 strategy/allocation pairs. | PASS | 9 strategy IDs × 7 method labels; 13,167 daily rows, 654,381 prediction rows, 63 performance rows. |
| 4 | Pair labels are a complete Cartesian set of nine IDs and seven method labels. | PASS | IDs S1–S9; EW, IV, ERC, HRP, MinVar, CVaR, MPT. This validates labels only, not archived method definitions. |
| 5 | Daily and prediction date coverage agrees by pair. | PASS | 209 decision dates per pair; daily execution dates cover 2026-01-06–2026-11-13. Date alignment does not verify an official exchange calendar. |
| 6 | Transaction and valuation coverage is internally consistent. | PASS | Both cover 35 pairs; other 28 pairs have zero holdings in daily records. No allocator lineage is implied. |
| 7 | Direct GLOBAL output presence was checked. | PASS | Zero GLOBAL rows in archived predictions, transaction symbols, and valuation symbols. This is not a test of risk-input presence. |
| 8 | Archived standalone return/risk/covariance/correlation/Buy-set artifacts were inventoried. | PASS_WITH_LIMITATIONS | None found in the inspected `dataset/` and `backtest_results/` artifacts; absence cannot identify unrecorded in-memory inputs. |
| 9 | Historical Buy Universe was identified or reconstructed. | PASS_WITH_LIMITATIONS | Correctly left `UNKNOWN`; archive has no explicit per-date Buy set. No reconstruction was performed. |
| 10 | Historical risk universe and risk input provenance were established. | PASS_WITH_LIMITATIONS | Correctly left `RISK_UNIVERSE_UNKNOWN`; no matrix, cutoff, source hash, or symbol list is archived. |
| 11 | Each of seven historical allocation implementations was verified. | PASS_WITH_LIMITATIONS | Matrix has one row per method; all historical implementations remain unknown because no run-linked code or allocation logs exist. |
| 12 | Raw/final weights and historical solver results were located. | PASS_WITH_LIMITATIONS | None recorded in archive outputs; current notebook code was not attributed to the archive. |
| 13 | Current notebook and approved Phase E references were distinguished from archive evidence. | PASS | Notebook 05 saved output says gate closed and all 63 experiments skipped; Notebook 06 saved output is blocked. Neither notebook is hash-linked to the archive. |
| 14 | Protected-input hashes were compared before/after deliverable creation. | PASS | 549 pre-existing protected paths compared against the pre-audit baseline; zero mismatches, missing paths, or unexpected protected paths. New audit directory excluded. |
| 15 | Prohibited operations were avoided during this audit. | PASS | No market-data download, yfinance call, model operation, prediction, optimization, historical backtest, 63-combination run, gate change, or Phase F action was performed. |

**Counts:** PASS = 10; PASS_WITH_LIMITATIONS = 5; FAIL = 0.  
**Audit evidence validation:** PASS_WITH_LIMITATIONS.  
**Historical risk/allocation lineage:** BLOCKED.

## Archived artifact SHA-256

| Artifact | SHA-256 |
|---|---|
| `backtest_results/superseded_20261115_pre_integrity_fixes/archive_manifest.json` | `514b6b968444b4c7363e8f606bf73f690b41a997ab2a311e6953f29de59c898e` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/daily_portfolio_results.csv` | `62ee4eb8c8ae65fc8505cf8bff985201ee472b31f9556ca41b3500b72c07d8d9` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/daily_predictions_audit.csv` | `6f8ee45ffeba1325e715c7a30c5bab3fcab1e54c321bbde91fff39702e28d657` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/performance_summary.csv` | `b72cac4dae5d904befcfd1b59e8353efa5eadc430302f6488af83109cd8d0351` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/portfolio_valuation_audit.csv` | `529395642379dcdd716a10f9019103724e67bd6a77f157cd993f185d397d87d8` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/transactions.csv` | `68630934bd6ead91cc9a0c89cc3f2bc3d7ea6fd71d119949ba41d300318c0879` |

## Protected hash verification

The pre-audit baseline enumerated 549 protected paths, including Notebook 05/06 and files under the protected data/model/result inputs. The post-audit comparison found:

- Baseline protected paths: 549
- Unchanged hashes: 549
- Hash mismatches: 0
- Missing protected paths: 0
- New files among the protected paths: 0

Only the nine deliverables in `backtest_results/archived_risk_allocation_lineage_audit/` were created for this workstream. No existing notebook, dataset, model, or Phase A–D artifact was edited.

## Current policy and code are not archive evidence

The approved Phase E specification remains a policy reference. Its full 60/252 common windows, centered sample covariance, no-fallback behavior, and method-specific constraints do not establish archived behavior. Current Notebook 05 static source includes legacy 50/200 minimum-history settings, Ledoit-Wolf estimators, EW fallbacks, and solver settings different from approved Phase E. Current Notebook 06 saved state allows EW/IV only and remains fail-closed. No archived run ID or source hash connects either notebook state to the superseded archive.

## Final status

`RISK_ALLOCATION_LINEAGE_AUDIT = COMPLETED / BLOCKED`  
`ARCHIVED_BUY_UNIVERSE = UNKNOWN`  
`HISTORICAL_RISK_UNIVERSE = UNKNOWN`  
`HISTORICAL_SOLVER_EVIDENCE = UNKNOWN`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`

No evidence was synthesized to replace absent historical records. No further workstream was started.
