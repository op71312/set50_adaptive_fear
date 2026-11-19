import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd


ROOT = Path(r"D:\Project_Github\set_fear_index")
RESULTS = ROOT / "backtest_results"
DATASET = ROOT / "dataset"
OUT = Path(__file__).resolve().parent
PHASE_A = RESULTS / "research_audit_20261116T044415991651Z_ee2aa7e1"
LINEAGE_PATH = RESULTS / "execution_data_lineage.json"
LINEAGE = json.loads(LINEAGE_PATH.read_text(encoding="utf-8"))
SNAPSHOT = Path(LINEAGE["original_snapshot"]["path"])
SIDECAR = SNAPSHOT.with_suffix(".json")
IMMUTABLE = RESULTS / "execution_data_v2" / "execution_ohlcv_original.parquet"
VERIFIED = RESULTS / "execution_data_v2" / "execution_ohlcv_verified_v2.parquet"
MASTER = DATASET / "verified_build_20261113_152948" / (
    "SET50_Master_Dataset_DateSymbol_Sorted_VolZ_Fixed.parquet"
)
MODEL = ROOT / "models" / "Original_Softmax_Final" / "final_softmax_model.joblib"
MEMBERSHIP = DATASET / "SET50_constituents_by_halfyear_2016_2026.csv"
DECLARATIONS = DATASET / "set50_declare_dates_2016_2026.csv"
LEDGER = RESULTS / "corporate_action_ledger_official.csv"
VENDOR_EVENTS = RESULTS / "corporate_action_vendor_events.csv"
IDENTITY_MAP = RESULTS / "security_identity_mapping.csv"
EXCLUSIONS = RESULTS / "research_controls" / "execution_excluded_symbols.csv"
PHASE_A_UNIVERSE = PHASE_A / "tradable_universe_2026.csv"
PHASE_A_GATE = PHASE_A / "phase_A_gate.csv"
OFFICIAL_CALENDAR = DATASET / "SET_trading_calendar_2026.csv"
OFFICIAL_ACTIONS = DATASET / "official_corporate_actions_2026.csv"
PINNED_SNAPSHOT = "14ca82c9a481118910952cfaaaeea08daecd6548d9d99e19a66e4d9c51ef986a"
PINNED_MODEL = "8ec9433bd5fa6419b7f6870f1058917b7fb3f6f0cb66cbc771a45f6956a048c7"


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def bool_value(value):
    if isinstance(value, bool):
        return value
    return text_value(value).lower() in {"true", "1", "yes"}


def publisher_from_url(value):
    host = urlparse(text_value(value)).hostname or ""
    if host == "set.or.th" or host.endswith(".set.or.th"):
        return "Stock Exchange of Thailand (publisher inferred from recorded URL; not fetched)"
    if host == "sec.or.th" or host.endswith(".sec.or.th"):
        return "Thai SEC (publisher inferred from recorded URL; not fetched)"
    if host:
        return f"Unverified publisher at {host}"
    return "Not recorded"


def to_date_text(value):
    parsed = pd.to_datetime(value, format="mixed", errors="coerce")
    if pd.isna(parsed):
        return ""
    return parsed.strftime("%Y-%m-%d")


def period_for_date(value):
    parsed = pd.to_datetime(value, format="mixed", errors="coerce")
    if pd.isna(parsed):
        return ""
    return f"{parsed.year}_H{1 if parsed.month <= 6 else 2}"


def hash_if_file(path):
    return sha256_file(path) if path is not None and Path(path).is_file() else ""


if not PHASE_A_GATE.is_file() or not PHASE_A_UNIVERSE.is_file():
    raise FileNotFoundError("The Phase A baseline deliverables are missing.")
if OUT.exists() and any(
    path.is_file() and path.name != Path(__file__).name for path in OUT.iterdir()
):
    raise FileExistsError(f"Refusing to overwrite existing evidence in {OUT}")


protected_paths = {
    "original_execution_snapshot": SNAPSHOT,
    "immutable_execution_copy": IMMUTABLE,
    "master_dataset": MASTER,
    "frozen_model": MODEL,
    "historical_membership": MEMBERSHIP,
    "membership_declarations": DECLARATIONS,
    "backtest_05_notebook": ROOT / "05_backtest.ipynb",
    "corporate_action_ledger": LEDGER,
    "execution_lineage": LINEAGE_PATH,
    "execution_sidecar": SIDECAR,
    "vendor_event_inventory": VENDOR_EVENTS,
    "security_identity_mapping": IDENTITY_MAP,
    "approved_exclusion_policy": EXCLUSIONS,
    "phase_a_universe": PHASE_A_UNIVERSE,
    "phase_a_gate": PHASE_A_GATE,
}
for file in PHASE_A.iterdir():
    if file.is_file():
        protected_paths[f"phase_a_artifact:{file.name}"] = file
hashes_before = {key: hash_if_file(path) for key, path in protected_paths.items()}

sidecar = json.loads(SIDECAR.read_text(encoding="utf-8"))
snapshot = pd.read_parquet(SNAPSHOT)
snapshot["Date"] = pd.to_datetime(snapshot["Date"], format="mixed", errors="coerce")
snapshot["Date_Key"] = snapshot["Date"].dt.strftime("%Y-%m-%d")
snapshot_hash = sha256_file(SNAPSHOT)
immutable_hash = hash_if_file(IMMUTABLE)

ledger = pd.read_csv(LEDGER, dtype=str, keep_default_na=False)
vendor_events = pd.read_csv(VENDOR_EVENTS, dtype=str, keep_default_na=False)
identity_map = pd.read_csv(IDENTITY_MAP, dtype=str, keep_default_na=False)
membership = pd.read_csv(MEMBERSHIP, dtype=str, keep_default_na=False)
declarations = pd.read_csv(DECLARATIONS, dtype=str, keep_default_na=False)
policy = pd.read_csv(EXCLUSIONS, dtype=str, keep_default_na=False)
phase_a_universe = pd.read_csv(PHASE_A_UNIVERSE, dtype=str, keep_default_na=False)
phase_a_gate = pd.read_csv(PHASE_A_GATE, dtype=str, keep_default_na=False)

member_sets = {}
for _, row in membership.iterrows():
    member_sets[row["period"]] = {
        text_value(value)
        for key, value in row.items()
        if key != "period" and text_value(value)
    }

declaration_map = {}
for _, row in declarations.iterrows():
    declaration_map[f'{row["year"]}_{row["review_period"]}'] = row.to_dict()

