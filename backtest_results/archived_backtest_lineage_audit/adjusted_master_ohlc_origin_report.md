# Adjusted Master OHLC origin and GLOBAL comparison

## Conclusion
The archive manifest's phrase **“adjusted Master OHLC as execution prices” does not identify an exact file**. It contains no path, SHA-256, build ID, input manifest, or run ID. The repository has three distinct Master variants. Their hashes differ, so they cannot be treated as the same artifact. They have the same GLOBAL OHLCV values on 2,638 matching date rows, but this does not establish which exact file the archive consumed.

The best documented local feature-Master lineage is separate from the corrected execution candidate: Notebook 03 cell 31 (saved execution count 51) uses `yf.download(..., auto_adjust=True, group_by="ticker")` to stage `source_ohlcv`; the `actions` argument is not specified. Cell 32 (count 52) builds the Master from that staged source and effective-period SET50 membership. GLOBAL Master OHLCV equals its staged source values on all 2,638 overlapping GLOBAL rows. Notebook 05's current `FEATURE_MASTER_PATH` points to the VolZ_Fixed variant, but this is only static current-code evidence and not a historical archive input hash.

## Distinct local Master artifacts
| Label | Path | Rows | Symbols | GLOBAL rows | Bytes | SHA-256 |
|---|---|---:|---:|---:|---:|---|
| `master` | `dataset\verified_build_20261113_152948\SET50_Master_Dataset.parquet` | 198,532 | 83 | 2,638 | 15,332,229 | `ef060baedd779a99b83a7cfa74b4bde20eb7bcf30fc1c05679f11b3c8c459f07` |
| `sorted` | `dataset\verified_build_20261113_152948\SET50_Master_Dataset_DateSymbol_Sorted.parquet` | 198,532 | 83 | 2,638 | 15,595,564 | `1ceef21d118c480ffe356e9604e9b2452dd20c5ba91537c40ef5a3e639c9d848` |
| `fixed` | `dataset\verified_build_20261113_152948\SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet` | 198,532 | 83 | 2,638 | 15,595,544 | `7424f01e92d4f507b2a5956898e1ef30050de7a50c7c4ee9a9aa402af4271505` |

For GLOBAL only, the three files' stored OHLCV values match row-for-row on all 2,638 shared keys. Their whole-file SHA-256 values differ. The exact archive source is `UNKNOWN_INSUFFICIENT_EVIDENCE`.

## Documented feature source
- Staged file: `dataset/verified_build_20261113_152948/source_ohlcv/GLOBAL.BK.parquet`; 2,742 rows, six columns, 2015-08-03 through 2026-11-13; SHA-256 `1dcef0bf67eca52f1f84237838a64e3075fd235277d6d2238aa6c8cfc6b40bf1`.
- `Download_Manifest.csv` reports GLOBAL downloaded with 2,742 rows, first date 2015-08-03, last date 2026-11-13, no missing OHLCV rows and no duplicate dates. The manifest does not include per-file hashes, yfinance version, retrieval time, interval, timezone, action setting, or requested ticker list.
- Notebook 03 cell 31 supplies `start=2015-08-01`, dynamic end=today+1, `auto_adjust=True`, `group_by="ticker"`; it does not pass `actions`.
- Notebook 03 cell 32 reads effective-period constituents/declaration dates, derives per-symbol features, creates an effective-period market proxy, and ranks `VolRank`, `CorrRank`, and `LiquidityRank` among period members. Ranks are left missing outside active membership.
- `dataset/parquet/GLOBAL.BK.parquet` is a distinct legacy file: 2,061 rows for 2017-01-04 through 2025-06-30, SHA-256 `61ac73480f8dbe09e57a6641016197d2eb0216a800a1890f79d5b54171228e1a`. On its 2,061 date overlap with staged feature source, Volume matches on all rows, but each OHLC column differs on 1,102 rows. This further demonstrates distinct local data versions; it does not identify the archive input.

## GLOBAL vs the execution candidate
Execution snapshot: `dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`, SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`, 17,430 rows, 10 columns; lineage records `auto_adjust=false`, `actions=true`, but interval, group_by and requested ticker list are UNKNOWN.

Corrected candidate: `backtest_results\execution_data_v2\execution_ohlcv_corrected_v2.parquet`, SHA-256 `4d35f215ce3a0243b13ef3eb582fc7904b0de8920ad85c78ee14497ff1fc5428`. Its sidecar records a 28/27 factor on GLOBAL OHLC before 2026-02-24 (36 changed rows), no Volume/Adj Close changes, `exchange_verified=false`, and evidence status `USER_PROVIDED_TERMS; OFFICIAL_SOURCE_URL_NOT_ATTACHED`.

Read-only comparison of stored GLOBAL rows:
- Master vs staged `auto_adjust=True` source: exact OHLCV equality on all 2,638 shared rows.
- Master vs original execution snapshot: Open/High/Low equal 174/210 each; Close equal 173/210; Volume equal 209/210.
- Master vs corrected candidate: Open/High/Low equal 174/210 each; Close equal 173/210; Volume equal 209/210.
- Original snapshot vs corrected candidate: 36 stored pre-boundary OHLC rows differ; Volume is unchanged on all 210 GLOBAL rows.

These are comparisons of existing values only; no price transformation or corrected dataset was generated. The feature Master is not byte-identical to the candidate, and their pre-boundary GLOBAL OHLC values are not identical. The archived results still cannot be linked or excluded from the exact candidate because the run input chain is missing.

## Evidence references
- `03_feature_engineering.ipynb` cells 31-32 (saved execution counts 51-52).
- `05_backtest.ipynb` cell 3 (saved code names fixed Master and separate execution paths); cells 20-22 are later candidate diagnostics, not the archived run.
- `execution_data_lineage.json`, execution snapshot sidecar, `Download_Manifest.csv`, three Master files, GLOBAL source/legacy files, and `archive_manifest.json`.
