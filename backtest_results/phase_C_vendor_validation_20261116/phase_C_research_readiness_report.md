# Phase C Research Readiness — Vendor-Based Validation

## Decision

**Candidate universe: non-empty. Research Backtest Gate: BLOCKED and remains closed.**

Approach B accepts Yahoo Finance/yfinance as a third-party historical market-data vendor. It is not described as official SET execution data. The candidate universe contains **1 eligible symbol(s)** and **4 member-date rows**: AOT. These are bounded research candidates, not an approval to run a portfolio backtest.

## Phase comparison

| Phase | Existing result | Candidate member-date rows evaluated | Tradable rows / candidates (not approved) | Gate |
|---|---|---:|---:|---|
| Phase A | {'PASS': 12, 'BLOCKED': 4} | 10,500 | 0 | BLOCKED |
| Phase B | {'PASS': 8, 'BLOCKED': 7, 'PASS_WITH_LIMITATIONS': 1} | 10,500 | 0 | BLOCKED |
| Phase C | Yahoo vendor approach; official 2026 membership recovered | 10,500 | 4 | BLOCKED |

Phase A and Phase B artifacts and results were preserved, not rewritten.

## Provenance and price quality

- Execution data: Yahoo Finance/yfinance 1.8.0, retrieval `2026-11-15T11:37:11.389684+00:00`, requested `2026-01-05` to `2026-11-14` exclusive, `auto_adjust=False`, `actions=True`.
- Exact execution ticker list, `interval`, `group_by`, and source timezone remain **UNKNOWN**. The snapshot and immutable copy both match pinned SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`.
- Feature acquisition source code uses `auto_adjust=True`; the pinned Master and execution snapshot are separate acquisitions with different price-adjustment settings. The exact feature downloader run is not bound to the Master hash by a run manifest.
- Missing OHLC remains {'Open': 63, 'High': 63, 'Low': 63, 'Close': 64} (253 field-cells), all on BANPU. No forward-fill, backfill, interpolation, zero fill, or price correction occurred.
- Snapshot-wide execution quality has 0 invalid/nonpositive OHLC rows, 62 missing-volume rows, 30 zero-volume rows, 3070 repeated observed closes, and 141 GLOBAL price-basis anomaly field-rows. Repeated prices/zero volume are not interpreted as suspension or stale status.

## BANPU / GLOBAL

- BANPU remains excluded for all of 2026 with reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`; the original missing OHLC cells remain documented.
- The missing execution OHLC rows do not feed the feature pipeline. Separately, BANPU feature observations do enter cross-sectional ranks/market proxy while present. Notebook 06 now filters approved exclusions before model inference, and the candidate universe excludes predictor dates until the 60-observation shared-feature washout. The four eligible AOT rows are after that window.
- GLOBAL remains excluded by existing policy. Its 141 anomalies are GLOBAL-only and do not establish a split. GLOBAL is not a 2026 SET50 constituent in either official PDF.

## Corporate actions and identity

- All 141 corporate-action ledger rows remain unconfirmed and unapplied; 97 event rows across 52 symbols overlap the official 2026 member union. Event-bearing member securities are excluded from the candidate universe. AOT has no local event record and no nonzero Yahoo Dividends/Stock Splits row; this is vendor evidence, not official confirmation.
- BANPU identity/merger claims remain unresolved and BANPU is excluded. AOT is continuous at the local vendor-ticker-key level only; no official issuer-ID claim is made.

## Membership / calendar

- Official SET H1 and H2 2026 PDFs were retrieved and match all 50 and 50 local constituent names respectively.
- The 2017_H1 local membership row remains unresolved: 49 nonblank unique names, one blank slot, no primary source. Phase A's 50 count was for 2026 daily membership, not 2017. Because the frozen model training period is `2016-2024`, the historical model context remains a research-validity blocker.
- The official trading calendar is unavailable. Candidate execution dates use the next observed date in the pinned Yahoo snapshot, not a generic weekday calendar.

## Exact remaining blockers

1. Board-lot, stale-valuation and fallback policies are unresolved.
2. CVaR formulation is not approved; allocation methods were not modified.
3. 2017_H1 historical membership and its relationship to frozen-model training features remain unresolved.
4. Full execution request semantics (exact ticker list, interval, grouping, timezone) remain unknown.
5. 141 action-ledger events have no verified primary terms; event-bearing 2026 symbols are excluded.
6. No official 2026 session calendar is present; only vendor-observed date alignment is supported.

## Stop conditions and regression

- 63 portfolio combinations run: **No**.
- Model fit/retrain: **No**.
- Source data or Notebook 05 modified: **No**.
- Actions applied, missing prices filled, or Research Gate opened: **No**.
- Notebook 06 synthetic regressions: **18/18 PASS**, including exclusion before model inference.
- The serialized Notebook 06 output matches the fresh run result (18/18); fresh execution evidence is in `notebook_06_synthetic_regression_results.csv`.
- Original snapshot, immutable copy, Master, frozen model, membership, declarations and Phase A/B evidence hashes: **unchanged**.

See `phase_C_gate.csv`, `phase_C_blocker_register.csv`, `phase_C_manifest.json`, and the focused reports for evidence paths.
