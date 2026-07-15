# Statistical Decision Matrix — Master Test Table (SAP v1.0)

**Purpose:** One master table listing every statistical test used anywhere in this project (already run, or frozen for a future notebook), so no test exists that isn't traceable to a research question, an H0/H1 pair, and a dissertation section. This is `statistical_analysis_plan.md` Part F, plus the explicit RQ3 model-comparison protocol (Part K), in one place.
**Owner:** Research Statistician sign-off.
**Dependencies:** `statistical_analysis_plan.md` (policy), `statistical_assumptions.md` (assumption checks each test relies on), `02_hypotheses.md`.
**Update Frequency:** Add a row before a new test is run; after execution, bind the row to its persisted result and update its status.
**Relation to Dissertation:** Direct source for Chapter 3 §3.4 test inventory and the "Statistical Methods" cross-reference used throughout Chapter 4 (Results).

---

## How to read this table

`Status`: ✅ Run (result already persisted/logged) · 🟡 Run, pending a correction/action noted in `Output` · ⬜ Frozen future work.

## Master test matrix

| Stage | RQ | Variable | Test | Purpose | H0 | H1 | Assumptions (→ `statistical_assumptions.md`) | Output | Supports dissertation section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| EDA | Context | SPY / QQQ / GLD / TLT daily return | Histogram, skewness/kurtosis, QQ-plot | Describe return distribution shape; motivate non-parametric preference downstream | — | — | — (descriptive) | Distribution figure, skew/kurtosis stats | Methods §3.2 / Results §4.5 | ✅ |
| EDA | RQ1/RQ2 | SPY log return, VIX, macro levels | ADF test | Test unit-root non-stationarity | Series has a unit root (non-stationary) | Series is stationary | Independence of residuals in the test regression | Stationary/non-stationary flags persisted by Notebook 02 | Methods §3.2 | ✅ |
| EDA | RQ1/RQ2 | SPY log return, VIX, macro levels | KPSS test | Cross-check ADF (opposite null) to avoid relying on one test's assumptions alone | Series is stationary | Series has a unit root | Independence of residuals | Stationary/non-stationary flags cross-checked against ADF | Methods §3.2 | ✅ |
| EDA | RQ2 | Engineered feature matrix | Pearson correlation matrix + threshold flag (\|r\| > 0.90) | Detect near-duplicate features before selection | — | — | Linearity of pairwise relationship | Correlation diagnostics and flagged pairs | Methods §3.3 | ✅ |
| EDA | RQ2 | Engineered feature matrix | Variance threshold (< 1e-8) | Detect near-constant, uninformative features | — | — | — | Three zero-training-variance features removed in FES v1.1 | Methods §3.3 | ✅ |
| Event Study | RQ1 | CAR per event, by event type | One-sample t-test of mean CAR against zero | Test whether an event type's average abnormal return differs from zero | Mean CAR = 0 | Mean CAR ≠ 0 | Approx. normality within type; independence across events is limited by clustering | Mean, 95% CI, t, raw p, Cohen's d | Results §4.1 | ✅ Run on 264 rows; all five intervals cross zero; max |d|=0.239 |
| Event Study | RQ1 | Five event-type mean-CAR tests under the current catalogue | Benjamini-Hochberg FDR correction | Control FDR across the simultaneous event-type family | — | — | — | BH q and final rejection flags | Results §4.1 | ✅ RQ1-v1.0 `PASS`; 0/5 rejected, minimum q=0.5810 |
| Causal Inference | RQ1 | Event sentiment → next-day return, adjusting for VIX regime + prior return | DoWhy `backdoor.linear_regression` | Estimate the causal effect of event sentiment net of identified confounders | Causal effect = 0 | Causal effect ≠ 0 | Correct DAG/backdoor identification; linear functional form; no unmeasured confounding (untestable — stated as a limitation) | Point estimate, 95% CI | Results §4.2 | ✅ |
| Causal Inference | RQ1 | Same estimate | Refutation tests (random common cause, placebo treatment, data-subset) | Robustness-check the causal estimate against known refutation strategies | Estimate is robust to the refuter | Estimate changes materially under the refuter | — | Refuted/not-refuted flag per test | Results §4.2 / Discussion §5.1 | ✅ |
| Feature Selection | RQ2 | 92 FES v1.1 engineered features | Random Forest impurity importance, threshold 0.001 | Rank features descriptively by predictive contribution | — (ranking, not a test) | — | Biased toward high-cardinality/continuous features (noted; SHAP corroboration used) | Complete 92-row ranking and `selected` flag | Results §4.3 | ✅ Current; no event feature in top 10, H0 not rejected |
| Feature Selection | RQ2 | Selected feature set | Variance Inflation Factor (VIF), threshold 10 | Quantify multicollinearity among selected features, esp. for LASSO coefficient interpretation | — | — | Linearity | VIF per feature | Methods §3.3 / Discussion §5.2 | ✅ Run in Notebook 05; 31 VIF>10 flags retained as non-blocking interpretability diagnostics |
| Feature Selection | RQ2 | Selected feature set | Mutual Information (optional corroboration, not primary) | Prospectively proposed cross-check of the RF ranking | — | — | — | MI score per feature, if implemented | Results §4.3 (secondary) | ⬜ Not run; non-binding and superseded for the current report by implemented held-out SHAP corroboration |
| Feature Selection | RQ2 | Test-set predictions | SHAP (TreeExplainer / LinearExplainer) | Corroborate impurity-importance ranking is not a training-set artefact | — | — | Model-specific (tree-based exactness for TreeExplainer; linearity for LinearExplainer) | Global summary + dependence plots | Results §4.3 | ✅ |
| Model Training | RQ3 | `fwd_return_1d`, 92-feature candidates vs. 27-feature Market baseline | Baseline_LASSO plus Event_LASSO, XGBoost and LightGBM | Produce paired predictions for the common 750-row test split | — | — | `TimeSeriesSplit`, no shuffling; train/test temporal independence | Trained models and row-level predictions | Results §4.4 | ✅ FES v1.1 validation `PASS` |
| Model Comparison | RQ3 | Paired squared-error series, each candidate vs. baseline | One-sided Diebold–Mariano test | Test whether RMSE improvement over baseline is statistically significant | RMSE difference = 0 | Candidate loss < baseline loss | Stationarity of loss differential; undefined when differential is constant | DM statistic and p-value | Results §4.4 | ✅ Run; no candidate clears the corrected threshold; Event_LASSO differential is identically zero |
| Model Comparison | RQ3 | Paired directional calls, each candidate vs. baseline, n=750 | One-sided two-proportion z-test | Test whether directional-accuracy improvement over baseline is statistically significant | Difference = 0 | Candidate accuracy > baseline accuracy | Approximate Bernoulli independence | z-stat, p-value, pp improvement | Results §4.4 | ✅ Run; no candidate clears the corrected threshold |
| Model Comparison | RQ3 | 3 candidates × 1 baseline | Bonferroni correction (α/3 = 0.0167) | Control family-wise error | — | — | — | Corrected verdicts | Results §4.4 | ✅ Applied; H0₃ not rejected |
| Residual Diagnostics | RQ3 | All four models | Durbin-Watson | Test first-order residual autocorrelation | No autocorrelation | Autocorrelation present | — | DW 1.989–2.112 | Results §4.5 | ✅ |
| Residual Diagnostics | RQ3 | All four models | Jarque-Bera | Test residual normality | Residuals normal | Residuals non-normal | Large-sample approximation | p≈0 for every model; heavy tails acknowledged | Results §4.5 | ✅ |
| Residual Diagnostics | RQ3 | Test-set predictions, all models | Empirical residual-quantile prediction intervals plus seeded block-bootstrap RMSE and Wilson direction intervals | Report uncertainty rather than point metrics alone | — | — | Training residual distribution used for PI; 21-day bootstrap blocks | 90%/95% PIs and 95% metric intervals | Results §4.4 / Appendix C | ✅ Persisted in `statistical_tests.json` |

