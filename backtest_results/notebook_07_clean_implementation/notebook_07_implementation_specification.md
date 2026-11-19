# Notebook 07 Implementation Specification

## 1. Purpose and scope

This document records the implementation plan and design contract for the clean portfolio-backtest notebook:

- `backtest_results/notebook_07_clean_implementation/07_dynamic_universe_portfolio_backtest.ipynb`
- `backtest_results/notebook_07_clean_implementation/07_dynamic_universe_portfolio_backtest_v2.ipynb`

This notebook is a research-only framework, not a historical backtest result. It is designed to implement the approved governance constraints and fail-closed behavior required by the project while preserving the current gate state:

- `RESEARCH_BACKTEST_GATE = BLOCKED`
- `PHASE_F = DO_NOT_BEGIN`

The notebook is intended to support future research backtesting only after the required evidence, identity, calendar, and execution controls are resolved.

## 2. Strict operating constraints

### Permitted

- Inspect repository files, datasets, metadata, and prior artifacts.
- Construct a new notebook for the clean implementation.
- Define reusable functions and synthetic validation logic.
- Produce documentation and implementation notes.

### Prohibited

- Modifying Notebook 03, 04, 05, or 06.
- Modifying master, feature, execution, or archived backtest sources.
- Retraining or refitting the Softmax model.
- Downloading Internet data or calling third-party APIs.
- Running a historical portfolio backtest as evidence.
- Opening the research backtest gate or starting Phase F.
- Treating synthetic tests as historical proof.

## 3. Notebook architecture

The notebook is organized into exactly nine main sections, each mapped to a distinct implementation concern:

1. Data Loading & Integrity
2. Dynamic Tradable Universe
3. Feature & Prediction
4. Strategy Signals
5. Portfolio Allocation
6. Execution Engine
7. Portfolio Valuation
8. Performance Evaluation
9. Audit & Export

## 4. Core implementation design

### 4.1 Data and lineage

The notebook is designed to separate source-level evidence from decision-time engineering logic:

- Master/feature data and execution data are loaded as distinct objects.
- Model metadata and model version are checked before prediction.
- Execution snapshot reference is kept separate from the feature snapshot.
- Source paths and relevant timestamps are recorded in a manifest.
- `Risk_Data_Hash` is required for risk-based allocation methods.
- E-029 lineage fields are included in run manifest design:
  - `Universe_Snapshot_ID`
  - `Prediction_Snapshot_ID`
  - `Execution_Eligibility_Snapshot_ID`
  - `Model_Version`
  - `Allocation_Policy_Version`
- Missing or inconsistent lineage is marked `PROVENANCE_INCOMPLETE`.

### 4.2 Dynamic universe

The implementation treats the tradable universe as a dynamic daily eligibility filter rather than a fixed 50-security requirement. The key design intent is:

- SET50 membership is evaluated using `effective_date` rather than announcement date.
- Membership changes are tracked historically.
- Holdings and buy universe are kept separate.
- Excluded symbols such as BANPU and GLOBAL remain explicitly blocked by policy or evidence.
- Missing execution Open or missing eligibility evidence triggers fail-closed behavior.
- Forced exits for membership removal are processed only when actual execution data supports the exit.

### 4.3 Feature prediction contract

The notebook uses the approved feature list in exact order:

1. `daily_return`
2. `momentum_20d`
3. `vol_z`
4. `VolRank`
5. `CorrRank`
6. `LiquidityRank`

The implementation preserves:

- date separation between prediction date and execution date,
- no use of actual future targets,
- no retraining or refitting,
- no scaler replacement,
- feature-order integrity,
- finite-value validation before inference,
- probability and class logging,
- model version and hash logging.

### 4.4 Strategy signal generation

The notebook includes a nine-strategy design corresponding to the approved signal matrix. Normal is always Hold. The strategy layer is separate from allocation logic and records:

- predicted class,
- probability vector,
- strategy identifier,
- action,
- membership status,
- execution eligibility,
- exclusion reason,
- model provenance.

### 4.5 Allocation methods

The notebook implements all seven methods required by the specification:

1. Equal Weight (EW)
2. Inverse Volatility (IV)
3. Equal Risk Contribution (ERC)
4. Hierarchical Risk Parity (HRP)
5. Minimum Variance (MinVar)
6. Conditional Value at Risk (CVaR)
7. Mean-Variance Portfolio Optimization (MPT)

Shared rules include:

- incremental cash-only allocation,
- sell before buy,
- forced exits before new buys,
- no short selling,
- no leverage,
- 25% max weight per buy security,
- iterative cap-and-redistribute,
- fail-closed cash allocation on invalid risk panels or solver failures.

### 4.6 Risk and solver rules

The implementation preserves the specified risk-window and fail-closed requirements:

