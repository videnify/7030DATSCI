# 04 — Statistics Plan

**Purpose:** Every statistical test used anywhere in the pipeline, why it was chosen over alternatives, its assumptions, how those assumptions are checked, and how multiple-comparison risk is handled. Written so that a statistics-literate examiner can audit the project's inferential claims without re-deriving them from the notebooks.
**Owner:** Ibrahim Haroun.
**Dependencies:** `02_hypotheses.md` (each test below answers a specific H0/H1 pair), `03_methodology.md`.
**Update Frequency:** Updated whenever a new statistical test is introduced or an assumption check fails and a remedy is applied — log the remedy in `10_decision_log.md`.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.4 (Statistical Analysis Plan) and the significance-reporting conventions used throughout Chapter 4 (Results).

**⚠️ SAP v1.0 status (2026-07-04):** This document is now the **operational, per-notebook layer** of the frozen Statistical Analysis Plan — the global policy freeze (α, one-sided/two-sided rules, outlier/transformation/scaling/stationarity policy), the master test matrix, the assumption matrix, and the reporting conventions have moved to a dedicated SAP suite so this document doesn't have to carry everything at once:
- `statistical_analysis_plan.md` — global policy freeze (Part A), RQ→statistics mapping (Part B), hypothesis freeze summary (Part C)
- `statistical_decision_matrix.md` — master test matrix (Part F), model comparison protocol (Part K)
- `statistical_assumptions.md` — assumption matrix (Part D), time-series diagnostics (Part H)
- `statistical_reporting_guidelines.md` — reporting/CI/effect-size conventions, figure requirements (Part L)
- `dataset_contract.md` — consumption rules for `master_dataset.parquet`

This document keeps the per-test narrative detail (why each test was chosen, what it found so far) and adds the per-notebook statistical plan (Part E) below, which did not previously exist anywhere in the Research Bible. Nothing already written below has been changed in substance — only extended.

---

## General conventions

- Significance threshold: α = 0.05 unless stated otherwise.
- All p-values are two-tailed unless a directional hypothesis is explicitly stated.
- Every reported "significant" result must state: test used, statistic, p-value, sample size, and the multiple-comparisons correction applied (if any) — a bare p-value without these is not acceptable anywhere in this project's outputs.
- Effect sizes (not just p-values) are reported wherever possible — statistical significance without an effect-size statement invites overclaiming, especially with the sample sizes here (thousands of trading days).

---

## Event Study Tests (→ H1 / RQ1)

**Primary test:** One-sample t-test of event-level CAR against H0: mean = 0, per event type. Implemented via `scipy.stats.ttest_1samp` (or equivalent) inside `src/causal_engine.py::EventStudy`.

**Assumptions:** Approximate normality of CAR within each event-type bucket (checked via visual QQ-plot / skewness-kurtosis inspection in `02_eda.ipynb`); independence across events (a known violation risk — see below).

**Known violation — event clustering:** Presidential communications and FOMC meetings are not independent draws in time; clustering (e.g. several statements in the same week around a crisis) inflates the effective sample size used by a naive t-test. **Mitigation:** cross-sectional t-test on CAAR (averaging first, testing second) rather than pooling all raw CAR observations into one t-test, which is the standard event-study-literature remedy for this exact problem.

**Multiple comparisons:** Five to eight event-type buckets are tested per sentiment method. A Benjamini-Hochberg False Discovery Rate correction is applied across the event-type family of tests before any single event type's result is reported as "significant" in the dissertation — a raw, uncorrected p < 0.05 across 5–8 simultaneous tests carries a meaningfully inflated false-positive risk and should not be reported as-is.

**Causal-effect confidence interval:** DoWhy's `backdoor.linear_regression` estimator reports a 95% CI directly from the regression's standard errors; "significant" for the causal estimate means the CI excludes zero, reported alongside the point estimate, never as a bare point estimate.

**Outputs checked against:** `data/processed/car_results.parquet` (`t_stat`, `p_value`, `significant` columns already computed per-event), `causal_estimates.parquet` (`ci_lower`, `ci_upper`).

---

## Feature Importance Tests (→ H2 / RQ2)

**Primary method:** Random Forest impurity-based importance (threshold 0.001 for feature retention), which is **not** a hypothesis test in the classical sense — it is a ranking, not a p-value. This is a deliberate choice: RQ2 asks "which features contribute most," a ranking question, not "is feature X's contribution non-zero," a testing question.

**Corroboration, not duplication:** SHAP values on the held-out test set are used to check that impurity-importance rankings are not a training-set artefact (impurity importance is known to be biased toward high-cardinality/continuous features) — a feature that ranks highly by impurity importance but shows inconsistent SHAP sign/magnitude on test data should be reported with that caveat, not silently kept at face value.

**No p-value is attached to "feature X is the most important"** — this would require a permutation test with a null distribution (feature values shuffled, importance re-computed, repeated N times) which is not currently implemented. If added, log it in `10_decision_log.md` and update this section; until then, importance rankings should be described as descriptive, not inferential, in the dissertation.

