# Notebook 08 Research Proxy Run Summary

- Run ID: `RPR2-34A9F42873AF435F85F143BBF33AB1E1`
- Run-level research gate: `CONDITIONAL_OPEN`
- Execution validation gate: `BLOCKED`
- Canonical historical gate: `BLOCKED` (unchanged)
- Phase F: `DO_NOT_BEGIN`
- Research universe: 53 union symbols; active H1/H2 sizes {'2026_H1': 49, '2026_H2': 49}
- Excluded symbols: BANPU, GLOBAL
- Observed vendor sessions: 210 (2026-01-05 through 2026-11-13)
- Prediction rows: 7301; non-finite rows rejected before inference: 0
- Combination records: 63; statuses: `{'COMPLETED_WITH_LIMITATIONS': 63}`
- Synthetic regression tests: 21; statuses: `{'PASS': 21}`
- Action log rows: 460045; position valuation rows include Strategy_ID and Allocation_Method.
- Filled transactions: 6,901; fees: 333,736.72; slippage: 198,630.66; total transaction cost: 532,367.38.
- Across combinations, PRICE_RETURN ranged from 0.00% to 23.89%; maximum drawdown ranged from -8.39% to 0.00%.
- Stale valuation count: 0 in all 63 combinations. CVaR audit: 539 valid windows (61-209 observations) and 2 dates not evaluated because no eligible buys existed.
- S5/S6/S8/S9 each retained all-cash accounting with zero transactions.
- Allocation failures retain cash and are counted; no alternate method is substituted.
- Metrics are unannualized PRICE_RETURN. No CAGR, Sharpe, Sortino, or Total Shareholder Return is claimed; unverified distributions/actions are not applied.
- Fills are theoretical fractional-share simulations using vendor raw Open, not exchange fills.
- Notebook 07 and protected source files were hash-checked before and after the run.

See `combination_status_63.csv` for every strategy/method record.
