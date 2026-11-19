# E-004 — Segment Annualization Analysis

**Current status:** `NEEDS_RESEARCHER_APPROVAL`  
**Recommendation:** Option B, proposed only; no annualization is authorized until the
researcher approves it.

## Existing approved boundary

The approved E-007/E2 policy permits performance metrics only within valid contiguous
equity segments. A segment contains valid portfolio equity values on consecutive
verified exchange-session ordinals. A stale or unavailable valuation, unverified
session, or nonconsecutive ordinal closes a segment. Do not bridge a gap or pool
segments as a full-period equity curve. Keep unavailable dates, affected holdings,
segment boundaries, and reasons in the audit output.

E2 permits actual elapsed verified sessions and calendar days, segment cumulative
return, and unannualized segment results. A segment with no valid one-session interval
has no return-based metrics. If equity is incomplete, do not report full-period CAGR,
Sharpe, Sortino, volatility, or maximum drawdown as though the series were complete.
Until E-004 is approved, annualized segment metrics are unavailable.

## Definitions used for comparison

For one valid segment, let:

- `E_0`, `E_n` be its first and last valid equity marks.
- `r_i = E_i / E_(i-1) - 1` be the valid one-session returns, for `i=1..n`.
- `n` be the count of valid one-session return intervals, equal to the difference in
  verified session ordinals between segment endpoints.
- `D` be actual calendar days between the segment endpoint dates.
- `s_r` be the sample standard deviation (`ddof=1`) of the one-session returns.
- `MDD_seg = min(E_i / max(E_0,...,E_i) - 1)` within this segment.

`E_0` and `E_n` must be positive for geometric annualized-return formulas. No formula
may include an interval crossing a segment boundary. `MDD_seg` is a segment drawdown,
not a full-period drawdown.

### Metric-specific constraints

- **Segment total return:** `E_n / E_0 - 1`; not annualized. It requires at least one
  valid return interval.
- **Volatility:** annualized session volatility is conventionally `s_r * sqrt(A)`;
  unannualized volatility is `s_r`. Sample volatility requires at least two returns.
  Square-root scaling presumes a suitable stationary/weakly dependent return process;
  serial correlation can distort the estimate.
- **Sharpe:** for per-session risk-free returns `rf_i`, the unannualized form is
  `mean(r_i - rf_i) / sd(r_i)`. Under a session annualizer `A`, the conventional
  annualized form multiplies this by `sqrt(A)`. A zero or missing denominator makes it
  unavailable. No risk-free-rate series or zero-rate convention is approved by E-004;
  do not assume one.
- **Sortino:** for a specified per-session minimum acceptable return `MAR_i`, define
  downside deviation as
  `sqrt(mean(min(r_i - MAR_i, 0)^2))`; the unannualized ratio is
  `mean(r_i - MAR_i) / downside_deviation`, and a session-annualized ratio uses
  `sqrt(A)` under the conventional scaling assumption. MAR, its conversion to
  per-session values, and zero-downside handling are not specified by E-004. Do not
  assume zero MAR or report an infinite ratio.
- **Maximum drawdown:** `MDD_seg`; it is not an annualized statistic. Reset its peak at
  the first valid equity mark in each segment and label it `SEGMENT_MAX_DRAWDOWN`.
- **CAGR:** a geometric annualized return is defined only for a positive equity ratio
  and positive elapsed-time denominator. If annualization is authorized, label it
  `SEGMENT_CAGR`; never present it as a complete-period CAGR when other segments or
  gaps exist.
- **Calmar:** if reported, define it as the segment's annualized CAGR divided by
  `abs(MDD_seg)`. It is unavailable when CAGR is unavailable or `MDD_seg=0`; do not
  emit infinity or use a drawdown from another segment.

The risk-free rate and MAR, if desired, require their own explicit specification.
Approving an annualization factor alone does not settle those inputs.

## Option A — Unannualized reporting only

### Definition and fields

Report segment total return `E_n/E_0 - 1`, actual calendar days `D`, verified-session
elapsed count `n`, number of valid return intervals, segment equity endpoints, and
`MDD_seg`. Report unannualized volatility as `s_r` only when `n>=2`. An unannualized
per-session Sharpe or Sortino is dimensionless, but still requires an explicitly
specified risk-free/MAR series and a finite nonzero denominator.

Do not annualize any value. Do not call `segment return / abs(MDD_seg)` Calmar; that
would be a different, period-dependent ratio.

### Minimum length, gaps, and limitations

