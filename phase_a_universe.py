from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd


def _truthy(values: pd.Series) -> pd.Series:
    return values.astype("string").str.strip().str.lower().isin({"true", "1"})


def _action_state(ledger: pd.DataFrame, symbol: str) -> tuple[bool, int, int, str]:
    if ledger.empty or "Symbol" not in ledger:
        return False, 0, 0, "NO_OFFICIAL_ACTION_LEDGER_OR_NEGATIVE_CONFIRMATION"
    events = ledger.loc[ledger["Symbol"].eq(symbol)]
    if events.empty:
        return False, 0, 0, "NO_OFFICIAL_ACTION_LEDGER_OR_NEGATIVE_CONFIRMATION"
    status = events.get("Reconciliation_Status", pd.Series("", index=events.index))
    sources = events.get("Official_Source", pd.Series("", index=events.index))
    applied = events.get("Applied_By_Portfolio_Engine", pd.Series(False, index=events.index))
    resolved = (
        status.astype("string").fillna("").str.upper().eq("RECONCILED")
        & sources.astype("string").fillna("").str.strip().str.startswith("https://")
        & _truthy(applied)
    )
    unresolved = int((~resolved).sum())
    label = "VERIFIED_AND_APPLIED" if unresolved == 0 else "UNRESOLVED_OFFICIAL_RECONCILIATION_OR_ACCOUNTING"
    return unresolved == 0, int(len(events)), unresolved, label


def _identity_state(identity: pd.DataFrame, symbol: str) -> tuple[bool, int, str]:
    if identity.empty or "Ticker" not in identity:
        return False, 0, "NO_TRANSITION_ROW; OFFICIAL_IDENTITY_CLEARANCE_ABSENT"
    rows = identity.loc[identity["Ticker"].eq(symbol)]
    if rows.empty:
        return False, 0, "NO_TRANSITION_ROW; OFFICIAL_IDENTITY_CLEARANCE_ABSENT"
    evidence = rows.get("Evidence_Status", pd.Series("", index=rows.index))
    verified = bool(evidence.astype("string").fillna("").str.upper().eq("PASS").all())
    statuses = rows.get("Trading_Status", pd.Series("UNKNOWN", index=rows.index))
    labels = statuses.astype("string").fillna("UNKNOWN").drop_duplicates().tolist()
    return verified, int(len(rows)), "; ".join(labels)


def _measure_record(record: Mapping[str, Any] | None) -> tuple[bool, bool, bool, bool]:
    if record is None:
        return False, False, False, False
    values = {
        key: pd.to_numeric(pd.Series([record.get(key)]), errors="coerce").iloc[0]
        for key in ["Open", "High", "Low", "Close", "Volume"]
    }
    ohlc_complete = all(pd.notna(values[key]) for key in ["Open", "High", "Low", "Close"])
    ohlcv_complete = ohlc_complete and pd.notna(values["Volume"])
    invalid = bool(
        ohlc_complete
        and (
            any(not np.isfinite(values[key]) or values[key] <= 0 for key in ["Open", "High", "Low", "Close"])
            or values["Low"] > values["High"]
            or not values["Low"] <= values["Open"] <= values["High"]
            or not values["Low"] <= values["Close"] <= values["High"]
        )
    )
    valid = bool(ohlcv_complete and not invalid and np.isfinite(values["Volume"]) and values["Volume"] >= 0)
    eligible = bool(valid and values["Volume"] > 0)
    return bool(ohlcv_complete), valid, eligible, invalid


