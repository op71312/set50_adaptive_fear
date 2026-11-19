# E1 — Board Lot and Trading Unit Policy

## Evidence table

| Local evidence | What it establishes | Date range / confidence |
|---|---|---|
| [05_backtest.ipynb](../../05_backtest.ipynb), order-sizing cell | The legacy prototype hard-codes `BOARD_LOT = 100` and rounds buys down to multiples of that value. It establishes code behavior only. | Prototype backtest period; high confidence about the code, no evidentiary value for exchange rules. |
| [06_research_backtest.ipynb](../../06_research_backtest.ipynb), configuration/execution guards | `BOARD_LOT_SIZE = None`; order sizing raises `PolicyUnresolvedError` when the value is absent. | Phase C harness; high confidence about current guard behavior. |
| Phase C and Phase D gate/readiness reports | Board-lot policy remains unresolved; no approval or authoritative schedule is recorded. | Research period; high confidence about recorded gate status. |
| Repository documentation and data inventory | No local primary-source schedule with effective dates, security-specific units, odd-lot rules, or historical exceptions was found. | 2016–2026 study horizon; high confidence that the inspected local artifacts do not contain this evidence, not proof that no external rule exists. |

No external websites, downloads, or inferred exchange rules were used.

## Scope and distinctions

The backtest horizon spans 2016–2026, so one constant would be defensible only if an
authoritative local source proves that the same unit applied to every relevant security
and date. No such proof was found.

- **Market segment:** the schedule must identify the market/board segment in which the
  order is intended. A unit for one segment must not be applied to another without
  evidence.
- **Regular board lot:** the standard unit applicable to an order in the regular market
  for the identified security, segment, and effective date.
- **Odd-lot trading unit:** the quantity convention for odd-lot orders in the applicable
  segment. It is not interchangeable with the regular board lot.
- **Minimum order quantity:** the smallest accepted order quantity, which may be
  distinct from either unit.
- **Quantity multiple:** the increment by which an order quantity must increase after
  satisfying the minimum. Record it independently rather than assuming it equals the
  board lot.
- **Actual held shares:** the portfolio ledger must retain the actual integer quantity
  held, including any residual or odd-lot quantity created by partial fills, legacy
  holdings, or corporate-action entitlements. Do not round the holding to a regular lot.
- **Regular-lot executable quantity:** for a sell, calculate only the quantity executable
  in the regular segment under the date-effective minimum and quantity multiple. Any
  residual remains held and must be represented separately; it is not implicitly sold.
  Buy sizing must use the corresponding verified rules for the intended segment.
- **Security identity / historical rule changes:** key rules to a verified security
  identity, with effective-from/effective-to dates. An unresolved ticker or identity
  transition blocks the schedule lookup and sizing. Current terms cannot establish
  earlier-period terms.

The legacy value 100 is not adopted. Phase C's `None` guard correctly prevents sizing
until all applicable dimensions and the effective-dated schedule are supported.

## Proposed implementation — requires researcher approval

Maintain a versioned schedule keyed by `Security_ID`, market segment, and effective
period (and ticker alias where needed):

`Security_ID, Symbol, Market_Segment, Effective_From, Effective_To, Regular_Board_Lot, Odd_Lot_Trading_Unit, Minimum_Order_Quantity, Quantity_Multiple, Source_Publisher, Source_URL_or_Local_Path, Evidence_Date, Verified_Status`

Rules:

1. Select the schedule row effective on the execution date; reject overlapping or missing
   rows, unknown segments, and unresolved identity transitions.
2. Size buys only after the method's incremental cash budget has been finalized and use
   the verified minimum and quantity multiple for that side/segment. For a quantity
   multiple `M`, minimum `Q_min`, raw Open `O`, slippage `s`, and fee rate `f`, find the
   greatest `q >= Q_min` with `q` a multiple of `M` for which
   `q * O * (1+s) * (1+f) <= budget`. If no such quantity exists, do not place the order.
   This is a proposed general rule; the exact relationship between minimum quantity and
   permitted multiples must be encoded from the verified schedule.
3. Keep actual holdings in integer shares. On regular-lot sale, execute only the
   verified regular-segment executable portion; record any unsold residual separately.
   Never assume it can be liquidated via the odd-lot segment without evidence and policy
   approval.
4. Never size from future Close. If evidence, identity, segment, price, quantity rule, or
   budget is invalid, block the order and retain the cash/holding.
5. Do not create fractional shares or silently round actual held shares.

### Researcher decisions still required

- Approve the authoritative source and coverage requirements for a 2016–2026 schedule.
- Approve how the schedule relates regular board lot, odd-lot unit, minimum order
  quantity, quantity multiple, and market segment.
- Decide whether odd-lot buys/sells are in scope and how actual residual holdings are
  treated at exit/end-of-period.
- Decide how to handle security identity changes and special trading units if source
  schedules are incomplete.

## Impact on reproducibility and readiness

Trading unit, minimum, and multiple affect shares purchased, residual cash, transaction
costs, regular-lot sellability, and all later holdings/returns. A global 100-share
assumption may systematically reject affordable orders, permit invalid quantities, or
misstate actual holdings and unsold residuals. The existing synthetic order-sizing test
verifies prototype arithmetic only; it does not verify historical market rules.

**Status: BLOCKED.** Do not execute portfolio sizing until an effective-dated source
schedule is locally available and the policy is approved.
