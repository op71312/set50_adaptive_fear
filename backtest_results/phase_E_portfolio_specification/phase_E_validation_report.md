# Phase E — Researcher Decision Finalization Validation Report

## Scope and safety outcome

This finalization updates specifications, the decision register, summary, changelog, and
manifest only. Researcher decisions E-005 through E-020 are recorded as `APPROVED`.
Approval is specification-only: no method was implemented or run on historical data.

No market data was downloaded; no yfinance call, historical backtest, or 63-combination
run occurred; no model was retrained; Notebook 05/06, source datasets, execution
snapshots, frozen model, and Phase A-D outputs were not modified. Research Backtest Gate
remains `BLOCKED`; Phase F remains `DO_NOT_BEGIN`.

## File inventory and scope

All ten files in `backtest_results/phase_E_portfolio_specification/` were inspected:

- `E1_board_lot_policy.md` (inspected; unchanged)
- `E2_valuation_stale_price_policy.md`
- `E3_risk_estimation_policy.md`
- `E4_allocation_methods_specification.md`
- `E5_cross_method_consistency.md`
- `phase_E_decision_register.csv`
- `phase_E_summary.md`
- `phase_E_validation_report.md`
- `phase_E_revision_changelog.md`
- `phase_E_manifest.json`

The nine files other than E1 are the files changed in this finalization. No files outside
the Phase E directory were changed.

## Decision status reconciliation

All decisions E-005 through E-020 are `APPROVED`, as explicitly directed by the
researcher. The register now follows the requested numbering for ERC, HRP, MinVar, CVaR,
and MPT. Prior volume/repeated-Close, EW, IV, fee, and common-contract decisions were
preserved under E-024 through E-028. The unapproved identifier extension is separated as
E-029.

| Decision range | Decision | Status |
|---|---|---|
| E-005 | Three verified-session stale threshold | `APPROVED` |
| E-006 | Portfolio valuation states and whole-portfolio unavailability | `APPROVED` |
| E-007 | Gap breaks and segment-by-segment metrics | `APPROVED` |
| E-008 | Common complete risk panel; centered sample covariance; no Ledoit-Wolf | `APPROVED` |
| E-009 | Date intersection; no imputation, pairwise deletion, or security removal | `APPROVED` |
| E-010 | EW none; IV/ERC/HRP/MinVar/MPT 60; CVaR 252 | `APPROVED` |
| E-011 | Failure means unavailable; retain cash; no fallback | `APPROVED` |
| E-012–E-013 | ERC objective, weights, solver, 5% post-cap RC tolerance | `APPROVED` |
| E-014 | HRP sample/sample methodology and algorithm | `APPROVED` |
| E-015–E-016 | MinVar fixed-`q_max` objective and SLSQP controls | `APPROVED` |
| E-017–E-018 | CVaR95 fractional-tail objective and HiGHS controls | `APPROVED` |
| E-019–E-020 | MPT objective, inputs, and SLSQP controls | `APPROVED` |

### Decisions still unresolved or blocked

| Decision / blocker | Status | Boundary |
|---|---|---|
| E-001 Historical effective-dated board-lot schedule | `BLOCKED` | No verified historical schedule; no sizing authorization. |
| E-002 Odd-lot scope/treatment | `NEEDS_RESEARCHER_APPROVAL` | Requires verified schedule and separate treatment decision. |
| E-004 Segment annualization convention | `APPROVED` | Option B: 252 verified-session intervals per nominal year; annualized segment metrics only at 252 consecutive valid return intervals (253 equity marks). Shorter segments remain unannualized. Risk-free Rate and MAR are separate unresolved decisions. |
| E-021 Research Backtest Gate | `BLOCKED` | This approval does not open or override it. |
| E-022 Phase D evidence/data blockers | `BLOCKED` | The 141 actions, 2017_H1 membership, official calendar, provenance, BANPU/GLOBAL, and one-security limitations remain. |
| E-023 Phase D baseline | `VERIFIED` | AOT only, four candidate rows; this is not portfolio readiness. |
| E-029 Additional snapshot/version identifier fields | `APPROVED` | Option B: all five are mandatory run/snapshot lineage references, not new numerical optimizer arguments; `Risk_Data_Hash` remains separately required. Do not infer/backfill archived IDs; report missing/inconsistent future lineage as `PROVENANCE_INCOMPLETE`. |

Decision register count (29 decisions): 20 `APPROVED`, 4 `APPROVED_EXISTING`, 1
`NEEDS_RESEARCHER_APPROVAL`, 3 `BLOCKED`, and 1 `VERIFIED`. Risk-free Rate and MAR remain
separate decisions requiring approval; they do not change the E-004 status.

## Specification consistency checks

