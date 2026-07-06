# 07A — Event_LASSO Summary (RQ3 Experiment 1)

## Purpose

Report the first controlled experiment of RQ3: whether adding event-derived information (macro, sentiment, event, temporal, interaction features) improves next-day SPY return prediction over the locked `Baseline_LASSO` (market-only, Mission 06). This is not an accuracy-maximisation exercise — it is a same-architecture, same-protocol test of information content. No comparison against XGBoost or LightGBM, and no significance testing (Diebold-Mariano, two-proportion z-test), is performed in this experiment — both are explicitly deferred to later missions.

## Model

`Event_LASSO` — `sklearn.linear_model.LassoCV`, `TimeSeriesSplit(n_splits=5)` for alpha selection, `random_state=42`, `max_iter=50000`, `tol=1e-6`. Selected `alpha = 0.0007347957825603087`. Trained on all 95 FES v1.0 features (Market, Macro & VIX, Sentiment, Event, Temporal, Interaction), unlike `Baseline_LASSO`'s 27 Market-only columns — otherwise identical architecture, CV protocol, and seed, so any performance difference is attributable to information content, not model class.

## Features used

All 95 engineered features in `feature_matrix.parquet` (FES v1.0) — no feature was added, removed, or redefined; `feature_matrix.parquet` was read unmodified. Of the 95, **11 retained non-zero coefficients** at the CV-selected alpha: `log_return`, `return_lag3d`, `return_lag5d`, `return_lag21d` (Market); `vix_change_1d`, `unemployment` (Macro & VIX); `mean_car`, `n_sig_events` (Event); `sent_x_vix_regime`, `monetary_x_vix`, `sent_x_high_vol` (Interaction). The remaining 84 features shrank to exactly zero. Notably, the model retained an event-study feature (`mean_car`) and two sentiment/macro interaction terms — features structurally invisible to `Baseline_LASSO` — rather than relying solely on price history.

## Training strategy

Identical chronological split, `TimeSeriesSplit(5)`, random seed (42), and persisted `feature_profile.json` scaling parameters (never refit) as `Baseline_LASSO` — train 2016-01-05 → 2022-12-30 (1,761 rows), test 2023-01-03 → 2025-12-29 (750 rows). Training time: 0.33 seconds (11 nonzero coefficients out of 95, LassoCV coordinate-descent path search).

## Metrics

| Split | RMSE | MAE | R² | Dir. Acc | IC |
|---|---|---|---|---|---|
| Train (n=1,761) | 0.011459 | 0.007448 | 0.093 | 0.558 | 0.163 |
| Test (n=750) | 0.009465 | 0.006502 | 0.033 | 0.564 | 0.166 |

Test-split classification-style framing (direction-as-class): precision 0.605, recall 0.694, F1 0.646, accuracy 0.564, **ROC-AUC 0.575**. Confusion matrix (test, n=750): TP=299, FP=195, FN=132, TN=124. 95% CI on test RMSE (block bootstrap, block length 21, 2000 resamples): [0.007486, 0.012118]. 95% CI on test Dir. Acc. (Wilson score): [0.528, 0.599]. Prediction intervals (empirical residual-quantile, train-split residuals only): 90% [−0.019484, +0.015529], 95% [−0.025091, +0.020060].

## Baseline comparison (`Baseline_LASSO` only — no other model)

| Metric | Baseline_LASSO (test) | Event_LASSO (test) | Absolute change | Relative change |
|---|---|---|---|---|
| RMSE | 0.009632 | 0.009465 | −0.000168 (lower is better) | **−1.74%** |
| MAE | 0.006551 | 0.006502 | −0.000049 | −0.74% |
| R² | −0.002 | 0.033 | +0.035 | n/a (sign change) |
| Dir. Acc | 0.575 | 0.564 | −0.011 | **−1.86%** (worse) |
| IC | not defined (constant prediction) | 0.166 | n/a — first defined value | n/a |
| ROC-AUC | 0.500 | 0.575 | +0.075 | n/a (chance → weak discrimination) |

**Absolute improvement:** Event_LASSO reduces test RMSE by 0.000168 and improves R² from slightly negative to slightly positive.
**Relative improvement:** ≈1.74% lower RMSE, ≈0.74% lower MAE.
**Practical significance:** No significance test is run in this experiment (Diebold-Mariano and the two-proportion z-test are explicitly out of scope here — deferred to the mission that formally compares all event-enhanced models). The effect sizes above should be read as descriptive only.

