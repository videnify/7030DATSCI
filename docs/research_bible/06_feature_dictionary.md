# 06 — Feature Dictionary (FES v1.1)

**Purpose:** Definition of every engineered feature in the frozen `data/processed/feature_matrix.parquet` (FES v1.1) — source variables, formula, category, research-question support, and baseline eligibility for each. FES v1.1 supersedes FES v1.0 by using direct catalogue-occurrence counts for the health/labour/other flags and enforcing the frozen training-variance threshold before save.
**Owner:** Ibrahim Haroun (Senior Data Science Architect / Research Statistician).
**Dependencies:** `feature_contract.md` (consumption rules — read that first), `feature_matrix_validation.json`, `feature_profile.json`, `statistical_analysis_plan.md` Part A, `04_statistics_plan.md` (feature-engineering thresholds), `dataset_contract.md`, `10_decision_log.md`.
**Update Frequency:** Regenerate only alongside a new Feature Matrix version — cross-check every column name and count directly against `feature_profile.json`, never from memory.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.3 (Feature Engineering). The FES v1.1 baseline, RQ2 importance, event-model/RQ3 comparison, and validated Notebook 08 figures cite this dictionary.

---

## How to read this dictionary

Every feature in FES v1.1 has exactly one **Category** (Market, Macro, Sentiment, Event, Temporal, Interaction — no feature belongs to two categories). Fields that are constant across an entire category are stated once in that category's header rather than repeated 92 times; fields that vary per feature are given in the per-feature table.

**Shared across every feature in this document:** Data type `float64`. Built by `05_feature_engineering.ipynb` from Dataset v1.2 `master_dataset.parquet` plus `car_results.parquet`. Missing-value handling: warm-up/boundary rows are trimmed, never back-filled (`statistical_analysis_plan.md` Part A) — see `feature_profile.json.missing_summary`.

---

## Summary

| Category | Feature count | Baseline-eligible | Event-model-eligible | Top structural feature |
|---|:---:|:---:|:---:|---|
| Market | 27 | ✅ | ✅ | `return_lag1d` (highest RQ2 rank in the legacy pass) |
| Macro & VIX | 16 | ❌ | ✅ | `vix_vs_ma` |
| Sentiment | 23 | ❌ | ✅ | `sent_mean_5d` |
| Event | 14 | ❌ | ✅ | `mean_car` |
| Temporal | 5 | ❌ | ✅ | `month_sin` |
| Interaction | 7 | ❌ | ✅ | `sig_event_x_momentum` |
| **Total** | **92** | 27 baseline-eligible | 92 event-model-eligible | — |

RF importance is a downstream RQ2 analysis, not a feature-freeze filter. Notebook 07 now ranks all 92 candidates reproducibly; 55 exceed the 0.001 reporting threshold.

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

## Sentiment Features (23) — Category header

