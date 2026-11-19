# E2 — Valuation, Missing Data, and Stale Price Policy

## Evidence and status

The Phase C vendor audit found 253 missing OHLC field-cells, all on BANPU; 62 missing
volume rows, 30 zero-volume rows, and 3,070 repeated observed closes. Repetition and zero
volume were explicitly not treated as proof of staleness or suspension. The 2026 exchange
calendar is unavailable. The 2026 snapshot is third-party Yahoo Finance data, not official
SET execution data.

The legacy [05_backtest.ipynb](../../05_backtest.ipynb) uses a five-calendar-day stale
limit and, when `Trading_Eligible` is absent, filters candidate Close rows using positive
Volume. Those are prototype mechanics, not approved historical rules; positive volume
does not prove an official session or validate a security's price. The
[06_research_backtest.ipynb](../../06_research_backtest.ipynb) leaves the stale threshold
unset and blocks when no approved value is supplied.

## Decision table

| Scenario | Required behavior | Audit output |
|---|---|---|
| Missing Open | No execution; do not substitute Close, prior Open, or an estimated price. Keep an unfilled/blocked order and do not spend its budget. | `Execution_Status=MISSING_OPEN`, `Order_Blocked_Reason`, `Decision_Date`, `Execution_Date`, `Source_Row_ID` |
| Missing Close for a held security | Carry the last verified Close as a valuation mark for at most 3 subsequent verified exchange sessions, labeling it stale. At age >3, mark the holding and portfolio valuation unavailable. Never insert zero. | `Valuation_Status=STALE_CARRIED` or `VALUATION_UNAVAILABLE`, `Price_Date`, `Stale_Observed_Sessions`, `Valuation_Source` |
| Zero or missing Volume | Treat as a data observation, not proof of suspension/non-trading. Require verified session/status evidence to classify a suspension. | Raw volume, `Volume_Status`, `Trading_Status_Evidence`; no inferred suspension flag |
| Repeated Close | Retain as observed; do not label stale solely from repetition. Evaluate only with a documented session calendar and independent status/quote evidence. | `Repeated_Close_Count`, `Is_Repeated_Close`, separate from `Is_Stale` |
| No Date-Symbol row | Do not fill OHLC or return. Determine whether the date is an exchange session from a verified calendar; otherwise status is unknown and eligibility/valuation is blocked. | `Row_Present=False`, `Session_Status=UNKNOWN` unless evidenced, `Data_Gap_Reason=UNRESOLVED` |
| Corporate-action price discontinuity | Quarantine the affected price/position continuity until event terms, effective date, and identity are verified. Do not rescale prices or shares from alignment diagnostics. | `Corporate_Action_Status=UNRESOLVED`, `Price_Basis_Status=UNRESOLVED`, `Position_Accounting_Status=BLOCKED` |

## Stale-session age and portfolio-level valuation state

For each held security, let `P` be the date of the last valid, observed Close and let the
verified exchange calendar define sessions after `P`:

- The valid observed Close date `P` has `Stale_Observed_Sessions = 0`.
- For each subsequent verified exchange session with no valid Close for the held
  security, increment the age by one. The first such session has age 1.
- A later verified session with a valid observed Close resets age to 0 and becomes the
  new `Price_Date`.
- Calendar days, vendor-observed rows, and unverified dates do not increment or reset
  this counter. Yahoo rows are not a substitute for an official session calendar.
- If session status cannot be established from the verified calendar, the age and
  valuation state cannot be certified; do not silently count or skip the date.

Assign one portfolio-level state per valuation date:

| State | Definition | Metrics |
|---|---|---|
| `PORTFOLIO_VALUE_VALID` | Every held position has a valid observed Close for the valuation session, and all required position/corporate-action accounting is resolved. | May be used in performance calculations subject to the other research gates. |
| `PORTFOLIO_VALUE_STALE` | No position is unvalued, but at least one held position uses a carried Close at age 1–3 verified exchange sessions. | Report as stale and disclose affected positions/value. Do not use any return interval touching this value; evaluate only separate valid contiguous segments. |
| `PORTFOLIO_VALUE_UNAVAILABLE` | Any held position has no valid current or permitted carried mark, stale age exceeds 3 sessions, session count is unverified, or material identity/corporate-action accounting is unresolved. | The entire portfolio equity is unavailable. Do not calculate performance metrics for this date, replace the value with zero, or skip it as if it were a valid date. |

This aggregation is intentionally conservative: a portfolio cannot be labeled fully
valid while any held position lacks a defensible mark.

## Return series, unavailable dates, and contiguous segments

A carried-forward Close can be shown as a flagged valuation mark under an approved stale
policy, but it **must not create a zero return**. Exclude every return interval whose
start or end portfolio value is `PORTFOLIO_VALUE_STALE` or
`PORTFOLIO_VALUE_UNAVAILABLE`. Keep its return as unavailable with a reason; do not
calculate a daily return from a carried mark.

