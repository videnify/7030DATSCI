# 03 — Methodology

**Purpose:** The full technical methodology for every analytical stage of the pipeline — event study, causal inference, NLP/sentiment, feature engineering, and machine learning — with enough detail that another researcher could reproduce each step without reading the notebook source first.
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `02_hypotheses.md`, `config.yaml` (all parameters below are read from there, not hand-picked per notebook).
**Update Frequency:** Updated whenever a methodological choice changes (e.g. estimation window length, model architecture); every change must reference a `10_decision_log.md` entry.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 (Methodology) in full.

**SAP v1.0 note (2026-07-04):** Every parameter and method below is now governed by the frozen Statistical Analysis Plan — see `statistical_analysis_plan.md` (global policy), `statistical_decision_matrix.md` (test matrix), `statistical_assumptions.md` (assumption checks, including the 🆕 stationarity, multicollinearity, and outlier policies not previously written down here), and `dataset_contract.md` (consumption rules for `master_dataset.parquet`, which Phase 5 below must read from rather than re-deriving). Any methodological change from this point forward requires a Version 2 SAP amendment and a `10_decision_log.md` entry — this document should not silently diverge from the SAP suite.

---

## 1. Event Study Methodology (→ RQ1)

**Model:** Market-model event study (Fama, Fisher, Jensen & Roll, 1969 tradition), implemented in `src/causal_engine.py::EventStudy`.

**Parameters** (from `config.yaml`):
| Parameter | Value |
|-----------|-------|
| Estimation window | 120 trading days before the event window |
| Event window (pre) | 5 trading days before the event date |
| Event window (post) | 10 trading days after the event date |

**Procedure:**
1. For each event date, fit a market-model regression of SPY log returns on a market proxy over the 120-day estimation window ending just before the event window opens.
2. Predict "normal" expected returns during the event window from the fitted model; Abnormal Return (AR) = actual − expected, per day.
3. Cumulative Abnormal Return (CAR) = sum of AR across the event window (day −5 to +10).
4. Aggregate to Cumulative Average Abnormal Return (CAAR) per event type (monetary, geopolitical, regulatory, trade, energy, health, labour) by averaging CAR across all events of that type.
5. Significance-test CAAR against zero (see `04_statistics_plan.md`).

**Inputs:** `data/raw/spy_ohlcv.parquet`, `data/processed/events_tagged.parquet` (or `high_impact_events.parquet` for the high-impact-only robustness subset).
**Outputs:** `data/processed/car_results.parquet` (1,796 event-level CAR records).
**Notebook:** `04_causal_analysis.ipynb`.

---

## 2. Causal Inference Methodology (→ RQ1)

Event-study CAR establishes *association*, not causation — the market-model residual could reflect confounding (e.g. an event coinciding with a volatility spike that would have moved price regardless). To address this, a second, causal layer is applied.

**Framework:** DoWhy (Microsoft Research) structural causal model.

**Causal DAG** (see `docs/architecture/archive/causal_dag_dowhy_professional_clean.svg` — archived, Architecture SVG Cleanup 2026-07-06): Treatment = event sentiment → Outcome = next-day SPY return. Confounders: VIX regime, prior-day market return. **Note (Sentiment Engine Freeze v1.0, 2026-07-06):** the already-frozen `causal_estimates.parquet` used the lexicon sentiment score as its treatment variable at the time it was computed (see `05_data_dictionary.md`) — that historical result is not being re-run. Per SEF v1.0, FinBERT is now the project's official primary sentiment engine; any future re-run of this causal model should use FinBERT sentiment as the primary treatment, with the lexicon score retained only as a fallback/historical comparator.

**Estimation method:** `backdoor.linear_regression` (from `config.yaml: causal.method`) — adjusts for the identified confounder set via linear regression on the backdoor-adjusted formula.

**Refutation tests** (from `config.yaml: causal.refutation_tests`), run against the primary estimate to check robustness:
1. `random_common_cause` — adds a random covariate; estimate should not change materially.
2. `placebo_treatment_refuter` — replaces the real treatment with random noise; estimate should collapse toward zero.
3. `data_subset_refuter` — re-estimates on a random subset of the data; estimate should remain stable in sign and rough magnitude.

