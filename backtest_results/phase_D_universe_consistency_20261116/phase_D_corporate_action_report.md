# Phase D Corporate-Action Scope

## Result

- Ledger rows inspected: 141.
- Recorded event-date range: 2026-02-23 to 2026-11-13. The recorded date is not assumed to be the effective date.
- Rows involving a symbol in the 2026 membership union: 97 across 52 symbols.
- Rows whose recorded event date falls inside that symbol's active 2026 membership period: 89 across 51 symbols.
- Additional union-overlap rows outside the symbol's active membership period on the recorded date: 8.
- Event labels: {"CASH_DIVIDEND": 137, "MERGER": 2, "SPLIT": 1, "STOCK_DIVIDEND+CASH_DIVIDEND": 1}.
- Rows with a populated official-source field: 0; rows with an evidence URL: 0.
- Confirmed terms or actions applied in Phase D: 0.
- All ledger rows remain `UNRESOLVED`; no action was applied and no source row was changed.

The local ledger's `Date`, event label, and any populated date/term fields are copied to
`phase_D_corporate_action_scope.csv`. Missing effective dates remain blank. A dividend,
split, merger, or stock-dividend label is recorded as a possible risk indicator only;
it is not proof that the described event occurred or that its terms are correct.

## Relevance

The 2026 membership-union rows could affect feature continuity or future execution
prices and, depending on verified terms, cash entitlements, share quantity, or identity.
Only the date-specific overlap is treated as potentially affecting a holding on the
recorded date. No event has evidence sufficient to confirm any impact. The 44 rows
outside the 2026 membership union do not concern current constituents; eight union
rows fall outside the affected symbol's active period on the recorded date. The four
AOT candidate dates have no local AOT ledger row. No corporate action was applied.

## Evidence still needed

For each event that may affect a 2026 member: a primary-source record of event terms,
effective/ex/record/payment dates as applicable, affected security identity, and
confirmation of the price/share/cash treatment. Do not use the diagnostic price
alignment or the ledger description as a substitute.
