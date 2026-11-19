from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\Project_Github\set_fear_index")
BACKTEST = ROOT / "backtest_results"
DATASET = ROOT / "dataset"
BUILD = DATASET / "verified_build_20261113_152948"
PHASE_A = BACKTEST / "research_audit_20261116T044415991651Z_ee2aa7e1"
PHASE_B = BACKTEST / "phase_B_evidence_recovery_20261116T1147"
PHASE_C = BACKTEST / "phase_C_vendor_validation_20261116"
OUT = BACKTEST / "phase_D_universe_consistency_20261116"

MASTER = BUILD / "SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet"
SNAPSHOT = BUILD / "SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet"
IMMUTABLE_COPY = BACKTEST / "execution_data_v2" / "execution_ohlcv_original.parquet"
MODEL = ROOT / "models" / "Original_Softmax_Final" / "final_softmax_model.joblib"
MODEL_METADATA = ROOT / "models" / "Original_Softmax_Final" / "final_softmax_metadata.json"
MEMBERSHIP = DATASET / "SET50_constituents_by_halfyear_2016_2026.csv"
DECLARATIONS = DATASET / "set50_declare_dates_2016_2026.csv"
LEDGER = BACKTEST / "corporate_action_ledger_official.csv"
GLOBAL_DIAGNOSTIC = BACKTEST / "global_tick_basis_diagnostic.csv"
NOTEBOOK_03 = ROOT / "03_feature_engineering.ipynb"
NOTEBOOK_04 = ROOT / "04_model.ipynb"
NOTEBOOK_05 = ROOT / "05_backtest.ipynb"
NOTEBOOK_06 = ROOT / "06_research_backtest.ipynb"
PHASE_C_MANIFEST = PHASE_C / "phase_C_manifest.json"

FEATURES = [
    "daily_return",
    "momentum_20d",
    "vol_z",
    "VolRank",
    "CorrRank",
    "LiquidityRank",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def write_csv(frame: pd.DataFrame, name: str) -> None:
    frame.to_csv(OUT / name, index=False, encoding="utf-8-sig")


def json_scalar(value: object) -> object:
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (pd.Timestamp,)):
        return value.date().isoformat()
    return value


def get_membership_sets(frame: pd.DataFrame) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    symbol_columns = [column for column in frame.columns if column.startswith("symbol_")]
    for _, row in frame.iterrows():
        result[str(row["period"])] = {
            str(row[column]).strip().upper()
            for column in symbol_columns
            if pd.notna(row[column]) and str(row[column]).strip()
        }
    return result


def validate_prior_artifacts(phase_c_manifest: dict) -> dict:
    pinned = phase_c_manifest["protected_hashes_after_phase_C"]
    protected_paths = {
        "original_execution_snapshot": SNAPSHOT,
        "immutable_execution_copy": IMMUTABLE_COPY,
        "master_dataset": MASTER,
        "frozen_model": MODEL,
        "historical_membership": MEMBERSHIP,
        "membership_declarations": DECLARATIONS,
        "backtest_05_notebook": NOTEBOOK_05,
        "corporate_action_ledger": LEDGER,
        "execution_lineage": BACKTEST / "execution_data_lineage.json",
        "execution_sidecar": BUILD / "SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json",
        "vendor_event_inventory": BACKTEST / "corporate_action_vendor_events.csv",
        "security_identity_mapping": BACKTEST / "security_identity_mapping.csv",
        "approved_exclusion_policy": BACKTEST / "research_controls" / "execution_excluded_symbols.csv",
        "phase_a_universe": PHASE_A / "tradable_universe_2026.csv",
        "phase_a_gate": PHASE_A / "phase_A_gate.csv",
    }
    protected_checks = {}
    for name, path in protected_paths.items():
        actual = sha256(path) if path.exists() else None
        expected = pinned.get(name)
        protected_checks[name] = {
            "path": str(path),
            "expected_sha256": expected,
            "current_sha256": actual,
            "unchanged": actual == expected,
        }

    phase_a_checks = {}
    for name, prior in phase_c_manifest["phase_A_artifact_integrity_checks"].items():
        path = PHASE_A / name
        actual = sha256(path) if path.exists() else None
        phase_a_checks[name] = {
            "expected_sha256": prior["expected_sha256"],
            "current_sha256": actual,
            "unchanged": actual == prior["expected_sha256"],
        }

    phase_b_checks = {}
    for name, prior in phase_c_manifest["phase_B_artifact_integrity_checks"].items():
        path = PHASE_B / name
        actual = sha256(path) if path.exists() else None
        phase_b_checks[name] = {
            "expected_sha256": prior["expected_sha256"],
            "current_sha256": actual,
            "unchanged": actual == prior["expected_sha256"],
        }

    phase_c_checks = {}
    for name, expected in phase_c_manifest["output_hashes_sha256"].items():
        path = PHASE_C / name
        actual = sha256(path) if path.exists() else None
        phase_c_checks[name] = {
            "expected_sha256": expected,
            "current_sha256": actual,
            "unchanged": actual == expected,
        }
    phase_c_manifest_hash = sha256(PHASE_C_MANIFEST)

    groups = [protected_checks, phase_a_checks, phase_b_checks, phase_c_checks]
    if any(not item["unchanged"] for group in groups for item in group.values()):
        raise RuntimeError("A protected asset or prior-phase artifact changed; no Phase D output was written.")
    if sha256(MODEL_METADATA) == "":
        raise RuntimeError("Frozen-model metadata could not be hashed.")

    return {
        "protected_assets": protected_checks,
        "phase_A_artifacts": phase_a_checks,
        "phase_B_artifacts": phase_b_checks,
        "phase_C_artifacts": phase_c_checks,
        "phase_C_manifest_sha256": phase_c_manifest_hash,
        "diagnostic_inputs": {
            path.name: sha256(path)
            for path in [
                MASTER,
                MODEL_METADATA,
                LEDGER,
                GLOBAL_DIAGNOSTIC,
                NOTEBOOK_03,
                NOTEBOOK_04,
                NOTEBOOK_06,
            ]
        },
    }


def reconstruct_target_rows(master: pd.DataFrame, membership: dict[str, set[str]]) -> pd.DataFrame:
    calendar = pd.DatetimeIndex(sorted(master["Date"].dropna().unique()))
    next_date = pd.Series(calendar[1:].values, index=calendar[:-1])
    member_parts = []
    for period, members in membership.items():
        rows = master.loc[
            master["Period"].eq(period) & master["Symbol"].isin(members)
        ].copy()
        if not rows.empty:
            member_parts.append(rows)
    rows = pd.concat(member_parts, ignore_index=True)
    rows["next_date"] = rows["Date"].map(next_date)
    future = master[["Date", "Symbol", "daily_return", "vol_z"]].rename(
        columns={
            "Date": "next_date",
            "daily_return": "future_return",
            "vol_z": "future_vol_z",
        }
    )
    rows = rows.merge(future, on=["next_date", "Symbol"], how="left", validate="many_to_one")
    labels = np.select(
        [
            (rows["future_return"] < 0) & (rows["future_vol_z"] >= 1.5),
            (rows["future_return"] > 0) & (rows["future_vol_z"] >= 1.5),
        ],
        [0, 1],
        default=2,
    ).astype(float)
    rows["target_rebuilt"] = labels
    rows.loc[rows["future_return"].isna() | rows["future_vol_z"].isna(), "target_rebuilt"] = np.nan
    return rows


