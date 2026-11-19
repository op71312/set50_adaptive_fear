# Notebook 07 canonical and diff report

## Scope
This verification inspected the two notebook candidates in:
- `backtest_results/notebook_07_clean_implementation/07_dynamic_universe_portfolio_backtest.ipynb`
- `backtest_results/notebook_07_clean_implementation/07_dynamic_universe_portfolio_backtest_v2.ipynb`

The objective was to establish whether the current notebooks are separate implementations or duplicate versions of the same code, whether a canonical notebook exists, and whether the synthetic 37-case pass result is reproducible without historical backtest execution.

## Canonical notebook identification

### Metadata
| Notebook | SHA-256 | Size (bytes) | Cell count | Markdown cells | Code cells |
|---|---:|---:|---:|---:|---:|
| `07_dynamic_universe_portfolio_backtest.ipynb` | `5749c8acc48e21fe1463edffa437d72ef8a453c1820c7bc9ff4f99558fb9f595` | 171308 | 24 | 11 | 13 |
| `07_dynamic_universe_portfolio_backtest_v2.ipynb` | `668a89e524dd9bba7fec1f52b3c25c9a3050862fe8875eae859f6a2fedaf7bbc` | 196063 | 24 | 11 | 13 |

### Code comparison
A direct source-text comparison showed both notebooks share the same 24-cell ordering, the same 11 markdown cells, the same 13 code cells, the same function definitions, the same synthetic test names, and the same execution sequence. The only material differences are file serialization metadata and different SHA-256 values.

### Canonical choice
The notebooks are effectively duplicate implementation versions rather than distinct, competing implementations. The evidence supports treating `07_dynamic_universe_portfolio_backtest.ipynb` as the canonical representative because it is the earliest file in the candidate set and has the same implementation logic as the `v2` version.

## Diff summary
- Same number of cells: 24
- Same number of markdown cells: 11
- Same number of code cells: 13
- Same function inventory and order
- Same `run_synthetic_tests()` logic and same assertion set
- Different SHA-256 and file size due to file copy/serialization differences, not a substantive code revision

## Executed test evidence
The notebook code was executed in an isolated namespace without using historical data or running a historical backtest. The `run_synthetic_tests()` function completed successfully and reported 37 synthetic cases with status `PASS`.

## Final status
- `RESEARCH_BACKTEST_GATE = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`
- `Historical backtest validity`: `NOT_SUPPORTED_BY_SYNTHETIC_ONLY_PASS`
