# Daily Equity, Cash, and Valuation Audit

## Archived structure and direct reconciliation

The archive contains 13,167 daily rows: 63 pairs × 209 dates. Stored dates cover execution dates 2026-01-06 through 2026-11-13 and decision dates 2026-01-05 through 2026-11-12. The daily schema includes Cash, Market_Value, Portfolio_Value, Holdings_Count, Stale_Holdings_Count, and Max_Stale_Calendar_Days; it has no return or initial-equity column.

Read-only checks on existing records found:

- `Portfolio_Value = Cash + Market_Value` for every daily row.
- Daily Market_Value equals the sum of recorded valuation `Market_Value` rows for the same pair/date.
- Each valuation-row Market_Value equals Shares × Valuation_Price.
- Daily Holdings_Count equals the number of valuation rows for that pair/date.
- Daily stale-holding count and maximum stale age agree with the corresponding valuation records.

All comparisons were exact within a small floating-point tolerance. These checks verify consistency among stored fields, not the validity of the source prices or the method that generated the records.

## Cash and holdings

Thirty-five pairs have transactions and recorded positions; 28 pairs have zero holdings and no transactions for all 209 dates. For those 28, archived Cash and Portfolio_Value are both $1,000,000 on every date and Market_Value is zero. This demonstrates that the stored daily equity includes cash for the all-cash cases. It does not establish the starting-equity denominator used by the metric calculation.

For active pairs, cash is present as a daily balance and is included in the observed Portfolio_Value identity. Transactions contain separate Gross and Cost fields, but there is no cash-before/cash-after value per fill. Initial cash and cash-flow lineage are not archived, so historical deduction of each buy cost or netting of sell proceeds cannot be independently confirmed from those records alone.

## Valuation coverage and stale marks

There are 67,633 position-valuation rows across the 35 pairs with holdings. Their row counts reconcile to daily holdings counts; the other 28 pairs have no position-valuation rows. Stale values are carried in the valuation rows and summed into daily Market_Value. See [stale valuation and missing price audit](./stale_valuation_and_missing_price_audit.md) for the BANPU findings.

The archive manifest says adjusted Master OHLC was used for execution, but does not identify the exact path or hash. The archive has no valuation-source ID or metric-input hash. Thus the retained daily equity is internally consistent but not source-verified.

## Status

`Daily accounting-field consistency = VERIFIED` for archived rows.  
`Cash flow and fee application = UNKNOWN_INSUFFICIENT_EVIDENCE`.  
`Historical equity/metric source lineage = UNKNOWN_INSUFFICIENT_EVIDENCE`.
