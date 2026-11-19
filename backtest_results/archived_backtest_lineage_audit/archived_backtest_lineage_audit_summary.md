# Archived backtest lineage audit summary

## Findings
- Archived directory contains 6 artifacts: one archive manifest and five result CSVs.
- Stored SHA-256 computed for all 6 archive artifacts. Archive manifest byte sizes match 5/5 result-file entries. A later validation-only manifest has a matching hash for 1 archived CSV.
- Performance summary, daily portfolio, and prediction files align on 63 strategy/allocation pairs. Daily rows are 209 per pair. Transactions and valuation records cover 35 pairs; the remaining 28 pairs have zero daily holdings.
- GLOBAL is absent from 2026 predictions, transactions, and valuation. Local 2026 membership also excludes it. The exact archived risk inputs and weights are not saved.
- GLOBAL has a confirmed path into historical SET50-period cross-sectional features: it is a member from 2017_H1 through 2025_H1, its staged feature-source OHLCV matches the base Master on all 2,638 shared rows, and Notebook 03 calculates member-period ranks/market proxy. Whether this exact feature build was used by the frozen model and archive is not hash-verified.

## Adjusted Master identity
The exact Adjusted Master used as execution prices is **UNKNOWN**. Local base, sorted, and VolZ_Fixed Master variants have distinct SHA-256 values; the archive records no path/hash. Their GLOBAL OHLCV values match each other on 2,638 rows and match the staged `auto_adjust=True` feature source, but differ from the `auto_adjust=False` execution candidate on pre-boundary rows.

## Candidate link
The candidate was derived from the execution snapshot with a metadata hash chain, but has no archived source-hash reference. Its exact link to historical results is `UNKNOWN_INSUFFICIENT_EVIDENCE`; no non-use conclusion is inferred from filenames or mtimes.

## Lineage status counts
- `DERIVATION_CONFIRMED`: 3
- `HASH_VERIFIED`: 1
- `METADATA_REFERENCE_ONLY`: 5
- `NO_REFERENCE_FOUND`: 1
- `STATIC_CODE_REFERENCE_ONLY`: 1
- `UNKNOWN_INSUFFICIENT_EVIDENCE`: 6


## Archived package status
`HISTORICAL_OUTPUTS_EXIST`; `INPUT_LINEAGE_PARTIALLY_VERIFIED`; `METHODOLOGY_NOT_VALIDATED`; `KNOWN_POLICY_MISMATCH`; `GLOBAL_INFLUENCE_UNKNOWN`; `SUPERSEDED`; `NOT_SUITABLE_AS_VALIDATED_RESEARCH_RESULT`.

## Recommended next evidence
Recover the original archived run's source-control commit/notebook hash, exact Master/feature/model/input hashes, run ID/configuration, point-in-time eligible and risk universes, risk matrices/cutoffs, allocation weights/solver diagnostics, and execution/valuation policy artifacts. This is an evidence request only; no rerun is authorized.

`ARCHIVED_BACKTEST_LINEAGE_AUDIT_COMPLETED`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
