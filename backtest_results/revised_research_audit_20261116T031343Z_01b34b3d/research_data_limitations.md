# Research Data Limitations — Backtest 2026

This document records limitations observed in local evidence before any Research Backtest. It does not open the Backtest Gate.

## Limitation 1 — BANPU exclusion

BANPU is excluded from portfolio eligibility for 2026-01-01 through 2026-12-31 with reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`. The original/master datasets and SET50 membership history are retained unchanged. Phase 1 found 253 missing OHLC cells across 64 dates from 2026-08-13 to 2026-11-13; no date-specific official evidence resolved the cause. The new universe excludes BANPU; the model and feature/target definitions were not changed or retrained.

## Limitation 2 — Data provider and acquisition metadata

Execution candidate data is Yahoo Finance via yfinance 1.8.0, with `auto_adjust=False` and `actions=True` recorded in the sidecar. It is not official exchange transaction data. `interval`, `group_by`, and exact requested ticker list remain `UNKNOWN`; this audit does not infer them. Coverage counts below are exact joins to the saved snapshot and are not proof that Yahoo contains every exchange session or an authorized execution price.

## Limitation 3 — Historical data revision

Yahoo Finance can revise historical values. The pinned snapshot SHA-256 for this audit is `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`. Other data vintages may differ; no source refresh was performed.

## Limitation 4 — Universe coverage

2026 membership was selected by effective date using the recorded 2026 H1/H2 sets (50 each). The union contains 54 symbols; 1 approved exclusion leaves 53 distinct member symbols in scope. Zero symbols currently meet the full verified-execution and corporate-action eligibility gate, so the verified Tradable Universe has 0 symbols. Among non-excluded member-date rows in the local Yahoo candidate, OHLC is complete for 10,290/10,290 (100.00%); this is candidate completeness only. Verified execution coverage is 0/10,290 (0.00%). The result cannot be described as full-set SET50 coverage.

## Limitation 5 — Execution simulation

Daily Open is a simulation input, not evidence that an order could have been matched at that price or quantity. Yahoo vendor OHLC has not been validated as exchange prints. No orders, portfolio holdings, or strategy returns were created in this audit.

## Limitation 6 — Other securities and corporate actions

No additional whole-year security exclusions were approved. GLOBAL has 141 recorded tick-basis diagnostic rows but is not in either 2026 SET50 membership list, so it is outside this audit's member universe and is not silently repaired or treated as an approved exclusion. 51 non-excluded member symbols have unreconciled corporate-action ledger entries; for the remaining symbols, the absence of a vendor event is not official proof that no action occurred. Excluding securities based on a full-year look-ahead of action events was not applied. The absence of complete, verified official corporate-action and execution records blocks all remaining member securities from trading eligibility.

## Research status

This is a pre-backtest validation only. Critical data and methodology blockers remain. `revised_backtest_gate.json` records `BLOCKED`; 63 combinations were not run.
