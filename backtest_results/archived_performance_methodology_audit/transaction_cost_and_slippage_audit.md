# Transaction Cost and Slippage Audit

## Archived transaction evidence

The archived `transactions.csv` contains 3,125 records: 2,247 BUY and 878 SELL. Its schema has one `Price`, `Gross`, and `Cost` field per transaction; it has no separate fee, slippage, raw Open, adjusted fill price, or cash-before/cash-after columns.

For every recorded transaction, `Gross = Shares × Price` and `Cost / Gross = 0.0026799` within floating-point precision. This is numerically equal to the later assumptions combined: fee 0.0016799 plus slippage 0.001 per side. The output therefore supports a recorded combined cost ratio, but cannot decompose the amount into fee and slippage or establish whether the recorded Price already contains any slippage adjustment.

For the 35 pairs with transactions, the stored performance-summary Transaction_Count, Total_Transaction_Cost, and Total_Turnover reconcile to the transaction rows. The 28 no-transaction pairs have blank summary fields rather than explicit zeros. Daily cash is present, but the archive does not retain per-fill cash balances or an initial-cash/run configuration to reconcile individual cash movements.

## Historical application status

| Question | Finding | Evidence classification |
|---|---|---|
| Cost separate from Gross? | Yes; distinct `Cost` and `Gross` columns. | `HASH_VERIFIED` |
| Recorded BUY cost ratio? | 0.0026799 for all 2,247 BUY records. | `DERIVATION_CONFIRMED` |
| Recorded SELL cost ratio? | 0.0026799 for all 878 SELL records. | `DERIVATION_CONFIRMED` |
| Matches later combined assumptions? | Numerically matches 0.0016799 + 0.001. This is not proof of those individual settings. | `DERIVATION_CONFIRMED` |
| BUY costs deducted from cash? | Current Notebook 05 code subtracts Gross + Cost; no archived cash-flow trace links that code to these records. | `STATIC_CODE_REFERENCE_ONLY` |
| SELL costs deducted from proceeds? | Current Notebook 05 code adds Gross − Cost; no archived cash-flow trace links that code to these records. | `STATIC_CODE_REFERENCE_ONLY` |
| Slippage applied once or twice? | Unknown; there is no raw/fill price decomposition or linked historical configuration. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Same setting for all 63 pairs? | Recorded per-transaction ratio is uniform for all transaction rows; 28 pairs have no transactions. Historical configuration identity is absent. | `DERIVATION_CONFIRMED` for recorded ratios |

## Code and price-source limits

Current Notebook 05 cells around the order-sizing helpers (execution count 147) set BUY_COST_RATE and SELL_COST_RATE to 0.0016799 and SLIPPAGE_RATE to 0.001, and define the recorded Cost as Gross × (fee + slippage). Current execution code applies cost to the cash balance. This is a static code reference only.

The archive manifest says adjusted Master OHLC was used as execution prices but provides no exact source path/hash. The archive does not document whether its single Price field is a raw Open, adjusted Open, or slippage-adjusted fill. Therefore the exact historical fee policy, slippage treatment, and cash reconciliation remain unverified. No cost or performance values were altered.
