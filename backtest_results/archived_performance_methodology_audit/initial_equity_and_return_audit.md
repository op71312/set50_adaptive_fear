# Initial Equity and Return Audit

## Archived evidence

The archived `daily_portfolio_results.csv` begins on 2026-01-06, with decision dates beginning on 2026-01-05. It contains no 2026-01-05 starting-equity row and no `Initial_Equity`, `Initial_Cash`, or per-day return field. Each of the 28 pairs with zero holdings records Cash = Portfolio_Value = 1,000,000 on its daily rows. This is an observed all-cash control value, not a run-linked declaration of the starting denominator for the other 35 pairs.

The recorded daily range has 209 rows and spans 311 calendar days from first to last execution-date mark. The 209 vendor-observed portfolio dates are not certified exchange sessions; an official session count is unavailable. The archived CAGR's exact start point and annualization interval remain unknown.

The archived `archive_manifest.json` explicitly lists the issue: “Total return and CAGR omitted the initial-equity baseline.” This is metadata about the prior run; it does not identify the exact denominator or source code. The archived `performance_summary.csv` nevertheless contains Total_Return and CAGR values for all 63 pairs. The archived package does not state whether those values were based on initial capital, the first recorded daily equity, invested capital, or another denominator.

## First-day treatment

The first stored equity mark is after the first recorded execution date. For example, S1/EW has first daily equity on 2026-01-06 after decision date 2026-01-05; S5/EW records its all-cash value on that same first daily date. No archived return series or first-period formula is retained. The first-day return treatment is therefore unknown.

## Classification

| Question | Finding | Finding status | Evidence classification |
|---|---|---|---|
| Initial cash | $1,000,000 appears in all-cash daily rows for 28 pairs. | PARTIALLY_VERIFIED | `METADATA_REFERENCE_ONLY` |
| Initial shares | No pre-run holdings or initial positions are recorded. | UNKNOWN | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Initial portfolio value | No explicit baseline row; the first active-pair value is an execution-date valuation. | UNKNOWN | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| First recorded daily equity | Present for all pairs on 2026-01-06. This verifies the retained observation, not return treatment. | VERIFIED_CORRECT | `HASH_VERIFIED` |
| Initial capital included in return denominator? | Archive manifest says the initial-equity baseline was omitted; the exact code path is unavailable. | VERIFIED_INCORRECT_PER_ARCHIVE_METADATA | `METADATA_REFERENCE_ONLY` |
| Return denominator | Cannot distinguish initial equity from first daily value or another base. | UNKNOWN | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| First return observation | Not stored and not linked to a historical formula. | UNKNOWN | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Same initial capital across all 63? | All-cash control pairs show $1,000,000; active pairs have no explicit initial-equity record. | PARTIALLY_VERIFIED | `UNKNOWN_INSUFFICIENT_EVIDENCE` |

## Current-code contrast only

Current saved Notebook 05 cell index 45 (execution count 152) inserts an initial row at `INITIAL_DATE` with `INITIAL_CASH`, then calculates `final_value / initial_equity - 1`. Cell index 46 (execution count 153) shows a saved synthetic regression fixture for that formula. Notebook 05 cell index 53 (execution count 156) says all 63 experiments were skipped because the evidence-derived gate was closed. There is no run ID or hash linking this current code or synthetic fixture to the archived performance CSV.

Therefore current code does not resolve the historical denominator. No return or CAGR was recalculated for this audit.
