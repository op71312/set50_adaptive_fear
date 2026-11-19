# Vendor Provenance Recovery — Phase C

## Existing execution snapshot

- Provider/library: `Yahoo Finance via yfinance.download`; yfinance `1.8.0`.
- Retrieval timestamp: `2026-11-15T11:37:11.389684+00:00`.
- Requested range: `2026-01-05` through `2026-11-14` (end exclusive).
- Requested ticker count: 83; exact requested ticker list: **UNKNOWN**. The observed output columns are not used to reconstruct that list.
- Settings verified from the sidecar: `auto_adjust=False`, `actions=True`.
- `interval` and `group_by`: **UNKNOWN** in the execution lineage. They are not inferred from the output shape.
- Snapshot SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`, matching both the immutable copy and Phase B's pinned hash.
- Source timezone: **UNKNOWN**. Stored Date values are timezone-naive; Notebook 06 normalizes parsed dates but does not establish source timezone.
- Price basis: Yahoo OHLC from an `auto_adjust=False` request, not official SET prints. The sidecar warns that historical split basis may still be adjusted; GLOBAL remains excluded due unresolved anomalies.

## Feature acquisition is a separate path

- Notebook 01 source code calls `yf.download(df['symbol'].tolist(), period='10y', interval='1d', auto_adjust=True, group_by='ticker')`.
- Notebook 03 also contains an executed dynamic-ticker downloader with `auto_adjust=True` and `group_by='ticker'`; its interval and actions argument are omitted.
- These are source-code facts, not a complete manifest tying a specific acquisition run to the pinned Master hash. The exact feature ticker list, run timestamp/library version, and whether actions were requested remain unknown.
- Therefore the feature source and execution snapshot are separate acquisition paths and use different adjustment settings; they are not the same OHLCV download.

See `vendor_provenance_recovery.csv` for each field's evidence class and path.
