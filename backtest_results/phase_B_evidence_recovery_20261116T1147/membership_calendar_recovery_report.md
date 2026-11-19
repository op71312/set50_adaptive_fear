# Membership and Trading Calendar Recovery — Phase B

## Membership records

- Local membership periods audited: 22; declaration rows: 22.
- The local membership file has 50 names in most periods; `2017_H1` has 49. Row counts are descriptive only and do not authenticate constituents.
- Declaration records contain 22/22 URL pointers. The 2026_H1 and 2026_H2 pointers identify SET-hosted documents, but the documents were not retrieved; each membership/effective-date/transition row therefore remains `BLOCKED_SOURCE_DOCUMENT_NOT_RETRIEVED`.
- No historical membership or declaration data was changed.
- The union of the 2026_H1 and 2026_H2 local member lists contains 54 symbols. This is a candidate list, not a verified official membership universe.

## Calendar and alignment

- 2026 candidate predictor dates reviewed: 210; date range `2026-01-05` through `2026-11-13`.
- The required official calendar `D:\Project_Github\set_fear_index\dataset\SET_trading_calendar_2026.csv` is present: `False`.
- The recorded next-observed feature dates and Phase A execution-date candidates are listed in `trading_calendar_evidence_audit.csv`. These are not treated as official SET sessions.
- No generic weekday calendar was substituted. All date alignment remains blocked; the final predictor date has no next observed date in the local feature set.

## Output

`membership_primary_evidence_audit.csv` records each local membership name and each constituent change, with source URL pointer, publisher host, effective-date claim, and retrieval/verification status. `trading_calendar_evidence_audit.csv` records candidate date alignment and the absent official-calendar evidence.
