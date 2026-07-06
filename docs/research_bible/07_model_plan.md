# 07 — Model Plan

**Purpose:** The complete modelling plan for RQ3 — which models are trained, why, their validation protocol, and the specification of the market-only baseline and the event-enhanced-vs-baseline comparison. RQ3 is now formally tested (Mission 07, 2026-07-05) — H0₃ is not rejected; see below.
**Owner:** Ibrahim Haroun.
**Dependencies:** `03_methodology.md` §5, `06_feature_dictionary.md`, `04_statistics_plan.md` §Model Comparison Tests.
**Update Frequency:** Update immediately when the baseline model (below) is added, and whenever hyperparameters are re-tuned.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.5 (Model Specification) and Chapter 4's RQ3 results section.

---

## ✅ RQ3 comparison complete (Mission 07, 2026-07-05) — H0₃ not rejected

All three event-enhanced models were retrained on the frozen `feature_matrix.parquet` (FES v1.0, 95 features) — the legacy models below (52-feature `model_features.parquet`) are now superseded. Full detail: `reports/statistics/07_event_models_summary.md`, `docs/research_bible/model_contract.md`.

| Model | Type | Role | Status |
|-------|------|------|--------|
| Event_LASSO | Regularised linear regression | Full-feature event-informed model | ✅ Retrained on FES v1.0 — `LassoCV`, `TimeSeriesSplit(5)`, seed 42; 11/95 nonzero coefficients |
| XGBoost | Gradient-boosted trees | Full-feature event-informed model | ✅ Retrained on FES v1.0 — `RandomizedSearchCV` (n_iter=25, `TimeSeriesSplit(5)`); still shows train/test overfitting (R² 0.267→0.019), reproducing the legacy L9 concern on the new matrix |
| LightGBM | Gradient-boosted trees (leaf-wise) | Full-feature event-informed model | ✅ Retrained on FES v1.0 — `RandomizedSearchCV` (n_iter=25, `TimeSeriesSplit(5)`) |
| `Baseline_LASSO` | Regularised linear regression, Market-only | RQ3 benchmark | ✅ Trained Mission 06 — all coefficients zero (null finding) |

### Result — H0₃ not rejected (Bonferroni α = 0.0167, one-sided)

| Model | Test RMSE | Test Dir. Acc | DM p (RMSE leg) | z-test p (Dir. Acc leg) | Verdict |
|---|---|---|---|---|---|
| Event_LASSO | 0.009465 | 0.564 | 0.056 | 0.662 | Does not beat baseline |
| XGBoost | 0.009533 | 0.556 | 0.163 | 0.767 | Does not beat baseline |
| LightGBM | 0.009529 | 0.549 | 0.161 | 0.839 | Does not beat baseline |

None of the three clears both legs (or either leg) at the corrected threshold — Event_LASSO comes closest (RMSE +1.74% over baseline, DM p=0.056) but does not clear even the uncorrected α=0.05. Directional accuracy is numerically *lower* for all three event-enhanced models than `Baseline_LASSO`'s 0.575 — an artefact of the baseline's constant-positive prediction matching the test period's up-day base rate exactly, not a real deficiency; see `reports/statistics/07_event_models_summary.md` Interpretation for the full caveat. Legacy full-feature numbers below (on the superseded `model_features.parquet`) are retained for historical reference only.

### Legacy models (superseded 2026-07-05 — trained on `model_features.parquet`, not `feature_matrix.parquet`)

| Model | Type | Role | Status |
|-------|------|------|--------|
| LASSO | Regularised linear regression | Interpretable, low-complexity reference model | ✅ Trained (legacy) — was `best_model` per `models/model_metadata.json` |
| XGBoost | Gradient-boosted trees | High-capacity non-linear model | ✅ Trained (legacy) — showed train/test overfitting (see below) |
| LightGBM | Gradient-boosted trees (leaf-wise) | High-capacity non-linear model, faster training | ✅ Trained (legacy) |

**Hyperparameters, validation protocol, and current test-set metrics:** see `03_methodology.md` §5 and `04_statistics_plan.md` §Model Comparison Tests for the full numbers already produced.

---

## ✅ Baseline trained (Mission 06, 2026-07-05) — `Baseline_LASSO` v1.0

RQ3 asks whether event-informed models **outperform a market-only baseline**. That baseline is now trained — see `docs/research_bible/model_contract.md` (MCP v1.0), `baseline_model_specification.md`, and `baseline_evaluation.md` for the full specification, evaluation, and interpretation. Summary below; those three documents are authoritative if anything here drifts.

### Baseline specification (as built, FES v1.0)

