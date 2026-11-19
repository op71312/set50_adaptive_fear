# Notebook 08 Provenance Investigation — Read-only

**Run ID:** `RPR-829A43493C6B4CADACEC3ED50621C407`

## 1. Executive Summary

**Overall finding: `NO_MATCH_FOUND` in the repository files, local Git history/object database, and repository archives searched.**

The run and reconciliation manifests record Notebook 08 SHA-256 `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081`. The only in-repository Notebook 08 source file found is the current runner, whose SHA-256 is `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8`.

The local Git repository has only its initial commit, whose tree does not contain the runner. A complete raw-content SHA-256 scan of all 719 local Git blob objects found no expected-hash match. Besides an unreachable blob identical to the current notebook, three additional unreachable Git blobs contain Notebook 08-like content, but their hashes differ and they have no path or commit association. They cannot be treated as the run's source.

The run manifest records the expected Notebook 08 hash but no source path or archived/executed notebook. The run's `SHA256SUMS.txt` checksums cover output artifacts, not the source Notebook 08. Thus, the exact file path and reason for the mismatch remain **NOT_VERIFIABLE** from repository evidence. No substitute source was selected.

## 2. Expected vs Current Hash

| Item | SHA-256 | File facts |
|---|---|---|
| Expected, as recorded in `run_manifest.json` line 12 and `reconciliation_manifest.json` line 15 | `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081` | 64-character digest; manifest does not record a source path |
| Current `D:\Project_Github\set_fear_index\08_set50_real_data_backtest_runner.ipynb` | `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8` | 96,445 bytes; last modified 2026-11-18 13:27:54 local |

The hashes differ. The current file is **not** an exact-hash match for the source hash recorded by the run.

## 3. Repository Search Results

Searched repository `.ipynb` files and likely Notebook 08 backup filenames, excluding `.git`, `.venv`, `node_modules`, and `__pycache__` from the filesystem notebook inventory. Eleven notebook files were found and hashed:

| Repository file | Bytes | SHA-256 |
|---|---:|---|
| `D:\Project_Github\set_fear_index\01_dataset.ipynb` | 75,060 | `c53b4869ca97b95d6c7c9c493d695e5d07a5a8231c78d4efed8146b7506b0031` |
| `D:\Project_Github\set_fear_index\02_eda_parquet.ipynb` | 259,882 | `2b55addc8e497ab2339c8124a06d8fe51cb13218a3d17f288de409340009c3c3` |
| `D:\Project_Github\set_fear_index\03_feature_engineering.ipynb` | 756,442 | `f1fee7bf11ea2796464b7540ff23b121af13d2ba884a6b01cc426b85180592b9` |
| `D:\Project_Github\set_fear_index\04_model.ipynb` | 224,668 | `1cfb1c83c9b4bcc317d7605c1d717e3e16bc5525aea644f0f38ce2e2a8320782` |
| `D:\Project_Github\set_fear_index\05_backtest.ipynb` | 155,366 | `1b2c5339244106942202dd7065589cdba2ed2a042732e621572be73d4b6343fb` |
| `D:\Project_Github\set_fear_index\06_research_backtest.ipynb` | 139,073 | `4b390d06306f74bd9360768fa2ce9ac86a86429fcf6cac66f1bc7800748a1a1c` |
| `D:\Project_Github\set_fear_index\07_dynamic_universe_portfolio_backtest_v2_corrected.ipynb` | 225,057 | `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070` |
| `D:\Project_Github\set_fear_index\08_set50_real_data_backtest_runner.ipynb` | 96,445 | `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8` |
| `D:\Project_Github\set_fear_index\backtest_results\notebook_07_clean_implementation\07_dynamic_universe_portfolio_backtest.ipynb` | 171,308 | `5749c8acc48e21fe1463edffa437d72ef8a453c1820c7bc9ff4f99558fb9f595` |
| `D:\Project_Github\set_fear_index\backtest_results\notebook_07_clean_implementation\07_dynamic_universe_portfolio_backtest_v2.ipynb` | 196,063 | `668a89e524dd9bba7fec1f52b3c25c9a3050862fe8875eae859f6a2fedaf7bbc` |
| `D:\Project_Github\set_fear_index\backtest_results\notebook_07_clean_implementation\07_dynamic_universe_portfolio_backtest_v2_execution_verified.ipynb` | 222,526 | `7c0083bdbb5e88adf205c570528380282ca67abcc69315e405eaf8d13a7c18fa` |

