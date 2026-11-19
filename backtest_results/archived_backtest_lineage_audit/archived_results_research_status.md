# Archived 63-combination package: research status

## Status labels
- `HISTORICAL_OUTPUTS_EXIST`: **YES** — five result CSVs plus the archive manifest are present.
- `INPUT_LINEAGE_PARTIALLY_VERIFIED`: **YES** — archive metadata names adjusted Master OHLC as the execution-price basis; stored output sizes match 5/5 manifest entries; the later validation-only manifest hashes the archived prediction audit and that hash matches. Exact historical input files/hashes remain missing.
- `INPUT_LINEAGE_VERIFIED`: **NO**.
- `METHODOLOGY_NOT_VALIDATED`: **YES** — no source/run hash chain, exact execution data ID, risk matrices, weights, or complete execution/valuation configuration.
- `KNOWN_POLICY_MISMATCH`: **YES** — archive manifest records single-asset cap bypass, return/CAGR calculation without initial-equity baseline, and BANPU stale valuation reaching 93 calendar days. Archived output includes BANPU: 9198 prediction rows, 44 transactions, and 844 valuation rows.
- `GLOBAL_INFLUENCE_UNKNOWN`: **YES** for archived model/risk/allocation outputs; historical feature-generation cross-sectional pathway is confirmed separately in the feature pipeline.
- `SUPERSEDED`: **YES** — archive manifest status is `superseded_not_for_strategy_selection`.
- `NOT_SUITABLE_AS_VALIDATED_RESEARCH_RESULT`: **YES**.

## What can be concluded
The archive contains 63 distinct strategy/allocation performance rows and 13,167 daily portfolio rows (209 rows per pair). Prediction rows contain all 63 pairs, 10,387 rows per pair, and 209 decision dates. Daily portfolio decision dates match prediction dates. Transactions and valuation rows cover the same 35 pairs; the other 28 pairs have zero holdings in every daily row, consistent with no position rows. These are structural checks on stored outputs, not proof of correct inputs or calculations.

The prediction universe has 54 symbols and no GLOBAL rows. Local 2026 membership lists exclude GLOBAL; all archived H1 member-date slots are present, while 63 H2 slots are missing, all BANPU. There are no GLOBAL rows in transactions or valuations. These facts support no observed GLOBAL position; they do not prove that no upstream historical feature or risk input used GLOBAL.

## What cannot be concluded
The exact “Adjusted Master OHLC” file, its input hash, archive run ID, code version, model version, prediction input hash, risk matrix/universe/cutoff, allocation weights, or execution configuration cannot be recovered from the archive. The archived metrics must not be used as approved/validated performance or as a reproducible baseline. This audit does not declare them valid or invalid solely from missing provenance.

## Stop status
No results were rerun, reproduced, recalculated, or modified. `RESEARCH_BACKTEST_GATE = BLOCKED`; `PHASE_F = DO_NOT_BEGIN`. Do not automatically start Workstream 2.
