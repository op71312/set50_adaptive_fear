# Workstream 1.9.1 — Decision and Scope Integrity

## Canonical decision status verification

The canonical source
`backtest_results\phase_E_portfolio_specification\phase_E_decision_register.csv`
was read without modification. E-004/E-029 remain approved under the recorded
researcher decisions. This workstream does not approve any new decision or alter
any status.

| Decision / policy | Required preserved status | Workstream 1.9.1 check |
|---|---|---|
| E-004 | `APPROVED`, Option B | Preserved. Annualization uses 252 verified exchange-session intervals/year and is permitted only with at least 252 valid consecutive one-session return intervals (253 valid equity marks). |
| E-029 | `APPROVED`, Option B | Preserved. Five run/snapshot lineage references remain required; no archived identifiers are inferred or backfilled. |
| E-001 | `BLOCKED` | Preserved; no verified effective-dated primary board-lot schedule was introduced. |
| E-002 | `NEEDS_RESEARCHER_APPROVAL` | Preserved; odd-lot/residual treatment remains unresolved. |
| Risk-free Rate | `NEEDS_RESEARCHER_APPROVAL` | Preserved as a separate researcher decision; E-004 does not approve it. |
| MAR | `NEEDS_RESEARCHER_APPROVAL` | Preserved as a separate researcher decision; E-004 does not approve it. |
| `Risk_Data_Hash` | `REQUIRED` | Preserved under E3; it remains separate from the five E-029 references. |
| E-005 through E-020 | `APPROVED` specifications | Preserved. Approval defines policy; it is not evidence that implementation or historical results satisfy that policy. |
| E-021 / E-022 | `BLOCKED` | Preserved. |
| E-023 | `VERIFIED` baseline only | Preserved; does not establish multi-security or seven-method readiness. |
| E-027 / E-028 | `APPROVED` | Preserved; no changes made. |

## Change record

- Canonical Decision Register changed: **No**.
- Decision approval statuses changed: **No**.
- Phase E specifications changed: **No**.
- Workstream 1.9 deliverables changed: **No**. Corrections are confined to the
  new Workstream 1.9.1 folder, including a corrected copy of the relevant
  evidence-inventory rows.
- Research Backtest Gate opened: **No**.
- Phase F started: **No**.

## Ongoing stop conditions

`RESEARCH_BACKTEST_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`

Approach B changes which execution-price source is acceptable; it does not
resolve source metadata, missing OHLC, corporate-action/security identity,
calendar, universe, model/archive lineage, risk-panel, implementation, or
researcher-decision blockers.
