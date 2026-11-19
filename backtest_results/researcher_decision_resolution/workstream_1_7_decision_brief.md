# Workstream 1.7 — Researcher Decision Brief

**Status:** `WORKSTREAM_1_7 = DECISION_BRIEF_PREPARED`  
**E-004:** `NEEDS_RESEARCHER_APPROVAL`  
**E-029:** `NEEDS_RESEARCHER_APPROVAL`  
**Research Backtest Gate:** `BLOCKED`  
**Phase F:** `DO_NOT_BEGIN`

## Executive summary

This package compares the available choices for E-004 segment annualization and E-029
snapshot/version identifiers. Recommendations below are proposals only. The Phase E
decision register was not changed, no decision was approved on the researcher's behalf,
and no historical metrics or identifiers were generated.

### Recommendations for researcher consideration

- **E-004 — Option B, verified-session annualization, with a conservative short-segment
  floor.** If approved, use a fixed factor of 252 verified exchange-session intervals
  per nominal year. Report annualized segment metrics only when a segment contains at
  least 252 valid consecutive one-session returns (253 valid equity marks); otherwise
  retain unannualized results and elapsed time. The 252-session annualizer is a proposed
  convention, not an existing approval and not implied by CVaR's 252-observation window.
  Risk-free and minimum-acceptable-return inputs remain separately unresolved.
- **E-029 — Option B, a minimum lineage manifest rather than five new allocator
  arguments.** Approve the five proposed identifiers as mandatory references at the
  run/snapshot lineage level if the researcher agrees that each represents a distinct
  object in the prediction-to-execution chain. Daily records should reference the
  relevant snapshot IDs; the fields need not all be repeated as optimizer inputs.
  Preserve the existing `Risk_Data_Hash` as a separate required identifier. No
  historical values for these five fields can be populated from the reviewed archive.

## E-004 — Segment annualization

The existing approved E-007/E2 boundary permits unannualized segment reporting and
actual elapsed-time disclosure. It requires valid contiguous equity segments, forbids
bridging gaps, and prohibits full-period performance metrics when the full equity series
is incomplete. Until E-004 is explicitly approved, annualized segment metrics remain
unavailable.

Option A is the safest immediate reporting policy and requires the fewest assumptions,
but it permanently avoids annualized comparisons if adopted. Option B is recommended
for comparable daily trading-performance reporting, subject to approval of the 252
factor and the 252-return reporting floor. Option C's calendar-time CAGR is
mathematically definable but its volatility and ratio scaling require assumptions about
variance across non-trading days; it is not recommended for daily trading comparisons.

The proposed Option B does not set a risk-free rate or MAR, redefine any approved
allocation/risk window, combine segments, or validate historical results. Metric-specific
definitions and short-segment treatment are in
[E004_segment_annualization_analysis.md](./E004_segment_annualization_analysis.md).

## E-029 — Snapshot/version identifiers

The current approved E5 allocator interface already requires
`Risk_Data_Hash`, decision date, method, eligible Buy symbols, deployable cash, risk
cutoff, lookback, and maximum weight. The five E-029 fields are not currently approved
requirements. `Risk_Data_Hash` identifies the exact ordered risk-input panel; it does
not identify model, prediction, universe, execution-eligibility, or policy artifacts.

Option A would add all five as mandatory fields to every allocator call. Option C would
leave them pending without defining the reproducibility contract. Option B is
recommended: retain the five as distinct, mandatory run/snapshot lineage references
only if approved, with per-decision links where the referenced snapshot changes. This
avoids broadening the allocator's numerical input contract while preserving a complete
provenance chain. Human-readable labels may supplement hashes but cannot replace them.

The W1.4 and W1.5 evidence describes archived risk universe, weights, solver lineage,
metric formulas, and run-linked inputs as unknown or absent. Therefore artifact
identifiers cannot be retroactively inferred from filenames, current notebooks, or
current files. See [E029_snapshot_identifier_analysis.md](./E029_snapshot_identifier_analysis.md).

## Cross-decision consistency

- **E-005 to E-020:** unchanged and not reopened. The approved valuation, common-risk
  panel, estimator, windows, fail-closed, allocation, and execution rules remain in
  force.
- **E-007:** annualization applies only inside valid segments. Segment boundaries,
  unavailable dates, and affected holdings remain preserved; no gap is bridged.
- **E-008/E-009:** `Risk_Data_Hash` remains required for the exact common complete risk
  panel. It is distinct from the five proposed identifiers.
- **E-010:** the 60/252 minimum *risk-estimation* windows are not performance
  annualization rules. The proposed 252-session annualization factor/floor is a separate
  E-004 proposal.
- **E-011:** insufficient segment length or missing required inputs yields unavailable
  metrics, not filled data, substituted dates, or fallback values.
- **E-027/E-028:** annualization uses the already specified net equity series after the
  approved fill-price and transaction-fee sequence. Snapshot identifiers document the
  existing execution/allocation contract; they do not alter its behavior.

No contradiction was found. The unresolved dependencies are explicit: the official
session calendar is not present; historical segment metric formulas are not linked to
the archive; and archived run/snapshot provenance is not established.

## Explicit researcher approval questions

1. **E-004:** Approve Option B with 252 verified-session intervals per nominal year,
   annualized reporting floor of 252 valid return intervals, and the metric-specific
   formulas and limitations in the analysis? If not, choose Option A or Option C and
   specify any different thresholds/inputs.
2. **E-004 parameters:** Confirm that annualized Sharpe/Sortino remain unavailable
   until risk-free/MAR definitions are separately approved; confirm that maximum
   drawdown remains unannualized and Calmar uses segment CAGR divided by absolute
   segment maximum drawdown.
3. **E-029:** Approve Option B's five distinct run/snapshot lineage references, required
   in the run manifest rather than as five new optimizer arguments? If not, choose
   Option A or Option C and specify which fields are mandatory.
4. **E-029 implementation boundary:** Confirm that existing `Risk_Data_Hash` remains
   separately required, that no identifier is inferred for archived runs, and that
   missing/inconsistent future lineage is reported as incomplete rather than silently
   substituted.

No response is presumed. Both decisions remain pending until the researcher explicitly
records a decision in the canonical Phase E register.

Reviewed source paths and hashes are recorded in
[source_evidence_inventory.csv](./source_evidence_inventory.csv). The canonical status
source remains the [Phase E decision register](../phase_E_portfolio_specification/phase_E_decision_register.csv).
