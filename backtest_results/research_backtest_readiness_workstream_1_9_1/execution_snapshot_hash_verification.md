# Workstream 1.9.1 — Execution Snapshot Hash Verification

## Result

**Execution Snapshot SHA-256 verified from file bytes:**

`14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`

The value ending `...19e66e4d9...` does **not** match the file. The actual
Execution Snapshot matches the value ending `...19a66e4d9...`. The competing
value supplied in the task was not found in the repository text search and is
not attributed to another artifact.

## Actual file identity and metadata

| Property | Verified value |
|---|---|
| Full path | `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet` |
| Artifact identity | Execution OHLCV vendor snapshot (Parquet) |
| File size | 324,428 bytes |
| Last modified (UTC) | 2026-11-15T11:37:12.0000000Z |
| SHA-256 computed from file bytes | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` |
| Sidecar download timestamp (UTC) | 2026-11-15T11:37:11.389684+00:00 |
| Sidecar identity | `SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json` |

File-system modification time and sidecar retrieval time are separate
timestamps. The sidecar identifies Yahoo Finance via yfinance 1.8.0,
`auto_adjust=false`, `actions=true`, the requested date range, 83 requested and
returned symbols, and 17,430 rows. It does not itself contain a SHA-256 field
for the Parquet file.

## Hash comparison

| Reference | Hash/value present | Comparison with actual bytes | Interpretation |
|---|---|---|---|
| Actual Execution Snapshot Parquet | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Exact match | Computed with SHA-256 over the named file. |
| Competing value supplied in the task | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19e66e4d9c51ef986a` | **Mismatch** | Not found in local repository text search; no evidence attributes it to a Feature Snapshot. |
| Workstream 1.9 Evidence Inventory, EVI-052 | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Exact match | EVI-052 path names the Execution Snapshot Parquet. |
| Workstream 1.9 Validation Report | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Exact match | Reports the Execution Snapshot hash. |
| Workstream 1.9 `SHA256SUMS.txt` | No direct Execution Snapshot hash entry | Not applicable | It hashes the six Workstream 1.9 deliverable files, not the underlying dataset. Its EVI inventory entry (`63c05e0d270ec863e66e4ac197bf70d593b20a72975ccba7beffe4da99c30303`) protects the file containing EVI-052. |
| Phase C `vendor_provenance_report.md` | `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a` | Exact match | Explicitly labels this as the snapshot hash. |
| `backtest_results\execution_data_lineage.json` | Same correct value in original snapshot lineage | Exact match | The embedded original snapshot path is the same Parquet path. |
| Workstream 1 / Phase B lineage and prior audit records | Same correct value in pinned/original/copy checks | Exact match in inspected references | The immutable execution copy was independently rehashed and matches. |
| Execution sidecar JSON itself | Its own file hash is `0b02751e384a678a441ba1c86e9c33123cd3deb574d4cbdab77ecdf00de6e7e9` | Different file, expected | This is the sidecar's hash, not the Parquet snapshot hash; the sidecar has no Parquet hash field. |

## Source identity versus Feature Snapshot

- **EVI-052 is verified as the Execution Snapshot.** Its source path ends in
  `SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`, and the
  computed hash matches the lineage and Phase C report.
- **EVI-053 is the Master Dataset Parquet**, at
  `dataset\verified_build_20261113_152948\SET50_Master_Dataset.parquet`, with
  SHA-256 `ef060baedd779a99b83a7cfa74b4bde20eb7bcf30fc1c05679f11b3c8c459f07`.
  That path is not a separately identified artifact named “Feature Snapshot.”
- Phase C describes feature acquisition as a separate path from execution and
  says the available source code does not provide a complete manifest tying a
  particular feature acquisition run to the pinned Master Dataset hash. The
  Feature Snapshot identity therefore remains `IDENTITY_UNRESOLVED`; neither
  supplied Execution Snapshot hash is assigned to it.
- The lineage report's `4d35f215...` hash identifies a separate derived
  corrected execution candidate, not the source Execution Snapshot or a Feature
  Snapshot.

## Discrepancy disposition

The Execution Snapshot discrepancy is **resolved by direct file hashing**: the
first value matches, the second does not. No source Parquet, sidecar, inventory,
or prior Workstream 1.9 file was changed. The unresolved issue is the identity
and lineage of any separately intended “Feature Snapshot”; existing evidence
does not identify one with the competing value.

### Evidence references

- `dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`
- `dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json`
- `backtest_results\execution_data_lineage.json`
- `backtest_results\execution_data_v2\execution_ohlcv_original.parquet`
- `backtest_results\phase_C_vendor_validation_20261116\vendor_provenance_report.md`
- `backtest_results\research_backtest_readiness_workstream_1_9\evidence_inventory_and_reuse.csv`
- `backtest_results\research_backtest_readiness_workstream_1_9\workstream_1_9_validation_report.md`
- `backtest_results\research_backtest_readiness_workstream_1_9\SHA256SUMS.txt`
