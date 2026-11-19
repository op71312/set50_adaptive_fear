# Training Model Lineage Validation Report

## Result

The read-only evidence review is complete, but key historical links remain unresolved. The audit is therefore `COMPLETED / BLOCKED`, not a readiness approval.

| # | Validation requirement | Result | Evidence / limitation |
|---:|---|---|---|
| 1 | Verify known reference artifact existence | `PASS_WITH_LIMITATIONS` | Model, metadata, test report, three current-build Masters, GLOBAL staged source, membership inputs, archived prediction CSV, archive manifest, and notebooks 03/04/05/06 exist. The named `04_model_training.ipynb` does not; the available relevant notebook is `04_model.ipynb`. |
| 2 | Recalculate current model and Master hashes | `PASS` | Frozen model SHA-256 `8ec9433b…6a048c7`; metadata `d26da9d0…1852be`; fixed Master `7424f01e…271505`; Global source `1dcef0bf…6c40bf1`. Full hashes are recorded in the reports and input inspection. |
| 3 | Verify protected source integrity | `PASS` | Compared SHA-256 for 542 pre-existing files under dataset, models, backtest results, and notebooks 03–06 before/after output creation; 0 mismatches and 0 missing files. New audit outputs are excluded from the protected-input comparison. |
| 4 | Give supporting evidence for every claimed relationship | `PASS_WITH_LIMITATIONS` | The 13-row lineage matrix has an evidence reference for each row and records classifications and unresolved gaps. Some references establish only saved-notebook path-level consumption, not the historical input bytes. |
| 5 | Avoid model identification by filename alone | `PASS` | Current model file identity is established by SHA-256. Its use by the archived prediction run remains explicitly unknown because no archive hash/run reference exists. |
| 6 | Avoid training-dataset identification by current path alone | `PASS` | The in-memory candidate is described from saved execution output, but not promoted to an exact historical dataset. No serialized training table/hash was located. |
| 7 | Separate GLOBAL direct and indirect exposure | `PASS` | Direct candidate member rows (1,942 feature-complete rows in 2016–2024) are distinguished from the leave-one-out market proxy and cross-sectional rank pathway. Actual training/model exposure remains unknown. |
| 8 | Assess historical membership independently | `PASS` | 2017_H1 has 49 unique listed names, 43 represented in the fixed Master, and 720 missing member-date slots across 120 dates; actual archived model exposure remains unknown. |
| 9 | Do not conflate model identity and prediction identity | `PASS` | Current model hash and archive prediction structure are reported separately. Archive has no model hash/run ID; 10,387 rows per pair differs from metadata `test_samples=10,436`. |
| 10 | Keep unsupported links explicitly unknown | `PASS` | Exact training dataset, historical Master bytes, frozen-model-to-archive identity, and GLOBAL/membership exposure in the exact model training set remain unknown. |
| 11 | No external download/provider calls | `PASS` | No network or provider calls were made; no market data was downloaded and no yfinance call was executed. |
| 12 | No training, prediction, allocation, or backtest execution | `PASS` | No model was loaded or trained, no predictions or weights were generated, and no backtest or portfolio allocation was run. Existing notebook outputs were read statically. |
| 13 | All nine deliverables exist and are internally consistent | `PASS_WITH_LIMITATIONS` | Final directory inventory contains the eight requested reports/matrix plus the SHA-256 manifest. Internal consistency checks cover schemas, evidence statuses, key counts, and documented limitations only; they do not prove historical validity. |
| 14 | New output hashes match final manifest | `PASS` | The manifest records SHA-256 and byte size for all eight other deliverables; the manifest self-hash is intentionally omitted. Hashes were independently recalculated after writing. |

## Key input hash verification

| Input | SHA-256 |
|---|---|
| `models/Original_Softmax_Final/final_softmax_model.joblib` | `8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7` |
| `models/Original_Softmax_Final/final_softmax_metadata.json` | `d26da9d09b94ab50dbb803bf33d2670b93aff2c8dbaf14fdb264eac89a1852be` |
| `dataset/verified_build_20261113_152948/SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet` | `7424f01e92d4f507b2a5956898e1ef30050de7a50c7c4ee9a9aa402af4271505` |
| `dataset/verified_build_20261113_152948/source_ohlcv/GLOBAL.BK.parquet` | `1dcef0bf67eca52f1f84237838a64e3075fd235277d6d2238aa6c8cfc6b40bf1` |
| `dataset/SET50_constituents_by_halfyear_2016_2026.csv` | `17002a2e63259c8144589df02bcfa9c82be1ba6285e5e142e63281779b23ddac` |
| `backtest_results/superseded_20261115_pre_integrity_fixes/daily_predictions_audit.csv` | `6f8ee45ffeba1325e715c7a30c5bab3fcab1e54c321bbde91fff39702e28d657` |

## Scope and gate

This report establishes artifact observations and evidence gaps only. It does not establish historical market validity, model suitability, or portfolio readiness. Existing model, data, notebook, archive, and gate artifacts were not modified.

`TRAINING_MODEL_LINEAGE_AUDIT = COMPLETED / BLOCKED`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
