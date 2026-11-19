# E4 — Allocation Method Specifications

## Common contract

Each method receives the same point-in-time eligible Buy-symbol set, deployable cash,
decision date, and validated risk inputs as applicable. It returns incremental cash
weights only; it does not size shares or use future execution prices. All weights pass
through the 25% per-security cap. Iteratively capped excess is redistributed over
remaining eligible securities; any unallocatable amount remains cash.

For `N` Buy symbols, `q_max = min(1, 0.25*N)`. The amount `q_max` is a fraction of
deployable incremental cash, not total portfolio value. With fewer than four Buy names,
the cap necessarily leaves some cash. A post-cap result must be audited because capping
can change a risk optimizer's original risk profile.

The formulas and solver controls below are researcher-approved specifications. They
remain specification-only and are not implemented or validated on historical data.

## Method details

### EW — Equal Weight

Set raw `u_i = 1` for every eligible Buy name, normalize over that exact set, and apply
the common iterative 25% cap. With fewer than four names, the maximum feasible deployment
is `0.25*N`; with four or more, the method can deploy all cash subject to rounding and
execution constraints. No risk-history input is required. No Buy names or no cash means
no allocation, not an error.

### IV — Inverse Volatility

For each eligible name estimate daily sample volatility `sigma_i` from the common
validated trailing 60-observation window. Raw weight is `u_i = 1/sigma_i`; normalize and
apply the shared cap.

Any non-finite or non-positive `sigma_i`, incomplete common input, or insufficient
history makes the **method decision unavailable** and retains cash. Do not remove a
security from the Buy universe, replace the input with EW, or apply a volatility floor.
The 06 harness already raises an explicit policy error in these cases.

### ERC — Equal Risk Contribution (Decisions E-012 and E-013)

For covariance `Sigma` and normalized risky-sleeve weights `s`, where `s_i>=0` and
`sum(s)=1`, define `v(s)=s' Sigma s`, `RC_i(s)=s_i(Sigma s)_i`, and
`p_i(s)=RC_i(s)/v(s)`. Minimize `sum_i (p_i(s)-1/N)^2`. Apply the resulting risky
composition to deployable cash using the common cap-and-redistribute procedure. The
final actual investment weights `w` must satisfy `0<=w_i<=0.25`; any unallocatable
amount remains residual cash. Store normalized `Risky_Sleeve_Weights` separately from
these actual incremental-cash weights; do not constrain the normalized sleeve to the 25%
actual-cash cap.

Record optimizer risky-sleeve weights, raw actual weights, and final post-cap actual
weights separately. Record raw and post-cap component and relative contributions,
calculating `RC_i(w)=w_i(Sigma w)_i` and `p_i(w)=RC_i(w)/(w'Sigma w)` for actual weights.
Define post-cap relative deviation as `max_i(abs(p_i(w)-1/N)/(1/N))`. ERC passes only if
solver convergence is reported, objective and weights are finite, the risky-sleeve sum
and actual-weight bounds pass, relative contributions sum to one within tolerance, and
post-cap relative deviation is at most 5%.

Use SLSQP with equal initialization, `maxiter=10000`, and `ftol=1e-8`; ERC relative
deviation tolerance is `0.05`. Record solver name/version, status, iterations, objective,
weight-sum and bound residuals, raw/post-cap weights, and risk-contribution diagnostics.
If SLSQP does not converge, constraints fail, or post-cap deviation exceeds 5%, mark ERC
unavailable and retain cash. Never substitute EW.

### HRP — Hierarchical Risk Parity (Decision E-014)

Use sample correlation for clustering and centered sample covariance for cluster-risk
calculations, both derived from the same 60-observation common complete return matrix.
Use identical common dates, symbol order, and estimation cutoff. Ledoit-Wolf shrinkage
and mixed sample/shrinkage estimators are not permitted without a new researcher
decision. Record observation count, cutoff, ordered symbols, risk-data hash, correlation
and covariance matrices, finite/symmetry checks, diagonal variances, correlation range,
eigenvalue/PSD status, and condition estimates.

