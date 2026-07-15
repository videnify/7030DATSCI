# 01 — Research Questions

**Purpose:** The authoritative, expanded statement of the three research questions this project answers — including sub-questions, scope boundaries, and what would count as a satisfactory answer to each. This is the document every other document must trace back to.
**Owner:** Ibrahim Haroun.
**Dependencies:** `00_project_overview.md`.
**Update Frequency:** Frozen after Phase 0 (Research Design) unless a supervisor-approved scope change occurs — any change must be logged in `10_decision_log.md`.
**Relation to Dissertation:** Direct source for dissertation Chapter 1 §1.3 (Research Questions) and the framing of Chapter 5 (Discussion).

---

## Governing rule

No notebook, figure, model, or statistical test should exist in this repository or the dissertation unless it directly supports one of the three questions below (see `docs/00_project_workflow.md`). Every question below has a corresponding row in `15_traceability_matrix.md`.

---

## RQ1 — Abnormal returns from political/monetary events

> **Do presidential communications and Federal Reserve announcements produce statistically significant abnormal returns in the S&P 500?**

### Sub-questions
1. Do FOMC rate decisions (scheduled, structured events) produce significant CAR around the announcement window?
2. Do presidential communications (unscheduled, unstructured events — speeches, press conferences, executive orders, proclamations) produce significant CAR?
3. Does the *sentiment* of the communication (positive/negative/neutral) moderate the size or direction of the abnormal return?
4. Does market regime (VIX level) moderate the event's impact?

### Method (summary — full detail in `03_methodology.md`)
Classical event study (Abnormal Return / Cumulative Abnormal Return via a market-model estimation window) plus a DoWhy backdoor-adjusted causal estimate, controlling for VIX regime and prior-day return as confounders.

### What counts as a satisfactory answer
A quantified mean CAR per event type with 95% CI, raw p-value, BH-FDR q-value and Cohen's d, plus a separately identified causal-effect estimate with its confidence interval. The completed result is null for all five event types after BH-FDR and positive for the pooled conditional DoWhy estimand; these are different claims and are reported separately.

### Current status
✅ Answered with current rebuilt data (Phase 4 complete). No event category reaches p<0.10 in the current 264-row CAR analysis, so the event-study leg is a null result. The pooled DoWhy estimate remains positive and significant (+0.005601, 95% CI [0.002295, 0.008907], p=0.0009). The dissertation must report this mixed evidence rather than retain the superseded claim that geopolitical CAR is significant. Full numbers are in `09_results_log.md`.

---

## RQ2 — Which features matter for next-day prediction

> **Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns?**

### Sub-questions
1. Do event-derived features (sentiment scores, event-type counts, days-since-last-event) rank among the top predictors, or are price/technical features dominant?
2. Which macro features (VIX, Fed Funds Rate, CPI, yield spread) carry the most weight?
5. Are there meaningful interaction effects (e.g. sentiment × VIX regime, high-impact-event × momentum)?

### Method (summary — full detail in `03_methodology.md`)
Random Forest feature importance over the frozen feature matrix, cross-checked against SHAP values from the predictive models. The importance threshold is a reporting aid, not a filter that defines FES v1.1.

### What counts as a satisfactory answer
A reproducible ranked feature-importance table with SHAP corroboration and an explicit statement of which category dominates.

### Current status
✅ **Answered on FES v1.1.** Notebook 07 reproducibly ranks all 92 features with the fixed Random Forest and generates held-out SHAP for every predictive candidate. Market/technical features dominate the RF top decile; macro signal is present (`vix` #5, `vix_change_5d` #7, `vix_change_1d` #10), but no event feature enters the top 10 (`mean_car` is the highest at #20). The frozen joint H2 rule is therefore not met and H0 is not rejected. LightGBM SHAP ranks `mean_car` fifth, retained as model-specific corroborating evidence rather than a reason to override the pre-specified RF rule.

---

## RQ3 — Do event-informed ML models beat a market-only baseline

> **Can machine learning models using event information outperform market-only baseline models?**

### Sub-questions
1. Do LASSO / XGBoost / LightGBM trained on the full (event + macro + price) feature set outperform a model trained on price/technical features only?
2. Is any improvement statistically significant, or within noise?
3. Is directional accuracy (a more decision-relevant metric than R² for a return-prediction task) meaningfully above chance (50%)?
4. Does any model generalise out-of-sample, or does in-sample performance collapse on the test set?

### Method (summary — full detail in `07_model_plan.md`)
Time-series cross-validated training of Event_LASSO, XGBoost, and LightGBM on all 92 FES v1.1 features, compared with `Baseline_LASSO` on the 27 Market-only features over the strict 2023-01-03 → 2025-12-29 hold-out.

### What counts as a satisfactory answer
A model-comparison table (RMSE, MAE, R², directional accuracy, IC) for all full-feature models against the market-only baseline, with the frozen DM/z-test/Bonferroni decision rule applied.

### Current status
✅ **Answered on FES v1.1: H0₃ not rejected.** Event_LASSO exactly reproduces the all-zero baseline (test RMSE 0.009631, directional accuracy 0.5747), so its DM comparison is undefined because the loss differential has zero variance. XGBoost (RMSE 0.009656, directional accuracy 0.4893) and LightGBM (0.009700, 0.4427) are numerically worse; their one-sided DM p-values are 0.6097 and 0.6724 and directional z-test p-values are 0.9995 and 1.0000. No candidate clears the Bonferroni-corrected α=0.0167 threshold on both required legs.

---

## Cross-RQ dependency note

RQ3 depends on RQ2's feature set (the "event-informed" model uses the features RQ2 identified as important) and indirectly on RQ1 (the `mean_car` feature used across RQ2/RQ3 is itself an RQ1 output). This is intentional — the three questions form a chain (does the event matter? → which signals from it matter? → do those signals help forecasting?) rather than three independent analyses, and the dissertation Discussion chapter should make this chain explicit rather than treating each RQ as siloed.