**Supports:** RQ1 (methodology — feeds the causal model's sentiment signal), RQ2. **Hypothesis:** H1 (context), H2. **Baseline-eligible:** ❌ No. **Dependencies:** `master_dataset.parquet` columns `overall_mean_sentiment`, `overall_net_sentiment`, `total_events`, and the retained per-category sentiment columns (`geopolitical`, `health`, `monetary`, `regulatory`, `trade`) — all predominantly FinBERT aggregates (SEF v1.0). `energy` and `labour` are excluded because each has training-split variance below 1e-8. **Expected behaviour:** raw per-category sentiment is genuinely zero (not missing) on non-event days.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `overall_mean_sentiment` / `overall_net_sentiment` / `total_events` | same-named `master_dataset.parquet` columns | Passthrough | Same-day aggregate sentiment/activity level | None |
| `monetary`, `trade`, `geopolitical`, `regulatory`, `health` | same-named columns | Passthrough | Per-category same-day sentiment | Parent/interaction multicollinearity remains an informational validation flag, not a blocker |
| `sent_mean_5d`/`10d`/`21d` | `overall_mean_sentiment` | `.rolling(w).mean()`, w∈{5,10,21} | Smoothed sentiment trend | None |
| `sent_std_5d`/`10d` | `overall_mean_sentiment` | `.rolling(w).std()`, w∈{5,10} | Sentiment volatility/disagreement proxy | None |
| `sent_momentum_5d`/`10d` | `overall_mean_sentiment`, `sent_mean_5d`/`10d` | `overall_mean_sentiment − sent_mean_{w}d` | Same-day sentiment surprise vs. recent trend | Both flagged \|r\|>0.90 vs. `overall_mean_sentiment` and vs. each other — definitional overlap (a same-day-minus-rolling-mean term is mechanically close to the same-day level when the rolling window is short), flagged not dropped |
| `sent_positive_day` / `sent_negative_day` | `overall_mean_sentiment` | `> 0` / `< 0` | Binary sentiment-direction flags | Mutually exclusive by construction |
| `monetary_lag1`/`5`, `trade_lag1`/`5`, `geopolitical_lag1`/`5` | `monetary`, `trade`, `geopolitical` | `.shift(n)`, n∈{1,5} | Lagged category-specific sentiment (these three categories chosen for lag features as the most policy-salient to RQ1's event types) | None — non-anticipative by construction |

---

## Event Features (14) — Category header

**Supports:** RQ1 (direct output of the event study), RQ2 (event signal in the importance ranking), RQ3. **Hypothesis:** H1, H2, H3. **Baseline-eligible:** ❌ No. **Dependencies:** `data/processed/car_results.parquet` for 10 features; Dataset v1.2 columns `n_health_catalogue_events`, `n_labour_catalogue_events`, and `n_other_catalogue_events` for the three direct occurrence flags. **Expected behaviour:** `car_results.parquet` contains at most one event-study row per date; the catalogue counts may exceed one, but their FES flags are binary presence indicators.

**Explicitly out of scope for FES v1.1:** `n_high_impact_events`, `days_since_hi_event`, and `high_impact_day` require `events_tagged.parquet`/`high_impact_events.parquet`'s `is_high_impact` flag, which is not one of the two approved FES inputs. Adding them would require a later versioned amendment naming a third input.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `mean_car` | `car_results.parquet: car` | Same-day cumulative abnormal return if an event occurred that day, else `0.0` | Direct event-study signal — the single feature that bridges RQ1's causal finding into RQ2/RQ3 | Zero-fill on non-event days follows the same "true zero" logic already used for sentiment (`dataset_version.md`) — not a missing-value compromise |
| `n_monetary_events` / `n_geopolitical_events` / `n_regulatory_events` / `n_trade_events` / `n_energy_events` | `car_results.parquet: event_type` | `(event_type == category)` same-day indicator | Per-category event-occurrence signal, event-study-derived | Binary (0/1), not a true count — see category note above |
| `n_sig_events` | `car_results.parquet: significant` | Same-day 0/1 pass-through of the individual-window diagnostic flag | Flags whether that event window's internally standardised statistic reached p<0.05 | This row-level feature is intentionally unchanged by the separate five-type BH-FDR analysis. It must not be interpreted as an event-type rejection flag; `event_type_statistics.parquet` is the inferential RQ1 source. |
| `car_positive` / `car_negative` | `car_results.parquet: car` | `car > 0` / `car < 0` on event days, else `0` | Directional event-reaction flags | None |
| `car_event_day` | `car_results.parquet: car` (notna) | `1` if any event-study row exists that date, else `0` | Base event-occurrence flag (denominator for the others) | None |
| `days_since_car_event` | `car_event_day` | Trading days since the most recent `car_event_day==1`, current-day event counts as `0` | Event-recency/decay signal | `NaN` before the first retained CAR event; correctly trimmed so the matrix begins 2016-02-24 |
| `health_event_day` / `labour_event_day` / `other_event_day` | Dataset v1.2 `n_health_catalogue_events` / `n_labour_catalogue_events` / `n_other_catalogue_events` | `(n_<category>_catalogue_events > 0).astype(float)` | Direct same-date catalogue-occurrence flags, independent of sentiment polarity | Same-date SPY-calendar policy excludes non-trading dates rather than reassigning them; see `11_limitations.md` L17 |

---

## Temporal Features (5) — Category header

**Supports:** RQ2, RQ3 (control variables — calendar effects are a known, non-event confound worth isolating). **Hypothesis:** H2, H3. **Baseline-eligible:** ❌ No — kept out of the baseline deliberately, so the baseline stays a strict "price/technical only" comparator matching `statistical_decision_matrix.md`'s existing definition; calendar effects can correlate with recurring scheduled events (e.g. FOMC's fixed 8-meetings-a-year cadence), so admitting them to the baseline risks smuggling in event-timing structure through the back door. **Dependencies:** `master_dataset.parquet: date` only. **Note on scope:** lag structure and rolling windows (also named in the mission's Part B Temporal examples) are *not* duplicated here — they are documented once, under the substantive category they belong to (Market, Sentiment), per the "one category only" rule. This category is reserved for pure calendar features.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `dow_sin` / `dow_cos` | `date` | `sin`/`cos(2π · day_of_week / 5)` | Cyclical day-of-week encoding (5-day trading week) | None |
| `month_sin` / `month_cos` | `date` | `sin`/`cos(2π · (month-1) / 12)` | Cyclical month encoding (captures seasonal effects without 12 dummy columns) | None |
| `quarter_num` | `date` | Calendar quarter, 1–4 | Coarse seasonal/reporting-cycle control | Ordinal (not cyclically encoded) — a 4-level variable does not warrant sin/cos treatment |

---

## Interaction Features (7) — Category header

**Supports:** RQ2, RQ3. **Hypothesis:** H2, H3. **Baseline-eligible:** ❌ No — every interaction below multiplies a market term by an event/macro/sentiment term, so none qualify even partially for the market-only baseline. **Dependencies:** the specific Market/Macro/Sentiment/Event columns named per row below (already documented above — not re-derived independently).

**Explicitly out of scope for FES v1.1:** `hi_event_x_momentum` requires the excluded `is_high_impact` input; `sig_event_x_momentum` uses the in-scope `n_sig_events` flag instead.

| Feature | Source variable(s) | Formula | Purpose | Potential risk |
|---|---|---|---|---|
| `sig_event_x_momentum` | `n_sig_events`, `momentum_63d` | Product | Momentum effect conditional on a statistically significant event that day | Sparse (mostly 0, since `n_sig_events` is rare) |
| `sent_x_vix_regime` | `overall_mean_sentiment`, `vix_regime` | Product | Sentiment effect conditional on high-volatility regime | None |
| `monetary_x_vix` | `monetary`, `vix` | Product | Monetary-sentiment effect scaled by volatility level | Flagged \|r\|>0.90 / VIF 12.15 vs. `monetary` — expected (shares a parent term) |
| `geopolit_x_vix_regime` | `geopolitical`, `vix_regime` | Product | Geopolitical-sentiment effect conditional on high-volatility regime | None |
| `monetary_x_rate_hike` | `monetary`, `rate_hike_signal` | Product | Monetary-sentiment effect conditional on a rate-hike signal | The former `monetary_x_rate_cut` term was removed because its training-split variance is below 1e-8 |
| `sent_x_high_vol` | `overall_mean_sentiment`, `high_vol_regime` | Product | Sentiment effect conditional on high realised-volatility regime | None |
| `car_x_sent` | `mean_car`, `overall_mean_sentiment` | Product | Event-study abnormal return scaled by same-day sentiment | Mostly 0 (both parent terms are frequently 0 on non-event days) |

---

## Version amendments and QA decisions

1. **`momentum_21d` restored to the Market group.** The pre-freeze dictionary's "Technical indicators" table omitted `momentum_21d` despite it being present in `model_features.parquet`'s actual column list (95 columns) — a documentation gap, not a feature that was ever truly absent. It is included here, bringing the Market category to its correct count of 27 (13 price/return + 14 technical, folded into one category per the mission's 5-category scheme).
2. **Historical FES v1.0 correction:** `monetary_x_rate_cut` was restored to the old Interaction group because it existed in that matrix. **FES v1.1 then removes it** under the binding training-variance threshold; this is a methodological removal, not a documentation omission.
3. **Baseline feature count is 27, not 26.** The correct, contract-enforced count remains 27 under FES v1.1.
4. **FES v1.1 variance enforcement:** `energy`, `labour`, and `monetary_x_rate_cut` were removed because their training-split variance is below 1e-8. No other feature was added or removed.
5. **FES v1.1 occurrence correction:** `health_event_day`, `labour_event_day`, and `other_event_day` now derive from explicit catalogue counts. Relative to FES v1.0, values change on 7, 90, and 299 rows respectively; the row index is unchanged.

---

## Reading this dictionary alongside RQ2

The current FES v1.1 Random Forest ranking contains 92 rows and selects 55 features above the 0.001 reporting threshold. Its top 10 are `log_return_hi`, `return_lag1d`, `return_lag3d`, `return_lag5d`, `vix`, `cum_return_5d`, `vix_change_5d`, `price_vs_ma200`, `momentum_63d`, and `vix_change_1d`. Macro/VIX features are present, but the highest event feature (`mean_car`) ranks #20, so H2's joint top-decile rule is not met. Held-out model SHAP is reported separately because its ranking is model-specific; notably, LightGBM ranks `mean_car` fifth.
