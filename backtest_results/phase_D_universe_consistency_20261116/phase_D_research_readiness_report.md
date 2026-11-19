# Phase D Research Readiness

## Decision

**Research Backtest Gate: BLOCKED.** Phase D is diagnostic only. No portfolio backtest,
single-security backtest, retraining, fit, download, source-data edit, or allocation
change was performed.

## Phase A–D comparison

| Phase | Requirement statuses (overall row excluded) | Candidate symbols | Candidate member-date rows | Gate |
|---|---|---:|---:|---|
| A | 12 PASS / 4 BLOCKED; 0 verified rows | 0 | 0 | BLOCKED |
| B | 8 PASS / 1 PASS_WITH_LIMITATIONS / 7 BLOCKED; 0 verified rows | 0 | 0 | BLOCKED |
| C | 4 PASS / 7 PASS_WITH_LIMITATIONS / 4 BLOCKED | 1 (AOT) | 4 | BLOCKED |
| D | 1 PASS_WITH_LIMITATIONS / 3 BLOCKED; overall BLOCKED | 1 (AOT) | 4 | BLOCKED |

Phase A and Phase B results and artifacts were not rewritten. Phase D did not convert
any prior `BLOCKED` status into a pass.

## Universe and evidence

- Eligible candidate symbols: AOT.
- Candidate member-date rows: 4.
- Phase D-added symbols/rows: 0 / 0.
- 51 current member symbols remain excluded for unverified corporate-action continuity.
- BANPU remains excluded for `INSUFFICIENT_VERIFIED_EXECUTION_DATA`; the original missing OHLC cells are unchanged.
- BTS cannot enter because VolRank, CorrRank, and LiquidityRank are missing on the four candidate dates.
- GLOBAL is not a 2026 SET50 constituent; its 141 price-basis anomaly rows do not establish an official split or affect 2026 SET50 shared calculations.
- Corporate-action status: all 141 local ledger events remain unresolved; 97 rows involve symbols in the 2026 membership union, while 89 fall inside the symbol's active period on the recorded date.
- 2017_H1 remains unresolved: 49 names plus one blank slot, and 720 listed member-date rows absent from Master. The current model-row reconstruction still matches its frozen 94,205-sample metadata.
- BANPU exclusion-aware same-date diagnostics change VolRank/LiquidityRank values for other securities in 2026. They were not written back to Master; the frozen model was not retrained.

## Separate readiness decisions

1. **Single-security diagnostic:** `PASS_WITH_LIMITATIONS` only for a pipeline smoke-test interpretation of the four AOT rows. It is not a performance estimate, and none was run. The broader vendor provenance/calendar limitations remain.
2. **Multi-security portfolio:** `BLOCKED`; one candidate symbol is not a multi-security universe.
3. **Seven allocation methods:** `BLOCKED`; the universe is single-security, portfolio policies are unresolved, and CVaR is unapproved.
4. **All 63 combinations:** `BLOCKED`; no backtest combination was run and the research gate remains closed.

## Remaining blockers and required evidence

See `phase_D_blocker_register.csv` for the scoped register. The critical outstanding items
are: resolve primary membership/data evidence for 2017_H1; retain frozen-feature
consistency while bounding BANPU effects; verify event terms for affected securities;
obtain complete vendor provenance and official session-calendar evidence; supply missing
BTS rank features without imputation; and approve the existing execution and CVaR policies.

The eligible candidate is non-empty but does **not** make multi-security portfolio,
allocation-method, or full-combination research ready. No missing value was filled,
no corporate action was applied, and no eligibility rule was relaxed.
