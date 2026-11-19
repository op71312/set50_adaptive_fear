# Training Dataset & Frozen Model Lineage Audit

## Executive summary

The repository contains a frozen Softmax model candidate and a saved model-training notebook state, but no serialized training dataset or cryptographic run manifest that connects the model to its exact Feature Master, membership inputs, or the archived 63-combination predictions. The saved Notebook 04 cells document a plausible training path; that is not sufficient to assert the archived backtest used the currently present model or the exact bytes of the current datasets.

The strongest supported conclusions are:

- The local model artifact is identified by its current path and SHA-256. Its identity as the archived run's model is **unknown**.
- Notebook `04_model.ipynb` saved execution outputs describe an in-memory complete-case modeling dataset of 116,465 rows and a 94,205-row 2016–2024 training split. No corresponding serialized training dataset was located; the exact dataset hash is unavailable.
- The saved Notebook 04 state reads the VolZ_Fixed Master path and the half-year membership CSV. The saved code/output supports consumption of those paths in that notebook state, but the input hashes at execution time are absent.
- GLOBAL's historical feature pathway is confirmed in the inspected Notebook 03 code: while it is a member, its return can enter other members' leave-one-out market proxies and its values can affect cross-sectional ranks. The current Master has 1,942 GLOBAL member rows in the stated 2016–2024 training years with all six feature fields populated. Whether those rows or affected peer features entered the exact training data used by the frozen model is **unknown**.
- The current membership file has 49 names for 2017_H1. The current fixed Master contains 5,160 member-date rows across 120 dates; six listed members are absent, leaving 720 missing member-date slots. Saved Notebook 04 outputs show the same 5,160 member rows in its candidate modeling path. This establishes a candidate-path exposure, not a hash-pinned link to the archived model.
- The archive prediction CSV has 10,387 rows per strategy/allocation pair (63 pairs), whereas the model metadata reports 10,436 test samples. The archive has no model hash, feature hash, or run ID; this difference is unexplained and prevents direct linkage.

## Decision table

| Question | Finding | Evidence classification |
|---|---|---|
| Exact local frozen model artifact identified? | Yes, as a current artifact by path and SHA-256. | `HASH_VERIFIED` |
| Is that artifact verified as the archived model? | No; archive rows and manifest contain no model hash or run ID. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Exact training dataset file identified? | No; the saved notebook describes an in-memory dataset, but no serialized training dataset/hash was found. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Candidate feature/master path identified? | The saved Notebook 04 state reads the VolZ_Fixed Master path; execution-time bytes are not pinned. | `CONSUMPTION_CONFIRMED` at path level; content hash at run time unknown |
| GLOBAL direct/indirect pathway in candidate data? | Candidate Master has GLOBAL member rows and the feature code has cross-sectional pathways. | `DERIVATION_CONFIRMED` for pathway; actual model exposure unknown |
| 2017_H1 membership gap in candidate path? | Yes: 49 members, 43 represented, 720 member-date slots absent in current candidate Master / saved Notebook 04 state. | `CONSUMPTION_CONFIRMED` at path/state level; archived-model exposure unknown |
| Archived prediction linkage? | No direct model, training-data, or feature-input identity reference. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |

## Audit outcome

The audit is **completed but blocked at the historical lineage stop conditions**. Do not repair, rebuild, retrain, or rerun anything as part of this workstream. Recovering a run manifest, serialized training data, historical input hashes, and prediction-job provenance would be required to resolve the unknown links.

`TRAINING_MODEL_LINEAGE_AUDIT = COMPLETED / BLOCKED`  
`FROZEN_MODEL_IDENTITY = PARTIALLY_VERIFIED`  
`TRAINING_DATASET_IDENTITY = PARTIALLY_VERIFIED`  
`GLOBAL_MODEL_EXPOSURE = UNKNOWN`  
`HISTORICAL_MEMBERSHIP_EXPOSURE = UNKNOWN`  
`ARCHIVED_PREDICTION_LINEAGE = UNKNOWN`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
