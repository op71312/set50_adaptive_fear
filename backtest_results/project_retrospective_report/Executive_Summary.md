# Executive Summary

## SET50 Adaptive Fear & Alpha System

This retrospective uses repository artifacts only. No model was retrained, no data was downloaded, and no historical backtest was rerun.

### Research objective and architecture

The project classifies market states as Panic, FOMO, and Normal, then maps predicted states into nine Buy/Sell/Hold strategies and compares seven constrained allocation methods. The documented pipeline is vendor OHLCV and half-year membership → target/feature engineering → time-ordered model selection → frozen Softmax model → 2026 predictions → strategy/allocation simulation → costs, valuation, and PRICE_RETURN reporting.

### Model

The frozen artifact is a StandardScaler + multinomial Logistic Regression pipeline with six inputs: `daily_return`, `momentum_20d`, `vol_z`, `VolRank`, `CorrRank`, and `LiquidityRank`. The saved 2026 test report gives accuracy 83.05%, Macro F1 0.3936, balanced accuracy 0.3932, and log loss 0.7459. Normal-class F1 is 0.9096, while Panic F1/recall are 0.1075/0.0907 and FOMO F1/recall are 0.1638/0.1800. Overall accuracy is therefore not a sufficient measure of usefulness for minority-state actions.

The saved training notebook records a 94,205-row 2016–2024 training split, 11,824-row 2025 validation split, and 10,436-row 2026 test split. No immutable hash of the exact training table exists; the model-to-training lineage is partial.

### Backtest

The named baseline is `RPR2-2DF88EE33C7C4A88BBE2CA46B3F79565`. Its output package contains 63 `COMPLETED_WITH_LIMITATIONS` combinations, 149 simulation sessions from 2026-03-31 through 2026-11-13, and 7,301 predictions. It uses Yahoo-vendor raw Open prices on an `OBSERVED_VENDOR_CALENDAR`, theoretical fractional shares, 0.1% per-side slippage, and 0.16799% per-side fees. It excludes BANPU and GLOBAL, applies no unverified corporate actions, and reports PRICE_RETURN without annualization or dividend/TSR claims.

Across combinations, exported PRICE_RETURN ranges 0.00%–23.89% and maximum drawdown ranges -8.39%–0.00%. Transaction costs total THB 532,367.38 across all combination records (fees THB 333,736.72; slippage THB 198,630.66). All 63 combinations have stale count zero on the vendor-observed calendar; that does not verify stale-age policy in exchange sessions. S5/S6/S8/S9 correctly remain all-cash in the exported accounting.

This retrospective independently checked the existing output files: 9,450 daily rows reconcile `Cash + Market_Value` exactly to `Portfolio_Equity`; all 63 start at THB 1,000,000; and recomputed unannualized return, maximum drawdown, and transaction cost match the stored summary/ledger. These checks validate output arithmetic only—not price validity, exact run-source identity, or exchange execution.

### Limitations and defensible conclusion

Important unresolved issues include 2017_H1 membership, 141 unconfirmed corporate-action ledger events, incomplete source request provenance, no official SET calendar, no verified board-lot schedule, and no complete frozen-model training hash. The current Notebook 08 hashes do not match the hash recorded by the named baseline run. Another RPR2 output directory has a different Run ID and Prediction Snapshot ID and is not combined with the named baseline here.

The outputs are suitable only as a **provisional, exploratory Research Proxy baseline** for code and accounting analysis. They are not verified tradable performance, not evidence of Total Shareholder Return, and not a causal demonstration of alpha. No gate was changed: run-scoped research gate `CONDITIONAL_OPEN`, execution validation `BLOCKED`, canonical historical gate `BLOCKED`, and Phase F `DO_NOT_BEGIN`.

See [Master Technical Report](./SET50_Adaptive_Fear_Alpha_System_Comprehensive_Technical_Report.md), [Research Limitations](./Research_Limitations.md), and [Backtest_63_Combination_Summary.csv](./Backtest_63_Combination_Summary.csv).