member_union_2026 = member_sets.get("2026_H1", set()) | member_sets.get("2026_H2", set())
ledger_symbols = set(ledger["Symbol"].astype(str))
ledger_member_symbols = ledger_symbols & member_union_2026
nonexcluded_members_2026 = member_union_2026 - set(policy["Symbol"].astype(str))
member_symbols_without_ledger = sorted(member_union_2026 - ledger_symbols)


# Task 1: retain every source row and add a conservative event-level assessment.
action_rows = []
for _, row in ledger.iterrows():
    record = row.to_dict()
    event_date = to_date_text(record.get("Date", ""))
    event_period = period_for_date(record.get("Date", ""))
    symbol = text_value(record.get("Symbol"))
    note = text_value(record.get("Evidence_Notes"))
    is_vendor = "Yahoo" in note or text_value(record.get("Event_ID")).startswith("VENDOR-")
    if is_vendor:
        publisher = "Yahoo Finance via yfinance.download (vendor; not official)"
        evidence_type = "VENDOR_EVENT_INVENTORY_ONLY"
    else:
        publisher = "Unspecified user-provided claim; no publisher recorded"
        evidence_type = "USER_CLAIM_WITHOUT_ATTACHED_SOURCE"
    in_union = symbol in member_union_2026
    action_rows.append({
        **record,
        "Event_Date_Normalized": event_date,
        "Candidate_Membership_Period": event_period,
        "Candidate_Member_On_Event_Date": (
            symbol in member_sets.get(event_period, set()) if event_period else ""
        ),
        "Candidate_Member_In_2026_H1": symbol in member_sets.get("2026_H1", set()),
        "Candidate_Member_In_2026_H2": symbol in member_sets.get("2026_H2", set()),
        "Candidate_Member_In_2026_Union": in_union,
        "Source_Publisher": publisher,
        "Evidence_Source_Type": evidence_type,
        "Evidence_URL": text_value(record.get("Official_Source")),
        "Local_Official_Source_Document_Found": False,
        "Recovery_Classification": "UNRESOLVED",
        "Classification_Rationale": (
            "The local ledger has no official source URL/document for this event. "
            "Vendor inventory and unattached user claims do not establish the action, "
            "terms, security identity, or effective date."
        ),
        "Potential_2026_Eligibility_Impact": (
            "BLOCKED_REVIEW_REQUIRED_FOR_2026_MEMBER_SYMBOL"
            if in_union else "NO_MATCH_IN_LOCAL_2026_MEMBERSHIP_UNION; membership itself is unverified"
        ),
        "Portfolio_Adjustment_Applied": False,
        "Evidence_Artifact_Path": str(LEDGER),
        "Evidence_Artifact_SHA256": sha256_file(LEDGER),
    })
corporate_action_recovery = pd.DataFrame(action_rows)
corporate_action_recovery.to_csv(OUT / "corporate_action_evidence_recovery.csv", index=False)

event_type_counts = ledger["Event_Type"].value_counts().to_dict()
unresolved_event_rows = int(corporate_action_recovery["Recovery_Classification"].eq("UNRESOLVED").sum())
member_event_rows = int(corporate_action_recovery["Candidate_Member_In_2026_Union"].astype(str).str.lower().isin(["true", "1"]).sum())
member_event_symbols = int(len(ledger_member_symbols))
source_url_count = int(ledger["Official_Source"].astype(str).str.strip().ne("").sum())
official_action_claims = int(corporate_action_recovery["Local_Official_Source_Document_Found"].sum())
identity_status_counts = identity_map["Evidence_Status"].value_counts().to_dict()

corporate_action_report = f"""# Corporate Action and Security Identity Recovery — Phase B

## Result

- Original ledger rows inspected: {len(ledger)}; rows individually classified `UNRESOLVED`: {unresolved_event_rows}.
- Original event symbols: {ledger['Symbol'].nunique()}; symbols intersecting the union of the local 2026_H1/H2 constituent files: {member_event_symbols}.
- Ledger rows whose symbols appear in that local 2026 membership union: {member_event_rows}.
- Official source URLs recorded in the ledger: {source_url_count}; locally available official event documents: {official_action_claims}.
- Portfolio-engine applications recorded: {int(ledger['Applied_By_Portfolio_Engine'].astype(str).str.lower().isin(['true','1']).sum())}.
- Event types recorded (not independently confirmed): `{json.dumps(event_type_counts, ensure_ascii=False)}`.

## 53-symbol count reconciliation

Phase A reported 53 unresolved, non-excluded 2026 member symbols. The local membership files contain 54 distinct symbols across 2026_H1 and 2026_H2; after the existing BANPU exclusion, 53 remain. The ledger contains events for {member_event_symbols} symbols in that 54-symbol union (including excluded BANPU); {len(member_symbols_without_ledger)} symbols have no ledger row: {', '.join(member_symbols_without_ledger)}. Thus the Phase A count of 53 is a universe-wide unresolved-status count, not 53 event-bearing symbols in the ledger. The local ledger supports {member_event_symbols} overlapping event symbols, and does not provide official negative confirmation for the symbols with no event row.

## Evidence and treatment

- The ledger's `Official_Source` field is blank for every row. The 136 vendor-origin records cite Yahoo Finance/yfinance in their notes; the five claim records do not attach a publisher URL or document.
- The candidate `Event_Type`, `Date`, security identifiers, ex/record/payment/trading/effective dates, cash amounts and ratios are reproduced from the ledger. They are not promoted to confirmed events.
- No price or quantity adjustment was applied. A price discontinuity or diagnostic factor is not treated as proof of a split.
- Event rows that overlap the local 2026 member set remain blocked for eligibility review; this does not assert membership was officially verified.
- No external sources were fetched or downloaded, per the preservation rule. Official event notices and security-identity evidence remain required.

## Identity findings

The local identity mapping contains {len(identity_map)} rows; status counts are `{json.dumps(identity_status_counts, ensure_ascii=False)}`. The mapping has no attached official URLs. BANPU/BPP identity, merger terms, fractional-share treatment, and post-event feature identity remain unresolved. Absence of an identity-mapping row for other symbols is not proof that no identity transition occurred.

## Output

`corporate_action_evidence_recovery.csv` preserves all 141 ledger rows and adds candidate membership context, source publisher, evidence URL, classification, rationale, and eligibility impact. Source ledger SHA-256: `{sha256_file(LEDGER)}`.
"""
(OUT / "corporate_action_recovery_report.md").write_text(corporate_action_report, encoding="utf-8")


# Task 2: audit only metadata already present in the workspace.
lineage = LINEAGE
source_rows = []