- IV: 60 verified sessions
- ERC: 60 verified sessions
- HRP: 60 verified sessions
- MinVar: 60 verified sessions
- CVaR: 252 verified sessions
- MPT: 60 verified sessions

Risk-based methods are designed to avoid:

- pairwise covariance deletion,
- zero replacement for missing returns,
- forward fill,
- mixed date windows,
- silent fallback to another allocation method.

### 4.7 Execution engine

The execution layer uses separate execution data and is explicitly designed to record the following information:

- raw Open,
- slippage-adjusted fill price,
- gross value,
- fee,
- slippage cost,
- total transaction cost,
- cash before and after,
- shares before and after,
- execution status,
- skip or failure reason.

Rules enforced in design:

- BUY fill price = Open × 1.001
- SELL fill price = Open × 0.999
- total transaction cost = 0.0026799 per side
- no shorting, no leverage, no invented prices,
- missing Open blocks execution,
- forced exit is processed before buy,
- hold positions are not sold to fund buys,
- unresolved board-lot and corporate-action rules remain blocked.

### 4.8 Valuation and stale policy

The notebook design follows E-005 / E-006:

- stale threshold = 3 verified exchange sessions,
- latest verified Close may be used only within the threshold,
- older than 3 sessions means valuation unavailable,
- portfolio equity becomes unavailable if any held security cannot be valued,
- no silent replacement of unavailable equity with cash-only equity.

### 4.9 Performance evaluation

The performance engine is designed to implement:

- Total Return
- CAGR
- Annualized Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Calmar Ratio
- Average Cash Weight
- Transaction Count
- Total Transaction Cost
- Total Turnover
- Stale Valuation Count
- Maximum Stale Verified Sessions

The notebook preserves the approved annualization rule:

- 252 verified exchange-session intervals per nominal year,
- 253 valid equity marks required before annualized metrics are allowed,
- shorter valid segments remain unannualized,
- missing returns are never bridged,
- no fabricated risk-free rate or MAR is assigned.

## 5. Proposed functions

The implementation is structured around reusable functions, with a clean separation of concerns. The notebook design includes the following function groups:

- `load_and_validate_data()`
- `build_dynamic_universe()`
- `generate_predictions()`
- `generate_strategy_signals()`
- `build_common_risk_panel()`
- `allocate_ew()`
- `allocate_iv()`
- `allocate_erc()`
- `allocate_hrp()`
- `allocate_minvar()`
- `allocate_cvar()`
- `allocate_mpt()`
- `apply_weight_cap()`
- `execute_orders()`
- `apply_corporate_actions()`
- `mark_to_market()`
- `calculate_performance()`
- `build_run_manifest()`
- `export_results()`

This function set is the implementation contract, not a claim that the full historical run has already succeeded.

## 6. Reproducibility and fail-closed design

The notebook intends to support reproducibility through:

- deterministic ordering,
- explicit configuration,
- fixed seeds where randomization is used,
- exact feature order,
- hash logging for dataset and risk panels,
- no mutation of source files,
- separate data loading and execution phases.

The fail-closed principle is enforced for all unresolved evidence domains, including:

- calendar validation,
- identity resolution,
- board-lot and odd-lot treatment,
- corporate-action evidence,
- risk-panel completeness,
- solver feasibility,
- valuation availability,
- provenance completeness.

## 7. Documentation and export expectations

The notebook design includes the following output artifacts:

- `predictions.csv`
- `transactions.csv`
- `daily_portfolio.csv`
- `position_valuation.csv`
- `allocation_weights.csv`
- `performance_summary.csv`
- `run_manifest.json`

These outputs are defined as auditable intermediate results, not historical backtest evidence. They are required to be explicit about missing data and blocked conditions.

## 8. Validation strategy

The notebook specification includes synthetic validation tests covering the required decision rules, including:

- dynamic universe change events,
- BANPU and GLOBAL exclusion handling,
- missing Open/Close handling,
- cash-only buy behavior,
- sell-all logic,
- forced-exit ordering,
- solver constraint checks,
- risk-window gating,
- no pairwise covariance deletion,
- no future leakage,
- fee/slippage accounting,
- annualization gating,
- lineage completeness checks.

These tests are documented as synthetic tests only. They do not stand in for validation of an actual historical research backtest.

## 9. Current status

Status summary:

- Implementation architecture: implemented in notebook structure
- Core allocation methods: included in design
- Synthetic validation scaffolding: included in design
- Historical backtest execution: not run
- Research gate: blocked
- Phase F: not authorized

## 10. Known limitations

The implementation must remain explicit about the following unresolved areas:

- official SET calendar verification status,
- corporate-action evidence adequacy,
- board-lot and odd-lot policy resolution,
- complete membership provenance,
- source identity for unresolved snapshots,
- absence of approved risk-free rate and MAR,
- vendor provenance limitations for the execution snapshot.

These items remain blockers and are not converted into pass conditions by the notebook implementation itself.
