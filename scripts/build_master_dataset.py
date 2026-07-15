"""
build_master_dataset.py — Dataset v1.2 dedicated freeze step
============================================================
This script is the sole authorised writer of data/processed/master_dataset.parquet.
It keeps the raw price/VIX/macro/sentiment merge outside Notebook 05, as required by
dataset_contract.md, and produces the machine-readable validation report alongside the
frozen parquet.

Dataset v1.2 promotes the three explicit occurrence-count fields created by Notebook 03:
``n_health_catalogue_events``, ``n_labour_catalogue_events``, and
``n_other_catalogue_events``. Unlike the frozen v1.0/v1.1 occurrence proxies, these fields
count catalogue rows independently of sentiment polarity, so a neutral FinBERT score is
not mistaken for "no event". Counts are aligned to the existing SPY trading-day calendar;
the validation report separately records events dated on non-trading days.

One documented v1.0 column group is NOT reconstructed here: QQQ/GLD/TLT. No data/raw file
for these exists in this environment (dataset_version.md lists them as "not used in any
RQ1-RQ3 result yet"), so they are omitted rather than fabricated. This is a scope note,
not a silent gap -- logged in the same decision-log entry.

Usage:
    python3 scripts/build_master_dataset.py
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"

SPLIT_BOUNDARY = pd.Timestamp("2022-12-30")  # train <= this date, test > this date
DATASET_VERSION = "1.2"
FREEZE_DATE = "2026-07-14"

print("Loading inputs...")
ohlcv = pd.read_parquet(RAW / "spy_ohlcv.parquet")
vix = pd.read_parquet(RAW / "vix.parquet")
macro = pd.read_parquet(RAW / "macro_indicators.parquet")
daily_sentiment = pd.read_parquet(PROC / "daily_sentiment.parquet").set_index("date")
gdelt = pd.read_parquet(PROC / "gdelt_daily_risk.parquet").set_index("date")

for df in (ohlcv, vix, macro, daily_sentiment, gdelt):
    df.index = pd.to_datetime(df.index).normalize()

trading_days = ohlcv.index

# ── Adjusted OHLC (dataset_version.md: "SPY OHLC, adjusted") ──────────────────
# spy_ohlcv's own adj_close is confirmed identical to spy_returns.parquet's spy_close
# (0.0 max abs diff, verified 2026-07-13). Scale open/high/low by the same per-day
# adjustment ratio so all four price columns share one consistent adjustment basis --
# using raw high/low alongside an adjusted close would distort bb_width/bb_position/
# intraday_range in 05_feature_engineering.ipynb, especially for early (2015-16) dates
# where the cumulative dividend adjustment is largest.
adj_ratio = ohlcv["adj_close"] / ohlcv["close"]
master = pd.DataFrame(index=trading_days)
master.index.name = "date"
master["spy_open"] = ohlcv["open"] * adj_ratio
master["spy_high"] = ohlcv["high"] * adj_ratio
master["spy_low"] = ohlcv["low"] * adj_ratio
master["spy_close"] = ohlcv["adj_close"]
master["spy_volume"] = ohlcv["volume"]

master["log_return"] = np.log(master["spy_close"] / master["spy_close"].shift(1))
master["fwd_return_1d"] = master["log_return"].shift(-1)

# ── VIX ─────────────────────────────────────────────────────────────────────
master["vix"] = vix["vix_close"].reindex(trading_days)

# ── Macro (forward-filled onto the SPY trading calendar) ──────────────────────
macro_cols = ["fed_funds_rate", "cpi", "unemployment", "treasury_10y",
              "treasury_2y", "mfg_employment", "yield_spread"]
macro_aligned = macro.reindex(trading_days).ffill()
for col in macro_cols:
    master[col] = macro_aligned[col]

# ── Sentiment/event (0.0 fill = "no tagged event that day", per dataset_version.md) ──
sent_cols = ["energy", "geopolitical", "health", "labour", "monetary", "other",
             "regulatory", "trade", "overall_mean_sentiment", "overall_net_sentiment",
             "total_events"]
for col in sent_cols:
    master[col] = daily_sentiment[col].reindex(trading_days).fillna(0.0)

# ── Explicit category occurrence counts (Dataset v1.2) ──────────────────────
# These are direct catalogue-row counts from Notebook 03, not sentiment proxies.
# Reindexing follows the established same-trading-day merge policy. Events dated on
# weekends/market holidays are not silently treated as trading-day events; their totals
# are quantified separately in the validation report below.
occurrence_cols = [
    "n_health_catalogue_events",
    "n_labour_catalogue_events",
    "n_other_catalogue_events",
]
missing_occurrence_cols = sorted(set(occurrence_cols) - set(daily_sentiment.columns))
assert not missing_occurrence_cols, (
    f"Notebook 03 output is missing Dataset v1.2 fields: {missing_occurrence_cols}"
)
for col in occurrence_cols:
    master[col] = daily_sentiment[col].reindex(trading_days).fillna(0).astype("int64")

# ── GDELT (now a full 4,018-day continuous series, not a 5-day sample -- see
#    10_decision_log.md, 2026-07-13). Merged directly from gdelt_daily_risk.parquet
#    rather than through daily_sentiment.parquet, since the latter only has rows for
#    days with a catalogued APP/FOMC event and would otherwise leave GDELT sparse on
#    the majority of calendar days where real GDELT data exists but no APP/FOMC event
#    happened to occur that day. ──────────────────────────────────────────────
gdelt_cols = ["gdelt_risk_score", "gdelt_mean_tone", "gdelt_n_events"]
for col in gdelt_cols:
    master[col] = gdelt[col].reindex(trading_days).fillna(0.0)

# ── Split (authoritative boundary per dataset_contract.md term 5) ─────────────
master = master.reset_index()
master["split"] = np.where(master["date"] <= SPLIT_BOUNDARY, "train", "test")

# ── Validation (mirrors dataset_version.md's v1.0 validation report) ──────────
print("\nValidation:")
n_dupe_dates = int(master["date"].duplicated().sum())
is_monotonic = bool(master["date"].is_monotonic_increasing)
gaps = master["date"].diff().dt.days.dropna()
max_gap = int(gaps.max())
n_big_gaps = int((gaps > 5).sum())
non_boundary_missing = int(
    master.drop(columns=["log_return", "fwd_return_1d"]).isna().sum().sum()
)
leakage_check = master["fwd_return_1d"].iloc[:-1].values == master["log_return"].shift(-1).iloc[:-1].values
leakage_mismatches = int((~leakage_check).sum())
last_row_fwd_is_nan = bool(pd.isna(master["fwd_return_1d"].iloc[-1]))
occurrence_values_valid = bool(
    master[occurrence_cols].notna().all().all()
    and (master[occurrence_cols] >= 0).all().all()
    and all(pd.api.types.is_integer_dtype(master[col]) for col in occurrence_cols)
)

all_calendar_occurrence_totals = {
    col: int(daily_sentiment[col].sum()) for col in occurrence_cols
}
trading_day_occurrence_totals = {
    col: int(daily_sentiment[col].reindex(trading_days).fillna(0).sum())
    for col in occurrence_cols
}
non_trading_day_occurrence_totals = {
    col: all_calendar_occurrence_totals[col] - trading_day_occurrence_totals[col]
    for col in occurrence_cols
}
master_occurrence_totals = {col: int(master[col].sum()) for col in occurrence_cols}
occurrence_reconciliation_mismatches = {
    col: {
        "expected_on_trading_days": trading_day_occurrence_totals[col],
        "actual_in_master": master_occurrence_totals[col],
    }
    for col in occurrence_cols
    if trading_day_occurrence_totals[col] != master_occurrence_totals[col]
}

checks = {
    "duplicate_dates": n_dupe_dates,
    "date_monotonic_increasing": is_monotonic,
    "max_gap_calendar_days": max_gap,
    "gaps_gt_5_days": n_big_gaps,
    "missing_outside_two_boundary_rows": non_boundary_missing,
    "leakage_check_mismatches": leakage_mismatches,
    "last_row_fwd_return_is_nan": last_row_fwd_is_nan,
    "occurrence_values_non_negative_non_null_integer": occurrence_values_valid,
    "occurrence_reconciliation_mismatches": occurrence_reconciliation_mismatches,
}
for k, v in checks.items():
    print(f"  {k:<38}: {v}")

assert n_dupe_dates == 0, "Duplicate dates found"
assert is_monotonic, "Dates not monotonic increasing"
assert non_boundary_missing == 0, f"Unexpected missing values: {non_boundary_missing}"
assert leakage_mismatches == 0, "fwd_return_1d != log_return.shift(-1) leakage check failed"
assert last_row_fwd_is_nan, "Last row fwd_return_1d should be NaN (no future data)"
assert occurrence_values_valid, "Occurrence counts must be non-negative, non-null integers"
assert not occurrence_reconciliation_mismatches, (
    f"Occurrence-count reconciliation failed: {occurrence_reconciliation_mismatches}"
)
print("\n✓ All validation checks passed")

print(f"\nRows: {len(master):,}  Columns: {master.shape[1]}")
print(f"Date range: {master['date'].min().date()} -> {master['date'].max().date()}")
print(f"Split counts:\n{master['split'].value_counts().to_string()}")

out_path = PROC / "master_dataset.parquet"
master.to_parquet(out_path, index=False)
print(f"\n✓ Saved {out_path.relative_to(ROOT)} ({len(master):,} rows x {master.shape[1]} cols)")

validation_report = {
    "dataset_version": DATASET_VERSION,
    "freeze_date": FREEZE_DATE,
    "validation_status": "PASS",
    "artifact": str(out_path.relative_to(ROOT)),
    "artifact_sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
    "source_artifacts": {
        "daily_sentiment": {
            "path": str((PROC / "daily_sentiment.parquet").relative_to(ROOT)),
            "sha256": hashlib.sha256((PROC / "daily_sentiment.parquet").read_bytes()).hexdigest(),
        },
        "gdelt_daily_risk": {
            "path": str((PROC / "gdelt_daily_risk.parquet").relative_to(ROOT)),
            "sha256": hashlib.sha256((PROC / "gdelt_daily_risk.parquet").read_bytes()).hexdigest(),
        },
    },
    "shape": {"rows": int(master.shape[0]), "columns": int(master.shape[1])},
    "columns": list(master.columns),
    "date_range": {
        "start": master["date"].min().date().isoformat(),
        "end": master["date"].max().date().isoformat(),
    },
    "split_counts": {
        key: int(value) for key, value in master["split"].value_counts().items()
    },
    "checks": checks,
    "occurrence_counts": {
        "all_catalogue_calendar_dates": all_calendar_occurrence_totals,
        "included_spy_trading_dates": trading_day_occurrence_totals,
        "excluded_non_trading_dates": non_trading_day_occurrence_totals,
        "master_dataset_totals": master_occurrence_totals,
        "alignment_policy": "same calendar date on the SPY trading-day index; no next-session reassignment",
    },
}
validation_path = PROC / "master_dataset_validation.json"
validation_path.write_text(json.dumps(validation_report, indent=2) + "\n", encoding="utf-8")
print(f"✓ Saved {validation_path.relative_to(ROOT)} (validation_status=PASS)")
print("Note: QQQ/GLD/TLT columns from the documented v1.0 schema are NOT included --")
print("no data/raw source exists for them in this environment (see script docstring).")