def add_source(field, value, status, evidence_path, interpretation):
    source_rows.append({
        "Field": field,
        "Observed_Value": value,
        "Status": status,
        "Evidence_Path": str(evidence_path) if evidence_path else "",
        "Evidence_SHA256": hash_if_file(evidence_path) if evidence_path and Path(evidence_path).is_file() else "",
        "Interpretation": interpretation,
        "External_Source_Fetched": False,
    })


add_source("Original provider", sidecar.get("source", lineage.get("source", "UNKNOWN")),
           "PASS_WITH_LIMITATIONS", SIDECAR,
           "Yahoo Finance via yfinance is recorded; this is vendor provenance, not exchange verification.")
add_source("yfinance version", sidecar.get("yfinance_version", "UNKNOWN"),
           "PASS_WITH_LIMITATIONS", SIDECAR, "Version is recorded in the sidecar.")
add_source("Downloaded/retrieval timestamp UTC", sidecar.get("downloaded_at_utc", "UNKNOWN"),
           "PASS_WITH_LIMITATIONS", SIDECAR, "Timestamp is recorded locally; it does not prove exchange accuracy.")
add_source("Requested start", sidecar.get("start", "UNKNOWN"), "PASS_WITH_LIMITATIONS", SIDECAR,
           "Start date is recorded in the sidecar.")
add_source("Requested end (exclusive)", sidecar.get("end_exclusive", "UNKNOWN"), "PASS_WITH_LIMITATIONS", SIDECAR,
           "End-exclusive date is recorded in the sidecar.")
add_source("Requested ticker count", sidecar.get("tickers_requested", "UNKNOWN"),
           "PASS_WITH_LIMITATIONS", SIDECAR,
           "A count is present, but the exact requested ticker list is absent.")
add_source("Returned ticker count", sidecar.get("tickers_returned", "UNKNOWN"),
           "PASS_WITH_LIMITATIONS", SIDECAR, "A count is present; it is not the original request list.")
add_source("Exact requested ticker list", lineage.get("requested_ticker_list", lineage.get("tickers", "UNKNOWN")),
           "BLOCKED", LINEAGE_PATH, "The lineage explicitly records UNKNOWN; do not infer from returned symbols.")
add_source("Interval", lineage.get("interval", "UNKNOWN"), "BLOCKED", LINEAGE_PATH,
           "The acquisition interval is explicitly UNKNOWN.")
add_source("group_by", lineage.get("group_by", "UNKNOWN"), "BLOCKED", LINEAGE_PATH,
           "The acquisition grouping is explicitly UNKNOWN.")
add_source("auto_adjust", sidecar.get("auto_adjust", lineage.get("auto_adjust", "UNKNOWN")),
           "PASS_WITH_LIMITATIONS", SIDECAR,
           "False is recorded; it does not independently prove raw exchange prices or eliminate historical adjustments.")
add_source("actions", sidecar.get("actions", lineage.get("actions", "UNKNOWN")),
           "PASS_WITH_LIMITATIONS", SIDECAR,
           "True is recorded; it does not authenticate the action terms.")
add_source("Snapshot path and SHA-256", f"{SNAPSHOT}; {snapshot_hash}", 
           "PASS" if snapshot_hash == PINNED_SNAPSHOT else "BLOCKED", LINEAGE_PATH,
           "Hash is pinned and matches the immutable copy; source response is not a separate archived artifact.")
add_source("Immutable-copy path and SHA-256", f"{IMMUTABLE}; {immutable_hash}",
           "PASS" if immutable_hash == PINNED_SNAPSHOT else "BLOCKED", IMMUTABLE,
           "The local immutable copy hash matches the pinned hash.")
add_source("Acquisition request/response manifest", "Not present; exact interval/group_by/ticker list unknown",
           "BLOCKED", LINEAGE_PATH, "The snapshot is hash-pinned, but the full vendor request/response provenance is incomplete.")
add_source("Exchange-authorized execution evidence", "Not present", "BLOCKED",
           RESULTS / "execution_price_integrity_audit.csv",
           "The existing audit identifies Yahoo Finance as the source and does not authorize it as exchange-verified execution data.")
add_source("Verified execution dataset", f"exists={VERIFIED.is_file()}",
           "BLOCKED", RESULTS / "verified_execution_data_status.json",
           "No verified execution parquet was created.")
add_source("Official corporate-action terms file", f"exists={OFFICIAL_ACTIONS.is_file()}",
           "BLOCKED", RESULTS / "verified_execution_data_status.json",
           "The required official actions file is absent.")
add_source("Official 2026 trading calendar", f"exists={OFFICIAL_CALENDAR.is_file()}",
           "BLOCKED", RESULTS / "verified_execution_data_status.json",
           "The required official calendar is absent.")
global_tick_path = RESULTS / "global_tick_basis_diagnostic.csv"
global_tick = pd.read_csv(global_tick_path) if global_tick_path.is_file() else pd.DataFrame()
add_source("GLOBAL historical tick-basis diagnostic",
           f"rows={len(global_tick)}; official action confirmation=0; no transformation applied in Phase B",
           "BLOCKED", global_tick_path,
           "Diagnostic alignment is not corporate-action evidence; GLOBAL is not asserted to have split.")
provenance = pd.DataFrame(source_rows)
provenance.to_csv(OUT / "execution_source_provenance_audit.csv", index=False)


missing_rows = []
for field in ["Open", "High", "Low", "Close"]:
    subset = snapshot.loc[snapshot[field].isna(), ["Date_Key", "Symbol", "Volume"]]
    for _, row in subset.iterrows():
        volume = row["Volume"]
        missing_rows.append({
            "Date": row["Date_Key"],
            "Symbol": text_value(row["Symbol"]),
            "Field": field,
            "Value_Status": "MISSING",
            "Volume": "" if pd.isna(volume) else volume,
            "Zero_Volume": bool(pd.notna(volume) and float(volume) == 0),
            "OHLCV_Row_Present_In_Snapshot": True,
            "Cause_Classification": "UNRESOLVED",
            "Classification_Rationale": (
                "No official trading-status, suspension, delisting, or identity-transition evidence "
                "is attached to this Date+Symbol+Field. No prices were imputed."
            ),
            "Source_Provider": sidecar.get("source", "UNKNOWN"),
            "Source_Artifact_Path": str(SNAPSHOT),
            "Source_Artifact_SHA256": snapshot_hash,
            "Official_Evidence_URL": "",
        })
completeness = pd.DataFrame(missing_rows).sort_values(["Date", "Symbol", "Field"]).reset_index(drop=True)
completeness.insert(0, "Missing_Record_ID", [f"OHLC-MISS-{i:04d}" for i in range(1, len(completeness) + 1)])
completeness.to_csv(OUT / "execution_price_completeness_audit.csv", index=False)

