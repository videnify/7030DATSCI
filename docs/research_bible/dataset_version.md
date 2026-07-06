# Dataset Version — `master_dataset.parquet` v1.0

**Purpose:** The frozen, canonical, cleaned-and-merged base dataset for the project — one row per SPY trading day, combining price, volatility, macro, and daily event/sentiment signal, prior to any feature engineering (lags, rolling windows, technical indicators). This is the Phase-2 "clean + merge" artefact the original 10-phase spec calls for, which the current 8-notebook pipeline had previously only ever reconstructed in-memory inside `05_feature_engineering.ipynb` rather than materialising as its own file. Freezing it here gives every downstream notebook, and any future re-run, a single verified source of truth to build features from.
**Owner:** Senior Data Science Architect (build/schema), Research Statistician (validation sign-off).
**Dependencies:** `data/raw/spy_ohlcv.parquet`, `prices.parquet`, `vix.parquet`, `macro_indicators.parquet`; `data/processed/daily_sentiment.parquet`. Upstream of `05_feature_engineering.ipynb` / `model_features.parquet` — feature engineering should read from `master_dataset.parquet` going forward rather than re-deriving the merge independently.
**Update Frequency:** Frozen. Any change requires a new version (`v1.1`, `v2.0`, etc.) with a new dated entry below and a corresponding `10_decision_log.md` entry — never silently overwrite a frozen version.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.1 (Data Sources) "final merged dataset" description and the reproducibility appendix.

---

## Version history

| Version | Date | Change | Approved by |
|---------|------|--------|-------------|
| 1.0 | 2026-07-04 | Initial freeze | 🟡 Pending Project Director review |

---

## Schema (34 columns, 2,765 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime64 | SPY trading day, calendar index for the whole dataset |
| `spy_close`, `spy_open`, `spy_high`, `spy_low` | float64 | SPY OHLC, adjusted |
| `spy_volume` | int64 | SPY daily volume |
| `QQQ`, `GLD`, `TLT` | float64 | Optional cross-asset closes — carried for the not-yet-scoped cross-asset check (`11_limitations.md` L8); not used in any RQ1–RQ3 result yet |
| `vix` | float64 | VIX daily close |
| `fed_funds_rate`, `cpi`, `unemployment`, `treasury_10y`, `treasury_2y`, `mfg_employment`, `yield_spread` | float64 | Macro indicators, forward-filled onto the SPY trading calendar from their native (often lower-frequency) release schedule |
| `energy`, `geopolitical`, `health`, `labour`, `monetary`, `other`, `regulatory`, `trade` | float64 | Daily mean sentiment by event category — predominantly FinBERT-sourced (official primary sentiment engine, Sentiment Engine Freeze v1.0; lexicon scorer used only as fallback/historical method — see `10_decision_log.md`); 0.0 on days with no events of that category — see Missing Value Policy below |
| `overall_mean_sentiment`, `overall_net_sentiment` | float64 | Daily aggregate sentiment across all categories |
| `total_events` | float64 | Count of tagged events that day, all categories |
| `gdelt_risk_score`, `gdelt_mean_tone`, `gdelt_n_events` | float64 | GDELT geopolitical risk signal — **5-day sample only, not representative of the full period** (`11_limitations.md` L7); present in the schema but should not be treated as a reliable daily signal until backfilled |
| `log_return` | float64 | Same-day SPY log return, `log(close_t / close_{t-1})` |
| `fwd_return_1d` | float64 | **Primary target variable** — forward 1-day SPY log return, `log(close_{t+1} / close_t)`, i.e. `log_return` shifted back one row. NaN on the final row by construction (no future data exists) |
| `split` | object | `"train"` (2015-01-02 → 2022-12-30) or `"test"` (2023-01-03 → 2025-12-30), matching the frozen Phase 5 chronological split |

## Target variable

`fwd_return_1d` — forward 1-day SPY log return. Frozen as the sole primary target for this dataset version; `fwd_return_5d`/`fwd_return_10d` (used as secondary targets in `model_features.parquet`) are **not** included here and should be (re)computed at the feature-engineering stage from `log_return` if needed, to keep this base dataset minimal.

