# Corporate Action and Security Identity Recovery — Phase B

## Result

- Original ledger rows inspected: 141; rows individually classified `UNRESOLVED`: 141.
- Original event symbols: 77; symbols intersecting the union of the local 2026_H1/H2 constituent files: 52.
- Ledger rows whose symbols appear in that local 2026 membership union: 97.
- Official source URLs recorded in the ledger: 0; locally available official event documents: 0.
- Portfolio-engine applications recorded: 0.
- Event types recorded (not independently confirmed): `{"CASH_DIVIDEND": 137, "MERGER": 2, "SPLIT": 1, "STOCK_DIVIDEND+CASH_DIVIDEND": 1}`.

## 53-symbol count reconciliation

Phase A reported 53 unresolved, non-excluded 2026 member symbols. The local membership files contain 54 distinct symbols across 2026_H1 and 2026_H2; after the existing BANPU exclusion, 53 remain. The ledger contains events for 52 symbols in that 54-symbol union (including excluded BANPU); 2 symbols have no ledger row: AOT, BTS. Thus the Phase A count of 53 is a universe-wide unresolved-status count, not 53 event-bearing symbols in the ledger. The local ledger supports 52 overlapping event symbols, and does not provide official negative confirmation for the symbols with no event row.

## Evidence and treatment

- The ledger's `Official_Source` field is blank for every row. The 136 vendor-origin records cite Yahoo Finance/yfinance in their notes; the five claim records do not attach a publisher URL or document.
- The candidate `Event_Type`, `Date`, security identifiers, ex/record/payment/trading/effective dates, cash amounts and ratios are reproduced from the ledger. They are not promoted to confirmed events.
- No price or quantity adjustment was applied. A price discontinuity or diagnostic factor is not treated as proof of a split.
- Event rows that overlap the local 2026 member set remain blocked for eligibility review; this does not assert membership was officially verified.
- No external sources were fetched or downloaded, per the preservation rule. Official event notices and security-identity evidence remain required.

## Identity findings

The local identity mapping contains 5 rows; status counts are `{"BLOCKED_SOURCE_URL_REQUIRED": 4, "BLOCKED_SOURCE_URL_AND_FEATURE_REBUILD_REQUIRED": 1}`. The mapping has no attached official URLs. BANPU/BPP identity, merger terms, fractional-share treatment, and post-event feature identity remain unresolved. Absence of an identity-mapping row for other symbols is not proof that no identity transition occurred.

## Output

`corporate_action_evidence_recovery.csv` preserves all 141 ledger rows and adds candidate membership context, source publisher, evidence URL, classification, rationale, and eligibility impact. Source ledger SHA-256: `613848ab5bd075654995b42515dc140a943eccc3e1fac9ddd84b2f192e1f1ee5`.
