# 07 — Model Plan

**Purpose:** The complete modelling plan and current result for RQ3 — which models are trained, why, their validation protocol, and the market-only baseline comparison. The prior FES v1.0 test is retained below as history; the FES v1.1 comparison is current.
**Owner:** Ibrahim Haroun.
**Dependencies:** `03_methodology.md` §5, `06_feature_dictionary.md`, `04_statistics_plan.md` §Model Comparison Tests.
**Update Frequency:** Update immediately when the baseline model (below) is added, and whenever hyperparameters are re-tuned.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.5 (Model Specification) and Chapter 4's RQ3 results section.

---

## ✅ Current FES v1.1 comparison (2026-07-14) — H0₃ not rejected

Notebook 07 retrained all candidates on the validated 92-feature matrix, applied the frozen DM/z-test/Bonferroni protocol, generated full SAP diagnostics and held-out SHAP, and passed hash-bound validation. A repeat execution reproduced all 13 primary artefact hashes.

| Model | Test RMSE | Test R² | Test Dir. Acc | Test IC | DM p | z-test p | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `Baseline_LASSO` | 0.009631 | −0.0015 | 0.5747 | undefined | — | — | Benchmark |
| Event_LASSO | 0.009631 | −0.0015 | 0.5747 | undefined | undefined¹ | 0.5000 | Does not beat baseline |
| XGBoost | 0.009656 | −0.0067 | 0.4893 | 0.0249 | 0.6097 | 0.9995 | Does not beat baseline |
| LightGBM | 0.009700 | −0.0158 | 0.4427 | −0.0506 | 0.6724 | 1.0000 | Does not beat baseline |

¹ Event_LASSO and baseline predictions are identical, so the loss differential has zero variance and the DM statistic is mathematically undefined; it is stored as JSON `null`, not fabricated as zero or `NaN`.

The Random Forest RQ2 ranking is also current: 55/92 features exceed 0.001, macro/VIX appears in the top decile, no event feature does, and `mean_car` ranks #20. LightGBM held-out SHAP ranks `mean_car` fifth, a model-specific signal that does not override H2's pre-specified Random Forest rule.

## Historical FES v1.0 comparison (Mission 07, 2026-07-05) — H0₃ not rejected

All three event-enhanced models were retrained on the then-frozen FES v1.0 95-feature matrix. These values are retained for audit/comparison only.

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

## ✅ Baseline frozen (Mission 06, 2026-07-14) — `Baseline_LASSO` v1.1

RQ3 asks whether event-informed models **outperform a market-only baseline**. That baseline is now trained — see `docs/research_bible/model_contract.md` (MCP v1.0), `baseline_model_specification.md`, and `baseline_evaluation.md` for the full specification, evaluation, and interpretation. Summary below; those three documents are authoritative if anything here drifts.

### Baseline specification (current FES v1.1 result)

| Aspect | Specification |
|--------|---------------|
| Model type | `LassoCV`, identical architecture to the existing full-feature LASSO, to isolate the effect of *features* rather than *model type* |
| Feature set | **27** Market-category features from `feature_matrix.parquet` (`docs/research_bible/feature_contract.md`) — price/return/technical indicators derived purely from SPY's own OHLCV, explicitly excluding Macro, Sentiment, Event, Temporal, and Interaction categories. (Note: 27, not the 26 originally estimated below — a `06_feature_dictionary.md` documentation gap, `momentum_21d`, was fixed at the Mission 05B freeze; see `10_decision_log.md`.) |
| Target | `fwd_return_1d` — identical to the full-feature models |
| Train/test split | FES v1.1: train 2016-02-24 → 2022-12-30 (1,727 rows), test 2023-01-03 → 2025-12-29 (750 rows) |
| Validation | `TimeSeriesSplit`, 5 folds, seed 42 — applied to both the outer CV diagnostics and (fixing a legacy gap in `src/models.py`, which defaulted to a shuffled KFold) the inner `LassoCV` alpha-selection CV |
| Hyperparameter tuning | `LassoCV`'s automatic coordinate-descent alpha-path search, same tuning discipline as the full-feature LASSO — genuinely tuned, not left at a default alpha |

### Result — all coefficients shrink to zero (reported as a legitimate null finding, not adjusted)

At the CV-selected alpha (0.0018533887501907256), all 27 Market coefficients shrink to exactly zero; `Baseline_LASSO` reduces to predicting the training-mean return for every test-period day (RMSE 0.009631, Dir. Acc. 0.575 test — numerically identical to the mean predictor, and the 0.575 figure is the test period's base rate of “up” days, not a directional edge; ROC-AUC 0.500 confirms no ranking skill). Notebook 06's validation is `PASS` and its historical FES v1.0 comparison is exact. Full interpretation: `baseline_evaluation.md` Part G.

### Why LASSO for the baseline (not a naive persistence/AR(1) model)

A naive persistence model (predict tomorrow's return = today's return, or = 0) is *too* weak — beating it proves little given financial returns are close to a random walk. A tuned LASSO on price/technical features only is a fairer, still genuinely "market-only" comparator, and reuses the same model class already validated in this project, keeping the model-type variable controlled. Both the persistence model and a random-guess comparator were computed anyway for context (`baseline_evaluation.md` Part D) — `Baseline_LASSO` clears both, but only because a constant mean prediction is a low bar for either naive comparator, not because of genuine market-only linear signal.

### Current 2026-07-14 comparison table and statistical tests

`reports/model_comparison/model_comparison.parquet` holds all four models (Baseline_LASSO, Event_LASSO, XGBoost, LightGBM) × {train, test} in the same RMSE/MAE/R2/Dir_Acc/IC schema. The superseded `data/processed/model_comparison.parquet` is not a current file and survives only in dated archives. The Diebold-Mariano and two-proportion z-test comparisons against `Baseline_LASSO`, Bonferroni-corrected (α = 0.0167), are complete for all three candidates in `reports/model_comparison/statistical_tests.json`.

---

## Model selection criteria (applied 2026-07-05)

A model is reported as "the best RQ3-answering model" only if it beats the baseline on **both** RMSE (via Diebold–Mariano, α = 0.0167 after Bonferroni) **and** directional accuracy (via two-proportion z-test, same α). A model that wins on one metric but not the other should be reported as a mixed result, not rounded up to "outperforms." **Applying this rule to the Mission 07 results: no model qualifies as "the best RQ3-answering model" — none clears even one leg at the corrected threshold.**

## XGBoost overfitting — persists under FES v1.1

The current XGBoost fit reaches train R² 0.2225 but falls to test R² −0.0067. This is a smaller gap than some historical runs but preserves the same out-of-sample failure signature. The evidence establishes persistence, not a unique causal explanation; feature-count-to-sample-size ratio, weak return signal, regime shift, and remaining model flexibility are plausible contributors tracked under `11_limitations.md` L9.

## Explainability handoff — current FES v1.1 outputs

SHAP values for all three event-enhanced models are computed on the FES v1.1 test split using exact linear decomposition for Event_LASSO and each tree library's native contribution API. Maximum reconstruction errors are 0, 2.33×10⁻⁹, and 8.67×10⁻¹⁸ respectively. `shap_importance_summary.parquet` provides the cross-model ranking handoff; Notebook 08 consumed this boundary on 2026-07-14 and regenerated the validated publication figures. Deeper dependence/interaction analysis remains optional future work, not part of the frozen RQ2 rule.
