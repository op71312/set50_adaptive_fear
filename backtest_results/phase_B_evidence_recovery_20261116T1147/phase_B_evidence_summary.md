# Phase B Evidence Recovery — Summary

## Outcome

**Phase B: BLOCKED. Research Backtest Gate remains CLOSED.** No new official evidence was available locally, and the no-download constraint was honored. No 63-combination backtest, model fit, or source download was performed.

Phase A's saved result was not changed: baseline status `BLOCKED` (12 PASS / 4 BLOCKED criteria as supplied), verified tradable rows 0, candidate data coverage 99.52%, verified coverage 0.00%. All Phase A artifacts were hash-checked before and after this work.

Phase B gate rows: 8 PASS, 1 PASS_WITH_LIMITATIONS, 8 BLOCKED (includes the overall roll-up).

## Findings

1. **Corporate actions / identity:** All 141 ledger events were inspected and remain `UNRESOLVED`; the ledger has no official source URLs, and no event was applied. The 2026 constituent union contains 54 symbols. 52 ledger symbols overlap that union (97 event rows); the no-event symbols are AOT, BTS. Phase A's 53 unresolved non-excluded member-symbol count is a status count, not 53 event-bearing symbols. All 141 event rows and this discrepancy are preserved in the recovery output.
2. **Execution provenance:** The existing sidecar records Yahoo Finance/yfinance 1.8.0, retrieval time `2026-11-15T11:37:11.389684+00:00`, requested range `2026-01-05` to `2026-11-14` exclusive, `auto_adjust=False`, and `actions=True`. The exact ticker list, interval, and group_by remain UNKNOWN. A pre-existing local SET cross-check covers only four recent GLOBAL dates (OHLC match, volumes differ); the source is not exchange-verified for the full execution snapshot.
3. **Missing OHLC:** 253 field-cells are missing: `{"Open": 63, "High": 63, "Low": 63, "Close": 64}` across 64 BANPU rows. All remain unresolved; vendor row presence/volume does not establish holiday, no-trading, or suspension.
4. **Membership/calendar:** 22 period rows and 22 recorded URL pointers were inspected. URLs were not fetched; membership content and transitions remain unverified. The official 2026 calendar file is absent; the 210 observed-date alignments are candidates only.
5. **Universe:** 10500 candidate member-date rows were evaluated; 0 are verified tradable. Existing BANPU/GLOBAL exclusions are preserved; other securities were not blanket-excluded to mask shared-source blockers.

## Regression validation

- Re-ran the notebook synthetic execution/no-lookahead tests in an isolated kernel: **17/17 PASS**.
- Evidence: `phase_B_regression_test_report.csv`; includes `no_future_row_in_date_t_prediction`.
- No backtest combination or model fit was executed.

## Protected-file integrity

Original snapshot SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`  
Immutable copy SHA-256: `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`  
Frozen model SHA-256: `8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7`  
Master dataset, membership, declaration, 05 backtest notebook, Phase A files, and source ledgers unchanged: `True`.

No source data was downloaded; no snapshot/master/membership/model was modified.

## Exact remaining blockers

- **B-CA-01 — Corporate actions (BLOCKED):** 141 unresolved ledger rows; 97 event rows overlap candidate 2026 membership; no official source URL/document. Evidence still needed: Official SET/issuer/SEC notice for each event with security identifier, terms, and effective/ex/record/payment/trading dates; reconcile any affected portfolio quantities/cash.
- **B-ID-01 — Security identity (BLOCKED):** Identity map has 5 rows with statuses {'BLOCKED_SOURCE_URL_REQUIRED': 4, 'BLOCKED_SOURCE_URL_AND_FEATURE_REBUILD_REQUIRED': 1}; no attached official URLs; two merger claims remain unsupported. Evidence still needed: Official issuer/SET/SEC identity and conversion documents, including fractional-share settlement; verified feature identity handling for any transition.
- **B-EX-01 — Execution provenance (BLOCKED):** Provider/timestamp/range/settings partially recorded; exact ticker list, interval, and group_by are UNKNOWN; no exchange-authorized source. Evidence still needed: Complete immutable acquisition manifest or authorized/exchange-verified OHLC source with documented date range and request semantics.
- **B-EX-02 — Missing execution data (BLOCKED):** 253 missing OHLC field-cells across 64 BANPU rows; all causes unresolved. Evidence still needed: Official trading-status evidence and authorized OHLC for each affected date/field, or documented evidence the date was not an official session. No forward/backfill.
- **B-EX-03 — Historical price basis (BLOCKED):** Yahoo vendor snapshot is not exchange-verified; GLOBAL diagnostic has 141 rows with no official action confirmation. Evidence still needed: Exchange-authorized raw execution/valuation basis plus official corporate-action reconciliation for affected symbols/dates.
- **B-MEM-01 — Membership effective dates and transitions (BLOCKED):** 22 period rows and 22 URL pointers exist, but official primary documents were not retrieved; 2017_H1 local row count is 49. Evidence still needed: Primary SET constituents/review documents for each period and validation of every effective date and constituent addition/removal against the local file.
- **B-CAL-01 — Official trading calendar and date alignment (BLOCKED):** Required calendar file exists=False; 210 next-observed date candidates are not official sessions. Evidence still needed: Official SET 2026 trading-session calendar and mapping of each predictor date to the correct execution session.
- **B-UNIV-01 — Non-empty verified universe (BLOCKED):** 10,500 candidate member-date rows; 0 rows satisfy the complete evidence criteria. Evidence still needed: Resolve source, membership/calendar, identity, corporate-action, and execution-price blockers; then reconstruct without relaxing criteria.

## Deliverables

All Phase B outputs are in `D:\Project_Github\set_fear_index\backtest_results\phase_B_evidence_recovery_20261116T1147`:

- `corporate_action_evidence_recovery.csv`
- `corporate_action_recovery_report.md`
- `execution_source_provenance_audit.csv`
- `execution_price_completeness_audit.csv`
- `execution_source_recovery_report.md`
- `membership_primary_evidence_audit.csv`
- `trading_calendar_evidence_audit.csv`
- `membership_calendar_recovery_report.md`
- `tradable_universe_2026_phase_B.csv`
- `execution_excluded_symbols_phase_B.csv`
- `tradable_universe_coverage_phase_B.csv`
- `phase_B_gate.csv`
- `phase_B_blocker_register.csv`
- `phase_B_regression_test_report.csv`

The builder and `phase_B_manifest.json` are also retained for reproducibility and integrity evidence.
