# Workstream 1.9.1 Validation Report

## Output location

The existing Workstream 1.9 folder is
`backtest_results\research_backtest_readiness_workstream_1_9`. The proposed
`backtest_results\research_backtest_readiness\workstream_1_9_1` parent does not
exist. To preserve the established sibling naming pattern and avoid modifying
Workstream 1.9, these deliverables are in:

`D:\Project_Github\set_fear_index\backtest_results\research_backtest_readiness_workstream_1_9_1\`

## Task results

| Task | Result | Evidence / limitation |
|---|---|---|
| A — Execution Snapshot SHA-256 | `PASS` | SHA-256 computed from the actual 324,428-byte Execution Snapshot Parquet is `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`. The competing `...19e66e...` value does not match and was not found in repository text search. |
| B — Evidence Inventory identity | `PASS_WITH_LIMITATIONS` | EVI-052 is the Execution Snapshot and matches its actual hash. EVI-051 is the sidecar JSON, a distinct file. EVI-053 is the Master Dataset; equivalence to a separately named Feature Snapshot is `IDENTITY_UNRESOLVED`. |
| C — Approach B wording | `PASS_WITH_LIMITATIONS` | Corrected copy permits Yahoo/yfinance vendor-based prices and removes official SET execution prints as a mandatory source. Request parameters, data-quality, identity/action, calendar, and lineage blockers remain. |
| D — Dependency graph | `PASS_WITH_LIMITATIONS` | Revised copy treats security identity and corporate-action evidence as parallel and mutually informative inputs to a joint mapping. This is a conceptual clarification, not a status or register change. |
| E — Decision/scope integrity | `PASS` | Required decision statuses were read from the canonical register and W1.8 validation source; no canonical decision register or prior deliverable was modified. |
| F — Deliverables/checksums | `PASS` | Six non-checksum deliverables were hashed; all six entries in the generated checksum file independently verify. |

## Hash and identity findings

- Full source path:
  `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet`
- Size: 324,428 bytes.
- File-system last-modified time: `2026-11-15T11:37:12.0000000Z`.
- Actual SHA-256:
  `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
- The sidecar's retrieval timestamp is `2026-11-15T11:37:11.389684+00:00`;
  it does not contain a Parquet hash. The separate execution lineage file and
  Phase C provenance report contain the actual matching hash.
- Workstream 1.9 `SHA256SUMS.txt` contains hashes of Workstream deliverables,
  not a direct Execution Snapshot hash. Its checksum for the Evidence Inventory
  matches the inventory file containing EVI-052.
- No local text match for the competing `...19e66e...` value was found. No
  evidence supports assigning that value to a Feature Snapshot.
- Phase C describes feature acquisition as separate from execution acquisition.
  The local Master Dataset hash verifies that named file, but no complete
  manifest ties it to a separately identified Feature Snapshot. That identity
  remains unresolved.

## Protected-file integrity

Before creating this output folder, SHA-256 baselines were captured for 15
relevant protected source/report files, including the actual Execution Snapshot,
sidecar, immutable copy, execution lineage/status, Phase C provenance, Workstream
1.9 inventory/report/checksum/roadmap/graph, and canonical decision sources.
The output directory did not exist at that time. Post-generation comparison
confirmed all 15 protected-file hashes are unchanged. The new output folder
contains exactly the six requested non-checksum deliverables plus
`SHA256SUMS.txt`; no other file was created there.

Existing repository Git status already contained unrelated untracked and deleted
entries. No cleanup or reversal of pre-existing state was attempted.

## Prohibited-action verification

- No Internet, download, yfinance call, or external API was used.
- No Execution Snapshot, sidecar, feature/master dataset, model, prediction,
  notebook, corporate-action ledger, archive, or canonical decision register was
  modified.
- No model fit/retraining, prediction, optimization, allocation, or backtest was
  run.
- No gate override or Phase F action occurred.

## Remaining blockers and final status

Vendor source selection under Approach B is accepted, but this does not clear
unknown request parameters, missing OHLC, GLOBAL price-basis anomalies,
corporate-action/security identity, verified-session calendar, universe,
model/archive lineage, risk panels, board-lot policy, or implementation/method
validation. E-004/E-029 approvals remain specification-only; `Risk_Data_Hash`
remains required.

`RESEARCH_BACKTEST_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`
