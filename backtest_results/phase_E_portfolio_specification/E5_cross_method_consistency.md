# E5 — Cross-Method Consistency Contract

## Shared allocation interface

Approved allocator input:

`Risk_Data_Hash, Decision_Date, Method, Eligible_Buy_Symbols, Deployable_Cash, Risk_Data_Cutoff, Lookback, Max_Weight=0.25`

Under E-029 Option B, approved 2026-11-17, the five proposed
`Universe_Snapshot_ID`, `Prediction_Snapshot_ID`,
`Execution_Eligibility_Snapshot_ID`, `Model_Version`, and
`Allocation_Policy_Version` identifiers are mandatory run/snapshot lineage references
in the lineage manifest. Daily records reference applicable snapshots where relevant.
They are metadata references, not five new numerical optimizer arguments.
`Risk_Data_Hash` remains separately required by the approved risk-data lineage policy.
Do not infer or backfill identifiers for archived historical runs. Missing or
inconsistent future lineage is reported as `PROVENANCE_INCOMPLETE`. This status does
not independently change E-011, E-028, or execution-gate behavior.

The input set and cash amount must be identical across allocation methods for the same
strategy/date. The allocator must not receive the next-session Open or Close. Its output
is a decision record, not an order. Use nine strategies from the Panic × FOMO × Normal
Cartesian product; Normal is always Hold. Sell liquidates the current position, Hold
preserves its share count, and Buy adds shares from incremental available cash only.
The common action order is Sell → forced SET50 exit → Buy → Hold; Hold is a
no-trade position-preservation action. Do not sell Hold positions to fund Buys. The
portfolio is long-only with no shorting or leverage.

`Risk_Data_Hash, Decision_Date, Method, Symbol, Raw_Weight, Final_Weight, Cash_Budget, Risk_Window, Observation_Count, Risk_Data_Cutoff, Method_Status, Failure_Reason, Solver_Metadata`

One row per eligible Buy symbol plus an auditable cash/residual summary. `Risk_Data_Hash`
must identify the exact same ordered risk-input frame across methods for the same
decision.

## Two distinct cash residuals

- **Allocation-budget residual cash** is computed before looking at execution prices:
  `Deployable_Cash * (1 - sum(Final_Weight))`. It reflects the cap ceiling when fewer
  than four securities are eligible or any method's approved cash decision.
- **Post-execution residual cash** is the actual ledger cash after valid fills, lot
  rounding, fees, and any unfilled/blocked orders. It is not necessarily equal to the
  allocation-budget residual; lot rounding and missing Open can leave more cash unused.

Report both separately. The allocation result must not change after execution quotes
become available; post-execution residual must not be retroactively relabeled as an
allocation weight.

Keep three distinct quantities: `Risky_Sleeve_Weights` (normalized composition of the
risky allocation, summing to one when nonempty), `Actual_Investment_Weights` (fractions
of deployable cash after method constraints and caps), and `Residual_Cash` (the
allocation-budget amount not allocated to risky investments). Post-execution cash is a
separate ledger result and must not be conflated with allocation-budget residual cash.

## Invariants across all methods

1. **Same Buy universe:** use the same point-in-time SET50, identity, exclusion,
   execution-eligibility and Buy-signal intersection. Do not remove a symbol only for one
   method because its risk input is inconvenient; that method becomes unavailable.
2. **Same deployable cash:** cash after successful Sell orders and forced exits, net of
   their costs. Failed exits produce no cash. Never liquidate a Hold to fund a Buy.
3. **Same cap:** each incremental allocation weight is at most 0.25; iteratively
   redistribute feasible excess; keep unallocatable cash. Do not apply this cap to total
   portfolio market value.
4. **Existing holdings:** a Buy signal adds to existing shares; a Hold retains quantity;
   a Sell liquidates the existing position when a valid execution Open exists.
5. **Same order sequence:** Sell, forced SET50 exit, Buy, then Hold
   (Hold preserves the existing position without an order). Do not liquidate a Hold to
   fund a Buy; no shorting or leverage is permitted.
6. **Same risk cutoff:** daily returns only, from validated prior observations and one
   shared cutoff. The legacy engine uses dates `< decision_date`; preserve that
   conservative cutoff unless explicitly approved otherwise.
7. **Same execution assumptions:** next eligible observed session, fill at
   `Open*(1 +/- 0.001)`, 0.0016799 transaction-cost rate per side, no gap limit, and no
   Close substitution for missing Open.
