# 07 — Event Models Summary

## Purpose

Report the retrained event-enhanced models (Event_LASSO, XGBoost, LightGBM) on the full 95-feature `feature_matrix.parquet` (FES v1.0), and the frozen statistical comparison of each against `Baseline_LASSO` (Mission 06) — the last step needed to answer RQ3/H3 with evidence.

## Models

| Model | Algorithm | Tuning | Training time |
|---|---|---|---|
| Event_LASSO | `sklearn.linear_model.LassoCV` | Automatic coordinate-descent alpha-path search, `TimeSeriesSplit(5)` | 0.35s |
| XGBoost | `xgboost.XGBRegressor` | `RandomizedSearchCV`, n_iter=25, `TimeSeriesSplit(5)`, seed 42 | 10.4s |
| LightGBM | `lightgbm.LGBMRegressor` | `RandomizedSearchCV`, n_iter=25, `TimeSeriesSplit(5)`, seed 42 | 3.8s |
| Random Forest (importance tool only) | `sklearn.ensemble.RandomForestRegressor` | Fixed (n_estimators=500) — not a predictive candidate, no CV tuning performed | 12.7s |

Full hyperparameters, versions, and dependencies: `models/event/event_model_metadata.json`. Full specification/fairness discussion: `docs/research_bible/model_contract.md`.

## Features used

All 95 features in `feature_matrix.parquet` (FES v1.0) — Market (27), Macro & VIX (16), Sentiment (25), Event (14), Temporal (5), Interaction (8). Identical feature set for all three predictive models (fairness requirement, `model_contract.md`).

## Training strategy

Identical to `Baseline_LASSO` (Mission 06): `feature_matrix.parquet`'s frozen chronological split (train 1,761 rows / test 750 rows), `TimeSeriesSplit(5)` for all CV, seed 42 throughout, scaling from `feature_profile.json`'s persisted train-split parameters (never refit). No dataset change, no feature engineering change, no statistical methodology change from SAP v1.0 / FES v1.0 / MCP v1.0.

## Metrics (test split, n=750)

| Model | RMSE | MAE | R² | Dir. Acc | IC |
|---|---|---|---|---|---|
| Baseline_LASSO | 0.009632 | 0.006551 | −0.002 | 0.575 | not defined |
| Event_LASSO | 0.009465 | 0.006502 | 0.033 | 0.564 | 0.166 |
| XGBoost | 0.009533 | 0.006581 | 0.019 | 0.556 | 0.160 |
| LightGBM | 0.009529 | 0.006576 | 0.020 | 0.549 | 0.108 |

Full metric suite (precision/recall/F1/ROC-AUC/confusion matrix, residual diagnostics, prediction intervals, bootstrap/Wilson CIs) per model: `reports/model_comparison/statistical_tests.json`, `reports/tables/07_model_comparison.csv`.

## Statistical comparison vs. `Baseline_LASSO` (test split, one-sided, Bonferroni α = 0.0167)

| Model | DM p (RMSE leg) | z-test p (Dir. Acc leg) | % RMSE improvement | pp Dir. Acc change | Verdict |
|---|---|---|---|---|---|
| Event_LASSO | 0.056 | 0.662 | +1.74% | −1.07 pp | Does not beat baseline (neither leg significant) |
| XGBoost | 0.163 | 0.767 | +1.03% | −1.87 pp | Does not beat baseline (neither leg significant) |
| LightGBM | 0.161 | 0.839 | +1.07% | −2.53 pp | Does not beat baseline (neither leg significant) |

BH-FDR correction is not applicable here — it governs RQ1's event-type family only (`statistical_analysis_plan.md` Part A); RQ3's frozen correction is Bonferroni across the 3 models (`statistical_decision_matrix.md` Part K), applied above. No additional hypothesis test was introduced.

## Feature importance (Random Forest, re-run on `feature_matrix.parquet` — replaces all legacy `model_features.parquet`-derived values)

Top 10: `log_return_hi` (market, 0.079), `mean_car` (event, 0.072), `return_lag1d` (market, 0.068), `cum_return_5d` (market, 0.037), `return_lag5d` (market, 0.036), `return_lag3d` (market, 0.035), `vix` (macro, 0.035), `vix_change_5d` (macro, 0.031), `return_lag10d` (market, 0.029), `vix_change_1d` (macro, 0.028). 61/95 features clear the frozen 0.001 importance threshold. Full ranking: `reports/model_comparison/feature_importance.parquet`, `reports/tables/07_feature_importance.csv`.

## SHAP (native TreeSHAP for XGBoost/LightGBM; exact linear SHAP for Event_LASSO)