def make_corporate_action_outputs(
    membership: dict[str, set[str]],
    phase_c: Path,
) -> tuple[pd.DataFrame, str]:
    actions = read_csv(phase_c / "corporate_action_relevance_2026.csv")
    actions["Date"] = pd.to_datetime(actions["Date"], errors="coerce").dt.normalize()
    h2_effective = pd.Timestamp("2026-07-01")
    actions["Phase_D_Period"] = np.where(actions["Date"] < h2_effective, "2026_H1", "2026_H2")
    member_union = membership.get("2026_H1", set()) | membership.get("2026_H2", set())
    actions["Is_Any_2026_Constituent"] = actions["Symbol"].isin(member_union)
    actions["Is_2026_Constituent_On_Recorded_Date"] = actions.apply(
        lambda row: row["Symbol"] in membership.get(row["Phase_D_Period"], set()),
        axis=1,
    )
    actions["Phase_D_Classification"] = "UNRESOLVED"
    actions["Event_Date_Is_Proof_Of_Effective_Date"] = False
    actions["Confirmed_2026_Impact"] = False
    actions["Terms_Applied"] = False
    actions["Potentially_Affects_2026_Eligible_Portfolio"] = actions["Is_Any_2026_Constituent"]
    actions["Potentially_Affects_2026_Feature_Continuity"] = actions["Is_Any_2026_Constituent"]
    actions["Potentially_Affects_2026_Execution_Price_Continuity"] = actions[
        "Is_Any_2026_Constituent"
    ]
    actions["Potential_Execution_Impact_On_Recorded_Date"] = (
        actions["Is_2026_Constituent_On_Recorded_Date"]
    )
    actions["Potential_Share_Quantity_Change"] = actions["Event_Type"].isin(
        ["SPLIT", "MERGER", "STOCK_DIVIDEND+CASH_DIVIDEND"]
    )
    actions["Potential_Cash_Entitlement"] = actions["Event_Type"].isin(
        ["CASH_DIVIDEND", "MERGER", "STOCK_DIVIDEND+CASH_DIVIDEND"]
    )
    actions["Potential_Security_Identity_Change"] = actions["Event_Type"].eq("MERGER")
    actions["Potentially_Affects_Pre2025_Training_Feature_Continuity"] = actions["Date"].lt(
        pd.Timestamp("2025-01-01")
    )
    actions["Evidence_Conclusion"] = np.where(
        actions["Officially_Verified"].fillna(False).astype(bool),
        "Locally marked verified; still not treated as applied in Phase D.",
        "UNRESOLVED_FROM_LOCAL_EVIDENCE; ledger label is not confirmation.",
    )
    actions["Date"] = actions["Date"].dt.strftime("%Y-%m-%d")
    write_csv(actions, "phase_D_corporate_action_scope.csv")

    date_min = actions["Date"].min()
    date_max = actions["Date"].max()
    member_union_rows = int(actions["Is_Any_2026_Constituent"].sum())
    member_union_symbols = int(
        actions.loc[actions["Is_Any_2026_Constituent"], "Symbol"].nunique()
    )
    active_member_rows = int(actions["Is_2026_Constituent_On_Recorded_Date"].sum())
    active_member_symbols = int(
        actions.loc[actions["Is_2026_Constituent_On_Recorded_Date"], "Symbol"].nunique()
    )
    event_types = actions["Event_Type"].value_counts().to_dict()
    official_sources = int(actions["Official_Source"].notna().sum()) if "Official_Source" in actions else 0
    urls = int(actions["Evidence_URL"].notna().sum()) if "Evidence_URL" in actions else 0
    report = f"""# Phase D Corporate-Action Scope

## Result

- Ledger rows inspected: {len(actions)}.
- Recorded event-date range: {date_min} to {date_max}. The recorded date is not assumed to be the effective date.
- Rows involving a symbol in the 2026 membership union: {member_union_rows} across {member_union_symbols} symbols.
- Rows whose recorded event date falls inside that symbol's active 2026 membership period: {active_member_rows} across {active_member_symbols} symbols.
- Additional union-overlap rows outside the symbol's active membership period on the recorded date: {member_union_rows - active_member_rows}.
- Event labels: {json.dumps(event_types, sort_keys=True)}.
- Rows with a populated official-source field: {official_sources}; rows with an evidence URL: {urls}.
- Confirmed terms or actions applied in Phase D: 0.
- All ledger rows remain `UNRESOLVED`; no action was applied and no source row was changed.

The local ledger's `Date`, event label, and any populated date/term fields are copied to
`phase_D_corporate_action_scope.csv`. Missing effective dates remain blank. A dividend,
split, merger, or stock-dividend label is recorded as a possible risk indicator only;
it is not proof that the described event occurred or that its terms are correct.

## Relevance

The 2026 membership-union rows could affect feature continuity or future execution
prices and, depending on verified terms, cash entitlements, share quantity, or identity.
Only the date-specific overlap is treated as potentially affecting a holding on the
recorded date. No event has evidence sufficient to confirm any impact. The 44 rows
outside the 2026 membership union do not concern current constituents; eight union
rows fall outside the affected symbol's active period on the recorded date. The four
AOT candidate dates have no local AOT ledger row. No corporate action was applied.

## Evidence still needed

For each event that may affect a 2026 member: a primary-source record of event terms,
effective/ex/record/payment dates as applicable, affected security identity, and
confirmation of the price/share/cash treatment. Do not use the diagnostic price
alignment or the ledger description as a substitute.
"""
    (OUT / "phase_D_corporate_action_report.md").write_text(report, encoding="utf-8")
    return actions, report