| Aspect | Specification |
|--------|---------------|
| Model type | `LassoCV`, identical architecture to the existing full-feature LASSO, to isolate the effect of *features* rather than *model type* |
| Feature set | **27** Market-category features from `feature_matrix.parquet` (`docs/research_bible/feature_contract.md`) — price/return/technical indicators derived purely from SPY's own OHLCV, explicitly excluding Macro, Sentiment, Event, Temporal, and Interaction categories. (Note: 27, not the 26 originally estimated below — a `06_feature_dictionary.md` documentation gap, `momentum_21d`, was fixed at the Mission 05B freeze; see `10_decision_log.md`.) |
| Target | `fwd_return_1d` — identical to the full-feature models |
| Train/test split | `feature_matrix.parquet`'s frozen split: train 2016-01-05 → 2022-12-30 (1,761 rows), test 2023-01-03 → 2025-12-29 (750 rows) — the FES v1.0 warm-up trim shifted the train start date slightly later than originally estimated here (2015-01-05), documented in `05_data_dictionary.md` |
| Validation | `TimeSeriesSplit`, 5 folds, seed 42 — applied to both the outer CV diagnostics and (fixing a legacy gap in `src/models.py`, which defaulted to a shuffled KFold) the inner `LassoCV` alpha-selection CV |
| Hyperparameter tuning | `LassoCV`'s automatic coordinate-descent alpha-path search, same tuning discipline as the full-feature LASSO — genuinely tuned, not left at a default alpha |

### Result — all coefficients shrink to zero (reported as a legitimate null finding, not adjusted)

At the CV-selected alpha (0.00185), all 27 Market coefficients shrink to exactly zero; `Baseline_LASSO` reduces to predicting the training-mean return for every test-period day (RMSE 0.009632, Dir. Acc. 0.575 test — numerically identical to a trivial mean predictor, and the 0.575 figure is the test period's base rate of "up" days, not a directional edge — ROC-AUC 0.500 confirms no ranking skill). Full interpretation: `baseline_evaluation.md` Part G.

### Why LASSO for the baseline (not a naive persistence/AR(1) model)

A naive persistence model (predict tomorrow's return = today's return, or = 0) is *too* weak — beating it proves little given financial returns are close to a random walk. A tuned LASSO on price/technical features only is a fairer, still genuinely "market-only" comparator, and reuses the same model class already validated in this project, keeping the model-type variable controlled. Both the persistence model and a random-guess comparator were computed anyway for context (`baseline_evaluation.md` Part D) — `Baseline_LASSO` clears both, but only because a constant mean prediction is a low bar for either naive comparator, not because of genuine market-only linear signal.

### Resolved 2026-07-05 (Mission 07) — comparison table and statistical tests complete

`reports/model_comparison/model_comparison.parquet` now holds all four models (Baseline_LASSO, Event_LASSO, XGBoost, LightGBM) × {train, test} in the same RMSE/MAE/R2/Dir_Acc/IC schema — kept in `reports/model_comparison/` rather than overwriting the legacy `data/processed/model_comparison.parquet` (which remains on disk as the pre-FES-v1.0 record; see `10_decision_log.md`). The Diebold-Mariano (RMSE) and two-proportion z-test (directional accuracy) comparisons against `Baseline_LASSO`, Bonferroni-corrected (α = 0.0167), are complete for all three event-enhanced models — full results in `reports/model_comparison/statistical_tests.json` and summarised above.

---

## Model selection criteria (applied 2026-07-05)

A model is reported as "the best RQ3-answering model" only if it beats the baseline on **both** RMSE (via Diebold–Mariano, α = 0.0167 after Bonferroni) **and** directional accuracy (via two-proportion z-test, same α). A model that wins on one metric but not the other should be reported as a mixed result, not rounded up to "outperforms." **Applying this rule to the Mission 07 results: no model qualifies as "the best RQ3-answering model" — none clears even one leg at the corrected threshold.**

## XGBoost overfitting — reproduced on the retrained FES v1.0 model, not resolved

The legacy XGBoost's train R² (0.554) collapsed to test R² (0.030) — the same signature reproduces on the FES v1.0 retrain (train R² 0.267 → test R² 0.019, a smaller absolute gap but the same qualitative collapse), despite genuine `RandomizedSearchCV` tuning via `TimeSeriesSplit(5)`. This confirms the overfitting is not an artefact of undertuning or of the specific legacy feature set — it persists across two independently-built feature matrices. A root-cause investigation (feature-count-to-sample-size ratio, regularisation strength) remains open, per `11_limitations.md` L9, and is out of scope for Mission 07 (no methodology changes permitted).

## Explainability handoff — complete for event-enhanced models (Mission 07)

SHAP values for all three event-enhanced models are computed on the FES v1.0 test split (`reports/model_comparison/shap_values_event_lasso.parquet`, `shap_values_xgboost.parquet`, `shap_values_lightgbm.parquet`), using each library's native contribution API (no external `shap`/`numba` dependency) — every model's SHAP values were verified to sum exactly to its own prediction. `Baseline_LASSO` was correctly not SHAP-analysed in Mission 06 (all coefficients zero, so SHAP values would be uniformly zero — nothing to explain) and remains so; Mission 08 (Explainability) is the next consumer of these SHAP artefacts for deeper dependence/interaction analysis.
