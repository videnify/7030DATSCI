# 03 — Methodology

**Purpose:** The full technical methodology for every analytical stage of the pipeline — event study, causal inference, NLP/sentiment, feature engineering, and machine learning — with enough detail that another researcher could reproduce each step without reading the notebook source first.
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `02_hypotheses.md`, `config.yaml` (all parameters below are read from there, not hand-picked per notebook).
**Update Frequency:** Updated whenever a methodological choice changes (e.g. estimation window length, model architecture); every change must reference a `10_decision_log.md` entry.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 (Methodology) in full.

**SAP v1.0 note (2026-07-04):** Every parameter and method below is now governed by the frozen Statistical Analysis Plan — see `statistical_analysis_plan.md` (global policy), `statistical_decision_matrix.md` (test matrix), `statistical_assumptions.md` (assumption checks, including the stationarity, multicollinearity, and outlier policies not previously written down here), and `dataset_contract.md` (consumption rules for `master_dataset.parquet`, which Phase 5 below must read from rather than re-deriving). Any methodological change from this point forward requires a Version 2 SAP amendment and a `10_decision_log.md` entry — this document should not silently diverge from the SAP suite.

---

## 1. Event Study Methodology (→ RQ1)

**Updated 2026-07-07 — this section previously described a market-model event study (Fama, Fisher, Jensen & Roll, 1969 tradition) with a 120-day estimation window, implemented via `src/causal_engine.py::EventStudy`. Live cross-checking of `04_causal_analysis.ipynb` against this description (during Chapter 3, Section 3.3 dissertation revision) found the notebook does not import or call `src/causal_engine.py::EventStudy` at all, and instead implements a different, simpler estimator over a different estimation window. `src/causal_engine.py::EventStudy` is unused legacy module code predating the notebook's current implementation and is not what produced the frozen `car_results.parquet`. This section now describes the notebook's actual, executed methodology. A second correction (also 2026-07-07, surfaced while drafting Section 3.4) fixed this section's "log return" language to "simple (percentage) return," matching `pct_change()` rather than a log transform. See `10_decision_log.md` (2026-07-07 entries) for both correction records.**

**Model:** Constant-mean-return (mean-adjusted) event study — the expected "normal" return for an event is SPY's own historical mean simple (percentage) return over a pre-event estimation window; there is no regression against a separate market-proxy series. Implemented directly in `04_causal_analysis.ipynb` (`compute_car()`, Cell 5).

**Return type note (corrected 2026-07-07):** the SPY return series used throughout this notebook (`spy['spy_return'] = spy['close'].pct_change()`, Cell 3) is a simple percentage return, not a log return. This is distinct from `log_return`/`fwd_return_1d` in `master_dataset.parquet` and `feature_matrix.parquet` (Section 4 below), which are genuine log returns computed independently in `05_feature_engineering.ipynb` via `np.log(...)`. The two notebooks use different return definitions for different purposes and should not be assumed interchangeable.

**Parameters** (from `04_causal_analysis.ipynb` Cell 1 constants — not currently read from `config.yaml`):
| Parameter | Value |
|-----------|-------|
| Estimation window | 252 to 21 trading days before the event date (`ESTIMATION_WINDOW = (-252, -21)`) |
| Event window (pre) | 5 trading days before the event date |
| Event window (post) | 10 trading days after the event date |

