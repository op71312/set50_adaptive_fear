# Consolidation Validation Report

## Result

**Evidence consolidation: PASS_WITH_LIMITATIONS**  
**Historical readiness: BLOCKED**  
**Research Backtest Gate: BLOCKED**  
**Phase F: DO_NOT_BEGIN**

The validation confirms internal consistency of this consolidation and preservation of
the existing repository. It does not validate historical prices, model suitability,
backtest performance, or policy approval beyond the existing Phase E register.

## Source coverage

The companion `source_evidence_inventory.csv` records the discovered report/artifact
paths, SHA-256 where readable, report date only when explicitly available, original
status/classification, whether content was reviewed or only hashed, and scoped
limitations. It includes Phase A-E, readiness reassessment, Workstreams 1.1-1.5,
corporate-action classification, relevant protected inputs, official 2026 membership
PDFs, and the archived result package.
The inventory contains **197 rows**: 196 present/hashable sources (189 text-readable,
7 binary-hashed) and one explicit `NOT_FOUND` record for the original Phase A narrative.
All present-source hashes and paths resolve; no missing source path remains in the
blocker register.

The original standalone Phase A narrative report was not found in the repository search.
Four later `phase_A_gate.csv` snapshots were found. Phase B's 12 PASS / 4 BLOCKED
carry-forward is preserved as a secondary report reference, not recreated as a missing
Phase A report.

Source conflicts preserved:

1. 2017_H1 is consistently 49 known names, but reports differ between 49 listed slots
   and 50 slots with one blank. Six listed symbols are absent from Master rows over 120
   dates; total known missing member-date rows are 720.
2. Corporate-action row counts use different definitions: 136 vendor-origin ledger
   rows plus five claims (Phase B), 137 nonzero vendor action fields (Phase C), and 138
   secondary-supported plus three candidate-only rows (later classification). Total
   ledger count is 141; no primary event or impact is confirmed.
3. Phase A summary counts are carried forward from Phase B; the original detailed Phase
   A narrative source is `NOT_FOUND`.

## Decision and blocker checks

| Check | Result | Evidence |
|---|---|---|
| CSV structure | PASS | All five CSV deliverables parse with every data row matching its header width. |
| Blocker register | PASS | 27 blockers: 23 `BLOCKED`, 1 `PASS_WITH_LIMITATIONS`, 3 `NEEDS_RESEARCHER_DECISION`; 14 Critical and 13 High. All dependencies resolve; all referenced source paths are in the inventory. |
| Phase E E-005..E-020 statuses | PASS | Exactly 16 entries are `APPROVED` in the Phase E register; each is labeled `APPROVED_SPECIFICATION_ONLY` in this consolidation. |
| Remaining Phase E statuses | PASS | E-001 remains evidence-blocked; E-002/E-004/E-029 remain `NEEDS_RESEARCHER_APPROVAL`; E-021/E-022 remain `BLOCKED`; E-023 is `VERIFIED` as baseline only. E1's source/coverage approval dependency is noted without status promotion. |
| Phase E status totals | PASS | 29 decisions: 18 APPROVED, 4 APPROVED_EXISTING, 3 NEEDS_RESEARCHER_APPROVAL, 3 BLOCKED, 1 VERIFIED. |
| 2026 membership | PASS | Official local SET PDF evidence: H1/H2 50/50, 54-symbol union; no inference to calendar/prices. |
| Corporate-action scope | PASS_WITH_LIMITATIONS | 141 rows, 0 primary, 0 confirmed impact, 0 applied; 97/89/8 scopes preserved with recorded-date limitation. |
| Execution provenance and quality | PASS_WITH_LIMITATIONS | Known and unknown request fields separated; 253 missing OHLC cells remain; Yahoo is not labeled official SET execution data. |
| Universe/method readiness | PASS | AOT-only 1 symbol/4 vendor candidate rows; fully verified rows 0; historical allocation methods 0/7; Notebook 06 support 2/7. |
| Archived model/risk/allocation/performance claims | PASS | Unknown links and archived limitations remain explicit; no reconstruction or replacement metrics. |
| Output path scope | PASS | Nine requested deliverables and the checksum manifest are confined to `backtest_results/research_backtest_readiness_consolidation/`. |
| Output hashes | PASS | All nine deliverable hashes in `SHA256SUMS.txt` verify; the SHA file excludes its own digest. |
| Protected input integrity | PASS | Compared the repository-wide pre-audit baseline of 20,096 files, excluding only `.git` and the new output directory: 20,096 unchanged; 0 hash mismatches, 0 missing, and 0 unexpected files outside the output directory. |
| Prohibited actions | PASS | No internet, market data download, yfinance call, model operation, notebook execution, optimizer, historical backtest, synthetic market data, or gate override was performed. |

## Final integrity results

To be completed after output generation and the exact pre-audit hash comparison:

- Pre-audit baseline files: **20,096**
- Unchanged protected files: **20,096**
- Hash mismatches: **0**
- Missing protected files: **0**
- Unexpected files outside the new consolidation directory: **0**
- Required deliverables present: **9 / 9**
- Companion source inventory present: **197 records; 196 present-source hashes verified; 1 explicit NOT_FOUND**
- Output SHA-256 verification: **PASS (9 / 9 deliverables; checksum file excludes itself)**

## Final stop

No evidence or specification change in this consolidation clears a critical gate
blocker. Preserve:

`RESEARCH_BACKTEST_READINESS = BLOCKED`  
`RESEARCH_BACKTEST_GATE = BLOCKED`  
`PHASE_F = DO_NOT_BEGIN`
