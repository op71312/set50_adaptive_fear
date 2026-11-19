from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\Project_Github\set_fear_index")
BACKTEST = ROOT / "backtest_results"
DATASET = ROOT / "dataset"
BUILD = DATASET / "verified_build_20261113_152948"
OUT = BACKTEST / "phase_C_vendor_validation_20261116"
SOURCES = OUT / "sources"
PHASE_A = BACKTEST / "research_audit_20261116T044415991651Z_ee2aa7e1"
PHASE_B = BACKTEST / "phase_B_evidence_recovery_20261116T1147"

SNAPSHOT = BUILD / "SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.parquet"
SIDECAR = BUILD / "SET50_Execution_OHLCV_2026_Yahoo_auto_adjust_false_snapshot.json"
MASTER = BUILD / "SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet"
IMMUTABLE_COPY = BACKTEST / "execution_data_v2" / "execution_ohlcv_original.parquet"
MODEL = ROOT / "models" / "Original_Softmax_Final" / "final_softmax_model.joblib"
MODEL_METADATA = ROOT / "models" / "Original_Softmax_Final" / "final_softmax_metadata.json"
MEMBERSHIP = DATASET / "SET50_constituents_by_halfyear_2016_2026.csv"
DECLARATIONS = DATASET / "set50_declare_dates_2016_2026.csv"
LEDGER = BACKTEST / "corporate_action_ledger_official.csv"
VENDOR_EVENTS = BACKTEST / "corporate_action_vendor_events.csv"
IDENTITY_MAP = BACKTEST / "security_identity_mapping.csv"
EXCLUSION_POLICY = BACKTEST / "research_controls" / "execution_excluded_symbols.csv"
GLOBAL_DIAGNOSTIC = BACKTEST / "global_tick_basis_diagnostic.csv"
LINEAGE = BACKTEST / "execution_data_lineage.json"
NOTEBOOK_01 = ROOT / "01_dataset.ipynb"
NOTEBOOK_03 = ROOT / "03_feature_engineering.ipynb"
NOTEBOOK_05 = ROOT / "05_backtest.ipynb"
NOTEBOOK_06 = ROOT / "06_research_backtest.ipynb"
NOTEBOOK_TEST_RESULTS = OUT / "notebook_06_synthetic_regression_results.csv"
PHASE_A_GATE = PHASE_A / "phase_A_gate.csv"
PHASE_B_GATE = PHASE_B / "phase_B_gate.csv"
PHASE_B_MANIFEST = PHASE_B / "phase_B_manifest.json"
H1_PDF = SOURCES / "SET50_100_H1_2026.pdf"
H2_PDF = SOURCES / "SET50-SET100-H2-2026.pdf"
H1_TEXT = SOURCES / "SET50_100_H1_2026.txt"
H2_TEXT = SOURCES / "SET50-SET100-H2-2026.txt"