**Outputs checked against:** `data/processed/feature_metadata.parquet` (`importance`, `selected`, `group` columns), `shap_values.parquet`.

---

## Model Comparison Tests (→ H3 / RQ3)

**Planned primary test (not yet run — depends on the missing baseline, see `07_model_plan.md`):**
1. **RMSE comparison:** Diebold–Mariano test on the paired squared-error series between the full-feature model and the price-only baseline (both evaluated on the identical test-period dates), or a block-bootstrap CI on the RMSE difference if DM-test assumptions (stationarity of the loss differential) are not met.
2. **Directional accuracy comparison:** Two-proportion z-test (or exact binomial test given n=750 test days) on the paired correct/incorrect direction calls between the two models.

**Multiple comparisons:** Three candidate models (LASSO, XGBoost, LightGBM) are each compared against the baseline — a Bonferroni correction (α/3 = 0.0167 per test) is applied before declaring any single model's improvement "significant," since three simultaneous comparisons against the same baseline is a family of tests, not one.

**Overfitting diagnostic (already run, not a formal hypothesis test but load-bearing for interpretation):** Train-vs-test metric gap per model. Current numbers (`data/processed/model_comparison.parquet`):

| Model | Split | R² | Dir. Acc |
|-------|-------|-----|----------|
| LASSO | train | 0.092 | 0.562 |
| LASSO | test | 0.033 | 0.564 |
| XGBoost | train | 0.554 | 0.753 |
| XGBoost | test | 0.030 | 0.524 |
| LightGBM | train | 0.221 | 0.610 |
| LightGBM | test | 0.031 | 0.551 |

XGBoost's train→test collapse (R² 0.554 → 0.030) is the clearest overfitting signature of the three and should be reported as such, not smoothed over by only quoting test-set numbers.

**Residual diagnostics (LASSO, current best model — `models/residual_diagnostics.json`):** Durbin-Watson 2.02 (no material autocorrelation), Jarque-Bera p ≈ 0.0 (residuals are not normally distributed — expected for financial returns, heavy-tailed per kurtosis 17.26), heteroskedasticity correlation 0.199 (mild). These diagnostics support using non-parametric/bootstrap significance tests over tests that assume Gaussian residuals when formally comparing models.

**Outputs checked against:** `data/processed/model_comparison.parquet`, `evaluation_summary.parquet`, `models/residual_diagnostics.json`.

---

## Multiple Comparisons — project-wide policy

| Family of tests | Count | Correction |
|------------------|-------|------------|
| Event-type CAAR tests (RQ1) | 5–8 (× 2 sentiment methods) | Benjamini-Hochberg FDR |
| Model-vs-baseline comparisons (RQ3) | 3 (LASSO, XGB, LGB vs. baseline) | Bonferroni (α/3) |
| Feature importance ranking (RQ2) | Descriptive — no correction applied (not a hypothesis-test family) | N/A |

## Assumption-violation escalation policy

If an assumption check fails materially (e.g. residuals are strongly non-normal, as already observed for LASSO), the response is: (1) note it explicitly in `09_results_log.md`, (2) prefer the non-parametric/robust alternative test already named above, (3) never silently proceed with the parametric test's p-value as if the check had passed.

---

## Feature-engineering thresholds (frozen, SAP v1.0 — 🆕 not previously written down)

Only the Random Forest importance threshold (0.001) was frozen before this SAP. The following were used implicitly or not at all, and are now fixed prospectively for Mission 05 (Feature Matrix v1.0):

| Threshold | Frozen value | Why |
|---|---|---|
| Variance threshold | Drop if training-split variance < 1e-8 | Removes near-constant features before they can dilute importance rankings with noise |
| Correlation threshold | Flag if pairwise \|Pearson r\| > 0.90 (train split only) | Surfaces near-duplicate features for interpretability review — flagged, not automatically dropped (see `statistical_assumptions.md`, Multicollinearity row) |
| VIF threshold | Flag if VIF > 10 | Standard multicollinearity severity threshold; matters for LASSO coefficient interpretation, not for tree-model predictive performance |
| RF importance threshold | Retain if importance > 0.001 (already frozen, Phase 5) | Unchanged — this is the one threshold already in use and already produced the RQ2 result |
| Mutual Information | Corroboration only, no independent threshold — cross-checked against the RF ranking, not used to select/drop features on its own | Avoids introducing a second, potentially conflicting "primary" selection method after RQ2 has already been answered using RF+SHAP |

Full reasoning for each threshold, and the assumption each protects, is in `statistical_assumptions.md` (Multicollinearity row) and `statistical_decision_matrix.md` (Feature Selection stage rows).

---

## Prediction intervals (frozen, SAP v1.0 — 🆕 not previously produced)

