# E3 — Risk Estimation Policy

## Approved inputs and implementation context

Preserve the existing windows: 60 trading observations for IV, ERC, HRP, MinVar, and
MPT; 252 for CVaR, with 95% confidence. Do not annualize daily decimal inputs or change
these windows silently.

The local code is not itself the approved policy: `05_backtest.ipynb` has 50/200 minimum
history constants and a Ledoit-Wolf implementation, while `06_research_backtest.ipynb`
requires full 60/252 windows and leaves `COVARIANCE_ESTIMATOR` and
`ALLOCATOR_FALLBACK_POLICY` unset. Phase D's risk-estimation status predates this
researcher decision. The specification is now approved; that approval does not certify
historical data or change either notebook.

## Approved covariance estimator

Use centered sample covariance:

`S = (X - mean(X))' (X - mean(X)) / (T - 1)`

The same common complete return matrix supplies sample covariance and correlation. Do
not use Ledoit-Wolf shrinkage unless a new researcher decision explicitly changes this
approved estimator. Centered sample covariance may be singular or sensitive to outliers;
validate the matrix and fail the method rather than silently regularizing, clipping, or
changing estimators.

## Missing observations and date alignment

For each allocation calculation, fix the complete eligible Buy-symbol set and one
point-in-time cutoff (dates strictly before the decision date). Select the **same date
set for every security in that complete universe**: a date is retained only when a valid
finite return exists for every eligible Buy security on that date and the session/date
is validated. Sort the common dates once and use that identical ordered panel and cutoff
for all securities in that calculation. Different methods may request different approved
window lengths, but must use the same common-universe and cutoff rules.

This filters dates only; it must not remove any security from the allocator's universe
to make risk inputs complete. If one eligible Buy security has missing history, the
common sample shrinks for all securities. If the complete unchanged universe cannot supply the full method window below, return
`UNAVAILABLE` with reason `INSUFFICIENT_HISTORY` and retain cash. No partial-window or
other fallback is permitted.

Do not replace missing values or returns with zero, forward-fill, use pairwise covariance,
or silently remove a security from a method-specific sample.

- Pairwise available covariance uses different observations per pair; the resulting
  matrix can fail positive-semidefinite checks and makes method comparisons sample-
  incomparable.
- A common complete matrix gives every pair the same observations and a PSD centered
  sample covariance up to numerical precision, but can shrink history or leave too few
  rows.
- Count rows only on an evidence-backed session calendar. No official 2026 calendar is
  present, so the existing vendor-observed dates do not certify a historical session
  count.

For decisions after close on `t`, use one shared risk-data cutoff across all methods.
The existing engine's `get_complete_history` uses dates strictly before `t`; retain that
no-lookahead cutoff unless explicitly approved otherwise. Do not use execution-date
Open/Close values in risk inputs.

## Full-window requirement and risk-data provenance

Use the full approved window, with no partial-window minimum or partial-window fallback:

| Methods | Required common observations | Calculation if fewer are available |
|---|---:|---|
| EW | None | EW does not consume historical risk data. |
| IV | 60 common complete observations | `UNAVAILABLE` / `INSUFFICIENT_HISTORY`; retain cash. |
| ERC, HRP, MinVar, MPT | 60 common complete observations | `UNAVAILABLE` / `INSUFFICIENT_HISTORY`; retain cash. |
| CVaR | 252 common complete observations | `UNAVAILABLE` / `INSUFFICIENT_HISTORY`; retain cash. |

The legacy Notebook 05 thresholds of 50/200 are implementation facts only and are not
carried forward. For every risk calculation, record `Risk_Data_Cutoff`,
`Risk_Data_Hash`, exact ordered `Eligible_Buy_Symbols`, the exact ordered common dates,
calendar identifier and verification state, `Requested_Window`,
`Common_Observation_Count`, `Window_Status`, first/last return dates, dropped-date count
and reasons, return-price basis, and estimator name/version where applicable. Hash the
exact ordered input panel (dates, symbols, values, and schema) deterministically; the
hash is lineage evidence, not proof that the input data are valid.

## Input and covariance validation

Before any method consumes risk data:

1. Require unique `(Date, Symbol)` input rows, one price basis, valid identity, verified
   session alignment, and finite decimal returns.
2. Verify exact equality between the eligible Buy-symbol set and the risk matrix columns.
   Never remove a symbol to accommodate missing risk inputs.
3. Use the identical ordered common-date set for all securities in each calculation at
   the shared cutoff; require 60 observations for IV/ERC/HRP/MinVar/MPT and 252 for CVaR.
   IV estimates each symbol's standard deviation from that full common return panel;
   CVaR consumes its 252 empirical return scenarios and does not require covariance.
   Missing observations do not trigger zero fill, forward fill, pairwise estimation,
   security removal, or a partial-window fallback.
4. For sample covariance, center each column and calculate
   `S = (X - mean(X))' (X - mean(X)) / (T - 1)`. Check output for finite entries,
   symmetry within recorded tolerance, positive diagonal variances, and
   eigenvalue/conditioning diagnostics.
5. Reject materially non-PSD, singular, ill-conditioned, or non-finite matrices; do not
   silently clip eigenvalues, add jitter, remove a security, or replace covariance.
6. After optimization, verify solver success, objective finiteness, constraints, bounds,
   cap, and normalization/cash invariants. Record solver name/version, status, iterations,
   tolerance, and residuals.
7. Treat non-positive volatility or zero portfolio variance as invalid for a method that
   requires it. Do not divide by zero or substitute a uniform allocation.

Numerical tolerances and any regularization beyond the named estimator require a
reproducible implementation and approval.

## Approved failure and cash-retention states — no automatic method substitution

| Condition | Recommended result | Prohibited behavior |
|---|---|---|
| No eligible Buy securities | `NO_ELIGIBLE_BUYS`; no allocation rows. | Calling an allocator or creating a synthetic position. |
| Zero deployable cash | `NO_DEPLOYABLE_CASH`; retain cash. | Emitting nonzero budgets. |
| Missing/invalid input or insufficient history | `ALLOCATION_UNAVAILABLE` with reason; retain the affected allocation as cash. | Zero-filling, dropping only the problematic name, or switching to EW. |
| Invalid volatility/covariance | Reject the method decision; report diagnostics. | Replacing zero volatility or repairing the matrix silently. |
| Optimizer non-convergence / infeasibility | `SOLVER_FAILED` or `INFEASIBLE`; no method weights. | Using last iterate, unconstrained weights, EW, or another method automatically. |
| All selected methods unavailable | No Buy orders; cash remains; research result is blocked. | Choosing an alternative allocator or treating the cash outcome as successful allocation. |

This failure and cash-retention policy is approved. Notebook 05 contains automatic EW
fallbacks for several risk methods; those prototype fallbacks are not permitted.
Unsupported methods or failed allocations remain unavailable and do not place Buy orders.

**Policy status: APPROVED. Historical risk readiness: BLOCKED.** The full common windows,
centered sample covariance, and fail-closed behavior are approved. Valid official session
evidence, sufficient common history, and the independent portfolio gate are still
required before historical use.