---

## PART K — Model Comparison Protocol (frozen, exact procedure)

RQ3 required an unambiguous, pre-specified procedure. The protocol below was frozen before the baseline comparison and was implemented unchanged in Notebook 07; this section now records both the procedure and its completion.

### Candidate set

| Model | Role |
|---|---|
| `Baseline_LASSO` | Market-only baseline — 27 Market features, tuned by `LassoCV`/`TimeSeriesSplit(5)` |
| `Event_LASSO` | Event-enhanced LASSO — all 92 FES v1.1 features |
| XGBoost | Event-enhanced tree model — all 92 FES v1.1 features |
| LightGBM | Event-enhanced tree model — all 92 FES v1.1 features |

### Random Forest scope — resolved

The mission brief's Part K instruction names "LASSO, Random Forest, XGBoost, LightGBM" as the models to compare. In this project, **Random Forest is used only as a feature-importance ranking tool (RQ2), not as a trained predictive candidate for RQ3** — `07_model_plan.md` and `models/model_metadata.json` both fix the RQ3 candidate set at LASSO/XGBoost/LightGBM plus the baseline. Two options exist:

1. **(Recommended, adopted here)** Keep RF as an RQ2-only tool; RQ3's candidate set stays at three models + baseline, exactly as already frozen in `07_model_plan.md`. Reason: adding RF as a fourth predictive model now would be a scope addition after Phases 1–8 already ran, with no result gap it closes (RQ3's blocking gap is the *baseline*, not a fourth model type) — this would add breadth without depth, contrary to the project's own governing principle.
2. Add RF as a fourth full-feature predictive model, purely for RQ3 completeness against the mission brief's literal wording.

