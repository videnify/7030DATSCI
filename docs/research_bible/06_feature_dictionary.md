# 06 — Feature Dictionary (FES v1.0)

**Purpose:** Definition of every engineered feature in the frozen `data/processed/feature_matrix.parquet` (FES v1.0) — source variables, formula, category, research-question support, and baseline eligibility for each. This supersedes the previous (pre-freeze) version of this document, which described `model_features.parquet` (88 candidate / 52 RF-selected features built by re-deriving the merge in-memory). That file and its importances remain on disk as a legacy artefact but is no longer the ground truth — see `10_decision_log.md` (2026-07-05 entry) for why a clean rebuild was chosen over patching the old one in place.
**Owner:** Ibrahim Haroun (Senior Data Science Architect / Research Statistician).
**Dependencies:** `feature_contract.md` (consumption rules — read that first), `feature_matrix_validation.json`, `feature_profile.json`, `statistical_analysis_plan.md` Part A, `04_statistics_plan.md` (feature-engineering thresholds), `dataset_contract.md`, `10_decision_log.md`.
**Update Frequency:** Regenerate only alongside a new Feature Matrix version — cross-check every column name and count directly against `feature_profile.json`, never from memory.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.3 (Feature Engineering). RQ2's feature-importance results (a separate, not-yet-run RF-selection pass on top of this frozen matrix) will cite this dictionary for what each ranked feature *means*.

---

## How to read this dictionary

