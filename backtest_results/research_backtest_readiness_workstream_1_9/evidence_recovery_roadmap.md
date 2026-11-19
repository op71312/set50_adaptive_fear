# Workstream 1.9 — Evidence Recovery Roadmap

## Purpose and boundary

This is a prioritized evidence-only roadmap, not authorization to recover data,
modify artifacts, implement methods, run a backtest, or begin Phase F. Existing
evidence blockers remain in place. E-004 and E-029 are approved specification
decisions, not evidence clearances.

## Priority 0 — Resolve primary evidence and session foundation

These tracks can be pursued in parallel, but their results must converge before
certifying a multi-security universe or execution history.

1. **Corporate actions and security identity (B-CA-01, B-ID-01, B-ID-02).**
   Reconcile the 141 ledger entries individually against authoritative event and
   identity evidence. The 97 union-overlap and 89 active-membership recorded-date
   counts are relevance scopes only. Current classification has 138
   secondary-supported and 3 candidate-only records; each of 141 price impacts
   remains potential, with no confirmed impact dimensions or applied adjustment.
   Preserve BANPU's 2026 exclusion and GLOBAL's precautionary exclusion. Do not
   infer a split, adjust prices, or treat every event as price-impacting.

2. **Official exchange-session calendar (B-CAL-01).** Obtain a dated, authoritative
   SET session calendar and define the verified session ordinal/date mapping.
   Yahoo-observed dates and weekdays are not exchange sessions. This evidence is
   needed for execution alignment, E-005 stale-age rules, E-007 segments, and
   E-004's 252 verified-session interval convention.

3. **Execution provenance and quality (B-EX-01/02/03).** Resolve source authority
   and the original request record. Existing metadata identifies Yahoo Finance via
   yfinance 1.8.0, retrieval at `2026-11-15T11:37:11.389684+00:00`, requested
   range `2026-01-05` through `2026-11-14` exclusive, 83 requested/returned
   symbols, `auto_adjust=False`, `actions=True`, and snapshot SHA-256
   `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
   The exact ticker list, interval, `group_by`, and source timezone are unknown.
   The snapshot is not exchange-verified. Resolve all 253 missing OHLC cells
   (Open 63, High 63, Low 63, Close 64) across 64 BANPU rows, plus the 141
   GLOBAL anomaly field-rows on 36 dates, using evidence rather than imputation.
   Missing/zero volume and repeated closes are diagnostic only.

4. **Historical membership (B-MEM-01).** Obtain primary 2017_H1 membership and
   effective-date evidence; reconcile the 50-slot/49-name/one-blank local file
   with the reports that describe 49 known names. Resolve the six listed symbols
   absent from Master for 120 dates (720 member-date rows) through source
   evidence, not guessed membership or synthetic series. Local 2026 H1/H2 lists
   match retained local SET PDFs at 50 names each; that 54-symbol union is scoped
   verification and does not prove a fully tradable universe.

## Priority 1 — Recover historical provenance and archive lineage

Proceed in parallel with Priority 0 where source access permits; do not retrofit
current artifacts into historical runs.

5. **Model, training, feature, and prediction lineage (B-FEAT-01, B-MOD-01/02).**
   Recover original training-input identity/hash, code and configuration, model
   and feature manifests, prediction job record, and reason for the 49-row
   difference between 10,436 test samples and 10,387 archived predictions per
   pair. Preserve the documented BANPU/GLOBAL feature pathway limitations.
   No model fitting, retraining, or prediction generation is part of this review.

6. **Archived allocation, execution, and performance lineage
   (B-ALLOC-01, B-EXEC-01, B-PERF-01, B-STALE-01, B-COST-01, B-RUN-01).**
   Recover run-linked Buy universes, risk panels and `Risk_Data_Hash`, raw/final
   weights, solver outcomes, input-to-order/fill links, valuation states, initial
   equity, return formulas, fee/slippage decomposition, and run/code/input hashes.
   Existing archives contain 63 strategy/method pairs, but missing lineage means
   those rows and reported metrics are not validated. Do not reconstruct
   historical behavior from current notebooks or output counts.

## Priority 2 — Establish eligibility, sizing, and method readiness

7. **Candidate universe (B-UNIV-01).** Reconcile identity, actions, execution,
   membership, calendar, and feature evidence before admitting any symbol. Current
   Phase C/D evidence has AOT only: one candidate symbol and four candidate
   member-date rows; fully verified tradable rows remain zero. Common complete
   dates must not silently remove a security.

8. **Risk panels (B-RISK-01).** Only after the complete eligible Buy universe is
   evidenced, establish ordered common-complete dates, a shared cutoff, the full
   approved windows (60 for IV/ERC/HRP/MinVar/MPT; 252 for CVaR), and
   `Risk_Data_Hash`. Do not impute, use pairwise dates, lower windows, or drop
   eligible symbols.

9. **Board lots and odd lots (B-LOT-01, B-DEC-02).** First obtain the
   effective-dated primary schedule required for E-001; only then request the
   E-002 researcher decision on odd-lot orders and residual/terminal treatment.
   Notebook 05's legacy `100` constant is not evidence. E-001 remains blocked;
   E-002 remains `NEEDS_RESEARCHER_APPROVAL`.

10. **Implementation and method validation (B-IMPL-01, B-METHOD-01, B-TEST-01).**
    In a separately authorized phase, reconcile implementation to approved
    Phase E, then validate the shared contract and all seven methods. Current
    historical readiness is 0/7; Notebook 06 only contains EW/IV paths (2/7),
    while five methods are unsupported. Phase E's 19 synthetic checks do not
    establish historical readiness.

## Priority 3 — Independent gate review only after prerequisites

After evidence, policy, and implementation prerequisites are actually satisfied,
perform a separate evidence-based gate review under explicit authorization.
Maintain `RESEARCH_BACKTEST_READINESS = BLOCKED`,
`RESEARCH_BACKTEST_GATE = BLOCKED`, and `PHASE_F = DO_NOT_BEGIN` until that
review and authorization occur. This roadmap does not initiate that work.

## Open decisions that remain

- E-001 board-lot policy is still blocked pending primary effective-date evidence.
- E-002 odd-lot/residual policy still requires researcher approval after E-001
  evidence is available.
- Risk-free Rate and MAR remain separate `NEEDS_RESEARCHER_APPROVAL` decisions;
  E-004 did not approve either.
- E-004's annualization convention and E-029's five lineage-reference fields are
  approved, but neither approval supplies a calendar, annualized result, or
  missing archived lineage.
