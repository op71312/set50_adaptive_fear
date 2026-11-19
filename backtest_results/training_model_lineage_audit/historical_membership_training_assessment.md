# Historical Membership Training Assessment

## Membership source identity

The current candidate input is `dataset/SET50_constituents_by_halfyear_2016_2026.csv`, SHA-256 `17002a2e63259c8144589df02bcfa9c82be1ba6285e5e142e63281779b23ddac`. The paired declaration-date file is `dataset/set50_declare_dates_2016_2026.csv`, SHA-256 `533624ed430850eb0e5c536ac9a5c949fe12342bf6ef2267df716f1a5488956f`.

Notebook 03 cell 32 and Notebook 04 cell 29 reference these paths. No execution-time membership hash is recorded, so the exact historical bytes used by the saved notebook or frozen model are not established.

## 2017_H1 coverage issue

Read-only comparison of the current membership file and fixed Master found:

- 2017_H1 has 49 listed slots and 49 unique names (not 50).
- The period has 120 Master dates.
- 43 of the 49 listed names have rows in the fixed Master for that period.
- Six listed symbols are absent: `DTAC`, `GLOW`, `INTUCH`, `ROBINS`, `SCB`, and `TMB`.
- Expected member-date slots: 49 × 120 = 5,880.
- Observed member-date rows: 5,160.
- Missing member-date slots: 720.

The saved Notebook 04 membership/modeling output reports 5,160 member rows for 2017_H1, consistent with the current Master coverage. Notebook 03's saved quality output reports only 44 available files for that period, showing that file availability and actual period row coverage are not identical measures.

## Potential feature effect

Notebook 03 ranks available member feature values over the effective-period member list; absent source rows cannot contribute a value and leave a smaller observed cross-section. Its market proxy uses member returns and daily available counts, with leave-one-out logic for member series. Missing members can therefore affect the realized sample used by ranks/proxies. No missing member was filled, and no feature was rebuilt in this audit.

## Training exposure classification

The saved Notebook 04 candidate path filters Master rows using the same membership file path and contains the 2017_H1 5,160-row result. This supports candidate-path consumption of the issue. Because the historical membership input hash, exact serialized training data, and model-to-archive identity are not pinned, actual inclusion of this membership issue in the archived model's training process remains **unknown**.

`HISTORICAL_MEMBERSHIP_EXPOSURE = UNKNOWN`