Every feature in FES v1.0 has exactly one **Category** (Market, Macro, Sentiment, Event, Temporal, Interaction — no feature belongs to two categories, per the mission's classification rule). Fields that are constant across an entire category (Data Type, Notebook Created, Dependencies, Baseline/Event-model eligibility, Supported RQs) are stated once in that category's header rather than repeated 95 times in a single unreadable table; fields that vary per feature (source variables, formula, purpose, specific risks) are given in the per-feature table. This inheritance structure is itself part of "well documented" — a flat 95-row × 14-column table would bury the signal an examiner or future-you actually needs.

**Shared across every feature in this document:** Data type `float64`. Built by the feature-engineering step (repo notebook `05_feature_engineering.ipynb`, to be updated to consume `master_dataset.parquet` + `car_results.parquet` per `feature_contract.md` rather than its previous in-memory re-derivation). Missing-value handling: warm-up/boundary rows trimmed, never back-filled (`statistical_analysis_plan.md` Part A) — see `feature_profile.json.missing_summary`.

---

## Summary

| Category | Feature count | Baseline-eligible | Event-model-eligible | Top structural feature |
|---|:---:|:---:|:---:|---|
| Market | 27 | ✅ | ✅ | `return_lag1d` (highest RQ2 rank in the legacy pass) |
| Macro & VIX | 16 | ❌ | ✅ | `vix_vs_ma` |
| Sentiment | 25 | ❌ | ✅ | `sent_mean_5d` |
| Event | 14 | ❌ | ✅ | `mean_car` |
| Temporal | 5 | ❌ | ✅ | `month_sin` |
| Interaction | 8 | ❌ | ✅ | `sig_event_x_momentum` |
| **Total** | **95** | 27 baseline-eligible | 95 event-model-eligible | — |

RF-importance selection (which of these 95 candidates clears the 0.001 threshold, `04_statistics_plan.md`) is a **separate, not-yet-run step** downstream of this freeze — see `15_traceability_matrix.md`. This dictionary documents the full frozen candidate set, not a post-selection subset.

---

## Market Features (27) — Category header

**Supports:** RQ2 (feature-importance ranking), RQ3 (both baseline and event-enhanced models). **Hypothesis:** H2 (descriptive ranking), H3 (model comparison). **Baseline-eligible:** ✅ Yes — this is the *only* category the market-only baseline (`Baseline_LASSO`) may read. **Dependencies:** `master_dataset.parquet` columns `spy_close/open/high/low/volume`, `log_return`. **Expected behaviour:** SPY log returns are stationary (confirmed, Mission 05A ADF/KPSS); technical indicators derived from a stationary series inherit that property. **Note:** the "Technical Indicators" sub-group from the pre-freeze dictionary is folded into Market Features here — the mission's Part B classification scheme defines five feature categories, not six, and price/volatility/momentum/RSI/Bollinger indicators are all market-derived by construction.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `log_return` | `spy_close` | `log(close_t/close_{t-1})` (passthrough from `master_dataset.parquet`) | Base return signal, same-day | None — already validated at dataset freeze |
| `log_return_hi` | `spy_high` | `log(high_t/high_{t-1})` | Intraday-high return proxy | Correlated with `log_return` by construction |
| `log_return_lo` | `spy_low` | `log(low_t/low_{t-1})` | Intraday-low return proxy | Correlated with `log_return` by construction |
| `intraday_range` | `spy_high`, `spy_low`, `spy_close` | `(high-low)/close` | Intraday volatility proxy | None |
| `volume_ratio` | `spy_volume` | `volume_t / rolling_mean(volume, 21)` | Relative volume signal | Rolling-window warm-up (handled by trim policy) |
| `return_lag1d`/`3d`/`5d`/`10d`/`21d` | `log_return` | `log_return.shift(n)`, n∈{1,3,5,10,21} | Autocorrelation/lag structure (lag set justified by ACF/PACF, `statistical_assumptions.md` Part H) | None — `.shift(n≥0)` only, non-anticipative by construction |
| `cum_return_5d`/`10d`/`21d` | `log_return` | `log_return.rolling(w).sum()`, w∈{5,10,21} | Multi-day momentum proxy | `cum_return_21d` flagged VIF>10 and \|r\|>0.90 vs. `momentum_21d` — expected near-identity (see below), flagged not dropped |
| `volatility_10d`/`21d`/`63d` | `log_return` | `log_return.rolling(w).std()`, w∈{10,21,63} | Realised-volatility regime signal | `volatility_10d`/`21d` flagged \|r\|>0.90 (overlapping windows) — expected, flagged not dropped |
| `momentum_21d`/`63d`/`126d` | `spy_close` | `close_t/close_{t-w} - 1`, w∈{21,63,126} | Multi-horizon price momentum | `momentum_21d` is near-identical to `cum_return_21d` (VIF 751.8, r=0.997) since `log(1+x)≈x` for small daily-compounded returns — both retained for interpretability (simple return vs. log return), flagged in `feature_matrix_validation.json`, not auto-dropped per `statistical_assumptions.md` policy |
| `rsi_14d` | `spy_close` | Standard 14-day RSI: `100 - 100/(1+RS)`, `RS = mean(gains,14)/mean(losses,14)` | Overbought/oversold momentum oscillator | VIF 10.85 (borderline) — flagged |
| `rsi_oversold` / `rsi_overbought` | `rsi_14d` | `rsi_14d < 30` / `> 70` | Binary regime flags derived from `rsi_14d` | Rare-event class imbalance (expected for a threshold flag) |
| `bb_width` | `spy_close` | `(upper−lower)/mid`, 20-day Bollinger Bands (±2σ) | Volatility-regime proxy | None |
| `bb_position` | `spy_close` | `(close−lower)/(upper−lower)` | Price position within Bollinger Band | None |
| `ma_cross` | `spy_close` | `MA50 > MA200` (binary) | Trend-regime flag | 200-day warm-up (largest single trim contributor) |
| `price_vs_ma200` | `spy_close` | `close/MA200 - 1` | Long-run trend-deviation signal | VIF 22.27 — flagged (structurally related to `ma_cross`/momentum features) |
| `high_vol_regime` | `volatility_21d` | `volatility_21d > q75(volatility_21d, train split)` | Volatility-regime binary flag | Threshold fit on **train split only** — a hard requirement to avoid leaking test-period volatility distribution into the regime cutoff |

---

## Macro & VIX Features (16) — Category header

**Supports:** RQ1 (context — VIX/rate regime as a confounder in the causal model), RQ2, RQ3 (event-enhanced only). **Hypothesis:** H2, H3. **Baseline-eligible:** ❌ No. **Dependencies:** `master_dataset.parquet` columns `vix`, `fed_funds_rate`, `cpi`, `unemployment`, `treasury_10y`, `yield_spread`. **Expected behaviour:** macro **levels** (`fed_funds_rate`, `treasury_10y`, `cpi` — used raw here) are expected to be non-stationary per Mission 05A's ADF/KPSS results; per `statistical_assumptions.md`, this is acceptable for tree models but any LASSO use of a raw level column should prefer its differenced counterpart (`fed_rate_change`, `cpi_mom`, `yield_spread_change`) — flagged here, not silently substituted, since both raw and differenced versions are retained in this matrix for exactly this reason.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `vix` | `vix` | Passthrough | Same-day volatility level | VIF 27.34 — flagged (correlated with its own derived regime/change features by construction) |
| `vix_change_1d` / `vix_change_5d` | `vix` | `vix.diff(1)` / `vix.diff(5)` | Volatility momentum | None |
| `vix_vs_ma` | `vix` | `vix / rolling_mean(vix,21) - 1` | Volatility relative to its own trend | None |
| `vix_regime` | `vix` | `vix > q75(vix, train split)` | High-volatility regime flag | Threshold fit on train split only (same leakage-avoidance rule as `high_vol_regime`) |
| `vix_spike` | `vix_change_1d` | `vix_change_1d > q90(vix.diff(1), train split)` | Volatility-shock flag | Same train-only threshold rule |
| `fed_funds_rate` | `fed_funds_rate` | Passthrough (raw level) | Monetary-policy stance | Non-stationary level — prefer `fed_rate_change` for LASSO (`statistical_assumptions.md`) |
| `yield_spread` | `yield_spread` | Passthrough (raw level, 10y−2y) | Yield-curve level | Non-stationary; see `yield_spread_change` |
| `treasury_10y` | `treasury_10y` | Passthrough (raw level) | Long-rate level | Non-stationary; retained for reference, not recommended for LASSO raw |
| `unemployment` | `unemployment` | Passthrough (raw level) | Labour-market macro control | Level series |
| `fed_rate_change` | `fed_funds_rate` | `fed_funds_rate.diff(21)` (~1 trading month) | Stationarity-safe monetary-policy-change signal | None — this is the differenced series `statistical_assumptions.md` requires in place of the raw level for linear models |
| `cpi_mom` | `cpi` | `cpi.diff(21)` | Stationarity-safe inflation-change signal | Forward-filled monthly source, so `diff(21)` approximates month-on-month change on the trading calendar |
| `yield_spread_change` | `yield_spread` | `yield_spread.diff(5)` | Stationarity-safe curve-steepening/flattening signal | None |
| `rate_hike_signal` / `rate_cut_signal` | `fed_rate_change` | `fed_rate_change > 0` / `< 0` | Directional monetary-policy flags | Mutually exclusive by construction (never both 1) |
| `inverted_yield` | `yield_spread` | `yield_spread < 0` | Recession-signal flag | Rare-event class imbalance (yield inversions are infrequent by nature) |

---

## Sentiment Features (25) — Category header

**Supports:** RQ1 (methodology — feeds the causal model's sentiment signal), RQ2. **Hypothesis:** H1 (context), H2. **Baseline-eligible:** ❌ No. **Dependencies:** `master_dataset.parquet` columns `overall_mean_sentiment`, `overall_net_sentiment`, `total_events`, and the eight per-category daily sentiment columns (`energy, geopolitical, health, labour, monetary, other, regulatory, trade`) — all already predominantly FinBERT-method aggregates (official primary sentiment engine, Sentiment Engine Freeze v1.0 — `10_decision_log.md`), with the lexicon scorer retained only as a fallback/historical method. **Expected behaviour:** raw per-category sentiment is genuinely zero (not missing) on non-event days, per `dataset_version.md`'s fill policy — every rolling/lag feature below inherits that same zero-is-a-true-value semantics.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `overall_mean_sentiment` / `overall_net_sentiment` / `total_events` | same-named `master_dataset.parquet` columns | Passthrough | Same-day aggregate sentiment/activity level | None |
| `monetary`, `trade`, `geopolitical`, `regulatory`, `energy`, `health`, `labour` | same-named columns | Passthrough | Per-category same-day sentiment | `monetary` flagged VIF 12.61 and \|r\|>0.90 vs. `monetary_x_vix` — expected (interaction term shares the parent variable), flagged not dropped |
| `sent_mean_5d`/`10d`/`21d` | `overall_mean_sentiment` | `.rolling(w).mean()`, w∈{5,10,21} | Smoothed sentiment trend | None |
| `sent_std_5d`/`10d` | `overall_mean_sentiment` | `.rolling(w).std()`, w∈{5,10} | Sentiment volatility/disagreement proxy | None |
| `sent_momentum_5d`/`10d` | `overall_mean_sentiment`, `sent_mean_5d`/`10d` | `overall_mean_sentiment − sent_mean_{w}d` | Same-day sentiment surprise vs. recent trend | Both flagged \|r\|>0.90 vs. `overall_mean_sentiment` and vs. each other — definitional overlap (a same-day-minus-rolling-mean term is mechanically close to the same-day level when the rolling window is short), flagged not dropped |
| `sent_positive_day` / `sent_negative_day` | `overall_mean_sentiment` | `> 0` / `< 0` | Binary sentiment-direction flags | Mutually exclusive by construction |
| `monetary_lag1`/`5`, `trade_lag1`/`5`, `geopolitical_lag1`/`5` | `monetary`, `trade`, `geopolitical` | `.shift(n)`, n∈{1,5} | Lagged category-specific sentiment (these three categories chosen for lag features as the most policy-salient to RQ1's event types) | None — non-anticipative by construction |

---

## Event Features (14) — Category header

**Supports:** RQ1 (direct output of the event study), RQ2 (event signal in the importance ranking), RQ3. **Hypothesis:** H1, H2, H3. **Baseline-eligible:** ❌ No — this is the category the market-only baseline must never see, by definition. **Dependencies:** `data/processed/car_results.parquet` (approved second input, `10_decision_log.md` 2026-07-05) for 10 of the 14 features below; `master_dataset.parquet`'s own per-category sentiment columns for the remaining 3 category-occurrence flags. **Expected behaviour:** `car_results.parquet` contains at most one event-study row per calendar date over the study period, so every count-style feature below is a same-day 0/1 indicator, not a multi-event sum — stated explicitly so a future notebook doesn't misinterpret `n_monetary_events` as capable of exceeding 1.

**Explicitly out of scope for v1.0:** `mean_car`, `n_sig_events`, and the per-category event flags below reconstruct only what `car_results.parquet` and `master_dataset.parquet` already contain. Three features from the pre-freeze dictionary — `n_high_impact_events`, `days_since_hi_event`, `high_impact_day` — required `events_tagged.parquet`/`high_impact_events.parquet`'s `is_high_impact` flag, which is **not** one of this freeze's two approved inputs. They are not reconstructed here; re-adding them is a defined candidate for a v1.1 amendment (would require a `10_decision_log.md` entry naming `high_impact_events.parquet` as a third approved input).

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `mean_car` | `car_results.parquet: car` | Same-day cumulative abnormal return if an event occurred that day, else `0.0` | Direct event-study signal — the single feature that bridges RQ1's causal finding into RQ2/RQ3 | Zero-fill on non-event days follows the same "true zero" logic already used for sentiment (`dataset_version.md`) — not a missing-value compromise |
| `n_monetary_events` / `n_geopolitical_events` / `n_regulatory_events` / `n_trade_events` / `n_energy_events` | `car_results.parquet: event_type` | `(event_type == category)` same-day indicator | Per-category event-occurrence signal, event-study-derived | Binary (0/1), not a true count — see category note above |
| `n_sig_events` | `car_results.parquet: significant` | Same-day 0/1 pass-through of the (pre-FDR-correction) event-study significance flag | Flags whether that day's event individually reached p<0.05 | Not yet BH-FDR corrected — same caveat as `car_results.parquet` itself (`11_limitations.md` L3); this is a feature-engineering passthrough, not a new statistical claim |
| `car_positive` / `car_negative` | `car_results.parquet: car` | `car > 0` / `car < 0` on event days, else `0` | Directional event-reaction flags | None |
| `car_event_day` | `car_results.parquet: car` (notna) | `1` if any event-study row exists that date, else `0` | Base event-occurrence flag (denominator for the others) | None |
| `days_since_car_event` | `car_event_day` | Trading days since the most recent `car_event_day==1`, current-day event counts as `0` | Event-recency/decay signal | `NaN` for every row before the first observed event in the study period (2016-01-05) — correctly trimmed by the warm-up policy, not back-filled |
| `health_event_day` / `labour_event_day` / `other_event_day` | `master_dataset.parquet: health/labour/other` | `sentiment_category != 0.0` | Occurrence proxy for the three event categories absent from `car_results.parquet`'s `event_type` set | This is an **occurrence flag**, not an event count — named deliberately differently from `n_<category>_events` (which are true car_results-derived indicators) to avoid implying a count that this input cannot support |

---

## Temporal Features (5) — Category header

**Supports:** RQ2, RQ3 (control variables — calendar effects are a known, non-event confound worth isolating). **Hypothesis:** H2, H3. **Baseline-eligible:** ❌ No — kept out of the baseline deliberately, so the baseline stays a strict "price/technical only" comparator matching `statistical_decision_matrix.md`'s existing definition; calendar effects can correlate with recurring scheduled events (e.g. FOMC's fixed 8-meetings-a-year cadence), so admitting them to the baseline risks smuggling in event-timing structure through the back door. **Dependencies:** `master_dataset.parquet: date` only. **Note on scope:** lag structure and rolling windows (also named in the mission's Part B Temporal examples) are *not* duplicated here — they are documented once, under the substantive category they belong to (Market, Sentiment), per the "one category only" rule. This category is reserved for pure calendar features.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `dow_sin` / `dow_cos` | `date` | `sin`/`cos(2π · day_of_week / 5)` | Cyclical day-of-week encoding (5-day trading week) | None |
| `month_sin` / `month_cos` | `date` | `sin`/`cos(2π · (month-1) / 12)` | Cyclical month encoding (captures seasonal effects without 12 dummy columns) | None |
| `quarter_num` | `date` | Calendar quarter, 1–4 | Coarse seasonal/reporting-cycle control | Ordinal (not cyclically encoded) — a 4-level variable does not warrant sin/cos treatment |

---

## Interaction Features (8) — Category header

**Supports:** RQ2, RQ3. **Hypothesis:** H2, H3. **Baseline-eligible:** ❌ No — every interaction below multiplies a market term by an event/macro/sentiment term, so none qualify even partially for the market-only baseline. **Dependencies:** the specific Market/Macro/Sentiment/Event columns named per row below (already documented above — not re-derived independently).

**Explicitly out of scope for v1.0:** `hi_event_x_momentum` (pre-freeze dictionary) required the same `is_high_impact` flag excluded above; replaced here by `sig_event_x_momentum`, built from the in-scope `n_sig_events` flag, preserving the same "event-significance × momentum" interaction concept without the out-of-scope dependency.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `sig_event_x_momentum` | `n_sig_events`, `momentum_63d` | Product | Momentum effect conditional on a statistically significant event that day | Sparse (mostly 0, since `n_sig_events` is rare) |
| `sent_x_vix_regime` | `overall_mean_sentiment`, `vix_regime` | Product | Sentiment effect conditional on high-volatility regime | None |
| `monetary_x_vix` | `monetary`, `vix` | Product | Monetary-sentiment effect scaled by volatility level | Flagged \|r\|>0.90 / VIF 12.15 vs. `monetary` — expected (shares a parent term) |
| `geopolit_x_vix_regime` | `geopolitical`, `vix_regime` | Product | Geopolitical-sentiment effect conditional on high-volatility regime | None |
| `monetary_x_rate_hike` / `monetary_x_rate_cut` | `monetary`, `rate_hike_signal`/`rate_cut_signal` | Product | Monetary-sentiment effect conditional on policy direction | Mutually exclusive in the same row (hike/cut flags are mutually exclusive) |
| `sent_x_high_vol` | `overall_mean_sentiment`, `high_vol_regime` | Product | Sentiment effect conditional on high realised-volatility regime | None |
| `car_x_sent` | `mean_car`, `overall_mean_sentiment` | Product | Event-study abnormal return scaled by same-day sentiment | Mostly 0 (both parent terms are frequently 0 on non-event days) |

---

## QA fixes made during this freeze (documented per `10_decision_log.md`)

1. **`momentum_21d` restored to the Market group.** The pre-freeze dictionary's "Technical indicators" table omitted `momentum_21d` despite it being present in `model_features.parquet`'s actual column list (95 columns) — a documentation gap, not a feature that was ever truly absent. It is included here, bringing the Market category to its correct count of 27 (13 price/return + 14 technical, folded into one category per the mission's 5-category scheme).
2. **`monetary_x_rate_cut` restored to the Interaction group.** Same class of gap — present in `model_features.parquet`'s columns but missing from the pre-freeze dictionary's interaction table (which listed 7, not the actual 8).
3. **Baseline feature count is 27, not 26.** `statistical_decision_matrix.md` states the market-only baseline has "26 features (price + technical only)" — that number inherits fix #1's gap. The correct, contract-enforced count under FES v1.0 is 27 (all Market-category features). `statistical_decision_matrix.md` should be read alongside this correction until it is itself updated at Mission 06.

---

## Reading this dictionary alongside RQ2 (updated 2026-07-05, Mission 07)

The RF-importance pass anticipated above has now been run on `feature_matrix.parquet` (Mission 07): top 10 by impurity importance are `log_return_hi` (market, 0.079), `mean_car` (event, 0.072), `return_lag1d` (market, 0.068), `cum_return_5d` (market, 0.037), `return_lag5d` (market, 0.036), `return_lag3d` (market, 0.035), `vix` (macro, 0.035), `vix_change_5d` (macro, 0.031), `return_lag10d` (market, 0.029), `vix_change_1d` (macro, 0.028) — 61/95 features clear the frozen 0.001 threshold. This qualitatively replicates the legacy 2026-07-04 finding (event and macro signal rank alongside, not below, price signal — `mean_car` is #2 overall here) but the exact percentages differ, as expected, from the superseded `model_features.parquet`-derived figures and must not be conflated with them. Full ranking, SHAP cross-corroboration (native TreeSHAP for XGBoost/LightGBM, exact linear SHAP for Event_LASSO), and the RQ3 model comparison this feeds into: `reports/model_comparison/feature_importance.parquet`, `reports/tables/07_shap_importance_summary.csv`, `reports/statistics/07_event_models_summary.md`.
