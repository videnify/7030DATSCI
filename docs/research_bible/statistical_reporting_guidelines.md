# Statistical Reporting Guidelines (SAP v1.0)

**Purpose:** Exact conventions for how any statistic, p-value, confidence interval, or effect size is written up anywhere in this project — notebooks, `09_results_log.md`, and the dissertation itself — so results are reported consistently and never as a bare, uninterpretable number. Also fixes the per-figure documentation requirement (Part L of the mission brief).
**Owner:** Research Statistician sign-off.
**Dependencies:** `statistical_analysis_plan.md` Part A (the policies these conventions implement), `statistical_decision_matrix.md`, `08_figures_plan.md`.
**Update Frequency:** Stable — update only if a new statistic type is introduced that the templates below don't cover.
**Relation to Dissertation:** Direct style authority for every numeric claim in Chapter 4 and every figure caption in the dissertation.

---

## Numeric reporting template

Every statistical claim in this project must be written using this template — in a notebook markdown cell, in `09_results_log.md`, or in the dissertation text:

```
[Test name] on [variable/sample], n = [sample size]:
statistic = [value], p = [exact value, or "< 0.001" only if below that],
95% CI [lower, upper], effect size = [value, named metric],
[multiple-comparison correction applied, or "no correction applicable — see reason"].
```

**Current example:** “Across five event-type mean-CAR tests (N=264), no null was rejected after Benjamini–Hochberg FDR correction (minimum raw p=0.1162; minimum q=0.5810); all 95% intervals crossed zero and the largest standardised magnitude was small (monetary d=−0.239). The separate pooled DoWhy estimate using the combined APP + FOMC treatment was +0.005601, 95% CI [+0.002295, +0.008907], p=0.0009.”

### Rounding conventions

| Quantity | Precision |
|---|---|
| p-values | 3 significant figures (e.g. `p = 0.0342`); `p < 0.001` once below that threshold — never `p = 0.000` |
| Returns / CAR / causal effects | 4 decimal places (log-return units, e.g. `+0.0051`) — matches existing `09_results_log.md` convention |
| R², directional accuracy, IC | 3 decimal places (e.g. `0.033`) — matches existing convention |
| RMSE / MAE | 6 decimal places (log-return-scale errors are small; matches existing `09_results_log.md` convention, e.g. `0.009465`) |
| Percentages (importance, sentiment shares) | 1 decimal place (e.g. `16.1%`) |

### What must never appear

- A bare p-value with no test name, statistic, sample size, or correction status.
- `p = 0.000` (report `p < 0.001` instead).
- A "significant" claim without an accompanying effect size.
- A model-comparison claim ("Model X beats baseline") without stating which of the two required legs (RMSE, directional accuracy) it passed, per `statistical_analysis_plan.md`'s model-selection policy.
- A causal-effect or CI claim rounded to look tighter than the source parquet file actually reports — always re-verify against the file named in the "Source" field, never from memory (this is the same "source file" discipline `09_results_log.md` already requires).

---

## Confidence interval and effect size conventions

| Test family | CI method | Effect size reported |
|---|---|---|
| Event-study mean-CAR test (RQ1) | Two-sided 95% t-distribution CI for the event-type mean | Cohen's d = mean CAR / sample SD within event type; report raw p and BH q |
| DoWhy causal estimate (RQ1) | Regression-based 95% CI from `backdoor.linear_regression` standard errors (already produced) | Point estimate in native log-return units (current pooled estimate 0.005601, approximately +0.56%) |
| RF/SHAP importance (RQ2) | Not applicable — descriptive ranking, no CI | Importance percentage / SHAP magnitude |
| Model comparison (RQ3) | Block-bootstrap CI on the RMSE difference (block length ≈ 21 trading days); binomial CI on directional-accuracy difference | % RMSE improvement over baseline; percentage-point directional-accuracy improvement |

---

## PART L — Figure Requirements

Every figure in `08_figures_plan.md` must be describable against this template before it is considered dissertation-ready. This does not replace `08_figures_plan.md`'s inventory — it adds the fields the mission brief requires that inventory did not previously carry explicitly.

```
Figure: [filename]
Purpose: [what it shows]
Supports RQ: [RQ1 / RQ2 / RQ3]
Supports H0/H1: [which hypothesis, if any — some figures are context-only]
Notebook: [source notebook]
Caption (dissertation-ready): [one sentence, stating what the reader should conclude, not just what is plotted]
Dissertation section: [chapter/section]
Statistical interpretation: [what statistical claim, if any, the figure visually supports — must match a row in statistical_decision_matrix.md if it claims significance]
```

### Applied to the four figures already flagged as primary evidence

| Figure | Supports RQ | Supports H0/H1 | Statistical interpretation |
|---|---|---|---|
| `04a_car_by_event_type.png` | RQ1 | H1 | Shows event-level CAR distributions and event-type means with 95% CI; labels report BH q and Cohen's d, with 0/5 rejected |
| `04c_causal_estimates.png` | RQ1 | H1 | Visualises the DoWhy point estimate + 95% CI — caption must state the CI explicitly, not just "significant" |
| `05a_feature_importance.png` | RQ2 | H2 | Descriptive ranking — caption must avoid implying a p-value exists for any single bar |
| `08c_predictive_pipeline.png` | RQ3 | H3 | Current FES v1.1 comparison; caption must state that no candidate clears either Bonferroni-corrected improvement leg and H0₃ is not rejected |

All remaining figures should be checked against this template as Chapter 4 is drafted; `08_figures_plan.md` remains the authoritative inventory of *which* figures exist — this document fixes *how* each is captioned and interpreted once selected for the dissertation.

---

## Definition of Done — this document

- [x] Universal numeric reporting template defined, with a worked example
- [x] Rounding conventions fixed per quantity type, consistent with existing `09_results_log.md` numbers
- [x] "What must never appear" list defined to prevent common overclaiming errors
- [x] CI and effect-size method fixed per test family
- [x] Figure requirement template defined and applied to the four primary-evidence figures