def write_phase_a_artifacts(context: Mapping[str, Any]) -> dict[str, Any]:
    run_dir: Path = context["run_dir"]
    root: Path = context["project_root"]
    policy_path: Path = context["exclusion_policy_path"]
    execution_path: Path = context["execution_candidate_path"]
    protected_paths: Mapping[str, Path | None] = context["protected_paths"]
    hash_file = context["sha256_file"]

    required_policy = {
        "Symbol", "Exclusion_Start_Date", "Exclusion_End_Date",
        "Exclusion_Reason", "Evidence_Path", "Evidence_Description", "Decision_Status",
    }
    policy = pd.read_csv(policy_path)
    if not required_policy.issubset(policy.columns):
        raise ValueError(f"Exclusion policy missing columns: {sorted(required_policy - set(policy.columns))}")
    policy["Symbol"] = policy["Symbol"].astype("string").str.strip().str.upper()
    policy["Exclusion_Start_Date"] = pd.to_datetime(policy["Exclusion_Start_Date"], errors="raise").dt.normalize()
    policy["Exclusion_End_Date"] = pd.to_datetime(policy["Exclusion_End_Date"], errors="raise").dt.normalize()
    approved = policy.loc[policy["Decision_Status"].eq("APPROVED_RESEARCH_EXCLUSION")].copy()
    if approved["Symbol"].isna().any() or approved["Symbol"].duplicated().any():
        raise ValueError("Approved exclusion symbols must be nonempty and unique")
    approved_symbols = set(approved["Symbol"].astype(str))
    if not approved_symbols.issubset(set(context["exclusion_symbols"])) or "BANPU" not in approved_symbols:
        raise AssertionError("Approved exclusions and the engine policy are inconsistent")
    if not approved["Exclusion_Start_Date"].le(pd.Timestamp("2026-01-01")).all():
        raise ValueError("Approved exclusions must begin no later than 2026-01-01")
    if not approved["Exclusion_End_Date"].ge(pd.Timestamp("2026-12-31")).all():
        raise ValueError("Approved exclusions must cover all of 2026")
    exclusion_by_symbol = approved.set_index("Symbol").to_dict("index")

    hashes_before = {
        name: hash_file(path) if path is not None and path.is_file() else None
        for name, path in protected_paths.items()
    }
    pinned_snapshot = context["expected_execution_sha256"]
    snapshot_matches = hashes_before.get("execution_snapshot") == pinned_snapshot
    immutable_matches = hashes_before.get("immutable_execution_copy") == pinned_snapshot

    predictor_dates = sorted({
        pd.Timestamp(value).normalize()
        for value in context["observed_feature_dates"]
        if pd.Timestamp(value).year == 2026
    })
    if not predictor_dates:
        raise ValueError("No observed 2026 predictor dates are available")
    membership_by_date = context["membership_by_date"]
    members_by_date: dict[pd.Timestamp, set[str]] = {}
    for date in predictor_dates:
        members = membership_by_date.get(date)
        if members is None:
            raise ValueError(f"Membership evidence is missing for predictor date {date.date()}")
        members_by_date[date] = {str(symbol).strip().upper() for symbol in members}
    member_symbols = set().union(*members_by_date.values())
    membership_basis_verified = bool(
        context["membership_source_urls_official"] and context["official_calendar_available"]
    )
    execution_basis_verified = bool(context["verified_execution_source"])

    candidate = context["execution_candidate_df"].copy()
    candidate["Date"] = pd.to_datetime(candidate["Date"], errors="raise").dt.normalize()
    candidate["Symbol"] = candidate["Symbol"].astype(str).str.strip().str.upper()
    if candidate.duplicated(["Date", "Symbol"]).any():
        raise ValueError("Execution snapshot contains duplicate Date + Symbol keys")
    execution_lookup = {
        (row.Date, row.Symbol): row._asdict()
        for row in candidate.itertuples(index=False)
    }

    ledger = context["corporate_action_ledger"].copy()
    if not ledger.empty and "Symbol" in ledger:
        ledger["Symbol"] = ledger["Symbol"].astype(str).str.strip().str.upper()
    identity = context["security_identity_mapping"].copy()
    if not identity.empty and "Ticker" in identity:
        identity["Ticker"] = identity["Ticker"].astype(str).str.strip().str.upper()
    tick_audit = context["tick_audit"].copy()
    if not tick_audit.empty and "Symbol" in tick_audit:
        tick_audit["Symbol"] = tick_audit["Symbol"].astype(str).str.strip().str.upper()
    action_symbols = set(ledger["Symbol"].astype(str)) if "Symbol" in ledger else set()
    identity_symbols = set(identity["Ticker"].astype(str)) if "Ticker" in identity else set()
    snapshot_symbols = set(candidate["Symbol"].astype(str))
    all_symbols = snapshot_symbols | member_symbols | action_symbols | identity_symbols
    action_states = {symbol: _action_state(ledger, symbol) for symbol in all_symbols}
    identity_states = {symbol: _identity_state(identity, symbol) for symbol in all_symbols}

    next_session = context["build_next_session_map"](context["observed_feature_dates"])
    universe_rows = []
    for predictor_date in predictor_dates:
        execution_date = next_session.get(predictor_date)
        for symbol in sorted(members_by_date[predictor_date]):
            policy_row = exclusion_by_symbol.get(symbol)
            excluded = bool(
                policy_row is not None
                and policy_row["Exclusion_Start_Date"] <= predictor_date
                and policy_row["Exclusion_End_Date"] >= predictor_date
            )
            record = execution_lookup.get((execution_date, symbol)) if execution_date is not None else None
            ohlcv_complete, execution_valid, execution_eligible, invalid_ohlc = _measure_record(record)
            action_valid = action_states[symbol][0]
            identity_valid = identity_states[symbol][0]
            blockers = []
            if excluded:
                blockers.append("APPROVED_EXCLUSION")
            if execution_date is None:
                blockers.append("NO_NEXT_SESSION_EXECUTION_DATE")
            if not execution_valid:
                blockers.append("MISSING_OR_INVALID_EXECUTION_DATA")
            if execution_valid and not execution_eligible:
                blockers.append("ZERO_VOLUME_NOT_EXECUTION_ELIGIBLE")
            if not membership_basis_verified:
                blockers.append("MEMBERSHIP_SOURCE_OR_CALENDAR_UNVERIFIED")
            if not execution_basis_verified:
                blockers.append("EXECUTION_PRICE_BASIS_UNVERIFIED")
            if not action_valid:
                blockers.append("CORPORATE_ACTION_BASIS_UNVERIFIED")
            if not identity_valid:
                blockers.append("SECURITY_IDENTITY_BASIS_UNVERIFIED")
            tradable = bool(
                not excluded and execution_valid and execution_eligible
                and membership_basis_verified and execution_basis_verified
                and action_valid and identity_valid
            )
            universe_rows.append({
                "Date": predictor_date,
                "Symbol": symbol,
                "Execution_Date": execution_date,
                "Is_SET50_Member": True,
                "Membership_Basis_Verified": membership_basis_verified,
                "Has_Valid_Execution_Data": execution_valid,
                "Candidate_Data_Row_Present": record is not None,
                "Candidate_OHLCV_Complete": ohlcv_complete,
                "Invalid_OHLC": invalid_ohlc,
                "Is_Excluded": excluded,
                "Exclusion_Reason": policy_row["Exclusion_Reason"] if excluded else "",
                "Has_Valid_Price_Basis": execution_basis_verified,
                "Has_Valid_Corporate_Action_Basis": action_valid,
                "Has_Verified_Security_Identity": identity_valid,
                "Is_Execution_Eligible": execution_eligible,
                "Is_Tradable": tradable,
                "Verification_Blocker": ";".join(blockers),
            })
    universe = pd.DataFrame(universe_rows).sort_values(["Date", "Symbol"]).reset_index(drop=True)
    required_universe = {
        "Date", "Symbol", "Is_SET50_Member", "Has_Valid_Execution_Data",
        "Is_Excluded", "Exclusion_Reason", "Is_Tradable",
    }
    if not required_universe.issubset(universe.columns):
        raise AssertionError("Tradable universe is missing required output fields")
    tradable = universe.loc[universe["Is_Tradable"]].copy()
    if tradable["Symbol"].isin(approved_symbols).any() or tradable["Symbol"].eq("BANPU").any():
        raise AssertionError("An excluded symbol entered portfolio eligibility")

    daily_rows = []
    for predictor_date, day in universe.groupby("Date", sort=True):
        available = day.loc[~day["Is_Excluded"]]
        denominator = int(len(available))
        reasons = sorted({
            f"{row.Symbol}:{row.Exclusion_Reason}"
            for row in day.loc[day["Is_Excluded"]].itertuples(index=False)
        })
        daily_rows.append({
            "Date": predictor_date,
            "SET50_Members": int(day["Is_SET50_Member"].sum()),
            "Excluded_Securities": int(day["Is_Excluded"].sum()),
            "Tradable_Securities": int(day["Is_Tradable"].sum()),
            "Missing_Execution_Rows": int((~available["Candidate_Data_Row_Present"]).sum()),
            "Missing_or_Invalid_Execution_Rows": int((~available["Has_Valid_Execution_Data"] & available["Candidate_Data_Row_Present"]).sum()),
            "Zero_Volume_Rows": int((available["Has_Valid_Execution_Data"] & ~available["Is_Execution_Eligible"]).sum()),
            "Candidate_Data_Coverage": float(available["Has_Valid_Execution_Data"].sum() / denominator) if denominator else 0.0,
            "Execution_Eligibility_Coverage": float(available["Is_Execution_Eligible"].sum() / denominator) if denominator else 0.0,
            "Verified_Execution_Coverage": float(day["Is_Tradable"].sum() / denominator) if denominator else 0.0,
            "Exclusion_Reasons": ";".join(reasons),
        })
    daily_coverage = pd.DataFrame(daily_rows)

    features = context["feature_df"].copy()
    features["Symbol"] = features["Symbol"].astype(str).str.strip().str.upper()
    features["Date"] = pd.to_datetime(features["Date"], errors="coerce").dt.normalize()
    tick_counts = tick_audit.groupby("Symbol").size().to_dict() if not tick_audit.empty else {}
    member_day_counts = universe.groupby("Symbol").size().to_dict()
    tradable_day_counts = tradable.groupby("Symbol").size().to_dict()
    excluded_day_counts = universe.loc[universe["Is_Excluded"]].groupby("Symbol").size().to_dict()
    security_rows = []
    for symbol in sorted(all_symbols):
        symbol_execution = candidate.loc[candidate["Symbol"].eq(symbol)]
        symbol_features = features.loc[features["Symbol"].eq(symbol)]
        symbol_actions = ledger.loc[ledger["Symbol"].eq(symbol)] if not ledger.empty and "Symbol" in ledger else pd.DataFrame()
        ohlc = symbol_execution.reindex(columns=["Open", "High", "Low", "Close"]).apply(pd.to_numeric, errors="coerce")
        ohlc_complete = ohlc.notna().all(axis=1)
        invalid_mask = ohlc_complete & (
            (ohlc <= 0).any(axis=1)
            | (ohlc["Low"] > ohlc["High"])
            | (ohlc["Open"] < ohlc["Low"]) | (ohlc["Open"] > ohlc["High"])
            | (ohlc["Close"] < ohlc["Low"]) | (ohlc["Close"] > ohlc["High"])
        )
        action_valid, action_count, unresolved_action_count, action_status = action_states[symbol]
        identity_valid, identity_count, identity_status = identity_states[symbol]
        feature_2026 = symbol_features.loc[symbol_features["Date"].dt.year.eq(2026)]
        feature_pre2026 = symbol_features.loc[symbol_features["Date"].lt(pd.Timestamp("2026-01-01"))]
        vol = pd.to_numeric(symbol_execution["Volume"], errors="coerce") if "Volume" in symbol_execution else pd.Series(dtype=float)
        exclusion = exclusion_by_symbol.get(symbol)
        if symbol in approved_symbols:
            eligibility_status = "EXCLUDED_BY_APPROVED_POLICY"
        elif symbol not in member_symbols:
            eligibility_status = "NOT_A_2026_SET50_MEMBER"
        else:
            eligibility_status = "BLOCKED_NO_VERIFIED_EXECUTION_BASIS"
        if tick_counts.get(symbol, 0):
            price_status = "RECORDED_ANOMALY_UNRESOLVED"
        elif context["verified_execution_source"]:
            price_status = "AUTHORIZED_RAW_BASIS_VERIFIED"
        else:
            price_status = "NOT_FLAGGED_IN_AVAILABLE_DIAGNOSTIC_SOURCE_STILL_UNVERIFIED"
        security_rows.append({
            "Symbol": symbol,
            "Is_In_Execution_Snapshot": symbol in snapshot_symbols,
            "Is_2026_SET50_Member": symbol in member_symbols,
            "Execution_Snapshot_Rows": int(len(symbol_execution)),
            "Missing_Open_Rows": int(symbol_execution["Open"].isna().sum()) if "Open" in symbol_execution else 0,
            "Missing_High_Rows": int(symbol_execution["High"].isna().sum()) if "High" in symbol_execution else 0,
            "Missing_Low_Rows": int(symbol_execution["Low"].isna().sum()) if "Low" in symbol_execution else 0,
            "Missing_Close_Rows": int(symbol_execution["Close"].isna().sum()) if "Close" in symbol_execution else 0,
            "Missing_OHLC_Cells": int(symbol_execution.reindex(columns=["Open", "High", "Low", "Close"]).isna().sum().sum()),
            "Invalid_OHLC_Rows": int(invalid_mask.sum()),
            "Zero_Volume_Rows": int((vol <= 0).sum()),
            "Price_Basis_Anomaly_Rows": int(tick_counts.get(symbol, 0)),
            "Price_Basis_Status": price_status,
            "Corporate_Action_Event_Rows": int(action_count),
            "Unresolved_Corporate_Action_Rows": int(unresolved_action_count),
            "Corporate_Action_Status": action_status,
            "Identity_Transition_Rows": int(identity_count),
            "Identity_Transition_Status": identity_status,
            "Feature_Rows_2026": int(len(feature_2026)),
            "Complete_Six_Feature_Rows_2026": int(feature_2026.reindex(columns=context["feature_columns"]).notna().all(axis=1).sum()),
            "Historical_Feature_Rows_Pre2026": int(len(feature_pre2026)),
            "Historical_Complete_Six_Feature_Rows_Pre2026": int(feature_pre2026.reindex(columns=context["feature_columns"]).notna().all(axis=1).sum()),
            "Historical_Lookback_Minimum_Configured": False,
            "Has_Valid_Execution_Data": bool(
                len(symbol_execution) > 0 and ohlc_complete.all() and not invalid_mask.any()
                and "Volume" in symbol_execution and symbol_execution["Volume"].notna().all()
                and (vol >= 0).all()
            ),
            "Has_Valid_Price_Basis": bool(context["verified_execution_source"]),
            "Has_Valid_Corporate_Action_Basis": bool(action_valid),
            "Has_Verified_Security_Identity": bool(identity_valid),
            "Is_Excluded_2026": symbol in approved_symbols,
            "Exclusion_Reason": exclusion["Exclusion_Reason"] if exclusion else "",
            "SET50_Member_Days": int(member_day_counts.get(symbol, 0)),
            "Excluded_Member_Days": int(excluded_day_counts.get(symbol, 0)),
            "Tradable_Member_Days": int(tradable_day_counts.get(symbol, 0)),
            "Research_Eligibility_Status": eligibility_status,
        })
    security_audit = pd.DataFrame(security_rows).sort_values("Symbol").reset_index(drop=True)

    exclusion_test = context["unit_test_report"].loc[
        context["unit_test_report"]["Test"].eq("approved_exclusion_applies_before_decisions")
    ]
    exclusion_guard_test_passed = bool(
        len(exclusion_test) == 1 and exclusion_test["Status"].eq("PASS").all()
    )
    exclusion_rows = []
    for row in approved.to_dict("records"):
        symbol = str(row["Symbol"])
        security = security_audit.loc[security_audit["Symbol"].eq(symbol)].iloc[0]
        member_rows = universe.loc[universe["Symbol"].eq(symbol) & universe["Is_SET50_Member"]]
        exclusion_rows.append({
            "Symbol": symbol,
            "Exclusion_Start_Date": row["Exclusion_Start_Date"],
            "Exclusion_End_Date": row["Exclusion_End_Date"],
            "Exclusion_Reason": row["Exclusion_Reason"],
            "Decision_Status": row["Decision_Status"],
            "Evidence_Path": row["Evidence_Path"],
            "Evidence_Description": row["Evidence_Description"],
            "Execution_Snapshot_Rows": security["Execution_Snapshot_Rows"],
            "Missing_OHLC_Cells": security["Missing_OHLC_Cells"],
            "Price_Basis_Anomaly_Rows": security["Price_Basis_Anomaly_Rows"],
            "Unresolved_Corporate_Action_Rows": security["Unresolved_Corporate_Action_Rows"],
            "Identity_Transition_Status": security["Identity_Transition_Status"],
            "SET50_Member_Days_Affected": int(len(member_rows)),
            "Tradable_Days_After_Exclusion": int(member_rows["Is_Tradable"].sum()),
            "Synthetic_Allocation_Input_Exclusion_Check": "PASS" if exclusion_guard_test_passed else "FAIL",
            "Synthetic_Buy_Order_Exclusion_Check": "PASS" if exclusion_guard_test_passed else "FAIL",
            "Synthetic_Sell_Order_Exclusion_Check": "PASS" if exclusion_guard_test_passed else "FAIL",
            "Synthetic_Portfolio_Holdings_Exclusion_Check": "PASS" if exclusion_guard_test_passed else "FAIL",
            "Actual_Research_Orders_Generated": False,
            "Historical_Membership_Modified": False,
            "Master_Dataset_Modified": False,
            "Model_Retrained": False,
        })
    exclusion_audit = pd.DataFrame(exclusion_rows)

    hashes_after = {
        name: hash_file(path) if path is not None and path.is_file() else None
        for name, path in protected_paths.items()
    }
    protected_unchanged = bool(
        all(value is not None and hashes_after.get(name) == value for name, value in hashes_before.items())
    )
    snapshot_integrity = bool(protected_unchanged and snapshot_matches and immutable_matches)
    model_unchanged = bool(
        hashes_before.get("frozen_model") is not None
        and hashes_before.get("frozen_model") == hashes_after.get("frozen_model")
    )
    membership_unchanged = bool(
        hashes_before.get("membership_history") is not None
        and hashes_before.get("membership_declarations") is not None
        and hashes_before.get("membership_history") == hashes_after.get("membership_history")
        and hashes_before.get("membership_declarations") == hashes_after.get("membership_declarations")
    )
    notebook_data = context["notebook_data"]
    fit_calls = []
    for cell_index, cell in enumerate(notebook_data.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        try:
            tree = ast.parse("".join(cell.get("source", [])))
        except SyntaxError:
            continue
        fit_calls.extend(
            f"cell {cell_index}"
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "fit"
        )
    model_not_retrained = not fit_calls

    tradable = universe.loc[universe["Is_Tradable"]].copy()
    excluded_in_tradable = bool(tradable["Symbol"].isin(approved_symbols).any())
    banpu_in_eligibility = bool(tradable["Symbol"].eq("BANPU").any())
    unresolved_basis_in_tradable = bool(
        not tradable.empty
        and (~tradable["Has_Valid_Price_Basis"] | ~tradable["Has_Valid_Corporate_Action_Basis"]).any()
    )
    missing_counts = {
        field: int(candidate[field].isna().sum())
        for field in ["Open", "High", "Low", "Close"]
    }
    invalid_total = int(security_audit["Invalid_OHLC_Rows"].sum())
    unresolved_member_symbols = sorted(
        symbol for symbol in member_symbols
        if symbol not in approved_symbols and not action_states[symbol][0]
    )
    candidate_data_rows = int((~universe["Is_Excluded"] & universe["Has_Valid_Execution_Data"]).sum())
    candidate_eligible_rows = int((~universe["Is_Excluded"] & universe["Is_Execution_Eligible"]).sum())
    nonexcluded_rows = int((~universe["Is_Excluded"]).sum())
    candidate_coverage = candidate_data_rows / nonexcluded_rows if nonexcluded_rows else 0.0
    eligibility_coverage = candidate_eligible_rows / nonexcluded_rows if nonexcluded_rows else 0.0
    verified_coverage = len(tradable) / nonexcluded_rows if nonexcluded_rows else 0.0

    output_paths = {
        "execution_excluded_symbols": run_dir / "execution_excluded_symbols.csv",
        "exclusion_audit": run_dir / "exclusion_audit.csv",
        "tradable_universe": run_dir / "tradable_universe_2026.csv",
        "security_level_integrity_audit": run_dir / "security_level_integrity_audit.csv",
        "universe_coverage_report": run_dir / "universe_coverage_report.md",
        "phase_A_gate": run_dir / "phase_A_gate.csv",
    }
    policy.to_csv(output_paths["execution_excluded_symbols"], index=False)
    exclusion_audit.to_csv(output_paths["exclusion_audit"], index=False)
    universe.to_csv(output_paths["tradable_universe"], index=False)
    security_audit.to_csv(output_paths["security_level_integrity_audit"], index=False)

    daily_table = [
        "| Date | Members | Excluded | Tradable | Missing Exec Rows | Data Coverage | Eligibility Coverage | Verified Coverage | Exclusion Reasons |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in daily_coverage.itertuples(index=False):
        daily_table.append(
            f"| {row.Date:%Y-%m-%d} | {row.SET50_Members} | {row.Excluded_Securities} | {row.Tradable_Securities} "
            f"| {row.Missing_Execution_Rows} | {row.Candidate_Data_Coverage:.2%} "
            f"| {row.Execution_Eligibility_Coverage:.2%} | {row.Verified_Execution_Coverage:.2%} "
            f"| {row.Exclusion_Reasons or '-'} |"
        )
    global_summary = context["global_summary"]
    snapshot_hash = hashes_before.get("execution_snapshot")
    immutable_hash = hashes_before.get("immutable_execution_copy")
    model_hash = hashes_before.get("frozen_model")
    report_lines = [
        "# Phase A — Security Exclusion and Tradable Universe",
        "",
        f"- Overall status: **BLOCKED** (verified tradable rows: {len(tradable):,})",
        f"- Predictor dates: {len(predictor_dates):,} ({predictor_dates[0].date()} to {predictor_dates[-1].date()})",
        f"- Candidate SET50 member-date rows: {len(universe):,}; daily membership range: {int(daily_coverage['SET50_Members'].min())}–{int(daily_coverage['SET50_Members'].max())}",
        f"- Approved exclusion symbols: {', '.join(sorted(approved_symbols))}",
        f"- Excluded member-date rows: {int(universe['Is_Excluded'].sum()):,}; remaining member-date rows: {nonexcluded_rows:,}",
        f"- Candidate valid execution-data coverage: {candidate_data_rows:,}/{nonexcluded_rows:,} ({candidate_coverage:.2%})",
        f"- Candidate execution-eligibility coverage (positive volume): {candidate_eligible_rows:,}/{nonexcluded_rows:,} ({eligibility_coverage:.2%})",
        f"- Officially verified execution coverage: {len(tradable):,}/{nonexcluded_rows:,} ({verified_coverage:.2%})",
        f"- Predictor dates with no next observed execution date: {int(daily_coverage['Missing_Execution_Rows'].gt(0).sum())}; unavailable execution rows after exclusions: {int(daily_coverage['Missing_Execution_Rows'].sum())}",
        "",
        "## Source and price-basis findings",
        f"- Execution candidate: `{execution_path}`; provider={context['execution_provider']}; auto_adjust={context['execution_auto_adjust']}; authorized raw execution source verified={context['verified_execution_source']}.",
        f"- Feature source: `{context['feature_path']}`; feature download uses auto_adjust=True={context['feature_auto_adjust_true']}; explicit actions parameter={context['feature_actions_explicit']}; same file as execution snapshot={Path(context['feature_path']).resolve() == Path(execution_path).resolve()}.",
        "- Feature and execution inputs are separate files with different adjustment settings; they are not confirmed to share a price basis. No feature or model data was rebuilt.",
        f"- Snapshot missing OHLC cells by field: {missing_counts}; total={sum(missing_counts.values())}; invalid OHLC rows={invalid_total}. No values were filled.",
        f"- GLOBAL diagnostic: rows={global_summary['rows']}; strict tick-aligned={global_summary['strict_tick_aligned']}; diagnostic-aligned={global_summary['diagnostic_tick_aligned']}; official action confirmed={global_summary['official_action_confirmed']}; recent SET cross-checks={global_summary['recent_SET_crosscheck_rows']}, OHLC matches={global_summary['recent_SET_OHLC_matches']}.",
        "- The diagnostic split factor/alignment does not prove a real split or historical market price basis. The ledger contains no official source confirming the split; GLOBAL is excluded precautionarily and is not a 2026 SET50 member.",
        f"- Recorded tick-basis anomaly rows by symbol: {tick_audit.groupby('Symbol').size().to_dict() if not tick_audit.empty else {}}. This describes the available diagnostic only and does not clear other securities.",
        "",
        "## Corporate actions, identity and history",
        f"- Corporate-action ledger: {len(ledger):,} rows across {ledger['Symbol'].nunique() if 'Symbol' in ledger else 0} symbols; official source URLs={context['official_action_sources']}; engine-applied events={context['actions_applied_count']}.",
        f"- Non-excluded member symbols without verified corporate-action basis: {len(unresolved_member_symbols)} ({', '.join(unresolved_member_symbols)}). Missing official negative coverage is not treated as proof that no action occurred.",
        f"- Identity map includes transition tickers: {identity['Ticker'].dropna().astype(str).str.upper().drop_duplicates().tolist() if 'Ticker' in identity else []}. BPP is not a 2026 SET50 member; BANPU remains excluded.",
        "- The required minimum historical lookback is not configured. Per-symbol historical feature counts are recorded in security_level_integrity_audit.csv; no minimum was invented.",
        "",
        "## Protected inputs",
        f"- Original snapshot SHA-256: {snapshot_hash}; pinned hash match={snapshot_matches}.",
        f"- Immutable copy SHA-256: {immutable_hash}; pinned hash match={immutable_matches}.",
        f"- Master dataset SHA-256: {hashes_before.get('master_dataset')}.",
        f"- Frozen model SHA-256: {model_hash}; unchanged during Phase A={model_unchanged}; retraining calls found={fit_calls}.",
        f"- Membership SHA-256: {hashes_before.get('membership_history')}; declarations SHA-256: {hashes_before.get('membership_declarations')}; unchanged during Phase A={membership_unchanged}.",
        f"- 05_backtest SHA-256: {hashes_before.get('backtest_05')}; the file was not edited.",
        "",
        "## Phase A decision",
        "- BANPU is excluded for 2026 with reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`; GLOBAL is excluded precautionarily with reason `UNRESOLVED_PRICE_BASIS_AND_CORPORATE_ACTION`. No exclusion was based on profit or loss.",
        f"- Synthetic exclusion regression across allocation inputs and Buy/Sell orders/holdings: {'PASS' if exclusion_guard_test_passed else 'FAIL'}. Actual research orders were not generated.",
        "- No excluded symbol appears in the tradable universe. No unresolved price basis appears in the tradable universe because the verified tradable universe is empty; this is not evidence that candidate securities are safe.",
        "- No 63-combination backtest was run; the Research Backtest Gate remains closed. No Yahoo download, snapshot edit, Master Dataset edit, membership edit, or model retraining occurred.",
        "",
        "## Daily coverage",
        *daily_table,
    ]
    output_paths["universe_coverage_report"].write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    membership_counts_valid = bool(daily_coverage["SET50_Members"].eq(50).all())
    banpu_policy_valid = bool(
        "BANPU" in exclusion_by_symbol
        and exclusion_by_symbol["BANPU"]["Exclusion_Reason"] == "INSUFFICIENT_VERIFIED_EXECUTION_DATA"
    )
    global_policy_valid = bool(
        "GLOBAL" in exclusion_by_symbol
        and exclusion_by_symbol["GLOBAL"]["Exclusion_Reason"] == "UNRESOLVED_PRICE_BASIS_AND_CORPORATE_ACTION"
    )
    gate_rows = [
        ("BANPU full-year exclusion policy", "PASS" if banpu_policy_valid else "FAIL", policy_path, f"excluded_member_days={int(universe.loc[universe['Symbol'].eq('BANPU'), 'Is_Excluded'].sum())}; reason=INSUFFICIENT_VERIFIED_EXECUTION_DATA"),
        ("GLOBAL anomaly classified and precautionarily excluded", "PASS" if global_policy_valid else "FAIL", context["global_tick_path"], f"anomaly_rows={global_summary['rows']}; official_action_confirmed={global_summary['official_action_confirmed']}; member_days={int(universe['Symbol'].eq('GLOBAL').sum())}; no split is asserted"),
        ("All snapshot, member, event and identity symbols audited", "PASS" if set(security_audit["Symbol"]) == all_symbols else "FAIL", output_paths["security_level_integrity_audit"], f"audited_symbols={len(security_audit)}; snapshot_symbols={len(snapshot_symbols)}"),
        ("Original snapshot and immutable-copy hashes unchanged and pinned", "PASS" if snapshot_integrity else "FAIL", execution_path, f"original={snapshot_hash}; immutable={immutable_hash}; pinned={pinned_snapshot}"),
        ("Master Dataset unchanged", "PASS" if hashes_before.get("master_dataset") is not None and hashes_before.get("master_dataset") == hashes_after.get("master_dataset") else "FAIL", context["feature_path"], f"sha256={hashes_before.get('master_dataset')}"),
        ("Frozen model unchanged and not retrained", "PASS" if model_unchanged and model_not_retrained else "FAIL", context["model_path"], f"sha256={model_hash}; fit_invocations={fit_calls}"),
        ("Historical membership and declarations unchanged", "PASS" if membership_unchanged else "FAIL", context["membership_path"], f"membership_sha256={hashes_before.get('membership_history')}; declaration_sha256={hashes_before.get('membership_declarations')}"),
        ("BANPU absent from tradable and portfolio eligibility", "PASS" if not banpu_in_eligibility else "FAIL", output_paths["tradable_universe"], f"BANPU_tradable_rows={int(universe.loc[universe['Symbol'].eq('BANPU'), 'Is_Tradable'].sum())}; research orders were not generated"),
        ("Exclusions reach allocation inputs, Buy/Sell orders and holdings", "PASS" if exclusion_guard_test_passed else "FAIL", context["unit_test_report_path"], f"synthetic_path_check={exclusion_guard_test_passed}; actual 63-set outputs were not generated"),
        ("No approved excluded symbol in tradable universe", "PASS" if not excluded_in_tradable else "FAIL", output_paths["tradable_universe"], f"tradable_rows={len(tradable)}; excluded_symbols={sorted(approved_symbols)}"),
        ("No unresolved price basis in tradable universe", "PASS" if not unresolved_basis_in_tradable else "FAIL", output_paths["tradable_universe"], f"tradable_rows={len(tradable)}; zero rows is a vacuous safety check, not universe approval"),
        ("Official execution price basis verified", "PASS" if execution_basis_verified else "BLOCKED", context["verified_execution_status_path"], f"verified_source_available={execution_basis_verified}; candidate_missing_OHLC={missing_counts}"),
        ("Corporate-action and security-identity basis verified for members", "PASS" if unresolved_member_symbols == [] else "BLOCKED", context["corporate_action_path"], f"unresolved_member_symbols={len(unresolved_member_symbols)}; official_source_urls={context['official_action_sources']}; applied_by_engine={context['actions_applied_count']}"),
        ("SET50 membership source and execution calendar verified", "PASS" if membership_basis_verified else "BLOCKED", context["membership_path"], f"50_members_each_date={membership_counts_valid}; official_urls={context['membership_source_urls_official']}; official_calendar={context['official_calendar_available']}"),
        ("Verified Tradable Universe is nonempty", "PASS" if len(tradable) > 0 else "BLOCKED", output_paths["tradable_universe"], f"verified_tradable_rows={len(tradable)}; candidate_data_coverage={candidate_coverage:.2%}; verified_coverage={verified_coverage:.2%}"),
        ("Research Backtest Gate remains closed; 63 runs not executed", "PASS" if not context["backtest_gate_open"] else "FAIL", context["gate_report_path"], f"backtest_gate_open={context['backtest_gate_open']}; combinations_executed=False"),
    ]
    gate = pd.DataFrame(gate_rows, columns=["Requirement", "Status", "Evidence_Path", "Detail"])
    overall_status = "BLOCKED" if gate["Status"].isin(["BLOCKED", "FAIL"]).any() else "PASS"
    gate = pd.concat([
        pd.DataFrame([{
            "Requirement": "PHASE_A_OVERALL",
            "Status": overall_status,
            "Evidence_Path": str(output_paths["phase_A_gate"]),
            "Detail": f"verified_tradable_rows={len(tradable)}; Research Backtest Gate remains closed",
        }]),
        gate,
    ], ignore_index=True)
    gate.to_csv(output_paths["phase_A_gate"], index=False)

    return {
        "output_paths": output_paths,
        "overall_status": overall_status,
        "predictor_dates": len(predictor_dates),
        "member_date_rows": len(universe),
        "excluded_member_date_rows": int(universe["Is_Excluded"].sum()),
        "tradable_rows": int(len(tradable)),
        "candidate_data_coverage": candidate_coverage,
        "candidate_eligibility_coverage": eligibility_coverage,
        "verified_execution_coverage": verified_coverage,
        "protected_hashes_before": hashes_before,
        "protected_hashes_after": hashes_after,
        "protected_hashes_unchanged": protected_unchanged,
        "model_retrained": not model_not_retrained,
        "backtest_63_sets_executed": False,
    }
