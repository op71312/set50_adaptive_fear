# Read-only Implementation Review

## Executive Summary

This review examines the current Notebook 07/08 source, the existing exports, and manifests for run `RPR-829A43493C6B4CADACEC3ED50621C407`. No backtest, prediction, model fitting, external data access, or source modification was performed.

| Review area | Status | Key finding |
|---|---|---|
| Turnover definition | **PASS — mathematical implementation**; **NOT_VERIFIABLE — policy alignment** | Source computes filled gross notional divided by mean equity over a valid contiguous segment. All 54 completed output rows reconcile to that formula. The Phase E decision register does not define a turnover formula. |
| Strategy action generation | **NOT_VERIFIABLE — exact run behavior** | Current Notebook 07 source defines the approved nine-action matrix and forces class 2 to HOLD. Current Notebook 08 groups signal sells and forced exits before buys. No action log is exported, and current Notebook 08 does not match the run-recorded hash. |
| Position valuation lineage | **NOT_VERIFIABLE — per-combination / run binding** | Current source marks positions using same-execution-date vendor Close and computes equity as cash plus market value. Exported valuation rows lack strategy and allocation identifiers; exact Notebook 08 provenance also differs from the run record. |
| Execution Snapshot SHA-256 | **PASS — actual file matches the 64-character hash** | The actual file hash matches the second value in the request and both run manifests. The first supplied value is 61 characters, not a valid SHA-256 digest. `SHA256SUMS.txt` does not include the source snapshot. |

**Material provenance limitation:** current Notebook 08 hashes to `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8`, whereas `run_manifest.json` and `reconciliation_manifest.json` record `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081`. The reviewed Notebook 08 source therefore cannot be proven identical to the exact source used for the run. The reason for the difference cannot be established from the available evidence.

## Scope and Constraints

- Reviewed only the existing run outputs and current repository source/manifests for the four requested topics.
- Did not run or repeat a backtest, model inference, or prediction generation.
- Did not download data, call external APIs, or alter source, notebooks, model, datasets, manifests, prior outputs, or gate statuses.
- Notebook source line references below mean line numbers within the indicated code cell; notebook JSON does not expose ordinary standalone Python line numbering.
- Output-level reconciliation facts are cited from the existing `targeted_reconciliation/TARGETED_RECONCILIATION_REPORT.md`; that reconciliation was not rerun here.

## 1. Turnover Definition

### Source behavior

In `07_dynamic_universe_portfolio_backtest_v2_corrected.ipynb`, Cell 21, `calculate_segment_metrics`:

- Lines 210–213 take the segment's first and last valid dates and use its daily equity rows.
- Lines 214–217 select only `FILLED` transactions whose `Execution_Date` is between the segment dates, inclusive.
- Line 220 sums `Gross_Notional` for those fills without filtering by side, so both BUY and SELL notionals contribute.
- Lines 221–222 divide that total by `np.mean(equity)` for the segment.

Cell 18, `valid_equity_segments`, lines 24–62, forms segments from positive, valid equity marks and splits at invalid marks or non-consecutive session ordinals. Thus the denominator is the arithmetic mean of valid daily `Portfolio_Equity` marks in the contiguous segment, not Initial Equity or a full-calendar-day series containing invalid marks.

### Run-output cross-check

The existing `performance_segments.csv` contains 54 rows. Every row covers `2026-03-31` through `2026-11-13`, with 150 valid equity marks and 149 return intervals. The existing reconciliation reports that reported turnover equals filled gross notional divided by mean daily equity for **54/54** completed combinations, with a maximum absolute difference of 0. No historical run was repeated for this review.

### Policy assessment

The current `phase_E_decision_register.csv` SHA-256 is `7cc61072a253a358c7613f2e9fb29ed57a52a5c80eaf0312951d75c8e3bd8c92`, matching the hash recorded for the run's Decision Register. A case-insensitive search of that register found no `turnover` entry. Therefore:

- **Mathematical implementation:** **PASS** — formula and completed output values agree.
- **Policy alignment:** **NOT_VERIFIABLE** — no turnover denominator/period definition was found in the cited approved register. The mean-segment-equity denominator is established as implementation behavior, not as an approved policy.

Evidence: Notebook 07 Cell 18 lines 24–62 and Cell 21 lines 210–222; `performance_segments.csv` (54 rows); `run_manifest.json` line 24; `phase_E_decision_register.csv`.

## 2. Strategy Action Generation

### Matrix and Normal behavior

Notebook 07 Cell 2 lines 26–47 lists all nine strategy IDs and maps prediction classes 0, 1, and 2 to the Panic, FOMO, and Normal actions. All nine class-2 entries are HOLD.