**Procedure:**
1. For each event date, compute the expected return as the mean SPY simple (percentage) return over the (−252, −21) trading-day estimation window relative to that date.
2. Abnormal Return (AR) on each day of the event window = actual return − expected return.
3. Cumulative Abnormal Return (CAR) = cumulative sum of AR across the event window (day −5 to +10).
4. The event study is run only on the `high_impact_events.parquet` subset (deduplicated to one record per date); its event types are constrained to the five categories in `HIGH_IMPACT_TYPES` (monetary, geopolitical, trade, regulatory, energy) — health and labour events cannot be flagged high-impact (see `03_event_detection.ipynb`'s high-impact criteria) and therefore never enter the event study.
5. Significance-test CAR against zero per event type (see `04_statistics_plan.md`, corrected 2026-07-07).

**Inputs:** `data/raw/spy_ohlcv.parquet`, `data/processed/high_impact_events.parquet`, `data/processed/daily_sentiment.parquet` (VIX and sentiment merged onto each event's date), `data/raw/vix.parquet`.
**Outputs:** `data/processed/car_results.parquet` (event-level CAR records, one per high-impact event date).
**Notebook:** `04_causal_analysis.ipynb`.

---

## 2. Causal Inference Methodology (→ RQ1)

Event-study CAR establishes *association*, not causation — the abnormal-return residual could reflect confounding (e.g. an event coinciding with a volatility spike that would have moved price regardless). To address this, a second, causal layer is applied.

**Framework:** DoWhy (Microsoft Research) structural causal model.

**Causal DAG:** Treatment = event sentiment → Outcome = next-day SPY return. Confounders: VIX regime and prior-day market return. In the current 2026-07-13 run, the pooled treatment is same-day combined APP FinBERT sentiment plus structured FOMC sentiment. The persisted `sentiment_method="lexicon"` value in `causal_estimates.parquet` is a legacy field label and must not be interpreted as the method used by the current pipeline. GDELT is not an input to this frozen DAG.

**Estimation method:** `backdoor.linear_regression` (from `config.yaml: causal.method`) — adjusts for the identified confounder set via linear regression on the backdoor-adjusted formula.

**Refutation tests** (from `config.yaml: causal.refutation_tests`), run against the primary estimate to check robustness:
1. `random_common_cause` — adds a random covariate; estimate should not change materially.
2. `placebo_treatment_refuter` — replaces the real treatment with random noise; estimate should collapse toward zero.
3. `data_subset_refuter` — re-estimates on a random subset of the data; estimate should remain stable in sign and rough magnitude.

**Inputs:** `data/processed/car_results.parquet`, `data/raw/vix.parquet`.
**Outputs:** `data/processed/car_results.parquet` (264 event windows), `event_type_statistics.parquet` (five mean-CAR rows with 95% t CI, raw p, BH q and Cohen's d), `rq1_reporting_validation.json` (`PASS`) and `causal_estimates.parquet` (causal effect, 95% CI, n_obs, n_nonzero per event type × persisted method label).
**Notebook:** `04_causal_analysis.ipynb`.

---

## 3. NLP & Sentiment Methodology (→ RQ1, RQ2)

**Event classification:** Rule-based keyword matching (not ML) tags the 916 economically pre-filtered APP presidential documents into one of eight categories: monetary, geopolitical, regulatory, trade, energy, health, labour, other. Deterministic and inspectable — a deliberate choice over an ML classifier given the category definitions are policy-domain-specific and a labelled training set does not exist (see `10_decision_log.md`). The 89 FOMC decisions are then added to form the verified 1,005-row unified catalogue; GDELT remains a separate continuous series rather than a catalogue event.

**Sentiment scoring — primary engine and fallback (Sentiment Engine Freeze v1.0, 2026-07-06):**
1. **FinBERT** (`ProsusAI/finbert`, via `src/event_detector.py::EventDetector`) — the project's **official, primary sentiment engine**. A transformer pretrained on financial-news sentiment, scored on document *titles* (not full text — see `11_limitations.md`). Parameters from `config.yaml: nlp` (batch_size 32, max_length 512, confidence threshold 0.7). FinBERT-generated sentiment is used to construct `events_tagged.parquet`, `daily_sentiment.parquet`, and all downstream datasets.
2. **Lexicon scorer** — a curated financial/political keyword lexicon, retained only as a **fallback mechanism** (used when FinBERT/PyTorch is unavailable in the runtime environment) and as a **historical prototype** predating this freeze. It is not the primary methodology used to generate the frozen datasets.

**Method selection (superseded 2026-07-06 — see `10_decision_log.md`, SEF v1.0):** An earlier decision had designated the lexicon scorer as primary, reasoning that FinBERT's title-level output on formal presidential language is 95.3% neutral (vs. 73.1% neutral for the lexicon method) — a domain-mismatch effect from FinBERT being trained on financial-news headlines, not policy speech. Live execution of `03_event_detection.ipynb` (Mission 03, 2026-07-06) confirmed the actual cached/frozen sentiment data is 99.2% FinBERT-sourced, not lexicon-sourced as previously documented. The Project Director resolved this discrepancy by ratifying FinBERT as the official primary engine to match the real pipeline output, rather than re-scoring the catalogue with the lexicon method. This is a documentation/governance correction only — no statistical outputs changed.

**FOMC enrichment:** FOMC meeting dates (`data/raw/fomc_dates.parquet`, 89 meetings) are merged into the same event catalogue with `rate_decision`, `is_emergency`, and `event_importance` fields, giving the "monetary" event type a structured, dated anchor alongside the unstructured presidential-communication events.

**GDELT integration:** Daily Goldstein-scale and tone scores from GDELT are merged into the base dataset as a candidate continuous geopolitical-risk control, not a discrete catalogue event. The full 2015–2025 history (4,018 days) was backfilled on 2026-07-13 (`data/raw/gdelt_daily_summary.parquet`). It is retained in `master_dataset.parquet` v1.2 but deliberately excluded from the frozen DoWhy DAG and `feature_matrix.parquet`; no reported RQ1–RQ3 result uses a GDELT-derived feature (see `11_limitations.md` L7).

**Daily occurrence aggregation and Dataset v1.2 freeze (2026-07-14):** `daily_sentiment.parquet` retains the eight mean-sentiment category columns and also stores direct catalogue-row counts for health, labour, and other. Dataset v1.2 promotes these counts to the SPY trading-day panel. Catalogue totals are 14/103/427; same-date trading-day totals are 12/96/395. The remaining 2/7/32 events occurred when SPY was closed and are recorded, not reassigned. The frozen 2,765 × 34 dataset passes missingness, leakage, dtype, and count-reconciliation checks in `master_dataset_validation.json`.

**Inputs:** `data/raw/app_presidential_documents_economic.parquet`, `data/raw/app_finbert_sentiment_cache.parquet`, `data/raw/fomc_dates.parquet`, `data/raw/gdelt_daily_summary.parquet`.
**Outputs:** `data/processed/events_tagged.parquet`, `daily_sentiment.parquet`, `high_impact_events.parquet`, `gdelt_daily_risk.parquet`.
**Notebook:** `03_event_detection.ipynb`.

---

## 4. Feature Engineering Methodology (→ RQ2, RQ3)

**Updated 2026-07-14 — this section describes FES v1.1, the current feature boundary. See `feature_contract.md` and `06_feature_dictionary.md` for the authoritative rules and column definitions. Notebooks 06–08 provide the validated baseline, event-model, RF/SHAP, comparison-test, and publication-figure boundary.**

The current FES v1.1 `feature_matrix.parquet` was built from Dataset v1.2 `master_dataset.parquet` plus `car_results.parquet`. Six feature categories are engineered:

| Category | Count | Examples |
|-------|-------|----------|
| Market | 27 | log returns, lagged returns (1/3/5/10/21d), cumulative returns, rolling volatility, momentum, RSI-14, Bollinger Band width/position |
| Macro & VIX | 16 | VIX level/change, Fed Funds Rate, CPI month-on-month, Treasury yields, yield-curve spread |
| Sentiment | 23 | retained daily sentiment categories, rolling mean/std, sentiment momentum |
| Event | 14 | event-type day counts, `mean_car`, days-since-last-CAR-event, significant-event flags |
| Temporal | 5 | cyclically encoded day-of-week and month, ordinal quarter |
| Interaction | 7 | sentiment × VIX regime, monetary × rate-hike signal, event-significance × momentum |
| **Total engineered** | **92** | — |

**Feature screening:** FES v1.1 enforces the frozen training-split variance threshold: features with variance below 1e-8 are removed before save. This removed `energy`, `labour`, and `monetary_x_rate_cut`. Correlation (|r| > 0.90) and VIF (> 10) checks remain **informational interpretability flags**, not automatic-drop rules; the current validation records 7 high-correlation pairs and 31 VIF>10 features. No RF-importance threshold is used to define the matrix.

**Target variable:** `fwd_return_1d` (forward 1-day SPY log return) is the sole frozen target. Forward 5-day/10-day targets remain out of scope for FES v1.1.

**Row scope:** after all features are constructed, warm-up and pre-first-CAR rows with undefined values are trimmed, yielding 2,477 rows spanning 2016-02-24 to 2025-12-29.

**Train/test split:** strict chronological split — train 2016-02-24 → 2022-12-30 (1,727 rows), test 2023-01-03 → 2025-12-29 (750 rows). No shuffling.

**Scaling:** per-feature mean and standard deviation computed on the training split only and persisted (`feature_profile.json`), then applied as `(x − mean) / std` uniformly to every engineered feature (including binary flags) in both splits. The scaler is never refit on the full matrix or on test data.

**Baseline eligibility:** the Market category (27 features) is the only category a market-only baseline model may read; the remaining 65 features are event-enhanced-model-only. This boundary is enforced in `feature_contract.md`.

**Inputs:** `data/processed/master_dataset.parquet`, `data/processed/car_results.parquet`.
**Outputs:** `data/processed/feature_matrix.parquet` (2,477 rows × 95 columns, including date/split/target), `feature_profile.json`, `feature_matrix_validation.json` (`PASS`).
**Notebook:** `05_feature_engineering.ipynb`.

---

## 5. Machine Learning Methodology (→ RQ3)

**Updated 2026-07-06 — this section previously described a three-model, no-baseline comparison and flagged a missing market-only baseline as blocking RQ3. That gap has since been closed (Model Contract Protocol, MCP v1.0). This section now describes the frozen model roster and comparison procedure; see `model_contract.md` (the binding rulebook this section summarises) and `baseline_model_specification.md`/`07_model_plan.md` for full detail. This correction is logged in `10_decision_log.md`.**

**Approved models (MCP v1.0):**

The feature scopes below describe the completed FES v1.1 modelling boundary. All model and RQ2/RQ3 comparison artefacts listed here are current and hash-bound by Notebook 06 or 07 validation.

| Role | Model | Feature scope |
|---|---|---|
| Baseline | `Baseline_LASSO` | Market category only (27 features) |
| Event-enhanced candidate | Event_LASSO | Full 92-feature set |
| Event-enhanced candidate | XGBoost | Full 92-feature set |
| Event-enhanced candidate | LightGBM | Full 92-feature set |
| Feature-importance tool (RQ2 only, not an RQ3 candidate) | Random Forest | Full 92-feature set |

`Baseline_LASSO` and Event_LASSO are the same algorithm (regularised linear regression via `LassoCV`) trained as two distinct model objects with different feature scopes and different roles: one establishes the floor RQ3 must clear, the other is a full-feature candidate tested against that floor. They are never conflated or stored as the same artefact.

**Validation protocol:** `TimeSeriesSplit` cross-validation, 5 folds, random seed fixed at 42 throughout, identically for the baseline and every event-enhanced candidate. `Baseline_LASSO` and Event_LASSO are tuned via `LassoCV`'s automatic coordinate-descent alpha-path search; XGBoost and LightGBM are tuned via `RandomizedSearchCV` constrained to respect time-series ordering (no shuffling across folds).

**Evaluation metrics:** every model is scored on the identical frozen metric set — RMSE, MAE, R², directional accuracy, Information Coefficient (Spearman rank correlation between prediction and actual return) — together with, for the direction-as-binary-class framing, precision/recall/F1/ROC-AUC and a confusion matrix, residual diagnostics (Durbin-Watson, Jarque-Bera, heteroskedasticity correlation), empirical residual-quantile prediction intervals, a block-bootstrap 95% CI on test RMSE, and a Wilson-score 95% CI on directional accuracy.

**Promotion criteria (the test an event-enhanced model must clear to be reported as beating the baseline):** on the test split, (1) its RMSE must be significantly lower than `Baseline_LASSO`'s via a one-sided Diebold-Mariano test, **and** (2) its directional accuracy must be significantly higher via a one-sided two-proportion z-test, both assessed at a Bonferroni-corrected α = 0.05 / 3 = 0.0167 (three event-enhanced candidates compared against one baseline). A model clearing only one leg is a mixed result and is not reported as beating the baseline.

**Explainability:** SHAP (`TreeExplainer` for XGBoost/LightGBM; the exact linear decomposition for Event_LASSO) computed on the test set, producing global importance rankings and per-feature attribution.

**RQ2 importance tool:** a fixed `RandomForestRegressor` (500 trees, seed 42, all 92 features) produces the descriptive impurity-importance ranking. It is not tuned or evaluated as an RQ3 predictive candidate. The 0.001 threshold controls reporting only; the complete 92-row ranking is retained.

**Inputs:** `data/processed/feature_matrix.parquet`, `feature_profile.json` (persisted scaling parameters).
**Outputs:** `models/baseline/baseline_lasso.joblib`, `models/baseline/baseline_model_metadata.json`, `reports/baseline/baseline_metrics.json`, `reports/baseline/baseline_predictions.parquet`, `reports/baseline/baseline_model_validation.json`; current event models plus Random Forest under `models/event/`; and `reports/model_comparison/{model_comparison.parquet,statistical_tests.json,event_model_predictions.parquet,feature_importance.parquet,shap_values_*.parquet,shap_importance_summary.parquet,model_evaluation_validation.json}`.
**Notebooks:** `06_model_training.ipynb` (baseline), `07_model_evaluation.ipynb` (event-enhanced training, statistical comparison, and RQ3 verdict).

---

## Reproducibility notes applicable to every stage above

- `config.yaml: model.random_seed = 42` fixes randomness project-wide; no notebook should override this locally.
- Every processed file is derived, never hand-edited — if a `data/processed/*.parquet` file is missing or looks wrong, re-run the notebook named in its row of `05_data_dictionary.md`, don't patch the file directly.
- No step in this methodology requires a paid API key; FRED and NewsAPI keys (both currently unrotated — see `DATSCI7030_Repository_Audit_Report.ipynb` §1) are optional/legacy paths only.
