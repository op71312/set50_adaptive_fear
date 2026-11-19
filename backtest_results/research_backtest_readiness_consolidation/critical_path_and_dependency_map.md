# Critical Path and Dependency Map

**Current state:** read-only evidence consolidation complete; no execution stage is
authorized. Every item below is a dependency description for a later, separately
authorized evidence/gate workflow, not permission to start it.

## Dependency graph

```text
PRIMARY EVIDENCE (parallel workstreams)
  ├─ Corporate-action terms / security identity ───────────────┐
  ├─ Execution source, provenance, missing OHLC, price basis ─┤
  ├─ Official session calendar and date mapping ───────────────┤
  └─ 2017_H1 membership + six missing member series ───────────┤
                                                               v
MODEL / FEATURE / ARCHIVE LINEAGE (parallel with evidence recovery)
  ├─ Exact training inputs, model/run hashes, 49-row discrepancy ─┤
  └─ Archived Buy Universe, risk panels, weights, solver, fills ──┤
                                                                 v
ELIGIBILITY AND HISTORY
  ├─ Evidence-backed multi-security eligible universe (B-UNIV-01)
  └─ Full common complete 60/252-observation panels (B-RISK-01)
                                                                 v
POLICY / IMPLEMENTATION (after evidence and decisions)
  ├─ E-001 board-lot evidence/source coverage ──> E-002 odd-lot decision
  ├─ E-004 segment annualization decision (only if annualized metrics required)
  ├─ E-029 optional identifiers decision (Risk_Data_Hash remains required)
  └─ Conform execution, valuation, allocators and accounting to Phase E
                                                                 v
VALIDATION / GATE
  ├─ Validate seven methods, common contract, cash/failure/segment behavior
  ├─ Preserve reproducible source/code/config hashes
  └─ New evidence-based gate review + explicit authorization
       └─ Until then: RESEARCH_BACKTEST_GATE=BLOCKED; PHASE_F=DO_NOT_BEGIN
```

## Critical path

1. Resolve the primary-source and vendor-basis blockers: B-CA-01, B-ID-01/02,
   B-EX-01/02/03, B-MEM-01, and B-CAL-01. The four source-recovery tracks may proceed
   independently, but the universe cannot be certified until their intersections are
   resolved.
2. Establish point-in-time model/feature and historical artifact identity: B-FEAT-01,
   B-MOD-01/02, B-ALLOC-01, B-EXEC-01, B-RUN-01. Do not attribute current notebook or
   current model behavior to archived outputs.
3. Form a compliant multi-security universe (B-UNIV-01), then prove each method's full
   common-complete window, symbol ordering, cutoff, return basis, and data hash
   (B-RISK-01). Missing observations must shrink the shared date set for every symbol;
   they must not remove a security or activate a partial-window fallback.
4. Resolve the sizing prerequisite E-001 with effective-dated primary schedule evidence.
   E-002 odd-lot scope depends on that schedule. E-004 governs annualization of valid
   segments; until approved, only unannualized segment metrics and elapsed time are
   permitted. E-029 concerns five optional identifiers; E3's `Risk_Data_Hash` remains
   required.
5. Only after those inputs/policies are stable, align the future implementation with
   approved Phase E and validate all seven methods, execution/valuation, fees, residual
   cash, failure behavior, and segmented reporting (B-IMPL-01, B-METHOD-01, B-TEST-01).
6. Reconcile reproducibility and artifacts, then conduct a separate evidence-based gate
   review. No historical run or Phase F action is authorized by this consolidation.

## Parallelizable evidence tracks

| Track | Work that can proceed independently | Convergence point |
|---|---|---|
| Corporate actions / identity | Primary notices, Security_IDs, event terms and settlement evidence for the 141 ledger entries; BANPU and GLOBAL handled separately. | Before affected symbols can be declared continuous or eligible. |
| Execution / vendor | Original request log, authorization/source policy, missing-date status and full-horizon price basis. | Before execution/valuation inputs are accepted. |
| Membership / calendar | 2017_H1 official membership and missing-series evidence; official session calendar and deterministic alignment. | Before model context, stale age, or execution date can be certified. |
| Model / archive lineage | Training dataset/model/prediction identity and archived 63-pair Buy/risk/weight/solver/performance trace. | Before historical outputs can be reproduced or trusted. |
| Researcher decisions | E-004 and E-029 can be decided independently; E-002 should follow E-001 schedule/source evidence. | Before affected reporting/interface policies are finalized. |

## Non-negotiable gates

- 2026 official membership is scoped `VERIFIED`; it does not imply official daily
  sessions or execution data.
- The AOT four-row sample is `PASS_WITH_LIMITATIONS` only as a vendor-based
  single-security diagnostic; it is not a portfolio.
- Phase E's 19 synthetic checks establish formula/implementation behavior only.
- Current readiness is 0/7 historical methods, despite EW/IV being the only two paths
  supported in Notebook 06.
- Keep all current blocker statuses and the Research Backtest Gate unchanged. No
  evidence recovery, model operation, data modification, or backtest is performed in
  this workstream.
