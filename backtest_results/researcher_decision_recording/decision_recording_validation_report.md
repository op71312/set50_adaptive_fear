# Workstream 1.8 — Decision Recording Validation

## Source coverage

The actual local canonical register, its original schema and E-004/E-029 rows, the
Phase E revision changelog, and the directly mirrored E2, E5, Phase E summary,
validation report, and manifest were reviewed. The canonical register remains the
status source. No missing referenced source was used to infer approval.

## Register validation

- Register schema retained: **10 columns**.
- Register decision rows retained: **29**; no decision IDs added or removed.
- E-004: original `NEEDS_RESEARCHER_APPROVAL`; final `APPROVED`, Option B, 252 verified
  session intervals/year, minimum 252 valid consecutive return intervals / 253 equity
  marks; shorter segments unannualized.
- E-029: original `NEEDS_RESEARCHER_APPROVAL`; final `APPROVED`, Option B, all five
  lineage references mandatory at run/snapshot level; `Risk_Data_Hash` separately
  required; no historical backfill; future missing/inconsistent lineage is
  `PROVENANCE_INCOMPLETE`.
- Row/field comparison against the pre-edit register: only E-004 and E-029 differ;
  no unrelated decision row changed.
- Final register SHA-256:
  `7cc61072a253a358c7613f2e9fb29ed57a52a5c80eaf0312951d75c8e3bd8c92`.

## Changelog and mirror validation

- The two approval entries are appended in the existing changelog format, dated
  `2026-11-17`, with prior entries preserved.
- E2, E5, Phase E summary, validation report, and manifest mirror the E-004/E-029
  approval scope.
- The manifest reports **20 `APPROVED`**, **4 `APPROVED_EXISTING`**, **1
  `NEEDS_RESEARCHER_APPROVAL`**, **3 `BLOCKED`**, and **1 `VERIFIED`** decisions.
- E-001 remains `BLOCKED`; E-002 remains `NEEDS_RESEARCHER_APPROVAL`; E-005 through
  E-020 remain `APPROVED`; E-021 and E-022 remain `BLOCKED`; E-023 remains `VERIFIED`
  baseline only; E-027 and E-028 remain `APPROVED`.
- Risk-free Rate and MAR remain separately `NEEDS_RESEARCHER_APPROVAL`; neither is
  approved by E-004.
- `Risk_Data_Hash` remains required.

## Protected-file and prohibited-action checks

The fresh repository-wide SHA-256 comparison is documented in
`protected_file_integrity_report.md`: all changes are limited to the seven permitted
Phase E documents and the five requested deliverables; no other baseline hash mismatch
or missing file was found.

No Notebook 05/06, model, dataset, archived output, execution data, or portfolio result
was modified. No market data or internet source was accessed; no model, prediction,
allocation method, optimizer, synthetic test, or historical backtest was run for this
workstream. The pre-existing Phase E synthetic suite is documented as predating the
E-004/E-029 recording and does not validate implementation of either approval.

## Final stop conditions

- `E004 = APPROVED`
- `E029 = APPROVED`
- `RISK_FREE_RATE = NEEDS_RESEARCHER_APPROVAL`
- `MAR = NEEDS_RESEARCHER_APPROVAL`
- `RISK_DATA_HASH = REQUIRED`
- `RESEARCH_BACKTEST_GATE = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`

## Final validation result

Register row/field comparison, changelog append-only check, mirrored status/count
checks, Phase E output-hash checks, and repository-wide protected-file comparison
passed. The deliverable checksum file was verified against the other four requested
deliverables.

`WORKSTREAM_1_8 = COMPLETED`

`E004 = APPROVED`

`E029 = APPROVED`

`RESEARCH_BACKTEST_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`
