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

**Updated 2026-07-06 — this section previously described the pre-freeze, 91-feature/52-selected pipeline. It now describes the frozen Feature Engineering Specification (FES v1.0), the only feature set any RQ2/RQ3 model may be trained or reported against. See `feature_contract.md` (the binding rulebook this section summarises) and `06_feature_dictionary.md` (per-feature detail) for the authoritative versions of everything below; this correction is logged in `10_decision_log.md`.**

`feature_matrix.parquet` is built from exactly two upstream artefacts — `data/processed/master_dataset.parquet` (Dataset v1.0) and `data/processed/car_results.parquet` (the Phase-4 event-study output) — and from no other processed file. Six feature categories are engineered (see `06_feature_dictionary.md` for the complete, column-level list):

| Category | Count | Examples |
|-------|-------|----------|
| Market | 27 | log returns, lagged returns (1/3/5/10/21d), cumulative returns, rolling volatility, momentum, RSI-14, Bollinger Band width/position |
| Macro & VIX | 16 | VIX level/change, Fed Funds Rate, CPI month-on-month, Treasury yields, yield-curve spread |
| Sentiment | 25 | daily sentiment by event type, rolling mean/std, sentiment momentum |
| Event | 14 | event-type day counts, `mean_car`, days-since-last-CAR-event, significant-event flags |
| Temporal | 5 | cyclically encoded day-of-week and month, ordinal quarter |
| Interaction | 8 | sentiment × VIX regime, monetary × rate-change, event-significance × momentum |
| **Total engineered** | **95** | — |

**Feature selection:** unlike the pre-freeze pipeline, FES v1.0 does not select a subset of a larger candidate pool by an importance threshold — all 95 engineered features are the frozen matrix. Variance (< 1e-8), correlation (|r| > 0.90), and VIF (> 10) checks are still run (`feature_matrix_validation.json`) but serve as **informational flags for the dissertation's multicollinearity discussion**, not an automatic-drop mechanism — a flagged feature is documented in `06_feature_dictionary.md`, not silently removed.

**Target variable:** `fwd_return_1d` (forward 1-day SPY log return) is the sole frozen target. Forward 5-day/10-day return targets are explicitly out of scope for FES v1.0 (`feature_contract.md`) — not engineered, not a secondary robustness check.

**Row scope:** after all features are constructed, rows with any undefined value are dropped (the binding constraint is `days_since_car_event`, undefined before the first recorded CAR event on 2016-01-05), yielding 2,511 rows spanning 2016-01-05 to 2025-12-29.

**Train/test split:** strict chronological split — train 2016-01-05 → 2022-12-30 (1,761 rows, 70.1%), test 2023-01-03 → 2025-12-29 (750 rows, 29.9%). No shuffling; this is a forecasting task and a random split would leak future information into training via overlapping rolling-window features.

**Scaling:** per-feature mean and standard deviation computed on the training split only and persisted (`feature_profile.json`), then applied as `(x − mean) / std` uniformly to every engineered feature (including binary flags) in both splits. The scaler is never refit on the full matrix or on test data.

**Baseline eligibility:** the Market category (27 features) is the only category a market-only baseline model may read; the remaining 68 features (Macro & VIX, Sentiment, Event, Temporal, Interaction) are event-enhanced-model-only. This boundary is enforced at the contract level (`feature_contract.md` "Baseline eligibility"), not left to per-notebook discretion, and is the mechanism that prevents event information from leaking into the RQ3 baseline.

**Inputs:** `data/processed/master_dataset.parquet`, `data/processed/car_results.parquet`.
**Outputs:** `data/processed/feature_matrix.parquet` (2,511 rows × 98 columns, incl. date/split/target), `feature_profile.json`, `feature_matrix_validation.json`.
**Notebook:** `05_feature_engineering.ipynb`.

---

## 5. Machine Learning Methodology (→ RQ3)

