# Critical-Path Analysis - Workstream 1.9.2

## Method

The critical path is the longest directed dependency chain by edge count in the registered DAG, calculated from the node and edge registers using a topological traversal. It is a dependency depth measure, not a calendar estimate, task schedule, or claim that all parallel work must wait serially. Parallel evidence streams can proceed independently until they converge.

- DAG: 81 nodes, 127 directed edges; acyclic.
- Terminal control node: `N_FINAL_GATE_STATUS` (`RESEARCH_BACKTEST_GATE=BLOCKED; PHASE_F=DO_NOT_BEGIN`).
- Longest chain: **18 edges**.

## Longest dependency chain

Node sequence:

`SRC_FEATURE_PATHWAY` -> `B-FEAT-01` -> `B-MOD-01` -> `B-MOD-02` -> `N_PREDICTION_SNAPSHOT` -> `N_PREDICTION_UNIVERSE` -> `N_DAILY_BUY_UNIVERSE` -> `N_HIST_RISK_INPUTS` -> `N_METHOD_IMPLEMENTATION` -> `N_ALLOCATION_SOLVER` -> `N_ORDER_SIZING` -> `N_ORDER_EXECUTION` -> `N_PORTFOLIO_VALUATION` -> `N_ARCHIVE_METRIC_REVIEW` -> `N_REPRODUCIBILITY` -> `N_GATE_INPUTS` -> `B-GATE-01` -> `D_E021` -> `N_FINAL_GATE_STATUS`

Edge sequence:

`M04` -> `M05` -> `M09` -> `M11` -> `U03` -> `U04` -> `R01` -> `R06` -> `R10` -> `R14` -> `L08` -> `VAL01` -> `PF02` -> `ARCH08` -> `G09` -> `G10` -> `G11` -> `G14`

## Converging critical prerequisites

- **Training/model/predictions:** incomplete training identity, point-in-time membership and feature exposure; model metadata declares 10,436 samples while archived predictions contain 10,387 per pair (49 unexplained).
- **Tradable universe:** independent identity/corporate-action evidence, vendor provenance and OHLC quality, calendar alignment, membership and eligibility evidence converge; no fully verified tradable row is available (AOT four member-date candidates are not a pass).
- **Risk/allocation:** archived Buy Universe and historical risk panel are missing; 2/7 notebook paths are supported while historical readiness is 0/7; no archived solver/weights trace is established.
- **Execution/valuation/performance:** no verified effective-dated board-lot schedule or E-002 decision; execution, stale valuation, costs, segment continuity and performance lineage remain blocked.
- **Historical provenance:** B-RUN-01 remains blocked. E-029 identifiers and Risk_Data_Hash are future manifest requirements only; they do not retrofit archived runs.
- **Final validation/gate:** integrated validation, reproducibility and eligible-universe evidence remain unsatisfied; E-021/E-022 remain blocked and E-023 is baseline-only.

## Separate forward-only E-029 chain

`B-DEC-29 -> D_E029 -> five required identifiers + Risk_Data_Hash -> N_FUTURE_RUN_MANIFEST -> N_DAILY_PROVENANCE -> N_FUTURE_AUDITABILITY`. This chain has no edge to historical `B-RUN-01` and no edge that opens the current gate. The five E-029 identifiers are provenance references, not optimizer arguments; Risk_Data_Hash is separately required under E3.

## Decision and gate constraints

- E-004 Option B is specification-approved: 252 verified exchange-session intervals/year; annualize only at 252 valid consecutive one-session returns (253 marks); shorter valid segments remain unannualized; do not bridge/combine. Risk-free Rate and MAR remain separately unresolved.
- E-005:E-020 and E-027/E-028 remain approved specifications/controls only, not implementation or historical execution evidence.
- E-001 remains BLOCKED; E-002 remains NEEDS_RESEARCHER_APPROVAL; board lots must not be assumed as 100 shares.
- Statuses of all 27 blockers are unchanged. Approval of E-004/E-029 clears no evidence, data, calendar, identity, implementation, or archive-lineage blocker.

**Final status: `RESEARCH_BACKTEST_GATE = BLOCKED`; `PHASE_F = DO_NOT_BEGIN`.**
