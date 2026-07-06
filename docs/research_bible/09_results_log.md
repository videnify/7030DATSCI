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

**Interpretation:** FinBERT's domain mismatch (trained on financial-news headlines, applied to formal presidential/policy language) produces an overwhelmingly neutral, low-discrimination signal. The lexicon method is materially more discriminative and was selected as the primary sentiment signal — logged as a decision in `10_decision_log.md`.

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

## Template fulfilled

The "market-only baseline vs. event-informed models" entry this template was reserved for is now logged above (2026-07-05, Mission 07). Retained here as a reference for the *next* RQ3 re-test (e.g. following a future Feature Matrix or Baseline version bump), not as an open item.
