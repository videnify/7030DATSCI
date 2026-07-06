# 02 — Hypotheses

**Purpose:** Formal, testable H0/H1 statements derived from RQ1–RQ3, each mapped to the specific statistical test used to accept or reject it. Bridges the plain-language research questions (`01_research_questions.md`) and the statistical machinery (`04_statistics_plan.md`).
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `04_statistics_plan.md`.
**Update Frequency:** Frozen after Phase 0 alongside the research questions; any post-hoc change to a hypothesis after seeing results must be logged in `10_decision_log.md` and flagged in the dissertation as such (to avoid the appearance of HARKing — Hypothesising After Results are Known).
**Relation to Dissertation:** Direct source for dissertation Chapter 3 (Methodology) §3.2 (Hypotheses) and the statistical-test framing in Chapter 4 (Results).

---

## H1 (supports RQ1) — Abnormal returns exist around political/monetary events

**H0:** The mean cumulative abnormal return (CAR) around presidential-communication and FOMC event windows is zero — i.e. these events carry no detectable market impact beyond what the market-model estimation window already predicts.

**H1:** The mean CAR around these event windows is significantly different from zero.

**Test:** One-sample t-test on CAR per event, aggregated to Cumulative Average Abnormal Return (CAAR) per event type; DoWhy backdoor linear regression for the causal-effect estimate with 95% CI. See `04_statistics_plan.md` §Event Study Tests.

**Decision rule:** Reject H0 at α = 0.05 for a given event type if the CAAR t-test p-value < 0.05 **and** the DoWhy CI excludes zero.

**Result so far (2026-07-04):** Partially rejected — Geopolitical events show a significant positive CAR (p<0.05); Monetary, Energy, Regulatory, and Trade do not reach significance individually, though the pooled DoWhy causal effect (lexicon sentiment, all event types) is significant (+0.0051, 95% CI [+0.0014, +0.0087]). See `09_results_log.md` for the full table and `data/processed/car_results.parquet` / `causal_estimates.parquet` for source data.

**SAP v1.0 fields** (`statistical_analysis_plan.md` Part C):
- **Type:** Two-sided, tested per event-type family, Benjamini-Hochberg FDR-corrected across the 5 event types.
- **Alpha / Confidence level:** α = 0.05 / 95%.
- **Effect size:** Cohen's d for the CAAR t-test; causal point estimate reported directly in log-return units (already a native effect size, e.g. +0.0051 ≈ +0.51% average abnormal return).
- **Practical interpretation:** A statistically significant CAAR for one event type out of five, plus a small but significant pooled causal effect, supports "the market reacts to a minority of these events, modestly on average" — not "these events reliably move the market." The dissertation must state both readings, not just the significant one.

---

## H2 (supports RQ2) — Event and macro features are informative predictors

**H0:** Event-derived and macroeconomic features contribute no more to next-day return prediction than would be expected by chance — i.e. price-lag-only features dominate the importance ranking and event/macro features cluster near zero importance.

**H1:** At least one event-derived feature and at least one macro feature rank among the top decile of feature importance, indicating genuine incremental predictive signal beyond price history alone.

**Test:** Random Forest permutation/impurity importance ranking (retain features with importance > 0.001) cross-validated against SHAP value magnitude and sign consistency on the held-out test set. See `04_statistics_plan.md` §Feature Importance Tests.

**Decision rule:** Reject H0 if ≥1 event-group feature and ≥1 macro-group feature appear in the top 10 by importance, with SHAP direction consistent with domain expectation (e.g. higher VIX associated with larger predicted moves, not necessarily direction).

**Result so far (2026-07-04):** Rejected — `mean_car` (event group) ranks #1 overall (16.1% importance) and `vix_vs_ma` (macro group) ranks #3 (10.0%); both appear in the top 3 of 52 selected features. See `06_feature_dictionary.md` and `data/processed/feature_metadata.parquet`.

