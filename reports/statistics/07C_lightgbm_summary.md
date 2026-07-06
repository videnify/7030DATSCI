# 07C — LightGBM Summary (RQ3 Experiment 3)

## Purpose

Third and final controlled experiment in the 07A/07B/07C isolated single-model sequence: does LightGBM, given the full 95-feature `feature_matrix.parquet`, improve next-day SPY return prediction over the locked `Baseline_LASSO`? No comparison against Event_LASSO or XGBoost within this experiment, no SHAP, no Random Forest importance, and no significance testing (Diebold-Mariano, two-proportion z-test) — all explicitly out of scope here, consistent with 07A/07B.

## Model

`LightGBM` — `lightgbm.LGBMRegressor` (`objective="regression"`), hyperparameters selected via `RandomizedSearchCV` (`n_iter=25`, `TimeSeriesSplit(5)`, `scoring="neg_root_mean_squared_error"`, `random_state=42`). Same train/test split, feature set (all 95 FES v1.0 features), and persisted `feature_profile.json` scaling as `Baseline_LASSO`, `Event_LASSO` (07A), and `XGBoost` (07B).

## Features used

All 95 engineered features in `feature_matrix.parquet` — read unmodified, nothing added, removed, or redefined.

## Training strategy

Identical chronological split (train 1,761 rows / test 750 rows), `TimeSeriesSplit(5)`, random seed 42, persisted scaling parameters (never refit). Training time: 7.70 seconds (25-iteration randomized search + refit).

**Hyperparameter search space** (`param_distributions`, persisted in full in `models/event/lightgbm_07c_metadata.json`, per the reproducibility practice adopted in 07B): `n_estimators` [200,300,500,700], `max_depth` [3,4,5,6,−1], `num_leaves` [15,31,47,63], `learning_rate` [0.01,0.03,0.05,0.1,0.2], `subsample` [0.6–1.0], `colsample_bytree` [0.5–1.0], `min_child_samples` [10,20,30,50], `reg_alpha` [0,0.1,0.5,1.0], `reg_lambda` [0.5,1.0,1.5,2.0].

**Selected hyperparameters:** `n_estimators=200`, `max_depth=3`, `num_leaves=31`, `learning_rate=0.01`, `subsample=0.8`, `colsample_bytree=0.6`, `min_child_samples=50`, `reg_alpha=0`, `reg_lambda=1.5`.

## Metrics

| Split | RMSE | MAE | R² | Dir. Acc | IC |
|---|---|---|---|---|---|
| Train (n=1,761) | 0.011299 | 0.007293 | 0.119 | 0.610 | 0.289 |
| Test (n=750) | 0.009470 | 0.006562 | 0.032 | 0.553 | 0.145 |

Test-split classification-style framing: precision 0.588, recall 0.747, F1 0.658, accuracy 0.553, ROC-AUC 0.544. Confusion matrix (test, n=750): TP=322, FP=226, FN=109, TN=93. 95% CI on test RMSE (block bootstrap, block length 21): [0.007541, 0.012037]. 95% CI on test Dir. Acc. (Wilson score): [0.518, 0.589]. Prediction intervals (empirical residual-quantile, train-split residuals only): 90% [−0.018284, +0.014885], 95% [−0.025151, +0.019848]. Residual diagnostics: skewness 0.693, excess kurtosis 16.89, Durbin-Watson 2.078, Jarque-Bera p<0.001 (non-normal, expected), heteroskedasticity correlation 0.254 (moderate, between Event_LASSO's ~0 and XGBoost's 0.330).

## Baseline comparison (`Baseline_LASSO` only — no other model)

| Metric | Baseline_LASSO (test) | LightGBM (test) | Absolute change | Relative change |
|---|---|---|---|---|
| RMSE | 0.009632 | 0.009470 | −0.000162 (better) | **−1.68%** |
| MAE | 0.006551 | 0.006562 | +0.000012 | +0.18% (essentially flat) |
| R² | −0.002 | 0.032 | +0.034 (better) | n/a |
| Dir. Acc | 0.575 | 0.553 | −0.021 (worse) | −3.71% (worse) |
| IC | not defined | 0.145 | n/a — first defined value | n/a |
| ROC-AUC | 0.500 | 0.544 | +0.044 | n/a (chance → weak discrimination) |

**Absolute/relative improvement:** LightGBM reduces test RMSE by 0.000162 (−1.68%) and improves R² from slightly negative to positive — a similar pattern to `Event_LASSO` (07A, −1.74%), though MAE is essentially unchanged (a negligible +0.18% increase, unlike Event_LASSO's small MAE improvement).
**Practical significance:** No significance test run (by design). The RMSE improvement is close in magnitude to Event_LASSO's and much better than XGBoost's (07B, +2.58% worse) — descriptively, LightGBM is the second-best of the three isolated experiments on RMSE, after Event_LASSO.

## Interpretation

**Has adding event-derived features improved prediction?** Descriptively, yes on the same legs as Event_LASSO (RMSE, R², IC, ROC-AUC), no on raw directional accuracy — and for the same reason already established in 07A/`baseline_evaluation.md`: `Baseline_LASSO`'s 0.575 is a mechanical base-rate artefact (constant prediction, ROC-AUC 0.500), not genuine skill, so a lower raw accuracy from a model that actually varies its calls (LightGBM's recall is 0.747, not 1.000) is not read as a deficiency on its own. ROC-AUC of 0.544 indicates weak but real discriminative ability — better than XGBoost's 0.517, weaker than Event_LASSO's 0.575.