**Inputs:** `data/processed/car_results.parquet`, `data/raw/vix.parquet`.
**Outputs:** `data/processed/causal_estimates.parquet` (causal effect, 95% CI, n_obs, n_nonzero per event type × sentiment method).
**Notebook:** `04_causal_analysis.ipynb`.

---

## 3. NLP & Sentiment Methodology (→ RQ1, RQ2)

**Event classification:** Rule-based keyword matching (not ML) tags each of the 11,629 APP presidential documents into one of eight categories: monetary, geopolitical, regulatory, trade, energy, health, labour, other. Deterministic and inspectable — a deliberate choice over an ML classifier given the category definitions are policy-domain-specific and a labelled training set does not exist (see `10_decision_log.md`).

**Sentiment scoring — primary engine and fallback (Sentiment Engine Freeze v1.0, 2026-07-06):**
1. **FinBERT** (`ProsusAI/finbert`, via `src/event_detector.py::EventDetector`) — the project's **official, primary sentiment engine**. A transformer pretrained on financial-news sentiment, scored on document *titles* (not full text — see `11_limitations.md`). Parameters from `config.yaml: nlp` (batch_size 32, max_length 512, confidence threshold 0.7). FinBERT-generated sentiment is used to construct `events_tagged.parquet`, `daily_sentiment.parquet`, and all downstream datasets.
2. **Lexicon scorer** — a curated financial/political keyword lexicon, retained only as a **fallback mechanism** (used when FinBERT/PyTorch is unavailable in the runtime environment) and as a **historical prototype** predating this freeze. It is not the primary methodology used to generate the frozen datasets.

**Method selection (superseded 2026-07-06 — see `10_decision_log.md`, SEF v1.0):** An earlier decision had designated the lexicon scorer as primary, reasoning that FinBERT's title-level output on formal presidential language is 95.3% neutral (vs. 73.1% neutral for the lexicon method) — a domain-mismatch effect from FinBERT being trained on financial-news headlines, not policy speech. Live execution of `03_event_detection.ipynb` (Mission 03, 2026-07-06) confirmed the actual cached/frozen sentiment data is 99.2% FinBERT-sourced, not lexicon-sourced as previously documented. The Project Director resolved this discrepancy by ratifying FinBERT as the official primary engine to match the real pipeline output, rather than re-scoring the catalogue with the lexicon method. This is a documentation/governance correction only — no statistical outputs changed.

**FOMC enrichment:** FOMC meeting dates (`data/raw/fomc_dates.parquet`, 89 meetings) are merged into the same event catalogue with `decision` and `is_surprise` fields, giving the "monetary" event type a structured, dated anchor alongside the unstructured presidential-communication events.

**GDELT integration:** Daily Goldstein-scale and tone scores from GDELT are merged as a geopolitical-risk confounder candidate. **Currently limited to a 5-day proof-of-concept sample** (`data/raw/gdelt_sample.parquet`) — see `11_limitations.md` before treating any GDELT-derived feature as final.

**Inputs:** `data/raw/app_presidential_documents.parquet`, `data/raw/fomc_dates.parquet`, `data/raw/gdelt_sample.parquet`.
**Outputs:** `data/processed/events_tagged.parquet`, `daily_sentiment.parquet`, `high_impact_events.parquet`, `gdelt_daily_risk.parquet`.
**Notebook:** `03_event_detection.ipynb`.

---

## 4. Feature Engineering Methodology (→ RQ2, RQ3)

Six feature groups are built from the outputs of Phases 1–4 (see `06_feature_dictionary.md` for the complete, column-level list):

| Group | Count | Examples |
|-------|-------|----------|
| Price & returns | 13 | log returns, lagged returns (1/3/5/10/21d), cumulative returns |
| Technical indicators | 14 | rolling volatility, momentum, RSI-14, Bollinger Band width/position |
| Sentiment | 25 | daily sentiment by event type, rolling mean/std, sentiment momentum |
| Event indicators | 14 | event-type dummies, days-since-last-high-impact-event, `mean_car` |
| Macro & VIX | 16 | VIX level/change, Fed Funds Rate, CPI MoM, yield-curve spread |
| Interactions | 8 | sentiment × VIX regime, high-impact-event × momentum |
| **Total engineered** | **91** | — |
| **Selected (RF importance > 0.001)** | **52** | — |