- `n=0`: disclose the single/no-interval segment and elapsed time; no return metric.
- `n=1`: cumulative return and drawdown are mathematically defined; sample volatility
  is not.
- `n>=2`: unannualized sample volatility can be calculated, subject to low-sample
  uncertainty. Sharpe/Sortino remain subject to input/denominator requirements above.
- A stale/unavailable mark ends the segment. No return is created across it and no
  subsequent equity is attached to the preceding segment.

### Metric and comparability effects

CAGR, annualized volatility, annualized Sharpe, annualized Sortino, and Calmar are
unavailable by policy. Segment total returns, raw per-session volatility, and
segment drawdowns remain interpretable as observed-period quantities. Different segment
durations make unannualized risk/return ratios less directly comparable across
strategies. Full disclosure of `n`, `D`, and gap/segment counts is essential.

### Reproducibility and risk

Option A avoids annualization assumptions and matches what can be reported under the
current approval. It is the most conservative immediate policy. Its trade-off is that
the same total return over different segment durations is not normalized, limiting
cross-strategy ranking. It should not be confused with an annualized comparison.

## Option B — Verified exchange-session annualization

### Proposed convention

Use one fixed proposed factor:

`A = 252 verified exchange-session return intervals per nominal year`.

For a segment with `n` valid one-session returns:

- `SEGMENT_CAGR = (E_n/E_0)^(252/n) - 1`.
- `SEGMENT_ANNUALIZED_VOLATILITY = s_r * sqrt(252)`.
- `SEGMENT_ANNUALIZED_SHARPE =
  sqrt(252) * mean(r_i-rf_i) / sd(r_i)`, only when an approved per-session risk-free
  series exists and the denominator is finite and positive.
- `SEGMENT_ANNUALIZED_SORTINO =
  sqrt(252) * mean(r_i-MAR_i) / downside_deviation`, only when an approved per-session
  MAR convention exists and downside deviation is finite and positive.
- `SEGMENT_MAX_DRAWDOWN = MDD_seg`, unannualized.
- `SEGMENT_CALMAR = SEGMENT_CAGR / abs(MDD_seg)`, only when both inputs are available
  and `MDD_seg<0`.

This 252 factor is a proposed performance convention; E3's 252-observation CVaR window
does not approve or determine it.

### Short segments and minimum observations

Proposed conservative reporting floor: annualized metrics are available only for
segments with `n>=252` consecutive valid one-session returns (253 valid equity marks
including the initial endpoint), positive endpoint equity, a verified calendar, and
all metric-specific inputs. For `n<252`, report only unannualized segment results and
elapsed time; mark all annualized metrics `UNAVAILABLE_SHORT_SEGMENT`. Apply the same
rule to every strategy and allocation method.

The floor is a reporting safeguard, not evidence that 252 observations make an estimate
statistically precise. A one-year sample can still have high estimation uncertainty,
nonstationarity, and serial dependence. Report interval count, segment duration,
missing/stale boundaries, and metric assumptions. Do not turn multiple short segments
into one 252-interval sample.

### Missing equity, comparability, and reproducibility

Only valid E2 segments qualify. Any stale/unavailable value or gap ends the segment;
the first valid mark after it starts another. No annualized value is computed across
the missing interval, and full-period metrics remain prohibited if the complete equity
series is incomplete. Use the same `A=252`, threshold, return frequency, formulas, and
field names across all strategies and allocation methods. Disclose each segment rather
than ranking incomparable segments without their coverage.

Required recorded inputs include segment ID and boundary reason, endpoint equity/dates,
ordered verified calendar session ordinals, `n`, `D`, the exact return series and
price/cost basis, metric formula/version, the 252 factor, threshold, and risk-free/MAR
series and conventions if Sharpe/Sortino are produced. Hashes identify the inputs but
do not establish their validity.

### Trade-offs and risks

This aligns annualization with the actual daily trading observations and uses one
factor for cross-method comparison. It is not the same as annualizing by elapsed
calendar time. A fixed 252 factor is a convention rather than an observed calendar
fact; annualization can amplify short or unstable samples, which is why the proposed
floor is conservative. If the exchange calendar is unavailable, verified-session
counts cannot be asserted and these metrics remain unavailable.

## Option C — Elapsed-calendar-time annualization

### Proposed formulas

For positive endpoint equity and `D>0` calendar days:

