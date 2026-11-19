# Historical Artifact Limitations

## Status

`ARCHIVED_RESULTS = EXIST / SUPERSEDED / NOT_VALIDATED`  
`ARCHIVED_RISK_ALLOCATION_LINEAGE = BLOCKED`  
`ARCHIVED_PERFORMANCE_TRUST = NOT_VALIDATED`

This document describes retained artifacts and evidentiary limits. It does not rerun,
repair, reproduce, or recalculate any historical result.

## Existing archive is not a new run

The superseded archive contains 63 strategy/allocation labels (nine strategies by seven
method names), 13,167 daily rows, 654,381 prediction rows, 3,125 transaction rows, and
67,633 valuation rows. The archive is an existing historical artifact. The current
backtest status and saved Notebook 05/06 states report no new 63-combination results in
the reviewed readiness workstreams. Do not state that no historical output ever
existed.

The archive manifest identifies “adjusted Master OHLC” as execution prices but provides
no exact file path/hash, run ID, source-code hash, or complete input manifest. Multiple
Master variants exist and have distinct file hashes. The archive cannot be linked or
definitively unlinked to the later GLOBAL-adjusted execution candidate from filenames,
timestamps, or absence of GLOBAL output rows.

## Prediction and model lineage

- The current frozen model file is identified locally by SHA-256
  `8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7`; its metadata
  SHA-256 is `d26da9d09b94ab50dbb803bf33d2670b93aff2c8dbaf14fdb264eac89a1852be`.
- The metadata records 94,205 training, 11,824 validation, and 10,436 test samples.
  The archive has 10,387 prediction rows per pair, a 49-row difference from metadata
  test samples. The mismatch is unexplained.
- No serialized training dataset hash or complete execution-time manifest binds the
  model, feature Master, membership inputs, prediction rows, and archive.
- GLOBAL's historical cross-sectional feature pathway is confirmed in the inspected
  feature code, but its inclusion in the exact model training set and its archived
  risk/allocation influence remain unknown.
- Phase D documents potential BANPU cross-sectional effects; the four AOT candidate
  dates are bounded clear of BANPU within the recorded 60-observation windows. This
  does not validate all historical training or feature inputs.

## Archived Buy Universe, risk, and allocation

The archive does not retain a date-level Buy set, allocator input universe, risk panel,
covariance/correlation matrix, CVaR scenarios, estimation cutoff, source hash, raw or
final weights, solver status, objective, iterations, residuals, or cap redistribution
audit. No traceable chain connects predictions to actions, Buy Universe, risk inputs,
weights, orders, and valuation. Current Notebook 05/06 behavior is not attributed to
the historical run.

The archive's row alignment across 63 labels and 209 dates is structural evidence only.
It does not prove correct method definitions, risk estimation, orders, prices, or
comparability. No missing allocation values or Buy sets were reconstructed.

## Archived valuation and performance

- The archive contains 378 stale valuation rows across six pairs, all BANPU, with a
  maximum recorded age of 93 **calendar days**. Those marks flow into retained position
  and portfolio value fields. This is not a verified exchange-session count.
- The archived output has no approved `PORTFOLIO_VALUE_VALID/STALE/UNAVAILABLE` lineage,
  no date-level missing-valuation audit, and no full run-linked stale policy.
- The archive manifest expressly notes that Total Return and CAGR omitted the
  initial-equity baseline. The denominator, first return, and archived formulas for
  CAGR, Sharpe, Sortino, Maximum Drawdown, and Calmar are not linked to the output.
- Stored equity identities reconcile structurally, but the source price and return
  methodology are not thereby validated.
- All 3,125 transactions record `Cost/Gross = 0.0026799`; fee and slippage are not
  separate, fill-price basis is unknown, and per-fill cash application is not
  established. This numeric ratio does not prove historical rate decomposition.
- Twenty-eight pairs are all-cash in retained daily rows; their $1,000,000 cash does not
  establish the active pairs' starting-equity denominator. Several metric fields are
  blank for no-trade pairs.

Accordingly, do not use archived metrics as validated research results, rank strategies
from them, or report a complete-period metric as if the equity series were complete.
Do not calculate substitute returns, equity curves, drawdowns, or counterfactual results
from the archive in this consolidation.

## Price and corporate-action lineage

All 141 corporate-action ledger entries remain unresolved at the primary-source/impact
level; no action was applied. Counts of vendor/claim rows differ between reports because
the source definitions differ; retain the reconciliation gap. The 97 union overlaps,
89 active recorded-date overlaps, and 8 outside active membership are potential scope
counts, not proof of effects.

The pre-existing GLOBAL candidate transformation is not official verification. The
archived output has no hash linking it to that candidate. No split is inferred, and no
historical price or ledger was changed in this consolidation.

## Applicable Phase E boundary

Approved Phase E policies are prospective specifications, not retroactive proof of
archive behavior. The approved three-verified-session stale threshold cannot be mapped
to the archive's calendar-day ages without an official session calendar. The approved
common complete windows, centered sample covariance, fixed-q_max MinVar/CVaR, solver
settings, fee sequence, and fail-closed behavior do not establish that the archived run
used them.

`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
