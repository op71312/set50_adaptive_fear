# Execution Data Integrity Audit — Phase 1

- Audit ID: `execution_data_phase1_20261115T152933Z_64083a5d`
- Created UTC: `2026-11-15T15:29:33.301042+00:00`
- Final status: **BLOCKED**; no official row-level evidence resolves missing OHLC.
- No yfinance/Yahoo redownload, snapshot mutation, or price fill was performed.

## Snapshot hashes
- Pinned SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`
- Original Snapshot before/after: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` / `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` — match.
- Immutable Copy before/after: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` / `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` — match.

## Acquisition provenance
- Provider: Yahoo Finance via yfinance.download; yfinance 1.8.0; auto_adjust=False; actions=True.
- Period: 2026-01-05 to 2026-11-14 (end exclusive); 83 requested and 83 returned tickers.
- interval=UNKNOWN; group_by=UNKNOWN; requested_ticker_list=UNKNOWN — all **UNKNOWN**.
- Notebook 05 documents that the original download cell was absent. Feature-data notebook request settings were not inferred to be the execution snapshot settings.
- Inspected Git history: d526415 Initial commit.

## Missing OHLC census
| Field | Missing |
|---|---:|
| Open | 63 |
| High | 63 |
| Low | 63 |
| Close | 64 |

| Symbol | Missing |
|---|---:|
| BANPU | 253 |

- Total: **253** cells across 64 BANPU dates, 2026-08-13 to 2026-11-13.
- 63 dates have all four OHLC fields missing; 2026-11-13 has only Close missing.
- Candidate Volume states by date/symbol: `{'NULL_IN_CANDIDATE': 62, 'ZERO_IN_CANDIDATE': 1, 'POSITIVE_IN_CANDIDATE': 1}`. This is not official evidence of a no-trade day.

## Official evidence and classification
- Confirmed causes: **0**. Unresolved cells: **253**. All rows are `Unknown` / `UNRESOLVED`.
- No missing value is classified as holiday, no-trade, suspension, delisting, corporate action/identity transition, or vendor loss without date-specific evidence.
- [BANPU Historical Trading (SET)](https://www.set.or.th/en/market/product/stock/quote/BANPU/historical-trading) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. Returned "No information found" for default view; not date-specific evidence. **No rows resolved.**
- [BANPU Rights & Benefits (SET)](https://www.set.or.th/en/market/product/stock/quote/BANPU/rights-benefits) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. No date-specific 2026 corporate-action rows were found in the retrieved content. **No rows resolved.**
- [BANPU News (SET)](https://www.set.or.th/en/market/product/stock/quote/BANPU/news) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. No date-specific announcement resolving these missing rows was found. **No rows resolved.**
- [Trading Holidays (SET English)](https://www.set.or.th/en/market/information/trading-holidays) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. SET 404; no calendar conclusion drawn. **No rows resolved.**
- [Trading Holidays (SET Thai)](https://www.set.or.th/th/market/information/trading-holidays) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. SET 404; no calendar conclusion drawn. **No rows resolved.**
- [SET Homepage](https://www.set.or.th/en/home) — reviewed 2026-11-15T15:29:33.301042+00:00; effective date: not available. Current market summary only; no BANPU date-specific historical data or calendar. **No rows resolved.**
- Required but absent official inputs: SET_Execution_OHLCV_Source_Patch.csv, SET_trading_calendar_2026.csv, official_corporate_actions_2026.csv.

## Regression checks and gate
- Original Snapshot and immutable copy match the pinned hash before and after the audit.
- All 253 missing cells are listed by Date + Symbol + Field with source row index/hash, snapshot path/hash, prior audit path/hash, and official-source status.
- No values were filled or changed; no new Yahoo data was downloaded.
- Prior Research Backtest Gate open: `False`; 63 combinations executed: `False`.
- Phase 1 gate: **BLOCKED**. Stop before Phase 2 pending authoritative date-specific evidence.

## Output files
- [execution_missing_rows_detail.csv](./execution_missing_rows_detail.csv)
- [execution_missing_reconciliation.csv](./execution_missing_reconciliation.csv)
- [execution_provenance_findings.json](./execution_provenance_findings.json)
- [execution_data_phase1_report.md](./execution_data_phase1_report.md)
- [execution_data_phase1_gate.csv](./execution_data_phase1_gate.csv)
