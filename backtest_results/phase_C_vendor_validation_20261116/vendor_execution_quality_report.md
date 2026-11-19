# Vendor Execution Quality — Phase C

## Scope and vendor status

- Provider: Yahoo Finance through the existing `yfinance.download` snapshot. This is accepted as third-party research data under Approach B; it is not official or exchange-authorized SET execution data.
- Snapshot SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`. No Yahoo download or price replacement was performed in Phase C.
- Coverage: 17,430 Date-Symbol rows, 83 symbols, 210 observed dates (2026-01-05 to 2026-11-13).

## Data quality

- Duplicate Date-Symbol records: 0.
- Missing OHLC field-cells: {'Open': 63, 'High': 63, 'Low': 63, 'Close': 64}; total 253. All missing fields are on BANPU across 64 rows.
- Non-positive/non-finite complete OHLC rows or OHLC boundary violations: 0.
- Volume missing / zero / negative rows: 62 / 30 / 0. Zero volume is not treated as proof of suspension or non-trading.
- Repeated consecutive observed Close values: 3070. This is a diagnostic only; repeated prices do not establish staleness.
- Vendor-reported action fields: 137 nonzero Dividends/Stock Splits rows across 76 symbols. These are vendor records, not official confirmations.
- Existing price-basis diagnostic: 141 anomaly field-rows, all for GLOBAL. GLOBAL remains excluded; no split is asserted from tick alignment.

## Eligible candidate sample check

- AOT's four candidate execution records have valid Open, Close, OHLC boundaries, and positive Volume: True.
- Predictor dates are aligned to the next date observed in the pinned vendor snapshot, not to an invented weekday calendar. The final observed predictor date has no next observed execution date.
- Candidate rows and record-level diagnostics are in `vendor_execution_quality_2026.csv`; no price was imputed or carried forward.

## Decision

The broad snapshot remains quality-limited because BANPU has 253 missing OHLC cells, volume has missing/zero rows, GLOBAL has unresolved basis anomalies, and the Yahoo date calendar is not an official SET calendar. These issues are bounded away from the four AOT candidate rows by the exclusion and date-scoped feature rules, but do not approve the Research Backtest Gate. Board-lot and stale valuation policies remain unresolved and no portfolio valuation was run.