**SAP v1.0 fields** (`statistical_analysis_plan.md` Part C):
- **Type:** Descriptive ranking, not a classical hypothesis test — no p-value is attached (see `04_statistics_plan.md` §Feature Importance Tests for why).
- **Alpha / Confidence level:** Not applicable — no significance threshold governs a ranking claim.
- **Effect size:** Importance percentage (RF impurity) and SHAP magnitude, reported side by side as corroborating rather than independent effect-size measures.
- **Practical interpretation:** "Event and macro signal rank alongside price signal" is a *ranking* statement, not a claim that any individual feature's contribution is statistically distinguishable from zero — the dissertation must not imply H2 was tested with a p-value, since none was computed.

---

## H3 (supports RQ3) — Event-informed models beat a market-only baseline

**H0:** An ML model trained on the full feature set (price + technical + sentiment + event + macro) does not significantly outperform a model trained on price/technical features only, on held-out test-period RMSE and directional accuracy.

**H1:** The full-feature model achieves significantly lower RMSE and/or significantly higher directional accuracy than the price-only baseline on the same held-out test period.

**Test:** Paired comparison of test-set RMSE and directional accuracy between the full-feature model(s) and the price-only baseline, both trained under an identical `TimeSeriesSplit` protocol with the same random seed (`config.yaml: model.random_seed = 42`). A Diebold–Mariano test (or bootstrap CI on the RMSE difference) is the planned significance test for the RMSE comparison; a two-proportion z-test (or exact binomial test) for the directional-accuracy comparison. See `04_statistics_plan.md` §Model Comparison Tests.

**Decision rule:** Reject H0 only if the RMSE improvement is statistically significant (not just numerically smaller) **and** directional accuracy improvement is significant at α = 0.05.

**Result (2026-07-05, Mission 07):** ✅ **Tested — H0 is not rejected.** `Baseline_LASSO` (Mission 06) and Event_LASSO/XGBoost/LightGBM (retrained on `feature_matrix.parquet`, FES v1.0) were compared under the identical `TimeSeriesSplit(5)`/seed-42 protocol. Diebold-Mariano (RMSE leg) one-sided p-values: 0.056 (Event_LASSO), 0.163 (XGBoost), 0.161 (LightGBM); two-proportion z-test (Dir. Acc. leg) one-sided p-values: 0.662, 0.767, 0.839. None clears the Bonferroni-corrected α = 0.0167 on either leg — per the decision rule below, H0 stands. See `reports/statistics/07_event_models_summary.md` and `09_results_log.md` (2026-07-05 entry) for the full numbers and the caveat that all three event-enhanced models' *lower* raw directional accuracy than the baseline is a base-rate artefact of the baseline's degenerate constant prediction, not a genuine directional deficiency.

**SAP v1.0 fields** (`statistical_analysis_plan.md` Part C, `statistical_decision_matrix.md` Part K):
- **Type:** One-sided (directional — "outperforms," not "differs from"), Bonferroni-corrected across 3 candidate models vs. the baseline.
- **Alpha / Confidence level:** α/3 = 0.0167 per model comparison / 95% CI on the RMSE difference (block-bootstrap) and directional-accuracy difference (binomial).
- **Effect size:** % RMSE improvement over baseline; percentage-point directional-accuracy improvement over baseline.
- **Practical interpretation:** A model must win on **both** legs (RMSE and directional accuracy) at the corrected α to be reported as "outperforms" — winning on one leg only is a mixed result, never rounded up. Given L2 (directional accuracy already close to chance for the existing event-informed models), even a "win" here should be reported alongside its economic-significance caveat, not as a standalone statistical headline.

---

## Hypothesis-testing discipline for this project

- All three hypotheses were fixed at Phase 0, before any modelling was run, and are treated as frozen (see `10_decision_log.md` for the Phase 0 sign-off, once logged).
- Multiple comparisons across five event types (H1) and across three candidate models (H3) require a correction — see `04_statistics_plan.md` §Multiple Comparisons for the Bonferroni/Benjamini-Hochberg policy applied before any p-value in this project is reported as "significant."
- A null result for any hypothesis is a valid dissertation finding and must be reported as such, not omitted or reframed post-hoc as "not the focus of this study."