field_missing = snapshot[["Open", "High", "Low", "Close"]].isna().sum().to_dict()
missing_dates = int(completeness["Date"].nunique()) if len(completeness) else 0
missing_symbols = sorted(completeness["Symbol"].unique().tolist()) if len(completeness) else []
volume_on_missing_rows = snapshot.loc[
    snapshot[["Open", "High", "Low", "Close"]].isna().any(axis=1), "Volume"
]
missing_snapshot_row_count = int(snapshot[["Open", "High", "Low", "Close"]].isna().any(axis=1).sum())
execution_report = f"""# Execution Source and Price Completeness Recovery — Phase B

## Provenance recovered from existing files

- Provider recorded: `{sidecar.get('source', 'UNKNOWN')}`; yfinance version `{sidecar.get('yfinance_version', 'UNKNOWN')}`.
- Sidecar retrieval timestamp: `{sidecar.get('downloaded_at_utc', 'UNKNOWN')}` UTC.
- Requested range: `{sidecar.get('start', 'UNKNOWN')}` through `{sidecar.get('end_exclusive', 'UNKNOWN')}` (end exclusive).
- `auto_adjust={sidecar.get('auto_adjust', 'UNKNOWN')}` and `actions={sidecar.get('actions', 'UNKNOWN')}` are recorded.
- Requested and returned ticker counts are `{sidecar.get('tickers_requested', 'UNKNOWN')}` and `{sidecar.get('tickers_returned', 'UNKNOWN')}`; the exact requested ticker list remains UNKNOWN.
- `interval` and `group_by` remain UNKNOWN in the lineage. No inference was made from the shape of the parquet.
- Original snapshot SHA-256 `{snapshot_hash}`; immutable copy SHA-256 `{immutable_hash}`; pinned hash `{PINNED_SNAPSHOT}`.
- The snapshot and immutable copy are traceable as hash-identical local artifacts. A complete original request/response manifest and exchange-authorized execution source are not present.
- Yahoo data is not described as official SET execution data. `auto_adjust=False` alone does not establish an exchange-raw historical price basis.

## OHLC completeness

- Missing OHLC field-cells: {len(completeness)}; by field: `{json.dumps({k: int(v) for k,v in field_missing.items()})}`.
- Rows with at least one missing OHLC field: {missing_snapshot_row_count}; affected symbols: `{', '.join(missing_symbols)}`.
- Missing-field dates span {completeness['Date'].min() if len(completeness) else 'NONE'} through {completeness['Date'].max() if len(completeness) else 'NONE'}; distinct dates with missing fields: {missing_dates}.
- Volume observed on affected rows: `{volume_on_missing_rows.value_counts(dropna=False).to_dict()}`. This does not prove a holiday, suspension, or no-trading condition.
- Every missing item is listed at Date + Symbol + Field in `execution_price_completeness_audit.csv` and remains `UNRESOLVED`; no fill or price alteration was performed.
- Entirely absent expected market sessions cannot be identified without an official trading calendar. The local calendar file is absent.

## Price-basis diagnostics

The existing GLOBAL diagnostic contains {len(global_tick)} rows; the Phase A evidence reports zero official action confirmation. Recent SET cross-checks are limited to a few dates and do not verify historical price basis. No split is asserted and no adjusted prices were used to repair this snapshot in Phase B.

## Output

`execution_source_provenance_audit.csv` records each known/unknown acquisition field and its source file. `execution_price_completeness_audit.csv` contains one row per missing OHLC field-cell. No source was fetched or downloaded during this audit.
"""
(OUT / "execution_source_recovery_report.md").write_text(execution_report, encoding="utf-8")


# Task 3: audit membership claims and date alignment without fetching listed URLs.
membership_audit_rows = []
previous_members = None
for _, row in membership.iterrows():
    period = row["period"]
    current_members = member_sets.get(period, set())
    decl = declaration_map.get(period, {})
    source_url = text_value(decl.get("source_url", ""))
    publisher = publisher_from_url(source_url)
    for symbol in sorted(current_members | (previous_members or set())):
        if previous_members is None:
            transition = "BASELINE"
        elif symbol in current_members and symbol not in previous_members:
            transition = "ADDED_IN_LOCAL_FILE"
        elif symbol not in current_members and symbol in previous_members:
            transition = "REMOVED_IN_LOCAL_FILE"
        else:
            transition = "CONTINUING_IN_LOCAL_FILE"
        membership_audit_rows.append({
            "Period": period,
            "Effective_Date_Claim": text_value(decl.get("effective_date", "")),
            "Announcement_Date_Claim": text_value(decl.get("announcement_date", "")),
            "Symbol": symbol,
            "Present_In_Current_Local_File": symbol in current_members,
            "Present_In_Previous_Local_File": (
                symbol in previous_members if previous_members is not None else ""
            ),
            "Local_File_Transition": transition,
            "Current_File_Member_Row_Count": len(current_members),
            "Expected_Count_50_Check": len(current_members) == 50,
            "Recorded_Source_URL": source_url,
            "Recorded_Source_Publisher": publisher,
            "Source_URL_Retrieved": False,
            "Official_Membership_Content_Verified": False,
            "Audit_Status": "BLOCKED_SOURCE_DOCUMENT_NOT_RETRIEVED",
            "Evidence_Path": str(MEMBERSHIP),
            "Declaration_Path": str(DECLARATIONS),
            "Membership_SHA256": sha256_file(MEMBERSHIP),
            "Declaration_SHA256": sha256_file(DECLARATIONS),
            "Rationale": (
                "The local constituent/declaration files and URL pointer are recorded, but the primary "
                "document was not fetched; a count of 50 is not proof of membership."
            ),
        })
    previous_members = current_members
membership_audit = pd.DataFrame(membership_audit_rows)
membership_audit.to_csv(OUT / "membership_primary_evidence_audit.csv", index=False)

