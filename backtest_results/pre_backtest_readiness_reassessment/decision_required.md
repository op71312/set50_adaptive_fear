# Decisions and Evidence Required Before Any Future Gate Review

This file is a request list for a future researcher/evidence owner. It does not request or authorize a backtest, download, notebook change, or Phase F.

## Researcher decisions still open

| Decision | Current status | Decision needed |
|---|---|---|
| E-001 — historical board lot | `BLOCKED` | Supply/approve an authoritative effective-dated schedule for each relevant security and market segment, separating regular board lot, odd-lot unit, minimum order quantity, quantity multiple, and actual holdings. A global `100` constant is not evidence. |
| E-002 — odd lots | `NEEDS_RESEARCHER_DECISION` | Decide whether odd-lot buys/sells are in scope and how residual shares and end-of-period holdings are treated, after schedule evidence is available. |
| E-004 — segment annualization | `NEEDS_RESEARCHER_DECISION` | Approve whether/how annualized metrics are produced for separate valid segments. Until then, report unannualized segment results and elapsed time only. |
| E-029 — additional version/snapshot identifiers | `NEEDS_RESEARCHER_DECISION` | Decide whether Universe_Snapshot_ID, Prediction_Snapshot_ID, Execution_Eligibility_Snapshot_ID, Model_Version, and Allocation_Policy_Version are mandatory. Risk_Data_Hash remains required under the approved specification. |

E-005 through E-020 are already `APPROVED`; no additional approval is inferred or requested for them.

## Evidence packages needed to resolve blockers

1. **Corporate actions:** For each potentially relevant event, provide a primary SET/issuer/SEC notice tied to the correct Security_ID, verified terms, event and effective/ex/record/payment/trading dates, and supported price/share/cash accounting. Reconcile all 141 ledger entries or document why an entry is irrelevant. Prioritize the 97 union-overlap rows, including the 89 recorded-date active-membership cases. Do not treat the recorded date or vendor label as proof.
2. **BANPU identity and execution:** Provide authoritative identity/transition/conversion documents, trading-status and effective-date evidence, source OHLC for missing dates or proof of non-sessions, and a feature-history reconstruction method consistent with the frozen pipeline. Preserve the existing exclusion until reviewed evidence resolves it.
3. **GLOBAL price basis:** Provide primary evidence for any effective-dated corporate action or price basis and an authorized tick schedule. The current diagnostic does not establish a split; retain the precautionary exclusion until source evidence is reviewed.
4. **Execution acquisition:** Recover the original immutable acquisition request/log including exact ticker list, interval, group_by, timezone, request range, settings, library version, and timestamp. Separately establish an authorized/verified execution-price source or a researcher-approved source policy; metadata completeness alone cannot verify prices.
5. **2017_H1 membership:** Provide primary SET evidence naming the 50th constituent and effective dates, plus a traceable source for the six listed names absent from the Master over 120 dates and an impact analysis for the frozen training features. Do not guess or backfill.
6. **Trading calendar:** Provide a verified official SET session calendar covering all required backtest dates and a deterministic predictor-to-next-session mapping. Do not use weekdays or Yahoo-observed dates as a replacement.
7. **Universe and risk history:** After the above blockers are resolved, demonstrate a multi-security candidate universe without relaxing eligibility, then verify the same complete eligible Buy universe has the full 60/252 common observations, cutoff, return basis, and risk-data hashes required by Phase E. Do not silently drop securities or use partial windows.
8. **Implementation and gate refresh:** Only after evidence/policies are resolved, bring the implementation and gate criteria into conformance with Phase E. Implement and independently test all seven methods and shared execution/valuation rules, including the 25% caps, fee sequence, fail-closed cash behavior, and unavailable valuation segmentation. This review did not edit or execute either notebook.

## Stop

No evidence request above changes the current decision: `RESEARCH_BACKTEST_GATE = BLOCKED`; `PHASE_F = DO_NOT_BEGIN`. Do not proceed until a new explicit researcher instruction and a fresh evidence-based gate review.
