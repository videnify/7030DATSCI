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

**Historical correction, 2026-07-07 — this section previously prescribed a CAAR-averaged t-test with a Benjamini-Hochberg correction as the event-study significance procedure. At that checkpoint, cross-checking `04_causal_analysis.ipynb` Cell 7 against the prescription found that the notebook tested event-level CAR and had not yet applied the planned multiple-comparisons correction. The event-level test remains the implemented inferential unit; the missing BH-FDR reporting step was subsequently completed on 2026-07-15, as recorded below. See `10_decision_log.md` and `11_limitations.md` for the dated correction trail.**

**Primary test:** One-sample t-test (`scipy.stats.ttest_1samp`) of the pooled, event-level CAR values against H0: mean = 0, computed separately per event type, directly on `04_causal_analysis.ipynb` Cell 7's `car_df` grouping — not on event-type-averaged CAAR.

**Robustness check:** A Wilcoxon signed-rank test (`scipy.stats.wilcoxon`) is additionally reported alongside the t-test for each event type, as a non-parametric check that does not assume approximate normality of the per-event CAR distribution.

**Secondary test:** An independent two-sample comparison (Welch's t-test and Mann-Whitney U) of CAR for positive-sentiment versus negative-sentiment events, pooled across event types.

**Assumptions:** Approximate normality of CAR within each event-type bucket for the t-test (the Wilcoxon check above is reported precisely because this assumption is not guaranteed to hold); independence across events (a known violation risk — see below, and `11_limitations.md` L4).

**Known violation — event clustering, not currently mitigated:** Presidential communications and FOMC meetings are not independent draws in time; clustering (e.g. several statements in the same week around a crisis) inflates the effective sample size used by a naive t-test on pooled per-event CAR. The event-study literature's standard remedy — testing on CAAR (event-type averages) rather than pooled raw CAR — is **not currently implemented** in `04_causal_analysis.ipynb`; the notebook tests the pooled raw per-event CAR values directly. This is recorded as an open limitation, not a silently-accepted assumption.

**Multiple comparisons: completed 2026-07-15.** The five event-type tests (monetary, geopolitical, trade, regulatory and energy) are corrected as one family with `statsmodels.stats.multitest.multipletests(..., method='fdr_bh')` at q=0.05. Notebook 04 persists raw p, BH q, the final rejection flag, a 95% t interval for mean CAR and Cohen's d. No type is rejected; minimum q=0.5810.

**Causal-effect confidence interval:** DoWhy's `backdoor.linear_regression` estimator reports a 95% CI directly from the regression's standard errors; "significant" for the causal estimate means the CI excludes zero, reported alongside the point estimate, never as a bare point estimate.

**Outputs checked against:** `data/processed/car_results.parquet` (individual-window diagnostics), `event_type_statistics.parquet` (the five inferential mean-CAR rows), `rq1_reporting_validation.json` (hash-bound `PASS`) and `causal_estimates.parquet` (`ci_lower`, `ci_upper`).

---

## Feature Importance Tests (→ H2 / RQ2)

**Primary method:** Random Forest impurity-based importance (threshold 0.001 for feature retention), which is **not** a hypothesis test in the classical sense — it is a ranking, not a p-value. This is a deliberate choice: RQ2 asks "which features contribute most," a ranking question, not "is feature X's contribution non-zero," a testing question.

**Corroboration, not duplication:** SHAP values on the held-out test set are used to check that impurity-importance rankings are not a training-set artefact (impurity importance is known to be biased toward high-cardinality/continuous features) — a feature that ranks highly by impurity importance but shows inconsistent SHAP sign/magnitude on test data should be reported with that caveat, not silently kept at face value.

**No p-value is attached to "feature X is the most important"** — this would require a permutation test with a null distribution (feature values shuffled, importance re-computed, repeated N times) which is not currently implemented. If added, log it in `10_decision_log.md` and update this section; until then, importance rankings should be described as descriptive, not inferential, in the dissertation.

**Outputs checked against:** `reports/model_comparison/feature_importance.parquet` and `shap_importance_summary.parquet`, both validated by `model_evaluation_validation.json`.

---

## Model Comparison Tests (→ H3 / RQ3)

**Completed primary tests (FES v1.1, Notebook 07):**
1. **RMSE comparison:** Diebold–Mariano test on the paired squared-error series between the full-feature model and the price-only baseline (both evaluated on the identical test-period dates), or a block-bootstrap CI on the RMSE difference if DM-test assumptions (stationarity of the loss differential) are not met.
2. **Directional accuracy comparison:** Two-proportion z-test (or exact binomial test given n=750 test days) on the paired correct/incorrect direction calls between the two models.

**Multiple comparisons:** Three candidate models (LASSO, XGBoost, LightGBM) are each compared against the baseline — a Bonferroni correction (α/3 = 0.0167 per test) is applied before declaring any single model's improvement "significant," since three simultaneous comparisons against the same baseline is a family of tests, not one.

**Overfitting diagnostic (not a formal hypothesis test but load-bearing for interpretation):** Train-vs-test metric gap per model. Current numbers (`reports/model_comparison/model_comparison.parquet`):

| Model | Split | R² | Dir. Acc |
|-------|-------|-----|----------|
| Baseline_LASSO | train | 0.000 | 0.548 |
| Baseline_LASSO | test | −0.002 | 0.575 |
| Event_LASSO | train | 0.000 | 0.548 |
| Event_LASSO | test | −0.002 | 0.575 |
| XGBoost | train | 0.222 | 0.655 |
| XGBoost | test | −0.007 | 0.489 |
| LightGBM | train | 0.153 | 0.595 |
| LightGBM | test | −0.016 | 0.443 |

XGBoost's train→test collapse (R² 0.222 → −0.007) is the clearest overfitting signature of the current three candidates and should be reported as such, not smoothed over by quoting only held-out RMSE.

**Residual diagnostics (current validation files):** Baseline_LASSO/Event_LASSO Durbin-Watson is 2.112 with Jarque-Bera p≈0 and excess kurtosis 18.06; XGBoost and LightGBM Durbin-Watson values are 1.989 and 2.032, with Jarque-Bera p≈0. These heavy-tailed residuals justify the persisted block-bootstrap RMSE intervals and conservative interpretation.

**Outputs checked against:** `reports/model_comparison/model_comparison.parquet`, `statistical_tests.json`, and `reports/baseline/baseline_metrics.json`.

---

## Multiple Comparisons — project-wide policy

| Family of tests | Count | Correction |
|------------------|-------|------------|
| Event-type mean-CAR tests (RQ1) | 5 event types under the current combined APP + FOMC treatment | Benjamini-Hochberg FDR |
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
| Mutual Information | Prospectively listed as optional corroboration, with no independent threshold; not implemented in the current run | The implemented held-out SHAP checks supply the current corroboration. MI is not part of the RQ2 decision rule and its absence is not a submission gate. |

Full reasoning for each threshold, and the assumption each protects, is in `statistical_assumptions.md` (Multicollinearity row) and `statistical_decision_matrix.md` (Feature Selection stage rows).

---

## Prediction intervals (frozen SAP v1.0 method — implemented)

Notebook 07 implements empirical residual-quantile 90%/95% prediction intervals from training residuals, plus seeded 21-day block-bootstrap RMSE intervals and Wilson directional-accuracy intervals. These are persisted in `statistical_tests.json`. A conditional heteroskedasticity-aware interval remains future work.

---

## Part E — Per-notebook statistical plan (🆕 not previously tabulated)

| Notebook | Purpose | RQ | Variables | Statistics | Plots | Tables | Tests | Outputs | Interpretation |
|---|---|---|---|---|---|---|---|---|---|
| `03_exploratory_analysis.ipynb` (repo: `02_eda.ipynb`) | Describe distributions, market behaviour, event frequency; run stationarity checks before any modelling | Context (all RQs) | SPY/QQQ/GLD/TLT returns, VIX, macro series, event counts | Skewness, kurtosis, descriptive stats | Histograms, QQ-plots, rolling-stat plots, ACF/PACF | Descriptive summary table | ADF and KPSS completed | Distribution figures, stationarity flags per series | Establishes the empirical baseline later phases test against; confirms log returns are the correct modelling scale |
| `04_event_study.ipynb` (repo: `04_causal_analysis.ipynb`) | Abnormal returns, CAR, event-type mean-CAR tests and causal estimate | RQ1 | Event-window CAR by type, sentiment and VIX regime | Mean CAR, 95% CI, Cohen's d and causal effect | `04a`–`04d` figures | `car_results.parquet`, `event_type_statistics.parquet`, `rq1_reporting_validation.json`, `causal_estimates.parquet` | Five one-sample event-type tests + BH-FDR; DoWhy backdoor estimate + refuters | Multiplicity-controlled CAR table, causal effect + 95% CI | RQ1 reporting `PASS`: 0/5 BH rejections; pooled conditional estimate positive, subject to identification assumptions |
| `05_sentiment_analysis.ipynb` (repo: folded into `03_event_detection.ipynb`) | Text preprocessing, sentiment scoring, event classification | RQ1 (methodology) → RQ2 | APP titles, FOMC structured signal, event type and sentiment score | Neutral/positive/negative shares | `03a`–`03d` figures | `events_tagged.parquet`, `daily_sentiment.parquet` | Descriptive method validation (not an inferential claim) | Current combined APP + FOMC sentiment distribution | FinBERT is the APP engine and structured FOMC scoring is retained; lexicon is fallback/history only — see `10_decision_log.md` |
| `06_feature_engineering.ipynb` (repo: `05_feature_engineering.ipynb`) | Rolling returns, lags, volatility, technical indicators, event/macro features | RQ2, RQ3 | 92 frozen features | Variance, correlation, VIF | `05_learning_outcome.png` | `feature_matrix.parquet`, `feature_profile.json` | Blocking variance/leakage/source checks; correlation/VIF diagnostics | FES v1.1 validated matrix | 92 features retained under the contract; three zero-training-variance features removed |
| `07_machine_learning.ipynb` (repo: `06_model_training.ipynb`) | Market-only baseline training and validation | RQ3 | `fwd_return_1d`, 27 Market features | RMSE, MAE, R², Dir. Acc., IC | `06_learning_outcome.png` | `baseline_metrics.json` | `TimeSeriesSplit`/`LassoCV`; output validation | Baseline model, predictions and validation | Baseline_LASSO is a constant mean predictor; validation `PASS` |
| `08_model_evaluation.ipynb` (repo: `07_model_evaluation.ipynb`) | Event models, RF importance, SHAP, diagnostics and final comparison | RQ2, RQ3 | 92 features and common 750-row test split | Full SAP metric suite | `07_learning_outcome.png`, Notebook 08 synthesis figures | Current files under `reports/model_comparison/` | DM, z-test, Bonferroni, residual and interval diagnostics all run | Models, predictions, RF/SHAP and validation | H0 for RQ2 and H0₃ for RQ3 are not rejected; XGBoost overfitting flagged |

Notebook names above follow the mission brief's 10-phase numbering; the current repository's 8-notebook implementation (right-hand column, "repo:") is mapped per `docs/00_project_workflow.md` — see that document and `10_decision_log.md` for why the two numbering schemes coexist. This table's RQ/statistics/test content applies regardless of which notebook filename ultimately hosts it.
