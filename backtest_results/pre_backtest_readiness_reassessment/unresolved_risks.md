# Unresolved Risks

**Overall classification:** `BLOCKED` for a historical research backtest.

This list distinguishes verified facts from potential impact. All paths refer to local repository files; no external evidence was sought.

## Critical evidence gaps

1. **Corporate actions — BLOCKED**
   - Verified from local records: 141 ledger rows; zero official source URLs; zero officially verified rows; zero confirmed impacts in Phase D; zero applied actions.
   - Potential scope: 97 rows overlap the 2026 membership union and 89 recorded event dates fall inside the affected symbol's active 2026 membership. Eight other union-overlap rows are outside active membership on their recorded date; 44 rows concern nonmembers.
   - Risk: terms, security IDs, effective/ex/record/payment/trading dates, and price/share/cash treatment remain unknown. The recorded date only supports scoping; it is not evidence that the event occurred on that date.
   - Evidence: [corporate_action_ledger_official.csv](../corporate_action_ledger_official.csv), [phase_D_corporate_action_scope.csv](../phase_D_universe_consistency_20261116/phase_D_corporate_action_scope.csv), [phase_D_corporate_action_report.md](../phase_D_universe_consistency_20261116/phase_D_corporate_action_report.md).

2. **BANPU identity, execution gaps and features — BLOCKED**
   - BANPU's full-2026 exclusion remains unchanged.
   - The identity map lacks primary identity/conversion evidence and verified new-identity features. The snapshot contains 253 missing OHLC field-cells across 64 BANPU rows.
   - Risk: identity continuity, trading status, historical price/quantity continuity and a valid feature rebuild are not established. Do not infer a split or merge terms.
   - Evidence: [security_identity_mapping.csv](../security_identity_mapping.csv), [banpu_missing_data_audit.csv](../banpu_missing_data_audit.csv), [phase_D_feature_consistency_report.md](../phase_D_universe_consistency_20261116/phase_D_feature_consistency_report.md).

3. **GLOBAL price basis — BLOCKED; nonmembership scope PASS_WITH_LIMITATIONS**
   - Official 2026 SET50 PDFs exclude GLOBAL; the precautionary exclusion remains.
   - A 141-field-row diagnostic across 36 dates is not official corporate-action evidence. The recent local SET cross-check covers only four dates and is insufficient to validate the full price history.
   - Risk: historical price basis/tick schedule and any action terms remain unresolved. No split claim or correction is accepted.
   - Evidence: [global_tick_basis_diagnostic.csv](../global_tick_basis_diagnostic.csv), [global_set_recent_crosscheck.csv](../global_set_recent_crosscheck.csv), [security_identity_report.md](../phase_C_vendor_validation_20261116/security_identity_report.md).

4. **Execution provenance and source authorization — BLOCKED**
   - Known metadata is captured in the snapshot sidecar and lineage. Unknown fields are the exact requested ticker list, `interval`, `group_by`, and source timezone.
   - Yahoo Finance/yfinance is third-party vendor data, not verified official SET execution data. The observed 83 symbols do not establish the original request list.
   - Risk: source basis, full request parameters, and authorized execution provenance cannot be reproduced from the sidecar alone.
   - Evidence: [execution_data_lineage.json](../execution_data_lineage.json), [vendor_provenance_recovery.csv](../phase_C_vendor_validation_20261116/vendor_provenance_recovery.csv), [execution source recovery report](../phase_B_evidence_recovery_20261116T1147/execution_source_recovery_report.md).

5. **Historical membership — 2017_H1 BLOCKED**
   - The local row has 49 names and one blank slot. No primary SET membership evidence was found. The model was trained over 2016–2024 and the feature Master has unresolved 2017 membership/context effects.
   - Risk: the missing constituent and its feature/rank/target effects cannot be identified locally. No name or data should be guessed.
   - Evidence: [membership_reconciliation_2017.csv](../phase_C_vendor_validation_20261116/membership_reconciliation_2017.csv), [phase_D_2017_membership_report.md](../phase_D_universe_consistency_20261116/phase_D_2017_membership_report.md).

6. **Official exchange-session calendar — BLOCKED**
   - No verified SET calendar covering required execution dates is present in the inspected repository evidence. The 210 Phase C predictor-date rows all have `Official_Trading_Session_Verified=False`.
   - Risk: next-observed vendor dates cannot validate execution alignment or Phase E stale-session ages. Weekdays and Yahoo rows are not substitutes.
   - Evidence: [trading_calendar_evidence_audit.csv](../phase_B_evidence_recovery_20261116T1147/trading_calendar_evidence_audit.csv), [tradable_universe_coverage_phase_C.csv](../phase_C_vendor_validation_20261116/tradable_universe_coverage_phase_C.csv).

7. **Universe and common risk panels — BLOCKED**
   - One vendor-based AOT candidate symbol and four candidate member-date rows; zero fully verified tradable rows. The remaining symbols are excluded or fail feature/execution requirements.
   - Risk: no multi-security allocation universe; common-complete-date rules cannot be used to silently drop symbols. Required 60/252 valid historical observations on the complete Buy universe are not established.
   - Evidence: [phase_D_symbol_eligibility.csv](../phase_D_universe_consistency_20261116/phase_D_symbol_eligibility.csv), [phase_D_gate.csv](../phase_D_universe_consistency_20261116/phase_D_gate.csv), [E3_risk_estimation_policy.md](../phase_E_portfolio_specification/E3_risk_estimation_policy.md).

8. **Implementation alignment — BLOCKED**
   - Notebook 05 remains a legacy prototype with `BOARD_LOT=100`, 5-calendar-day stale threshold, legacy 50/200 history constants, Ledoit-Wolf covariance, and EW fallbacks; its HRP mixes sample correlation and shrinkage covariance. Its CVaR uses a ceiling tail and SLSQP.
   - Notebook 06 has `BOARD_LOT_SIZE`, `MAX_STALE_CALENDAR_DAYS`, `COVARIANCE_ESTIMATOR`, `CVAR_FORMULATION`, and `ALLOCATOR_FALLBACK_POLICY` unset; only EW and IV are implemented and five methods are rejected by guards.
   - Risk: Phase E approval is not implementation or compatibility verification. No notebook execution was performed.
   - Evidence: read-only source cells in [05_backtest.ipynb](../../05_backtest.ipynb) and [06_research_backtest.ipynb](../../06_research_backtest.ipynb); [phase_E_validation_report.md](../phase_E_portfolio_specification/phase_E_validation_report.md).

## Open policy decisions

- E-001 effective-dated board-lot schedule: `BLOCKED`.
- E-002 odd-lot treatment: `NEEDS_RESEARCHER_DECISION`.
- E-004 segment annualization convention: `NEEDS_RESEARCHER_DECISION`.
- E-029 additional snapshot/version fields: `NEEDS_RESEARCHER_DECISION`.

E-005 through E-020 are approved in the register. Do not reopen them or infer approval for E-001/E-002/E-004/E-029.

## Gate impact

The 2026 membership evidence and Phase E decisions improve bounded sub-scopes only. Corporate-action, identity, execution, historical membership, calendar, universe, method implementation, and board-lot blockers remain. Research Backtest Gate stays `BLOCKED`; Phase F stays `DO_NOT_BEGIN`.