No file in this inventory matches the expected hash. No `08_set50_backtest_experiment_runner.ipynb` or filename-pattern Notebook 08 backup was found. A repository content search for `proxy_execute_orders` and the Notebook 08 research-runner heading returned only the current Notebook 08, not another source copy.

The requested run directory contains result CSV/Markdown artifacts and manifests, but no Notebook 08 execution copy. No file in the run tree has a Notebook 08/execution-copy filename.

## 4. Git History Results

- Local Git top-level: `D:\Project_Github\set_fear_index`.
- Branches: `main` only.
- Tags: none.
- Reachable history: one commit, `d5264152453bef4c9b56c9e56922204c7b99a75c` (`Initial commit`, 2026-11-07).
- The `HEAD` tree contains only `.gitattributes` and `README.md`; it contains no Notebook 08 path.
- `git log --all --full-history` for likely Notebook 08/runner paths returned no entries. The reflogs contain only the initial commit on `main` and `HEAD`.

`git fsck` reported 717 unreachable blobs and no unreachable commit/tree path for a Notebook 08 history. All 719 blobs in the local Git object database were read as raw blob contents and SHA-256 hashed; none matched the expected digest.

The local object database also contains an unreachable blob whose raw content hash equals the **current** Notebook 08 file. It is not an alternate source and does not match the run:

| Git object path (object only; not a source path) | Raw content SHA-256 | Finding |
|---|---|---|
| `D:\Project_Github\set_fear_index\.git\objects\8d\a2cf1a6063c411afa2335d64d31142f27c75f8` (blob `8da2cf1a6063c411afa2335d64d31142f27c75f8`) | `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8` | Exact copy of current worktree notebook content; not the expected digest |

Three additional unreachable blobs have Notebook 08-like titles/signatures, but are not attached to any commit or source path:

| Git object path (object only; not a source path) | Raw content SHA-256 | Size | Notebook shape |
|---|---|---:|---|
| `D:\Project_Github\set_fear_index\.git\objects\48\a4114542d2400a6a4ed08fa85416e2a016e188` (blob `48a4114542d2400a6a4ed08fa85416e2a016e188`) | `5299b04c7492e17ac1ac950c5a3433ce84c98d22436627bc3adcea1e45f7b522` | 96,275 | 14 cells, 7 code cells |
| `D:\Project_Github\set_fear_index\.git\objects\74\a7563e6d9ab0d3ece59482155c7f6b23445342` (blob `74a7563e6d9ab0d3ece59482155c7f6b23445342`) | `b0d043d10a058bb2ae738bd74cebe07595365b194513ee79204ee339f02b4040` | 96,187 | 14 cells, 7 code cells |
| `D:\Project_Github\set_fear_index\.git\objects\dc\768c25203c05b5572ace63892da8044ec80533` (blob `dc768c25203c05b5572ace63892da8044ec80533`) | `7d4ddfa503f2181879157ae15d5139474ba257b0ab529d8740f78456a472f2a4` | 30,647 | 13 cells, 6 code cells |

These are not hash matches. Their Git object IDs identify content only; they do not establish original filenames, commit history, or use in this run.

**Git classification: `NO_MATCH_FOUND`.** A run-like unreferenced blob is not evidence that it is the run's source.

## 5. Backup and Archive Results

Inspected the three repository directories whose names indicate archived audits:

- `D:\Project_Github\set_fear_index\backtest_results\archived_backtest_lineage_audit`
- `D:\Project_Github\set_fear_index\backtest_results\archived_risk_allocation_lineage_audit`
- `D:\Project_Github\set_fear_index\backtest_results\archived_performance_methodology_audit`

Together these contain 28 files: 8 CSV, 19 Markdown, and 1 JSON. No Notebook 08 notebook, backup-extension file, or archive container was present. A wider repository filename search also found no Notebook 08 backup copy.