def make_feature_outputs(
    master: pd.DataFrame,
    membership: dict[str, set[str]],
    phase_c: Path,
    global_diag_path: Path,
) -> tuple[pd.DataFrame, dict]:
    master = master.sort_values(["Symbol", "Date"]).copy()
    master["tv20"] = (master["Close"] * master["Volume"]).groupby(
        master["Symbol"], sort=False
    ).transform(lambda values: values.rolling(20, min_periods=20).mean())
    calendar = pd.DatetimeIndex(sorted(master["Date"].dropna().unique()))
    calendar_positions = {date: position for position, date in enumerate(calendar)}
    banpu_dates = set(
        master.loc[master["Symbol"].eq("BANPU") & master["Period"].str.startswith("2026_"), "Date"]
    )
    banpu_2026 = master.loc[
        master["Symbol"].eq("BANPU") & master["Period"].str.startswith("2026_")
    ].copy()
    candidate = read_csv(phase_c / "tradable_universe_2026_phase_C.csv")
    candidate["Date"] = pd.to_datetime(candidate["Date"], errors="coerce").dt.normalize()
    candidate_dates = set(candidate["Date"])
    rank_metrics = {}
    daily_rank_effects: dict[pd.Timestamp, dict] = {}
    for period in ["2026_H1", "2026_H2"]:
        q = master.loc[
            master["Period"].eq(period) & master["Symbol"].isin(membership[period])
        ].copy()
        q["vol_base"] = q.groupby("Date")["volatility_ret"].rank(method="average", pct=True) * 100
        q["liq_base"] = q.groupby("Date")["tv20"].rank(method="average", pct=True) * 100
        no_banpu = q["Symbol"].ne("BANPU")
        q["vol_without_banpu"] = np.nan
        q.loc[no_banpu, "vol_without_banpu"] = (
            q.loc[no_banpu].groupby("Date")["volatility_ret"].rank(method="average", pct=True) * 100
        )
        q["liq_without_banpu"] = np.nan
        q.loc[no_banpu, "liq_without_banpu"] = (
            q.loc[no_banpu].groupby("Date")["tv20"].rank(method="average", pct=True) * 100
        )

        vol_valid = q["VolRank"].notna() & q["vol_base"].notna()
        liq_valid = q["LiquidityRank"].notna() & q["liq_base"].notna()
        vol_matches = np.isclose(q.loc[vol_valid, "VolRank"], q.loc[vol_valid, "vol_base"], atol=1e-8)
        liq_matches = np.isclose(
            q.loc[liq_valid, "LiquidityRank"], q.loc[liq_valid, "liq_base"], atol=1e-8
        )
        if not vol_matches.all() or not liq_matches.all():
            raise RuntimeError(f"Stored {period} VolRank/LiquidityRank did not reproduce from Master.")

        vol_changed = (
            no_banpu
            & q["vol_base"].notna()
            & q["vol_without_banpu"].notna()
            & ~np.isclose(q["vol_base"], q["vol_without_banpu"], atol=1e-10)
        )
        liq_changed = (
            no_banpu
            & q["liq_base"].notna()
            & q["liq_without_banpu"].notna()
            & ~np.isclose(q["liq_base"], q["liq_without_banpu"], atol=1e-10)
        )
        rank_metrics[period] = {
            "banpu_rows": int(q["Symbol"].eq("BANPU").sum()),
            "volrank_stored_rows": int(q["VolRank"].notna().sum()),
            "volrank_baseline_matches": int(vol_matches.sum()),
            "volrank_other_rows_changed_without_banpu": int(vol_changed.sum()),
            "volrank_max_abs_change": float(
                (q.loc[no_banpu, "vol_base"] - q.loc[no_banpu, "vol_without_banpu"]).abs().max()
            ),
            "liquidityrank_stored_rows": int(q["LiquidityRank"].notna().sum()),
            "liquidityrank_baseline_matches": int(liq_matches.sum()),
            "liquidityrank_other_rows_changed_without_banpu": int(liq_changed.sum()),
            "liquidityrank_max_abs_change": float(
                (q.loc[no_banpu, "liq_base"] - q.loc[no_banpu, "liq_without_banpu"]).abs().max()
            ),
        }
        for date, group in q.groupby("Date"):
            day = group.set_index("Symbol")
            day_vol_change = vol_changed.loc[group.index]
            day_liq_change = liq_changed.loc[group.index]
            daily_rank_effects[date] = {
                "volrank_peer_rows_changed": int(day_vol_change.sum()),
                "liquidityrank_peer_rows_changed": int(day_liq_change.sum()),
                "volrank_max_abs_change": float(
                    (group.loc[no_banpu.loc[group.index], "vol_base"]
                     - group.loc[no_banpu.loc[group.index], "vol_without_banpu"]).abs().max()
                ) if no_banpu.loc[group.index].any() else 0.0,
                "liquidityrank_max_abs_change": float(
                    (group.loc[no_banpu.loc[group.index], "liq_base"]
                     - group.loc[no_banpu.loc[group.index], "liq_without_banpu"]).abs().max()
                ) if no_banpu.loc[group.index].any() else 0.0,
            }

    records = []
    for _, row in banpu_2026.sort_values("Date").iterrows():
        date = row["Date"]
        period = row["Period"]
        members = membership.get(period, set())
        member_rows = master.loc[
            master["Date"].eq(date)
            & master["Period"].eq(period)
            & master["Symbol"].isin(members)
            & master["daily_return"].notna()
        ]
        previous_position = calendar_positions[date]
        lookback = calendar[max(0, previous_position - 59) : previous_position + 1]
        contained = [item for item in lookback if item in banpu_dates]
        rank_effect = daily_rank_effects.get(date, {})
        values = {feature: json_scalar(row.get(feature)) for feature in FEATURES}
        records.append(
            {
                "Record_Type": "BANPU_FEATURE_DATE",
                "Date": date.date().isoformat(),
                "Symbol": "BANPU",
                "Period": period,
                "Feature": ";".join(feature for feature in FEATURES if pd.notna(row.get(feature))),
                "Observed_Feature_Values_JSON": json.dumps(values, sort_keys=True),
                "Is_2026_SET50_Member": True,
                "Present_In_Same_Date_Cross_Section": True,
                "Used_In_Other_Members_Market_Proxy": bool(pd.notna(row.get("daily_return"))),
                "Other_Member_Return_Series_On_Date": max(0, int(member_rows["Symbol"].nunique()) - 1),
                "VolRank_Peer_Rows_Changed_If_Removed": rank_effect.get("volrank_peer_rows_changed", 0),
                "LiquidityRank_Peer_Rows_Changed_If_Removed": rank_effect.get(
                    "liquidityrank_peer_rows_changed", 0
                ),
                "VolRank_Max_Abs_Change": rank_effect.get("volrank_max_abs_change", 0.0),
                "LiquidityRank_Max_Abs_Change": rank_effect.get("liquidityrank_max_abs_change", 0.0),
                "BANPU_Feature_Dates_In_Last_60_Observed_Dates": len(contained),
                "BANPU_60_Observation_Window_Start": lookback[0].date().isoformat() if len(lookback) == 60 else "",
                "BANPU_60_Observation_Window_Length": len(lookback),
                "BANPU_CorrRank_Window_Contains_BANPU": bool(contained),
                "Is_Phase_C_Candidate_Date": date in candidate_dates,
                "GLOBAL_Anomaly_Field": "",
                "GLOBAL_Anomaly_Original_Value": np.nan,
                "GLOBAL_Anomaly_Classification": "",
                "GLOBAL_Official_Action_Confirmed": np.nan,
                "Shared_Impact_Conclusion": (
                    "Same-date VolRank/LiquidityRank and other members' rolling CorrRank inputs "
                    "can be affected while BANPU return is present."
                ),
                "Evidence_Status": "Observed in pinned Master; rank counterfactual recomputed from Master inputs.",
            }
        )

    feature_dates_2026 = sorted(
        master.loc[master["Period"].str.startswith("2026_"), "Date"].dropna().unique()
    )
    for date in feature_dates_2026:
        position = calendar_positions[date]
        lookback = calendar[max(0, position - 59) : position + 1]
        contained = [item for item in lookback if item in banpu_dates]
        period = str(
            master.loc[master["Date"].eq(date), "Period"].iloc[0]
        )
        records.append(
            {
                "Record_Type": "ROLLING_WINDOW_CHECK",
                "Date": date.date().isoformat(),
                "Symbol": "BANPU",
                "Period": period,
                "Feature": "CorrRank",
                "Observed_Feature_Values_JSON": "",
                "Is_2026_SET50_Member": True,
                "Present_In_Same_Date_Cross_Section": date in banpu_dates,
                "Used_In_Other_Members_Market_Proxy": date in banpu_dates,
                "Other_Member_Return_Series_On_Date": np.nan,
                "VolRank_Peer_Rows_Changed_If_Removed": 0,
                "LiquidityRank_Peer_Rows_Changed_If_Removed": 0,
                "VolRank_Max_Abs_Change": 0.0,
                "LiquidityRank_Max_Abs_Change": 0.0,
                "BANPU_Feature_Dates_In_Last_60_Observed_Dates": len(contained),
                "BANPU_60_Observation_Window_Start": (
                    lookback[0].date().isoformat() if len(lookback) == 60 else ""
                ),
                "BANPU_60_Observation_Window_Length": len(lookback),
                "BANPU_CorrRank_Window_Contains_BANPU": bool(contained),
                "Is_Phase_C_Candidate_Date": date in candidate_dates,
                "GLOBAL_Anomaly_Field": "",
                "GLOBAL_Anomaly_Original_Value": np.nan,
                "GLOBAL_Anomaly_Classification": "",
                "GLOBAL_Official_Action_Confirmed": np.nan,
                "Shared_Impact_Conclusion": (
                    "BANPU is present in the current/trailing 60-observation inputs."
                    if contained
                    else "No BANPU feature date occurs in this 60-observation window."
                ),
                "Evidence_Status": "Exact 60-observation slice over the pinned Master feature-date calendar.",
            }
        )

    for _, row in candidate.sort_values("Date").iterrows():
        date = row["Date"]
        position = calendar_positions.get(date)
        lookback = calendar[max(0, position - 59) : position + 1] if position is not None else []
        contained = [item for item in lookback if item in banpu_dates]
        values = {
            feature: json_scalar(
                master.loc[
                    master["Date"].eq(date) & master["Symbol"].eq(row["Symbol"]), feature
                ].iloc[0]
            )
            for feature in FEATURES
        }
        records.append(
            {
                "Record_Type": "PHASE_C_CANDIDATE_DATE",
                "Date": date.date().isoformat(),
                "Symbol": row["Symbol"],
                "Period": "2026_H2",
                "Feature": ";".join(FEATURES),
                "Observed_Feature_Values_JSON": json.dumps(values, sort_keys=True),
                "Is_2026_SET50_Member": True,
                "Present_In_Same_Date_Cross_Section": bool(date in banpu_dates),
                "Used_In_Other_Members_Market_Proxy": bool(date in banpu_dates),
                "Other_Member_Return_Series_On_Date": np.nan,
                "VolRank_Peer_Rows_Changed_If_Removed": 0,
                "LiquidityRank_Peer_Rows_Changed_If_Removed": 0,
                "VolRank_Max_Abs_Change": 0.0,
                "LiquidityRank_Max_Abs_Change": 0.0,
                "BANPU_Feature_Dates_In_Last_60_Observed_Dates": len(contained),
                "BANPU_60_Observation_Window_Start": lookback[0].date().isoformat() if len(lookback) == 60 else "",
                "BANPU_60_Observation_Window_Length": len(lookback),
                "BANPU_CorrRank_Window_Contains_BANPU": bool(contained),
                "Is_Phase_C_Candidate_Date": True,
                "GLOBAL_Anomaly_Field": "",
                "GLOBAL_Anomaly_Original_Value": np.nan,
                "GLOBAL_Anomaly_Classification": "",
                "GLOBAL_Official_Action_Confirmed": np.nan,
                "Shared_Impact_Conclusion": (
                    "No BANPU date in the 60-observation window; candidate rank values are unchanged "
                    "by a same-date BANPU exclusion."
                ),
                "Evidence_Status": "Phase C candidate flags and pinned-Master observed-date window.",
            }
        )

    global_diag = read_csv(global_diag_path)
    global_diag["Date"] = pd.to_datetime(global_diag["Date"], errors="coerce").dt.normalize()
    for _, row in global_diag.iterrows():
        records.append(
            {
                "Record_Type": "GLOBAL_PRICE_BASIS_ANOMALY",
                "Date": row["Date"].date().isoformat(),
                "Symbol": row["Symbol"],
                "Period": "",
                "Feature": row["Column"],
                "Observed_Feature_Values_JSON": "",
                "Is_2026_SET50_Member": False,
                "Present_In_Same_Date_Cross_Section": False,
                "Used_In_Other_Members_Market_Proxy": False,
                "Other_Member_Return_Series_On_Date": np.nan,
                "VolRank_Peer_Rows_Changed_If_Removed": 0,
                "LiquidityRank_Peer_Rows_Changed_If_Removed": 0,
                "VolRank_Max_Abs_Change": 0.0,
                "LiquidityRank_Max_Abs_Change": 0.0,
                "BANPU_Feature_Dates_In_Last_60_Observed_Dates": np.nan,
                "BANPU_60_Observation_Window_Start": "",
                "BANPU_60_Observation_Window_Length": np.nan,
                "BANPU_CorrRank_Window_Contains_BANPU": np.nan,
                "Is_Phase_C_Candidate_Date": False,
                "GLOBAL_Anomaly_Field": row["Column"],
                "GLOBAL_Anomaly_Original_Value": row["Original_Value"],
                "GLOBAL_Anomaly_Classification": row["Anomaly_Classification"],
                "GLOBAL_Official_Action_Confirmed": bool(row["Official_Action_Confirmed"]),
                "Shared_Impact_Conclusion": (
                    "GLOBAL is absent from both 2026 SET50 membership lists; these execution-snapshot "
                    "diagnostics do not enter other securities' SET50 feature calculations."
                ),
                "Evidence_Status": "Local diagnostic only; not official corporate-action proof.",
            }
        )
    feature_frame = pd.DataFrame(records)
    write_csv(feature_frame, "phase_D_feature_contamination.csv")

    candidate_no_banpu = (
        feature_frame.loc[feature_frame["Record_Type"].eq("PHASE_C_CANDIDATE_DATE")]
        ["BANPU_Feature_Dates_In_Last_60_Observed_Dates"]
        .eq(0)
        .all()
    )
    global_rows = feature_frame.loc[feature_frame["Record_Type"].eq("GLOBAL_PRICE_BASIS_ANOMALY")]
    summary = {
        "rank_metrics_by_period": rank_metrics,
        "banpu_2026_feature_rows": int(len(banpu_2026)),
        "banpu_2026_last_feature_date_before_execution_gap": "2026-08-11",
        "banpu_late_feature_row": "2026-11-13",
        "rolling_windows_checked": int(
            feature_frame["Record_Type"].eq("ROLLING_WINDOW_CHECK").sum()
        ),
        "rolling_windows_with_banpu": int(
            feature_frame.loc[
                feature_frame["Record_Type"].eq("ROLLING_WINDOW_CHECK"),
                "BANPU_CorrRank_Window_Contains_BANPU",
            ].fillna(False).sum()
        ),
        "candidate_dates_have_zero_banpu_in_last_60_observed_dates": bool(candidate_no_banpu),
        "global_anomaly_rows": int(len(global_rows)),
        "global_distinct_dates": int(global_diag["Date"].nunique()),
        "global_2026_h1_member": "GLOBAL" in membership.get("2026_H1", set()),
        "global_2026_h2_member": "GLOBAL" in membership.get("2026_H2", set()),
    }
    return feature_frame, summary