feature_path = MASTER
feature_dates = pd.read_parquet(feature_path, columns=["Date"])["Date"]
feature_dates = pd.to_datetime(feature_dates, format="mixed", errors="coerce").dropna()
feature_dates = sorted(feature_dates.loc[feature_dates.dt.year.eq(2026)].dt.normalize().unique())
phase_a_dates = phase_a_universe[["Date", "Execution_Date"]].drop_duplicates("Date")
phase_a_dates["Date_Key"] = phase_a_dates["Date"].map(to_date_text)
phase_a_dates["Phase_A_Execution_Date_Key"] = phase_a_dates["Execution_Date"].map(to_date_text)
phase_a_execution_map = dict(zip(phase_a_dates["Date_Key"], phase_a_dates["Phase_A_Execution_Date_Key"]))
snapshot_dates = set(snapshot["Date_Key"].dropna())
calendar_rows = []
for index, predictor_date in enumerate(feature_dates):
    predictor_key = pd.Timestamp(predictor_date).strftime("%Y-%m-%d")
    next_observed = (
        pd.Timestamp(feature_dates[index + 1]).strftime("%Y-%m-%d")
        if index + 1 < len(feature_dates) else ""
    )
    phase_a_exec = phase_a_execution_map.get(predictor_key, "")
    calendar_rows.append({
        "Predictor_Date": predictor_key,
        "Next_Observed_Feature_Date_Candidate": next_observed,
        "Phase_A_Execution_Date_Candidate": phase_a_exec,
        "Phase_A_Execution_Date_Matches_Next_Observed_Feature_Date": (
            phase_a_exec == next_observed if next_observed else False
        ),
        "Candidate_Execution_Date_In_Snapshot": phase_a_exec in snapshot_dates if phase_a_exec else False,
        "Official_Calendar_Path": str(OFFICIAL_CALENDAR),
        "Official_Calendar_File_Present": OFFICIAL_CALENDAR.is_file(),
        "Official_Session_Verified": False,
        "Date_Alignment_Status": "BLOCKED_NO_OFFICIAL_TRADING_CALENDAR",
        "Date_Source": str(feature_path),
        "Membership_Declaration_Path": str(DECLARATIONS),
        "Rationale": (
            "Next observed feature date is only a candidate alignment; it does not establish an official SET session."
        ),
    })
calendar_audit = pd.DataFrame(calendar_rows)
calendar_audit.to_csv(OUT / "trading_calendar_evidence_audit.csv", index=False)

period_url_count = int(declarations["source_url"].astype(str).str.strip().ne("").sum())
membership_report = f"""# Membership and Trading Calendar Recovery — Phase B

## Membership records

- Local membership periods audited: {len(membership)}; declaration rows: {len(declarations)}.
- The local membership file has 50 names in most periods; `2017_H1` has {len(member_sets.get('2017_H1', set()))}. Row counts are descriptive only and do not authenticate constituents.
- Declaration records contain {period_url_count}/{len(declarations)} URL pointers. The 2026_H1 and 2026_H2 pointers identify SET-hosted documents, but the documents were not retrieved; each membership/effective-date/transition row therefore remains `BLOCKED_SOURCE_DOCUMENT_NOT_RETRIEVED`.
- No historical membership or declaration data was changed.
- The union of the 2026_H1 and 2026_H2 local member lists contains {len(member_union_2026)} symbols. This is a candidate list, not a verified official membership universe.

## Calendar and alignment

- 2026 candidate predictor dates reviewed: {len(calendar_audit)}; date range `{calendar_audit['Predictor_Date'].min() if len(calendar_audit) else 'NONE'}` through `{calendar_audit['Predictor_Date'].max() if len(calendar_audit) else 'NONE'}`.
- The required official calendar `{OFFICIAL_CALENDAR}` is present: `{OFFICIAL_CALENDAR.is_file()}`.
- The recorded next-observed feature dates and Phase A execution-date candidates are listed in `trading_calendar_evidence_audit.csv`. These are not treated as official SET sessions.
- No generic weekday calendar was substituted. All date alignment remains blocked; the final predictor date has no next observed date in the local feature set.

## Output

`membership_primary_evidence_audit.csv` records each local membership name and each constituent change, with source URL pointer, publisher host, effective-date claim, and retrieval/verification status. `trading_calendar_evidence_audit.csv` records candidate date alignment and the absent official-calendar evidence.
"""
(OUT / "membership_calendar_recovery_report.md").write_text(membership_report, encoding="utf-8")


# Task 4: candidate-only reconstruction. Shared price-source and calendar blockers
# are not converted into per-symbol exclusions.
snapshot_lookup = {}
for _, row in snapshot.iterrows():
    key = (row["Date_Key"], text_value(row["Symbol"]))
    snapshot_lookup[key] = {
        "row_present": True,
        "open_close_complete": bool(pd.notna(row.get("Open")) and pd.notna(row.get("Close"))),
        "ohlc_complete": bool(all(pd.notna(row.get(field)) for field in ["Open", "High", "Low", "Close"])),
        "volume": row.get("Volume"),
    }

policy_ranges = {}
for _, row in policy.iterrows():
    policy_ranges.setdefault(text_value(row["Symbol"]), []).append(row)

universe_rows = []
for _, row in phase_a_universe.iterrows():
    predictor_date = to_date_text(row.get("Date", ""))
    execution_date = to_date_text(row.get("Execution_Date", ""))
    symbol = text_value(row.get("Symbol"))
    period = period_for_date(predictor_date)
    member_claim = symbol in member_sets.get(period, set())
    approved_excluded = False
    exclusion_reason = ""
    for policy_row in policy_ranges.get(symbol, []):
        start = to_date_text(policy_row.get("Exclusion_Start_Date", ""))
        end = to_date_text(policy_row.get("Exclusion_End_Date", ""))
        if predictor_date and (not start or predictor_date >= start) and (not end or predictor_date <= end):
            approved_excluded = True
            exclusion_reason = text_value(policy_row.get("Exclusion_Reason", ""))
            break
    execution = snapshot_lookup.get((execution_date, symbol), {})
    open_close_complete = bool(execution.get("open_close_complete", False))
    ohlc_complete = bool(execution.get("ohlc_complete", False))
    blockers = []
    if not member_claim:
        blockers.append("LOCAL_MEMBERSHIP_CLAIM_NOT_MATCHED")
    blockers.append("OFFICIAL_MEMBERSHIP_DOCUMENT_NOT_VERIFIED")
    blockers.append("SECURITY_IDENTITY_NOT_OFFICIALLY_VERIFIED")
    blockers.append("EXECUTION_PRICE_BASIS_NOT_EXCHANGE_VERIFIED")
    blockers.append("CORPORATE_ACTION_TERMS_OR_NEGATIVE_CONFIRMATION_MISSING")
    blockers.append("OFFICIAL_TRADING_CALENDAR_NOT_AVAILABLE")
    if not execution_date:
        blockers.append("NO_NEXT_OBSERVED_EXECUTION_DATE")
    if not open_close_complete:
        blockers.append("REQUIRED_EXECUTION_OPEN_OR_CLOSE_MISSING")
    if approved_excluded:
        blockers.append(f"APPROVED_EXCLUSION:{exclusion_reason}")
    tradable = bool(
        member_claim and not approved_excluded and open_close_complete
        and False  # No official membership, identity, price basis, action basis, or calendar evidence.
    )
    universe_rows.append({
        "Date": predictor_date,
        "Symbol": symbol,
        "Execution_Date_Candidate": execution_date,
        "Is_SET50_Member_In_Local_File": member_claim,
        "Is_Approved_Excluded": approved_excluded,
        "Exclusion_Reason": exclusion_reason,
        "Candidate_Execution_Row_Present": bool(execution.get("row_present", False)),
        "Candidate_Open_Close_Complete": open_close_complete,
        "Candidate_OHLC_Complete": ohlc_complete,
        "Official_Membership_Verified": False,
        "Security_Identity_Verified": False,
        "Execution_Price_Basis_Verified": False,
        "Corporate_Action_Basis_Verified": False,
        "Official_Execution_Date_Verified": False,
        "Is_Tradable": tradable,
        "Eligibility_Status": "BLOCKED",
        "Blocking_Requirements": ";".join(blockers),
        "Evidence_References": (
            f"{PHASE_A_UNIVERSE};{MEMBERSHIP};{DECLARATIONS};{SNAPSHOT};"
            f"{LEDGER};{IDENTITY_MAP};{OFFICIAL_CALENDAR}"
        ),
    })
