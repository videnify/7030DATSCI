# 07B — XGBoost Summary (RQ3 Experiment 2)

## Purpose

Second controlled experiment of RQ3, following the same isolated single-model protocol as `07A_event_lasso_summary.md`: does XGBoost, given the full 95-feature `feature_matrix.parquet`, improve next-day SPY return prediction over the locked `Baseline_LASSO`? No comparison against LightGBM, no SHAP, no Random Forest importance, and no significance testing (Diebold-Mariano, two-proportion z-test) is performed in this experiment — all explicitly deferred.

## Model

`XGBoost` — `xgboost.XGBRegressor` (`objective="reg:squarederror"`, `tree_method="hist"`), hyperparameters selected via `RandomizedSearchCV` (`n_iter=25`, `TimeSeriesSplit(5)`, `scoring="neg_root_mean_squared_error"`, `random_state=42`). Same train/test split, feature set (all 95 FES v1.0 features), and persisted `feature_profile.json` scaling as `Baseline_LASSO` and `Event_LASSO` (07A) — scaling is applied uniformly even though tree models do not strictly require it, per `feature_contract.md`'s "identical preprocessing across LASSO/XGBoost/LightGBM" rule, so model architecture remains the only varying factor.

## Features used

All 95 engineered features in `feature_matrix.parquet` — read unmodified, nothing added, removed, or redefined.

## Training strategy

Identical chronological split (train 1,761 rows / test 750 rows), `TimeSeriesSplit(5)`, random seed 42, persisted scaling parameters (never refit) — identical to `Baseline_LASSO` and `Event_LASSO`. Training time: 9.45 seconds (25-iteration randomized search + refit).

**Hyperparameter search space** (`param_distributions`, documented here and in `models/event/xgboost_07b_metadata.json` for full reproducibility): `n_estimators` [200,300,500,700], `max_depth` [3,4,5,6,8], `learning_rate` [0.01,0.03,0.05,0.1,0.2], `subsample` [0.6–1.0], `colsample_bytree` [0.5–1.0], `min_child_weight` [1,3,5,7], `reg_alpha` [0,0.1,0.5,1.0], `reg_lambda` [0.5,1.0,1.5,2.0].

**Selected hyperparameters:** `n_estimators=200`, `max_depth=5`, `learning_rate=0.05`, `subsample=0.9`, `colsample_bytree=0.5`, `min_child_weight=5`, `reg_alpha=0.1`, `reg_lambda=0.5`.

## Metrics

| Split | RMSE | MAE | R² | Dir. Acc | IC |
|---|---|---|---|---|---|
| Train (n=1,761) | 0.007642 | 0.005483 | 0.597 | 0.755 | 0.738 |
| Test (n=750) | 0.009881 | 0.006779 | −0.054 | 0.512 | 0.073 |

Test-split classification-style framing: precision 0.578, recall 0.557, F1 0.567, accuracy 0.512, ROC-AUC 0.517. Confusion matrix (test, n=750): TP=240, FP=175, FN=191, TN=144. 95% CI on test RMSE (block bootstrap, block length 21): [0.007658, 0.012866]. 95% CI on test Dir. Acc. (Wilson score): [0.476, 0.548]. Prediction intervals (empirical residual-quantile, train-split residuals only): 90% [−0.013388, +0.011508], 95% [−0.017481, +0.014052]. Residual diagnostics: skewness 0.769, excess kurtosis 17.39, Durbin-Watson 2.046, Jarque-Bera p<0.001 (non-normal, expected for daily returns), heteroskedasticity correlation 0.330 (unlike the two LASSO models, this is materially non-zero — residual magnitude correlates with prediction magnitude, a signature of the model fitting non-uniform variance in-sample).

## Baseline comparison (`Baseline_LASSO` only — no other model)

| Metric | Baseline_LASSO (test) | XGBoost (test) | Absolute change | Relative change |
|---|---|---|---|---|
| RMSE | 0.009632 | 0.009881 | +0.000249 (worse) | **+2.58%** (worse) |
| MAE | 0.006551 | 0.006779 | +0.000228 | +3.48% (worse) |
| R² | −0.002 | −0.054 | −0.052 (worse) | n/a |
| Dir. Acc | 0.575 | 0.512 | −0.063 (worse) | **−10.9%** (worse) |
| IC | not defined | 0.073 | n/a — first defined value | n/a |
| ROC-AUC | 0.500 | 0.517 | +0.017 | n/a (chance → very weak discrimination) |

**Absolute/relative improvement:** None — XGBoost is descriptively *worse* than `Baseline_LASSO` on RMSE, MAE, R², and directional accuracy in this experiment. Its only advantages are a defined (weakly positive) IC and a ROC-AUC marginally above 0.500.
**Practical significance:** No significance test is run in this experiment (by design). Given the direction and size of the gaps above, a formal test would be very unlikely to find XGBoost superior on either leg — but that conclusion is left to the mission that runs the formal comparison, not asserted here.

