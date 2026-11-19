# Research Limitations

## Evidence status

The RPR2 outputs are a `RESEARCH_PROXY_V2` run, not a verified exchange backtest. The run manifest records `RESEARCH_BACKTEST_GATE = CONDITIONAL_OPEN`, `EXECUTION_VALIDATION_GATE = BLOCKED`, `Canonical_Historical_Gate = BLOCKED`, and `PHASE_F = DO_NOT_BEGIN`. No statuses are changed by this retrospective.

## Data limitations

- **Vendor prices:** Feature and execution inputs originate from Yahoo Finance/yfinance. The execution snapshot uses `auto_adjust=False`, but is not official SET execution data or proof of attainable fills.
- **Request provenance:** Phase C reports the exact historical request ticker list, interval, grouping, and source timezone as unknown.
- **Historical coverage:** Eight expected symbols have no Parquet in the verified feature build: BPP, DTAC, GLOW, INTUCH, MTLS, PS, ROBINS, and TMB. No prices or identities are fabricated.
- **2017_H1 membership:** The local record has 49 known/nonblank names and an unresolved slot; the Master lacks 720 known member-date rows across 120 dates. This period overlaps model training.
- **Corporate actions:** 141 ledger rows are unconfirmed by primary evidence; no unverified actions are applied in RPR2. Excluding unverified distributions means PRICE_RETURN is not Total Shareholder Return.
- **Identity:** BANPU conversion/identity history remains unresolved and BANPU has missing execution OHLC; GLOBAL price-basis anomalies do not establish a split. Both are excluded from the Research Proxy.
- **Calendar:** `OBSERVED_VENDOR_CALENDAR` uses vendor rows, not official SET exchange sessions. Zero stale marks on that calendar do not verify E-005/E-006 exchange-session compliance.
- **Feature quality:** Data/rank audits report structural checks passing, but rank coverage is incomplete in early periods and historical feature/model lineage is not fully pinned.

## Model and statistical limitations

- The exact training table is not saved or hash-linked to the frozen artifact. Model metadata and saved notebook row counts are consistent but do not establish byte-level input identity.
- The archived prediction package has 10,387 rows per pair versus 10,436 test samples in model metadata; the 49-row difference is unexplained.
- The 2026 test period is one finite period and the RPR2 investment horizon is 149 observed-vendor sessions. No independent later OOS period is available in this package.
- Panic and FOMO F1 scores are low (0.1075 and 0.1638); Normal's dominant support contributes strongly to headline accuracy.
- Comparing 9 × 7 = 63 configurations creates selection/multiple-comparison risk. The observed top return is exploratory, not a pre-registered superiority result.
- No uncertainty intervals, multiple-comparison adjustment, calibration analysis, or causal attribution of model predictions to portfolio returns is verified here.

## Execution and accounting limitations

- Raw vendor Open plus fixed slippage is a proxy fill rule. It is not proof of execution availability, market impact, queue position, or broker fill.
- The RPR2 run uses theoretical fractional shares. No exchange-tradability or board-lot compliance is claimed.
- Fees and slippage are approved research assumptions, not independently verified historical brokerage/tax schedules.
- Corporate distributions and unverified corporate actions are omitted; metrics are PRICE_RETURN, not Total Shareholder Return.
- The stale count is zero on the observed-vendor calendar, but the official calendar needed to express verified exchange-session age is unavailable.
- Turnover is inherited from Notebook 07 implementation; the approved Phase E register does not define a turnover denominator. Treat the reported value as implementation output, not a fully approved policy metric.
- The run manifest's Notebook 08 hash differs from the current root and sibling notebook hashes. Exact source-to-run identity remains `NOT_VERIFIABLE`.
- A second RPR2 folder has a different Run ID and Prediction Snapshot ID. Its files must not be mixed with the named RPR2-2DF baseline.

## Methodological limits

- Risk windows and seven allocators are subject to a run-scoped E-030 CVaR exception; this does not alter canonical historical policy. CVaR uses at least 60 common-complete observations in an expanding window for RPR2 only.
- Synthetic regressions (21/21 pass) demonstrate only tested software behavior on synthetic inputs. They do not validate historical prices, membership, identity, execution, or performance.
- Output arithmetic reconciliation checks exported records; it cannot establish that the original model never saw unintended information or that all source implementations match the run.
- No annualized CAGR, Sharpe, or Sortino is treated as verified under the observed-vendor calendar. The report does not derive substitute annual metrics.

## Claims not supported

The evidence does not support claims that:

1. RPR2 is a Verified Tradable Backtest or exchange-tradable performance.
2. Total Shareholder Return was measured.
3. Any strategy/allocation is superior or generates causal alpha.
4. The current Notebook 08 is exactly the source that produced the named run.
5. The current frozen model can be reproduced from an exact, hash-identified training table.
6. Zero stale count proves official exchange-session compliance.
7. E-030 opened the canonical historical gate or authorized Phase F.

## Required next evidence

Prioritize primary-source 2017 membership and security identity/corporate-action records, official SET calendar, complete execution request provenance, verified board-lot rules, an immutable training-data/run chain, exact Notebook 08 source for the named run, and an independent subsequent out-of-sample period. Any future execution-validation work requires separate authorization and must not retroactively relabel this proxy.
