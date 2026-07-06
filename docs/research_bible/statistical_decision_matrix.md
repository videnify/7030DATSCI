# Statistical Decision Matrix — Master Test Table (SAP v1.0)

**Purpose:** One master table listing every statistical test used anywhere in this project (already run, or frozen for a future notebook), so no test exists that isn't traceable to a research question, an H0/H1 pair, and a dissertation section. This is `statistical_analysis_plan.md` Part F, plus the explicit RQ3 model-comparison protocol (Part K), in one place.
**Owner:** Research Statistician sign-off.
**Dependencies:** `statistical_analysis_plan.md` (policy), `statistical_assumptions.md` (assumption checks each test relies on), `02_hypotheses.md`.
**Update Frequency:** Add a row before a new test is run — this table is written prospectively for anything not yet executed (RQ3 rows), not reconstructed afterward.
**Relation to Dissertation:** Direct source for Chapter 3 §3.4 test inventory and the "Statistical Methods" cross-reference used throughout Chapter 4 (Results).

---

## How to read this table

`Status`: ✅ Run (result already in `09_results_log.md`) · 🟡 Run, pending a correction/action noted in `Output` · ⬜ Frozen, not yet run (RQ3 baseline-dependent).

## Master test matrix

| Stage | RQ | Variable | Test | Purpose | H0 | H1 | Assumptions (→ `statistical_assumptions.md`) | Output | Supports dissertation section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| EDA | Context | SPY / QQQ / GLD / TLT daily return | Histogram, skewness/kurtosis, QQ-plot | Describe return distribution shape; motivate non-parametric preference downstream | — | — | — (descriptive) | Distribution figure, skew/kurtosis stats | Methods §3.2 / Results §4.5 | ✅ |
| EDA | RQ1/RQ2 | SPY log return, VIX, macro levels | ADF test | Test unit-root non-stationarity | Series has a unit root (non-stationary) | Series is stationary | Independence of residuals in the test regression | Stationary/non-stationary flag per series | Methods §3.2 | ⬜ 🆕 |
| EDA | RQ1/RQ2 | SPY log return, VIX, macro levels | KPSS test | Cross-check ADF (opposite null) to avoid relying on one test's assumptions alone | Series is stationary | Series has a unit root | Independence of residuals | Stationary/non-stationary flag per series, cross-checked against ADF | Methods §3.2 | ⬜ 🆕 |
| EDA | RQ2 | Engineered feature matrix | Pearson correlation matrix + threshold flag (\|r\| > 0.90) | Detect near-duplicate features before selection | — | — | Linearity of pairwise relationship | Correlation heatmap, flagged pairs list | Methods §3.3 | ⬜ 🆕 |
| EDA | RQ2 | Engineered feature matrix | Variance threshold (< 1e-8) | Detect near-constant, uninformative features | — | — | — | Dropped-feature list | Methods §3.3 | ⬜ 🆕 |
| Event Study | RQ1 | CAR per event, by event type | One-sample t-test (CAR → CAAR) | Test whether the event type's average abnormal return differs from zero | Mean CAR = 0 | Mean CAR ≠ 0 | Approx. normality of CAR within type; independence across events (violated — see `statistical_assumptions.md`) | t-stat, p-value, Cohen's d | Results §4.1 | 🟡 — run, BH-FDR correction not yet applied (`11_limitations.md` L3) |
| Event Study | RQ1 | CAAR t-test family (5 event types × 2 sentiment methods) | Benjamini-Hochberg FDR correction | Control false-discovery rate across the simultaneous event-type family | — | — | — | FDR-adjusted p-values, revised significance flags | Results §4.1 | ⬜ Frozen, action required before RQ1 is reported as final |
| Causal Inference | RQ1 | Event sentiment → next-day return, adjusting for VIX regime + prior return | DoWhy `backdoor.linear_regression` | Estimate the causal effect of event sentiment net of identified confounders | Causal effect = 0 | Causal effect ≠ 0 | Correct DAG/backdoor identification; linear functional form; no unmeasured confounding (untestable — stated as a limitation) | Point estimate, 95% CI | Results §4.2 | ✅ |
| Causal Inference | RQ1 | Same estimate | Refutation tests (random common cause, placebo treatment, data-subset) | Robustness-check the causal estimate against known refutation strategies | Estimate is robust to the refuter | Estimate changes materially under the refuter | — | Refuted/not-refuted flag per test | Results §4.2 / Discussion §5.1 | ✅ |
| Feature Selection | RQ2 | 88 candidate engineered features | Random Forest impurity importance, threshold 0.001 | Rank and select features by predictive contribution | — (ranking, not a test) | — | Not sensitive to multicollinearity in ranking, but biased toward high-cardinality/continuous features (noted, not corrected) | Ranked importance table, `selected` flag | Results §4.3 | ✅ |
| Feature Selection | RQ2 | Selected feature set | Variance Inflation Factor (VIF), threshold 10 | Quantify multicollinearity among selected features, esp. for LASSO coefficient interpretability | — | — | Linearity | VIF per feature | Methods §3.3 / Discussion §5.2 | ⬜ 🆕 |
| Feature Selection | RQ2 | Selected feature set | Mutual Information (corroboration, not primary) | Cross-check RF-importance ranking with a non-linear-relationship-agnostic measure | — | — | — | MI score per feature, compared against RF rank | Results §4.3 (secondary) | ⬜ 🆕 |
| Feature Selection | RQ2 | Test-set predictions | SHAP (TreeExplainer / LinearExplainer) | Corroborate impurity-importance ranking is not a training-set artefact | — | — | Model-specific (tree-based exactness for TreeExplainer; linearity for LinearExplainer) | Global summary + dependence plots | Results §4.3 | ✅ |
| Model Training | RQ3 | `fwd_return_1d`, full 52-feature set vs. 26-feature baseline set | Model training (LASSO, XGBoost, LightGBM) × (full, baseline) | Produce the paired predictions the RQ3 tests below compare | — | — | `TimeSeriesSplit`, no shuffling; train/test temporal independence | Trained models, test-set predictions | Results §4.4 | 🟡 — full-feature models ✅ run; baseline ⬜ not yet trained |
| Model Comparison | RQ3 | Paired squared-error series, full-feature model vs. baseline, test split | Diebold-Mariano test (or block-bootstrap CI on RMSE difference if DM assumptions fail) | Test whether RMSE improvement over baseline is statistically significant | RMSE difference = 0 | RMSE difference < 0 (full-feature model better) — one-sided | Stationarity of the loss differential | DM statistic, p-value, 95% bootstrap CI on RMSE diff | Results §4.4 | ⬜ Frozen, not yet run |
| Model Comparison | RQ3 | Paired directional-accuracy series, full-feature model vs. baseline, test split | Two-proportion z-test (or exact binomial, n=750) | Test whether directional-accuracy improvement over baseline is statistically significant | Dir. Acc. difference = 0 | Dir. Acc. difference > 0 — one-sided | Independent Bernoulli trials (approximately, given test-set size) | z-stat, p-value, pp improvement | Results §4.4 | ⬜ Frozen, not yet run |
| Model Comparison | RQ3 | 3 candidate models × 1 baseline | Bonferroni correction (α/3 = 0.0167) | Control family-wise error across LASSO/XGBoost/LightGBM vs. baseline comparisons | — | — | — | Corrected significance flags | Results §4.4 | ⬜ Frozen, not yet run |
| Residual Diagnostics | RQ3 | LASSO (best model) residuals | Durbin-Watson | Test residual autocorrelation | No autocorrelation | Autocorrelation present | — | DW statistic (2.02 — pass) | Results §4.5 | ✅ |
| Residual Diagnostics | RQ3 | LASSO residuals | Jarque-Bera | Test residual normality | Residuals normal | Residuals non-normal | Large-sample approximation | JB statistic, p-value (p≈0.0 — fails; expected for financial returns) | Results §4.5 | ✅ |
| Residual Diagnostics | RQ3 | LASSO residuals | Breusch-Pagan-style heteroskedasticity correlation | Test residual variance stability | Homoskedastic | Heteroskedastic | Linearity of the variance-regressor relationship | Correlation stat (0.199 — mild) | Results §4.5 | ✅ |
| Residual Diagnostics | RQ3 | Test-set predictions, all models | Prediction interval construction (empirical residual-quantile method) | Report calibrated uncertainty around each point prediction, not just a point RMSE | — | — | Residual distribution stable across the test period (to be checked, given known heavy tails) | 90%/95% prediction interval per test-day prediction | Results §4.4 / Appendix C | ⬜ 🆕, not yet run |

