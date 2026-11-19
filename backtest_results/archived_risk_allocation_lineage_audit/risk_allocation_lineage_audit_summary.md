# Archived Risk & Allocation Lineage Audit

## Executive summary

The archived package contains 63 strategy/allocation result groups and structurally aligned prediction, daily portfolio, transaction, and valuation files. It does **not** contain archived risk panels, covariance/correlation matrices, Buy Universe snapshots, raw/final optimizer weights, solver diagnostics, or a run manifest linking those results to historical code and inputs.

The exact historical Buy Universe and Risk Estimation Universe therefore remain unknown. The archive's metadata says it used adjusted Master OHLC as execution prices, but does not identify a file or hash and does not specify whether those prices were also used to estimate risk. GLOBAL is absent from recorded 2026 predictions, transactions, and valuation, so no direct holding is observed. Its historic risk-input and allocation influence cannot be established from the available records.

## Validated archive structure

- Six archive artifacts are present; the five output CSV byte sizes match the archive manifest.
- Performance, daily portfolio, and prediction files cover all 63 pairs: nine IDs (`S1`–`S9`) by seven methods (`EW`, `IV`, `ERC`, `HRP`, `MinVar`, `CVaR`, `MPT`).
- There are 209 daily records and 209 decision dates per pair; prediction rows cover the same 209 decision dates, with 10,387 rows per pair.
- Transaction and valuation records cover 35 pairs. The other 28 pairs have zero holdings in every daily row.
- No GLOBAL rows occur in archived prediction, transaction, or valuation symbol fields.
- The archive contains daily cash and position valuation fields, but does not store raw allocation weights, risk input identifiers, or a method-specific allocation audit.

These are structural checks on retained output, not proof of historically correct risk calculations, allocation logic, or execution policy. The archive manifest itself records known issues: adjusted Master OHLC execution prices, a single-asset cap bypass in some methods, omitted initial-equity baseline for return/CAGR, and BANPU stale valuation up to 93 calendar days.

## Risk and allocation findings

`RISK_UNIVERSE_UNKNOWN`: no historical daily Buy Universe or risk-symbol set is recorded. Do not infer the risk universe from the prediction rows, current membership file, current notebook logic, or transactions.

All seven methods' **archived implementations are unverified**. The present `05_backtest.ipynb` contains implementations for seven methods, but it is a later/static code reference and its saved run state says the gate was closed and all 63 experiments were skipped. The available `06_research_backtest.ipynb` saved state marks only EW and IV implemented and also records a blocked gate. Neither file is hash-linked to the archived package.

The current-code references differ from approved Phase E specifications in important places: 50/200 minimum-history constants rather than full 60/252 windows; Ledoit-Wolf rather than approved centered sample covariance; automatic EW fallbacks; and, for MinVar/CVaR, a full-investment sum constraint in the visible code before post-cap processing. These are implementation observations only and are not attributed to the archived run.

## GLOBAL exposure

- **Direct holding exposure:** no recorded GLOBAL prediction, transaction, or valuation rows in the archived package.
- **Direct risk-input exposure:** unknown; no risk universe or matrix is archived.
- **Indirect historical feature exposure:** a separate Feature Master audit confirmed a GLOBAL feature-generation pathway while GLOBAL was a historical SET50 constituent.
- **Indirect risk/allocation influence:** unknown; there is no archived risk panel, weights, or solver trace linking GLOBAL to an allocation.
- **Performance impact:** not assessed; no counterfactual calculation was performed.

## Final decision table

| Question | Finding | Evidence classification |
|---|---|---|
| Archived Buy Universe identified? | No; no per-date Buy set or allocation input snapshot. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Historical Risk Universe identified? | No; `RISK_UNIVERSE_UNKNOWN`. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Risk matrices identified? | No standalone archived return/covariance/correlation/scenario matrix found. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Raw allocation weights identified? | No. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Final allocation weights identified? | No. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| EW historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| IV historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| ERC historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| HRP historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| MinVar historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| CVaR historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| MPT historical implementation verified? | No; current code only is visible. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| GLOBAL direct holding exposure verified? | No direct GLOBAL position recorded in inspected outputs. | `HASH_VERIFIED` archive files; no direct rows |
| GLOBAL direct risk-input exposure verified? | No; risk inputs absent. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| GLOBAL allocation influence verified? | No; input-to-weight lineage absent. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Historical solver execution verified? | No per-date solver outputs exist. | `UNKNOWN_INSUFFICIENT_EVIDENCE` |
| Portfolio execution/valuation lineage verified? | Partially: output rows align structurally, but source/rule lineage is absent. | `METADATA_REFERENCE_ONLY` |

`RISK_ALLOCATION_LINEAGE_AUDIT = COMPLETED / BLOCKED`  
`ARCHIVED_BUY_UNIVERSE = UNKNOWN`  
`HISTORICAL_RISK_UNIVERSE = UNKNOWN`  
`RISK_INPUT_LINEAGE = UNKNOWN`  
`ALLOCATION_WEIGHT_LINEAGE = UNKNOWN`  
`GLOBAL_RISK_EXPOSURE = UNKNOWN`  
`GLOBAL_ALLOCATION_INFLUENCE = UNKNOWN`  
`HISTORICAL_SOLVER_EVIDENCE = UNKNOWN`  
`PORTFOLIO_EXECUTION_LINEAGE = PARTIALLY_VERIFIED`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`

No evidence was repaired or reconstructed. Do not automatically start Workstream 1.5.