1. Set correlation distance `d_ij = sqrt((1-rho_ij)/2)` with finite/range checks.
2. Perform hierarchical clustering on the condensed distance matrix using **single
   linkage**.
3. Quasi-diagonalize by the hierarchical leaf order.
4. Recursively bisect the ordered cluster. For each half, calculate inverse-variance
   within-cluster weights and its estimated cluster variance `V_L`, `V_R`; allocate
   `alpha_L = 1 - V_L/(V_L+V_R)` to the left half and the remainder to the right.
5. Normalize risky-sleeve weights and apply the shared cap-and-redistribute rule to
   actual investment weights.

Reject invalid correlations, zero cluster variance, malformed linkage, or any
non-finite result. Record estimator pair, linkage method, leaf order, cluster variances,
and post-cap weights. A clustering or allocation error marks HRP unavailable and retains
cash; do not use a fallback. HRP remains unimplemented in the Phase C harness.

### MinVar — Minimum Variance (Decisions E-015 and E-016)

For `N` eligible Buy securities, use the approved target `q_max=min(1,0.25*N)` and solve

`minimize w' Sigma w`

subject to `0 <= w_i <= 0.25` and `sum(w) = q_max`.

Each `w_i` is a fraction of **deployable incremental Buy cash**, not a fraction of total
portfolio equity.

The feasible target sums are `0.25, 0.50, 0.75, 1.00, 1.00` for `N=1,2,3,4,5`;
`w_i=q_max/N` demonstrates feasibility for each. For fewer than four names,
`1-q_max` remains allocation-budget cash.

Use SLSQP with `maxiter=10000`, objective tolerance `ftol=1e-10`, constraint tolerance
`1e-8`, and weight-feasibility tolerance `1e-8`. Verify solver success, finite objective,
bounds, weight sum, and all residuals against their tolerances. If any check fails,
mark MinVar unavailable and retain cash; do not substitute another allocator.

### CVaR — Conditional Value at Risk

Preserve the 252-observation history and 95% confidence. For scenario return vector
`r_t`, define loss `L_t(w) = -r_t'w`. Empirical tail CVaR can be represented by the
Rockafellar–Uryasev expression:

`min_(eta,u) eta + [1/((1-alpha)T)] * sum_t u_t`

subject to `u_t >= L_t(w)-eta`, `u_t >= 0`, and the approved weight/cash constraints.
An implementation must use daily decimal returns and record the exact tail weighting.
For 252 equally weighted observations at 95%, the tail probability mass is
`m = (1-0.95)*252 = 12.6` observations. Define scenario loss as
`L_t(w) = -r_t'w` and sort from largest/worst loss to smallest:
`L_(1) >= ... >= L_(252)`. With no ties at the cutoff, empirical 5% expected shortfall is
`(sum_(j=1..12) L_(j) + 0.6*L_(13))/12.6`. Averaging the worst 13 gives a 13/252 =
5.1587% tail and is not exactly a 5% tail.

**Tie handling:** use full-precision computed losses, do not round them for sorting, and
group exactly equal losses at the tail boundary. Include every loss strictly worse than
the boundary fully; distribute the remaining fractional tail mass equally across all
observations tied at the boundary. This makes the tail value invariant to arbitrary
row-order tie breaking. Sort the scenario records by descending loss and then ascending
verified session date as a deterministic record order, but do not use that secondary
ordering to choose only some tied observations. Record the cutoff loss, tie-group size,
fractional weight per tied observation, and total tail mass (12.6). The legacy `ceil`
convention is not carried forward.

### Approved fixed-`q_max` CVaR formulation (Decisions E-017 and E-018)

Using the same `q_max = min(1, 0.25*N)`, the approved objective is

`minimize empirical CVaR_0.95(w)`

