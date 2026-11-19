# Phase E — Portfolio Construction Specification

## Decision

**Specification work only. The Research Backtest Gate remains `BLOCKED`. Phase F remains
`DO_NOT_BEGIN`.**
No historical portfolio backtest, 63-combination run, market-data download, yfinance call,
model fit/refit, source-data edit, or Notebook 05/06 edit was performed.

The researcher has approved the specified policies in Decision E-005 through E-020.
Approval is limited to specification; it does not resolve Phase D evidence blockers,
implement allocators, or open the Research Backtest Gate.

## Evidence inspected

- [05_backtest.ipynb](../../05_backtest.ipynb): existing portfolio engine, sizing and
  valuation prototypes, allocator implementations, and a closed-gate guard.
- [06_research_backtest.ipynb](../../06_research_backtest.ipynb): Phase C research harness,
  safety checks, synthetic regression cases, and explicit unresolved-policy guards.
- [research_gate_checklist.csv](../research_gate_checklist.csv),
  [execution_data_lineage.json](../execution_data_lineage.json), and
  [verified_execution_data_status.json](../verified_execution_data_status.json).
- Phase C vendor quality, provenance, and readiness reports; Phase D universe, feature
  consistency, and blocker reports.
- Existing local exclusion policy and Phase C / D manifests. No outside source was queried.

## Verified existing decisions

The following are carried forward as approved rules, not recommendations:

- Nine Panic/FOMO strategies, with Normal = Hold; no short selling or leverage.
- Sell, forced SET50 exit, Buy, then Hold. Hold positions cannot fund Buys.
- Seven named allocation methods; allocations apply only to incremental cash for Buy
  signals. Existing holdings remain. Per-security incremental allocation cap is 25%,
  with iterative redistribution and residual cash retained.
- Three-session stale valuation using a verified exchange-session count; portfolio-level
  valid/stale/unavailable states; no return bridging; performance reporting by continuous
  segment. E-004 Option B is approved: 252 verified-session intervals per nominal year;
  annualized segment metrics require at least 252 valid consecutive one-session return
  intervals (253 valid equity marks); shorter segments remain unannualized. Risk-free
  Rate and MAR remain separate approvals.
- Common complete dates across every eligible Buy security; no zero/forward fill, pairwise
  deletion, or security removal. Use centered sample covariance; Ledoit-Wolf is not
  permitted without a new decision.
- Minimum risk windows: EW none; IV/ERC/HRP/MinVar/MPT 60 common sessions; CVaR 252.
  Insufficient history or failed solver means that method is unavailable and its cash is
  retained, with no automatic fallback.
- ERC SLSQP controls and 5% post-cap relative-risk-contribution deviation; HRP sample
  correlation/covariance from the same matrix; fixed-`q_max` MinVar and CVaR formulations
  and their approved solver/tolerance settings.
- MPT risk aversion `lambda = 5`, arithmetic mean return and centered sample covariance
  from 60 common sessions, long-only weights, 25% cap, `sum(w) <= 1`, residual cash.
- Decision after close on `t`; next eligible observed execution session's Open; value at
  that session's Close; 0.001 per-side slippage; 0.0016799 transaction-cost rate per side;
  no gap limit; missing Open means no execution.
- BANPU is an approved 2026 exclusion for insufficient verified execution data.
  GLOBAL's existing precautionary exclusion remains; its diagnostic is not proof of a split.
- Phase C records BANPU's approved exclusion across prediction/eligibility and portfolio
  paths while preserving its historical Master rows. Phase D found potential shared
  feature effects outside the four AOT dates; those candidate dates have no BANPU rows in
  the recorded 60-observation windows. This does not authorize rewriting frozen features.
- Phase D's single-security pipeline smoke diagnostic is
  `PASS_WITH_LIMITATIONS` only; it is not portfolio or performance evidence.
- Transaction fees are calculated on slippage-adjusted fill notional; fee and slippage
  values remain research assumptions, not verified historical broker schedules.

## Important code-versus-approval distinction

