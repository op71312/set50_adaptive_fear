# Frozen Model Identity Report

## Current serialized artifact

| Property | Finding |
|---|---|
| Path | `models/Original_Softmax_Final/final_softmax_model.joblib` |
| Format | Joblib-serialized scikit-learn Pipeline, as specified by Notebook 04's `joblib.dump` call |
| Size | 1,969 bytes |
| Current SHA-256 | `8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7` |
| Sidecar metadata | `models/Original_Softmax_Final/final_softmax_metadata.json`, 986 bytes, SHA-256 `d26da9d09b94ab50dbb803bf33d2670b93aff2c8dbaf14fdb264eac89a1852be` |
| Test report | `models/Original_Softmax_Final/final_test_2026.json`, 919 bytes, SHA-256 `2384c92df4635cbaebbca9d8097651ec05595255ba691da3ab8852ecba16ec2c` |
| Metadata creation field | `2026-11-15T09:34:35.479083` |
| Model/run/commit identifier | No model version, run ID, commit ID, or training-data hash is recorded in the metadata. |

The hash verifies the identity of the **current local file only**. It does not show that the archived prediction job used this file.
The serialized joblib object was not deserialized during this read-only audit; no claim is made about additional metadata embedded inside the binary beyond the estimator structure recorded in the saved Notebook 04 output.

## Estimator and preprocessing evidence

Notebook `04_model.ipynb` saved outputs for cells 82–84 (execution counts 99–101) describe and export:

- Pipeline: `StandardScaler()` followed by `LogisticRegression`.
- Logistic Regression: solver `saga`, `max_iter=5000`, `random_state=42`.
- Selected parameters: `C=10`, `class_weight={0: 10, 1: 10, 2: 1}`, `l1_ratio=0`.
- Metadata describes the algorithm as Multinomial Logistic Regression. The notebook output does not record an explicit `multi_class` setting or the scikit-learn version.
- Hyperparameter search: 75 combinations, five time-series folds, refit on macro-F1; saved cell 53 output (execution count 47) records these best parameters and mean CV macro-F1 `0.3936269750915103`.
- Prediction rule: `Argmax`.
- Feature order: `daily_return`, `momentum_20d`, `vol_z`, `VolRank`, `CorrRank`, `LiquidityRank`.
- Class mapping/order: `0 = Panic`, `1 = FOMO`, `2 = Normal`.

The metadata records 94,205 training samples, 11,824 validation samples, 10,436 test samples; periods 2016–2024, 2025, and 2026 respectively. These values match the saved Notebook 04 split output. The metadata and notebook do not record a training-data hash.

## Link to archived predictions

The archived `daily_predictions_audit.csv` contains fields `Date`, `Symbol`, `Predicted_Class`, `P_Panic`, `P_FOMO`, `P_Normal`, `Strategy`, and `Allocation`. It contains no model hash, model version, feature input hash, training dataset ID, or prediction-run ID.

Its 10,387 predictions per strategy/allocation pair differ from the metadata's 10,436 test samples by 49 rows. Structural date/symbol coverage does not identify a model. No verifiable hash or direct run reference links this current model file to the archived predictions.

**Classification:** current model file `HASH_VERIFIED`; current notebook export path `CONSUMPTION_CONFIRMED` for that saved notebook state, but exact serialized bytes at that time are not pinned; archived-model identity `UNKNOWN_INSUFFICIENT_EVIDENCE`.

No model was loaded, fit, or otherwise executed during this audit.
