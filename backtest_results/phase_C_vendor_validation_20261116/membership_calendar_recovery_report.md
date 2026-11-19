# Membership Reconciliation — Phase C

## 2026 membership

- Retrieved and text-extracted the SET-hosted H1 and H2 2026 PDFs cited by the local declaration file.
- Each official PDF contains 50 unique constituents and matches the corresponding 50-symbol local row exactly (H1: 50/50; H2: 50/50).
- Effective dates match the local declaration file: 2026-01-01 and 2026-07-01. The verified 2026 union has 54 symbols.
- PDFs and extracted text are retained under `sources/`; their SHA-256 values are in `membership_2026_primary_evidence_audit.csv` and the manifest.

## 2017_H1 discrepancy

- The local 2017_H1 row has 50 slots, 49 nonblank unique symbols, 0 duplicates, and 1 blank slot.
- Phase A's `SET50_Members == 50` check is computed over its 2026 predictor dates. Phase B counts every period row and found 49 names for 2017_H1. These are different counting units; the audits are not contradictory and neither count indicates an implementation error.
- The local 2017 source URL is MGR Online (secondary), not a primary SET document. No official 2017_H1 list was established; the missing symbol is not filled.
- The Master has 68 symbols labeled 2017_H1 and 67-68 symbols on its dates. That label does not reconcile the local 49-name claim.
- Since the frozen model's training period is `2016-2024`, this remains an unresolved historical model-context issue. It does not change the officially verified 2026 membership dates or the AOT candidate membership.

No historical membership or declaration file was modified.
