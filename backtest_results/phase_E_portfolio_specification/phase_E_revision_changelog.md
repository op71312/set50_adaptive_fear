# Phase E Researcher Decision Finalization Changelog

## Scope

This finalization records researcher-approved specification decisions received
2026-11-16. Documentation, decision register, synthetic validations, and manifest only
were changed. Approval applies to specification and does not constitute implementation,
historical validation, or gate approval.

## Decision ID mapping

The final researcher instruction assigns E-012/E-013 to ERC, E-014 to HRP,
E-015/E-016 to MinVar, E-017/E-018 to CVaR, and E-019/E-020 to MPT. This differs from
the earlier register numbering. To preserve prior decisions without reusing IDs:

- Prior E-006 volume/repeated-Close rule is retained as E-024.
- Prior E-012 EW and E-013 IV rules are retained as E-025 and E-026.
- Prior E-019 fill/fee rule is retained as E-027.
- Prior E-020 shared allocation/execution rules are retained as E-028; the proposed
  snapshot/version identifier extension is separated as E-029 and remains unapproved.

E-001 through E-004 and E-021 through E-023 retain their identities. The decision
register is the canonical mapping.

## Researcher-approved decisions

| Decision | Recorded approved rule | Status |
|---|---|---|
| E-005 | Carry last verified Close for at most 3 subsequent verified exchange sessions; beyond age 3 the holding is unavailable. Yahoo rows are not a session calendar. | `APPROVED` |
| E-006 | Portfolio states are `PORTFOLIO_VALUE_VALID`, `PORTFOLIO_VALUE_STALE`, and `PORTFOLIO_VALUE_UNAVAILABLE`; any unavailable holding makes the entire portfolio equity unavailable. | `APPROVED` |
| E-007 | Break equity/return series at stale or unavailable observations; report continuous segments separately; prohibit full-period CAGR, Sharpe, and maximum drawdown when equity is incomplete. Segment annualization remains unresolved under E-004. | `APPROVED` |
| E-008 | Use common complete Buy-universe dates and centered sample covariance; HRP correlation and covariance come from the same return matrix; Ledoit-Wolf requires a new decision. | `APPROVED` |
| E-009 | Drop incomplete dates for every Buy security together; do not zero-fill, forward-fill, pairwise-delete, or remove a security. | `APPROVED` |
| E-010 | EW requires no risk history; IV/ERC/HRP/MinVar/MPT require 60 common sessions; CVaR requires 252. No partial windows. | `APPROVED` |
| E-011 | Insufficient inputs or failed checks make the method unavailable; retain cash; no automatic fallback. | `APPROVED` |
| E-012 | ERC relative-risk-contribution objective, risky-sleeve/actual-weight separation, 25% cap, and cap-and-redistribute; verify post-cap contributions. | `APPROVED` |
| E-013 | ERC SLSQP `maxiter=10000`, `ftol=1e-8`, maximum post-cap relative RC deviation 5%; otherwise unavailable and cash retained. | `APPROVED` |
| E-014 | HRP uses `sqrt((1-correlation)/2)`, single linkage, hierarchical clustering, quasi-diagonalization, and recursive bisection on the common sample/sample panel. | `APPROVED` |
| E-015 | MinVar minimizes `w'Σw` with `0<=w_i<=0.25`, `sum(w)=q_max`, `q_max=min(1,0.25N)`. | `APPROVED` |
| E-016 | MinVar SLSQP `maxiter=10000`, objective tolerance `1e-10`, constraint/weight tolerance `1e-8`; failed checks retain cash. | `APPROVED` |
| E-017 | CVaR95 over 252 common observations, fixed `q_max`; 12 full worst losses plus 0.6 boundary mass; split boundary ties equally. | `APPROVED` |
| E-018 | CVaR HiGHS `maxiter=100000`, primal and dual feasibility tolerances `1e-8`; failed checks retain cash. | `APPROVED` |
| E-019 | MPT maximizes `w'μ-5w'Σw`, with 60-session arithmetic mean and centered sample covariance, daily decimal returns, `0<=w_i<=0.25`, `sum(w)<=1`, and residual cash. | `APPROVED` |
| E-020 | MPT SLSQP `maxiter=10000`, objective tolerance `1e-10`, constraint/weight tolerance `1e-8`; failed checks retain cash. | `APPROVED` |

