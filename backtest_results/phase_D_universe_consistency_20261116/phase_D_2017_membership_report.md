# Phase D — 2017_H1 Membership Impact

## Local membership record

The local row has 50 symbol slots, 49 nonblank unique names, and 1
blank slot(s), with no duplicate names. The blank slot does not name a missing constituent;
no name is added.

The pinned Master has 8,096 rows across 120 dates and
68 unique symbols (daily symbol count 67–68).
Joining the 49 known names produces 5,160 rows, or 43 per date, leaving
720 expected member-date rows absent. The six
known listed symbols absent on all 120 dates are: DTAC, GLOW, INTUCH, ROBINS, SCB, TMB.
This is a Master coverage fact, not proof that any one is the blank 50th constituent.

The Master also contains 25 names outside the local 49-name list.
None has all six model features plus target (0
complete rows), but this does not establish that one of them is the missing official member.

## Model and feature impact

Notebook 04's target alignment was reconstructed using the next global feature date and
the same symbol's next-date return and volatility-z value. The reconstruction yields
94,205 complete training samples, exactly matching the frozen model's recorded
94,205. The 2017_H1 slice contains 5,144 current training rows;
16 additional known-member rows lack CorrRank and
are omitted by the complete-feature filter.

The 2017_H1 target distribution in the current complete sample is
`{"0": 214, "1": 282, "2": 4648}`.
Before filtering on feature completeness it is
`{"0": 214, "1": 283, "2": 4663}`.
The six feature availability counts and membership sensitivity are in the CSV.
The three per-symbol features are not directly changed by membership. VolRank,
CorrRank, and LiquidityRank depend on member populations or the member-only proxy and
could change if the missing constituent had been available.

## Bounded conclusion

The blank member's identity and numerical effect cannot be recovered from local evidence.
At most 120 additional member-date rows could exist for one unknown symbol on the
observed dates, but its source data, features, targets, rank effects, and target
distribution are unknown. The six specifically absent listed names account for 720
known-list member-date gaps. The frozen model and Master were not modified or retrained.
The affected historical membership/model context therefore remains unresolved and
continues to block research-validity approval.
