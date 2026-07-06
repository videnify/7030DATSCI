# 09 — Results Log

**Purpose:** A dated, append-only log of headline results as the project progresses — the permanent record of "what did we find and when," so results are never reconstructed from memory or from a notebook's last saved output. Every entry names its source file for re-verification.
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `02_hypotheses.md`, `04_statistics_plan.md`.
**Update Frequency:** **Every time a phase produces a new headline number.** Append, never overwrite — if a number changes on a re-run, add a new dated entry noting the change and why, don't edit the old entry away.
**Relation to Dissertation:** Primary source for dissertation Chapter 4 (Results) — the dissertation text should not contain a number that doesn't trace back to an entry here.

---

## How to log an entry

```
### YYYY-MM-DD — <short title>
**RQ:** RQ1 / RQ2 / RQ3
**Source:** <exact file path>
**Result:** <the number(s), stated precisely>
**Interpretation:** <one or two sentences, no more — save discussion for the dissertation itself>
**Caveats:** <anything that qualifies the result — multiple comparisons, sample size, etc.>
```

---

## 2026-07-04 — Event study: CAR by event type (RQ1)

**RQ:** RQ1
**Source:** `data/processed/car_results.parquet`, `data/processed/causal_estimates.parquet`

**Result:**
| Event Type | Mean CAR | Significant (event-study t-test) |
|------------|----------|:---:|
| Geopolitical | +0.0032 | ✅ p<0.05 |
| Energy | +0.0012 | — |
| Regulatory | +0.0007 | — |
| Trade | −0.0002 | — |
| Monetary | −0.0043 | — |

DoWhy causal effect (lexicon sentiment, pooled across event types): **+0.0051**, 95% CI **[+0.0014, +0.0087]**. Only 4.7% of individual events produced a statistically significant price reaction.

**Interpretation:** The market reacts significantly to a minority of events, and reaction direction is heterogeneous by category — geopolitical events show a significant positive CAR, monetary events show the largest (negative) point estimate but do not reach individual significance. The pooled causal estimate is significant and positive, consistent with sentiment carrying real information content on average even though most individual events don't move price detectably.

**Caveats:** The per-event-type significance flags above are **not yet corrected for multiple comparisons** across the 5 event-type tests (see `04_statistics_plan.md` §Event Study Tests, Benjamini-Hochberg policy) — treat the "✅" above as provisional until that correction is applied and logged as a follow-up entry.

---

## 2026-07-04 — Sentiment scoring method comparison (RQ1 methodology)

**RQ:** RQ1 (methodology choice, feeds RQ2)
**Source:** Root `README.md` Phase 3 section, cross-checked against `data/processed/events_tagged.parquet`

**Result:** FinBERT (document titles): 95.3% neutral, 2.7% positive, 2.0% negative, mean score +0.0067. Lexicon method: 73.1% neutral, 14.5% positive, 12.3% negative.

**Interpretation:** FinBERT's domain mismatch (trained on financial-news headlines, applied to formal presidential/policy language) produces an overwhelmingly neutral, low-discrimination signal. At the time of this entry, the lexicon method was judged materially more discriminative and was selected as the primary sentiment signal — logged as a decision in `10_decision_log.md`.

**Update (2026-07-06, Sentiment Engine Freeze v1.0):** This method-selection reasoning was superseded by a Project Director decision — FinBERT is now the project's official primary sentiment engine, matching the fact that the actual frozen event catalogue is 99.2% FinBERT-sourced, not lexicon-sourced as concluded here. The percentages above are historical and unchanged; see `10_decision_log.md` for the full SEF v1.0 entry.

**Caveats:** Both methods score document *titles* only, not full text — see `11_limitations.md`.

---

## 2026-07-04 — Feature importance ranking (RQ2)

**RQ:** RQ2
**Source:** `data/processed/feature_metadata.parquet`

**Result:** Top 3 of 52 selected features by Random Forest importance: `mean_car` (event, 16.1%), `return_lag1d` (price, 10.2%), `vix_vs_ma` (macro, 10.0%). Full ranking in `06_feature_dictionary.md`.

**Interpretation:** Event-derived signal is not dominant but is not negligible — the top-ranked feature overall is event-derived, ahead of every price and technical feature. Macro (VIX-relative) signal is comparably strong to price-lag signal.

