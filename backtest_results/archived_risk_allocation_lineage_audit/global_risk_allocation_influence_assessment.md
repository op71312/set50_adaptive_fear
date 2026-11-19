# GLOBAL Risk and Allocation Influence Assessment

## Findings by exposure type

| Exposure type | Finding | Evidence classification |
|---|---|---|
| Direct holding exposure | No GLOBAL rows appear in the archived predictions, transaction symbols, or valuation symbols. | `HASH_VERIFIED` archive artifacts; no direct rows observed |
| Direct risk-input exposure | Unknown; no archived Buy/risk universe, return panel, covariance/correlation matrix, CVaR scenarios, or input hash. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Indirect historical feature exposure | A prior read-only feature lineage audit confirmed a GLOBAL pathway into historical member-period market proxies and cross-sectional ranks while it was a constituent. | `DERIVATION_CONFIRMED` for pathway only |
| Indirect allocation influence | Unknown; no link from any GLOBAL-containing risk input to archived weights or solver outputs. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Portfolio performance impact | Not evaluated; no counterfactual calculation was performed. | Not assessed |

## What the archive establishes

The archived package contains zero GLOBAL rows in `daily_predictions_audit.csv`, `transactions.csv`, and `portfolio_valuation_audit.csv`. This rules out a recorded direct GLOBAL holding in the inspected result tables. It does not show whether historical GLOBAL returns appeared in a market-wide feature, Buy candidates, return panel, covariance matrix, correlation matrix, HRP cluster, MPT expected-return vector, or CVaR scenario matrix.

## Indirect historical pathway

The read-only Workstream 1.3 report [`global_training_exposure_assessment.md`](../training_model_lineage_audit/global_training_exposure_assessment.md), section “Indirect cross-sectional pathway,” records Notebook 03 cell 32's member-period return proxy and rank mechanisms; it classifies the feature-generation pathway as `DERIVATION_CONFIRMED`. The archived lineage report [`global_indirect_influence_assessment.md`](../archived_backtest_lineage_audit/global_indirect_influence_assessment.md), rows “Historical feature ranks / market proxy” and “Risk return matrix, volatility, covariance/correlation,” separately distinguishes that feature pathway from the unknown archived risk-input lineage.

These reports establish that a candidate feature-generation pathway existed while GLOBAL was a historical member and that the periods overlap the model training years. They do not establish that the exact feature Master or model was used in the archived run. The Workstream 1.3 assessment also says the serialized training table/hash was not found and actual GLOBAL inclusion in that exact model's training is unknown.

An indirect **risk** pathway would require GLOBAL to have been included in the historical risk estimation universe or in a relevant derived risk input. Neither that universe nor any risk matrix is present in the archive. No indirect allocation influence can therefore be confirmed.

## Limitations

- Archive manifest says adjusted Master OHLC was used for execution, but does not name/hash that file and does not identify risk inputs.
- No archived raw/final weights or risk-data cutoff/hash is available.
- The current Notebook 05 allocator functions and current Notebook 06 gate harness are not linked to the archived run.
- No counterfactual risk matrices, weights, predictions, or returns were calculated.

`GLOBAL_RISK_EXPOSURE = UNKNOWN`  
`GLOBAL_ALLOCATION_INFLUENCE = UNKNOWN`
