# Workstream 1.9.1 — Approach B Roadmap Correction

## Adopted source approach

Researcher-selected **Approach B — Vendor-Based Research Backtest** permits
Yahoo Finance/yfinance as a third-party vendor source for research execution
prices. Official SET execution prints are **not** a mandatory price-source
prerequisite under this approach. Vendor origin, data limitations, and impact on
research interpretation must be stated rather than represented as exchange
prints.

This source-policy choice does not make the current snapshot complete,
reproducible, identity-safe, or ready for a backtest. The current snapshot is
identified as Yahoo/yfinance 1.8.0 and its exact Parquet hash is verified, but
the request ticker list, interval, `group_by`, and source timezone remain
`UNKNOWN`. Price completeness, corporate-action treatment, identity, calendar
alignment, and archived run lineage remain blockers.

## Corrected roadmap language

The prior Workstream 1.9 roadmap's phrases “resolve source authority,”
“authorized price-source policy,” and “authorized OHLC” could be read as
requiring official SET execution data. The following replacement wording applies
to this corrected copy only; the original Workstream 1.9 deliverables remain
unchanged.

### Execution provenance and quality (B-EX-01/02/03)

Use the researcher-approved vendor-based source approach. Record the vendor and
library version, exact source artifact path and content hash, retrieval time,
requested date range, ticker list, interval, `group_by`, timezone, and adjustment
and actions settings to the extent they can be verified. Do not invent missing
request metadata or infer it from output columns.

For the current Yahoo/yfinance snapshot, source family/version, retrieval time,
date range, symbol counts, `auto_adjust=false`, `actions=true`, row count, and
file hash are verified. The exact ticker list, interval, `group_by`, and source
timezone are `UNKNOWN`. The data is vendor-observed and is not represented as
official SET prints.

Assess missing and anomalous OHLC fields against the chosen vendor snapshot and
document the resulting limitations. The existing 253 missing OHLC field-cells
across BANPU rows and 141 GLOBAL anomaly field-rows across 36 dates remain
unresolved; no imputation, correction, or cause is inferred. Missing/zero volume
and repeated closes remain diagnostics rather than proof of suspension or
staleness.

### Session calendar and execution alignment (B-CAL-01)

Vendor prices may be used under Approach B, but vendor-observed dates must not
be called official SET sessions without evidence. Verify execution-date and
session alignment against a suitable, reproducible calendar source; record the
calendar identity and any residual uncertainty. The local official-session
calendar path checked for this workstream is `NOT_FOUND`. This continues to
block verified-session counting for E-004 and stale-age rules, even though
official SET execution prices are not required.

### Security identity and corporate actions (B-ID-01/02; B-CA-01)

Link vendor ticker history and corporate-action records to a verified security
identity and event terms/dates. Identity and event documents may inform one
another; do not assume every ledger event changed a price or position. Preserve
BANPU's 2026 exclusion and GLOBAL's precautionary exclusion. Do not claim a
split or use the existing 28/27 candidate as a verified correction.

### Reproducibility, no-lookahead, and reporting

Preserve the vendor snapshot and source lineage immutably; record the data cut,
prediction/execution date relationship, code/configuration and hashes, and
known unknowns. Verify no-lookahead and execution-price completeness against
the selected vendor data. State how vendor limitations, missing data, identity,
corporate actions, and calendar uncertainty affect the research conclusions.
Do not treat the source-selection decision as evidence that those checks passed.

## Field-level status

| Requirement | Status | Basis / remaining work |
|---|---|---|
| Vendor source is permitted by Approach B | `PASS_WITH_LIMITATIONS` | Yahoo Finance via yfinance 1.8.0 is identified; it is third-party vendor data, not official SET prints. |
| Execution Snapshot identity and hash | `VERIFIED` | Exact Parquet path and bytes match SHA-256 `14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a`. |
| Request ticker list | `UNKNOWN` | Exact requested list is not preserved in the inspected sidecar/lineage. |
| Interval and `group_by` | `UNKNOWN` | Explicitly unknown in execution lineage. |
| Source timezone | `UNKNOWN` | Not established by timezone-naive output dates. |
| Retrieval timestamp, range, flags and version | `VERIFIED` | As recorded in the sidecar; this does not establish missing parameters. |
| OHLC completeness / GLOBAL price basis | `BLOCKED` | Existing missing fields and anomalies remain unresolved. |
| Corporate-action and security identity treatment | `BLOCKED` | Event impacts and identity continuity are not fully verified. |
| Verified exchange-session/calendar mapping | `BLOCKED` | No local official calendar was found; vendor dates are not official sessions. |
| No-lookahead and full-run reproducibility | `PARTIALLY_VERIFIED` | Existing four-row AOT diagnostic has limited checks; full run inputs and lineage are not established. |

## Gate impact

Approach B corrects the **price-source requirement**, not the evidence status.
B-EX-01 remains unresolved at the full-provenance level; B-EX-02, B-EX-03,
B-ID-01/02, B-CA-01, B-CAL-01, B-UNIV-01, and archive/implementation blockers
remain. No blocker is promoted to PASS solely because the researcher selected
vendor-based research.

`RESEARCH_BACKTEST_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`