**Caveats:** Impurity-based importance, not a permutation-tested statistic — see `04_statistics_plan.md` §Feature Importance Tests for why no p-value is attached to this ranking.

---

## 2026-07-04 — Model comparison, no baseline yet (RQ3 — incomplete)

**RQ:** RQ3 (partial — baseline missing, see `07_model_plan.md`)
**Source:** `data/processed/model_comparison.parquet`, `models/model_metadata.json`, `models/residual_diagnostics.json`

**Result:**
| Model | Split | RMSE | R² | Dir. Acc | IC |
|-------|-------|------|-----|----------|-----|
| LASSO | test | 0.009465 | 0.033 | 0.564 | 0.179 |
| XGBoost | test | 0.009480 | 0.030 | 0.524 | 0.121 |
| LightGBM | test | 0.009474 | 0.031 | 0.551 | 0.133 |

LASSO train R² 0.092 → test R² 0.033 (stable); XGBoost train R² 0.554 → test R² 0.030 (large overfitting gap); LASSO residuals: Durbin-Watson 2.02, Jarque-Bera p≈0.0 (heavy-tailed, kurtosis 17.26), heteroskedasticity correlation 0.199.

**Interpretation:** LASSO is the most stable of the three event-informed models and is currently flagged `best_model`, with test directional accuracy of 56.4% — modestly above chance. XGBoost shows clear overfitting (large train/test gap). **This table cannot yet answer RQ3** because there is no market-only baseline row to compare against — see `07_model_plan.md` for the specification of the missing baseline model.

**Caveats:** Directional accuracy of 52–56% is close to a coin flip; any RQ3 conclusion once the baseline exists must state both statistical and economic significance explicitly (see `01_research_questions.md` RQ3 sub-question 3, `04_statistics_plan.md`).

---

## 2026-07-04 — Statistical Analysis Plan v1.0 frozen (Mission 04 — process log, not a research result)

**RQ:** N/A — governance/process entry, logged here (rather than only in `10_decision_log.md`) because it changes what counts as a reportable "result" from this date forward.
**Source:** `statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`, `statistical_reporting_guidelines.md`, `dataset_contract.md`.

**Result:** All statistical policy (α = 0.05, two-sided default / one-sided for RQ3, multiple-comparison corrections, missing-data/outlier/transformation/scaling/stationarity policy) and the full test matrix (run and not-yet-run) are frozen at v1.0. RQ1/RQ2 methodology already in use is ratified as-is (no numbers above changed); RQ3's remaining protocol (baseline training, Diebold-Mariano, two-proportion z-test, Bonferroni correction) is frozen prospectively, before it runs.

**Interpretation:** From this point forward, any new statistical method, threshold, or test requires a Version 2 SAP amendment and a `10_decision_log.md` entry — no result above or below this line should be produced using a method not traceable to the SAP suite.

**Caveats:** Benjamini-Hochberg FDR correction on the five event-type CAAR tests (RQ1) is still pending execution, not just pending write-up — see the 2026-07-04 CAR entry above and `13_validation_checklist.md`.

---

## 2026-07-05 — SAP v1.0 EDA implementation on `master_dataset.parquet` (Mission 05A)

**RQ:** Context for RQ1/RQ2 — establishes the empirical baseline the event study and feature engineering are built on.
**Source:** `notebooks/02_eda.ipynb` §9 (new); `reports/tables/02_descriptive_statistics.csv`, `02_stationarity_tests.csv`, `02_correlation_pearson.csv`, `02_correlation_spearman.csv`; `reports/figures/02m`–`02r`.