**Updated 2026-07-06 — this section previously described a three-model, no-baseline comparison and flagged a missing market-only baseline as blocking RQ3. That gap has since been closed (Model Contract Protocol, MCP v1.0). This section now describes the frozen model roster and comparison procedure; see `model_contract.md` (the binding rulebook this section summarises) and `baseline_model_specification.md`/`07_model_plan.md` for full detail. This correction is logged in `10_decision_log.md`.**

**Approved models (MCP v1.0):**

| Role | Model | Feature scope |
|---|---|---|
| Baseline | `Baseline_LASSO` | Market category only (27 features) |
| Event-enhanced candidate | Event_LASSO | Full 95-feature set |
| Event-enhanced candidate | XGBoost | Full 95-feature set |
| Event-enhanced candidate | LightGBM | Full 95-feature set |
| Feature-importance tool (RQ2 only, not an RQ3 candidate) | Random Forest | Full 95-feature set |

`Baseline_LASSO` and Event_LASSO are the same algorithm (regularised linear regression via `LassoCV`) trained as two distinct model objects with different feature scopes and different roles: one establishes the floor RQ3 must clear, the other is a full-feature candidate tested against that floor. They are never conflated or stored as the same artefact.

**Validation protocol:** `TimeSeriesSplit` cross-validation, 5 folds, random seed fixed at 42 throughout, identically for the baseline and every event-enhanced candidate. `Baseline_LASSO` and Event_LASSO are tuned via `LassoCV`'s automatic coordinate-descent alpha-path search; XGBoost and LightGBM are tuned via `RandomizedSearchCV` constrained to respect time-series ordering (no shuffling across folds).

**Evaluation metrics:** every model is scored on the identical frozen metric set — RMSE, MAE, R², directional accuracy, Information Coefficient (Spearman rank correlation between prediction and actual return) — together with, for the direction-as-binary-class framing, precision/recall/F1/ROC-AUC and a confusion matrix, residual diagnostics (Durbin-Watson, Jarque-Bera, heteroskedasticity correlation), empirical residual-quantile prediction intervals, a block-bootstrap 95% CI on test RMSE, and a Wilson-score 95% CI on directional accuracy.

**Promotion criteria (the test an event-enhanced model must clear to be reported as beating the baseline):** on the test split, (1) its RMSE must be significantly lower than `Baseline_LASSO`'s via a one-sided Diebold-Mariano test, **and** (2) its directional accuracy must be significantly higher via a one-sided two-proportion z-test, both assessed at a Bonferroni-corrected α = 0.05 / 3 = 0.0167 (three event-enhanced candidates compared against one baseline). A model clearing only one leg is a mixed result and is not reported as beating the baseline.

**Explainability:** SHAP (`TreeExplainer` for XGBoost/LightGBM; the exact linear decomposition for Event_LASSO) computed on the test set, producing global importance rankings and per-feature attribution.

**Inputs:** `data/processed/feature_matrix.parquet`, `feature_profile.json` (persisted scaling parameters).
**Outputs:** `models/baseline/baseline_lasso.joblib`, `models/baseline/baseline_model_metadata.json`, `reports/baseline/baseline_metrics.json`, `reports/baseline/baseline_predictions.parquet`; `models/event/event_model_metadata.json`, `reports/model_comparison/model_comparison.parquet`, `reports/model_comparison/statistical_tests.json`, `reports/model_comparison/feature_importance.parquet`, `reports/model_comparison/shap_values_*.parquet`.
**Notebooks:** `06_model_training.ipynb` (baseline), `07_model_evaluation.ipynb` (event-enhanced training, statistical comparison, and RQ3 verdict).

---

## Reproducibility notes applicable to every stage above

- `config.yaml: model.random_seed = 42` fixes randomness project-wide; no notebook should override this locally.
- Every processed file is derived, never hand-edited — if a `data/processed/*.parquet` file is missing or looks wrong, re-run the notebook named in its row of `05_data_dictionary.md`, don't patch the file directly.
- No step in this methodology requires a paid API key; FRED and NewsAPI keys (both currently unrotated — see `DATSCI7030_Repository_Audit_Report.ipynb` §1) are optional/legacy paths only.