---

## PART K — Model Comparison Protocol (frozen, exact procedure)

RQ3 requires an unambiguous, pre-specified procedure — this is written now, before the baseline exists, precisely so it cannot be adjusted after seeing which comparison looks best.

### Candidate set

| Model | Role |
|---|---|
| `Baseline_LASSO` | Market-only baseline — 26 features (price + technical only), tuned independently via the same `RandomizedSearchCV` protocol |
| LASSO | Full-feature (52-column) event-informed model — already trained |
| XGBoost | Full-feature event-informed model — already trained |
| LightGBM | Full-feature event-informed model — already trained |

### 🔴 Open scope question — Random Forest is not a fourth candidate model

The mission brief's Part K instruction names "LASSO, Random Forest, XGBoost, LightGBM" as the models to compare. In this project, **Random Forest is used only as a feature-importance ranking tool (RQ2), not as a trained predictive candidate for RQ3** — `07_model_plan.md` and `models/model_metadata.json` both fix the RQ3 candidate set at LASSO/XGBoost/LightGBM plus the baseline. Two options exist:

1. **(Recommended, adopted here)** Keep RF as an RQ2-only tool; RQ3's candidate set stays at three models + baseline, exactly as already frozen in `07_model_plan.md`. Reason: adding RF as a fourth predictive model now would be a scope addition after Phases 1–8 already ran, with no result gap it closes (RQ3's blocking gap is the *baseline*, not a fourth model type) — this would add breadth without depth, contrary to the project's own governing principle.
2. Add RF as a fourth full-feature predictive model, purely for RQ3 completeness against the mission brief's literal wording.