phase_b_universe = pd.DataFrame(universe_rows)
phase_b_universe.to_csv(OUT / "tradable_universe_2026_phase_B.csv", index=False)

excluded_rows = []
for _, row in policy.iterrows():
    symbol = text_value(row.get("Symbol"))
    rows = phase_b_universe.loc[phase_b_universe["Symbol"].eq(symbol)]
    record = row.to_dict()
    record.update({
        "Candidate_Member_Date_Rows": int(len(rows)),
        "Candidate_Member_Date_Rows_Excluded": int(rows["Is_Approved_Excluded"].sum()),
        "Tradable_Rows": int(rows["Is_Tradable"].sum()),
        "Policy_Preserved_Not_Modified": True,
        "Evidence_Status": text_value(row.get("Decision_Status", "EXISTING_POLICY")),
        "Source_Policy_Path": str(EXCLUSIONS),
        "Source_Policy_SHA256": sha256_file(EXCLUSIONS),
        "Note": "Existing approved exclusion only; unresolved shared price/calendar issues are blockers, not expanded exclusions.",
    })
    excluded_rows.append(record)
phase_b_exclusions = pd.DataFrame(excluded_rows)
phase_b_exclusions.to_csv(OUT / "execution_excluded_symbols_phase_B.csv", index=False)

coverage_rows = []
for date, group in phase_b_universe.groupby("Date", sort=True):
    member_count = int(group["Is_SET50_Member_In_Local_File"].sum())
    excluded_count = int((group["Is_SET50_Member_In_Local_File"] & group["Is_Approved_Excluded"]).sum())
    denominator = max(member_count - excluded_count, 0)
    data_count = int((group["Candidate_Open_Close_Complete"] & ~group["Is_Approved_Excluded"]).sum())
    tradable_count = int(group["Is_Tradable"].sum())
    coverage_rows.append({
        "Predictor_Date": date,
        "Local_SET50_Member_Count": member_count,
        "Approved_Excluded_Member_Count": excluded_count,
        "Candidate_Open_Close_Complete_Count_NonExcluded": data_count,
        "Candidate_Open_Close_Coverage_NonExcluded": data_count / denominator if denominator else 0.0,
        "Official_Membership_Verified_Count": 0,
        "Official_Price_Basis_Verified_Count": 0,
        "Official_Calendar_Aligned_Count": 0,
        "Verified_Tradable_Count": tradable_count,
        "Verified_Tradable_Coverage": tradable_count / denominator if denominator else 0.0,
        "Official_Calendar_Status": "BLOCKED",
        "Coverage_Status": "BLOCKED_ZERO_VERIFIED_TRADABLE_ROWS",
        "Source_Path": str(PHASE_A_UNIVERSE),
    })
coverage = pd.DataFrame(coverage_rows)
coverage.to_csv(OUT / "tradable_universe_coverage_phase_B.csv", index=False)


