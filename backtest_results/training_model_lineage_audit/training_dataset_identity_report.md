# Training Dataset Identity Report

## Finding

No separately serialized training dataset, final modeling table, or training-data hash was located in the inspected repository artifacts. Notebook 04 constructs the modeling rows in memory; its saved outputs report counts and date ranges but do not preserve a row-level dataset artifact. Therefore the exact historical training dataset is **not identified**.

## Candidate dataset described by saved Notebook 04

Notebook `04_model.ipynb`:

1. Cell 3 (execution count 3) reads `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet`.
2. Cell 29 (execution count 26) loads `dataset/SET50_constituents_by_halfyear_2016_2026.csv` and filters rows to effective-period members.
3. Cell 31 (execution count 28) forms `model_df` from `Date`, `Target_Date`, `Period`, `Symbol`, the six model features, and `target_aligned`.
4. Cell 37 (execution count 34) removes rows with a missing target or any missing feature.
5. Cell 39 (execution count 36) splits by `Target_Date` year.

| Candidate stage | Saved notebook dimensions / characteristics | Saved output evidence |
|---|---|---|
| Candidate `model_df` | 119,224 rows × 11 columns; six features plus target and date/period/symbol identifiers. | Cell 31, exec 28 |
| Complete-case `final_model_df` | 116,465 rows × 11 columns; zero remaining missing values. Class counts: 0 = 5,044; 1 = 6,183; 2 = 105,238. | Cell 37, exec 34 |
| Feature-date / target-date span | Feature dates 2016-03-28–2026-11-12; target dates 2016-03-29–2026-11-13. | Cell 38, exec 35 |
| 2016–2024 training split | 94,205 rows; feature dates 2016-03-28–2024-12-27; target dates 2016-03-29–2024-12-30. Class counts: 0 = 4,114; 1 = 4,877; 2 = 85,214. | Cell 39, exec 36 |
| 2025 validation split | 11,824 rows; target dates 2025-01-02–2025-12-30. | Cell 39, exec 36 |
| 2026 test split | 10,436 rows; target dates 2026-01-05–2026-11-13. | Cell 39, exec 36 |

Before complete-case filtering, the saved output reports 108 missing targets, 2,709 rows with at least one missing feature, and 58 rows missing both. These rows were excluded in that notebook state; this is not evidence that every training run used the same data bytes or row selection.

The 94,205 training count matches the model metadata's `training_samples`. This is a consistency check, not a cryptographic link.

## Existing Master candidates

All three Master artifacts in the `verified_build_20261113_152948` build have 198,532 rows, 17 columns, 83 symbols, and date span 2016-01-04–2026-11-13:

| Candidate | SHA-256 | Bytes |
|---|---|---:|
| `dataset/verified_build_20261113_152948/SET50_Master_Dataset.parquet` | `ef060baedd779a99b83a7cfa74b4bde20eb7bcf30fc1c05679f11b3c8c459f07` | 15,332,229 |
| `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted.parquet` | `1ceef21d118c480ffe356e9604e9b2452dd20c5ba91537c40ef5a3e639c9d848` | 15,595,564 |
| `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet` | `7424f01e92d4f507b2a5956898e1ef30050de7a50c7c4ee9a9aa402af4271505` | 15,595,544 |

An earlier base Master also exists at `dataset/verified_build_20261113_144731/SET50_Master_Dataset.parquet` (198,532 rows, 17 columns; SHA-256 `f31177247af1bb1d11072316539041a6bf5681011f2c137309abffcff7f57746`). The saved Notebook 04 code names the VolZ_Fixed path, but no execution-time input hash identifies the precise bytes it read.

## Identity classification

The in-memory candidate training table is characterized by notebook outputs but has no file path, file size, or SHA-256. No other candidate file is promoted to the historical Training Dataset.

**Training dataset identity:** `PARTIALLY_VERIFIED` as a saved-notebook candidate process and summary; exact historical training dataset identity `UNKNOWN_INSUFFICIENT_EVIDENCE`.