**This SAP freezes option 1.** If a supervisor specifically wants option 2, that is a Version 2 SAP amendment requiring a `10_decision_log.md` entry before any RF-as-predictor code is written — not a silent addition.

### Procedure (in order)

1. Train `Baseline_LASSO` on the 26-feature price/technical-only matrix, identical `TimeSeriesSplit` (5 folds, seed 42), identical `RandomizedSearchCV` tuning budget as the three full-feature models.
2. Add `Baseline_LASSO` train/test rows to `model_comparison.parquet` (same schema: `Model, Split, RMSE, MAE, R2, Dir_Acc, IC`).
3. For each of {LASSO, XGBoost, LightGBM} vs. `Baseline_LASSO`, on the test split only:
   a. Compute the paired squared-error differential per test day; run Diebold-Mariano (one-sided: full-feature model's error is lower). If the loss differential fails a stationarity pre-check, substitute a block-bootstrap CI (block length ≈ 21 trading days, to respect return autocorrelation) on the RMSE difference instead of DM.
   b. Compute the paired correct/incorrect directional call per test day; run a two-proportion z-test (one-sided: full-feature model's accuracy is higher).
4. Apply Bonferroni correction: reject H0 for a given model only if its p-value (RMSE test) < 0.0167 **and** its p-value (directional-accuracy test) < 0.0167.
5. A model is reported as "beats the baseline" only if it clears **both** legs of step 4 — a model clearing one leg only is reported as a mixed result (see `statistical_analysis_plan.md` Part A, "Model selection policy").
6. Log the completed result in `09_results_log.md` using the template already provided there ("Template for the next entry"), and flip `01_research_questions.md` RQ3 status from 🔴 to ✅/❌ based on the outcome — never leave it silently unresolved once the tests are run.
7. Regenerate `06a_model_comparison.png`, `08c_predictive_pipeline.png`, `08d_full_dashboard.png` (per `08_figures_plan.md`, "Figures requiring an update once the baseline model lands").

### Multiple-comparison family sizes (restated from `statistical_analysis_plan.md` Part A)

| Family | Count | Correction |
|---|---|---|
| Event-type CAAR tests (RQ1) | 5 event types × 2 sentiment methods = up to 10, reported primarily for lexicon method (5) | Benjamini-Hochberg FDR |
| Model-vs-baseline comparisons (RQ3) | 3 (LASSO, XGBoost, LightGBM vs. `Baseline_LASSO`) × 2 metrics (RMSE, Dir. Acc.) = 6 tests, corrected as 3 pairs | Bonferroni (α/3 = 0.0167) |
| Feature importance ranking (RQ2) | Descriptive, not a test family | No correction (not applicable) |

---

## Definition of Done — this document

- [x] Every test used in the project (run or frozen) appears with Stage/RQ/Variable/Test/Purpose/H0/H1/Assumptions/Output/Dissertation section
- [x] RQ3 model-comparison protocol fully specified, in exact execution order, before the baseline is trained
- [x] Open scope question (RF as 4th model) surfaced explicitly rather than silently resolved either way
- [x] Multiple-comparison family sizes and corrections restated and consistent with `statistical_analysis_plan.md`
