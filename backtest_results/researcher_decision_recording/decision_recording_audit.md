# Workstream 1.8 — Decision Recording Audit

## Result

This workstream records, but does not expand, the researcher's explicit approvals of
E-004 and E-029. The approvals were received in the current conversation and recorded
on 2026-11-17 using the repository's ISO date convention. No researcher identity was
inferred.

| Decision | Original status | Final status | Approved option |
|---|---|---|---|
| E-004 | `NEEDS_RESEARCHER_APPROVAL` | `APPROVED` | Option B |
| E-029 | `NEEDS_RESEARCHER_APPROVAL` | `APPROVED` | Option B |

The canonical register is
`backtest_results/phase_E_portfolio_specification/phase_E_decision_register.csv`.
Its original SHA-256 was
`43ce34d96b462134d4d697231573b762ff8ee72de690704fdaeb016bda530a99`. Its final
SHA-256 is recorded in `decision_register_change_log.csv` and verified against the
register after recording.

## Exact approvals recorded

### E-004 — Segment annualization

The E-004 register row now records Option B: 252 verified exchange-session return
intervals per nominal year; annualized segment metrics are permitted only for at least
252 valid consecutive one-session return intervals (253 valid equity marks). Shorter
valid segments remain unannualized and disclose elapsed time. Gaps are not bridged and
segments are not combined. Risk-free Rate and MAR remain separate decisions requiring
approval. No historical performance metrics were calculated.

### E-029 — Snapshot/version identifiers

The E-029 register row now records Option B: `Universe_Snapshot_ID`,
`Prediction_Snapshot_ID`, `Execution_Eligibility_Snapshot_ID`, `Model_Version`, and
`Allocation_Policy_Version` are mandatory run/snapshot lineage references in the
lineage manifest; daily records reference applicable snapshots where relevant. These
are not five new numerical optimizer arguments. `Risk_Data_Hash` remains separately
required. Archived identifiers must not be inferred or backfilled. Missing or
inconsistent future lineage is reported as `PROVENANCE_INCOMPLETE`. This approval does
not independently change E-011, E-028, or execution-gate behavior.

## Files changed

Existing canonical Phase E documents changed only to record or mirror E-004/E-029:

- `backtest_results/phase_E_portfolio_specification/phase_E_decision_register.csv`
  — only the E-004 and E-029 rows, using existing columns.
- `backtest_results/phase_E_portfolio_specification/phase_E_revision_changelog.md`
  — two appended decision entries; prior changelog text retained.
- `backtest_results/phase_E_portfolio_specification/E2_valuation_stale_price_policy.md`
  — E-004 status and approved threshold mirrored; RF/MAR and evidence limitations
  remain explicit.
- `backtest_results/phase_E_portfolio_specification/E5_cross_method_consistency.md`
  — E-029 status and lineage behavior mirrored; `Risk_Data_Hash` retained.
- `backtest_results/phase_E_portfolio_specification/phase_E_summary.md`
  — E-004/E-029 approvals and remaining unresolved matters mirrored.
- `backtest_results/phase_E_portfolio_specification/phase_E_validation_report.md`
  — decision statuses and historical test-scope limitation clarified.
- `backtest_results/phase_E_portfolio_specification/phase_E_manifest.json`
  — status counts, remaining approval list, synthetic-check caveat, and hashes
  refreshed.

New deliverables are the five files in
`backtest_results/researcher_decision_recording/`. No other source or protected files
were authorized for modification. No new decision-register row or schema column was
introduced.

### Register row/field comparison

- E-004 changed fields: `Existing_Approved_Rule`, `Available_Evidence`,
  `Proposed_Recommendation`, `Alternative_Options`, `Risk_of_Each_Option`,
  `Approval_Required`, and `Current_Status`.
- E-029 changed fields: `Existing_Approved_Rule`, `Available_Evidence`,
  `Proposed_Recommendation`, `Alternative_Options`, `Risk_of_Each_Option`,
  `Approval_Required`, and `Current_Status`.
- All other fields and all other register rows are unchanged at the parsed field level.
  The 10-column schema and 29 decision IDs are retained.

## Other decisions and constraints

E-001 remains `BLOCKED`; E-002 remains `NEEDS_RESEARCHER_APPROVAL`; E-005 through E-020
remain `APPROVED`; E-021 and E-022 remain `BLOCKED`; E-023 remains `VERIFIED` as a
baseline only; E-027 and E-028 remain `APPROVED`. Risk-free Rate and MAR remain
`NEEDS_RESEARCHER_APPROVAL`. The prior E-007 record was not changed; its segmentation
and gap rules remain in force, with the later E-004 approval controlling annualization.

The Research Backtest Gate remains `BLOCKED`; Phase F remains `DO_NOT_BEGIN`. The
decision recording does not implement annualization or identifiers and does not clear
data, calendar, corporate-action, universe, sizing, execution, or historical-lineage
blockers.

## Protected assets and prohibited actions

No historical data, execution snapshot, dataset, model, notebook, archived result, or
portfolio output was modified. No market data was downloaded; no internet or external
data source was accessed; no model was loaded or trained; no predictions, allocations,
optimizers, or backtests were run. The Workstream 1.7 decision-preparation reports were
preserved as historical preparation artifacts.
