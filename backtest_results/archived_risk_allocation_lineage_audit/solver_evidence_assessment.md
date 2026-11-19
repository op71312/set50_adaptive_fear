# Solver Evidence Assessment

## Archived solver evidence

No archived solver log, optimization result, solver name/version, convergence flag, objective value, iteration count, constraint residual, raw weight vector, or final weight vector was found. Consequently, no historical solver execution or solver success can be verified for ERC, HRP, MinVar, CVaR, or MPT.

The five archived output CSVs do not include solver diagnostics. The archive manifest lists only those outputs and byte sizes, without a run ID, code hash, risk-input hash, or solver configuration.

## Notebook code references (not attributed to the archived run)

The saved current `05_backtest.ipynb` source contains:

| Method | Current code-only solver/configuration observation | Historical result evidence |
|---|---|---|
| EW | No optimizer. | None. |
| IV | No optimizer; standard deviation/inverse-volatility code. | None. |
| ERC | SLSQP, current code uses `maxiter=500`, `ftol=1e-12`; missing history or optimizer failure returns EW. | No archived status/objective/iterations/weights. |
| HRP | SciPy hierarchical clustering with single linkage; current cluster-risk code uses Ledoit-Wolf covariance; exceptions return EW. | No archived correlation, tree, order, cluster variances, or weights. |
| MinVar | SLSQP, current code uses `maxiter=500`, `ftol=1e-12`; missing history or optimizer failure returns EW. | No archived covariance, objective, status, residuals, or weights. |
| CVaR | SLSQP, current code uses `maxiter=500`, `ftol=1e-10`; uses `ceil(5% × T)` worst losses and falls back to EW on failure. | No archived scenarios, tail records, status, objective, or weights. |
| MPT | SLSQP, current code uses `maxiter=500`, `ftol=1e-12`; lambda 5 and cash-allowed sum constraint; missing history/runtime failure returns EW. | No archived μ/Σ, status, objective, residual cash, or weights. |

These parameters are visible in current saved code cells 29 and 31 (execution counts 144–145) and associated definitions. They are not historical solver evidence. They also differ from the approved E4 solver settings and fail-closed policy; the current code must not be substituted for an archived implementation.

## Saved execution-state distinction

- Notebook 05 cell 33 (execution count 146) has a saved synthetic regression test using generated in-memory returns for cap and MPT-cash mechanics. Its output is a test result, not a historical portfolio/date solver result.
- Notebook 05 cell 53 (execution count 156) records that the gate was closed, all 63 experiments were skipped, and no portfolio result CSVs were written in that saved state.
- Notebook 06 cell 22 (execution count 23) explicitly allows only EW and IV in its fail-closed harness; its saved audit output remains `BLOCKED`. No historical optimizer output is present.

No cell was executed during this audit. Synthetic test output, method definitions, and solver configuration do not establish that a solver generated any archived allocation.

`HISTORICAL_SOLVER_EVIDENCE = UNKNOWN`