- `SEGMENT_CAGR_calendar = (E_n/E_0)^(365.25/D) - 1`.
- With `n` one-session returns, an approximate annualized volatility factor is
  `sqrt(365.25*n/D)`, giving
  `s_r * sqrt(365.25*n/D)`. Annualized Sharpe and Sortino would use the same factor
  applied to their per-session ratios, subject to approved RF/MAR inputs.
- Segment maximum drawdown remains unannualized; Calmar uses this calendar-time CAGR
  divided by `abs(MDD_seg)`.

`365.25` calendar days per nominal year is a proposed convention. Do not insert zero
returns for weekends or holidays to create a calendar-daily series.

### Minimum length, missing equity, and limitations

If this option were selected, a conservative comparable reporting rule would require
both `D>=365.25` and `n>=252` consecutive verified session intervals for annualized
metrics. Shorter segments would remain unannualized. This threshold and factor are
proposals, not current rules. All E2 gap/segment restrictions still apply.

Calendar-time CAGR is straightforward from endpoints, but risk metrics are not
unambiguously calendar-time quantities when returns occur only on exchange sessions.
The volatility/ratio scalar above uses average calendar time per observed session and
assumes a time-homogeneous variance rate through weekends and holidays. Unequal session
spacings and overnight/weekend risk challenge that assumption. Calendar-day scaling may
make identical session-return paths appear to have different annualized risk because
their segment start/end dates span different holidays or weekends.

The W1.5 formula audit notes a calendar-day/365.25 formula in a static Notebook 05 code
reference, while explicitly stating the archived run's annualization formula is unknown
and unlinked. That code observation is not historical evidence and does not approve
Option C.

### Comparability and reproducibility

All methods would need identical `365.25`-day basis, endpoint treatment, floor,
calendar-day count, and risk-free/MAR conversion. Record `D`, `n`, the exact `D/n`
scaling, return series, segment boundaries, formula version, and rate inputs. This
method is not recommended for daily trading-performance comparisons because its return
annualizer and risk scaling use different clocks and require assumptions about
non-trading time.

## Comparison and recommendation

| Criterion | Option A: unannualized | Option B: verified sessions | Option C: calendar time |
|---|---|---|---|
| Return annualization | None | Proposed 252-session CAGR | Proposed 365.25-day CAGR |
| Volatility/ratio scaling | None | `sqrt(252)` | `sqrt(365.25*n/D)` approximation |
| Minimum proposed annualized sample | Not applicable | `n>=252` consecutive returns | `n>=252` and `D>=365.25` |
| Required time evidence | Valid session ordinals for elapsed count | Verified official session calendar and ordinal | Exact endpoint dates; session returns still needed for risk |
| Short segments | Unannualized only | Unannualized only below floor | Unannualized only below floor |
| Gaps/unavailable equity | Separate segments; no bridge | Same | Same |
| CAGR / annualized volatility / Sharpe / Sortino / Calmar | Unavailable | Segment-only, if floor and inputs pass | Segment-only, if floor and inputs pass |
| Maximum drawdown | Segment drawdown, not annualized | Same | Same |
| Trading-performance comparability | Limited across durations | Best aligned to trading observations | Calendar exposure can vary independently of trading observations |
| Main risk | Less normalized across segment lengths | Square-root and short-sample assumptions | Calendar-time variance assumption and irregular interval lengths |

**Recommendation: Option B, subject to explicit approval.** It uses the exchange-session
clock on which the approved return series is sampled and applies one fixed convention
across methods. The proposed 252-return floor prevents reporting magnified annualized
statistics from very short segments, while retaining unannualized results. It does not
make Sharpe/Sortino available without approved RF/MAR inputs, and it does not validate
historical segments.

Until the researcher approves E-004, retain the current approved boundary: unannualized
segment results and actual elapsed time only; all annualized segment metrics unavailable.
E-004 remains `NEEDS_RESEARCHER_APPROVAL`.

## Sources

The reviewed source paths and SHA-256 values are recorded in
[source_evidence_inventory.csv](./source_evidence_inventory.csv). Key documents:
[Phase E decision register](../phase_E_portfolio_specification/phase_E_decision_register.csv),
[E2 policy](../phase_E_portfolio_specification/E2_valuation_stale_price_policy.md),
[Phase E validation report](../phase_E_portfolio_specification/phase_E_validation_report.md),
[W1.5 performance summary](../archived_performance_methodology_audit/archived_performance_methodology_summary.md),
[W1.5 metric formula audit](../archived_performance_methodology_audit/performance_metric_formula_audit.csv),
and [initial equity/return audit](../archived_performance_methodology_audit/initial_equity_and_return_audit.md).