**Result:**
- **Stationarity (ADF+KPSS):** `log_return` stationary (ADF p<0.001, KPSS p=0.10, agree). `spy_close` and macro **levels** (`fed_funds_rate`, `cpi`, `treasury_10y`, `yield_spread`) non-stationary; their first differences stationary — confirms the differenced macro features already engineered in `06_feature_dictionary.md` are the correct scale. Disagreements (ADF vs. KPSS) on `vix`, `cpi_diff`, `unemployment` — reported as genuine ambiguity, not resolved by picking the convenient test.
- **Normality:** `log_return` excess kurtosis 14.54, QQ-plot shows clear tail departure — non-normal, as expected for daily financial returns and consistent with the LASSO residual Jarque-Bera result already logged (kurtosis 17.26).
- **Correlation:** 23 feature pairs exceed |Pearson r| > 0.90 — mostly structurally expected (OHLC near-duplication, rate-level co-movement); one spurious-trend pairing flagged (`spy_close`/`cpi`, r=0.952 — both non-stationary trending series, not a real relationship).
- **GDELT:** `gdelt_risk_score`/`gdelt_mean_tone`/`gdelt_n_events` are exactly zero (mean = std = 0) across all 2,765 rows — reconfirms L7 at full-dataset scale, not just the 5-day sample scale.
- **ACF/PACF:** negligible autocorrelation in `log_return` beyond lag 1 — consistent with, does not motivate extending, the existing 1/3/5/10/21-day lag feature set.

**Interpretation:** No result above changes any RQ1/RQ2/RQ3 finding already logged — this section validates the assumptions those findings implicitly relied on. All tests were pre-specified in SAP v1.0 (`statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`) before this implementation ran; no new statistical method was introduced.

**Caveats:** VIX/CPI-diff/unemployment ADF-KPSS disagreement is unresolved by design (both tests are retained per policy, not adjudicated); this is a reporting caveat for Chapter 4, not a blocking issue. Feature engineering, model training, and model selection remain out of scope for this mission (Mission 05/06).

---

## 2026-07-05 — Feature Matrix v1.0 frozen (Mission 05B — engineering log, not a new research result)

**RQ:** N/A — governance/engineering entry, logged here because it changes what feature set any future RQ2/RQ3 result is derived from.
**Source:** `data/processed/feature_matrix.parquet`, `feature_matrix_validation.json`, `feature_profile.json`, `docs/research_bible/feature_contract.md`, `06_feature_dictionary.md`.

**Result:** 95 candidate engineered features frozen (Market 27, Macro & VIX 16, Sentiment 25, Event 14, Temporal 5, Interaction 8) across 2,511 rows (train 1,761 / test 750), built from `master_dataset.parquet` + `car_results.parquet` only. Validation: **PASS** — 0 duplicate/constant/near-zero-variance features, 0 unexpected nulls, 0 target-leakage mismatches, non-anticipative lag structure spot-checked. 6 feature pairs flagged \|Pearson r\|>0.90 (train split) and 10 features flagged VIF>10 — all structurally expected (overlapping rolling windows, an interaction term vs. its own parent, momentum vs. cumulative-return near-identity) and documented per-feature, none auto-dropped per the frozen SAP policy.

**Interpretation:** This is an engineering freeze, not a new RQ1–RQ3 finding — no model has been trained on this matrix yet. It closes the single largest ambiguity blocking Mission 06 (Baseline Model): the market-only baseline's feature scope is now contractually fixed at the 27 Market-category columns (`feature_contract.md`), so RQ3's model comparison cannot accidentally leak event/macro/sentiment signal into the baseline.

**Caveats:** RF-importance selection (the step that produced the legacy "top 3 features" RQ2 result, `09_results_log.md` 2026-07-04) has **not** been re-run against this new matrix — the old percentages (`mean_car` 16.1%, `return_lag1d` 10.2%, `vix_vs_ma` 10.0%) were computed on the superseded `model_features.parquet` and must not be quoted as if they already describe `feature_matrix.parquet`. The market-only baseline's feature count is 27, not the 26 previously stated in `statistical_decision_matrix.md` — a documentation gap (missing `momentum_21d`) fixed during this freeze, see `10_decision_log.md`.

---

## 2026-07-05 — Market-only baseline trained: `Baseline_LASSO` v1.0 (Mission 06 — RQ3 partially unblocked)

**RQ:** RQ3
**Source:** `reports/baseline/baseline_metrics.json`, `reports/baseline/baseline_predictions.parquet`, `models/baseline/baseline_model_metadata.json`, `docs/research_bible/baseline_evaluation.md`.

