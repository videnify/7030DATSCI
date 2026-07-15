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

**Test:** Within each event type, a two-sided one-sample t-test of event-level CAR against zero, with a 95% t interval for the mean, Cohen's d and Benjamini–Hochberg FDR correction across the five-type family; DoWhy backdoor linear regression supplies the separate conditional causal estimate. See `04_statistics_plan.md` §Event Study Tests.

**Decision rule:** Reject an event-type H0 only when its BH-adjusted q-value is below 0.05. Interpret the pooled DoWhy estimate separately because it has a different estimand and identification assumptions; its CI does not rescue a null event-type test.

**Current result (RQ1-v1.0, 2026-07-15):** No event-type H0 is rejected. Across 264 observations, the minimum raw p-value is 0.1162 and the minimum BH-adjusted q-value is 0.5810; all five mean-CAR intervals cross zero. Cohen's d ranges from −0.239 to +0.086, so magnitudes are negligible to small. The separate pooled DoWhy estimate remains positive (+0.005601, 95% CI [+0.002295, +0.008907], p=0.0009). This qualified conclusion supersedes the historical geopolitical-significance claim. Sources: `event_type_statistics.parquet`, `rq1_reporting_validation.json`, and `causal_estimates.parquet`.

**SAP v1.0 fields** (`statistical_analysis_plan.md` Part C):
- **Type:** Two-sided, tested per event-type family, Benjamini-Hochberg FDR-corrected across the 5 event types.
- **Alpha / Confidence level:** α = 0.05 / 95%.
- **Effect size:** Cohen's d for the event-type mean-CAR test; causal point estimate reported directly in log-return units (current pooled estimate +0.005601 ≈ +0.56%).
- **Practical interpretation:** The five event-type tests provide no multiplicity-controlled abnormal-return evidence and their standardised magnitudes are small. The positive pooled conditional estimate is reported as separate observational evidence, not as proof that an event category reliably moves the market.

---

## H2 (supports RQ2) — Event and macro features are informative predictors

**H0:** Event-derived and macroeconomic features contribute no more to next-day return prediction than would be expected by chance — i.e. price-lag-only features dominate the importance ranking and event/macro features cluster near zero importance.

**H1:** At least one event-derived feature and at least one macro feature rank among the top decile of feature importance, indicating genuine incremental predictive signal beyond price history alone.

**Test:** Random Forest permutation/impurity importance ranking (retain features with importance > 0.001) cross-validated against SHAP value magnitude and sign consistency on the held-out test set. See `04_statistics_plan.md` §Feature Importance Tests.

**Decision rule:** Reject H0 if ≥1 event-group feature and ≥1 macro-group feature appear in the top 10 by importance, with SHAP direction consistent with domain expectation (e.g. higher VIX associated with larger predicted moves, not necessarily direction).

**Current result (FES v1.1, 2026-07-14):** H0 is not rejected under this descriptive rule. The fixed Random Forest ranks macro features in the top 10 (`vix` #5, `vix_change_5d` #7, `vix_change_1d` #10), but its highest event feature is `mean_car` at #20. Fifty-five of 92 features exceed the 0.001 reporting threshold. Held-out LightGBM SHAP ranks `mean_car` fifth, but this model-specific result does not satisfy the pre-specified requirement that both groups appear in the RF top decile.

**SAP v1.0 fields** (`statistical_analysis_plan.md` Part C):
- **Type:** Descriptive ranking, not a classical hypothesis test — no p-value is attached (see `04_statistics_plan.md` §Feature Importance Tests for why).
- **Alpha / Confidence level:** Not applicable — no significance threshold governs a ranking claim.
- **Effect size:** Importance percentage (RF impurity) and SHAP magnitude, reported side by side as corroborating rather than independent effect-size measures.
- **Practical interpretation:** Macro/VIX signal ranks alongside price signal in the RF top decile, while event signal does not. This is a *ranking* result, not a claim that an individual contribution is statistically distinguishable from zero; no p-value was computed for H2.

---

## H3 (supports RQ3) — Event-informed models beat a market-only baseline

**H0:** An ML model trained on the full feature set (price + technical + sentiment + event + macro) does not significantly outperform a model trained on price/technical features only, on held-out test-period RMSE and directional accuracy.

**H1:** The full-feature model achieves significantly lower RMSE and/or significantly higher directional accuracy than the price-only baseline on the same held-out test period.

**Test:** Paired comparison of test-set RMSE and directional accuracy between the full-feature model(s) and the price-only baseline, both trained under an identical `TimeSeriesSplit` protocol with the same random seed (`config.yaml: model.random_seed = 42`). A Diebold–Mariano test (or bootstrap CI on the RMSE difference) is the planned significance test for the RMSE comparison; a two-proportion z-test (or exact binomial test) for the directional-accuracy comparison. See `04_statistics_plan.md` §Model Comparison Tests.

**Decision rule:** Reject H0 only if the RMSE improvement is statistically significant (not just numerically smaller) **and** directional accuracy improvement is significant at α = 0.05.

**Current result (FES v1.1, 2026-07-14):** H0 is not rejected. Event_LASSO is exactly identical to the baseline, making the DM statistic undefined because the loss differential has zero variance; its directional z-test p-value is 0.5000. XGBoost and LightGBM are numerically worse than the baseline, with one-sided DM p-values 0.6097 and 0.6724 and directional z-test p-values 0.9995 and 1.0000. None clears α=0.0167 on either required improvement leg. The dated archive retains the FES v1.0 result for migration audit only.

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
