# Feature Master Lineage Report

## Candidate artifacts and hashes

| Artifact | Path | Rows / shape | SHA-256 | Evidence |
|---|---|---:|---|---|
| Base Master (current build) | `dataset/verified_build_20261113_152948/SET50_Master_Dataset.parquet` | 198,532 × 17 | `ef060baedd779a99b83a7cfa74b4bde20eb7bcf30fc1c05679f11b3c8c459f07` | Current file hash and Parquet structure |
| Sorted Master | `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted.parquet` | 198,532 × 17 | `1ceef21d118c480ffe356e9604e9b2452dd20c5ba91537c40ef5a3e639c9d848` | Current file hash and Parquet structure |
| VolZ_Fixed Master | `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet` | 198,532 × 17 | `7424f01e92d4f507b2a5956898e1ef30050de7a50c7c4ee9a9aa402af4271505` | Current file hash; saved Notebook 04 cell 3 names this path |
| Earlier base Master | `dataset/verified_build_20261113_144731/SET50_Master_Dataset.parquet` | 198,532 × 17 | `f31177247af1bb1d11072316539041a6bf5681011f2c137309abffcff7f57746` | Separate candidate; no historical run linkage |
| GLOBAL feature source | `dataset/verified_build_20261113_152948/source_ohlcv/GLOBAL.BK.parquet` | 2,742 rows | `1dcef0bf67eca52f1f84237838a64e3075fd235277d6d2238aa6c8cfc6b40bf1` | Current source-file hash |

The Masters are distinct files with distinct hashes. A current notebook path reference does not prove which historical bytes were consumed.

## Notebook 03: feature source to Master

`03_feature_engineering.ipynb` saved cells 31–32 have execution counts 51–52:

- Cell 31 stages OHLCV files under `verified_build_*/source_ohlcv` and records `auto_adjust=True`, `group_by="ticker"`, 83 symbols in saved output. It does not specify the `actions` argument. The downloaded data was not acquired by this audit.
- Cell 32 reads the staged source, `SET50_constituents_by_halfyear_2016_2026.csv`, `set50_declare_dates_2016_2026.csv`, and `dataset/summary/stock_summary.parquet`; it writes the base `SET50_Master_Dataset.parquet` and quality reports.
- The code computes member-period return and liquidity/volatility features, `Corr_60d`, and the `VolRank`, `CorrRank`, and `LiquidityRank` cross-sectional ranks.
- The market proxy is built period by period from effective-period member returns; member series use leave-one-out returns. Rank calculations use that period's member list and available values. Missing symbols/dates are not synthesized.
- Saved output for the 2017_H1 quality check records 49 expected members, 44 available files, and 120 dates. The current Master structurally contains 5,160 member rows in that period (43 members × 120 dates), leaving 720 member-date slots absent.

These notebook states evidence a feature-generation path and saved output, but the build does not provide a complete per-input SHA-256 manifest tying every source file and membership file to the Master hash.

## Notebook 04: Master to model

`04_model.ipynb` cell 3 (execution count 3) reads the VolZ_Fixed path listed above. Saved cells 29–39 (execution counts 26–36) then use the half-year membership file, construct the candidate modeling rows, drop missing labels/features, and split by target year. Cells 52–53 configure and execute the five-fold GridSearchCV. Cell 84 (execution count 101) writes the best estimator to the current model path.

The saved execution outputs provide path-level consumption evidence and candidate dataset summaries. They do not record SHA-256 values for the Master, membership CSV, in-memory modeling rows, or estimator at the moment of execution. The later current file hashes cannot retroactively establish the bytes consumed.

The prompt mentions `04_model_training.ipynb`; that filename is unavailable in the repository. The relevant available notebook is `04_model.ipynb`. Notebook 06's attached excerpt only describes fail-closed behavior and does not provide a training-data or model hash link.

## Conclusion

The candidate lineage is plausible and partially supported by saved code and execution outputs. Exact historical Feature Master identity and a hash-verified Master → training dataset → frozen-model chain are not established. The model-to-archive lineage remains unknown.