**Result:** `Baseline_LASSO` (LassoCV, `TimeSeriesSplit(5)`, seed 42, 27 Market-category features only) selects alpha = 0.0018492955165777085, at which **all 27 coefficients shrink to exactly zero**. Test-split metrics: RMSE 0.009632, MAE 0.006551, R² −0.002, Dir. Acc. 0.575 (95% Wilson CI [0.539, 0.610]), IC not defined (constant prediction). These are numerically identical to a trivial train-mean predictor. Comparison-only context (not official RQ3 contenders): Random Guess Dir. Acc. 0.519, Persistence Dir. Acc. 0.508 — `Baseline_LASSO` clears both, but only because they are weak comparators, not because of genuine market-only linear signal.

**Interpretation:** The market-only baseline, honestly tuned via cross-validated L1 regularisation, contains no exploitable linear signal in SPY price/technical history for next-day returns — a legitimate null finding, consistent with weak-form market efficiency and with this project's existing RQ2 finding that the strongest signal came from event (`mean_car`) and macro (`vix_vs_ma`) features rather than price history. This makes RQ3 formally testable for the first time (H3 was previously "untestable as specified," `02_hypotheses.md`) — Mission 07 must now train the full-feature LASSO/XGBoost/LightGBM against this exact number and run the Diebold-Mariano / two-proportion z-test comparison.

**Caveats:** The 0.575 test directional accuracy equals the test period's base rate of "up" days (431/750) — confirmed by ROC-AUC = 0.500 (ranking power exactly at chance) — and must not be read as a directional edge in any downstream write-up. Only a single model family (LASSO) was used for the baseline; a market-only tree-based baseline was considered and explicitly not added, to keep model architecture constant across the RQ3 comparison (`10_decision_log.md`). `Baseline_LASSO` has not yet been joined to `model_comparison.parquet` or formally compared against the event-enhanced models — that is Mission 07, not this entry.

---

## 2026-07-05 — RQ3 model comparison complete: H0₃ not rejected (Mission 07)

**RQ:** RQ3
**Source:** `reports/model_comparison/model_comparison.parquet`, `reports/model_comparison/statistical_tests.json`, `reports/model_comparison/feature_importance.parquet`, `reports/model_comparison/shap_values_*.parquet`, `models/event/event_model_metadata.json`.

**Result:** Event_LASSO, XGBoost, and LightGBM were retrained on `feature_matrix.parquet` (FES v1.0, 95 features), identical split/`TimeSeriesSplit(5)`/seed 42/scaling to `Baseline_LASSO`. Test-split metrics: Event_LASSO RMSE 0.009465 (R² 0.033, Dir. Acc. 0.564), XGBoost RMSE 0.009533 (R² 0.019, Dir. Acc. 0.556), LightGBM RMSE 0.009529 (R² 0.020, Dir. Acc. 0.549) — vs. `Baseline_LASSO` RMSE 0.009632 (Dir. Acc. 0.575). Diebold-Mariano (RMSE leg) one-sided p-values: 0.056 (Event_LASSO), 0.163 (XGBoost), 0.161 (LightGBM). Two-proportion z-test (Dir. Acc. leg) one-sided p-values: 0.662, 0.767, 0.839 respectively. **None clears the Bonferroni-corrected threshold (α = 0.0167) on either leg — H0₃ is not rejected.**

**Interpretation:** No event-enhanced model statistically significantly outperforms the market-only baseline at the frozen threshold. Event_LASSO is numerically closest (+1.74% RMSE improvement, smallest p-value) but does not clear even the uncorrected α = 0.05. All three event-enhanced models show *lower* raw directional accuracy than `Baseline_LASSO` — a mechanical consequence of the baseline's constant-positive prediction matching the test period's 57.5% up-day base rate exactly, not a genuine directional deficiency in the event-enhanced models (see `reports/statistics/07_event_models_summary.md` for the full caveat). XGBoost's overfitting (train R² 0.267 → test R² 0.019) reproduces on the new feature matrix, confirming it is not an artefact of the superseded feature set. Random Forest importance (re-run on `feature_matrix.parquet`, replacing all legacy `model_features.parquet`-derived values) ranks `mean_car` (event) #2 overall and several VIX-derived macro features in the top 10 — qualitatively consistent with the legacy RQ2 finding that event/macro signal ranks alongside price signal, cross-corroborated by native TreeSHAP (XGBoost/LightGBM) and exact linear SHAP (Event_LASSO).