FEATURE_COLUMNS = [
    "daily_return",
    "momentum_20d",
    "vol_z",
    "VolRank",
    "CorrRank",
    "LiquidityRank",
]
OHLC = ["Open", "High", "Low", "Close"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def required_file(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def write_csv(name: str, frame: pd.DataFrame) -> Path:
    path = OUT / name
    frame.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def member_names(membership: pd.DataFrame, period: str) -> list[str]:
    rows = membership.loc[membership["period"].astype(str).eq(period)]
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one local membership row for {period}; got {len(rows)}")
    columns = [name for name in membership.columns if name.startswith("symbol_")]
    values = [
        str(value).strip().upper()
        for value in rows.iloc[0][columns].tolist()
        if pd.notna(value) and str(value).strip()
    ]
    return values


def parse_official_constituents(text_path: Path) -> list[str]:
    symbols: list[str] = []
    in_constituents = True
    for line in text_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().lower() in {"inclusion", "exclusion"}:
            in_constituents = False
        if not in_constituents:
            continue
        match = re.match(r"\s*(\d{1,2})\s+([A-Z0-9]+)\s+", line)
        if match and int(match.group(1)) == len(symbols) + 1:
            symbols.append(match.group(2).upper())
    if len(symbols) != 50 or len(set(symbols)) != 50:
        raise ValueError(f"Could not verify 50 unique constituents in {text_path}: {len(symbols)}")
    return symbols


def cell_source(notebook: dict, index: int) -> str:
    return "".join(notebook["cells"][index].get("source", []))


def output_text(cell: dict) -> str:
    chunks = []
    for output in cell.get("outputs", []):
        data = output.get("text", [])
        chunks.extend(data if isinstance(data, list) else [str(data)])
    return "".join(chunks)


def bool_value(value: object) -> bool:
    return bool(pd.notna(value) and value)


OUT.mkdir(parents=True, exist_ok=True)
for path in [
    SNAPSHOT,
    SIDECAR,
    MASTER,
    IMMUTABLE_COPY,
    MODEL,
    MODEL_METADATA,
    MEMBERSHIP,
    DECLARATIONS,
    LEDGER,
    VENDOR_EVENTS,
    IDENTITY_MAP,
    EXCLUSION_POLICY,
    GLOBAL_DIAGNOSTIC,
    LINEAGE,
    NOTEBOOK_01,
    NOTEBOOK_03,
    NOTEBOOK_05,
    NOTEBOOK_06,
    NOTEBOOK_TEST_RESULTS,
    PHASE_A_GATE,
    PHASE_B_GATE,
    PHASE_B_MANIFEST,
    H1_PDF,
    H2_PDF,
    H1_TEXT,
    H2_TEXT,
]:
    required_file(path)

phase_b_manifest = json.loads(PHASE_B_MANIFEST.read_text(encoding="utf-8"))
phase_b_pins = phase_b_manifest["protected_hashes_after"]
protected_paths = {
    "original_execution_snapshot": SNAPSHOT,
    "immutable_execution_copy": IMMUTABLE_COPY,
    "master_dataset": MASTER,
    "frozen_model": MODEL,
    "historical_membership": MEMBERSHIP,
    "membership_declarations": DECLARATIONS,
    "backtest_05_notebook": NOTEBOOK_05,
    "corporate_action_ledger": LEDGER,
    "execution_lineage": LINEAGE,
    "execution_sidecar": SIDECAR,
    "vendor_event_inventory": VENDOR_EVENTS,
    "security_identity_mapping": IDENTITY_MAP,
    "approved_exclusion_policy": EXCLUSION_POLICY,
    "phase_a_universe": PHASE_A / "tradable_universe_2026.csv",
    "phase_a_gate": PHASE_A_GATE,
}
protected_before = {name: sha256(required_file(path)) for name, path in protected_paths.items()}
protected_pin_checks = {
    name: {
        "pinned_sha256": phase_b_pins.get(name),
        "current_sha256": protected_before[name],
        "matches_phase_B": protected_before[name] == phase_b_pins.get(name),
    }
    for name in protected_paths
}
if not all(check["matches_phase_B"] for check in protected_pin_checks.values()):
    raise AssertionError("A protected input differs from Phase B's recorded post-run hash.")

phase_b_output_checks = {}
for name, expected_hash in phase_b_manifest.get("output_hashes", {}).items():
    path = PHASE_B / name
    phase_b_output_checks[name] = {
        "exists": path.is_file(),
        "expected_sha256": expected_hash,
        "current_sha256": sha256(path) if path.is_file() else None,
        "unchanged": path.is_file() and sha256(path) == expected_hash,
    }
if not all(row["unchanged"] for row in phase_b_output_checks.values()):
    raise AssertionError("A Phase B evidence artifact changed during Phase C.")

phase_a_artifact_names = {
    "unit_test_report.csv",
    "source_inventory.csv",
    "feature_impact_audit.csv",
    "gate_evidence.csv",
    "execution_excluded_symbols.csv",
    "exclusion_audit.csv",
    "tradable_universe_2026.csv",
    "security_level_integrity_audit.csv",
    "universe_coverage_report.md",
    "phase_A_gate.csv",
    "run_manifest.json",
}
phase_a_output_checks = {}
for name in phase_a_artifact_names:
    expected_hash = phase_b_pins.get(f"phase_a_artifact:{name}")
    path = PHASE_A / name
    phase_a_output_checks[name] = {
        "exists": path.is_file(),
        "expected_sha256": expected_hash,
        "current_sha256": sha256(path) if path.is_file() else None,
        "unchanged": path.is_file() and sha256(path) == expected_hash,
    }
if not all(row["unchanged"] for row in phase_a_output_checks.values()):
    raise AssertionError("A Phase A evidence artifact changed during Phase C.")

snapshot_hash = sha256(SNAPSHOT)
immutable_hash = sha256(IMMUTABLE_COPY)
master_hash = sha256(MASTER)
model_hash = sha256(MODEL)
membership_hash = sha256(MEMBERSHIP)
declaration_hash = sha256(DECLARATIONS)
notebook_05_hash = sha256(NOTEBOOK_05)
notebook_06_hash = sha256(NOTEBOOK_06)

sidecar = json.loads(SIDECAR.read_text(encoding="utf-8"))
lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
model_metadata = json.loads(MODEL_METADATA.read_text(encoding="utf-8"))
snapshot = pd.read_parquet(SNAPSHOT)
master = pd.read_parquet(MASTER)
ledger = pd.read_csv(LEDGER)
vendor_events = pd.read_csv(VENDOR_EVENTS)
identity_map = pd.read_csv(IDENTITY_MAP)
membership = pd.read_csv(MEMBERSHIP)
declarations = pd.read_csv(DECLARATIONS)
policy = pd.read_csv(EXCLUSION_POLICY)
global_diag = pd.read_csv(GLOBAL_DIAGNOSTIC)
phase_a_gate = pd.read_csv(PHASE_A_GATE)
phase_b_gate = pd.read_csv(PHASE_B_GATE)

snapshot["Date"] = pd.to_datetime(snapshot["Date"], errors="raise").dt.normalize()
snapshot["Symbol"] = snapshot["Symbol"].astype("string").str.strip().str.upper()
master["Date"] = pd.to_datetime(master["Date"], errors="raise").dt.normalize()
master["Symbol"] = master["Symbol"].astype("string").str.strip().str.upper()
ledger["Symbol"] = ledger["Symbol"].astype("string").str.strip().str.upper()
vendor_events["Symbol"] = vendor_events["Symbol"].astype("string").str.strip().str.upper()
identity_map["Ticker"] = identity_map["Ticker"].astype("string").str.strip().str.upper()

if snapshot.duplicated(["Date", "Symbol"]).any():
    raise AssertionError("Duplicate execution Date + Symbol keys found.")
if master.duplicated(["Date", "Symbol"]).any():
    raise AssertionError("Duplicate Master Dataset Date + Symbol keys found.")

local_h1 = member_names(membership, "2026_H1")
local_h2 = member_names(membership, "2026_H2")
official_h1 = parse_official_constituents(H1_TEXT)
official_h2 = parse_official_constituents(H2_TEXT)
if set(local_h1) != set(official_h1) or set(local_h2) != set(official_h2):
    raise AssertionError("The cited 2026 SET PDFs do not match the local 2026 membership lists.")
members_by_period = {"2026_H1": set(official_h1), "2026_H2": set(official_h2)}
members_2026 = set(official_h1) | set(official_h2)

declaration_by_period = {
    f"{int(row.year)}_{str(row.review_period).strip().upper()}": row
    for row in declarations.itertuples(index=False)
}
effective_h1 = pd.Timestamp(declaration_by_period["2026_H1"].effective_date)
effective_h2 = pd.Timestamp(declaration_by_period["2026_H2"].effective_date)
if effective_h1 != pd.Timestamp("2026-01-01") or effective_h2 != pd.Timestamp("2026-07-01"):
    raise AssertionError("Unexpected 2026 membership effective dates in the local declaration file.")

execution_dates = sorted(snapshot["Date"].drop_duplicates().tolist())
feature_dates = sorted(master.loc[master["Date"].dt.year.eq(2026), "Date"].drop_duplicates().tolist())
predictor_dates = sorted(set(execution_dates) & set(feature_dates))
next_session = {execution_dates[i]: execution_dates[i + 1] for i in range(len(execution_dates) - 1)}

snapshot_ohlc = snapshot[OHLC].apply(pd.to_numeric, errors="coerce")
snapshot["OHLC_Complete"] = snapshot_ohlc.notna().all(axis=1)
snapshot["OHLC_Positive_Finite"] = (
    np.isfinite(snapshot_ohlc.to_numpy(dtype=float)).all(axis=1)
    & snapshot_ohlc.gt(0).all(axis=1)
)
snapshot["OHLC_Boundaries_Valid"] = (
    snapshot["OHLC_Complete"]
    & (snapshot["High"] >= snapshot[["Open", "Close", "Low"]].max(axis=1))
    & (snapshot["Low"] <= snapshot[["Open", "Close"]].min(axis=1))
)
snapshot["Valid_OHLC"] = (
    snapshot["OHLC_Complete"]
    & snapshot["OHLC_Positive_Finite"]
    & snapshot["OHLC_Boundaries_Valid"]
)
volume = pd.to_numeric(snapshot["Volume"], errors="coerce")
snapshot["Volume_Missing"] = volume.isna()
snapshot["Volume_Zero"] = volume.eq(0)
snapshot["Volume_Negative"] = volume.lt(0)
snapshot["Volume_Positive"] = volume.gt(0)
snapshot["Valid_Execution_Data"] = snapshot["Valid_OHLC"] & snapshot["Volume_Positive"]
snapshot = snapshot.sort_values(["Symbol", "Date"]).reset_index(drop=True)
previous_close = snapshot.groupby("Symbol", sort=False)["Close"].shift()
snapshot["Repeated_Close_From_Previous_Observed_Row"] = (
    snapshot["Close"].notna()
    & previous_close.notna()
    & snapshot["Close"].eq(previous_close)
)
snapshot["Dividends"] = pd.to_numeric(snapshot.get("Dividends", 0), errors="coerce").fillna(0)
snapshot["Stock Splits"] = pd.to_numeric(snapshot.get("Stock Splits", 0), errors="coerce").fillna(0)

global_diag["Date"] = pd.to_datetime(global_diag["Date"], errors="coerce").dt.normalize()
global_diag["Symbol"] = global_diag["Symbol"].astype("string").str.strip().str.upper()
global_anomaly_groups = (
    global_diag.groupby(["Date", "Symbol"], dropna=False)
    .agg(
        Price_Basis_Anomaly_Rows=("Column", "size"),
        Price_Basis_Anomaly_Fields=("Column", lambda values: ";".join(sorted(set(map(str, values))))),
    )
    .reset_index()
)
global_anomaly_lookup = {
    (row.Date, str(row.Symbol)): row._asdict()
    for row in global_anomaly_groups.itertuples(index=False)
}

quality = snapshot[
    [
        "Date",
        "Symbol",
        *OHLC,
        "Adj Close",
        "Volume",
        "Dividends",
        "Stock Splits",
        "OHLC_Complete",
        "OHLC_Positive_Finite",
        "OHLC_Boundaries_Valid",
        "Valid_OHLC",
        "Volume_Missing",
        "Volume_Zero",
        "Volume_Negative",
        "Volume_Positive",
        "Valid_Execution_Data",
        "Repeated_Close_From_Previous_Observed_Row",
    ]
].copy()
quality["Price_Basis_Anomaly_Rows"] = [
    global_anomaly_lookup.get((row.Date, str(row.Symbol)), {}).get("Price_Basis_Anomaly_Rows", 0)
    for row in quality.itertuples(index=False)
]
quality["Price_Basis_Anomaly_Fields"] = [
    global_anomaly_lookup.get((row.Date, str(row.Symbol)), {}).get("Price_Basis_Anomaly_Fields", "")
    for row in quality.itertuples(index=False)
]
quality["Stale_Valuation_Conclusion"] = "NOT_INFERRED_FROM_REPEATED_PRICE_OR_ZERO_VOLUME"
quality["Data_Provider"] = "Yahoo Finance via yfinance; third-party research vendor"
quality["Official_SET_Execution_Data"] = False
write_csv("vendor_execution_quality_2026.csv", quality)

missing_ohlc = snapshot[OHLC].isna()
missing_by_field = {name: int(missing_ohlc[name].sum()) for name in OHLC}
missing_rows = snapshot.loc[missing_ohlc.any(axis=1)].copy()
missing_cells = int(missing_ohlc.sum().sum())
missing_symbols = sorted(missing_rows["Symbol"].dropna().unique().tolist())
missing_start = missing_rows["Date"].min()
missing_end = missing_rows["Date"].max()
if missing_cells != 253 or missing_symbols != ["BANPU"]:
    raise AssertionError("The Phase B missing OHLC inventory changed unexpectedly.")

event_date_columns = ["Date", "Ex_Date", "Effective_Date", "Trading_Date"]
ledger_dates = {
    column: pd.to_datetime(ledger[column], errors="coerce")
    for column in event_date_columns
}
def event_has_2026_date(row_index: int) -> bool:
    return any(
        values.iloc[row_index] is not pd.NaT
        and pd.notna(values.iloc[row_index])
        and values.iloc[row_index].year == 2026
        for values in ledger_dates.values()
    )

event_rows = []
for index, row in ledger.iterrows():
    symbol = str(row.get("Symbol", "")).strip().upper()
    event_type = str(row.get("Event_Type", "")).strip().upper()
    event_dates = [
        values.iloc[index]
        for values in ledger_dates.values()
        if pd.notna(values.iloc[index])
    ]
    candidate_date = event_dates[0] if event_dates else pd.NaT
    official_source = row.get("Official_Source")
    official_verified = bool(pd.notna(official_source) and str(official_source).strip())
    in_current_member_union = symbol in members_2026
    in_2026 = event_has_2026_date(index)
    if not in_current_member_union:
        category = "C_UNRELATED_TO_VERIFIED_2026_MEMBER_UNIVERSE"
        relevance = "No direct eligible-universe membership; event itself remains unverified."
    elif not in_2026:
        category = "B_HISTORICAL_FEATURE_OR_PRICE_CONTINUITY"
        relevance = "Historical event candidate; no primary evidence verifies terms or effect."
    elif official_verified:
        category = "A_VERIFIED_2026_IMPACT"
        relevance = "A source URL is present, but terms still require independent review."
    else:
        category = "D_UNRESOLVED"
        relevance = "Potential 2026 member impact; no official source or applied terms."
    event_rows.append(
        {
            **row.to_dict(),
            "Source_Publisher": (
                "Yahoo Finance via yfinance.download"
                if str(row.get("Event_ID", "")).startswith("VENDOR-")
                else "UNRECORDED_USER_CLAIM"
            ),
            "Evidence_URL": str(official_source) if official_verified else "",
            "Evidence_Source_Type": (
                "THIRD_PARTY_VENDOR_SNAPSHOT"
                if str(row.get("Event_ID", "")).startswith("VENDOR-")
                else "UNVERIFIED_USER_CLAIM"
            ),
            "Local_2026_Membership_Overlap": in_current_member_union,
            "Potentially_Affects_2026_Research_Period": in_2026,
            "Potentially_Affects_Historical_Feature_Continuity": in_2026,
            "Potentially_Affects_Execution_Price_Continuity": in_2026,
            "Potentially_Changes_Share_Quantity": event_type in {
                "MERGER",
                "SPLIT",
                "STOCK_DIVIDEND+CASH_DIVIDEND",
            },
            "Potential_Cash_Entitlement": "DIVIDEND" in event_type,
            "Potentially_Changes_Security_Identity": event_type == "MERGER",
            "Officially_Verified": official_verified,
            "Impact_Category": category,
            "2026_Relevance_Assessment": relevance,
            "Event_Date_Used_For_Scope_Only": candidate_date,
            "Applied_By_Portfolio_Engine": False,
        }
    )
corporate_relevance = pd.DataFrame(event_rows)
write_csv("corporate_action_relevance_2026.csv", corporate_relevance)

identity_tickers = set(identity_map["Ticker"].dropna().astype(str))
ledger_symbol_counts = ledger.groupby("Symbol").size().to_dict()
identity_symbol_counts = identity_map.groupby("Ticker").size().to_dict()
snapshot_symbol_rows = snapshot.groupby("Symbol").size().to_dict()
master_symbol_rows_2026 = master.loc[master["Date"].dt.year.eq(2026)].groupby("Symbol").size().to_dict()
identity_rows = []
identity_scope = sorted(members_2026 | {"GLOBAL", "BPP", "BANPUU"})
for symbol in identity_scope:
    is_member = symbol in members_2026
    snapshot_rows = int(snapshot_symbol_rows.get(symbol, 0))
    feature_rows = int(master_symbol_rows_2026.get(symbol, 0))
    map_rows = int(identity_symbol_counts.get(symbol, 0))
    if not is_member:
        classification = "NOT_APPLICABLE_TO_2026"
        basis = "Not in the official 2026 SET50 constituent lists; included only as identity-claim context."
    elif symbol in identity_tickers:
        classification = "EXCLUDED_IDENTITY_UNRESOLVED"
        basis = "Local identity map contains an unresolved identity/merger claim without a primary source."
    else:
        classification = "VERIFIED_CONTINUOUS_IDENTITY"
        basis = (
            "Stable vendor ticker key is present in the existing execution snapshot and feature Master; "
            "no local identity-transition row was found. This is not official issuer-identifier verification."
        )
    identity_rows.append(
        {
            "Symbol": symbol,
            "Is_2026_SET50_Member": is_member,
            "Is_SET50_H1_2026": symbol in set(official_h1),
            "Is_SET50_H2_2026": symbol in set(official_h2),
            "Identity_Classification": classification,
            "Verification_Basis": basis,
            "Execution_Snapshot_Rows": snapshot_rows,
            "Feature_Master_Rows_2026": feature_rows,
            "Local_Identity_Map_Rows": map_rows,
            "Local_Corporate_Action_Rows": int(ledger_symbol_counts.get(symbol, 0)),
            "Official_Issuer_Identity_Verified": False,
            "Eligible_Identity_Status": (
                "EXCLUDED" if classification == "EXCLUDED_IDENTITY_UNRESOLVED" else "VENDOR_CONTINUITY_ONLY"
            ),
        }
    )
identity_scope_df = pd.DataFrame(identity_rows)
write_csv("security_identity_scope_2026.csv", identity_scope_df)

nb01 = json.loads(NOTEBOOK_01.read_text(encoding="utf-8"))
nb03 = json.loads(NOTEBOOK_03.read_text(encoding="utf-8"))
nb06 = json.loads(NOTEBOOK_06.read_text(encoding="utf-8"))
feature_download_01 = cell_source(nb01, 6)
feature_download_03 = cell_source(nb03, 31)
feature_rank_code = "\n".join(
    cell_source(nb03, index)
    for index in [20, 22, 26]
)
prediction_code = cell_source(nb06, 14)
test_code = cell_source(nb06, 24)
tests_output = output_text(nb06["cells"][24])
pre_inference_filter_present = "apply_approved_exclusions(feature_rows, 'Feature inputs')" in prediction_code
banpu_input_test_present = "test_excluded_symbols_are_removed_before_model_inference" in test_code
test_evidence = pd.read_csv(NOTEBOOK_TEST_RESULTS)
test_pass_count = int(test_evidence["Status"].eq("PASS").sum())
test_fail_count = int(test_evidence["Status"].eq("FAIL").sum())
serialized_test_pass_count = sum(
    "synthetic fixture assertion passed" in line
    for line in tests_output.splitlines()
)
serialized_output_stale = serialized_test_pass_count != test_pass_count
serialized_output_state = (
    "is stale"
    if serialized_output_stale
    else "matches the fresh run result"
)
test_evidence_names = set(test_evidence["Test"].astype(str))
if not pre_inference_filter_present or not banpu_input_test_present or test_pass_count != 18 or test_fail_count:
    raise AssertionError("Notebook 06 pre-inference exclusion regression is not passing.")
if (
    len(test_evidence) != 18
    or test_evidence_names != set(test_code.split("for test_name, test_function in [", 1)[1].split("]:", 1)[0].split("'")[1::2])
    or not test_evidence["Execution_Evidence"].astype(str).str.contains("Live Notebook 06 cell execution").all()
):
    raise AssertionError("Notebook 06 live regression evidence does not match the test source.")

feature_master_2026 = master.loc[master["Date"].dt.year.eq(2026)].copy()
banpu_features = feature_master_2026.loc[feature_master_2026["Symbol"].eq("BANPU")].copy()
banpu_feature_dates = set(banpu_features["Date"].tolist())
banpu_feature_before_gap = [
    date for date in banpu_feature_dates
    if missing_start is not pd.NaT and date < missing_start
]
last_banpu_feature_before_missing = max(banpu_feature_before_gap) if banpu_feature_before_gap else pd.NaT
feature_calendar = sorted(set(feature_dates) & set(execution_dates))

feature_lookup = {
    (row.Date, str(row.Symbol)): row._asdict()
    for row in feature_master_2026.itertuples(index=False)
}
execution = snapshot.set_index(["Date", "Symbol"], drop=False)
action_symbols_2026 = set(
    corporate_relevance.loc[
        corporate_relevance["Local_2026_Membership_Overlap"]
        & corporate_relevance["Potentially_Affects_2026_Research_Period"],
        "Symbol",
    ].astype(str)
)
unresolved_event_symbols = action_symbols_2026 - {"BANPU"}
approved_policy = policy.loc[policy["Decision_Status"].eq("APPROVED_RESEARCH_EXCLUSION")].copy()
approved_policy["Symbol"] = approved_policy["Symbol"].astype(str).str.strip().str.upper()
approved_by_symbol = approved_policy.set_index("Symbol").to_dict("index")
approved_symbols = set(approved_by_symbol)
if approved_by_symbol.get("BANPU", {}).get("Exclusion_Reason") != "INSUFFICIENT_VERIFIED_EXECUTION_DATA":
    raise AssertionError("The approved BANPU exclusion reason changed.")
if approved_by_symbol.get("GLOBAL", {}).get("Exclusion_Reason") != "UNRESOLVED_PRICE_BASIS_AND_CORPORATE_ACTION":
    raise AssertionError("The approved GLOBAL exclusion reason changed.")

global_anomaly_symbols = set(global_diag["Symbol"].dropna().astype(str))
event_by_symbol = {
    symbol: group.copy()
    for symbol, group in corporate_relevance.groupby("Symbol", dropna=False)
}
identity_class = identity_scope_df.set_index("Symbol")["Identity_Classification"].to_dict()
feature_records = {key: value for key, value in feature_lookup.items()}
execution_records = {
    (row.Date, str(row.Symbol)): row._asdict()
    for row in snapshot.itertuples(index=False)
}

universe_rows = []
coverage_rows = []
for predictor_date in predictor_dates:
    period = "2026_H1" if predictor_date < effective_h2 else "2026_H2"
    members = sorted(members_by_period[period])
    execution_date = next_session.get(predictor_date)
    for symbol in members:
        feature_record = feature_records.get((predictor_date, symbol))
        exec_record = execution_records.get((execution_date, symbol)) if execution_date is not None else None
        feature_ok = bool(
            feature_record is not None
            and all(
                pd.notna(feature_record.get(column))
                and np.isfinite(float(feature_record[column]))
                for column in FEATURE_COLUMNS
            )
        )
        exec_open = pd.to_numeric(pd.Series([exec_record.get("Open") if exec_record else np.nan]), errors="coerce").iloc[0]
        exec_close = pd.to_numeric(pd.Series([exec_record.get("Close") if exec_record else np.nan]), errors="coerce").iloc[0]
        exec_volume = pd.to_numeric(pd.Series([exec_record.get("Volume") if exec_record else np.nan]), errors="coerce").iloc[0]
        exec_ohlc_valid = bool(exec_record and exec_record.get("Valid_OHLC", False))
        exec_valid = bool(
            exec_record
            and exec_ohlc_valid
            and pd.notna(exec_open)
            and np.isfinite(float(exec_open))
            and exec_open > 0
            and pd.notna(exec_close)
            and np.isfinite(float(exec_close))
            and exec_close > 0
            and pd.notna(exec_volume)
            and np.isfinite(float(exec_volume))
            and exec_volume > 0
        )
        current_date_has_banpu = predictor_date in banpu_feature_dates
        date_position = feature_calendar.index(predictor_date)
        lookback_dates = feature_calendar[max(0, date_position - 59): date_position + 1]
        banpu_in_rolling_window = any(date in banpu_feature_dates for date in lookback_dates)
        proxy_clear = (
            len(lookback_dates) == 60
            and not current_date_has_banpu
            and not banpu_in_rolling_window
        )
        approved = symbol in approved_symbols
        policy_reason = approved_by_symbol.get(symbol, {}).get("Exclusion_Reason", "")
        unresolved_action = symbol in unresolved_event_symbols
        identity_status = identity_class.get(symbol, "EXCLUDED_IDENTITY_UNRESOLVED")
        identity_ok = identity_status == "VERIFIED_CONTINUOUS_IDENTITY"
        price_anomaly_count = global_anomaly_lookup.get(
            (execution_date, symbol), {}
        ).get("Price_Basis_Anomaly_Rows", 0) if execution_date is not None else 0
        price_basis_ok = int(price_anomaly_count) == 0

        if approved:
            excluded, exclusion_reason, reason_code = True, policy_reason, "APPROVED_SECURITY_EXCLUSION"
        elif unresolved_action:
            excluded = True
            exclusion_reason = "UNRESOLVED_2026_CORPORATE_ACTION"
            reason_code = "UNRESOLVED_CORPORATE_ACTION_CASH_OR_SHARE_CONTINUITY"
        else:
            excluded, exclusion_reason, reason_code = False, "", ""

        if reason_code:
            eligible = False
        elif not proxy_clear:
            eligible = False
            reason_code = "BANPU_SHARED_FEATURE_PROXY_WASHOUT"
            exclusion_reason = (
                "Banpu contributes to precomputed cross-sectional ranks/market proxy within the "
                "current-date/60-observation CorrRank window."
            )
        elif not feature_ok:
            eligible = False
            reason_code = "MISSING_OR_NONFINITE_MODEL_FEATURE"
            exclusion_reason = "One or more frozen model features are absent or non-finite."
        elif not identity_ok:
            eligible = False
            reason_code = "SECURITY_IDENTITY_UNRESOLVED"
            exclusion_reason = "Identity transition is unresolved in the local identity map."
        elif not price_basis_ok:
            eligible = False
            reason_code = "PRICE_BASIS_ANOMALY"
            exclusion_reason = "Execution-date price-basis diagnostic has an unresolved anomaly."
        elif execution_date is None:
            eligible = False
            reason_code = "NO_NEXT_VENDOR_OBSERVED_EXECUTION_DATE"
            exclusion_reason = "No next observed execution date exists in the pinned Yahoo snapshot."
        elif not exec_valid:
            eligible = False
            reason_code = "MISSING_OR_INVALID_EXECUTION_OPEN_CLOSE_VOLUME"
            exclusion_reason = "Next-date Open/Close/OHLC or positive Volume is missing or invalid."
        else:
            eligible = True
            reason_code = "ELIGIBLE_VENDOR_RESEARCH_CANDIDATE"
            exclusion_reason = ""

        universe_rows.append(
            {
                "Date": predictor_date,
                "Symbol": symbol,
                "Is_SET50_Member": True,
                "Has_Valid_Execution_Data": exec_valid,
                "Is_Excluded": excluded,
                "Exclusion_Reason": exclusion_reason,
                "Is_Tradable": eligible,
                "Execution_Date": execution_date,
                "Execution_Open": exec_open,
                "Valuation_Close": exec_close,
                "Execution_Volume": exec_volume,
                "Has_Valid_Feature_Data": feature_ok,
                "Is_Feature_Proxy_Clear": proxy_clear,
                "BANPU_In_Current_Feature_Cross_Section": current_date_has_banpu,
                "BANPU_In_Rolling_60_Date_Feature_Window": banpu_in_rolling_window,
                "Is_Identity_Continuous": identity_ok,
                "Identity_Classification": identity_status,
                "Has_Unresolved_2026_Corporate_Action": unresolved_action,
                "Has_Valid_Vendor_Price_Basis": price_basis_ok,
                "Price_Basis_Anomaly_Rows": int(price_anomaly_count),
                "Is_Next_Observed_Date_Aligned": execution_date is not None,
                "Official_Trading_Calendar_Verified": False,
                "No_Lookahead_Feature_Date_Only": True,
                "Reason_Code": reason_code,
                "Membership_Source": (
                    "SET official H1 2026 PDF" if period == "2026_H1" else "SET official H2 2026 PDF"
                ),
                "Membership_Effective_Period": period,
            }
        )

    daily = [row for row in universe_rows if row["Date"] == predictor_date]
    all_member_missing = 0
    missing_field_cells = 0
    invalid_exec = 0
    for symbol in members:
        if execution_date is None:
            continue
        record = execution_records.get((execution_date, symbol))
        if record is None:
            all_member_missing += 1
            continue
        field_missing = sum(pd.isna(record.get(field)) for field in OHLC)
        missing_field_cells += int(field_missing)
        if not record.get("Valid_Execution_Data", False):
            invalid_exec += 1
    valid_exec_count = sum(bool(row["Has_Valid_Execution_Data"]) for row in daily)
    tradable_count = sum(bool(row["Is_Tradable"]) for row in daily)
    excluded_count = sum(bool(row["Is_Excluded"]) for row in daily)
    reasons = sorted(set(row["Reason_Code"] for row in daily if row["Reason_Code"]))
    denominator = len(members) if execution_date is not None else 0
    coverage_rows.append(
        {
            "Date": predictor_date,
            "Next_Observed_Execution_Date": execution_date,
            "Official_Trading_Session_Verified": False,
            "SET50_Member_Count": len(members),
            "Excluded_Security_Count": excluded_count,
            "Tradable_Security_Count": tradable_count,
            "Missing_Execution_Rows": all_member_missing,
            "Missing_OHLC_Field_Cells": missing_field_cells,
            "Missing_or_Invalid_Execution_Rows": invalid_exec,
            "Candidate_Data_Coverage_Pct": (
                100.0 * valid_exec_count / denominator if denominator else np.nan
            ),
            "Tradable_Coverage_Pct": (
                100.0 * tradable_count / len(members) if members else np.nan
            ),
            "Exclusion_Reasons": ";".join(reasons),
        }
    )

universe = pd.DataFrame(universe_rows).sort_values(["Date", "Symbol"]).reset_index(drop=True)
coverage = pd.DataFrame(coverage_rows).sort_values("Date").reset_index(drop=True)
tradable = universe.loc[universe["Is_Tradable"]].copy()
if tradable["Symbol"].isin(approved_symbols).any() or tradable["Symbol"].eq("BANPU").any():
    raise AssertionError("An approved excluded symbol entered the Phase C candidate universe.")
if tradable["Symbol"].isin(unresolved_event_symbols).any():
    raise AssertionError("An unresolved event-bearing symbol entered the Phase C candidate universe.")
if len(tradable) != 4 or set(tradable["Symbol"]) != {"AOT"}:
    raise AssertionError(f"Unexpected candidate universe: {len(tradable)} rows / {tradable.Symbol.unique()}")
if tradable["Date"].min() != pd.Timestamp("2026-11-09") or tradable["Date"].max() != pd.Timestamp("2026-11-12"):
    raise AssertionError("Unexpected 60-observation Banpu feature washout interval.")
if not tradable["BANPU_In_Rolling_60_Date_Feature_Window"].eq(False).all():
    raise AssertionError("Banpu feature observations remain in an eligible rolling feature window.")
if tradable["Is_Excluded"].any() or not tradable["Is_Tradable"].all():
    raise AssertionError("The tradable universe contains an excluded or non-tradable row.")

write_csv("tradable_universe_2026_phase_C.csv", tradable)
write_csv("tradable_universe_coverage_phase_C.csv", coverage)

event_member_rows = corporate_relevance.loc[
    corporate_relevance["Local_2026_Membership_Overlap"]
    & corporate_relevance["Potentially_Affects_2026_Research_Period"]
]
event_member_symbols = set(event_member_rows["Symbol"].astype(str))
exclusion_rows = []
for symbol in sorted(members_2026 | {"GLOBAL"}):
    if symbol in approved_by_symbol:
        policy_row = approved_by_symbol[symbol]
        reason = str(policy_row["Exclusion_Reason"])
        status = "APPROVED_EXISTING_POLICY"
    elif symbol in event_member_symbols:
        reason = "UNRESOLVED_2026_CORPORATE_ACTION_CASH_OR_SHARE_CONTINUITY"
        status = "PHASE_C_SCOPE_EXCLUSION"
    else:
        continue
    symbol_rows = universe.loc[universe["Symbol"].eq(symbol)]
    event_subset = event_member_rows.loc[event_member_rows["Symbol"].astype(str).eq(symbol)]
    exclusion_rows.append(
        {
            "Symbol": symbol,
            "Exclusion_Start_Date": "2026-01-01",
            "Exclusion_End_Date": "2026-12-31",
            "Exclusion_Reason": reason,
            "Decision_Status": status,
            "SET50_Member_2026": symbol in members_2026,
            "Local_Corporate_Action_Rows_2026": len(event_subset),
            "Corporate_Action_Event_IDs": ";".join(event_subset["Event_ID"].astype(str).tolist()),
            "GLOBAL_Price_Basis_Anomaly_Rows": int(
                global_diag.loc[global_diag["Symbol"].astype(str).eq(symbol)].shape[0]
            ),
            "Missing_OHLC_Field_Cells": int(
                snapshot.loc[snapshot["Symbol"].astype(str).eq(symbol), OHLC].isna().sum().sum()
            ),
            "Eligible_Member_Date_Rows": int(symbol_rows["Is_Tradable"].sum()),
            "Evidence": (
                str(policy_row["Evidence_Description"])
                if symbol in approved_by_symbol
                else "Local 2026 event record has no official source URL; potential cash/share continuity is unverified."
            ),
            "No_PnL_Based_Exclusion": True,
        }
    )
exclusions = pd.DataFrame(exclusion_rows).sort_values("Symbol").reset_index(drop=True)
write_csv("execution_excluded_symbols_phase_C.csv", exclusions)

membership_audit_rows = []
for period, local_values, official_values, pdf, pdf_hash, url in [
    (
        "2026_H1",
        local_h1,
        official_h1,
        H1_PDF,
        sha256(H1_PDF),
        "https://media.set.or.th/set/Documents/2025/Dec/SET50_100_H1_2026.pdf",
    ),
    (
        "2026_H2",
        local_h2,
        official_h2,
        H2_PDF,
        sha256(H2_PDF),
        "https://media.set.or.th/set/Documents/2026/Jun/SET50-SET100-H2-2026.pdf",
    ),
]:
    effective = effective_h1 if period == "2026_H1" else effective_h2
    for symbol in sorted(set(local_values) | set(official_values)):
        membership_audit_rows.append(
            {
                "Period": period,
                "Effective_Date": effective.date().isoformat(),
                "Symbol": symbol,
                "Local_File_Present": symbol in set(local_values),
                "Official_SET_PDF_Present": symbol in set(official_values),
                "Local_Official_Match": (symbol in set(local_values)) == (symbol in set(official_values)),
                "Publisher": "Stock Exchange of Thailand",
                "Source_URL": url,
                "Retrieved_PDF_SHA256": pdf_hash,
                "Evidence_Path": str(pdf),
                "Status": "VERIFIED_FROM_OFFICIAL_SET_PDF",
            }
        )
write_csv("membership_2026_primary_evidence_audit.csv", pd.DataFrame(membership_audit_rows))

row_2017 = membership.loc[membership["period"].astype(str).eq("2017_H1")].iloc[0]
member_columns = [name for name in membership.columns if name.startswith("symbol_")]
raw_2017 = [row_2017[column] for column in member_columns]
names_2017 = [str(value).strip().upper() for value in raw_2017 if pd.notna(value) and str(value).strip()]
duplicates_2017 = len(names_2017) - len(set(names_2017))
feature_2017 = master.loc[master["Period"].astype(str).eq("2017_H1")]
feature_2017_counts = feature_2017.groupby("Date")["Symbol"].nunique()
phase_a_membership_rows = phase_a_gate.loc[
    phase_a_gate.iloc[:, 0].astype(str).str.contains("SET50 membership source", case=False, na=False)
]
phase_b_2017_source_url = str(
    declarations.loc[
        declarations["year"].eq(2017) & declarations["review_period"].astype(str).str.upper().eq("H1"),
        "source_url",
    ].iloc[0]
)
reconciliation = pd.DataFrame(
    [
        {
            "Period": "2017_H1",
            "Membership_File_Slots": len(member_columns),
            "Nonblank_Symbols": len(names_2017),
            "Unique_Symbols": len(set(names_2017)),
            "Duplicate_Symbol_Entries": duplicates_2017,
            "Blank_Symbol_Slots": len(member_columns) - len(names_2017),
            "Phase_A_Count_Scope": "2026 predictor-date universe only; checks daily member count in 2026.",
            "Phase_A_Reported_Members_Per_Date": "50",
            "Phase_B_Count_Scope": "All historical period rows; counts nonblank unique names in 2017_H1.",
            "Phase_B_Reported_2017_H1_Members": len(set(names_2017)),
            "Count_Discrepancy_Cause": "Different counting units; Phase A's 50 is a 2026 daily count, while Phase B exposed one blank 2017_H1 membership slot.",
            "Audit_Implementation_Error": False,
            "Date_Interpretation": "Local declaration file sets 2017_H1 effective date to 2017-01-01; no off-by-one issue was found for this count.",
            "2017_H1_Primary_SET_Evidence_Found": False,
            "Local_Secondary_Source_URL": phase_b_2017_source_url,
            "Feature_Master_2017_H1_Unique_Symbols": int(feature_2017["Symbol"].nunique()),
            "Feature_Master_2017_H1_Min_Daily_Symbol_Count": int(feature_2017_counts.min()),
            "Feature_Master_2017_H1_Max_Daily_Symbol_Count": int(feature_2017_counts.max()),
            "Frozen_Model_Training_Period": model_metadata.get("training_period"),
            "Affects_2026_Eligible_Membership": False,
            "Affects_Historical_Model_Context": True,
            "Status": "BLOCKED_HISTORICAL_PRIMARY_MEMBERSHIP_AND_FEATURE_CONTEXT_UNRESOLVED",
            "Evidence_Note": "Do not fill the blank. The 2026 official SET PDFs match their local lists; the 2017_H1 source is secondary and the feature Master Period label has 67-68 symbols/day, so it does not resolve the 49-name period claim.",
        }
    ]
)
write_csv("membership_reconciliation_2017.csv", reconciliation)

vendor_provenance_rows = [
    ("Execution provider", sidecar.get("source"), "VERIFIED_FROM_METADATA", SIDECAR, "Yahoo Finance via yfinance.download; third-party vendor, not official SET data."),
    ("Execution library/version", f"yfinance {sidecar.get('yfinance_version')}", "VERIFIED_FROM_METADATA", SIDECAR, "Recorded in the existing snapshot sidecar."),
    ("Execution retrieval timestamp", sidecar.get("downloaded_at_utc"), "VERIFIED_FROM_METADATA", SIDECAR, "UTC timestamp recorded in the existing snapshot sidecar."),
    ("Execution requested start", sidecar.get("start"), "VERIFIED_FROM_METADATA", SIDECAR, "Recorded start date."),
    ("Execution requested end (exclusive)", sidecar.get("end_exclusive"), "VERIFIED_FROM_METADATA", SIDECAR, "Recorded exclusive end date."),
    ("Execution requested ticker count", sidecar.get("tickers_requested"), "VERIFIED_FROM_METADATA", SIDECAR, "Count only; not the exact requested ticker list."),
    ("Execution exact requested ticker list", "UNKNOWN", "UNKNOWN", LINEAGE, "Do not infer the requested list from the 83 output symbols."),
    ("Execution interval", lineage.get("interval", "UNKNOWN"), "UNKNOWN", LINEAGE, "The original request interval is not recorded."),
    ("Execution group_by", lineage.get("group_by", "UNKNOWN"), "UNKNOWN", LINEAGE, "The original request grouping is not recorded."),
    ("Execution auto_adjust", sidecar.get("auto_adjust"), "VERIFIED_FROM_METADATA", SIDECAR, "The snapshot request setting is false."),
    ("Execution actions", sidecar.get("actions"), "VERIFIED_FROM_METADATA", SIDECAR, "The snapshot request setting is true."),
    ("Execution OHLC historical basis", "Yahoo OHLC from auto_adjust=False request; not exchange verified; split basis unresolved", "UNKNOWN", SIDECAR, "The sidecar explicitly warns that historical split basis may be adjusted; GLOBAL has unresolved basis anomalies."),
    ("Execution source artifact SHA-256", snapshot_hash, "VERIFIED_FROM_METADATA", LINEAGE, "Current hash matches the original and immutable-copy Phase B pins."),
    ("Execution Date timezone", "UNKNOWN; stored Date values are timezone-naive", "UNKNOWN", SNAPSHOT, "No source timezone or conversion rule is recorded."),
    ("Execution processing date normalization", "pd.to_datetime(...).dt.normalize() in Notebook 06", "VERIFIED_FROM_SOURCE_CODE", NOTEBOOK_06, "Backtest dates are normalized; this does not establish source timezone."),
    ("Feature downloader in Notebook 01", "yf.download(df['symbol'].tolist(), period='10y', interval='1d', auto_adjust=True, group_by='ticker')", "VERIFIED_FROM_SOURCE_CODE", NOTEBOOK_01, "Executed cell source; exact ticker values at that run and data artifact linkage are not recorded."),
    ("Feature downloader in Notebook 01 actions", "actions parameter omitted", "UNKNOWN", NOTEBOOK_01, "Omission does not prove actions=False."),
    ("Feature downloader in Notebook 03", "dynamic Yahoo ticker list; start_date=2015-08-01; end_date=today+1; auto_adjust=True; group_by='ticker'; interval/actions omitted", "VERIFIED_FROM_SOURCE_CODE", NOTEBOOK_03, "Executed cell source; exact run is not tied by a manifest to the pinned Master hash."),
    ("Feature exact ticker list", "UNKNOWN; source expression is dynamic", "UNKNOWN", NOTEBOOK_01, "Do not infer the exact list from final Master columns."),
    ("Feature retrieval timestamp/library version", "UNKNOWN", "UNKNOWN", NOTEBOOK_01, "No per-run metadata ties the feature acquisition to the pinned Master artifact."),
    ("Feature adjusted-price setting", "auto_adjust=True in existing downloader code", "VERIFIED_FROM_SOURCE_CODE", NOTEBOOK_01, "Feature source code and execution snapshot settings differ."),
    ("Feature source artifact SHA-256", master_hash, "VERIFIED_FROM_METADATA", PHASE_B_MANIFEST, "Pinned Master hash matches Phase B."),
    ("Feature/execution acquisition identity", "Separate acquisition paths and different auto_adjust settings", "VERIFIED_FROM_SOURCE_CODE", NOTEBOOK_01, "Features use adjusted-price downloader code; execution uses a separate auto_adjust=False snapshot."),
]
provenance = pd.DataFrame(
    [
        {
            "Field": field,
            "Value": value,
            "Evidence_Status": status,
            "Evidence_Path": str(path),
            "Evidence_Detail": detail,
        }
        for field, value, status, path, detail in vendor_provenance_rows
    ]
)
write_csv("vendor_provenance_recovery.csv", provenance)

missing_execution_dates = sorted(missing_rows["Date"].drop_duplicates().tolist())
last_banpu_feature_date_before_gap = (
    last_banpu_feature_before_missing.date().isoformat()
    if pd.notna(last_banpu_feature_before_missing)
    else ""
)
overlap_missing_banpu = int(
    missing_rows["Date"].isin(banpu_feature_dates).sum()
)
washout_dates = [
    date
    for date in predictor_dates
    if len(feature_calendar[max(0, feature_calendar.index(date) - 59): feature_calendar.index(date) + 1]) == 60
    and not any(
        window_date in banpu_feature_dates
        for window_date in feature_calendar[max(0, feature_calendar.index(date) - 59): feature_calendar.index(date) + 1]
    )
]
first_clean_decision_date = min(washout_dates).date().isoformat() if washout_dates else ""

banpu_impact_rows = [
    {
        "Surface": "Original missing execution OHLC",
        "Observed_Fact": f"{missing_cells} missing OHLC field-cells on {len(missing_execution_dates)} BANPU rows from {missing_start.date()} to {missing_end.date()}",
        "Exclusion_Propagation": "BANPU remains excluded for all of 2026 with the existing reason.",
        "Shared_Calculation_Impact": "Execution snapshot values are not inputs to the Master feature rank/proxy formulas.",
        "Status": "PASS_WITH_LIMITATIONS",
        "Evidence": str(SNAPSHOT),
    },
    {
        "Surface": "BANPU feature observations in the pinned Master",
        "Observed_Fact": f"{len(banpu_features)} 2026 feature rows; last row before missing execution begins is {last_banpu_feature_date_before_gap}; one late row is on 2026-11-13.",
        "Exclusion_Propagation": "Approved symbols are now filtered before frozen_model.predict and predict_proba.",
        "Shared_Calculation_Impact": "BANPU is included in same-date VolRank/LiquidityRank and in other members' leave-one-out market proxy while its feature returns exist.",
        "Status": "PASS_WITH_LIMITATIONS",
        "Evidence": str(MASTER),
    },
    {
        "Surface": "CorrRank/market-proxy washout",
        "Observed_Fact": f"Corr_60d uses a 60-observation rolling window; first date with no BANPU row in the current/last-60 feature dates is {first_clean_decision_date}.",
        "Exclusion_Propagation": "All earlier member-date rows are not eligible; the candidate universe only retains dates whose current and trailing 60 observations exclude BANPU.",
        "Shared_Calculation_Impact": "No BANPU return is present in the rolling market proxy window for the four eligible AOT predictor dates.",
        "Status": "PASS_WITH_LIMITATIONS",
        "Evidence": str(NOTEBOOK_03),
    },
    {
        "Surface": "Prediction model feature rows",
        "Observed_Fact": f"Notebook 06 applies the approved exclusions before inference; the dedicated SpyModel test passes; {test_pass_count}/18 synthetic tests pass.",
        "Exclusion_Propagation": "BANPU and GLOBAL rows do not enter frozen model inference.",
        "Shared_Calculation_Impact": "This does not rewrite precomputed features or historical training data.",
        "Status": "PASS",
        "Evidence": str(NOTEBOOK_06),
    },
    {
        "Surface": "Allocation inputs, orders, holdings, valuation",
        "Observed_Fact": "Notebook 06 runner filters predictions and execution data before signals and guards holdings/orders; actual portfolio output was not generated.",
        "Exclusion_Propagation": "Synthetic regression verifies BANPU/GLOBAL are absent from allocation inputs and Buy/Sell/holdings paths.",
        "Shared_Calculation_Impact": "No actual portfolio order or holding artifact exists because all backtests remain unrun.",
        "Status": "PASS_WITH_LIMITATIONS",
        "Evidence": str(NOTEBOOK_06),
    },
]
write_csv("banpu_impact_isolation.csv", pd.DataFrame(banpu_impact_rows))

member_event_count = int(len(event_member_rows))
member_event_symbols_count = len(event_member_symbols)
event_category_counts = corporate_relevance["Impact_Category"].value_counts().to_dict()
write_csv(
    "corporate_action_relevance_2026.csv",
    corporate_relevance,
)

zero_volume_rows = int(snapshot["Volume_Zero"].sum())
missing_volume_rows = int(snapshot["Volume_Missing"].sum())
negative_volume_rows = int(snapshot["Volume_Negative"].sum())
invalid_ohlc_rows = int(
    (
        snapshot["OHLC_Complete"]
        & (
            ~snapshot["OHLC_Positive_Finite"]
            | ~snapshot["OHLC_Boundaries_Valid"]
        )
    ).sum()
)
repeat_close_rows = int(snapshot["Repeated_Close_From_Previous_Observed_Row"].sum())
action_rows_2026 = int(
    snapshot["Dividends"].ne(0).sum() + snapshot["Stock Splits"].ne(0).sum()
)
source_tick_rows = int(len(global_diag))
vendor_action_symbols = set(
    snapshot.loc[
        snapshot["Dividends"].ne(0) | snapshot["Stock Splits"].ne(0),
        "Symbol",
    ].astype(str)
)
banpu_feature_by_period = banpu_features.groupby("Period").size().to_dict()
banpu_miss_feature_overlap_dates = sorted(
    missing_rows.loc[missing_rows["Date"].isin(banpu_feature_dates), "Date"]
    .drop_duplicates()
    .dt.strftime("%Y-%m-%d")
    .tolist()
)
candidate_quality = quality.loc[
    quality["Symbol"].astype(str).eq("AOT")
    & quality["Date"].isin(tradable["Execution_Date"])
].copy()

action_category_counts = corporate_relevance["Impact_Category"].value_counts().to_dict()

quality_report = f"""# Vendor Execution Quality — Phase C

## Scope and vendor status

- Provider: Yahoo Finance through the existing `yfinance.download` snapshot. This is accepted as third-party research data under Approach B; it is not official or exchange-authorized SET execution data.
- Snapshot SHA-256: `{snapshot_hash}`. No Yahoo download or price replacement was performed in Phase C.
- Coverage: {len(snapshot):,} Date-Symbol rows, {snapshot['Symbol'].nunique()} symbols, {snapshot['Date'].nunique()} observed dates ({snapshot['Date'].min().date()} to {snapshot['Date'].max().date()}).

## Data quality

- Duplicate Date-Symbol records: {int(snapshot.duplicated(['Date', 'Symbol']).sum())}.
- Missing OHLC field-cells: {missing_by_field}; total {missing_cells}. All missing fields are on BANPU across {len(missing_rows)} rows.
- Non-positive/non-finite complete OHLC rows or OHLC boundary violations: {invalid_ohlc_rows}.
- Volume missing / zero / negative rows: {missing_volume_rows} / {zero_volume_rows} / {negative_volume_rows}. Zero volume is not treated as proof of suspension or non-trading.
- Repeated consecutive observed Close values: {repeat_close_rows}. This is a diagnostic only; repeated prices do not establish staleness.
- Vendor-reported action fields: {action_rows_2026} nonzero Dividends/Stock Splits rows across {len(vendor_action_symbols)} symbols. These are vendor records, not official confirmations.
- Existing price-basis diagnostic: {source_tick_rows} anomaly field-rows, all for GLOBAL. GLOBAL remains excluded; no split is asserted from tick alignment.

## Eligible candidate sample check

- AOT's four candidate execution records have valid Open, Close, OHLC boundaries, and positive Volume: {bool(candidate_quality['Valid_Execution_Data'].all()) if len(candidate_quality) == 4 else False}.
- Predictor dates are aligned to the next date observed in the pinned vendor snapshot, not to an invented weekday calendar. The final observed predictor date has no next observed execution date.
- Candidate rows and record-level diagnostics are in `vendor_execution_quality_2026.csv`; no price was imputed or carried forward.

## Decision

The broad snapshot remains quality-limited because BANPU has 253 missing OHLC cells, volume has missing/zero rows, GLOBAL has unresolved basis anomalies, and the Yahoo date calendar is not an official SET calendar. These issues are bounded away from the four AOT candidate rows by the exclusion and date-scoped feature rules, but do not approve the Research Backtest Gate. Board-lot and stale valuation policies remain unresolved and no portfolio valuation was run.
"""
(OUT / "vendor_execution_quality_report.md").write_text(quality_report, encoding="utf-8")

provenance_report = f"""# Vendor Provenance Recovery — Phase C

## Existing execution snapshot

- Provider/library: `{sidecar.get('source')}`; yfinance `{sidecar.get('yfinance_version')}`.
- Retrieval timestamp: `{sidecar.get('downloaded_at_utc')}`.
- Requested range: `{sidecar.get('start')}` through `{sidecar.get('end_exclusive')}` (end exclusive).
- Requested ticker count: {sidecar.get('tickers_requested')}; exact requested ticker list: **UNKNOWN**. The observed output columns are not used to reconstruct that list.
- Settings verified from the sidecar: `auto_adjust={sidecar.get('auto_adjust')}`, `actions={sidecar.get('actions')}`.
- `interval` and `group_by`: **UNKNOWN** in the execution lineage. They are not inferred from the output shape.
- Snapshot SHA-256: `{snapshot_hash}`, matching both the immutable copy and Phase B's pinned hash.
- Source timezone: **UNKNOWN**. Stored Date values are timezone-naive; Notebook 06 normalizes parsed dates but does not establish source timezone.
- Price basis: Yahoo OHLC from an `auto_adjust=False` request, not official SET prints. The sidecar warns that historical split basis may still be adjusted; GLOBAL remains excluded due unresolved anomalies.

## Feature acquisition is a separate path

- Notebook 01 source code calls `yf.download(df['symbol'].tolist(), period='10y', interval='1d', auto_adjust=True, group_by='ticker')`.
- Notebook 03 also contains an executed dynamic-ticker downloader with `auto_adjust=True` and `group_by='ticker'`; its interval and actions argument are omitted.
- These are source-code facts, not a complete manifest tying a specific acquisition run to the pinned Master hash. The exact feature ticker list, run timestamp/library version, and whether actions were requested remain unknown.
- Therefore the feature source and execution snapshot are separate acquisition paths and use different adjustment settings; they are not the same OHLCV download.

See `vendor_provenance_recovery.csv` for each field's evidence class and path.
"""
(OUT / "vendor_provenance_report.md").write_text(provenance_report, encoding="utf-8")

banpu_report = f"""# BANPU Impact Isolation — Phase C

## Execution data

- BANPU remains excluded for all of 2026 with the unchanged reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`.
- The original snapshot still contains {missing_cells} missing OHLC cells across {len(missing_rows)} BANPU rows ({missing_start.date()} through {missing_end.date()}); no prices were filled.
- Those execution OHLC values are not used by the Master feature rank or market-proxy formulas. The missing execution bars therefore do not directly enter shared feature calculations.

## Shared feature effects

- The pinned Master has {len(banpu_features)} BANPU feature rows in 2026 ({banpu_feature_by_period}); the last BANPU feature observation before the execution-missing interval is {last_banpu_feature_date_before_gap}. There is one late BANPU feature row on 2026-11-13, which has no next observed execution date and is not an eligible predictor row.
- Notebook 03 computes same-date cross-sectional VolRank/LiquidityRank and a SET50 market proxy. For each other member, the leave-one-out proxy includes BANPU's return when present; `Corr_60d` then uses a 60-observation rolling window.
- The first predictor date whose current and trailing 60 observed feature dates contain no BANPU row is {first_clean_decision_date}. The Phase C universe excludes earlier dates; this is a date-bounded restriction, not a rebuild of the Master.

## Propagation through Notebook 06

- The edited `generate_predictions` function applies the approved exclusion policy before the frozen model's `predict` and `predict_proba` calls.
- The targeted test confirms BANPU is removed from model input. The full synthetic regression cell passed {test_pass_count}/18 tests.
- The saved notebook output block contains {serialized_test_pass_count} passing rows and {serialized_output_state}; the fresh run result is also preserved in `notebook_06_synthetic_regression_results.csv`.
- Downstream runner guards still filter predictions/execution data before signals and contain order/holding exclusion checks. No actual allocation, order, holding, or valuation outputs were produced because no backtest was run.

## Classification

`PASS_WITH_LIMITATIONS` for the BANPU missing-execution issue within the eligible Phase C candidate sample: BANPU is excluded, its execution gaps are not feature inputs, its precomputed feature influence is excluded by a 60-observation date washout, and its own late feature row cannot be executed. The historical Master remains unchanged; no claim is made that BANPU never influenced features outside the eligible date window.
"""
(OUT / "banpu_impact_report.md").write_text(banpu_report, encoding="utf-8")

event_category_counts = {key: int(value) for key, value in action_category_counts.items()}
corporate_report = f"""# Corporate Action Relevance — Phase C

## Inventory result

- Inspected all {len(ledger)} local ledger rows ({len(vendor_events)} vendor action records plus {len(ledger) - len(vendor_events)} user-provided claims).
- `Official_Source` is blank for all {len(ledger)} ledger rows; none is confirmed or applied by the portfolio engine.
- Local event labels include {ledger['Event_Type'].value_counts().to_dict()}; these labels are treated as claims, not confirmation of event terms.
- 2026 verified impact: 0. Historical verified impact: 0. Category C, outside the officially verified 2026 SET50 member union: {event_category_counts.get('C_UNRELATED_TO_VERIFIED_2026_MEMBER_UNIVERSE', 0)}. Category D unresolved member-overlap rows: {event_category_counts.get('D_UNRESOLVED', 0)}.
- The 2026 member-overlap set contains {member_event_count} unresolved event rows across {member_event_symbols_count} symbols. AOT and BTS have no local ledger rows; the snapshot also has no nonzero Yahoo Dividends/Stock Splits for either.

## Impact handling

- Candidate cash entitlement, share-quantity, identity, feature-continuity, and execution-price effects are marked as potential only in `corporate_action_relevance_2026.csv`.
- Event-bearing member securities are excluded from the Phase C candidate universe for the 2026 period because the local event records have no verified terms and the engine rejects unverified actions. This does not alter historical membership or apply any event.
- Non-member events are categorized outside the 2026 eligible universe based on the SET H1/H2 2026 primary membership PDFs; the events themselves remain unverified.

No Yahoo data was downloaded to investigate events. Only already-local evidence was used.
"""
(OUT / "corporate_action_relevance_report.md").write_text(corporate_report, encoding="utf-8")

identity_report = f"""# Security Identity Scope — Phase C

- The 2026 local constituent union contains {len(members_2026)} symbols and matches the retrieved SET H1/H2 2026 constituent PDFs.
- BANPU is `EXCLUDED_IDENTITY_UNRESOLVED`: the local identity map and user claims contain unsupported merger/conversion details, and no primary URL is attached. BANPU remains excluded under its existing execution-data reason.
- The other 2026 tickers are classified `VERIFIED_CONTINUOUS_IDENTITY` only at the vendor-key level: their ticker keys are observed in the existing snapshot/Master and there is no local identity-map transition row. This is not official issuer-identifier verification.
- BPP and BANPUU are included as non-2026 identity-claim context; GLOBAL is included as a non-member with its existing exclusion and price-basis issue.

The detailed row-level scope is in `security_identity_scope_2026.csv`. No identity mapping or feature history was changed.
"""
(OUT / "security_identity_report.md").write_text(identity_report, encoding="utf-8")

membership_report = f"""# Membership Reconciliation — Phase C

## 2026 membership

- Retrieved and text-extracted the SET-hosted H1 and H2 2026 PDFs cited by the local declaration file.
- Each official PDF contains 50 unique constituents and matches the corresponding 50-symbol local row exactly (H1: {len(official_h1)}/50; H2: {len(official_h2)}/50).
- Effective dates match the local declaration file: 2026-01-01 and 2026-07-01. The verified 2026 union has {len(members_2026)} symbols.
- PDFs and extracted text are retained under `sources/`; their SHA-256 values are in `membership_2026_primary_evidence_audit.csv` and the manifest.

## 2017_H1 discrepancy

- The local 2017_H1 row has {len(member_columns)} slots, {len(names_2017)} nonblank unique symbols, {duplicates_2017} duplicates, and {len(member_columns) - len(names_2017)} blank slot.
- Phase A's `SET50_Members == 50` check is computed over its 2026 predictor dates. Phase B counts every period row and found 49 names for 2017_H1. These are different counting units; the audits are not contradictory and neither count indicates an implementation error.
- The local 2017 source URL is MGR Online (secondary), not a primary SET document. No official 2017_H1 list was established; the missing symbol is not filled.
- The Master has {int(feature_2017['Symbol'].nunique())} symbols labeled 2017_H1 and {int(feature_2017_counts.min())}-{int(feature_2017_counts.max())} symbols on its dates. That label does not reconcile the local 49-name claim.
- Since the frozen model's training period is `{model_metadata.get('training_period')}`, this remains an unresolved historical model-context issue. It does not change the officially verified 2026 membership dates or the AOT candidate membership.

No historical membership or declaration file was modified.
"""
(OUT / "membership_calendar_recovery_report.md").write_text(membership_report, encoding="utf-8")

coverage_summary = (
    coverage.groupby("Date")
    .agg(
        SET50_Members=("SET50_Member_Count", "first"),
        Excluded_Securities=("Excluded_Security_Count", "first"),
        Tradable_Securities=("Tradable_Security_Count", "first"),
        Missing_Execution_Rows=("Missing_Execution_Rows", "first"),
        Missing_OHLC_Field_Cells=("Missing_OHLC_Field_Cells", "first"),
        Candidate_Data_Coverage_Pct=("Candidate_Data_Coverage_Pct", "first"),
        Tradable_Coverage_Pct=("Tradable_Coverage_Pct", "first"),
    )
    .reset_index()
)
overall_candidate_coverage = (
    100.0 * int(universe["Has_Valid_Execution_Data"].sum()) / len(universe)
    if len(universe)
    else 0.0
)
overall_tradable_coverage = 100.0 * len(tradable) / len(universe) if len(universe) else 0.0
coverage_report = f"""# Tradable Universe Coverage — Phase C

- Official 2026 membership rows evaluated: {len(universe):,}; 50 constituents on every candidate predictor date.
- Candidate data coverage (valid next-date OHLC and positive volume): {overall_candidate_coverage:.2f}%.
- Candidate tradable rows after exclusions and feature/date requirements: {len(tradable)} ({overall_tradable_coverage:.4f}% of member-date rows).
- Eligible symbols: {", ".join(sorted(tradable['Symbol'].astype(str).unique())) or "NONE"}.
- Snapshot missing OHLC rows are not filled. BANPU's {missing_cells} missing field-cells are documented separately; it is fully excluded.
- The per-date counts, next observed execution dates, missing rows/field-cells, coverage, and exclusion reasons are in `tradable_universe_coverage_phase_C.csv`.
- Coverage is not an approval measure; the Research Backtest Gate remains closed.
"""
(OUT / "universe_coverage_phase_C.md").write_text(coverage_report, encoding="utf-8")

phase_a_status_counts = phase_a_gate.loc[
    ~phase_a_gate.iloc[:, 0].astype(str).str.upper().eq("PHASE_A_OVERALL"), "Status"
].value_counts().to_dict()
phase_b_status_counts = phase_b_gate.loc[
    ~phase_b_gate.iloc[:, 0].astype(str).str.upper().eq("PHASE_B_OVERALL"), "Status"
].value_counts().to_dict()
phase_a_rows = len(pd.read_csv(PHASE_A / "tradable_universe_2026.csv"))
phase_a_tradable_rows = int(
    pd.read_csv(PHASE_A / "tradable_universe_2026.csv")["Is_Tradable"]
    .astype(str)
    .str.lower()
    .isin(["true", "1"])
    .sum()
)
phase_b_rows = len(pd.read_csv(PHASE_B / "tradable_universe_2026_phase_B.csv"))
phase_b_tradable_rows = int(
    pd.read_csv(PHASE_B / "tradable_universe_2026_phase_B.csv")["Is_Tradable"].astype(bool).sum()
)

gate_rows = [
    ("Protected snapshot, immutable copy, Master, model, membership, declarations and Notebook 05 unchanged", "PASS", "Current SHA-256 values match Phase B recorded hashes.", "Notebook 06 is the only source notebook intentionally edited."),
    ("2026 membership supported by official primary source", "PASS", "Both SET PDFs were retrieved, extracted and match the local 50-symbol H1/H2 lists.", "No official 2026 session calendar was retrieved."),
    ("Vendor provenance recovery", "PASS_WITH_LIMITATIONS", "Provider, library version, retrieval time, date range, auto_adjust, actions, and source hash are recorded.", "Exact ticker list, interval, group_by, timezone and exact feature-acquisition run remain UNKNOWN."),
    ("BANPU missing execution impact", "PASS_WITH_LIMITATIONS", "BANPU is excluded for 2026; 253 missing OHLC cells remain; execution bars are not inputs to feature formulas.", "Precomputed BANPU feature effects are bounded by excluding the affected dates and the 60-observation washout."),
    ("BANPU excluded before model inference", "PASS", f"Notebook 06 has pre-inference exclusion and the dedicated test passes; synthetic suite {test_pass_count}/18.", "The Master and frozen model were not changed."),
    ("GLOBAL investigation / exclusion", "PASS_WITH_LIMITATIONS", f"{source_tick_rows} basis diagnostic field-rows are confined to GLOBAL; GLOBAL is absent from both official 2026 membership lists.", "No official corporate-action confirmation; no split is asserted."),
    ("Corporate-action impact in eligible sample", "PASS_WITH_LIMITATIONS", "Event-bearing 2026 member symbols are excluded; the four eligible rows are AOT with no local ledger or Yahoo action row.", "All 141 ledger rows remain unconfirmed; only vendor/local evidence is available."),
    ("Identity confidence in eligible sample", "PASS_WITH_LIMITATIONS", "AOT has continuous vendor ticker-key observations and no local identity transition row.", "No official issuer-ID confirmation; BANPU remains identity-unresolved and excluded."),
    ("2017_H1 historical membership/model context", "BLOCKED", "One blank membership slot; no primary SET 2017 source; model training period includes 2017.", "Do not fill the missing name or retrain the frozen model."),
    ("Execution quality for eligible AOT rows", "PASS_WITH_LIMITATIONS", "All four next-date AOT records have valid OHLC, positive volume and no flagged basis anomaly.", "Snapshot-wide missing/zero volume, repeated closes and unverified vendor basis remain documented."),
    ("Date alignment", "PASS_WITH_LIMITATIONS", "Candidate dates use the next date observed in the pinned vendor snapshot; no generic weekday calendar is substituted.", "Official 2026 trading calendar remains unavailable."),
    ("Tradable candidate universe non-empty", "PASS", f"{len(tradable)} candidate member-date rows across {tradable['Symbol'].nunique()} symbol(s).", "A non-empty candidate is not an approved backtest universe."),
    ("Board-lot, stale valuation and allocator fallback policies resolved", "BLOCKED", "Notebook 06 still has unresolved board-lot/stale policies; no policy was invented.", "Required before any portfolio run."),
    ("CVaR formulation approved", "BLOCKED", "No approved CVaR formulation was found; allocation methods were not changed.", "Required before any CVaR combination can run."),
    ("Research Backtest Gate", "BLOCKED", "The gate remains closed; no 63-combination backtest was run.", "Historical model context and research-methodology blockers remain."),
]
overall_status = "BLOCKED" if any(row[1] == "BLOCKED" for row in gate_rows) else "PASS"
gate_rows.append(
    (
        "PHASE_C_OVERALL",
        overall_status,
        "A candidate sample was constructed; critical blockers remain.",
        "Do not open the Research Backtest Gate or run portfolio combinations.",
    )
)
gate = pd.DataFrame(gate_rows, columns=["Requirement", "Status", "Evidence", "Remaining_Limitation_or_Blocker"])
write_csv("phase_C_gate.csv", gate)

blocker_rows = [
    {
        "Blocker_ID": "C-METHOD-01",
        "Status": "BLOCKED",
        "Scope": "All portfolio combinations",
        "Blocker": "Board-lot, stale valuation and fallback policies are unresolved.",
        "Evidence_Still_Needed": "Approve the existing policy definitions without inventing defaults; use only after user/research approval.",
        "Impact": "Portfolio sizing, no-fill handling and valuation cannot be validated.",
    },
    {
        "Blocker_ID": "C-CVAR-01",
        "Status": "BLOCKED",
        "Scope": "CVaR allocation",
        "Blocker": "CVaR formulation is not approved.",
        "Evidence_Still_Needed": "Explicit research-methodology approval for the CVaR objective/constraints and historical input window.",
        "Impact": "No CVaR backtest may run; no formulation was invented.",
    },
    {
        "Blocker_ID": "C-MEM-2017-01",
        "Status": "BLOCKED",
        "Scope": "Frozen model historical training context",
        "Blocker": "2017_H1 local membership has 49 names with one blank slot and no primary SET evidence; Master labels show 67-68 symbols per date.",
        "Evidence_Still_Needed": "Primary SET 2017_H1 constituents/effective-date document and source reconciliation for historical feature membership.",
        "Impact": "Does not alter verified 2026 membership; leaves historical model context unresolved.",
    },
    {
        "Blocker_ID": "C-PROV-01",
        "Status": "PASS_WITH_LIMITATIONS",
        "Scope": "Execution snapshot provenance",
        "Blocker": "Exact requested ticker list, interval, group_by and timezone are unknown.",
        "Evidence_Still_Needed": "If a complete acquisition record is required, recover an existing original request log/manifest; do not reconstruct from output columns.",
        "Impact": "Snapshot remains pinned and reproducible by hash; missing request semantics are disclosed.",
    },
    {
        "Blocker_ID": "C-ACTION-01",
        "Status": "PASS_WITH_LIMITATIONS",
        "Scope": "Non-eligible event-bearing securities",
        "Blocker": "141 local action ledger rows lack official source URLs or confirmed terms; 97 overlap the verified 2026 member union.",
        "Evidence_Still_Needed": "Primary issuer/SET/SEC terms and effective dates before any affected symbol is included.",
        "Impact": "Affected 2026 member securities are excluded; no action is applied to the eligible candidate.",
    },
    {
        "Blocker_ID": "C-CALENDAR-01",
        "Status": "PASS_WITH_LIMITATIONS",
        "Scope": "Vendor date alignment",
        "Blocker": "No official 2026 SET trading calendar is available locally.",
        "Evidence_Still_Needed": "Official calendar if exchange-session claims are needed; current candidate alignment uses the next observed vendor date.",
        "Impact": "Does not use a generic weekday calendar; calendar status is not described as official.",
    },
]
write_csv("phase_C_blocker_register.csv", pd.DataFrame(blocker_rows))

readiness_report = f"""# Phase C Research Readiness — Vendor-Based Validation

## Decision

**Candidate universe: non-empty. Research Backtest Gate: BLOCKED and remains closed.**

Approach B accepts Yahoo Finance/yfinance as a third-party historical market-data vendor. It is not described as official SET execution data. The candidate universe contains **{tradable['Symbol'].nunique()} eligible symbol(s)** and **{len(tradable)} member-date rows**: {", ".join(sorted(tradable['Symbol'].astype(str).unique()))}. These are bounded research candidates, not an approval to run a portfolio backtest.

## Phase comparison

| Phase | Existing result | Candidate member-date rows evaluated | Tradable rows / candidates (not approved) | Gate |
|---|---|---:|---:|---|
| Phase A | {phase_a_status_counts} | {phase_a_rows:,} | {phase_a_tradable_rows:,} | BLOCKED |
| Phase B | {phase_b_status_counts} | {phase_b_rows:,} | {phase_b_tradable_rows:,} | BLOCKED |
| Phase C | Yahoo vendor approach; official 2026 membership recovered | {len(universe):,} | {len(tradable):,} | BLOCKED |

Phase A and Phase B artifacts and results were preserved, not rewritten.

## Provenance and price quality

- Execution data: Yahoo Finance/yfinance 1.8.0, retrieval `{sidecar.get('downloaded_at_utc')}`, requested `{sidecar.get('start')}` to `{sidecar.get('end_exclusive')}` exclusive, `auto_adjust=False`, `actions=True`.
- Exact execution ticker list, `interval`, `group_by`, and source timezone remain **UNKNOWN**. The snapshot and immutable copy both match pinned SHA-256 `{snapshot_hash}`.
- Feature acquisition source code uses `auto_adjust=True`; the pinned Master and execution snapshot are separate acquisitions with different price-adjustment settings. The exact feature downloader run is not bound to the Master hash by a run manifest.
- Missing OHLC remains {missing_by_field} (253 field-cells), all on BANPU. No forward-fill, backfill, interpolation, zero fill, or price correction occurred.
- Snapshot-wide execution quality has {invalid_ohlc_rows} invalid/nonpositive OHLC rows, {missing_volume_rows} missing-volume rows, {zero_volume_rows} zero-volume rows, {repeat_close_rows} repeated observed closes, and {source_tick_rows} GLOBAL price-basis anomaly field-rows. Repeated prices/zero volume are not interpreted as suspension or stale status.

## BANPU / GLOBAL

- BANPU remains excluded for all of 2026 with reason `INSUFFICIENT_VERIFIED_EXECUTION_DATA`; the original missing OHLC cells remain documented.
- The missing execution OHLC rows do not feed the feature pipeline. Separately, BANPU feature observations do enter cross-sectional ranks/market proxy while present. Notebook 06 now filters approved exclusions before model inference, and the candidate universe excludes predictor dates until the 60-observation shared-feature washout. The four eligible AOT rows are after that window.
- GLOBAL remains excluded by existing policy. Its {source_tick_rows} anomalies are GLOBAL-only and do not establish a split. GLOBAL is not a 2026 SET50 constituent in either official PDF.

## Corporate actions and identity

- All {len(ledger)} corporate-action ledger rows remain unconfirmed and unapplied; {member_event_count} event rows across {member_event_symbols_count} symbols overlap the official 2026 member union. Event-bearing member securities are excluded from the candidate universe. AOT has no local event record and no nonzero Yahoo Dividends/Stock Splits row; this is vendor evidence, not official confirmation.
- BANPU identity/merger claims remain unresolved and BANPU is excluded. AOT is continuous at the local vendor-ticker-key level only; no official issuer-ID claim is made.

## Membership / calendar

- Official SET H1 and H2 2026 PDFs were retrieved and match all {len(official_h1)} and {len(official_h2)} local constituent names respectively.
- The 2017_H1 local membership row remains unresolved: 49 nonblank unique names, one blank slot, no primary source. Phase A's 50 count was for 2026 daily membership, not 2017. Because the frozen model training period is `{model_metadata.get('training_period')}`, the historical model context remains a research-validity blocker.
- The official trading calendar is unavailable. Candidate execution dates use the next observed date in the pinned Yahoo snapshot, not a generic weekday calendar.

## Exact remaining blockers

1. Board-lot, stale-valuation and fallback policies are unresolved.
2. CVaR formulation is not approved; allocation methods were not modified.
3. 2017_H1 historical membership and its relationship to frozen-model training features remain unresolved.
4. Full execution request semantics (exact ticker list, interval, grouping, timezone) remain unknown.
5. 141 action-ledger events have no verified primary terms; event-bearing 2026 symbols are excluded.
6. No official 2026 session calendar is present; only vendor-observed date alignment is supported.

## Stop conditions and regression

- 63 portfolio combinations run: **No**.
- Model fit/retrain: **No**.
- Source data or Notebook 05 modified: **No**.
- Actions applied, missing prices filled, or Research Gate opened: **No**.
- Notebook 06 synthetic regressions: **{test_pass_count}/18 PASS**, including exclusion before model inference.
- The serialized Notebook 06 output {serialized_output_state} ({serialized_test_pass_count}/18); fresh execution evidence is in `notebook_06_synthetic_regression_results.csv`.
- Original snapshot, immutable copy, Master, frozen model, membership, declarations and Phase A/B evidence hashes: **unchanged**.

See `phase_C_gate.csv`, `phase_C_blocker_register.csv`, `phase_C_manifest.json`, and the focused reports for evidence paths.
"""
(OUT / "phase_C_research_readiness_report.md").write_text(readiness_report, encoding="utf-8")

gate_summary = {
    "overall_status": overall_status,
    "eligible_symbols": sorted(tradable["Symbol"].astype(str).unique()),
    "eligible_member_date_rows": int(len(tradable)),
    "member_date_rows_evaluated": int(len(universe)),
    "missing_ohlc_field_cells": missing_by_field,
    "corporate_action_categories": event_category_counts,
    "banpu_first_clean_decision_date": first_clean_decision_date,
    "notebook_06_synthetic_tests_passed": test_pass_count,
    "notebook_06_saved_output_stale": serialized_output_stale,
    "notebook_06_serialized_test_pass_count": serialized_test_pass_count,
    "research_backtest_gate_open": False,
}

output_names = [
    "notebook_06_synthetic_regression_results.csv",
    "vendor_provenance_recovery.csv",
    "vendor_provenance_report.md",
    "banpu_impact_isolation.csv",
    "banpu_impact_report.md",
    "corporate_action_relevance_2026.csv",
    "corporate_action_relevance_report.md",
    "security_identity_scope_2026.csv",
    "security_identity_report.md",
    "membership_reconciliation_2017.csv",
    "membership_calendar_recovery_report.md",
    "membership_2026_primary_evidence_audit.csv",
    "vendor_execution_quality_2026.csv",
    "vendor_execution_quality_report.md",
    "tradable_universe_2026_phase_C.csv",
    "execution_excluded_symbols_phase_C.csv",
    "tradable_universe_coverage_phase_C.csv",
    "universe_coverage_phase_C.md",
    "phase_C_gate.csv",
    "phase_C_blocker_register.csv",
    "phase_C_research_readiness_report.md",
]
output_hashes = {name: sha256(OUT / name) for name in output_names}
protected_after = {name: sha256(path) for name, path in protected_paths.items()}
if protected_after != protected_before:
    raise AssertionError("A protected source asset changed during Phase C generation.")

manifest = {
    "schema_version": "phase-c-v1",
    "phase": "Phase C — Vendor-Based Research Backtest Validation",
    "approach": "B — Yahoo Finance/yfinance accepted as a third-party historical market-data vendor, not official SET execution data",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "workspace": str(OUT),
    "official_membership_documents_retrieved": True,
    "market_data_downloaded": False,
    "yfinance_download_performed": False,
    "source_data_modified": False,
    "master_dataset_modified": False,
    "frozen_model_fit_or_retrained": False,
    "notebook_05_modified": False,
    "notebook_06_modified": True,
    "notebook_06_change": "Filter approved excluded symbols from feature rows before frozen model predict/predict_proba; add focused synthetic regression.",
    "corporate_actions_applied": False,
    "prices_imputed_or_corrected": False,
    "portfolio_backtests_63_executed": False,
    "research_backtest_gate_open": False,
    "protected_hashes_phase_B_baseline": phase_b_pins,
    "protected_hashes_before_phase_C": protected_before,
    "protected_hash_checks": protected_pin_checks,
    "protected_hashes_after_phase_C": protected_after,
    "phase_A_artifact_integrity_checks": phase_a_output_checks,
    "phase_B_artifact_integrity_checks": phase_b_output_checks,
    "new_official_membership_sources": {
        "2026_H1": {
            "url": "https://media.set.or.th/set/Documents/2025/Dec/SET50_100_H1_2026.pdf",
            "publisher": "Stock Exchange of Thailand",
            "pdf_path": str(H1_PDF),
            "pdf_sha256": sha256(H1_PDF),
            "extracted_text_path": str(H1_TEXT),
            "local_members_match": True,
        },
        "2026_H2": {
            "url": "https://media.set.or.th/set/Documents/2026/Jun/SET50-SET100-H2-2026.pdf",
            "publisher": "Stock Exchange of Thailand",
            "pdf_path": str(H2_PDF),
            "pdf_sha256": sha256(H2_PDF),
            "extracted_text_path": str(H2_TEXT),
            "local_members_match": True,
        },
    },
    "eligible_universe": gate_summary,
    "phase_A_gate_status_counts": {str(key): int(value) for key, value in phase_a_status_counts.items()},
    "phase_B_gate_status_counts": {str(key): int(value) for key, value in phase_b_status_counts.items()},
    "candidate_coverage_pct": float(overall_candidate_coverage),
    "tradable_coverage_pct": float(overall_tradable_coverage),
    "banpu_execution_missing": {
        "field_cells": missing_by_field,
        "total_field_cells": missing_cells,
        "rows": int(len(missing_rows)),
        "symbols": missing_symbols,
        "date_range": [missing_start.date().isoformat(), missing_end.date().isoformat()],
        "feature_row_overlap_dates": banpu_miss_feature_overlap_dates,
        "first_clean_decision_date": first_clean_decision_date,
    },
    "corporate_action_inventory": {
        "rows": int(len(ledger)),
        "vendor_action_rows": int(len(vendor_events)),
        "official_source_count": int(ledger["Official_Source"].notna().sum()),
        "applied_rows": int(ledger["Applied_By_Portfolio_Engine"].fillna(False).astype(bool).sum()),
        "category_counts": event_category_counts,
    },
    "notebook_06_regression": {
        "tests_passed": test_pass_count,
        "tests_failed": test_fail_count,
        "serialized_output_pass_count": serialized_test_pass_count,
        "serialized_output_stale": serialized_output_stale,
        "evidence_path": str(NOTEBOOK_TEST_RESULTS),
        "pre_inference_filter_present": pre_inference_filter_present,
        "excluded_symbols_removed_before_model_inference_test_present": banpu_input_test_present,
    },
    "unresolved_blockers": [
        "Board-lot, stale valuation and fallback policies.",
        "CVaR formulation is not approved.",
        "2017_H1 historical membership/model context.",
        "Execution interval, group_by, exact ticker list and source timezone.",
        "141 unverified action-ledger events; affected member securities remain excluded.",
        "Official 2026 trading calendar unavailable.",
    ],
    "output_hashes_sha256": output_hashes,
    "manifest_self_hash": "not included",
}
(OUT / "phase_C_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")

print(json.dumps(gate_summary, indent=2, ensure_ascii=False))
print("Phase C outputs:", len(output_names) + 1)
print("Protected sources unchanged:", protected_after == protected_before)
print("Phase A/B audit artifacts unchanged:", all(row["unchanged"] for row in phase_a_output_checks.values()) and all(row["unchanged"] for row in phase_b_output_checks.values()))