8. **Same output contract and status vocabulary:** all methods expose the approved core
   fields, raw/final weights, cap adjustment, risk sample/count and hash, method status,
   failure reason, allocation-budget residual, post-execution residual, and solver
   diagnostics. Include references to the applicable E-029 lineage-manifest identifiers
   where relevant; do not make them numerical optimizer arguments. Preserve
   `Risk_Data_Hash` as required and report missing/inconsistent future lineage as
   `PROVENANCE_INCOMPLETE`. Do not hide a failure as a zero allocation or backfill
   historical identifiers.
9. **No lookahead:** predictions/risk inputs are frozen at the decision timestamp. Final
   weights must be persisted before revealing execution-date Open/Close to the allocator.
10. **Separate sizing:** after weights are finalized, order sizing reads the valid
    execution Open and approved effective-date lot schedule. Do not conflate fractional
    allocation weights with whole executable shares.

## Approved execution and transaction-fee sequence

Execute at the Open of the next eligible execution trading session and mark to market at
that same session's Close. Use 0.001 slippage per side and transaction cost 0.0016799 per
side, with no gap limit. Missing Open means no execution; never substitute Close or a
prior price.

1. Calculate slippage-adjusted `Fill_Price = Raw_Open * (1 + 0.001)` for buys or
   `Raw_Open * (1 - 0.001)` for sells.
2. Calculate `Gross_Notional = Shares * Fill_Price`.
3. Calculate `Fee = Gross_Notional * 0.0016799`.
4. For a buy, `Cash_Debit = Gross_Notional + Fee`; for a sell,
   `Cash_Credit = Gross_Notional - Fee`.

Do not add slippage again as a separate cash fee: it is already reflected in fill price.
Record `Raw_Open`, `Fill_Price`, `Gross_Notional`, `Fee_Rate`, `Fee`, and
`Cash_Debit_or_Credit` separately. The
legacy Notebook 05 combines rates additively on raw Open; that prototype is not the
approved calculation. This phase makes no code change.

## Edge-case contract (conceptual; not historical results)

| Case | Expected shared behavior |
|---|---|
| Zero Buy securities | No allocator call; `NO_ELIGIBLE_BUYS`; no order. |
| One Buy security | Maximum allocation is 25% of deployable cash; the remaining 75% stays cash. |
| Two or three Buy securities | Maximum deployment is 50% or 75%, respectively; residual remains cash. |
| Four Buy securities | Up to 100% can be allocated, with each weight at most 25%. |
| More than four Buy securities | Up to 100% can be allocated; apply the same iterative cap to every method. |
| Zero available cash | `NO_DEPLOYABLE_CASH`; no allocation or order. |
| Cash too small for one lot | Weight decision remains auditable; share quantity is zero and cash remains; do not lower lot size. |
| All expected returns negative | MPT may select all cash under its approved constraints; do not force risky exposure. |
| Missing risk observations | Do not fill or remove symbols; common complete-date sample shrinks across the complete Buy universe; if below the approved full window, mark that method unavailable. |
| Singular / non-PSD covariance | Reject or mark unavailable under the approved numerical policy; no silent jitter, clipping, or EW fallback. |
| Non-positive volatility | IV unavailable unless an approved rule says otherwise; do not divide or substitute a volatility floor. |
| Raw weights exceed 25% | Apply the same deterministic cap/redistribution step and record both raw and final weights. |
| Any method fails | That method is unavailable for its strategy-method run; place no Buy orders for that run and retain cash; report the common failure status with method-specific reason. Do not substitute EW or a different method. If all methods are unavailable, the allocation comparison remains blocked. |
| Missing execution Open | No fill; no Close/prior price substitution; record blocked order. |
| Missing valuation Close | Apply only an approved bounded stale-mark policy; otherwise valuation is unavailable. |

These are specification-level approved outcomes, not a run of historical data or the
portfolio engine. Synthetic formula checks are recorded in
[phase_E_validation_report.md](./phase_E_validation_report.md).

## Approval and readiness

The interface is an approved shared specification, but it does not resolve the current
method implementations, missing evidence, or Phase D universe limitations.
The Phase C harness implements only EW and IV, and its 63-run function refuses to execute
while the gate is closed or the allocator set is incomplete.

**Policy status: APPROVED. Historical execution readiness: BLOCKED.** The rules do not
open the Research Backtest Gate or authorize historical portfolio construction or Phase F.
