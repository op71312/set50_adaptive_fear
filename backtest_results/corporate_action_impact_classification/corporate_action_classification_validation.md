# Corporate Action Classification — Validation Report

**Classification status:** `CORPORATE_ACTION_IMPACT_CLASSIFICATION_COMPLETED`  
**Research Backtest Gate:** `BLOCKED`  
**Phase F:** `DO_NOT_BEGIN`

| Check | Result | Evidence |
|---|---|---|
| Original ledger row count | PASS | 141 source rows and 141 output rows |
| Event identity / row traceability | PASS | 141 unique Event_IDs and source line numbers 2–142 |
| No silent duplicate merge/drop | PASS | All source IDs represented once; suspected relationships remain separate |
| Controlled status values | PASS | All classification statuses use the requested vocabularies |
| Traceable confirmed claims | PASS | Confirmed event and impact counts are zero |
| Unknown vs not applicable | PASS | Insufficient evidence is not coded as not applicable |
| Membership counts | PASS | union=97, active=89, outside-active=8 |
| BANPU/GLOBAL restrictions | PASS | Existing exclusions are retained; no eligibility policy changed |
| Engine-applied event flags | PASS WITH LIMITATION | Ledger and Phase D report zero applied; existing candidate exception follows |
| Input hashes and protected notebooks | PASS | 27 local files hashed before and after generation; no change detected |
| Source-file modification | PASS | None by this workstream |
| Gate / Phase F | PASS | Gate remains BLOCKED; Phase F remains DO_NOT_BEGIN |

## Pre-existing adjusted candidate — validation exception

**BLOCKED for a repository-wide claim that no historical adjustment exists.** The existing `execution_ohlcv_corrected_v2.parquet` candidate has GLOBAL factor `1.037037037037037` applied to 36 rows before 2026-02-24, with evidence status `USER_PROVIDED_TERMS; OFFICIAL_SOURCE_URL_NOT_ATTACHED`. Its SHA-256 matches `execution_data_lineage.json`; it is not official/verified. The status sidecar says `verified_dataset_created=false`. The original snapshot hash also matches its lineage. This workstream did not touch either file or apply any adjustment. The candidate does not confirm the corporate action, but it prevents an unqualified repository-wide assertion that no historical derived data was adjusted.

## Counts and stop conditions

- Event labels: `{"CASH_DIVIDEND": 137, "MERGER": 2, "SPLIT": 1, "STOCK_DIVIDEND+CASH_DIVIDEND": 1}`.
- Event existence: `{"SUPPORTED_SECONDARY": 138, "CANDIDATE_ONLY": 3}`; official evidence: `{"VENDOR_ONLY": 138, "NO_EVIDENCE_FOUND": 3}`.
- Confirmed impact records: price=0, share=0, cash=0, security identity=0.
- Potential indicators: price=141, share=4, cash=140, identity=2.
- Entirely unresolved for official event existence/terms/impact: 141/141.

`CORPORATE_ACTION_IMPACT_CLASSIFICATION_COMPLETED`
`RESEARCH_BACKTEST_GATE = BLOCKED`
`PHASE_F = DO_NOT_BEGIN`