# Task 5: prove preservation and publish a fail-closed gate.
hashes_after = {key: hash_if_file(path) for key, path in protected_paths.items()}
protected_unchanged = all(
    hashes_before.get(key) and hashes_before.get(key) == hashes_after.get(key)
    for key in hashes_before
)
snapshot_and_copy_pinned = (
    hashes_after.get("original_execution_snapshot") == PINNED_SNAPSHOT
    and hashes_after.get("immutable_execution_copy") == PINNED_SNAPSHOT
)
model_unchanged = hashes_after.get("frozen_model") == PINNED_MODEL
phase_a_unchanged = all(
    hashes_before[key] == hashes_after[key]
    for key in hashes_before if key.startswith("phase_a_artifact:")
)
no_excluded_tradable = not phase_b_universe.loc[
    phase_b_universe["Is_Tradable"], "Symbol"
].isin(policy["Symbol"]).any()
all_tradable_proof = bool(
    len(phase_b_universe.loc[phase_b_universe["Is_Tradable"]]) > 0
    and phase_b_universe.loc[phase_b_universe["Is_Tradable"], [
        "Official_Membership_Verified", "Security_Identity_Verified",
        "Execution_Price_Basis_Verified", "Corporate_Action_Basis_Verified",
        "Official_Execution_Date_Verified", "Candidate_Open_Close_Complete",
    ]].all(axis=None)
)
unit_tests = pd.read_csv(PHASE_A / "unit_test_report.csv", dtype=str, keep_default_na=False)
unit_tests_pass = len(unit_tests) == 17 and unit_tests["Status"].eq("PASS").all()
gate_rows = [
    ("PHASE_B_OVERALL", "BLOCKED", "No verified tradable rows; critical evidence remains unresolved."),
    ("Phase A baseline and artifacts preserved", "PASS" if phase_a_unchanged else "BLOCKED",
     f"Phase A directory={PHASE_A}; all pre-existing files unchanged={phase_a_unchanged}."),
    ("Original and immutable snapshot hashes remain pinned", "PASS" if snapshot_and_copy_pinned else "BLOCKED",
     f"original={hashes_after.get('original_execution_snapshot')}; immutable={hashes_after.get('immutable_execution_copy')}; pinned={PINNED_SNAPSHOT}."),
    ("Master, frozen model, membership, declarations and 05 notebook unchanged", "PASS" if protected_unchanged and model_unchanged else "BLOCKED",
     f"protected_hashes_unchanged={protected_unchanged}; frozen_model_pinned={model_unchanged}."),
    ("All 141 ledger rows individually classified without unsupported confirmation", "PASS" if unresolved_event_rows == len(ledger) else "BLOCKED",
     f"rows={len(ledger)}; UNRESOLVED={unresolved_event_rows}; official URLs={source_url_count}; no action applied."),
    ("Official corporate-action terms and security identity verified for member events", "BLOCKED",
     f"member-event rows={member_event_rows}; matching member symbols={member_event_symbols}; official action evidence={official_action_claims}; identity evidence statuses={identity_status_counts}."),
    ("Existing execution provenance captured", "PASS_WITH_LIMITATIONS",
     f"provider, timestamp, date range, auto_adjust and actions recorded; interval/group_by/exact requested ticker list UNKNOWN."),
    ("Complete acquisition request manifest and exchange-authorized price basis available", "BLOCKED",
     "Request fields remain UNKNOWN and the source is Yahoo Finance via yfinance, not exchange-verified."),
    ("All missing OHLC causes reconciled to official trading status", "BLOCKED",
     f"missing field-cells={len(completeness)}; by field={field_missing}; affected rows={missing_snapshot_row_count}; causes unresolved."),
    ("Primary membership documents support effective dates and transitions", "BLOCKED",
     f"periods={len(membership)}; URLs recorded={period_url_count}, but documents not retrieved and membership content not verified."),
    ("Official SET trading calendar and predictor-to-execution alignment verified", "BLOCKED",
     f"candidate predictor dates={len(calendar_audit)}; official calendar present={OFFICIAL_CALENDAR.is_file()}."),
    ("No approved excluded symbol appears as tradable", "PASS" if no_excluded_tradable else "BLOCKED",
     f"tradable rows={int(phase_b_universe['Is_Tradable'].sum())}; exclusion symbols={policy['Symbol'].tolist()}."),
    ("Every tradable row has all required evidence", "PASS" if all_tradable_proof else "BLOCKED",
     f"tradable rows={int(phase_b_universe['Is_Tradable'].sum())}; zero-row universe cannot satisfy this validation."),
    ("Verified tradable universe is non-empty", "PASS" if int(phase_b_universe["Is_Tradable"].sum()) > 0 else "BLOCKED",
     f"candidate rows={len(phase_b_universe)}; verified tradable rows={int(phase_b_universe['Is_Tradable'].sum())}."),
    ("Existing synthetic no-lookahead and execution regressions remain valid", "PASS" if unit_tests_pass else "BLOCKED",
     f"Phase A regression tests={len(unit_tests)}; passed={int(unit_tests['Status'].eq('PASS').sum())}; failed={int(unit_tests['Status'].eq('FAIL').sum())}."),
    ("No external data download, model fit, or 63-set backtest performed", "PASS",
     "This Phase B builder only read local files; no downloader, model fitting, or backtest runner was invoked."),
]
gate = pd.DataFrame(gate_rows, columns=["Requirement", "Status", "Detail"])
gate.insert(2, "Evidence_Path", str(OUT))
gate.to_csv(OUT / "phase_B_gate.csv", index=False)

blockers = [
    ("B-CA-01", "BLOCKED", "Corporate actions", f"{len(ledger)} unresolved ledger rows; {member_event_rows} event rows overlap candidate 2026 membership; no official source URL/document.", "Official SET/issuer/SEC notice for each event with security identifier, terms, and effective/ex/record/payment/trading dates; reconcile any affected portfolio quantities/cash.", "Member-event symbols remain ineligible until their event/negative evidence is resolved."),
    ("B-ID-01", "BLOCKED", "Security identity", f"Identity map has {len(identity_map)} rows with statuses {identity_status_counts}; no attached official URLs; two merger claims remain unsupported.", "Official issuer/SET/SEC identity and conversion documents, including fractional-share settlement; verified feature identity handling for any transition.", "Identity and share-count continuity cannot be proven."),
    ("B-EX-01", "BLOCKED", "Execution provenance", "Provider/timestamp/range/settings partially recorded; exact ticker list, interval, and group_by are UNKNOWN; no exchange-authorized source.", "Complete immutable acquisition manifest or authorized/exchange-verified OHLC source with documented date range and request semantics.", "No eligible sample can claim verified execution prices."),
    ("B-EX-02", "BLOCKED", "Missing execution data", f"{len(completeness)} missing OHLC field-cells across {missing_snapshot_row_count} BANPU rows; all causes unresolved.", "Official trading-status evidence and authorized OHLC for each affected date/field, or documented evidence the date was not an official session. No forward/backfill.", "BANPU is already excluded; missing rows remain unresolved and cannot be inferred as holidays/suspensions."),
    ("B-EX-03", "BLOCKED", "Historical price basis", f"Yahoo vendor snapshot is not exchange-verified; GLOBAL diagnostic has {len(global_tick)} rows with no official action confirmation.", "Exchange-authorized raw execution/valuation basis plus official corporate-action reconciliation for affected symbols/dates.", "Price continuity is not established market-wide; excluding GLOBAL alone does not resolve it."),
    ("B-MEM-01", "BLOCKED", "Membership effective dates and transitions", f"{len(membership)} period rows and {period_url_count} URL pointers exist, but official primary documents were not retrieved; 2017_H1 local row count is {len(member_sets.get('2017_H1', set()))}.", "Primary SET constituents/review documents for each period and validation of every effective date and constituent addition/removal against the local file.", "Membership remains a candidate claim, not verified evidence."),
    ("B-CAL-01", "BLOCKED", "Official trading calendar and date alignment", f"Required calendar file exists={OFFICIAL_CALENDAR.is_file()}; {len(calendar_audit)} next-observed date candidates are not official sessions.", "Official SET 2026 trading-session calendar and mapping of each predictor date to the correct execution session.", "Target-date alignment cannot be verified; do not substitute weekdays or next observed vendor rows."),
    ("B-UNIV-01", "BLOCKED", "Non-empty verified universe", f"10,500 candidate member-date rows; 0 rows satisfy the complete evidence criteria.", "Resolve source, membership/calendar, identity, corporate-action, and execution-price blockers; then reconstruct without relaxing criteria.", "Research backtest gate must remain closed; zero-row sample remains BLOCKED."),
]
blocker_register = pd.DataFrame(blockers, columns=[
    "Blocker_ID", "Status", "Scope", "Observed_Evidence",
    "Evidence_Required_To_Clear", "Eligibility_Impact",
])
blocker_register.to_csv(OUT / "phase_B_blocker_register.csv", index=False)