## Decisions not approved or not cleared

- E-001 historical effective-dated board-lot schedule: `BLOCKED`.
- E-002 odd-lot scope/treatment: `NEEDS_RESEARCHER_APPROVAL`.
- E-004 annualization convention for valid segments: `NEEDS_RESEARCHER_APPROVAL`.
- E-021 Research Backtest Gate: `BLOCKED`.
- E-022 Phase D evidence/data blockers: `BLOCKED`.
- E-023 Phase D baseline: `VERIFIED`; it does not establish portfolio readiness.
- E-029 additional snapshot/version identifier extension: `NEEDS_RESEARCHER_APPROVAL`.
- E-024 through E-028 preserve no-inference, EW/IV, fee, and common method-contract
  decisions; see their register statuses.

## Files changed in this finalization

All changed files are under `backtest_results/phase_E_portfolio_specification/`:

- `E2_valuation_stale_price_policy.md`
- `E3_risk_estimation_policy.md`
- `E4_allocation_methods_specification.md`
- `E5_cross_method_consistency.md`
- `phase_E_decision_register.csv`
- `phase_E_summary.md`
- `phase_E_validation_report.md`
- `phase_E_revision_changelog.md`
- `phase_E_manifest.json`

`E1_board_lot_policy.md` was inspected and left unchanged. No Notebook 05/06, source
dataset, execution snapshot, frozen model, or Phase A-D artifact was modified. No market
data was downloaded; no historical backtest or 63-combination run occurred; the
Research Backtest Gate remains `BLOCKED`; Phase F remains `DO_NOT_BEGIN`.

## Workstream 1.8 — Controlled Decision Recording (2026-11-17)

Approval source for both entries: explicit researcher instruction in the current
conversation. No researcher identity was inferred. The canonical register's original
SHA-256 was
`43ce34d96b462134d4d697231573b762ff8ee72de690704fdaeb016bda530a99`. The recording
audit is `backtest_results/researcher_decision_recording/decision_recording_audit.md`.

| Decision ID | Previous status | New status | Approved option and exact scope | Explicit exclusions and unresolved matters | Recording date |
|---|---|---|---|---|---|
| E-004 | `NEEDS_RESEARCHER_APPROVAL` | `APPROVED` | Option B: use 252 verified exchange-session return intervals per nominal year. Annualized segment metrics require at least 252 valid consecutive one-session return intervals (253 valid equity marks); shorter valid segments remain unannualized with elapsed-time disclosure. Do not bridge gaps or combine segments. | Risk-free Rate and MAR remain separate decisions and are not approved. No metric was calculated and no implementation or historical readiness was authorized. | 2026-11-17 |
| E-029 | `NEEDS_RESEARCHER_APPROVAL` | `APPROVED` | Option B: `Universe_Snapshot_ID`, `Prediction_Snapshot_ID`, `Execution_Eligibility_Snapshot_ID`, `Model_Version`, and `Allocation_Policy_Version` are mandatory run/snapshot lineage references in the lineage manifest; daily records reference applicable snapshots where relevant. These are not five new numerical optimizer arguments. | `Risk_Data_Hash` remains separately required. Do not infer or backfill archived historical identifiers. Missing or inconsistent future lineage is `PROVENANCE_INCOMPLETE`. This does not independently change E-011, E-028, or execution-gate behavior. | 2026-11-17 |

These entries supersede the earlier pending-status statements above only for E-004 and
E-029. E-001, E-002, E-005 through E-020, E-021 through E-023, and E-027/E-028 were not
changed by this recording. The Research Backtest Gate remains `BLOCKED`; Phase F remains
`DO_NOT_BEGIN`.

The earlier E-007 wording that segment annualization remained unresolved is historical
context; this later E-004 approval controls the annualization convention without
changing E-007's approved gap and segment-boundary rules.