RQ3's model comparison has so far reported only point predictions and aggregate error metrics (RMSE, MAE, R², directional accuracy). A point forecast without a calibrated interval understates how uncertain a single next-day return prediction actually is. **Method (frozen for Mission 07/08, not yet run):** empirical residual-quantile prediction intervals — compute the training-set residual distribution per model, take the 5th/95th percentile (90% PI) and 2.5th/97.5th percentile (95% PI), and apply as a constant-width band around each test-set point prediction. A more sophisticated conditional (heteroskedasticity-aware) interval is not adopted at v1.0, given the already-documented mild heteroskedasticity (correlation 0.199) does not currently justify the added complexity — this is a candidate Version 2 SAP amendment if a supervisor wants it.

---

## Part E — Per-notebook statistical plan (🆕 not previously tabulated)

| Notebook | Purpose | RQ | Variables | Statistics | Plots | Tables | Tests | Outputs | Interpretation |
|---|---|---|---|---|---|---|---|---|---|
| `03_exploratory_analysis.ipynb` (repo: `02_eda.ipynb`) | Describe distributions, market behaviour, event frequency; run stationarity checks before any modelling | Context (all RQs) | SPY/QQQ/GLD/TLT returns, VIX, macro series, event counts | Skewness, kurtosis, descriptive stats | Histograms, QQ-plots, rolling-stat plots, ACF/PACF | Descriptive summary table | ADF, KPSS (🆕, not yet run) | Distribution figures, stationarity flags per series | Establishes the empirical baseline later phases test against; confirms log returns are the correct modelling scale |
| `04_event_study.ipynb` (repo: `04_causal_analysis.ipynb`) | Abnormal returns, CAR, CAAR, significance testing, causal estimate | RQ1 | Event-window CAR by type, sentiment, VIX regime | CAAR, Cohen's d | `04a`–`04d` figures | `car_results.parquet`, `causal_estimates.parquet` | One-sample t-test (CAAR), DoWhy backdoor estimate + refutation tests, BH-FDR correction (🟡 pending) | CAR/CAAR table, causal effect + 95% CI | Minority of events move price significantly; pooled causal effect is significant and positive |
| `05_sentiment_analysis.ipynb` (repo: folded into `03_event_detection.ipynb`) | Text preprocessing, sentiment scoring, event classification | RQ1 (methodology) → RQ2 | Document titles, event type, sentiment score (lexicon, FinBERT) | Neutral/positive/negative share by method | `03a`–`03d` figures | `events_tagged.parquet`, `daily_sentiment.parquet` | Descriptive comparison (no formal hypothesis test — a method-selection decision, not an inferential claim) | Sentiment distributions by method | FinBERT is the project's official primary sentiment engine (Sentiment Engine Freeze v1.0, 2026-07-06); lexicon retained as fallback/historical method — see `10_decision_log.md` |
| `06_feature_engineering.ipynb` (repo: `05_feature_engineering.ipynb`) | Rolling returns, lags, volatility, technical indicators, event/macro features, selection | RQ2, RQ3 | 88 candidate engineered features | Variance, correlation, VIF, RF importance, Mutual Information (corroboration) | `05a`–`05c` figures | `feature_metadata.parquet` | Variance/correlation/VIF threshold checks (🆕), RF importance ranking, MI corroboration | Selected 52/88-feature set | Event (`mean_car`) and macro (`vix_vs_ma`) features rank alongside price signal |
| `07_machine_learning.ipynb` (repo: `06_model_training.ipynb`) | Baseline model, LASSO/XGBoost/LightGBM training, cross-validation | RQ3 | `fwd_return_1d`, full vs. baseline feature sets | RMSE, MAE, R², Dir. Acc., IC | `06a`–`06d` figures | `model_comparison.parquet` | `TimeSeriesSplit` CV, `RandomizedSearchCV` tuning (baseline model ⬜ not yet trained) | Trained models, test predictions | Cannot report an RQ3 conclusion until the baseline exists |
| `08_model_evaluation.ipynb` (repo: `07_model_evaluation.ipynb`) | ROC/precision/recall-style diagnostics, confusion matrix framing, feature importance, SHAP, final discussion | RQ2, RQ3 | Test-set predictions, residuals, SHAP values | Durbin-Watson, Jarque-Bera, heteroskedasticity correlation; DM test + two-proportion z-test (🆕, not yet run) | `07a`–`07d` figures | `evaluation_summary.parquet`, `shap_values.parquet` | Residual diagnostics (✅ run), model-vs-baseline paired tests (⬜ not yet run) | Extended metrics, SHAP deep-dive, final RQ3 verdict | RQ3 verdict pending baseline; XGBoost overfitting flagged |

Notebook names above follow the mission brief's 10-phase numbering; the current repository's 8-notebook implementation (right-hand column, "repo:") is mapped per `docs/00_project_workflow.md` — see that document and `10_decision_log.md` for why the two numbering schemes coexist. This table's RQ/statistics/test content applies regardless of which notebook filename ultimately hosts it.
