# Validation report

**PASS — 17 passed, 0 failed.**

## Checks
- [PASS] Archive directory inventory: One manifest plus five CSV files found.
- [PASS] Archive manifest sizes: 5 listed file sizes compared.
- [PASS] Archive output hashes computed: 6 stored artifact hashes computed.
- [PASS] 63 pair universe: Summary, daily and prediction sets contain 63 pairs.
- [PASS] Daily rows per pair: 13,167 daily rows, 209 per each of 63 pairs.
- [PASS] Prediction date/pair alignment: Pairs and decision dates align structurally.
- [PASS] Transactions/valuation coverage: 35 pairs have position records; 28 remaining pairs are zero-holdings throughout.
- [PASS] Membership row comparison: No nonmember prediction symbols; 63 missing H2 rows are BANPU.
- [PASS] GLOBAL absent from archived final symbol rows: Prediction/valuation/transaction GLOBAL rows: {'predictions': 0, 'valuation': 0, 'transactions': 0}.
- [PASS] Feature source to Master GLOBAL values: All 2,638 shared GLOBAL OHLCV rows match.
- [PASS] Master variants remain distinct artifacts: Three local Master variants have three distinct hashes.
- [PASS] Candidate provenance hashes: Snapshot and corrected candidate hashes match execution_data_lineage.json.
- [PASS] Prior archive prediction hash: Prediction audit hash matches the later validation-only manifest.
- [PASS] Protected inputs unchanged: 315 protected files hashed; mismatches=0, missing=0.
- [PASS] No forbidden operations: No internet/download/yfinance calls, notebook/pipeline execution, model loading/fitting, prediction/weight generation, or backtest was performed.
- [PASS] Gate and Phase F preserved: Research Backtest Gate remains BLOCKED; Phase F remains DO_NOT_BEGIN.
- [PASS] Unknown links preserved: Candidate-to-archive and archive risk/model links remain explicitly unknown.


## Integrity and scope
- Protected inputs hashed before/after: 315; mismatches: 0; missing after: 0.
- Notebook 05/06, frozen model/metadata, source datasets, archived files, and Phase A-E/reassessment outputs are included in the hash comparison where present.
- Existing outputs were inspected, not regenerated. Archived hash/row comparisons are structural consistency checks, not backtest reproduction or methodology validation.
- The candidate's exact archived use, archived model/data lineage, and risk/allocation universe remain `UNKNOWN_INSUFFICIENT_EVIDENCE`.
- No internet or external services were accessed; no market data downloaded; no notebook/pipeline run; no model fit/load; no predictions, weights, or backtests generated.

`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