## Train / test split (frozen, matches Phase 5)

| Split | Rows | Date range |
|-------|------|------------|
| Train | 2,014 | 2015-01-02 → 2022-12-30 |
| Test | 751 | 2023-01-03 → 2025-12-30 |

Row counts are 1 higher per split than `model_features.parquet` (2,013 / 750) because this base dataset has no lag/rolling-window warm-up trimming — the very first row(s) that lag features would turn to `NaN` are still present here as valid rows (only `log_return`/`fwd_return_1d` are `NaN` at the two natural boundaries). This is expected and not a discrepancy to reconcile away — see `05_data_dictionary.md`.

## Missing value policy

| Column group | Policy | Rationale |
|---------------|--------|-----------|
| Price/VIX (`spy_*`, `QQQ/GLD/TLT`, `vix`) | No missing values found on any of the 2,765 trading days | These are exchange-traded closes; a gap would indicate a genuine data-collection defect, not an expected absence |
| Macro (`fed_funds_rate`, `cpi`, etc.) | Forward-filled onto the trading calendar | Macro releases are lower-frequency (monthly/less) than daily trading; forward-fill carries the last known value, standard practice for merging macro into a daily panel. Zero `NaN` remained after this step |
| Sentiment/event (`energy`...`total_events`) | Filled with `0.0` | A missing row from the `daily_sentiment` join means no tagged event occurred that day — a true zero, not an unknown value |
| `gdelt_*` | Filled with `0.0` (same join logic) | Same reasoning, compounded by the 5-day sample limitation — treat as structurally sparse, not just event-sparse |
| `log_return` | 1 `NaN` (first row) | No prior day exists to difference against — expected |
| `fwd_return_1d` | 1 `NaN` (last row) | No future day exists yet — expected, and is the proof point for the leakage check below |

---

## Validation report (run 2026-07-04, `data/processed/master_dataset_validation.json`)

| Check | Result | Verdict |
|-------|--------|---------|
| Duplicate dates | 0 | ✅ Pass |
| Date monotonic increasing | True | ✅ Pass |
| Max gap between consecutive dates | 4 calendar days | ✅ Pass (consistent with long weekends/holidays; no unexplained gap) |
| Gaps > 5 calendar days | 0 | ✅ Pass |
| Missing values outside the two expected boundary rows | 0 | ✅ Pass |
| Look-ahead / leakage check: `fwd_return_1d[t] == log_return[t+1]` for all non-null rows | 0 mismatches | ✅ Pass |
| Last row `fwd_return_1d` is `NaN` (proves the target was not back-filled from anywhere) | True | ✅ Pass |

**Look-ahead bias / leakage — reasoning, not just the mechanical check:** every non-target column in this dataset is a same-day-or-earlier observation (same-day close, same-day VIX, forward-filled macro from a prior release, same-day event/sentiment aggregation). The only forward-looking column is `fwd_return_1d`, which is explicitly named and documented as the target, is `NaN` on the last row, and is verified above to be an exact one-row shift of `log_return` — there is no path by which a future value has been folded into a feature column. Feature-engineering notebooks that build on this file must preserve this property: any new lag/rolling feature must be computed using `.shift(n)` with `n >= 0` relative to `date`, never a centred or backward window that reaches into `t+1`.

---

## Definition of Done — status

| Item | Status |
|------|:---:|
| `master_dataset.parquet` created | ✅ |
| Schema frozen (34 columns, documented above) | ✅ |
| `05_data_dictionary.md` updated | ✅ |
| Validation report complete | ✅ (`master_dataset_validation.json`) |
| Dataset Version 1.0 approved | 🟡 Pending Project Director review |

## Review Gate

**Project Director approval required before this version is used as the input to Mission 05 (Feature Matrix v1.0).** All validation checks above pass; no blocking issues found. Two carried-forward, non-blocking notes for the Director's awareness: (1) `QQQ`/`GLD`/`TLT` are included in the schema but remain unused pending the Mission-independent decision in `10_decision_log.md`/`11_limitations.md` L8; (2) `gdelt_*` columns are structurally present but sparse (5-day sample) and should not be fed into modelling as-is (`11_limitations.md` L7).