pass_count = int(gate["Status"].eq("PASS").sum())
limitation_count = int(gate["Status"].eq("PASS_WITH_LIMITATIONS").sum())
blocked_count = int(gate["Status"].eq("BLOCKED").sum())
phase_a_baseline = phase_a_gate.loc[
    phase_a_gate["Requirement"].eq("PHASE_A_OVERALL"), "Status"
].iloc[0]
summary = f"""# Phase B Evidence Recovery — Summary

## Outcome

**Phase B: BLOCKED. Research Backtest Gate remains CLOSED.** No new official evidence was available locally, and the no-download constraint was honored. No 63-combination backtest, model fit, or source download was performed.

Phase A's saved result was not changed: baseline status `{phase_a_baseline}` (12 PASS / 4 BLOCKED criteria as supplied), verified tradable rows 0, candidate data coverage 99.52%, verified coverage 0.00%. All Phase A artifacts were hash-checked before and after this work.

Phase B gate rows: {pass_count} PASS, {limitation_count} PASS_WITH_LIMITATIONS, {blocked_count} BLOCKED (includes the overall roll-up).

## Findings

1. **Corporate actions / identity:** All {len(ledger)} ledger events were inspected and remain `UNRESOLVED`; the ledger has no official source URLs, and no event was applied. The 2026 constituent union contains {len(member_union_2026)} symbols. {member_event_symbols} ledger symbols overlap that union ({member_event_rows} event rows); the no-event symbols are {', '.join(member_symbols_without_ledger)}. Phase A's 53 unresolved non-excluded member-symbol count is a status count, not 53 event-bearing symbols. All {unresolved_event_rows} event rows and this discrepancy are preserved in the recovery output.
2. **Execution provenance:** The existing sidecar records Yahoo Finance/yfinance {sidecar.get('yfinance_version', 'UNKNOWN')}, retrieval time `{sidecar.get('downloaded_at_utc', 'UNKNOWN')}`, requested range `{sidecar.get('start', 'UNKNOWN')}` to `{sidecar.get('end_exclusive', 'UNKNOWN')}` exclusive, `auto_adjust={sidecar.get('auto_adjust', 'UNKNOWN')}`, and `actions={sidecar.get('actions', 'UNKNOWN')}`. The exact ticker list, interval, and group_by remain UNKNOWN. The source is not exchange-verified.
3. **Missing OHLC:** {len(completeness)} field-cells are missing: `{json.dumps({k: int(v) for k,v in field_missing.items()})}` across {missing_snapshot_row_count} BANPU rows. All remain unresolved; vendor row presence/volume does not establish holiday, no-trading, or suspension.
4. **Membership/calendar:** {len(membership)} period rows and {period_url_count} recorded URL pointers were inspected. URLs were not fetched; membership content and transitions remain unverified. The official 2026 calendar file is absent; the {len(calendar_audit)} observed-date alignments are candidates only.
5. **Universe:** {len(phase_b_universe)} candidate member-date rows were evaluated; {int(phase_b_universe['Is_Tradable'].sum())} are verified tradable. Existing BANPU/GLOBAL exclusions are preserved; other securities were not blanket-excluded to mask shared-source blockers.

## Protected-file integrity

Original snapshot SHA-256: `{hashes_after.get('original_execution_snapshot')}`  
Immutable copy SHA-256: `{hashes_after.get('immutable_execution_copy')}`  
Frozen model SHA-256: `{hashes_after.get('frozen_model')}`  
Master dataset, membership, declaration, 05 backtest notebook, Phase A files, and source ledgers unchanged: `{protected_unchanged}`.

No source data was downloaded; no snapshot/master/membership/model was modified.

## Exact remaining blockers

"""
for _, blocker in blocker_register.iterrows():
    summary += (
        f"- **{blocker['Blocker_ID']} — {blocker['Scope']} ({blocker['Status']}):** "
        f"{blocker['Observed_Evidence']} Evidence still needed: {blocker['Evidence_Required_To_Clear']}\n"
    )
summary += f"""
## Deliverables

All Phase B outputs are in `{OUT}`:

- `corporate_action_evidence_recovery.csv`
- `corporate_action_recovery_report.md`
- `execution_source_provenance_audit.csv`
- `execution_price_completeness_audit.csv`
- `execution_source_recovery_report.md`
- `membership_primary_evidence_audit.csv`
- `trading_calendar_evidence_audit.csv`
- `membership_calendar_recovery_report.md`
- `tradable_universe_2026_phase_B.csv`
- `execution_excluded_symbols_phase_B.csv`
- `tradable_universe_coverage_phase_B.csv`
- `phase_B_gate.csv`
- `phase_B_blocker_register.csv`

The builder and `phase_B_manifest.json` are also retained for reproducibility and integrity evidence.
"""
(OUT / "phase_B_evidence_summary.md").write_text(summary, encoding="utf-8")

output_files = sorted(file for file in OUT.iterdir() if file.is_file() and file.name != "phase_B_manifest.json")
manifest = {
    "phase": "B",
    "status": "BLOCKED",
    "created_utc": pd.Timestamp.now(tz="UTC").isoformat(),
    "workspace": str(OUT),
    "phase_a_workspace": str(PHASE_A),
    "phase_a_result_preserved": phase_a_unchanged,
    "phase_a_baseline_status": phase_a_baseline,
    "source_files_read_only": True,
    "external_download_performed": False,
    "yfinance_redownload_performed": False,
    "model_fit_performed": False,
    "backtest_63_sets_executed": False,
    "candidate_member_date_rows": int(len(phase_b_universe)),
    "verified_tradable_rows": int(phase_b_universe["Is_Tradable"].sum()),
    "corporate_action_rows": int(len(ledger)),
    "corporate_action_rows_unresolved": unresolved_event_rows,
    "missing_ohlc_field_cells": int(len(completeness)),
    "protected_hashes_before": hashes_before,
    "protected_hashes_after": hashes_after,
    "output_hashes": {file.name: sha256_file(file) for file in output_files},
}
(OUT / "phase_B_manifest.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print("Phase B output directory:", OUT)
print("Gate counts:", {"PASS": pass_count, "PASS_WITH_LIMITATIONS": limitation_count, "BLOCKED": blocked_count})
print("Corporate action rows:", len(corporate_action_recovery), "all unresolved:", unresolved_event_rows)
print("Missing OHLC field-cells:", len(completeness), "by field:", field_missing)
print("Membership periods:", len(membership), "calendar candidate dates:", len(calendar_audit))
print("Candidate member-date rows:", len(phase_b_universe), "verified tradable rows:", int(phase_b_universe["Is_Tradable"].sum()))
print("Protected hashes unchanged:", protected_unchanged, "Phase A unchanged:", phase_a_unchanged)
print("Downloads/backtests:", False, False)