**Caveats:** This is a null result for H3 and is reported as such, not reframed. The directional-accuracy leg's dependence on a degenerate baseline (see Interpretation) means it is a weaker comparison than the RMSE leg for this specific baseline; a future Feature Matrix or Baseline version that produces a non-degenerate baseline would give a fairer Dir. Acc. comparison. XGBoost's overfitting remains uninvestigated at the root-cause level (`11_limitations.md` L9) — out of scope for this mission (no methodology changes permitted). RF/SHAP importance percentages above supersede, and are not directly comparable to, the legacy 2026-07-04 percentages (different underlying feature matrix).

---

## 2026-07-06 — Event_LASSO isolated re-run: RQ3 Experiment 1 of 3 (Mission 07A)

**RQ:** RQ3 (also informs RQ2 via retained-feature list)
**Source:** `reports/event/event_lasso_07a_metrics.json`, `reports/event/event_lasso_07a_predictions.parquet`, `models/event/event_lasso_07a_metadata.json`, `reports/statistics/07A_event_lasso_summary.md`.

**Result:** `Event_LASSO` retrained in isolation (all 95 FES v1.0 features, identical split/`TimeSeriesSplit(5)`/seed 42/persisted scaling to `Baseline_LASSO`) as the first of a planned three-part RQ3 experiment sequence (07A Event_LASSO / 07B / 07C). Selected alpha = 0.0007347957825603087; 11/95 coefficients retained non-zero (`log_return`, `return_lag3d`, `return_lag5d`, `return_lag21d`, `vix_change_1d`, `unemployment`, `mean_car`, `n_sig_events`, `sent_x_vix_regime`, `monetary_x_vix`, `sent_x_high_vol`). Test-split: RMSE 0.009465 (−1.74% vs. `Baseline_LASSO`'s 0.009632), MAE 0.006502, R² 0.033 (vs. −0.002), Dir. Acc. 0.564 (vs. 0.575), IC 0.166 (first defined IC in the RQ3 line — `Baseline_LASSO`'s is undefined), ROC-AUC 0.575 (vs. 0.500).

**Interpretation:** Descriptive-only evidence (no Diebold-Mariano or two-proportion z-test run in this experiment, by design — see `10_decision_log.md`). Event_LASSO shows better RMSE/MAE/R²/IC/ROC-AUC than `Baseline_LASSO` but *lower* raw directional accuracy — the latter is not read as a deficiency, since `Baseline_LASSO`'s 0.575 is a mechanical base-rate artefact (constant prediction, ROC-AUC 0.500) rather than genuine skill, per `baseline_evaluation.md`'s standing caveat. The retained feature list — including the event-study `mean_car` and two sentiment/macro interaction terms — is qualitative evidence that event-derived information carries linear signal beyond what `Baseline_LASSO` can access (which was zero).

**Cross-check:** This isolated re-run's test-split metrics match the existing 2026-07-05 Mission 07 Event_LASSO entry above almost exactly (RMSE/R²/Dir.Acc/IC identical to displayed precision; train Dir. Acc. differs by ~0.1 percentage point, consistent with a sign-tie edge case, not a methodology difference) — treated as a reproducibility confirmation, not a new number superseding the prior one. Saved under distinct `_07a`-suffixed filenames so neither run's artefacts overwrite the other.

**Caveats:** RQ3 is **not** answered by this entry — this is Experiment 1 of 3; XGBoost/LightGBM (07B/07C) and any formal significance testing remain outstanding for this narrower experiment sequence (the 2026-07-05 Mission 07 entry already ran the full three-model DM/z-test comparison, but this 07A/07B/07C sequence re-derives the same ground more granularly per the current mission structure — both are retained, not in conflict, since neither is a Feature Matrix or Baseline version change).

---

## 2026-07-06 — XGBoost isolated re-run: RQ3 Experiment 2 of 3 (Mission 07B)

**RQ:** RQ3 (also informs RQ2 via gain-importance list)
**Source:** `reports/event/xgboost_07b_metrics.json`, `reports/event/xgboost_07b_predictions.parquet`, `models/event/xgboost_07b_metadata.json`, `reports/statistics/07B_xgboost_summary.md`.

