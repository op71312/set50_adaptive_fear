# Archived Buy Universe Assessment

## Finding

The exact historical Buy Universe is **unknown**. No daily Buy-symbol snapshot, allocator-call log, raw weight table, or order-budget record was found in the archived package. The archived prediction CSV contains symbol, predicted class, class probabilities, strategy ID, and allocation ID; it does not record the resulting per-strategy `Action`, eligibility reason, or the exact symbol set passed to an allocator.

Do not reconstruct the Buy Universe from saved predictions, current strategy definitions, current membership files, transaction rows, or current Notebook 05 code. In particular, observed trades are not a complete record of Buy candidates: a candidate may have been blocked, assigned zero budget, failed allocation, or not executed.

## Evidence and distinctions

| Universe / concept | Evidence in archive | Assessment |
|---|---|---|
| Prediction-symbol universe | `daily_predictions_audit.csv` stores rows for 54 symbols over 209 dates, repeated for all 63 pairs. | Observed prediction output only; not the Buy Universe. |
| Buy Universe | No explicit Buy flag/set or per-date allocator input file. | `UNKNOWN_INSUFFICIENT_EVIDENCE`. |
| Held Portfolio Universe | Valuation rows identify nonzero share positions for 35 strategy/allocation pairs. | Observed holdings/marks only; it is not an allocator's risk universe. |
| Active SET50 membership at predictor date | No membership snapshot/hash is recorded in the archive. | Unknown historical input identity. |
| Active membership at execution date | No membership snapshot/hash or forced-exit reason is recorded in the archived transactions. | Unknown; current code must not be substituted. |
| Entire available historical price universe | No archived input path or hash identifies the historical price universe used for risk estimation. | Unknown. |

The archived prediction rows have 54 distinct symbols; GLOBAL has zero rows. The transaction and valuation symbol columns also contain zero GLOBAL rows. This establishes no **recorded direct GLOBAL holding**, not the eligibility logic or risk input set.

## Current-code reference (not historical evidence)

The present `05_backtest.ipynb` saved code derives `buy_names` from action `Buy`, checks execution-date membership and a usable Open, then passes that list to `ALLOCATION_METHODS[allocation_name]`. Sells/forced exits are processed before that step in the current code. Its saved execution state is not linked to the archived run; it cannot establish the archived eligibility date, membership rule, order sequence, or exclusion policy.

The present `06_research_backtest.ipynb` is a fail-closed validation harness, not a record of the archived run. It requires eligibility, policy and gate inputs and saves no historical Buy Universe for the archived package.

## Stop condition

Because no historical Buy Universe snapshot or run-linked allocation input exists, this investigation stops short of deriving any per-date Buy set. `ARCHIVED_BUY_UNIVERSE = UNKNOWN`; Research Backtest Gate remains `BLOCKED`.