An unavailable/stale date breaks the return series. The next valid portfolio value after
the gap starts a new segment; it is not connected to the previous valid equity as an
ordinary one-session return. Retain the missing interval and reason in the audit output.

**Approved segmented reporting policy:**

- A contiguous segment consists only of consecutive verified exchange-session ordinals
  for which portfolio values are `PORTFOLIO_VALUE_VALID`. Any stale/unavailable value,
  unverified session, or nonconsecutive ordinal closes the segment.
- Calculate a one-session return only when both endpoints are valid and their verified
  session ordinals differ by exactly one. Do not bridge gaps.
- Report performance metrics separately for each segment. At minimum, report each
  segment's start/end date, starting/ending equity, number of valid
  one-session intervals, verified session elapsed count, calendar elapsed days, and
  cumulative return `E_end/E_start - 1` separately. Do not concatenate segment returns
  or pool them into a purported full-period equity curve.
- Segment drawdown is reset at the segment's first valid equity and must be labeled
  `SEGMENT_MAX_DRAWDOWN`; it is not a full-period maximum drawdown.
- Do not report full-period CAGR, Sharpe, Sortino, volatility, or maximum drawdown as if
  the equity series were complete when any valuation gap exists. Under E-004 Option B,
  approved 2026-11-17, use 252 verified exchange-session return intervals per nominal
  year. Annualized segment metrics are permitted only when the segment contains at
  least 252 valid consecutive one-session return intervals (253 valid equity marks).
  Shorter segments retain unannualized metrics and elapsed-time disclosure. Do not
  bridge gaps or combine segments. Risk-free Rate and MAR remain separate decisions;
  Sharpe and Sortino require those inputs to be separately approved.
- A segment with no valid one-session interval has no return-based metrics.

Segment boundaries, unavailable dates, affected holdings, and reasons must remain in the
audit output. Segmented metrics are not a complete full-period equity result and do not
establish portfolio readiness.

## Approved stale valuation rule

Use the last verified Close only as a **temporary valuation mark**, never as an execution
quote. The approved maximum stale age is **3 subsequent verified exchange sessions**.
Age is 0 on the valid Close date, then 1, 2, and 3 on successive verified sessions
without a valid Close. A new valid Close resets age to 0. Once age exceeds 3, the holding
and portfolio value are unavailable. If a verified session calendar is absent or cannot
establish the session sequence, stale age and valuation cannot be certified.

During the temporary carry:

- Exclude the stale security from new Buy decisions and from risk-estimation inputs.
- Do not describe the resulting unchanged mark as an observed zero return. The stale
  date breaks the portfolio-return segment; return/risk calculations for intervals
  touching that date are unavailable.
- Show stale-mark counts and affected market value alongside equity/performance results.
- Do not force-liquidate at a missing or invented Open. Keep the holding, flag any
  unfilled exit, and set portfolio valuation unavailable after the limit until a valid
  price or separately approved settlement policy exists.
- Do not calculate or report performance metrics for any date with
  `PORTFOLIO_VALUE_UNAVAILABLE`. Keep a date-level audit row and the missing valuation
  reason; do not silently omit the date from the performance series.
- Preserve every stale/unavailable valuation date and each affected holding in the
  valuation audit, with the segment ID/boundary reason where applicable.

## Performance and accounting implications

Carrying a previous Close can keep reported equity flat while the true value moves.
This can understate volatility and drawdown, delay recognition of losses, distort daily
returns, and change ranking of strategies. A zero fill would create a fictitious total
loss; a zero return fill would create fictitious stability. Both are prohibited.

## Required output fields

At minimum: `Date`, `Symbol`, `Shares`, `Close`, `Price_Date`, `Valuation_Source`,
`Stale_Observed_Sessions`, `Is_Stale`, `Session_Status`, `Row_Present`,
`Trading_Status_Evidence`, `Corporate_Action_Status`, `Price_Basis_Status`,
`Valuation_Status`, `Execution_Status`, `Order_Blocked_Reason`, `Market_Value`,
`Portfolio_Value_Status` (one of the three defined states), and an auditable
source/artifact identifier. Include `Verified_Calendar_ID` and
`Verified_Calendar_Session_Ordinal` for the age calculation.

**Policy status: APPROVED. Historical valuation readiness: BLOCKED.** The three-session
rule and portfolio-level treatment are approved, but the official session calendar and
other Phase D evidence limitations remain unresolved. E-004 Option B is approved as a
segment-reporting convention; annualized metrics still require a verified session
calendar, sufficient segment observations, and any separately approved risk-free/MAR
inputs. Historical valuation readiness remains blocked.