**Practical importance — concentrated, event-heavy feature reliance:** LightGBM's gain importance is striking: `mean_car` (the event-study abnormal-return feature) alone accounts for 36.9% of total gain — by far the single most important feature, more than double the next-ranked `return_lag5d` (18.8%). `vix` and `vix_change_1d` (macro) also rank in the top 6. This is the clearest evidence across all three 07A/07B/07C experiments that event-derived information is not merely marginally useful but is the dominant signal this particular model relies on — a materially stronger version of the qualitative pattern already seen in Event_LASSO's retained-feature list (which also kept `mean_car`) and consistent with this project's standing RQ2 finding that `mean_car` ranks among the top features project-wide (`09_results_log.md`, 2026-07-04 and 2026-07-05 entries).

**Overfitting — present, but much milder than XGBoost:** Train R² (0.119) to test R² (0.032) is a real but modest gap, in clear contrast to XGBoost's collapse (0.597 → −0.054, 07B). Train directional accuracy (0.610) to test (0.553) shows the same modest, not severe, pattern. LightGBM's shallower selected tree depth (`max_depth=3`, `num_leaves=31`) relative to XGBoost's (`max_depth=5`) and its lower learning rate (0.01 vs. 0.05) likely explain the difference — consistent with `future_improvements.md`'s newly-logged observation (07B) that overfitting severity is sensitive to the search space and resulting hyperparameters, not a fixed property of the feature set or algorithm family alone.

**Statistical evidence:** Descriptive only — no Diebold-Mariano or two-proportion z-test has been run. The RMSE improvement (−1.68%) is of similar magnitude to Event_LASSO's (−1.74%, DM p=0.056 in the existing 2026-07-05 Mission 07 full comparison, not significant at the corrected threshold) — on that precedent, LightGBM's improvement is very unlikely to clear a Bonferroni-corrected significance threshold either, but that determination is left to a future formal-testing mission, not asserted here.

**Limitations:**
1. Search-space caveat identical to 07B: only the winning `best_params` from the original 2026-07-05 Mission 07 LightGBM run were persisted, not its full search space, so this experiment's reconstructed grid does not guarantee an exact numerical match (and did not produce one — see Cross-check below).
2. Single hyperparameter search draw (25 iterations); a larger budget might find a different configuration.
3. `mean_car`'s dominant gain-importance share (36.9%) means this model's apparent RQ3 improvement is concentrated in one feature — a robustness question (does the improvement survive if `mean_car` alone is removed?) that is out of scope for this experiment but worth flagging for Mission 08 (Explainability) or a future ablation.
4. **RQ3 is not answered by this experiment.** This is Experiment 3 of 3 — with 07A, 07B, and 07C now complete, a formal significance-testing pass (or citing the existing 2026-07-05 Mission 07 DM/z-test results, which already covered all three models) is the next step to actually answer RQ3 under this granular protocol.

## Supports

**Research Question:** RQ3 (also strongly informs RQ2 via the `mean_car`-dominant gain-importance list). **Hypothesis:** H3 (`02_hypotheses.md`) — descriptive evidence only, not yet statistically tested.

## Files

`models/event/lightgbm_07c.joblib` (fitted model object), `models/event/lightgbm_07c_metadata.json` (hyperparameters, search space, seed, feature list), `reports/event/lightgbm_07c_predictions.parquet` (row-level train+test predictions/residuals), `reports/event/lightgbm_07c_metrics.json` (full metric suite, matching `reports/baseline/baseline_metrics.json`'s schema).

## Cross-check note

An earlier, broader Mission 07 run (2026-07-05) already trained a LightGBM model on this same feature matrix (test RMSE 0.009529, R² 0.020, Dir. Acc. 0.549 — also better than baseline on RMSE/R², also worse on raw Dir. Acc.). This experiment's numbers (RMSE 0.009470, R² 0.032, Dir. Acc. 0.553) are close but not identical — consistent with, and explained by, the same `RandomizedSearchCV` search-space caveat logged for 07B (the original run's exact search space was never persisted). Both runs agree qualitatively: LightGBM modestly improves RMSE/R² over baseline without XGBoost-level overfitting, and does not clear raw directional accuracy against the baseline's mechanical rate. This experiment's artefacts are saved under distinct `_07c` filenames so neither run overwrites the other.

## 07A/07B/07C sequence — summary table

| Model | Test RMSE | vs. Baseline | Test R² | Test Dir. Acc | Test IC | Test ROC-AUC | Overfitting (train R² → test R²) |
|---|---|---|---|---|---|---|---|
| `Baseline_LASSO` | 0.009632 | — | −0.002 | 0.575 | not defined | 0.500 | 0.000 → −0.002 (none, constant prediction) |
| Event_LASSO (07A) | 0.009465 | −1.74% | 0.033 | 0.564 | 0.166 | 0.575 | 0.093 → 0.033 (mild) |
| XGBoost (07B) | 0.009881 | +2.58% (worse) | −0.054 | 0.512 | 0.073 | 0.517 | 0.597 → −0.054 (severe) |
| LightGBM (07C) | 0.009470 | −1.68% | 0.032 | 0.553 | 0.145 | 0.544 | 0.119 → 0.032 (mild) |

Descriptively, Event_LASSO and LightGBM show similar, modest RMSE/R² improvements over the baseline with mild overfitting; XGBoost underperforms the baseline outright with severe overfitting in this specific hyperparameter draw. None of these comparisons has been statistically tested in the 07A/07B/07C sequence itself — the existing 2026-07-05 Mission 07 entry already ran the formal Diebold-Mariano/two-proportion z-test protocol on its own (numerically close but not identical) versions of all three models and found H0₃ not rejected for any of them.
