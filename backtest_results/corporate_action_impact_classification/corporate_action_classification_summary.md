# Corporate Action & Security Identity Impact Classification

**Status:** `CORPORATE_ACTION_IMPACT_CLASSIFICATION_COMPLETED`  
**Scope:** local, read-only classification of all 141 original ledger rows. Completion does not mean events or impacts are officially verified.  
**Research Backtest Gate:** `BLOCKED`  
**Phase F:** `DO_NOT_BEGIN`

## Executive result

- All **141** source rows appear one-to-one; original CSV line references 2–142 are retained. No deduplication occurred.
- **0** records have primary event-source evidence and **0** impact dimensions are confirmed. There are 136 vendor-origin rows and 5 user-claim rows; two claims have same-symbol/date vendor candidates with unresolved terms, while three have no matching vendor row.
- Local Phase D risk indicators show possible price continuity for 141 rows, possible share impact for 4, possible cash entitlement for 140, and possible identity impact for 2. These are not verified event impacts.
- Membership scopes: **97** union-overlap rows, **89** active-member-on-recorded-date rows, **8** union rows outside active membership on recorded date, and **44** nonmembers on that date.
- This workstream changed no source data, notebook, ledger, price, quantity, cash, exclusion, gate, or Phase A–D artifact. An existing unverified GLOBAL-adjusted candidate is described below.

## Counts

### Original event labels

| Event label | Records |
|---|---:|
| `CASH_DIVIDEND` | 137 |
| `MERGER` | 2 |
| `SPLIT` | 1 |
| `STOCK_DIVIDEND+CASH_DIVIDEND` | 1 |

### Event existence and official evidence

| Status | Records | Meaning |
|---|---:|---|
| `SUPPORTED_SECONDARY` | 138 | Local vendor-reported rows, including two same-date related claim rows; not official confirmation |
| `CANDIDATE_ONLY` | 3 | Three unattached claims with no same-symbol/date vendor entry |
| `CONFIRMED_PRIMARY` | 0 | No primary event notice located |
| `UNVERIFIED` | 0 | No additional event evidence classification |
| `CONTRADICTED` | 0 | No local evidence sufficient to reject event existence |

| Official evidence status | Records |
|---|---:|
| `PRIMARY_SOURCE_CONFIRMED` | 0 |
| `LOCAL_SECONDARY_ONLY` | 0 |
| `VENDOR_ONLY` | 138 |
| `NO_EVIDENCE_FOUND` | 3 |

### Impact status

| Dimension | Confirmed | Potential indicator | No impact evidence | Unknown |
|---|---:|---:|---:|---:|
| Price | 0 | 141 | 0 | 0 |
| Share quantity | 0 | 4 | 137 | 0 |
| Cash balance | 0 | 140 | 1 | 0 |
| Security identity | 0 | 2 | 139 | 0 |

Potential indicators are based on local event labels/vendor fields and Phase D risk-scope flags; they are not independent proof that an event occurred. “No impact evidence” does not prove no impact.
Confidence refers to the reproducibility of the local evidence classification, not the probability that a corporate action occurred or that its terms are accurate.

### Identity and membership

| Security identity status | Records |
|---|---:|
| `VERIFIED` | 0 |
| `PARTIALLY_VERIFIED` | 95 |
| `UNVERIFIED` | 46 |
| `NOT_APPLICABLE` | 0 |

| Membership relevance | Records |
|---|---:|
| `ACTIVE_MEMBER_ON_RECORDED_DATE` | 89 |
| `UNION_MEMBER_OUTSIDE_RECORDED_DATE` | 8 |
| `NOT_MEMBER_ON_RECORDED_DATE` | 44 |
| `UNKNOWN` | 0 |

- `PARTIALLY_VERIFIED` means only vendor-key continuity was observed; it is not legal issuer-identity confirmation. `UNVERIFIED` does not mean an identity transition occurred.
- Symbols represented: **77**; symbols with multiple ledger records (not necessarily the same event): **57**.
- Symbols involved in explicit suspected relation groups: **3** (BANPU, BPP, GLOBAL); the groups are hypotheses, and original records remain separate.
- Entirely unresolved for primary event existence, verified terms, and confirmed impact: **141/141**.

## Suspected relationships and discrepancies

