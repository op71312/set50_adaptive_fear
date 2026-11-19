# Stale Valuation and Missing Price Audit

## Archived fields and observed exposure

`portfolio_valuation_audit.csv` records `Valuation_Price`, `Price_Date`, `Stale_Calendar_Days`, and `Is_Stale`. The age is a calendar-day difference between valuation Date and Price_Date, not a verified exchange-session count.

Read-only inventory:

- 67,633 valuation rows total.
- 378 rows have `Is_Stale=True`; all are BANPU.
- Stale rows occur in six pairs: S1/HRP, S1/CVaR, S4/EW, S4/IV, S4/HRP, and S4/MPT. Each has 63 stale BANPU rows.
- Maximum observed age is 93 calendar days, at valuation Date 2026-11-12 using Price_Date 2026-08-11 and Valuation_Price 14.600000381469727.
- All 844 BANPU valuation rows are included in recorded position values; the 378 stale rows contribute to stored Market_Value and daily Portfolio_Value.
- The 63 stale observations per affected pair and the 93-day maxima agree with the nonblank performance-summary stale fields. Zero-position pairs have blank stale summary fields rather than explicit zeroes.

The stored values therefore contain prolonged carried-price exposure. This does not mean 93 exchange sessions elapsed, and no official trading calendar was used to convert the age.

## Missing prices and portfolio availability

The archive contains valuation rows for every position counted in daily Holdings_Count, so no held position is missing from the retained valuation table on those dates. However, the archive does not record an unavailable portfolio-value state or an authoritative rule for missing/stale prices. It is not possible to determine whether price gaps were skipped, carried, or treated differently before the retained valuation rows were created.

Because stale position values are included in daily equity, any metric process consuming that equity series would be exposed to those marks. There is no run-linked metric input series, so the exact metric exposure and its direction or magnitude are unknown. No drawdown, return, or other performance metric was recalculated.

## Historical code distinction

Current Notebook 05's saved `mark_to_market` code (cell index 42; execution count 150) computes calendar-day age and raises when it exceeds `MAX_STALE_CALENDAR_DAYS = 5`. That current code would reject a 93-day mark if run as saved. The archive manifest and values establish that the current saved code is not proven to be the archived implementation; the archived code identity is absent. Current Phase E's later three-verified-exchange-session policy is not applied retroactively here.

## Status

`Observed stale mark and calendar-day age = DERIVATION_CONFIRMED`.  
`Historical missing-price and stale acceptance policy = UNKNOWN_INSUFFICIENT_EVIDENCE`.  
`BANPU stale metric impact = exposure confirmed; magnitude not assessed`.