## Interpretation

**Has adding event-derived features improved prediction?** Mixed, model-dependent evidence, not a clean "yes." On the RMSE/MAE/R² leg, Event_LASSO is descriptively better than `Baseline_LASSO`: it is the first model in this project's RQ3 line to produce a non-trivial (non-constant) prediction with a positive R² and a defined, positive Information Coefficient (0.166) — meaning its predictions carry genuine rank-correlation with actual returns, something `Baseline_LASSO` structurally cannot claim (its IC is undefined because every prediction is the same constant). ROC-AUC rising from 0.500 (baseline — a constant score has zero rank-ordering power) to 0.575 is further evidence of real, if modest, discriminative ability.

On the raw directional-accuracy leg, Event_LASSO's 56.4% is *below* `Baseline_LASSO`'s 57.5% — but per `baseline_evaluation.md`'s explicit warning, `Baseline_LASSO`'s 57.5% is a mechanical artefact of always predicting "up" in a test period where 57.5% of days were genuinely up (its recall is 1.000 by construction, and its ROC-AUC of 0.500 proves it has no real discriminative power). Event_LASSO's lower raw accuracy comes from a model that actually varies its calls (recall 0.694, not 1.000) and has real, if weak, ranking ability (ROC-AUC 0.575) — so the two accuracy figures are not measuring the same thing, and a naive "0.564 < 0.575, therefore worse" reading would repeat exactly the mistake `baseline_evaluation.md` warned against.

**Statistical evidence:** Descriptive only in this experiment — no Diebold-Mariano or two-proportion z-test has been run, so "Event_LASSO beats Baseline_LASSO" cannot yet be claimed at any confidence level. The promotion criteria in `model_contract.md` (significant on both RMSE and directional accuracy, Bonferroni-corrected) have not been evaluated here by design.

**Practical importance:** The 11 retained non-zero features — particularly `mean_car` (event-study abnormal return signal) and two sentiment/macro interaction terms — indicate the model is drawing on genuinely event-derived information, not merely re-deriving a market signal `Baseline_LASSO` also had access to (which was zero). This is a qualitatively meaningful finding for RQ2/RQ3 regardless of the eventual significance verdict: event and interaction features carry linear signal that market-only features do not.

**Limitations:**
1. This is a single model class (LASSO) — this experiment says nothing about whether a non-linear model (XGBoost, LightGBM) captures more of this signal; that is explicitly Mission 07B/07C's task, not this one.
2. No significance test has been run; the RMSE/directional-accuracy improvements/declines above are effect sizes, not evidence of a statistically reliable difference.
3. Directional accuracy alone is a misleading comparator here given `Baseline_LASSO`'s degenerate constant-prediction behaviour; ROC-AUC is the more informative of the two directional metrics in this specific comparison, a point that must carry forward into any later mission that aggregates directional accuracy across models.
4. **RQ3 is not answered by this experiment.** This is Experiment 1 of a planned 07A/07B/07C sequence — a verdict on H3 requires the remaining experiments and the formal significance-testing mission.

## Supports

**Research Question:** RQ3 (also informs RQ2 via the retained-feature list). **Hypothesis:** H3 (`02_hypotheses.md`) — this experiment provides descriptive, not yet statistically tested, evidence relevant to H3.

## Files

`models/event/event_lasso_07a.joblib` (fitted model object), `models/event/event_lasso_07a_metadata.json` (hyperparameters, seed, feature list), `reports/event/event_lasso_07a_predictions.parquet` (row-level train+test predictions/residuals), `reports/event/event_lasso_07a_metrics.json` (full metric suite, matching `reports/baseline/baseline_metrics.json`'s schema).

## Cross-check note

An earlier, broader Mission 07 run (2026-07-05, `models/event/event_lasso.joblib` / `reports/model_comparison/`) already trained an Event_LASSO model on this same feature matrix as part of a three-model (LASSO/XGBoost/LightGBM) comparison. This experiment's independently re-run numbers match that prior run almost exactly (test RMSE/R²/Dir.Acc/IC identical to displayed precision; train directional accuracy differs by ~0.1 percentage point, consistent with a sign-tie edge case at a near-zero prediction, not a methodological difference) — treated here as a reproducibility cross-check, not a contradiction. This experiment's artefacts are saved under distinct `_07a` filenames so neither run overwrites the other.
