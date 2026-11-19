# Revised Research Backtest — Final Audit

- Audit ID: `revised_research_audit_20261116T031343Z_01b34b3d`
- Created UTC: `2026-11-16T03:13:43.412694+00:00`
- Final decision: **BLOCKED**. Validation only; no Backtest combinations ran.

| Audit Category | Status | Evidence | Verification Result |
|---|---|---|---|
| Original Data Integrity | PASS | `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet` | Original and immutable-copy hash match pinned SHA-256 before/after. |
| Acquisition Provenance | BLOCKED | `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json` | auto_adjust=False/actions=True recorded; interval/group_by/ticker list UNKNOWN. |
| BANPU Exclusion | PASS_WITH_LIMITATIONS | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\execution_excluded_symbols.csv` | Approved full-year portfolio eligibility exclusion; no source/model deletion. |
| Other Security Exclusions | PASS_WITH_LIMITATIONS | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\revised_research_audit.csv` | No additional exclusions approved; 52 member symbols have unresolved vendor-action entries. |
| Tradable Universe | BLOCKED | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\tradable_universe_2026.csv` | 54 distinct original members; 1 excluded; 0 fully eligible. |
| Execution Data Coverage | BLOCKED | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\execution_eligible_data_audit.csv` | Candidate OHLC complete 100.00%; verified execution coverage 0.00%. |
| Corporate Actions | BLOCKED | `D:\Project_Github\set_fear_index\backtest_results\corporate_action_ledger_official.csv` | No official action terms and accounting across eligible members. |
| Point-in-Time Membership | PASS | `D:\Project_Github\set_fear_index\dataset\set50_declare_dates_2016_2026.csv` | 2026 H1/H2 effective dates used, 50 members per period. |
| No Lookahead | BLOCKED | `D:\Project_Github\set_fear_index\06_research_backtest.ipynb` | Full feature provenance and validated session calendar remain unresolved. |
| Execution Engine | PASS_WITH_LIMITATIONS | `D:\Project_Github\set_fear_index\06_research_backtest.ipynb | D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\revised_backtest_manifest.json` | 17 synthetic checks were rerun and pass; results are recorded in the revised manifest. No market-data verification. |
| Portfolio Accounting | BLOCKED | `D:\Project_Github\set_fear_index\backtest_results\corporate_action_ledger_official.csv` | Synthetic tests do not resolve missing corporate action accounting. |
| Allocation Methods | BLOCKED | `D:\Project_Github\set_fear_index\06_research_backtest.ipynb` | Only EW and IV are implemented; all seven methods are not ready. |
| Research Limitations | PASS | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\research_data_limitations.md` | Six limitations documented. |
| Final Backtest Gate | BLOCKED | `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\revised_backtest_gate.json` | Do not run 63 combinations. |

## Coverage and exclusions
- Original membership: 54 distinct symbols across 2026 H1/H2; 50 per effective period.
- Approved whole-year exclusions: 1 (BANPU).
- Distinct remaining membership symbols: 53.
- Verified eligible Tradable Universe symbols: 0.
- Non-excluded member-date rows: 10,290; candidate rows with complete OHLC: 10,290 (100.00%).
- Fully verified execution rows: 0 (0.00%); missing candidate OHLC cells after BANPU exclusion: 0.
- Unresolved official corporate-action event symbols among 2026 member list: 52.

## Gate decision
- Gate A — Source Data Integrity: **BLOCKED**.
- Gate B — Eligible Universe Integrity: **BLOCKED**.
- Gate C — Research Backtest Integrity: **BLOCKED**.
- Backtest Gate remains **CLOSED**. Do not execute 63 combinations.

### Critical blockers
- **Acquisition provenance is complete** (A — Source Data Integrity): provider=Yahoo Finance via yfinance.download; auto_adjust=False; actions=True; interval=UNKNOWN; group_by=UNKNOWN; requested_ticker_list=UNKNOWN. Evidence: `D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json | D:\Project_Github\set_fear_index\backtest_results\execution_data_lineage.json`.
- **Execution source is official or authorized** (A — Source Data Integrity): Yahoo candidate is not exchange-authorized; verified dataset and official patch are absent. Evidence: `D:\Project_Github\set_fear_index\backtest_results\verified_execution_data_status.json`.
- **Verified execution coverage for remaining members** (B — Eligible Universe Integrity): 0/10290 rows satisfy the full source authorization, price and action criteria (0.00%); no verified source. Evidence: `D:\Project_Github\set_fear_index\backtest_results\revised_research_audit_20261116T031343Z_01b34b3d\execution_eligible_data_audit.csv | D:\Project_Github\set_fear_index\backtest_results\verified_execution_data_status.json`.
- **Corporate action and identity basis for remaining members** (B — Eligible Universe Integrity): 51 of 53 non-excluded member symbols have unresolved vendor-action rows; no full official negative/positive action ledger. Evidence: `D:\Project_Github\set_fear_index\backtest_results\corporate_action_ledger_official.csv | D:\Project_Github\set_fear_index\backtest_results\security_identity_mapping.csv`.
- **No lookahead and six-feature input lineage** (C — Research Backtest Integrity): Feature-only/unit future-row tests pass, but full point-in-time feature provenance and validated execution calendar are not established. Evidence: `D:\Project_Github\set_fear_index\06_research_backtest.ipynb | D:\Project_Github\set_fear_index\dataset\verified_build_20261113_152948\SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet`.
- **Portfolio accounting and corporate action reconciliation** (C — Research Backtest Integrity): Synthetic accounting tests pass, but 141 ledger rows are not officially reconciled or applied by the portfolio engine. Evidence: `D:\Project_Github\set_fear_index\backtest_results\corporate_action_ledger_official.csv`.
- **All seven allocation methods implemented and reviewed** (C — Research Backtest Integrity): Only EW and IV are implemented; ERC, HRP, MinVar, CVaR and MPT are not ready. Evidence: `D:\Project_Github\set_fear_index\06_research_backtest.ipynb`.
- **CVaR formulation and no-all-cash constraint** (C — Research Backtest Integrity): Objective/constraints have not been approved. Evidence: `D:\Project_Github\set_fear_index\06_research_backtest.ipynb`.
- **Board lot, stale valuation, covariance and fallback policies** (C — Research Backtest Integrity): At least one required policy remains unset; none inferred or defaulted. Evidence: `D:\Project_Github\set_fear_index\06_research_backtest.ipynb`.

## Final answers
1. Excluded symbols: **1** approved (BANPU).
2. Fully verified Tradable Universe: **0** symbols; 53 distinct symbols remain in the membership candidate set.
3. Candidate OHLC completeness after BANPU exclusion: **100.00%**; verified execution coverage: **0.00%**.
4. Critical blockers remain: **Yes (9 checks)**.
5. Ready to run 63 combinations: **No — BLOCKED**.

No source prices were filled or edited, no Yahoo download was performed, no model was retrained, and no results were generated.