**Feature selection:** Random Forest impurity importance, threshold 0.001, computed once on the training period only (no test-period leakage into the selection step itself). As of SAP v1.0, this is preceded by variance (< 1e-8), correlation (|r| > 0.90), and VIF (> 10) threshold checks — see `04_statistics_plan.md` "Feature-engineering thresholds" and `statistical_assumptions.md` (Multicollinearity) — and corroborated, not replaced, by a Mutual Information ranking.

**Target variable:** `fwd_return_1d` (forward 1-day log return) is the primary target (`models/model_metadata.json: primary_target`). Forward 5-day and 10-day returns are also engineered as secondary targets for robustness checks, not used in the primary RQ3 comparison.

**Train/test split:** Strict chronological split — train 2015-01-05 → 2022-12-31 (2,013 rows, 73%), test 2023-01-01 → 2025-12-29 (750 rows, 27%). No shuffling; this is a forecasting task and any random split would leak future information into training via overlapping rolling-window features.

**Scaling:** `StandardScaler` fit on the training set only (`data/processed/scaler.pkl`), applied to both splits — never re-fit on test data.

**Inputs:** `data/processed/events_tagged.parquet`, `daily_sentiment.parquet`, `data/raw/prices.parquet`, `vix.parquet`, `macro_indicators.parquet`.
**Outputs:** `data/processed/model_features.parquet` (2,763 rows × 95 cols), `feature_metadata.parquet`, `scaler.pkl`.
**Notebook:** `05_feature_engineering.ipynb`.

---

## 5. Machine Learning Methodology (→ RQ3)

**Candidate models:** LASSO (regularised linear regression, interpretable baseline-complexity model), XGBoost, LightGBM.

**Validation protocol:** `TimeSeriesSplit` cross-validation, 5 folds (`config.yaml: model.cv_splits`), random seed fixed at 42 throughout for reproducibility. Hyperparameter tuning via `RandomizedSearchCV` constrained to respect time-series ordering (no shuffling across folds).

**Hyperparameters actually selected** (`models/model_metadata.json`):
| Model | Key hyperparameters |
|-------|---------------------|
| LASSO | α = 0.000518 |
| XGBoost | n_estimators 600, learning_rate 0.01, max_depth 6, subsample 0.7, colsample_bytree 0.6, reg_λ 1.5, reg_α 0.1, min_child_weight 5 |
| LightGBM | n_estimators 200, learning_rate 0.01, num_leaves 127, max_depth 5, subsample 0.9, colsample_bytree 0.6, reg_λ 0.1, reg_α 0.01 |

**⚠️ Missing baseline (RQ3-blocking):** All three models above are trained on the same 52-feature (price + technical + sentiment + event + macro) matrix. No model in the current comparison is trained on price/technical features only. See `07_model_plan.md` for the specification of the missing baseline and `01_research_questions.md` (RQ3 status) for why this blocks a full RQ3 answer.

**Explainability:** SHAP (TreeExplainer for XGBoost/LightGBM; LinearExplainer for LASSO) computed on the test set, producing global summary plots and per-feature dependence plots.

**Inputs:** `data/processed/model_features.parquet`, `feature_metadata.parquet`, `scaler.pkl`.
**Outputs:** `models/lasso.pkl`, `xgboost.json`, `lightgbm.txt`, `model_metadata.json`; `data/processed/test_predictions.parquet`, `shap_values.parquet`.
**Notebooks:** `06_model_training.ipynb` (training/tuning), `07_model_evaluation.ipynb` (extended evaluation, residual diagnostics, SHAP deep-dive).

---

## Reproducibility notes applicable to every stage above

- `config.yaml: model.random_seed = 42` fixes randomness project-wide; no notebook should override this locally.
- Every processed file is derived, never hand-edited — if a `data/processed/*.parquet` file is missing or looks wrong, re-run the notebook named in its row of `05_data_dictionary.md`, don't patch the file directly.
- No step in this methodology requires a paid API key; FRED and NewsAPI keys (both currently unrotated — see `DATSCI7030_Repository_Audit_Report.ipynb` §1) are optional/legacy paths only.