The later/effective `strategy_signals` definition in Notebook 07 Cell 21 lines 68–106:

- selects the mapping by `strategy_id` (lines 75–76, 90–91);
- sets action/target weights according to BUY/SELL (lines 94–99); and
- explicitly forces class 2 to `HOLD`, preserves its current weight, and sets reason `NORMAL_ALWAYS_HOLD` (lines 100–104).

Notebook 07 Cell 20 lines 175–203 calls prediction generation for `predictor_date`/`execution_date`, then calls `strategy_signals` with the prediction, current weights, strategy ID, and parameters. The signal function itself accepts no Actual Target or Future Return argument and derives actions from the prediction class, not from realized return fields.

### Execution ordering and audit trail

Current Notebook 08 Cell 9 lines 163–165 builds one set from signal SELLs and forced exits, then processes that liquidation set. Lines 183–221 process BUY candidates afterward. HOLD is a no-op because it enters neither set of transactions. This implements liquidations before buys, but does not retain an explicit, separately auditable `SELL` then `FORCED_EXIT` stage; both are combined.

Notebook 08 Cell 11 lines 108–134 exports Transactions, Daily Portfolio, Position Valuation, Allocation Weights, and Eligibility, but no strategy-action log. Transaction rows carry Strategy_ID and Allocation_Method and execution Side, but do not record each symbol's original Action, HOLD, or forced-exit reason as a distinct action event.

**Status: NOT_VERIFIABLE for the exact run.** The current Notebook 07 source is hash-pinned to the run (see integrity findings), and its matrix is consistent with the requested action mapping. However, the existing output has no action log, current Notebook 08 differs from the run-recorded Notebook 08 hash, and therefore the current Notebook 08 ordering cannot be bound conclusively to the historical run. The current source's combined liquidation-before-buy behavior is evidenced, but is not a per-run action-log verification.

Evidence: Notebook 07 Cell 2 lines 26–47, Cell 20 lines 175–203, Cell 21 lines 68–106; Notebook 08 Cell 9 lines 163–221 and Cell 11 lines 108–134; run export inventory in `SHA256SUMS.txt`.

## 3. Position Valuation Lineage

### Current source behavior

Notebook 07 Cell 16 defines the position valuation columns and `mark_portfolio`:

- Cell source lines 75–90 require a verified-calendar flag and session ordinal for a valid valuation.
- Lines 111–133 use a valid quote Close for the current date or reuse a previous valid mark; stale age is measured by session ordinal and values beyond `MAX_STALE_VERIFIED_SESSIONS` make portfolio value unavailable.
- Lines 134–147 calculate position value as quantity × mark price.
- Lines 149–168 calculate daily equity as cash + market value when valuation is available.

Notebook 08 Cell 9 lines 227–243 adapts finite observed vendor Closes into quote rows labeled `Status="VERIFIED"` for the Notebook 07 mark function, while adding `OBSERVED_VENDOR_CALENDAR` and proxy valuation labels. This `VERIFIED` quote status must not be interpreted as verification of an official exchange calendar or exchange-tradable price.

Notebook 07 Cell 20 lines 320–331 builds Close quotes from execution-date rows and calls `mark_portfolio` with that `execution_date`; this is the current-source path for marking at that day's observed Close after that session's order handling. The daily record receives Strategy_ID and Allocation_Method at lines 333–350, but the position rows are appended directly at lines 351–357 without those fields.

### Output linkage and look-ahead limits

The existing `position_valuation.csv` columns are:

`Date, Symbol, Quantity, Mark_Price, Price_Date, Stale_Observed_Session_Age, Valuation_Status, Position_Value, Calendar_Classification, Valuation_Source_Status, Run_ID, Research_Backtest_Gate, Execution_Validation_Gate, Research_Classification, Price_Return_Basis`

There is no `Strategy_ID` or `Allocation_Method`. Notebook 08 Cell 11 lines 108–125 adds run, gate, classification, and price-return labels to valuation rows, but no combination identifiers. The rows are accumulated in loop order, but no persisted row key or boundary metadata reliably associates an individual mark with one of the 54 completed combinations. The prior reconciliation also records that valuation rows cannot be joined to individual combinations.

The existing daily output's cash-plus-market-value arithmetic was reconciled in the earlier output-only report, but that does not independently establish per-combination position quantities/marks or prove that the historical implementation never used future information. The current source uses execution-date Close for subsequent marking; this observation alone is not proof of the complete run's causal behavior.

