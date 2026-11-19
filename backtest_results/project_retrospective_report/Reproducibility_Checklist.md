# Reproducibility Checklist

## Dataset and feature pipeline

| Check | Status | Evidence / limitation |
|---|---|---|
| Feature Master path, schema, row count, and current SHA-256 recorded | `PASS_WITH_LIMITATIONS` | RPR2 manifest records the feature SHA; exact training-time bytes are not separately linked to the frozen model. |
| Execution snapshot path/hash and 210 observed dates recorded | `PASS_WITH_LIMITATIONS` | SHA matches the local snapshot; vendor provenance is incomplete and calendar is not official SET. |
| 2026 H1/H2 membership evidence identified | `PASS_WITH_LIMITATIONS` | Official lists match 50 names each; identity, prices, corporate actions, and tradability are separate unresolved questions. |
| Historical 2017_H1 membership complete | `BLOCKED` | 49 known/nonblank names; unresolved slot and 720 missing known member-date rows. |
| Corporate-action evidence fully primary-source verified | `BLOCKED` | 141 ledger events remain unconfirmed; none are applied in the proxy. |
| Exact training table preserved and hashed | `NOT_VERIFIABLE` | Candidate table is in-memory notebook state; no serialized training table/hash located. |

## Model

| Check | Status | Evidence / limitation |
|---|---|---|
| Frozen model artifact identity | `PASS` | Current artifact SHA-256 is recorded in model lineage report and RPR2 manifest. |
| Feature order and class mapping | `PASS` | Six inputs and classes 0/1/2 recorded in model metadata and run manifest. |
| Saved CV / validation / test outputs | `PASS_WITH_LIMITATIONS` | CV and thresholded validation outputs exist in Notebook 04; the frozen artifact declares Argmax, so a same-rule Argmax validation result is not established. No immutable training-data hash exists. |
| Exact archived-model-to-prediction provenance | `NOT_VERIFIABLE` | Archived prediction audit lacks model/run hashes; 49-row test/prediction discrepancy unresolved. |
| Model was refit during this retrospective | `NOT_PERFORMED` | Read-only evidence inspection only. |

## Notebook and source

| Check | Status | Evidence / limitation |
|---|---|---|
| Notebook 07 current hash matches RPR2 record | `PASS` | Hash `77ef752a...498f070` recorded before/after in the baseline manifest. |
| Notebook 08 exact source used by RPR2-2DF recovered | `NOT_VERIFIABLE` | Manifest records `0dc604...`; current sibling v2 and root hashes differ. |
| Notebook 08 was executed in this retrospective | `NOT_PERFORMED` | No notebook cells were executed for this report. |
| Local Git history supports full chronology | `NOT_VERIFIABLE` | Local history contains only the initial commit; project evidence is in artifacts, not a full commit trail. |

## Backtest outputs

| Check | Status | Evidence / limitation |
|---|---|---|
| 63 Strategy × Allocation result rows present | `PASS` | Named baseline CSV has 63 rows; all are `COMPLETED_WITH_LIMITATIONS`. |
| Output Run ID consistently identified | `PASS_WITH_LIMITATIONS` | This checklist uses RPR2-2DF only. A second RPR2 folder has distinct IDs and is not merged. |
| Cash + market value equals daily equity | `PASS` | Recomputed from existing baseline output; maximum absolute residual 0. |
| Initial equity matches baseline | `PASS` | First daily mark is THB 1,000,000 for all 63 combinations. |
| Total return and maximum drawdown match stored daily series | `PASS` | Recomputed unannualized values exactly match all 63 summary rows. |
| Fees + slippage reconcile with reported aggregate cost | `PASS` | Filled-row fee and slippage sums match the aggregate performance-summary cost. |
| Official exchange execution validity | `BLOCKED` | Vendor raw Open and observed dates; theoretical fractional shares; 0 verified tradable names. |
| Stale-age compliance on verified SET sessions | `NOT_VERIFIABLE` | No official calendar; zero stale rows is only an observed-vendor-calendar result. |
| Annualized CAGR / Sharpe / Sortino | `NOT_REPORTED` | Do not treat annualized metrics as verified on this calendar. |

## Scope and gate

- No model fit or inference performed during report preparation.
- No backtest was rerun.
- No dataset, model, notebook, decision register, gate, or historical output was changed.
- No external data or API was used.
- `RESEARCH_BACKTEST_GATE = CONDITIONAL_OPEN` (run scope only).
- `EXECUTION_VALIDATION_GATE = BLOCKED`.
- `Canonical_Historical_Gate = BLOCKED`.
- `PHASE_F = DO_NOT_BEGIN`.

The supporting files are linked in [Evidence_Index.csv](./Evidence_Index.csv) and hashed in [Report_Manifest_SHA256.txt](./Report_Manifest_SHA256.txt).
