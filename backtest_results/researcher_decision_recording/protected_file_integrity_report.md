# Protected File Integrity Report

## Baseline and result

- Repository-wide pre-edit baseline: **20,113 files**, SHA-256 inventory at
  `C:\Users\User\AppData\Local\Temp\workstream_1_8_before.json`.
- Baseline files changed: **7**, all explicitly permitted Phase E decision or mirrored
  status documents listed below.
- Baseline files unchanged: **20,106**, each SHA-256 matched its baseline entry.
- Missing baseline files: **0**.
- Hash mismatches outside the permitted change list: **0**.
- New files: exactly the five requested Workstream 1.8 deliverables in
  `backtest_results/researcher_decision_recording/`; no other new files.
- Unexpected files: **0**.

## Changed existing files

| File | Original SHA-256 | Final SHA-256 | Permitted scope |
|---|---|---|---|
| `backtest_results/phase_E_portfolio_specification/phase_E_decision_register.csv` | `43ce34d96b462134d4d697231573b762ff8ee72de690704fdaeb016bda530a99` | `7cc61072a253a358c7613f2e9fb29ed57a52a5c80eaf0312951d75c8e3bd8c92` | Only E-004 and E-029 rows |
| `backtest_results/phase_E_portfolio_specification/phase_E_revision_changelog.md` | `7f50ea6ec4ef85ba289edfa303891d3d28bbdc6b7578ccd82651594b97874cc1` | `c396b9be24bca2dbe620d0f9a084990b44f580210fa3a36c20f2af5b3506a2e8` | Two entries appended; prior content preserved |
| `backtest_results/phase_E_portfolio_specification/E2_valuation_stale_price_policy.md` | `7e174a993128dfa4cffa8f5420feccc7f7a8118b4ea9975ef66a283592add06a` | `fdfe17bafb150b0b5777bdb569d28c53ec06bc01383ede06f1088aea4eabb121` | E-004 mirror |
| `backtest_results/phase_E_portfolio_specification/E5_cross_method_consistency.md` | `d946ea00905d5ad8482256ee1d5fd81a8e56676677c0706a1393af4121eada14` | `5d748e811d6f24c8c4f080736b17f188f75b861de53276d9fded72726d514a50` | E-029 mirror |
| `backtest_results/phase_E_portfolio_specification/phase_E_summary.md` | `390f4b5fca522ddb6a9caa445cd29a82b14c2172212fd16df3266c0618020f5e` | `bd19ee8fabdd38e511b02eaaeb1f1f24e2d16d4f12ead29e752857551b52ed52` | Decision status and stop-state mirrors |
| `backtest_results/phase_E_portfolio_specification/phase_E_validation_report.md` | `b512b830cf3ea90b7131e9afca542ec7cd3456c4e129035b304607ea12a048ec` | `9c495a9fb83d87bd6fccb1afeaf65f293b316e5c61153040c46b4685c305a4fd` | Decision status and test-scope mirror |
| `backtest_results/phase_E_portfolio_specification/phase_E_manifest.json` | `09a9b4ed1da64d561980738cca00e4bff6ece7a176ea0d48a98cff96c144b47b` | `4f5c7209c55e9c910ee84841903671c05cf45aad6e45cd4bcc6b490ec0d4c0f3` | Status counts, approval list, caveat, and document hashes refreshed |

## Unchanged files and protected scope

All **20,106** other pre-existing repository files are byte-identical by SHA-256 to
the pre-edit baseline. The baseline includes the frozen notebooks, models, datasets,
execution snapshots, archived outputs, Phase A-D artifacts, and prior workstream
reports. No protected asset was changed. No historical data or results were modified.

The only new files are:

- `backtest_results/researcher_decision_recording/decision_recording_audit.md`
- `backtest_results/researcher_decision_recording/decision_register_change_log.csv`
- `backtest_results/researcher_decision_recording/protected_file_integrity_report.md`
- `backtest_results/researcher_decision_recording/decision_recording_validation_report.md`
- `backtest_results/researcher_decision_recording/SHA256SUMS.txt`