Computed via each library's built-in contribution API (`xgboost`'s `pred_contribs=True`, `lightgbm`'s `pred_contrib=True`) and the closed-form linear-model SHAP identity for Event_LASSO — no external `shap`/`numba` dependency required. Every model's SHAP values were verified to sum exactly to its own prediction (reconstruction check passed for all three, `reports/model_comparison/shap_values_*.parquet`). `mean_car` and the VIX-derived features corroborate the RF ranking's qualitative shape (event and macro signal present among the top-ranked features across all three models) — full comparison table: `reports/tables/07_shap_importance_summary.csv`, figure: `reports/figures/07c_shap_summary.png`.

## Interpretation — answering RQ3 using evidence only

**None of the three event-enhanced models statistically significantly outperforms `Baseline_LASSO`** at the frozen Bonferroni-corrected threshold (α = 0.0167) on either the RMSE leg (Diebold-Mariano) or the directional-accuracy leg (two-proportion z-test) — H3's decision rule (`02_hypotheses.md`) requires both legs to be significant, and none of the three models clears even one. **H0₃ is not rejected.** This is reported as the honest outcome, not reframed.

Numerically, `Event_LASSO` comes closest: RMSE improves 1.74% over the baseline and its DM p-value (0.056, one-sided, uncorrected) is the smallest of the three — still short of even the uncorrected α = 0.05 threshold, let alone the corrected 0.0167. XGBoost and LightGBM show smaller, non-significant RMSE improvements (1.0–1.1%) and, on the training split, XGBoost's R² (0.267) collapsing to 0.019 on test is the same overfitting signature already documented for the legacy XGBoost model (`11_limitations.md` L9) — reappearing on the retrained FES v1.0 version, not resolved by the feature-matrix rebuild.

**Directional accuracy is lower for all three event-enhanced models than for `Baseline_LASSO`.** This must not be read as the event-enhanced models being "worse at direction" in a meaningful sense: `Baseline_LASSO`'s 0.575 is a mechanical artefact of always predicting a positive constant, which happens to match the test period's 57.5% up-day base rate exactly (`baseline_evaluation.md` Part G) — a model that actually varies its prediction (as all three event-enhanced models do) will inevitably call some days "down" and lose credit on up-days it correctly judged were less certain. The two-proportion z-test comparison above is the frozen SAP procedure and is reported as specified, but its z-statistic here is measuring "did the model match a degenerate always-up baseline's accuracy," not "did the model correctly detect direction" — a caveat any downstream reader of this result must carry forward, not a new statistical adjustment.

**Practical significance:** even Event_LASSO's non-significant 1.74% RMSE improvement and 11-of-95 nonzero coefficients (`mean_car`, `vix`-derived, and price-lag terms retained; see `models/event/event_model_metadata.json`) represent a small, economically marginal edge before any transaction-cost consideration (`11_limitations.md` L2, L10) — this finding does not overstate a tradeable signal.

## Limitations

1. Event_LASSO retains only 11 of 95 features after L1 shrinkage — a sparse, interpretable model, but the RQ2 corroboration above should be read primarily from RF importance/SHAP (all 95 candidates), not from which 11 survived LASSO's penalty.
2. XGBoost's train/test R² gap (0.267 → 0.019) reproduces the pre-existing overfitting concern on the new feature matrix — a candidate for a follow-up regularisation investigation, not resolved in this mission (out of scope: no dataset/methodology changes permitted).
3. The directional-accuracy comparison's dependence on the baseline's degenerate constant prediction (see Interpretation above) means the z-test leg is a weaker, more easily "passed or failed" comparison than the RMSE leg here — worth flagging explicitly in the dissertation Discussion chapter rather than treating both legs as equally informative.
4. RF-importance percentages and SHAP magnitudes above are **not directly comparable** to the legacy `model_features.parquet`-derived percentages in `09_results_log.md` (2026-07-04) — different underlying feature matrix (FES v1.0 vs. the superseded 91-feature matrix) — the legacy numbers are formally superseded by this mission's re-run, per the mission's requirement to "replace all legacy feature-importance values."

## Supports

**Research Question:** RQ3. **Hypothesis:** H3 — this mission provides the test result: **H0₃ is not rejected** (no event-enhanced model beats the baseline on both legs at the corrected threshold).

## Figures

`reports/figures/07a_model_comparison.png` (RMSE/Dir. Acc. bar chart, all 4 models), `07b_feature_importance_rf.png` (top 25 RF importances by category), `07c_shap_summary.png` (SHAP magnitude comparison across models, top 15 features), `07d_residual_analysis.png` (residual distribution and test-period prediction timeline, Event_LASSO vs. Baseline_LASSO).

## Tables

`reports/tables/07_model_comparison.csv`, `reports/tables/07_feature_importance.csv`, `reports/tables/07_shap_importance_summary.csv`; full detail in `reports/model_comparison/model_comparison.parquet`, `statistical_tests.json`, `feature_importance.parquet`, `shap_values_*.parquet`, `event_model_predictions.parquet`.