| Hypothesis | Event IDs | Limitation |
|---|---|---|
| `REL-BANPU-BPP-MERGER-20260803` | CLAIM-BANPU-MERGER-20260803, CLAIM-BPP-MERGER-20260803 | Same date and target identifier but different predecessor symbols and ratios; shared transaction is suspected, not verified. |
| `REL-BANPU-DIV-20260416` | VENDOR-0042, CLAIM-BANPU-20260416 | Same symbol/date and claimed dividend amount in vendor and user-claim rows; could be the same event, but no primary source confirms it. |
| `REL-GLOBAL-20260224` | VENDOR-0003, CLAIM-GLOBAL-20260224 | Same symbol/date; vendor split/dividend fields and user-claim label/ratio representation differ; suspected only. |

- The GLOBAL vendor row is labeled `SPLIT` and the local vendor event inventory records split and cash fields; the user claim uses `STOCK_DIVIDEND+CASH_DIVIDEND` with a different ratio convention. This discrepancy is not resolved as event truth or terms.
- BANPU vendor and user-claim dividend rows share symbol/date but disagree on amount: vendor 0.35/share versus claim 0.18/share. Neither is chosen; primary notice and entitlement evidence are absent.
- BANPU/BPP merger claims share date and target identifier but have different predecessor ratios. Identity mapping remains source-blocked.
- No original rows were deduplicated; vendor/user values were not promoted to official truth.

## Membership and special cases

- Eight union-overlap rows are outside active membership on the recorded date: VENDOR-0009 (BCP, 2026-03-02); VENDOR-0016 (TFG, 2026-03-04); VENDOR-0052 (THAI, 2026-04-24); VENDOR-0073 (MRDIYT, 2026-05-11); VENDOR-0076 (MRDIYT, 2026-05-21); VENDOR-0077 (TFG, 2026-05-25); VENDOR-0099 (CBG, 2026-08-27); VENDOR-0133 (SAWAD, 2026-10-06). Recorded date is not a verified effective date.
- The 44 nonmember rows are not evidence that an event did not occur or that a security is ineligible for all historical uses.
- BANPU full-2026 exclusion and GLOBAL precautionary exclusion are preserved. No new exclusion, reinstatement, split, ratio, or replacement ticker is asserted.
- Local 2026 SET H1/H2 membership evidence supports membership relevance only; it is not corporate-action evidence.

- Phase D marks no potential impact on pre-2025 training feature continuity; this is a scope flag, not proof of any event or price adjustment.

## Pre-existing GLOBAL candidate transformation

The local execution lineage and candidate hash show a **pre-existing non-verified candidate** applying factor `1.037037037037037` to GLOBAL OHLC rows before 2026-02-24 (**36 rows changed**) based on user terms without an attached official source. This workstream did not create, rerun, modify, or accept that candidate. The original snapshot hash matches its declared hash; `verified_execution_data_status.json` says no verified dataset was created. Therefore a repository-wide claim that no adjustment exists anywhere in historical derived data is **not supported**; only no adjustment by this workstream and no verified/authorized adjustment are supported.

## Evidence packages needed

1. Primary SET/issuer notices for event existence, legal security identifiers, effective/ex/record/payment/trading dates, ratios and amounts.
2. Original documents supporting the five user claims, including GLOBAL ratio convention, BANPU/BPP entitlements, merger ratios, successor identity and fractional settlement.
3. Authorized historical prices and official adjustment methodology; not anomaly rescaling.
4. Official quantity entitlements and settlement records; official cash terms and actual payment postings.
5. Primary legal identity continuity and membership/effective-date evidence before eligibility decisions.

## Deliverables and final state

[Row-level classification](./corporate_action_impact_classification.csv)  
[Unresolved evidence register](./unresolved_event_evidence_register.csv)  
[Security-level summary](./security_level_impact_summary.csv)  
[Validation report](./corporate_action_classification_validation.md)  
[SHA-256 manifest](./manifest.json)

`CORPORATE_ACTION_IMPACT_CLASSIFICATION_COMPLETED`

`RESEARCH_BACKTEST_GATE = BLOCKED`

`PHASE_F = DO_NOT_BEGIN`

No internet/external services, data downloads, yfinance, historical backtests, 63-combination runs, notebook edits, source-data edits, gate overrides, or Phase F actions were performed.
