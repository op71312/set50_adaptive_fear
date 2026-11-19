# Phase D — Feature Contamination and Frozen Model Consistency

## BANPU

The pinned Master contains 147 BANPU feature-date rows in 2026.
Notebook 03 calculates `VolRank` and `LiquidityRank` cross-sectionally within the SET50
period. The member-only market proxy is leave-one-out for each member, and each
`Corr_60d` uses `rolling(window=60, min_periods=60).corr(...)` on observed feature dates.
Thus BANPU can affect other members' same-date VolRank/LiquidityRank and their rolling
CorrRank inputs while its return is present. `daily_return`, `momentum_20d`, and `vol_z`
are per-symbol calculations and have no direct cross-symbol effect.

The Phase C washout code takes `feature_calendar[max(0, date_position - 59):date_position + 1]`:
at most 60 global observed feature dates, inclusive of the predictor date. It requires
exactly 60 observations and no BANPU row anywhere in that slice. Phase D records this
test for 210 observed 2026 dates; BANPU is in
206 of those current/trailing windows.

Recomputed against the pinned Master using the source rank definitions:

| Period | BANPU rows | Other VolRank rows changed if removed | Max absolute change | Other LiquidityRank rows changed if removed | Max absolute change |
|---|---:|---:|---:|---:|---:|
| 2026_H1 | 118 | 5666 | 2.000000 | 5664 | 1.959184 |
| 2026_H2 | 29 | 1398 | 2.000000 | 1392 | 1.959184 |

The baseline rank calculations reproduce the stored rank values for all observed
2026 member rows in these periods. These counterfactual ranks are diagnostics only;
they were not written into the Master or used to refit the model.

For the four Phase C AOT predictor dates (2026-11-09 through 2026-11-12), the 60
observed-date windows start 2026-08-13, 2026-08-14, 2026-08-17, and 2026-08-18,
respectively, and contain no BANPU feature row. The last BANPU feature row before the
execution-gap interval is 2026-08-11. A separate 2026-11-13 BANPU row is later than
all four predictor dates and is not used as future information; it would restart the
proxy/rolling window for later predictors. The Phase C candidate
flags and the pinned Master date sequence both show zero BANPU observations in those
four windows. Therefore, the AOT candidate-date VolRank/LiquidityRank and the 60-date
CorrRank inputs are unaffected by removing BANPU on those dates.

Exclusion-aware recalculation over 2026 would change many same-date ranks, so the
inference inputs would no longer use the same member population as the frozen model's
original training transformation. The actual training feature distribution, frozen
model, and stored features remain unchanged; the bounded AOT sample uses the original
values. This does not resolve historical 2017_H1 membership uncertainty.

## GLOBAL

The diagnostic contains 141 GLOBAL field-rows across
36 dates. GLOBAL is not a member of either 2026
SET50 period. Notebook 03 builds the shared rank/proxy inputs from effective-period
SET50 members; the execution-snapshot anomaly therefore does not enter other 2026
symbols' shared model features. The diagnostic's split-basis candidate and tick
alignment do not prove a corporate action. `Official_Action_Confirmed` remains false;
no split basis is asserted and no adjusted value is applied.

## Frozen model and limits

No features were overwritten and no model was retrained. The rank counterfactual
demonstrates inference consistency risk if BANPU were removed from the feature
population outside the four-date washout. The report does not treat the feature data
as officially sourced execution data or infer corporate-action terms.
