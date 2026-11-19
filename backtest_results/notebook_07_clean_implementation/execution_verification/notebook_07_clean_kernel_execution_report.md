# Notebook 07 clean-kernel execution report

- Source notebook: `D:\Project_Github\set_fear_index\07_dynamic_universe_portfolio_backtest_v2_corrected.ipynb`
- Source SHA256 before execution (`PRE_EXECUTION_SHA256`): `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070`
- Source SHA256 after execution: `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070`
- Source unchanged: `TRUE`
- Source size: 225057 bytes
- Source modified timestamp: 2026-11-18T09:48:14+07:00
- Pre-execution copy: `C:\Users\User\.copilot\session-state\a8803654-a123-474b-9c60-c15bccca0dd9\files\07_dynamic_universe_portfolio_backtest_v2_corrected.pre_execution.ipynb` (SHA256 `77ef752a98612fd85132a63371587103c08f89662c7109d433a313aaf498f070`)
- Executed notebook: `D:\Project_Github\set_fear_index\backtest_results\notebook_07_clean_implementation\07_dynamic_universe_portfolio_backtest_v2_execution_verified.ipynb`
- Executed notebook SHA256: `7c0083bdbb5e88adf205c570528380282ca67abcc69315e405eaf8d13a7c18fa`
- Python: 3.11.12 (main, May 22 2025, 01:56:58) [MSC v.1943 64 bit (AMD64)]
- Executable: `D:\Project_Github\set_fear_index\.venv\Scripts\python.exe`
- Packages: `{"ipykernel": "7.4.0", "joblib": "1.6.0", "jupyter_client": "8.10.0", "numpy": "2.4.6", "pandas": "3.1.1", "scipy": "1.17.1", "sklearn": "1.9.1"}`

- Total notebook cells: 27
- Code cells: 15
- Successfully executed code cells: 15
- Failed code cells: 0
- Unexecuted code cells: 0 ([])
- First failed notebook cell: None

- Original synthetic tests: 37/37, all PASS = True
- Targeted regression tests: 6/6, all PASS = True

## Warnings / stderr

- Kernel startup emitted a non-fatal Jupyter warning that its local TCP communication was unencrypted.
- No notebook-cell warnings or exceptions were captured.

## Corrected implementation and policy checks

- Corrected overrides for `generate_predictions`, `strategy_signals`, `fractional_tail_cvar`, and `calculate_segment_metrics` are defined in code cell 21, before the original synthetic tests (cell 23) and targeted regression tests (cell 25). No later code cell redefines them.
- R01/R02 call `strategy_signals`; R03 calls `fractional_tail_cvar`; R04 and R06 call `calculate_segment_metrics` or inspect its exported schema; R05 calls `generate_predictions` with a synthetic dummy model and a non-finite feature.
- R01 and R02 pass for all nine strategies; Normal/HOLD behavior and the Panic × FOMO action matrix are exercised against the corrected function.
- R03 passes for CVaR's tied boundary mass; tied observations receive the same fractional tail weight.
- R04 passes for a 19-interval segment remaining unannualized. The original suite also exercises the 252-interval threshold and segmented reporting.
- R05 confirms non-finite features are blocked before synthetic model inference.
- R06 confirms the performance schema includes the six named required summary metrics.
- The notebook documents incremental cash with residual cash retained, a 25% position cap, and no fixed 50% cash reserve (E-025/E-028). Its execution description uses 0.1% per-side slippage and the code applies `Open × 1.001` to buys and `Open × 0.999` to sells. The fee is 0.0016799 per-side on fill notional, matching E-027; slippage is reflected in fill price and separately recorded, not charged a second time.

## Data and execution boundary

- The readiness audit loaded local feature and execution Parquet snapshots, model artifact/metadata, membership files, corporate-action ledger, and decision register for read-only identity/hash, schema/readiness, and status inspection.
- Local feature and execution prices were accessed for audit/schema verification; they were not passed into prediction, real order execution, or historical performance simulation.
- No external API or download was intentionally called by notebook code.
- No historical portfolio backtest was run; `run_portfolio_backtest` was defined but not invoked by notebook execution or either synthetic suite.
- Synthetic tests invoked implementation functions using synthetic fixtures; the notebook writes only to temporary directories during tests.
- No model fitting/refitting or inference over historical data was performed.
- Protected source artifacts checked: 11.
- Protected-source hash changes: 0
- Protected-source missing after execution: 0
- Protected-source changed paths: None
- Protected-source missing paths: None

## Final statuses

- `NOTEBOOK_EXECUTION = PASS`
- `ORIGINAL_SYNTHETIC_TESTS = 37/37 PASS`
- `TARGETED_REGRESSION_TESTS = 6/6 PASS`
- `RESEARCH_BACKTEST_GATE = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`