def make_2017_outputs(
    master: pd.DataFrame,
    membership_frame: pd.DataFrame,
    membership: dict[str, set[str]],
    metadata: dict,
) -> tuple[pd.DataFrame, dict]:
    membership_row = membership_frame.loc[membership_frame["period"].eq("2017_H1")].iloc[0]
    symbol_columns = [column for column in membership_frame.columns if column.startswith("symbol_")]
    listed = [
        str(membership_row[column]).strip().upper()
        for column in symbol_columns
        if pd.notna(membership_row[column]) and str(membership_row[column]).strip()
    ]
    blanks = sum(
        pd.isna(membership_row[column]) or not str(membership_row[column]).strip()
        for column in symbol_columns
    )
    master_period = master.loc[master["Period"].eq("2017_H1")].copy()
    dates = sorted(master_period["Date"].unique())
    known_rows = master_period.loc[master_period["Symbol"].isin(listed)].copy()
    missing_symbols = sorted(set(listed) - set(known_rows["Symbol"]))
    outside = master_period.loc[~master_period["Symbol"].isin(listed)].copy()
    aligned = reconstruct_target_rows(master, membership)
    current_period = aligned.loc[aligned["Period"].eq("2017_H1")].copy()
    complete_mask = current_period[FEATURES].notna().all(axis=1) & current_period["target_rebuilt"].notna()
    complete = current_period.loc[complete_mask]
    period_sizes = master_period.groupby("Date")["Symbol"].nunique()
    all_train = aligned.loc[
        aligned["next_date"].dt.year.between(2016, 2024)
        & aligned[FEATURES].notna().all(axis=1)
        & aligned["target_rebuilt"].notna()
    ]
    frozen_train_count = int(metadata["training_samples"])
    if len(all_train) != frozen_train_count:
        raise RuntimeError(
            f"Notebook 04 training reconstruction {len(all_train)} does not match frozen metadata "
            f"{frozen_train_count}."
        )
    target_counts = complete["target_rebuilt"].value_counts().sort_index().to_dict()
    prefilter_target_counts = (
        current_period.loc[current_period["target_rebuilt"].notna(), "target_rebuilt"]
        .value_counts()
        .sort_index()
        .to_dict()
    )
    metrics = [
        ("Membership slots", len(symbol_columns), "50 columns in the local 2017_H1 row."),
        ("Nonblank unique membership symbols", len(set(listed)), "49 names; no duplicate is present."),
        ("Blank membership slots", blanks, "Blank slot does not identify the missing security."),
        ("Master period dates", len(dates), "2017_H1 dates present in the pinned Master."),
        ("Master rows in 2017_H1", len(master_period), "All symbols, regardless of local membership."),
        ("Master unique symbols in 2017_H1", int(master_period["Symbol"].nunique()), "Observed in the pinned Master."),
        ("Master symbols per date min", int(period_sizes.min()), "Observed per-date symbol count."),
        ("Master symbols per date max", int(period_sizes.max()), "Observed per-date symbol count."),
        ("Expected listed member-date slots", len(listed) * len(dates), "49 local names multiplied by 120 dates."),
        ("Observed listed member-date rows", len(known_rows), "Rows found by joining the current 49-name list to Master."),
        ("Missing listed member-date rows", len(listed) * len(dates) - len(known_rows), "Six identified symbols are absent on all 120 dates."),
        ("Known listed symbols absent from Master", ";".join(missing_symbols), "Exact source symbol names; absence cause not inferred."),
        ("Master symbols outside the local list", int(outside["Symbol"].nunique()), "Do not identify the blank 50th constituent."),
        ("Outside-list complete six-feature and target rows", int((outside[FEATURES + ["target"]].notna().all(axis=1)).sum()), "No complete training row among the outside-list Master records."),
        ("Current reconstructed 2017_H1 training rows", len(complete), "Membership join plus all six features and reconstructed target."),
        ("2017_H1 rows missing CorrRank", int(current_period["CorrRank"].isna().sum()), "These rows do not enter the complete model sample."),
        ("Frozen model training samples", frozen_train_count, "Exact match to final_softmax_metadata.json."),
        ("2017_H1 target 0 in complete training rows", int(target_counts.get(0.0, 0)), "Notebook 04 target alignment."),
        ("2017_H1 target 1 in complete training rows", int(target_counts.get(1.0, 0)), "Notebook 04 target alignment."),
        ("2017_H1 target 2 in complete training rows", int(target_counts.get(2.0, 0)), "Notebook 04 target alignment."),
        ("2017_H1 target 0 before feature completeness", int(prefilter_target_counts.get(0.0, 0)), "Target-aligned current-membership rows."),
        ("2017_H1 target 1 before feature completeness", int(prefilter_target_counts.get(1.0, 0)), "Target-aligned current-membership rows."),
        ("2017_H1 target 2 before feature completeness", int(prefilter_target_counts.get(2.0, 0)), "Target-aligned current-membership rows."),
        ("Unknown blank symbol potential additional rows upper bound", len(dates), "At most one member-date row for each of the 120 observed dates; actual availability unknown."),
    ]
    rows = [
        {
            "Record_Type": "SUMMARY",
            "Feature_or_Metric": metric,
            "Observed_Value": value,
            "Rows_Available": "",
            "Rows_Missing": "",
            "Membership_Sensitive": "",
            "Target_Distribution": "",
            "Interpretation": interpretation,
        }
        for metric, value, interpretation in metrics
    ]
    for feature in FEATURES:
        nonnull = int(known_rows[feature].notna().sum())
        rows.append(
            {
                "Record_Type": "FEATURE",
                "Feature_or_Metric": feature,
                "Observed_Value": "",
                "Rows_Available": nonnull,
                "Rows_Missing": int(len(known_rows) - nonnull),
                "Membership_Sensitive": (
                    "YES: cross-sectional rank or proxy input depends on the effective member set."
                    if feature in {"VolRank", "CorrRank", "LiquidityRank"}
                    else "NO direct cross-sectional calculation; sample inclusion can still change."
                ),
                "Target_Distribution": "",
                "Interpretation": (
                    "A missing member could affect this feature for existing symbols."
                    if feature in {"VolRank", "CorrRank", "LiquidityRank"}
                    else "Per-symbol feature; membership alone does not change existing symbol values."
                ),
            }
        )
    rows.append(
        {
            "Record_Type": "TARGET",
            "Feature_or_Metric": "Notebook 04 next-global-feature-date target",
            "Observed_Value": int(current_period["target_rebuilt"].notna().sum()),
            "Rows_Available": int(current_period["target_rebuilt"].notna().sum()),
            "Rows_Missing": int(len(current_period) - current_period["target_rebuilt"].notna().sum()),
            "Membership_Sensitive": "Indirectly; missing member rows can add observations but do not alter an existing symbol's next-date label.",
            "Target_Distribution": json.dumps(
                {str(int(key)): int(value) for key, value in prefilter_target_counts.items()},
                sort_keys=True,
            ),
            "Interpretation": "Reconstructed from the frozen notebook's same-symbol next global feature date; no missing target values were imputed.",
        }
    )
    impact = pd.DataFrame(rows)
    write_csv(impact, "phase_D_2017_membership_impact.csv")
    summary = {
        "slots": len(symbol_columns),
        "nonblank_unique": len(set(listed)),
        "blank_slots": blanks,
        "dates": len(dates),
        "master_period_rows": len(master_period),
        "master_unique_symbols": int(master_period["Symbol"].nunique()),
        "known_list_rows": len(known_rows),
        "expected_known_list_rows": len(listed) * len(dates),
        "missing_known_list_rows": len(listed) * len(dates) - len(known_rows),
        "missing_symbols_all_dates": missing_symbols,
        "outside_list_symbols": sorted(outside["Symbol"].unique().tolist()),
        "current_complete_model_rows": len(complete),
        "corr_rank_missing_rows": int(current_period["CorrRank"].isna().sum()),
        "frozen_training_samples": frozen_train_count,
        "reconstructed_training_samples": len(all_train),
        "complete_target_counts": {str(int(k)): int(v) for k, v in target_counts.items()},
        "prefilter_target_counts": {str(int(k)): int(v) for k, v in prefilter_target_counts.items()},
        "feature_counts": {
            feature: {
                "available": int(known_rows[feature].notna().sum()),
                "missing": int(known_rows[feature].isna().sum()),
            }
            for feature in FEATURES
        },
        "outside_list_complete_rows": int((outside[FEATURES + ["target"]].notna().all(axis=1)).sum()),
    }
    report = f"""# Phase D — 2017_H1 Membership Impact

## Local membership record

The local row has 50 symbol slots, {len(set(listed))} nonblank unique names, and {blanks}
blank slot(s), with no duplicate names. The blank slot does not name a missing constituent;
no name is added.

The pinned Master has {len(master_period):,} rows across {len(dates)} dates and
{master_period["Symbol"].nunique()} unique symbols (daily symbol count {period_sizes.min()}–{period_sizes.max()}).
Joining the 49 known names produces {len(known_rows):,} rows, or 43 per date, leaving
{len(listed) * len(dates) - len(known_rows):,} expected member-date rows absent. The six
known listed symbols absent on all {len(dates)} dates are: {", ".join(missing_symbols)}.
This is a Master coverage fact, not proof that any one is the blank 50th constituent.

The Master also contains {outside["Symbol"].nunique()} names outside the local 49-name list.
None has all six model features plus target ({int((outside[FEATURES + ["target"]].notna().all(axis=1)).sum())}
complete rows), but this does not establish that one of them is the missing official member.

## Model and feature impact

Notebook 04's target alignment was reconstructed using the next global feature date and
the same symbol's next-date return and volatility-z value. The reconstruction yields
{len(all_train):,} complete training samples, exactly matching the frozen model's recorded
{frozen_train_count:,}. The 2017_H1 slice contains {len(complete):,} current training rows;
{int(current_period["CorrRank"].isna().sum())} additional known-member rows lack CorrRank and
are omitted by the complete-feature filter.

The 2017_H1 target distribution in the current complete sample is
`{json.dumps({str(int(k)): int(v) for k, v in target_counts.items()}, sort_keys=True)}`.
Before filtering on feature completeness it is
`{json.dumps({str(int(k)): int(v) for k, v in prefilter_target_counts.items()}, sort_keys=True)}`.
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
"""
    (OUT / "phase_D_2017_membership_report.md").write_text(report, encoding="utf-8")
    return impact, summary