subject to `0 <= w_i <= 0.25` and `sum(w) = q_max`,

using the selected fractional-tail convention over the common 252-observation scenarios.
Each `w_i` is a fraction of deployable incremental cash, not total portfolio equity.
The feasible target sums for `N=1..5` are `0.25, 0.50, 0.75, 1.00, 1.00`, respectively.
For `N<4`, the risky mix is allocated to the maximum feasible exposure rather than one;
the remaining allocation-budget cash fraction is `1-q_max`. For `N>=4`, up to all
deployable cash can be assigned subject to the 25% caps. These constraints avoid the
infeasibility of `sum(w)=1` when fewer than four securities are eligible, but they do
not select an independently optimized cash/risk target.

Use HiGHS with `maxiter=100000`, primal feasibility tolerance `1e-8`, and dual
feasibility tolerance `1e-8`. Record solver status, iteration count, CVaR objective,
weight bounds, weight sum, constraint residuals, tail cutoff, tie-group size, and
fractional tie mass. If the solver fails or any objective/weight/constraint check fails,
mark CVaR unavailable and retain cash; do not substitute another allocator.

The fixed-`q_max` objective, empirical fractional tail, tie convention, solver controls,
and fail-closed behavior are approved specifications. They do not resolve the historical
252-session data or gate blockers; CVaR remains unavailable for the current historical
universe.

### MPT — Mean-Variance Optimization (Decisions E-019 and E-020)

Use the approved expected-return and covariance inputs and preserve the objective:

`maximize w' mu - 5*w' Sigma w`

subject to `0 <= w_i <= 0.25` and `sum(w) <= 1`. Estimate `mu` as the arithmetic mean
of daily decimal returns over 60 common complete sessions. Use centered sample covariance
from the same 60 common complete sessions. Residual cash is retained as `1-sum(w)`.

Negative expected return is not an invalid input. If every expected return is
non-positive and `Sigma` is PSD, zero weights (cash) maximize the stated objective.
Use SLSQP with zero initialization, `maxiter=10000`, objective tolerance `ftol=1e-10`,
constraint tolerance `1e-8`, and weight-feasibility tolerance `1e-8`. Record solver
status, iterations, objective value, bounds, weight sum, cash residual, and constraint
residuals. If SLSQP fails or any constraint fails, mark MPT unavailable and retain cash;
do not automatically fall back to EW.

## Method comparison

| Method | Risk input | Raw output | Approved validation/failure criteria | Phase C harness |
|---|---|---|---|---|
| EW | None | Equal incremental cash weights | None in the basic formula; data universe and execution still block use. | Implemented |
| IV | 60 common returns / volatility | Inverse-volatility weights | Full window; invalid/non-positive volatility makes method unavailable and retains cash. | Implemented with fail-closed input errors |
| ERC | 60 common returns / centered sample covariance | Equal relative risk contributions; normalized sleeve, then actual-weight 25% cap | SLSQP convergence and post-cap contribution deviation <=5%. | Not implemented |
| HRP | 60 common returns / sample correlation and covariance | Single linkage, quasi-diagonalization, recursive bisection | Fail closed on clustering/allocation errors. | Not implemented |
| MinVar | 60 common returns / centered sample covariance | Minimum variance with `sum(w)=q_max` | SLSQP controls and feasibility checks are fixed above. | Not implemented |
| CVaR | 252 common return scenarios, 95% | Empirical fractional-tail risk with `sum(w)=q_max` | HiGHS controls and 12.6-tail/tie rules are fixed above. | Not implemented |
| MPT | 60 common returns / arithmetic mean and centered sample covariance | Approved mean-variance objective; residual cash allowed | SLSQP controls and feasibility checks are fixed above; `lambda=5`. | Not implemented |

Any calculated raw weights must be preserved with their post-cap weights, cash fraction,
eligibility set, risk-data cutoff, and method status. This specification does not
authorize a historical allocation run.