The legacy [05_backtest.ipynb](../../05_backtest.ipynb) contains `BOARD_LOT = 100`,
`MAX_STALE_CALENDAR_DAYS = 5`, short/CVaR minimum-history constants of 50/200, a
Ledoit-Wolf covariance helper, and allocator fallbacks to EW. These are implementation
facts, **not the approved policies**. Some do not match the Phase E decisions:
[06_research_backtest.ipynb](../../06_research_backtest.ipynb) leaves board lot, stale
threshold, covariance estimator, fallback policy, and CVaR formulation unset; supports
only EW and IV allocators; and refuses to run unsupported methods. Phase E does not
change either notebook or activate unsupported methods.

## Readiness

| Area | Phase E result | Why |
|---|---|---|
| Board-lot policy | BLOCKED | No locally verified, date-effective historical trading-unit schedule; a code constant is insufficient evidence. |
| Valuation / stale-price policy | APPROVED | Three verified sessions, portfolio states, gap handling, and segmented reporting are specified; official calendar and historical evidence remain blockers. |
| Risk estimation | APPROVED | Centered sample covariance, common complete samples, full windows, and fail-closed cash retention are specified; historical input validity remains blocked. |
| EW / IV | APPROVED SPECIFICATION; BLOCKED for historical execution | Their formulas remain specified; the universe, eligibility, execution data, and gate are blocked. |
| ERC | APPROVED SPECIFICATION; BLOCKED for historical execution | Solver and 5% post-cap RC tolerance are specified; the Phase C harness does not implement ERC. |
| HRP | APPROVED SPECIFICATION; BLOCKED for historical execution | Sample/sample method and failure policy are specified; the harness does not implement HRP. |
| MinVar | APPROVED SPECIFICATION; BLOCKED for historical execution | Fixed-`q_max` objective and SLSQP controls are approved; risk inputs and universe remain blocked. |
| CVaR | APPROVED SPECIFICATION; BLOCKED for historical execution | Fixed-`q_max`, 252-session fractional tail, and HiGHS controls are approved; data and universe remain blocked. |
| MPT | APPROVED SPECIFICATION; BLOCKED for historical execution | Objective, input estimates, and SLSQP controls are specified; historical data and universe remain blocked. |
| Multi-security portfolio | BLOCKED | Phase D has only AOT, four candidate member-date rows. |
| 63-combination backtest | BLOCKED | Research gate remains closed; no combination was run. |

## Decision status

- E-004 Option B and E-029 Option B were approved and recorded on 2026-11-17. E-004
  permits annualized segment metrics only at its approved 252-valid-return threshold;
  E-029 makes the five lineage references mandatory at run/snapshot level.
- E-001 historical board-lot schedule remains `BLOCKED`; E-002 odd-lot treatment remains
  `NEEDS_RESEARCHER_APPROVAL`, pending effective-dated identity/segment evidence.
- Risk-free Rate and MAR remain separate `NEEDS_RESEARCHER_APPROVAL` decisions; neither
  was approved by E-004.
- Policy approval does not validate market data, implement methods, or promote any
  strategy/method combination to historical readiness.

## Continuing blockers and Phase F stop

Phase D's limitations remain: 141 unresolved corporate-action events; unresolved
2017_H1 membership and model-context effects; no verified official 2026 trading calendar;
incomplete execution acquisition provenance; BANPU exclusion and missing OHLC; GLOBAL
exclusion; and only one remaining candidate security. The vendor snapshot is Yahoo Finance
research data, not official SET execution data. The frozen model and original datasets
remain unchanged.

**Phase F cannot begin.** Resolve the independent data/universe blockers and outstanding
decisions E-001 and E-002, and separately approve any risk-free/MAR definitions if those
metrics are required, then rerun the documented gate. Approval of E-004/E-029 does not
clear historical lineage or open the gate.

## Final clarification validation

The final synthetic suite passed **19 checks (19 PASS / 0 FAIL)**. Decisions E-005
through E-020 are `APPROVED`; E-004 and E-029 are also now `APPROVED`. E-001, E-021,
and E-022 remain `BLOCKED`; E-002 remains `NEEDS_RESEARCHER_APPROVAL`; Risk-free Rate
and MAR remain separate pending approvals. The 19-check suite predates the 2026-11-17
recording and does not test the newly approved E-004 threshold or implement E-029
identifiers. No tests or metrics were run in the decision-recording workstream.
Synthetic checks validate only the behavior they covered, not historical validity or
portfolio readiness.
