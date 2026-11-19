# GLOBAL Training Exposure Assessment

## Conclusions by stage

| Stage | Finding | Classification |
|---|---|---|
| Feature-generation pathway | Confirmed in the inspected Notebook 03 code: GLOBAL returns can enter member-period market proxies and GLOBAL's feature values can participate in member-period cross-sectional ranks while it is a constituent. | `DERIVATION_CONFIRMED` for pathway |
| Candidate Master rows | Current fixed Master contains 1,942 GLOBAL rows in active membership periods within 2016–2024; all six model feature columns are populated on those rows. This count is a read-only structural query, not a recreated training set. | `HASH_VERIFIED` artifact plus `CANDIDATE_ONLY` eligibility |
| Exact serialized training dataset | No serialized training table/hash was found. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| GLOBAL rows in actual frozen-model training | Not established; candidate path is present, but exact dataset/model input hashes are absent. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Downstream influence on archived predictions | Possible through historical features if the candidate chain was used; archive contains no model/data hashes. No magnitude or causal effect is established. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Performance impact | Not evaluated; counterfactual features, predictions, and portfolio results were prohibited. | Not assessed |

## Direct row exposure

The current membership file lists GLOBAL as a SET50 member from 2017_H1 through 2025_H1. The current fixed Master contains 1,942 GLOBAL member-date rows during 2017_H1–2024_H2 with all six model features non-missing. Notebook 04 filters to effective-period members and then removes missing target/feature rows. The saved notebook output does not break final training rows down by symbol. Thus GLOBAL rows were available to the candidate process, but actual inclusion in the exact model training dataset is not confirmed.

The prediction universe in the archived 2026 CSV has no GLOBAL rows (0 in the `Symbol` field). That fact only addresses direct 2026 prediction rows; it does not rule out historical training or indirect feature influence.

## Indirect cross-sectional pathway

Notebook 03 cell 32 (saved execution count 52) provides these mechanisms:

- `market_proxy` is calculated from each effective period's member returns.
- For a member's proxy, the code uses leave-one-out returns. When GLOBAL is an active member, its return can therefore enter the proxy used for other members' rolling `Corr_60d`/`CorrRank` values.
- `VolRank`, `CorrRank`, and `LiquidityRank` are calculated across period members. GLOBAL's valid rank-source values can affect the percentile positions of other member securities.
- `daily_return`, `momentum_20d`, and `vol_z` are per-security features; GLOBAL's own observations can appear in its candidate rows if complete.

This confirms a code-level feature pathway in the saved feature build. It does not establish that the exact Master was consumed by the exact historical training process, nor that the archive's model artifact was produced from it.

## No counterfactual claim

No feature values were recomputed or perturbed; no ranks, predictions, weights, or backtests were generated. No quantitative performance or prediction impact is claimed.

`GLOBAL_MODEL_EXPOSURE = UNKNOWN`
