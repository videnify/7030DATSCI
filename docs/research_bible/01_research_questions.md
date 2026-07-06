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
A quantified CAR per event type with a significance test (t-test / p-value) **and** a causal-effect estimate with a confidence interval that does not trivially span implausible ranges. A null result (no significant effect) is a valid and reportable answer — RQ1 is a test, not a foregone conclusion.

### Current status
✅ Answered with current data (Phase 4 complete). Headline finding: only a minority of events (~4.7%) produce statistically significant CAR, and effect direction is heterogeneous across event types (geopolitical positive and significant; monetary negative but not significant at conventional thresholds). Full numbers in `09_results_log.md`.

---

## RQ2 — Which features matter for next-day prediction

> **Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns?**

### Sub-questions
1. Do event-derived features (sentiment scores, event-type counts, days-since-last-event) rank among the top predictors, or are price/technical features dominant?
2. Which macro features (VIX, Fed Funds Rate, CPI, yield spread) carry the most weight?
5. Are there meaningful interaction effects (e.g. sentiment × VIX regime, high-impact-event × momentum)?

### Method (summary — full detail in `03_methodology.md`)
Feature importance from a Random Forest selection pass (feature retained if importance > 0.001), cross-checked against SHAP values from the final predictive models.

### What counts as a satisfactory answer
A ranked feature-importance table (already produced — see `06_feature_dictionary.md` and `data/processed/feature_metadata.parquet`) with SHAP corroboration, and an explicit statement of which *group* (price, technical, sentiment, event, macro, interaction) dominates.

### Current status
✅ Answered with current data (Phase 5–7 complete). Headline finding: the single most important feature is `mean_car` (an event-derived feature, 16.1% importance), followed by `return_lag1d` (price, 10.2%) and `vix_vs_ma` (macro, 10.0%) — i.e. event information is not dominant but is not negligible either; it sits alongside, not below, price and macro signal. Full ranking in `09_results_log.md`.

---

## RQ3 — Do event-informed ML models beat a market-only baseline

> **Can machine learning models using event information outperform market-only baseline models?**

### Sub-questions
1. Do LASSO / XGBoost / LightGBM trained on the full (event + macro + price) feature set outperform a model trained on price/technical features only?
2. Is any improvement statistically significant, or within noise?
3. Is directional accuracy (a more decision-relevant metric than R² for a return-prediction task) meaningfully above chance (50%)?
4. Does any model generalise out-of-sample, or does in-sample performance collapse on the test set?

### Method (summary — full detail in `07_model_plan.md`)
Time-series cross-validated training of LASSO (baseline-complexity model), XGBoost, and LightGBM on the full 52-feature set, evaluated on a strict chronological hold-out (2023-01-01 → 2025-12-29).

### What counts as a satisfactory answer
A model-comparison table (RMSE, MAE, R², directional accuracy, IC) for the full-feature models **against a genuine price-only baseline trained under the identical protocol**. This is the one open methodological gap in the current project (see below) — without the price-only baseline, RQ3 cannot yet be answered, only *approached*.

### Current status
✅ **Answered (2026-07-05, Mission 07).** `reports/model_comparison/model_comparison.parquet` compares `Baseline_LASSO` (27 Market-only features, `feature_matrix.parquet`) against Event_LASSO, XGBoost, and LightGBM (all 95 features, same frozen matrix). None of the three event-enhanced models clears the Bonferroni-corrected significance threshold (α = 0.0167) on either the RMSE (Diebold-Mariano) or directional-accuracy (two-proportion z-test) leg — **H0₃ is not rejected**. Event_LASSO is numerically closest (RMSE +1.74% over baseline, DM p = 0.056 one-sided uncorrected) but does not clear even α = 0.05. XGBoost reproduces its known overfitting signature on the new feature matrix (train R² 0.267 → test R² 0.019). Full detail: `07_model_plan.md`, `reports/statistics/07_event_models_summary.md`, `10_decision_log.md`. This supersedes the prior 2026-07-04 "not yet answered" status — the blocking gap (no market-only baseline) is closed, and the comparison itself is complete, with a null result reported honestly rather than a forced positive finding.

---

## Cross-RQ dependency note

RQ3 depends on RQ2's feature set (the "event-informed" model uses the features RQ2 identified as important) and indirectly on RQ1 (the `mean_car` feature used across RQ2/RQ3 is itself an RQ1 output). This is intentional — the three questions form a chain (does the event matter? → which signals from it matter? → do those signals help forecasting?) rather than three independent analyses, and the dissertation Discussion chapter should make this chain explicit rather than treating each RQ as siloed.
