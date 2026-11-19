# Corporate Action Relevance — Phase C

## Inventory result

- Inspected all 141 local ledger rows (136 vendor action records plus 5 user-provided claims).
- `Official_Source` is blank for all 141 ledger rows; none is confirmed or applied by the portfolio engine.
- Local event labels include {'CASH_DIVIDEND': 137, 'MERGER': 2, 'SPLIT': 1, 'STOCK_DIVIDEND+CASH_DIVIDEND': 1}; these labels are treated as claims, not confirmation of event terms.
- 2026 verified impact: 0. Historical verified impact: 0. Category C, outside the officially verified 2026 SET50 member union: 44. Category D unresolved member-overlap rows: 97.
- The 2026 member-overlap set contains 97 unresolved event rows across 52 symbols. AOT and BTS have no local ledger rows; the snapshot also has no nonzero Yahoo Dividends/Stock Splits for either.

## Impact handling

- Candidate cash entitlement, share-quantity, identity, feature-continuity, and execution-price effects are marked as potential only in `corporate_action_relevance_2026.csv`.
- Event-bearing member securities are excluded from the Phase C candidate universe for the 2026 period because the local event records have no verified terms and the engine rejects unverified actions. This does not alter historical membership or apply any event.
- Non-member events are categorized outside the 2026 eligible universe based on the SET H1/H2 2026 primary membership PDFs; the events themselves remain unverified.

No Yahoo data was downloaded to investigate events. Only already-local evidence was used.