## Interpretation

**Has adding event-derived features (via XGBoost) improved prediction?** No — not in this experiment. XGBoost's test-split performance is worse than `Baseline_LASSO`'s on every regression metric (RMSE, MAE, R²) and on raw directional accuracy. This is a materially different, more pronounced result than `Event_LASSO`'s (07A), which was descriptively *better* than the baseline on RMSE/R²/IC/ROC-AUC.

**Statistical evidence:** Descriptive only — no Diebold-Mariano or two-proportion z-test has been run. The gap here (RMSE +2.58% worse, Dir. Acc −10.9% worse) is large enough that a formal test would be unlikely to favour XGBoost, but that determination belongs to the mission that runs the test, not this one.

**Practical importance — overfitting, not lack of signal:** The train/test gap is severe: train R² 0.597 collapses to test R² −0.054, and train directional accuracy (0.755) collapses to worse-than-coin-flip on test (0.512). This reproduces, and in this run's specific hyperparameter draw exceeds in magnitude, the overfitting signature already documented for XGBoost throughout this project (`11_limitations.md` L9, `07_model_plan.md`: legacy train R² 0.554→test R² 0.030; Mission 07 FES v1.0 retrain train R² 0.267→test R² 0.019). The top gain-importance features (`rate_hike_signal`, `mean_car`, `return_lag10d`, `month_sin`, `vix_vs_ma`, `car_positive`) do include genuine event/macro signal (`mean_car`, `car_positive`, `vix_vs_ma`) alongside price/calendar features — so the model is not simply ignoring event information, it is overfitting to it (and to everything else) in-sample without that pattern generalising.

**Limitations:**
1. **Hyperparameter search space is not identical to the original Mission 07 XGBoost run.** Only that run's winning point estimate (`subsample=0.9, reg_lambda=0.5, reg_alpha=0.5, n_estimators=500, min_child_weight=3, max_depth=6, learning_rate=0.1, colsample_bytree=0.5`) was persisted in `models/event/event_model_metadata.json`; the full `param_distributions` it searched over were not recorded anywhere in the Research Bible. This experiment's search space was reconstructed to be a reasonable, standard XGBoost tuning grid consistent with that winning point, but `RandomizedSearchCV`'s result depends on the exact distributions offered — unlike `LassoCV`'s deterministic alpha-path search (07A matched the prior Event_LASSO run to full floating-point precision), an exact numerical match to the prior XGBoost run was not guaranteed here, and did not occur (this run: test RMSE 0.009881, R² −0.054; prior run: test RMSE 0.009533, R² 0.019 — same qualitative overfitting pattern, different severity). **Recommendation logged to `future_improvements.md`: persist full `param_distributions` alongside `best_params` for every future randomized-search model, exactly as this experiment now does, to make tree-model reproducibility as tight as the linear models'.**
2. Root-cause investigation of the overfitting (feature-count-to-sample-size ratio, regularisation strength) remains open and out of scope for this experiment, per the existing `11_limitations.md` L9 item.
3. This is a single hyperparameter search draw (25 iterations) — a larger search budget might find a less-overfit configuration, but expanding the search budget is a methodology change and out of scope here.
4. **RQ3 is not answered by this experiment.** This is Experiment 2 of 3 (07A/07B/07C) — LightGBM (07C) and any formal significance testing remain outstanding.

## Supports

**Research Question:** RQ3 (also informs RQ2 via gain-importance list). **Hypothesis:** H3 (`02_hypotheses.md`) — descriptive evidence only, not yet statistically tested.

## Files

`models/event/xgboost_07b.joblib` (fitted model object), `models/event/xgboost_07b_metadata.json` (hyperparameters, search space, seed, feature list), `reports/event/xgboost_07b_predictions.parquet` (row-level train+test predictions/residuals), `reports/event/xgboost_07b_metrics.json` (full metric suite, matching `reports/baseline/baseline_metrics.json`'s schema).

## Cross-check note

An earlier, broader Mission 07 run (2026-07-05) already trained an XGBoost model on this same feature matrix as part of a three-model comparison (test RMSE 0.009533, R² 0.019, Dir. Acc. 0.556 — also worse than baseline, also overfit, but less severely). This experiment's numbers do not match that run exactly — expected and explained under Limitations item 1 above (different `RandomizedSearchCV` draw, not a data or methodology error). Both runs agree qualitatively: XGBoost overfits and does not beat `Baseline_LASSO` in this project's data regime. This experiment's artefacts are saved under distinct `_07b` filenames so neither run overwrites the other.
