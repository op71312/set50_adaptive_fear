# Execution Source and Price Completeness Recovery — Phase B

## Provenance recovered from existing files

- Provider recorded: `Yahoo Finance via yfinance.download`; yfinance version `1.8.0`.
- Sidecar retrieval timestamp: `2026-11-15T11:37:11.389684+00:00` UTC.
- Requested range: `2026-01-05` through `2026-11-14` (end exclusive).
- `auto_adjust=False` and `actions=True` are recorded.
- Requested and returned ticker counts are `83` and `83`; the exact requested ticker list remains UNKNOWN.
- `interval` and `group_by` remain UNKNOWN in the lineage. No inference was made from the shape of the parquet.
- Original snapshot SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`; immutable copy SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`; pinned hash `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
- The snapshot and immutable copy are traceable as hash-identical local artifacts. A complete original request/response manifest and exchange-authorized execution source are not present.
- Yahoo data is not described as official SET execution data. `auto_adjust=False` alone does not establish an exchange-raw historical price basis.

## OHLC completeness

- Missing OHLC field-cells: 253; by field: `{"Open": 63, "High": 63, "Low": 63, "Close": 64}`.
- Rows with at least one missing OHLC field: 64; affected symbols: `BANPU`.
- Missing-field dates span 2026-08-13 through 2026-11-13; distinct dates with missing fields: 64.
- Volume observed on affected rows: `{nan: 62, 0.0: 1, 3288829.0: 1}`. This does not prove a holiday, suspension, or no-trading condition.
- Every missing item is listed at Date + Symbol + Field in `execution_price_completeness_audit.csv` and remains `UNRESOLVED`; no fill or price alteration was performed.
- Entirely absent expected market sessions cannot be identified without an official trading calendar. The local calendar file is absent.

## Price-basis diagnostics

The existing GLOBAL diagnostic contains 141 rows; the Phase A evidence reports zero official action confirmation. A pre-existing local SET cross-check records 4 recent dates (2026-11-10 to 2026-11-13) with OHLC matching on all four dates; Yahoo volume differs. The recorded SET historical-trading URL is retained in the provenance audit. This does not verify historical price basis, other symbols, or any corporate action. No split is asserted and no adjusted prices were used to repair this snapshot in Phase B.

## Output

`execution_source_provenance_audit.csv` records each known/unknown acquisition field and its source file. `execution_price_completeness_audit.csv` contains one row per missing OHLC field-cell. No source was fetched or downloaded during this audit.