**This SAP freezes option 1.** If a supervisor specifically wants option 2, that is a Version 2 SAP amendment requiring a `10_decision_log.md` entry before any RF-as-predictor code is written — not a silent addition.

### Procedure (in order)

1. Train `Baseline_LASSO` on the 27-feature Market matrix with `TimeSeriesSplit(5)` and `LassoCV`; train the three candidates on all 92 FES v1.1 features under their frozen tuning rules.
2. Add `Baseline_LASSO` train/test rows to `model_comparison.parquet` (same schema: `Model, Split, RMSE, MAE, R2, Dir_Acc, IC`).
3. For each of {LASSO, XGBoost, LightGBM} vs. `Baseline_LASSO`, on the test split only:
   a. Compute the paired squared-error differential per test day; run Diebold-Mariano (one-sided: full-feature model's error is lower). If the loss differential fails a stationarity pre-check, substitute a block-bootstrap CI (block length ≈ 21 trading days, to respect return autocorrelation) on the RMSE difference instead of DM.
   b. Compute the paired correct/incorrect directional call per test day; run a two-proportion z-test (one-sided: full-feature model's accuracy is higher).
4. Apply Bonferroni correction: reject H0 for a given model only if its p-value (RMSE test) < 0.0167 **and** its p-value (directional-accuracy test) < 0.0167.
5. A model is reported as "beats the baseline" only if it clears **both** legs of step 4 — a model clearing one leg only is reported as a mixed result (see `statistical_analysis_plan.md` Part A, "Model selection policy").
6. Log the completed result in `09_results_log.md` using the template already provided there ("Template for the next entry"), and flip `01_research_questions.md` RQ3 status from 🔴 to ✅/❌ based on the outcome — never leave it silently unresolved once the tests are run.
7. Regenerate `08c_predictive_pipeline.png` and `08d_full_dashboard.png`, then bind them through `results_visualisation_validation.json`. **Completed 2026-07-14.**

### Multiple-comparison family sizes (restated from `statistical_analysis_plan.md` Part A)

| Family | Count | Correction |
|---|---|---|
| Event-type mean-CAR tests (RQ1) | 5 event types under the current combined APP + FOMC treatment | Benjamini-Hochberg FDR |
| Model-vs-baseline comparisons (RQ3) | 3 (LASSO, XGBoost, LightGBM vs. `Baseline_LASSO`) × 2 metrics (RMSE, Dir. Acc.) = 6 tests, corrected as 3 pairs | Bonferroni (α/3 = 0.0167) |
| Feature importance ranking (RQ2) | Descriptive, not a test family | No correction (not applicable) |

---

## Definition of Done — this document

- [x] Every test used in the project (run or frozen) appears with Stage/RQ/Variable/Test/Purpose/H0/H1/Assumptions/Output/Dissertation section
- [x] RQ3 model-comparison protocol fully specified, in exact execution order, before the baseline is trained
- [x] Open scope question (RF as 4th model) surfaced explicitly rather than silently resolved either way
- [x] Multiple-comparison family sizes and corrections restated and consistent with `statistical_analysis_plan.md`