| Check | Result | Evidence |
|---|---|---|
| Decision register matches researcher numbering | PASS | E-012/013 ERC; E-014 HRP; E-015/016 MinVar; E-017/018 CVaR; E-019/020 MPT. |
| Every E-005 through E-020 status is approved | PASS | Register contains exactly 16 rows in this range, each `APPROVED`. |
| E2 threshold and states | PASS | Age 0 at valid Close; stale ages 1–3 only on verified sessions; age >3 or any unavailable holding makes portfolio value unavailable. |
| E2 return-series handling | PASS | No carried-price zero return, no gap bridging, unavailable dates/holdings preserved, segments reported separately. |
| E2 full-period and annualization rules | PASS | No full-period metrics for incomplete equity; E-004 Option B uses 252 verified-session intervals and a 252-valid-return reporting floor; shorter segments remain unannualized. |
| E3 common panel and sample covariance | PASS | Same ordered complete dates/symbols/cutoff; centered sample covariance; no Ledoit-Wolf absent a new decision. |
| E3 windows and failure behavior | PASS | EW none; IV/ERC/HRP/MinVar/MPT 60; CVaR 252; insufficiency means unavailable and cash retained. |
| ERC controls | PASS | SLSQP 10,000 iterations, `ftol=1e-8`, post-cap relative RC deviation <=5%; failures retain cash. |
| HRP controls | PASS | Sample correlation/covariance from same panel; prescribed distance, single linkage, quasi-diagonalization, recursive bisection. |
| MinVar controls | PASS | Fixed `q_max=min(1,0.25N)`, 25% bounds, sum=q_max; SLSQP 10,000, objective 1e-10, constraints/weights 1e-8. |
| CVaR controls | PASS | 252 scenarios, 95%, tail mass 12.6, symmetric tie split; HiGHS 100,000, primal/dual 1e-8. |
| MPT controls | PASS | 60-session arithmetic mean and centered sample covariance; lambda 5; SLSQP 10,000, objective 1e-10, constraints/weights 1e-8. |
| Shared allocation/execution rules | PASS | Nine strategy combinations; specified action order; Buy uses incremental cash; cap/residual, execution, slippage, fee, and no-fallback rules aligned across docs. |
| Phase D baseline and gate state | PASS | AOT/four rows and all historical readiness blockers preserved; gate remains blocked. |

## Synthetic validation

Synthetic checks are formula, constraint, and document-consistency checks only. They are
not historical market evidence, backtests, or proof of portfolio readiness. The
validation runner uses only in-memory synthetic values and local specification files.

| # | Synthetic check | Result |
|---:|---|---|
| 1 | Verified-session stale age 0→1→2→3→unavailable; reset on a new valid Close | PASS |
| 2 | Any unavailable holding makes whole-portfolio valuation unavailable | PASS |
| 3 | Carried/stale/unavailable values do not create returns or bridge segments | PASS |
| 4 | Contiguous segments retain actual session/calendar elapsed time; annualization unavailable | PASS |
| 5 | Common-date intersection spans all eligible Buy symbols with fixed order/cutoff | PASS |
| 6 | Missing data rejects dates, keeps every symbol, and does not fill or pairwise-delete | PASS |
| 7 | EW has no risk window; full 60/252 windows enforced, no partial fallback | PASS |
| 8 | Centered sample covariance and same-panel sample correlation | PASS |
| 9 | Ledoit-Wolf and mixed HRP estimators excluded by specification | PASS |
| 10 | ERC normalized sleeve, actual-weight 25% cap, cap-and-redistribute, and RC arithmetic | PASS |
| 11 | ERC SLSQP settings and 5% post-cap deviation boundary | PASS |
| 12 | MinVar fixed-`q_max` feasibility for N=1,2,3,4,5 and cap/cash invariants | PASS |
| 13 | MinVar solver and tolerance values match register/specification | PASS |
| 14 | CVaR 12.6 tail arithmetic and equal fractional allocation across boundary ties | PASS |
| 15 | CVaR HiGHS settings and fixed-`q_max` constraints match register/specification | PASS |
| 16 | MPT objective, 60-session mean/covariance, bounds, and residual cash | PASS |
| 17 | MPT SLSQP settings and tolerance values match register/specification | PASS |
| 18 | Allocation cap/residual and independent buy/sell fee arithmetic | PASS |
| 19 | Approved/blocked statuses, preserved stop conditions, and no gate override | PASS |

**Synthetic validation: 19 PASS / 0 FAIL.** No synthetic check was interpreted as
historical validity or portfolio approval.
These checks were executed before the 2026-11-17 E-004/E-029 decision recording. They
do not test the newly approved 252-interval threshold, and no new tests or metrics were
run in the decision-recording workstream.

## Protected hash verification

SHA-256 comparison against the pre-finalization manifest covered all 16 protected input
files: Notebook 05/06, execution snapshots, Master Dataset, model, membership/declaration
files, corporate-action ledger, execution exclusions/control files, and recorded Phase
C/D manifests and gate/readiness outputs. **16/16 matched.**

The refreshed manifest records hashes for all nine non-manifest Phase E output files.
Final SHA-256 verification matched **9/9 outputs** and the changelog checksum. All edits
in this task are confined to `backtest_results/phase_E_portfolio_specification/`.

## Final stop condition

`PHASE_E_SPECIFICATION_UPDATED`

`PHASE_E_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`

No historical backtest, 63-combination run, market-data download, model retraining,
protected-file modification, or gate override is authorized.
