# Notebook 07 fail-closed and lineage audit

## Scope
This review checks the actual implementation for fail-closed behavior, no-lookahead guardrails, and E-029 lineage enforcement. It does not approve any historical backtest or research gate state change.

## Key fail-closed checks observed in the implementation

### No-lookahead and order-of-operations safeguards
- `generate_predictions`: raises `NoLookaheadError` if `Target_Date <= Feature_Date`.
- `build_dynamic_universe`: raises `NoLookaheadError` if `Execution_Date <= Predictor_Date`.
- `run_portfolio_backtest`: calls `validate_run_context` before any execution and is blocked if gate or lineage status fails.
- `execute_orders`: allocation is performed before Open-price retrieval, as proven by synthetic test `29_allocation_precedes_execution_open`.

### Missing data blocks execution
- Missing `Open` price yields no fill and preserves cash (`27_missing_open_preserves_cash`).
- Missing board-lot rule or unverified lot schedule blocks sizing (`31_unverified_board_lot_blocks_before_open`).
- Missing close beyond the stale threshold leads to `PORTFOLIO_VALUE_UNAVAILABLE` (`34_stale_marks_capped_at_three_sessions` / `35_missing_close_without_prior_mark`).
- Unverified calendar blocks daily equity valuation (`36_calendar_required_for_daily_valuation`).

### Provenance and lineage integrity
- `generate_predictions` requires non-empty `Model_Version` and `Prediction_Snapshot_ID` lineage values.
- `build_run_manifest` requires the five E-029 lineage references and `Risk_Data_Hash` and returns `PROVENANCE_INCOMPLETE` if missing.
- `validate_run_context` rejects any missing required E-029 reference or missing `Risk_Data_Hash`.
- `export_run_outputs` blocks export unless `Research_Backtest_Gate == "AUTHORIZED"` and the manifest status is `COMPLETE`.

### Default-risk and unresolved status checks
The synthetic segment test validates the fail-closed condition in `calculate_segment_metrics`:
- below the 252-interval threshold, the segment remains unannualized
- `Risk_Free_Status` remains `NEEDS_RESEARCHER_APPROVAL`
- `MAR_Status` remains `NEEDS_RESEARCHER_APPROVAL`

This is the correct code path and does not silently substitute hidden defaults.

## Code locations for main findings
- Feature date / target date order: `generate_predictions`
- Membership and identity gate: `build_dynamic_universe`
- Price and lot validation: `execute_orders`, `_lot_rule_for`, `_buy_quantity`
- Valuation and stale-price logic: `mark_portfolio`
- Manifest and export gate: `build_run_manifest`, `validate_run_context`, `export_run_outputs`
- Segment annualization and unresolved RF/MAR status: `calculate_segment_metrics`

## Final verdict
The implementation is fail-closed and lineage-aware. It does not claim historical research validity or authorize Phase F. The code path is consistent with `RESEARCH_BACKTEST_GATE = BLOCKED` and `PHASE_F = DO_NOT_BEGIN`.