**Backup/archive classification: `NO_MATCH_FOUND`.** These audit archives contain reports/evidence, not a matching Notebook 08 source.

## 6. Exact Hash Match Findings

| Search area | Result |
|---|---|
| Repository Notebook 08 files and likely named backups | `NO_MATCH_FOUND` |
| Run output directory execution/notebook copies | `NO_MATCH_FOUND` |
| Reachable local Git history, branches, tags, reflogs | `NO_MATCH_FOUND` |
| All local Git blob contents, including unreachable blobs | `NO_MATCH_FOUND` |
| Repository backup/archive directories | `NO_MATCH_FOUND` |

The expected digest occurs in metadata/report text, not in a matching Notebook 08 file:

- `run_manifest.json` line 12 records `Notebook_08_SHA256`; it records no Notebook 08 source path.
- `reconciliation_manifest.json` line 15 repeats the same value.
- `TARGETED_RECONCILIATION_REPORT.md` and the earlier implementation review report repeat the manifest value.
- The run's `SHA256SUMS.txt` lists checksums for exported run outputs (including `run_manifest.json`) and has no Notebook 08 source-file entry.

**Overall classification: `NO_MATCH_FOUND`.** No path can be supplied for the expected-hash file because none was found. No alternative file is designated as the original.

## 7. Notebook Source Comparison

No file with the expected SHA-256 was found; therefore the requested exact-source comparison is **not applicable**. No cell-by-cell or code/markdown diff was used to infer which version produced the run.

Current Notebook 08 facts, collected without executing it:

- SHA-256: `b76c97b7b37f4035b754ceb90f2f9ea88c2d5c40955b7d8ba19cf432873e63a8`.
- Cell count: 14 total, 7 code cells.
- All 7 code-cell `execution_count` fields are null.
- Notebook metadata says `execution_mode = REAL_DATA_READINESS_ONLY`, `executed_at_local = 2026-11-18T11:27:11.035774+07:00`, and `kernel = fresh ipykernel`; this metadata does not identify the target Run ID.

The three unreferenced Notebook 08-like Git blobs listed above have different hashes and are not source comparisons for the target run. Their existence does not establish whether source differences would affect run results.

## 8. Provenance Conclusion

The manifests establish that the run was recorded with Notebook 08 hash `5b375e7a9b5ace41c4eb95919d7a6dfe881833fa1bf193983a9e3afc5533d081`, but do not identify the source path or preserve a matching notebook execution copy. The current Notebook 08 file and all other repository files/objects searched have different content hashes.

Accordingly:

- Whether the current Notebook 08 source is identical to the run source: **NOT_VERIFIABLE**.
- The path of the source file whose hash was recorded: **NOT_VERIFIABLE**.
- The cause or effect of the source mismatch: **NOT_VERIFIABLE**.
- An exact local repository, Git-history, or archive match: **NO_MATCH_FOUND**.

The read-only repository search is complete within the stated scope. No external service, external backup, or out-of-repository attachment was searched.

## 9. Recommended Next Steps

1. Keep this run's source attribution **NOT_VERIFIABLE** unless an authorized retained source copy can be provided and its raw SHA-256 equals the manifest value.
2. Do not substitute the current Notebook 08 or any similarly named/unreachable Git blob for the expected-hash source.
3. If an exact local run-time source copy becomes available, first hash it, then compare cell count/order, source cells, functions, configuration, execution, transaction, valuation, and export logic against the current notebook without executing either one.
4. For future runs, retain the exact Notebook 08 source beside the run outputs and record its full relative path, hash, and execution-copy hash in the manifest and checksum list.

## 10. Confirmation of Read-only Compliance

- No notebook was edited, executed, or restored from a Git object.
- No backtest, model inference, download, external API call, checkout, reset, cherry-pick, or Git state change was performed.
- Manifests, checksum lists, source datasets, model, prior run outputs, and gate/blocker statuses were not modified.
- The only deliverable created for this investigation is this report.

Gate statuses remain unchanged:

- `RESEARCH_BACKTEST_GATE = CONDITIONAL_OPEN`
- `EXECUTION_VALIDATION_GATE = BLOCKED`
- `Canonical_Historical_Gate = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`