**Result:** `XGBoost` retrained in isolation (all 95 FES v1.0 features, identical split/`TimeSeriesSplit(5)`/seed 42/persisted scaling to `Baseline_LASSO`/`Event_LASSO`), tuned via `RandomizedSearchCV` (n_iter=25, `TimeSeriesSplit(5)`, seed 42). Selected params: `n_estimators=200, max_depth=5, learning_rate=0.05, subsample=0.9, colsample_bytree=0.5, min_child_weight=5, reg_alpha=0.1, reg_lambda=0.5`. Test-split: RMSE 0.009881 (+2.58% *worse* than `Baseline_LASSO`'s 0.009632), MAE 0.006779, R² −0.054 (vs. −0.002), Dir. Acc. 0.512 (vs. 0.575), IC 0.073 (first defined value for this model), ROC-AUC 0.517 (vs. 0.500). Train R² 0.597 collapses to test R² −0.054 — severe overfitting.

**Interpretation:** Unlike `Event_LASSO` (07A), XGBoost is descriptively *worse* than `Baseline_LASSO` on every regression metric and on raw directional accuracy in this experiment — no evidence here that event-derived features improve prediction via this model. The train/test collapse reproduces (and in this specific hyperparameter draw, exceeds in magnitude) the XGBoost overfitting already documented at two prior feature-matrix versions (`11_limitations.md` L9: legacy train R² 0.554→test R² 0.030; 2026-07-05 FES v1.0 retrain train R² 0.267→test R² 0.019). Top gain-importance features include genuine event/macro signal (`mean_car`, `car_positive`, `vix_vs_ma`) alongside price/calendar features, indicating the model is overfitting to (not ignoring) event information.

**Cross-check:** This run's numbers do **not** match the 2026-07-05 Mission 07 XGBoost entry exactly (that run: test RMSE 0.009533, R² 0.019, Dir. Acc. 0.556) — expected, since `RandomizedSearchCV`'s exact result depends on the full `param_distributions` searched, and only the prior run's winning point estimate was persisted in `event_model_metadata.json`, not its full search space. This experiment's search space (documented in `models/event/xgboost_07b_metadata.json`) was reconstructed as a reasonable standard grid consistent with that winning point, but an exact match was not guaranteed and did not occur — both runs agree qualitatively (XGBoost overfits, does not beat baseline).

**Caveats:** RQ3 is **not** answered by this entry — this is Experiment 2 of 3; LightGBM (07C) and any formal significance testing remain outstanding. No significance test run in this experiment, by design. A recommendation to persist full `param_distributions` for every future randomized-search model (as done here) is logged in `future_improvements.md` so future tree-model re-runs can be reproduced as tightly as `Event_LASSO`'s deterministic `LassoCV` path search.

---

## 2026-07-06 — LightGBM isolated re-run: RQ3 Experiment 3 of 3 (Mission 07C) — sequence complete

**RQ:** RQ3 (also strongly informs RQ2 via gain-importance list)
**Source:** `reports/event/lightgbm_07c_metrics.json`, `reports/event/lightgbm_07c_predictions.parquet`, `models/event/lightgbm_07c_metadata.json`, `reports/statistics/07C_lightgbm_summary.md`.

**Result:** `LightGBM` retrained in isolation (all 95 FES v1.0 features, identical split/`TimeSeriesSplit(5)`/seed 42/persisted scaling to `Baseline_LASSO`/07A/07B), tuned via `RandomizedSearchCV` (n_iter=25, `TimeSeriesSplit(5)`, seed 42; full `param_distributions` persisted per the 07B recommendation). Selected params: `n_estimators=200, max_depth=3, num_leaves=31, learning_rate=0.01, subsample=0.8, colsample_bytree=0.6, min_child_samples=50, reg_alpha=0, reg_lambda=1.5`. Test-split: RMSE 0.009470 (−1.68% vs. `Baseline_LASSO`'s 0.009632), MAE 0.006562 (+0.18%, essentially flat), R² 0.032 (vs. −0.002), Dir. Acc. 0.553 (vs. 0.575), IC 0.145, ROC-AUC 0.544 (vs. 0.500). Train R² 0.119 → test R² 0.032 — mild, not severe, overfitting (contrast with 07B's XGBoost collapse of 0.597 → −0.054).

**Interpretation:** LightGBM's pattern matches `Event_LASSO` (07A) more closely than `XGBoost` (07B): descriptively better than baseline on RMSE/R²/IC/ROC-AUC, worse on raw directional accuracy for the same base-rate reason already established. The standout finding is gain-importance concentration: `mean_car` alone accounts for 36.9% of total gain, more than double the next feature (`return_lag5d`, 18.8%) — the strongest single-feature evidence across all three 07A/07B/07C experiments that event-study information (not just macro/sentiment generally) drives this project's clearest event-enhanced signal. This corroborates, with more concentration than before, the standing RQ2 finding that `mean_car` ranks among the top predictive features project-wide.

**07A/07B/07C sequence complete — summary:**

| Model | Test RMSE | vs. Baseline | Test R² | Test Dir. Acc | Overfitting |
|---|---|---|---|---|---|
| `Baseline_LASSO` | 0.009632 | — | −0.002 | 0.575 | None (constant) |
| Event_LASSO (07A) | 0.009465 | −1.74% | 0.033 | 0.564 | Mild |
| XGBoost (07B) | 0.009881 | +2.58% (worse) | −0.054 | 0.512 | Severe |
| LightGBM (07C) | 0.009470 | −1.68% | 0.032 | 0.553 | Mild |

**Cross-check:** As with 07B, this run's numbers are close to, but do not exactly match, the 2026-07-05 Mission 07 LightGBM entry (test RMSE 0.009529, R² 0.020, Dir. Acc. 0.549) — same search-space-not-persisted caveat as 07B, both runs agree qualitatively.

**Caveats:** RQ3 is still **not formally answered** by the 07A/07B/07C sequence itself — no Diebold-Mariano or two-proportion z-test has been run within this sequence for any of the three models. The existing 2026-07-05 Mission 07 entry already ran that formal protocol on its own (numerically close) versions of all three models and found H0₃ not rejected for each. Given how closely both sets of numbers agree in direction and rough magnitude, a formal test on this sequence's own numbers would very likely reach the same qualitative verdict, but that is a determination for a dedicated significance-testing mission to make, not asserted here. `mean_car`'s dominant share of LightGBM's gain importance (36.9%) raises a robustness question (does the RMSE improvement survive without it?) flagged for Mission 08 or a future ablation, not answered here.

---

## Template fulfilled

The "market-only baseline vs. event-informed models" entry this template was reserved for is now logged above (2026-07-05, Mission 07). Retained here as a reference for the *next* RQ3 re-test (e.g. following a future Feature Matrix or Baseline version bump), not as an open item.

---

## 2026-07-06 — Mission 03-PRECHECK: event-detection notebook alignment (process log, not a research result)

**RQ:** N/A — governance/documentation entry, logged here because it confirms no research number in this log changes as a result.
**Source:** `notebooks/03_event_detection.ipynb` (documentation cells added: expanded title/purpose header, EDA cross-reference, event-definitions table, pre-save validation cell, post-save verification cell, handoff section); `docs/research_bible/{05_data_dictionary.md, 10_decision_log.md, dataset_contract.md, 15_traceability_matrix.md, statistical_decision_matrix.md}` (reviewed, cross-checked, no conflicts found).

**Result:** `03_event_detection.ipynb` confirmed consistent with `02_eda.ipynb`'s EDA findings (stationarity, GDELT limitation, weak raw correlations — see the notebook's new "Link to EDA" section for the exact citations), the frozen Research Bible, and SAP v1.0. Two scope clarifications were made explicit and logged as decisions (`10_decision_log.md`, 2026-07-06): (1) this notebook must not consume `master_dataset.parquet` (circular dependency — `master_dataset.parquet` is built from this notebook's own `daily_sentiment.parquet` output), and (2) event-window construction remains solely in `04_causal_analysis.ipynb`, not duplicated here. No existing executable cell was modified; two new read-only validation/verification code cells were added.

**Interpretation:** This notebook was already substantively well-aligned with the rest of the pipeline — the alignment pass found documentation gaps (no explicit RQ/hypothesis/EDA-link header, no consolidated event-definitions table, no pre-save validation checks) rather than logic errors. The one thing worth flagging forward: the mission brief that triggered this pass suggested inputs/outputs (`master_dataset.parquet` as an input; `detected_events.parquet`/`event_windows.parquet`/`event_calendar.parquet` as outputs) that do not match the actual, correct pipeline dependency graph — this mismatch was identified and not applied, rather than followed mechanically.

**Caveats:** The two new validation cells (`validation-checks`, `post-save-verification`) have not yet been executed — their diagnostic output will only exist once the notebook is next run top-to-bottom. This entry records that the checks were *added*, not that they have *passed*.

---

## 2026-07-06 — Mission 03: full execution, validation, and freeze of `03_event_detection.ipynb`

**RQ:** RQ1/RQ2 (this notebook's outputs feed both, per `15_traceability_matrix.md`).
**Source:** Live top-to-bottom execution via `nbclient`; `data/processed/{events_tagged,daily_sentiment,high_impact_events,gdelt_daily_risk}.parquet`; `reports/figures/03{a,b,c,d}_*.png`.

**Result:**
- **Catalogue:** 11,664 total events — 11,570 core-president APP documents + 89 FOMC decisions + 5 GDELT rows. Event-type distribution: other 6,392 (54.8%), regulatory 2,246 (19.3%), geopolitical 1,617 (13.9%), health 438, monetary 293, trade 276, labour 243, energy 159.
- **Sentiment:** 11,081 neutral (95.0%), 324 positive (2.8%), 259 negative (2.2%); mean numeric sentiment +0.0054. `sentiment_source`: `finbert` 11,570 (99.2%, reused from a prior cache), `rule` 89, `gdelt_goldstein` 5.
- **High-impact events:** 4,100 of 11,664 (35.2%) — regulatory 2,019, geopolitical 1,453, trade 253, monetary 227, energy 148.
- **Validation checks (new, `validation-checks` cell):** 124 duplicate `(date, title, doc_type)` rows found (genuine same-day, identically-titled documents — e.g. recurring proclamation/press-briefing titles — not a pipeline defect); 0 null dates; **5 rows outside the nominal 2015–2025 study window**, all GDELT (`date` 2026-05-02 → 2026-05-06 — the "5-day sample" is a recent live pull, not a historical sample drawn from within the study period); 0 missing sentiment labels.
- **Post-save verification:** all 4 output files confirmed on disk with shapes matching the in-memory objects exactly.
- Two runtime bugs found and fixed during execution (see `10_decision_log.md` for full reasoning): a `KeyError: 'decision'` from an upstream `fomc_dates.parquet` column rename (`decision` → `rate_decision`), and a cache-merge row-explosion in the sentiment-scoring cell (fixed by deduplicating the cache on `title` before merging).

**Interpretation:** The notebook now executes cleanly end-to-end and its outputs are verified consistent with what the code actually produces (not assumed from stale documentation). Two corrections to prior Research Bible entries follow directly: `events_tagged.parquet`/`high_impact_events.parquet` row counts in `05_data_dictionary.md` were substantially wrong (180,594/7,864 vs. the actual 11,664/4,100) and are now fixed. Separately, and more substantively, the actual sentiment signal in this catalogue is dominantly FinBERT-sourced (99.2% of rows), which contradicts the "lexicon is primary" methodology decision recorded elsewhere in this Research Bible — flagged in `10_decision_log.md` as requiring a founder decision, not resolved here. The GDELT date-range finding (5 rows entirely in 2026-05, outside 2015–2025) sharpens `11_limitations.md` L7: the sample isn't just short, it doesn't overlap the study period at all, reinforcing that it should not be treated as an active predictor (consistent with `02_eda.ipynb` §9.2's finding that `gdelt_*` columns show no variation in `master_dataset.parquet`).

**Caveats:** This notebook's own outputs (`events_tagged.parquet` etc.) were regenerated by this execution — `master_dataset.parquet` and `feature_matrix.parquet` (both frozen, both read-only per their contracts) were **not** touched, re-derived, or re-validated against these new numbers. If a future session wants to confirm `master_dataset.parquet` still accurately reflects the current `daily_sentiment.parquet`, that comparison has not been done here and should not be assumed to pass.

**Resolved (2026-07-06, Sentiment Engine Freeze v1.0):** The Project Director ratified FinBERT as the project's official primary sentiment engine, matching this notebook's actual output rather than the previously documented "lexicon is primary" position. Documentation updated accordingly across the Research Bible, README, and Notebook 03 — no datasets, models, or statistical outputs were changed. See `10_decision_log.md`.