**Status: NOT_VERIFIABLE for per-combination valuation and run-level look-ahead.** Current source semantics are inspectable, and Notebook 07's current hash matches the run record; nevertheless, valuation outputs lack combination keys, and Notebook 08's current hash does not match the run record.

Evidence: Notebook 07 Cell 16 lines 75–168 and Cell 20 lines 320–357; Notebook 08 Cell 9 lines 227–243 and Cell 11 lines 108–125; `position_valuation.csv` header.

## 4. Execution Snapshot SHA-256

Actual source file:

`dataset/verified_build_20261113_152948/SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`

| Evidence | SHA-256 / observation | Result |
|---|---|---|
| Actual file, read and hashed during this review | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` (324,428 bytes) | Actual digest |
| `run_manifest.json` lines 15 and 30 | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Matches actual |
| `reconciliation_manifest.json` lines 19 and 34 | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Matches actual |
| Notebook 07 `EXPECTED_EXECUTION_SHA256` | Same 64-character value | Matches actual |
| Previously recorded value supplied in the request | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19e4d9c51ef986a` (61 characters) | Not a valid 64-character SHA-256 representation; does not match actual |
| Run `SHA256SUMS.txt` | Lists run output exports; no Execution Snapshot entry | Cannot verify the source snapshot from this file |

**Status: PASS for the second value; the first value is invalid/nonmatching.** The actual file, run manifest, reconciliation manifest, and Notebook 07 expected hash agree. `SHA256SUMS.txt` is an output checksum list, not a checksum attestation for this source file.

## Source and Run Integrity Findings

| Item | Run-recorded SHA-256 | Current SHA-256 | Finding |
|---|---|---|---|
| Notebook 07 corrected implementation | `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070` | Same | Hash matches run record |
| Notebook 08 research runner | `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081` | `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8` | Hash mismatch; exact run source is not established |

The Notebook 08 discrepancy is a provenance gap, not evidence by itself that the run outputs are wrong or that a specific code change caused the difference.

## Impact on Research Proxy Reliability

- Turnover arithmetic in the existing completed outputs is consistent with the current Notebook 07 formula, but that denominator is not traceable to an approved turnover policy in the Phase E register.
- Strategy mapping and Normal HOLD behavior are explicit in current Notebook 07, but the absence of an action log prevents output-level confirmation; Notebook 08 source hash drift further limits exact run attribution.
- Position values cannot be reconciled independently for each combination because the exported valuation file omits Strategy_ID and Allocation_Method. This limits auditability of holdings, marks, and any combination-specific stale valuation.
- The source Snapshot hash conflict resolves to the 64-character value found in the file and run manifests; the shorter supplied value is not a valid SHA-256 digest. The run output checksum list does not checksum that source file.
- These findings support only a provisional Research Proxy assessment. They do not establish execution validation, exchange tradability, or verified total-return performance.

## Recommendations (No Changes Made)

1. Preserve the exact Notebook 08 source used for any future run and record a matching immutable hash; investigate the existing hash drift before treating current source as the run's exact implementation.
2. Export a per-decision action log with Run_ID, Strategy_ID, Allocation_Method, predictor/execution dates, prediction class, Action, forced-exit flag/reason, and action processing order.
3. Add Strategy_ID and Allocation_Method to every position valuation row, and retain a stable combination/snapshot key.
4. Record the approved turnover formula, period, and denominator explicitly in the policy register or run manifest.
5. Keep vendor quote validity separate from official exchange-calendar verification; include source calendar/session semantics in valuation rows.
6. Correct the malformed 61-character hash reference in its owning record and include the execution snapshot in a source-input checksum manifest in any future run record. No existing hash record was changed here.

## Gate Status (Unchanged)

- `RESEARCH_BACKTEST_GATE = CONDITIONAL_OPEN`
- `EXECUTION_VALIDATION_GATE = BLOCKED`
- `Canonical_Historical_Gate = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`

No gate or blocker status was changed.

## Final Evidence Classification

| Topic | What is established | What still requires evidence |
|---|---|---|
| Turnover | Formula in current Notebook 07 source; output agreement for 54/54 completed combinations | Policy approval for mean-segment-equity denominator |
| Strategy actions | Current Notebook 07 Cartesian matrix and class-2 HOLD implementation; current Notebook 08 liquidation-before-buy code | Exact Notebook 08 source used for the run; output action log linking every action to combination |
| Position valuation | Current-source Close/quantity/value/equity flow; exported valuation columns | Per-combination lineage and run-level assurance against look-ahead |
| Execution Snapshot hash | Actual file hash; agreement with run and reconciliation manifests | `SHA256SUMS.txt` does not include this input; the earlier 61-character value is invalid |