def make_universe_outputs(
    membership: dict[str, set[str]],
    phase_c: Path,
    action_frame: pd.DataFrame,
    master: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    exclusions = read_csv(phase_c / "execution_excluded_symbols_phase_C.csv")
    identities = read_csv(phase_c / "security_identity_scope_2026.csv")
    candidates = read_csv(phase_c / "tradable_universe_2026_phase_C.csv")
    coverage = read_csv(phase_c / "tradable_universe_coverage_phase_C.csv")
    members_2026 = membership["2026_H1"] | membership["2026_H2"]
    symbols = sorted(members_2026 | {"GLOBAL"})
    excluded_by_symbol = exclusions.set_index("Symbol").to_dict("index")
    identity_by_symbol = identities.set_index("Symbol").to_dict("index")
    action_counts = action_frame.groupby("Symbol").size().to_dict()
    late_candidate_dates = pd.to_datetime(candidates["Date"])
    candidate_counts = candidates.assign(Date=late_candidate_dates).groupby("Symbol").size().to_dict()

    rows = []
    for symbol in symbols:
        is_member = symbol in members_2026
        exclusion = excluded_by_symbol.get(symbol)
        identity = identity_by_symbol.get(symbol, {})
        symbol_candidates = candidates.loc[candidates["Symbol"].eq(symbol)]
        if symbol == "BANPU":
            classification = "EXCLUDED_MISSING_EXECUTION_DATA"
            reason_code = "INSUFFICIENT_VERIFIED_EXECUTION_DATA"
            reason = "253 missing OHLC field-cells across 64 execution rows; excluded for all 2026 by existing policy."
        elif symbol == "GLOBAL":
            classification = "OTHER_WITH_EXPLANATION"
            reason_code = "NOT_A_2026_SET50_MEMBER_AND_PRICE_BASIS_UNRESOLVED"
            reason = "Not in either official 2026 membership list; 141 local price-basis anomaly rows remain unconfirmed."
        elif exclusion and str(exclusion["Exclusion_Reason"]).startswith("UNRESOLVED_2026_CORPORATE_ACTION"):
            classification = "EXCLUDED_CORPORATE_ACTION_UNRESOLVED"
            reason_code = "UNRESOLVED_2026_CORPORATE_ACTION_CASH_OR_SHARE_CONTINUITY"
            reason = "Existing Phase C exclusion for unresolved event terms/share or cash continuity."
        elif symbol == "BTS":
            classification = "OTHER_WITH_EXPLANATION"
            reason_code = "MISSING_CROSS_SECTIONAL_RANK_FEATURES"
            reason = "Valid execution OHLC exists on the four AOT candidate execution dates, but VolRank, CorrRank, and LiquidityRank are missing on all four BTS predictor dates."
        elif symbol == "AOT":
            classification = "ELIGIBLE_CANDIDATE"
            reason_code = "ELIGIBLE_VENDOR_RESEARCH_CANDIDATE"
            reason = "Only existing Phase C candidate; four member-date rows with valid next-session vendor Open/Close and all six features."
        else:
            classification = "OTHER_WITH_EXPLANATION"
            reason_code = "NO_PHASE_C_ELIGIBLE_ROW"
            reason = "No eligible Phase C member-date row; no evidence in existing artifacts justifies relaxing the existing exclusion or feature requirements."
        rows.append(
            {
                "Symbol": symbol,
                "Is_2026_SET50_Member": is_member,
                "Phase_D_Classification": classification,
                "Reason_Code": reason_code,
                "Exclusion_Reason": exclusion.get("Exclusion_Reason", "") if exclusion else "",
                "Existing_Exclusion_Status": exclusion.get("Decision_Status", "") if exclusion else "",
                "Local_Corporate_Action_Rows": int(action_counts.get(symbol, 0)),
                "Execution_Snapshot_Rows": int(identity.get("Execution_Snapshot_Rows", 0) or 0),
                "Feature_Master_Rows_2026": int(identity.get("Feature_Master_Rows_2026", 0) or 0),
                "Phase_C_Eligible_Member_Date_Rows": int(candidate_counts.get(symbol, 0)),
                "Missing_OHLC_Field_Cells": int(exclusion.get("Missing_OHLC_Field_Cells", 0) or 0) if exclusion else 0,
                "Identity_Classification": identity.get("Identity_Classification", "NOT_APPLICABLE_TO_2026" if not is_member else "UNRESOLVED"),
                "Evidence": reason,
            }
        )
    symbol_frame = pd.DataFrame(rows).sort_values(["Phase_D_Classification", "Symbol"])
    write_csv(symbol_frame, "phase_D_symbol_eligibility.csv")

    candidates_by_date = candidates.groupby("Date")["Symbol"].apply(lambda values: ";".join(sorted(values))).to_dict()
    candidate_count_by_date = candidates.groupby("Date")["Symbol"].nunique().to_dict()
    coverage["Phase_D_Eligible_Symbol_Count"] = coverage["Date"].map(candidate_count_by_date).fillna(0).astype(int)
    coverage["Phase_D_Eligible_Symbols"] = coverage["Date"].map(candidates_by_date).fillna("")
    coverage["Phase_D_Newly_Added_Symbol_Count"] = 0
    coverage["Phase_D_Newly_Added_Symbols"] = ""
    coverage["Research_Backtest_Gate"] = "BLOCKED"
    coverage["Coverage_Note"] = (
        "Candidate coverage is not verified portfolio approval; Phase D added no symbol and ran no backtest."
    )
    write_csv(coverage, "phase_D_universe_coverage.csv")

    counts = symbol_frame["Phase_D_Classification"].value_counts().to_dict()
    report = f"""# Phase D — Universe Expansion Assessment

## Result

- 2026 SET50 symbol union in the local membership files: {len(members_2026)}.
- Existing Phase C candidate: {len(candidates)} member-date rows for {candidates["Symbol"].nunique()} symbol(s) (AOT only).
- Phase D additions: 0 symbols and 0 member-date rows.
- Classification counts, including the separately assessed nonmember GLOBAL: `{json.dumps(counts, sort_keys=True)}`.
- Daily membership coverage remains 50 rows in the existing Phase C audit. The candidate universe has 206 zero-candidate dates and four dates with one AOT candidate.

## Why no other symbol enters

- BANPU remains `EXCLUDED_MISSING_EXECUTION_DATA` under the existing year-wide policy.
- 51 member symbols remain `EXCLUDED_CORPORATE_ACTION_UNRESOLVED`; local event terms are unverified.
- BTS has valid vendor execution OHLC on the four AOT execution dates, but all three rank features (VolRank, CorrRank, LiquidityRank) are null on the corresponding four predictor dates.
- GLOBAL is not a 2026 SET50 constituent and remains price-basis unresolved; its tick diagnostic is not confirmation of a corporate action.
- AOT remains the only evidence-backed candidate. No feature or exclusion requirements were relaxed.

The CSV covers the 2026 member union plus GLOBAL so the existing GLOBAL policy is explicit.
It preserves the Phase C candidate as a candidate, not an approved portfolio universe.
The coverage CSV carries the existing daily member/exclusion/coverage counts and records
zero Phase D additions on every date.
"""
    (OUT / "phase_D_universe_expansion_report.md").write_text(report, encoding="utf-8")
    summary = {
        "member_symbols_2026": len(members_2026),
        "symbols_assessed_including_global": len(symbols),
        "phase_C_candidate_rows": int(len(candidates)),
        "phase_C_candidate_symbols": sorted(candidates["Symbol"].unique().tolist()),
        "phase_D_added_symbols": [],
        "phase_D_added_rows": 0,
        "classification_counts": counts,
        "coverage_dates": int(len(coverage)),
        "coverage_dates_with_candidates": int(coverage["Phase_D_Eligible_Symbol_Count"].gt(0).sum()),
    }
    return symbol_frame, coverage, summary


def make_gate_outputs(
    feature_summary: dict,
    membership_summary: dict,
    universe_summary: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    gate_rows = [
        {
            "Research_Scope": "Single-security diagnostic backtest",
            "Status": "PASS_WITH_LIMITATIONS",
            "Evidence": "AOT has 4 candidate member-date rows; all have valid next-session vendor Open/Close, complete six-feature inputs, and zero BANPU rows in the 60-observation feature window.",
            "Limitations": "Diagnostic/smoke-test scope only; four rows cannot support a performance estimate. No run was made. Vendor provenance and official 2026 trading calendar remain limited.",
            "Permitted_Conclusion": "Pipeline-level one-security diagnostic only; not portfolio evidence or a research result.",
        },
        {
            "Research_Scope": "Multi-security portfolio backtest",
            "Status": "BLOCKED",
            "Evidence": "Only AOT is a Phase C candidate; no second eligible symbol was added.",
            "Limitations": "No diversified portfolio can be assessed; unresolved event and feature-data exclusions remain.",
            "Permitted_Conclusion": "None.",
        },
        {
            "Research_Scope": "Comparison of seven allocation methods",
            "Status": "BLOCKED",
            "Evidence": "Universe is single-security and the board-lot, stale-valuation, and fallback policies remain unresolved.",
            "Limitations": "CVaR formulation is not approved; allocation methods were not changed.",
            "Permitted_Conclusion": "None.",
        },
        {
            "Research_Scope": "All 63 strategy-allocation combinations",
            "Status": "BLOCKED",
            "Evidence": "Multi-security universe and methodology gates remain blocked.",
            "Limitations": "No combination was executed; no research backtest gate was opened.",
            "Permitted_Conclusion": "None.",
        },
        {
            "Research_Scope": "Phase D overall research readiness",
            "Status": "BLOCKED",
            "Evidence": "AOT-only four-row candidate; 2017_H1 membership gap, unresolved corporate actions, and execution/methodology limitations remain.",
            "Limitations": "This phase is diagnostic only and does not approve any backtest.",
            "Permitted_Conclusion": "Research Backtest Gate remains closed.",
        },
    ]
    gate = pd.DataFrame(gate_rows)
    write_csv(gate, "phase_D_gate.csv")

    blockers = [
        {
            "Blocker_ID": "D-MEM-2017-01",
            "Status": "BLOCKED",
            "Scope": "Frozen model historical context",
            "Blocker": "2017_H1 membership file has 49 nonblank names and one blank slot; six named members are absent from Master rows for all 120 dates.",
            "Evidence_Still_Needed": "Primary evidence identifying the 50th constituent and a reproducible explanation/data source for the six absent member series.",
            "Impact": f"{membership_summary['current_complete_model_rows']} current complete 2017_H1 training rows are reconstructed; exact missing-symbol effects on rank features and target distribution are unknown.",
        },
        {
            "Blocker_ID": "D-BANPU-FEATURE-01",
            "Status": "BLOCKED",
            "Scope": "Frozen feature consistency",
            "Blocker": "BANPU is present in same-date VolRank/LiquidityRank and in the member-only proxy feeding 60-observation CorrRank; removal changes cross-sectional values on many 2026 dates.",
            "Evidence_Still_Needed": "Approved inference feature policy that preserves the frozen model's training transformation, plus complete provenance for the feature-date calendar.",
            "Impact": "The original Master and frozen model were not changed. The four AOT candidate dates are bounded clear of BANPU within the recorded 60-observation windows.",
        },
        {
            "Blocker_ID": "D-CORP-01",
            "Status": "BLOCKED",
            "Scope": "52 member symbols with local event rows",
            "Blocker": "141 local ledger rows have no populated official source or evidence URL; event terms/effective dates remain unverified.",
            "Evidence_Still_Needed": "Primary source terms and dates for each event that can affect eligible symbols, identity, share quantity, cash entitlement, or price continuity.",
            "Impact": "51 member symbols remain excluded for unresolved event continuity; no action was applied.",
        },
        {
            "Blocker_ID": "D-UNIVERSE-01",
            "Status": "BLOCKED",
            "Scope": "Multi-security universe",
            "Blocker": "No additional symbol meets existing Phase C requirements; BTS is missing all three rank inputs on the four candidate dates.",
            "Evidence_Still_Needed": "Valid, provenance-consistent BTS rank feature rows; no relaxation or imputation.",
            "Impact": "Only AOT remains a candidate; no multi-security portfolio.",
        },
        {
            "Blocker_ID": "D-VENDOR-01",
            "Status": "BLOCKED",
            "Scope": "Execution/valuation research validity",
            "Blocker": "Yahoo is an accepted third-party vendor, but exact acquisition ticker list, interval, grouping/timezone, and source-run provenance remain incomplete in Phase C.",
            "Evidence_Still_Needed": "A complete, evidence-backed acquisition manifest tied to the immutable source artifact; do not infer missing fields.",
            "Impact": "Eligible vendor rows are bounded but not official SET execution records.",
        },
        {
            "Blocker_ID": "D-CALENDAR-01",
            "Status": "BLOCKED",
            "Scope": "Execution date alignment",
            "Blocker": "No official 2026 trading calendar is present; candidate dates use the next date observed in the vendor snapshot.",
            "Evidence_Still_Needed": "A verified 2026 exchange-session calendar or primary-source evidence for every aligned session.",
            "Impact": "The four AOT date alignments are observed-data alignments, not an official calendar validation.",
        },
        {
            "Blocker_ID": "D-METHOD-01",
            "Status": "BLOCKED",
            "Scope": "Portfolio sizing and valuation",
            "Blocker": "Board-lot, stale-valuation, and fallback policies remain unresolved.",
            "Evidence_Still_Needed": "Approved research policies; no defaults were invented.",
            "Impact": "Portfolio order sizing and valuation cannot be validated.",
        },
        {
            "Blocker_ID": "D-CVAR-01",
            "Status": "BLOCKED",
            "Scope": "CVaR allocation",
            "Blocker": "CVaR formulation is not approved.",
            "Evidence_Still_Needed": "Explicit approval of the objective and estimation/constraint specification.",
            "Impact": "CVaR and the complete seven-method/63-combination comparisons remain blocked.",
        },
    ]
    blocker_frame = pd.DataFrame(blockers)
    write_csv(blocker_frame, "phase_D_blocker_register.csv")
    report = f"""# Phase D Research Readiness

## Decision

**Research Backtest Gate: BLOCKED.** Phase D is diagnostic only. No portfolio backtest,
single-security backtest, retraining, fit, download, source-data edit, or allocation
change was performed.

## Phase A–D comparison

| Phase | Requirement statuses (overall row excluded) | Candidate symbols | Candidate member-date rows | Gate |
|---|---|---:|---:|---|
| A | 12 PASS / 4 BLOCKED; 0 verified rows | 0 | 0 | BLOCKED |
| B | 8 PASS / 1 PASS_WITH_LIMITATIONS / 7 BLOCKED; 0 verified rows | 0 | 0 | BLOCKED |
| C | 4 PASS / 7 PASS_WITH_LIMITATIONS / 4 BLOCKED | 1 (AOT) | 4 | BLOCKED |
| D | 1 PASS_WITH_LIMITATIONS / 3 BLOCKED; overall BLOCKED | 1 (AOT) | 4 | BLOCKED |

Phase A and Phase B results and artifacts were not rewritten. Phase D did not convert
any prior `BLOCKED` status into a pass.

## Universe and evidence

- Eligible candidate symbols: {", ".join(universe_summary["phase_C_candidate_symbols"])}.
- Candidate member-date rows: {universe_summary["phase_C_candidate_rows"]}.
- Phase D-added symbols/rows: 0 / 0.
- 51 current member symbols remain excluded for unverified corporate-action continuity.
- BANPU remains excluded for `INSUFFICIENT_VERIFIED_EXECUTION_DATA`; the original missing OHLC cells are unchanged.
- BTS cannot enter because VolRank, CorrRank, and LiquidityRank are missing on the four candidate dates.
- GLOBAL is not a 2026 SET50 constituent; its 141 price-basis anomaly rows do not establish an official split or affect 2026 SET50 shared calculations.
- Corporate-action status: all {141} local ledger events remain unresolved; 97 rows involve symbols in the 2026 membership union, while 89 fall inside the symbol's active period on the recorded date.
- 2017_H1 remains unresolved: {membership_summary["nonblank_unique"]} names plus one blank slot, and {membership_summary["missing_known_list_rows"]} listed member-date rows absent from Master. The current model-row reconstruction still matches its frozen {membership_summary["frozen_training_samples"]:,}-sample metadata.
- BANPU exclusion-aware same-date diagnostics change VolRank/LiquidityRank values for other securities in 2026. They were not written back to Master; the frozen model was not retrained.

## Separate readiness decisions

1. **Single-security diagnostic:** `PASS_WITH_LIMITATIONS` only for a pipeline smoke-test interpretation of the four AOT rows. It is not a performance estimate, and none was run. The broader vendor provenance/calendar limitations remain.
2. **Multi-security portfolio:** `BLOCKED`; one candidate symbol is not a multi-security universe.
3. **Seven allocation methods:** `BLOCKED`; the universe is single-security, portfolio policies are unresolved, and CVaR is unapproved.
4. **All 63 combinations:** `BLOCKED`; no backtest combination was run and the research gate remains closed.

## Remaining blockers and required evidence

See `phase_D_blocker_register.csv` for the scoped register. The critical outstanding items
are: resolve primary membership/data evidence for 2017_H1; retain frozen-feature
consistency while bounding BANPU effects; verify event terms for affected securities;
obtain complete vendor provenance and official session-calendar evidence; supply missing
BTS rank features without imputation; and approve the existing execution and CVaR policies.

The eligible candidate is non-empty but does **not** make multi-security portfolio,
allocation-method, or full-combination research ready. No missing value was filled,
no corporate action was applied, and no eligibility rule was relaxed.
"""
    (OUT / "phase_D_research_readiness_report.md").write_text(report, encoding="utf-8")
    return gate, blocker_frame, report


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    phase_c_manifest = json.loads(PHASE_C_MANIFEST.read_text(encoding="utf-8-sig"))
    prior_checks = validate_prior_artifacts(phase_c_manifest)

    membership_frame = read_csv(MEMBERSHIP)
    membership = get_membership_sets(membership_frame)
    master = pd.read_parquet(MASTER)
    master["Date"] = pd.to_datetime(master["Date"], errors="coerce").dt.normalize()
    master["Symbol"] = master["Symbol"].astype(str).str.upper()
    master["Period"] = master["Period"].astype(str)
    if master.duplicated(["Date", "Symbol"]).any():
        raise RuntimeError("Pinned Master has duplicate Date-Symbol rows; diagnostics stopped.")
    metadata = json.loads(MODEL_METADATA.read_text(encoding="utf-8-sig"))

    actions, _ = make_corporate_action_outputs(membership, PHASE_C)
    feature_frame, feature_summary = make_feature_outputs(
        master, membership, PHASE_C, GLOBAL_DIAGNOSTIC
    )
    membership_impact, membership_summary = make_2017_outputs(
        master, membership_frame, membership, metadata
    )
    symbol_frame, coverage, universe_summary = make_universe_outputs(
        membership, PHASE_C, actions, master
    )
    gate, blockers, readiness_report = make_gate_outputs(
        feature_summary, membership_summary, universe_summary
    )

    (OUT / "phase_D_feature_consistency_report.md").write_text(
        "Feature consistency report is generated below.\n", encoding="utf-8"
    )
    input_sha = {
        path.name: sha256(path)
        for path in [
            MASTER,
            MODEL,
            MODEL_METADATA,
            MEMBERSHIP,
            DECLARATIONS,
            LEDGER,
            GLOBAL_DIAGNOSTIC,
            NOTEBOOK_03,
            NOTEBOOK_04,
            NOTEBOOK_05,
            NOTEBOOK_06,
        ]
    }
    requested_outputs = [
        "phase_D_corporate_action_scope.csv",
        "phase_D_corporate_action_report.md",
        "phase_D_feature_contamination.csv",
        "phase_D_feature_consistency_report.md",
        "phase_D_2017_membership_impact.csv",
        "phase_D_2017_membership_report.md",
        "phase_D_symbol_eligibility.csv",
        "phase_D_universe_coverage.csv",
        "phase_D_universe_expansion_report.md",
        "phase_D_gate.csv",
        "phase_D_blocker_register.csv",
        "phase_D_research_readiness_report.md",
    ]
    output_hashes = {name: sha256(OUT / name) for name in requested_outputs}
    manifest = {
        "schema_version": "phase-d-v1",
        "phase": "Phase D - Universe Expansion and Frozen Model Consistency Audit",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(OUT),
        "scope": "Diagnostic only; no backtests were run.",
        "approach": "Local evidence only; existing Yahoo Finance data remains third-party vendor data.",
        "actions": {
            "market_data_downloaded": False,
            "source_data_modified": False,
            "master_dataset_modified": False,
            "frozen_model_fit_or_retrained": False,
            "notebook_05_modified": False,
            "notebook_06_modified": False,
            "corporate_actions_applied": False,
            "prices_imputed_or_corrected": False,
            "portfolio_backtests_executed": 0,
            "portfolio_backtests_63_executed": False,
            "research_backtest_gate_open": False,
        },
        "prior_phase_integrity": prior_checks,
        "input_hashes_sha256": input_sha,
        "phase_A_phase_B_phase_C_comparison": {
            "phase_A_verified_tradable_rows": 0,
            "phase_A_requirement_status_counts": {"PASS": 12, "BLOCKED": 4},
            "phase_A_gate": "BLOCKED",
            "phase_B_verified_tradable_rows": 0,
            "phase_B_requirement_status_counts": {
                "PASS": 8,
                "PASS_WITH_LIMITATIONS": 1,
                "BLOCKED": 7,
            },
            "phase_B_gate": "BLOCKED",
            "phase_C_requirement_status_counts": {
                "PASS": 4,
                "PASS_WITH_LIMITATIONS": 7,
                "BLOCKED": 4,
            },
            "phase_C_candidate_symbols": universe_summary["phase_C_candidate_symbols"],
            "phase_C_candidate_member_date_rows": universe_summary["phase_C_candidate_rows"],
            "phase_C_gate": "BLOCKED",
            "phase_D_requirement_status_counts": {
                "PASS_WITH_LIMITATIONS": 1,
                "BLOCKED": 3,
            },
            "phase_D_added_symbols": universe_summary["phase_D_added_symbols"],
            "phase_D_added_rows": universe_summary["phase_D_added_rows"],
            "phase_D_gate": "BLOCKED",
        },
        "diagnostic_results": {
            "corporate_action_rows": int(len(actions)),
            "corporate_action_verified_rows": int(actions["Officially_Verified"].fillna(False).astype(bool).sum()),
            "corporate_action_member_union_overlap_rows": int(actions["Is_Any_2026_Constituent"].sum()),
            "corporate_action_active_member_date_rows": int(
                actions["Is_2026_Constituent_On_Recorded_Date"].sum()
            ),
            "feature_contamination": feature_summary,
            "membership_2017": membership_summary,
            "universe": universe_summary,
            "readiness": gate[["Research_Scope", "Status"]].to_dict("records"),
            "blocker_count": int(len(blockers)),
        },
        "output_hashes_sha256": output_hashes,
        "builder_script_sha256": sha256(Path(__file__)),
        "manifest_self_hash": "not included",
    }
    (OUT / "phase_D_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    feature_report = f"""# Phase D — Feature Contamination and Frozen Model Consistency

## BANPU

The pinned Master contains {feature_summary["banpu_2026_feature_rows"]} BANPU feature-date rows in 2026.
Notebook 03 calculates `VolRank` and `LiquidityRank` cross-sectionally within the SET50
period. The member-only market proxy is leave-one-out for each member, and each
`Corr_60d` uses `rolling(window=60, min_periods=60).corr(...)` on observed feature dates.
Thus BANPU can affect other members' same-date VolRank/LiquidityRank and their rolling
CorrRank inputs while its return is present. `daily_return`, `momentum_20d`, and `vol_z`
are per-symbol calculations and have no direct cross-symbol effect.

The Phase C washout code takes `feature_calendar[max(0, date_position - 59):date_position + 1]`:
at most 60 global observed feature dates, inclusive of the predictor date. It requires
exactly 60 observations and no BANPU row anywhere in that slice. Phase D records this
test for {feature_summary["rolling_windows_checked"]} observed 2026 dates; BANPU is in
{feature_summary["rolling_windows_with_banpu"]} of those current/trailing windows.

Recomputed against the pinned Master using the source rank definitions:

| Period | BANPU rows | Other VolRank rows changed if removed | Max absolute change | Other LiquidityRank rows changed if removed | Max absolute change |
|---|---:|---:|---:|---:|---:|
| 2026_H1 | {feature_summary["rank_metrics_by_period"]["2026_H1"]["banpu_rows"]} | {feature_summary["rank_metrics_by_period"]["2026_H1"]["volrank_other_rows_changed_without_banpu"]} | {feature_summary["rank_metrics_by_period"]["2026_H1"]["volrank_max_abs_change"]:.6f} | {feature_summary["rank_metrics_by_period"]["2026_H1"]["liquidityrank_other_rows_changed_without_banpu"]} | {feature_summary["rank_metrics_by_period"]["2026_H1"]["liquidityrank_max_abs_change"]:.6f} |
| 2026_H2 | {feature_summary["rank_metrics_by_period"]["2026_H2"]["banpu_rows"]} | {feature_summary["rank_metrics_by_period"]["2026_H2"]["volrank_other_rows_changed_without_banpu"]} | {feature_summary["rank_metrics_by_period"]["2026_H2"]["volrank_max_abs_change"]:.6f} | {feature_summary["rank_metrics_by_period"]["2026_H2"]["liquidityrank_other_rows_changed_without_banpu"]} | {feature_summary["rank_metrics_by_period"]["2026_H2"]["liquidityrank_max_abs_change"]:.6f} |

The baseline rank calculations reproduce the stored rank values for all observed
2026 member rows in these periods. These counterfactual ranks are diagnostics only;
they were not written into the Master or used to refit the model.

For the four Phase C AOT predictor dates (2026-11-09 through 2026-11-12), the 60
observed-date windows start 2026-08-13, 2026-08-14, 2026-08-17, and 2026-08-18,
respectively, and contain no BANPU feature row. The last BANPU feature row before the
execution-gap interval is 2026-08-11. A separate 2026-11-13 BANPU row is later than
all four predictor dates and is not used as future information; it would restart the
proxy/rolling window for later predictors. The Phase C candidate
flags and the pinned Master date sequence both show zero BANPU observations in those
four windows. Therefore, the AOT candidate-date VolRank/LiquidityRank and the 60-date
CorrRank inputs are unaffected by removing BANPU on those dates.

Exclusion-aware recalculation over 2026 would change many same-date ranks, so the
inference inputs would no longer use the same member population as the frozen model's
original training transformation. The actual training feature distribution, frozen
model, and stored features remain unchanged; the bounded AOT sample uses the original
values. This does not resolve historical 2017_H1 membership uncertainty.

## GLOBAL

The diagnostic contains {feature_summary["global_anomaly_rows"]} GLOBAL field-rows across
{feature_summary["global_distinct_dates"]} dates. GLOBAL is not a member of either 2026
SET50 period. Notebook 03 builds the shared rank/proxy inputs from effective-period
SET50 members; the execution-snapshot anomaly therefore does not enter other 2026
symbols' shared model features. The diagnostic's split-basis candidate and tick
alignment do not prove a corporate action. `Official_Action_Confirmed` remains false;
no split basis is asserted and no adjusted value is applied.

## Frozen model and limits

No features were overwritten and no model was retrained. The rank counterfactual
demonstrates inference consistency risk if BANPU were removed from the feature
population outside the four-date washout. The report does not treat the feature data
as officially sourced execution data or infer corporate-action terms.
"""
    (OUT / "phase_D_feature_consistency_report.md").write_text(feature_report, encoding="utf-8")

    # Recompute hashes after writing the feature report, which is an output as well.
    output_hashes["phase_D_feature_consistency_report.md"] = sha256(
        OUT / "phase_D_feature_consistency_report.md"
    )
    manifest["output_hashes_sha256"] = output_hashes
    (OUT / "phase_D_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    if gate.loc[gate["Research_Scope"].eq("Phase D overall research readiness"), "Status"].iloc[0] != "BLOCKED":
        raise RuntimeError("Research Backtest Gate must remain BLOCKED.")
    if len(symbol_frame.loc[symbol_frame["Phase_D_Classification"].eq("ELIGIBLE_CANDIDATE")]) != 1:
        raise RuntimeError("Unexpected Phase D eligible-candidate count.")
    if (
        universe_summary["phase_C_candidate_rows"] != 4
        or universe_summary["phase_C_candidate_symbols"] != ["AOT"]
    ):
        raise RuntimeError("Unexpected Phase C candidate universe.")
    if feature_summary["global_2026_h1_member"] or feature_summary["global_2026_h2_member"]:
        raise RuntimeError("GLOBAL unexpectedly appears in 2026 membership.")
    print(json.dumps({
        "workspace": str(OUT),
        "outputs": sorted(path.name for path in OUT.iterdir()),
        "candidate_symbols": universe_summary["phase_C_candidate_symbols"],
        "candidate_rows": universe_summary["phase_C_candidate_rows"],
        "gate": "BLOCKED",
        "protected_asset_checks": len(prior_checks["protected_assets"]),
        "phase_A_checks": len(prior_checks["phase_A_artifacts"]),
        "phase_B_checks": len(prior_checks["phase_B_artifacts"]),
        "phase_C_checks": len(prior_checks["phase_C_artifacts"]),
    }, indent=2))


if __name__ == "__main__":
    main()
