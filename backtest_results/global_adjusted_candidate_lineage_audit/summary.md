# Summary: GLOBAL adjusted candidate lineage audit

**Exact candidate use is confirmed for Notebook 05 diagnostics, not confirmed for portfolio/backtest results. An archived result package exists; its exact lineage to the candidate is unknown.**

| Area | Finding |
|---|---|
| Candidate | Derived from original snapshot; GLOBAL OHLC before 2026-02-24 multiplied by 28/27; 36 rows reported changed; not exchange-verified. |
| Notebook 05 | Loaded for eligibility/return diagnostics and execution diagnostics. |
| Features/model | No direct candidate path identified; complete indirect exclusion not proven due missing hash chains. |
| Notebook 06 | Inspected saved input loads original snapshot, not corrected candidate. |
| Archived results | 63 performance-summary pairs exist. Manifest says adjusted Master OHLC; exact input hashes are absent. Candidate link is `UNKNOWN_INSUFFICIENT_EVIDENCE`. |
| Current saved run | No new result files; Notebook 05 output says 63 experiments skipped. |

Archived files: performance summary 63 rows; daily portfolio 13167; transactions 3125; valuation 67633; predictions 654381. GLOBAL rows in archived predictions/valuation/transactions: 0/0/0.

`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`

No market data was downloaded; no yfinance call, notebook/pipeline execution, model training, prediction generation, or backtest/63-combination run occurred during this audit. Existing archived results are disclosed and were not regenerated. Candidate correctness remains unresolved.
