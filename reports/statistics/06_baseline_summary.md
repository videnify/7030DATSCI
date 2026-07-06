# 06 — Baseline Summary

## Purpose

Report the market-only baseline model (`Baseline_LASSO`) that RQ3's event-enhanced models (Mission 07: LASSO, XGBoost, LightGBM on the full 95-feature `feature_matrix.parquet`) must outperform to support H3. This is the last artefact needed to make RQ3 formally testable.

## Model

`Baseline_LASSO` — `sklearn.linear_model.LassoCV`, `TimeSeriesSplit(n_splits=5)` for alpha selection, `random_state=42`, `max_iter=50000`. Selected `alpha = 0.0018492955165777085`. Full specification: `docs/research_bible/baseline_model_specification.md`. Full evaluation: `docs/research_bible/baseline_evaluation.md`.

## Features used

27 Market-category features from `feature_matrix.parquet` (FES v1.0) — SPY price/return/volume history and SPY-derived technical indicators only (returns/lags/cumulative returns, realised volatility, momentum, RSI, Bollinger Bands, moving-average trend flags). No macro, sentiment, event, temporal, or interaction feature is readable by this model — enforced by `docs/research_bible/feature_contract.md`'s Baseline Eligibility table and verified in `baseline_evaluation.md` Part I.

## Training strategy

Chronological split inherited unchanged from `feature_matrix.parquet` (train 2016-01-05 → 2022-12-30, 1,761 rows; test 2023-01-03 → 2025-12-29, 750 rows). `TimeSeriesSplit(5)` for both hyperparameter selection and CV-fold diagnostics — no shuffling. Feature scaling applied using the pre-frozen, train-split-only parameters in `feature_profile.json` (never refit). Same random seed (42) as every other model in this project.

## Metrics

| Split | RMSE | MAE | R² | Dir. Acc |
|---|---|---|---|---|
| Train | 0.012035 | 0.007615 | 0.000 | 0.547 |
| Test | 0.009632 | 0.006551 | −0.002 | 0.575 |

Test-split classification-style framing (direction-as-class): precision 0.575, recall 1.000, F1 0.730, ROC-AUC 0.500. 95% CI on test RMSE (block bootstrap): [0.007634, 0.012449]. 95% CI on test Dir. Acc. (Wilson score): [0.539, 0.610]. Full metric set, comparison baselines (random guess, persistence, mean predictor), residual diagnostics, and prediction intervals: `docs/research_bible/baseline_evaluation.md`, `reports/baseline/baseline_metrics.json`, `reports/tables/06_baseline_metrics.csv`.

## Interpretation

Once genuinely tuned via cross-validated L1 regularisation, `Baseline_LASSO` shrinks all 27 Market coefficients to exactly zero and reduces to predicting the training-split's unconditional mean return every day — numerically identical to a trivial mean predictor. This is reported as a legitimate null finding, not adjusted or re-tuned away: within a linear model, SPY price/technical history alone carries no exploitable signal for next-day returns once regularisation strength is chosen honestly, consistent with weak-form market efficiency and with this project's prior finding that the strongest predictive signal came from event (`mean_car`) and macro (`vix_vs_ma`) features, not price history. The 57.5% test directional accuracy is the test period's base rate of "up" days (431/750), not evidence of skill — confirmed by ROC-AUC = 0.500. Full narrative: `docs/research_bible/baseline_evaluation.md` Part G.

## Limitations

1. A single linear model family (LASSO) is used for the baseline — a tree-based market-only baseline was considered and rejected (`docs/research_bible/10_decision_log.md`, `07_model_plan.md`) to keep model architecture constant across the RQ3 comparison; this means the "no linear signal" finding above does not rule out non-linear market-only signal, a scope boundary worth stating explicitly in Chapter 5.
2. The 27-feature Market category (vs. the previously-stated 26 in `statistical_decision_matrix.md`) reflects a documentation-gap fix made during Mission 05B (`momentum_21d` restored) — noted so the count discrepancy is not mistaken for a new error here.
3. No comparison against event-enhanced models is made in this report — by design, per this mission's scope. Mission 07 performs that comparison.

## Supports

**Research Question:** RQ3. **Hypothesis:** H3 (`02_hypotheses.md`) — this artefact makes H3 testable for the first time; it does not itself test H3.

## Figures

`reports/figures/06a_baseline_diagnostics.png` — test-period prediction vs. actual timeline, predicted-vs-actual scatter, residual histogram, and QQ-plot of standardised residuals.

## Tables

`reports/tables/06_baseline_metrics.csv` — `Baseline_LASSO` (train/test) and the three comparison baselines (test only), same RMSE/MAE/R²/Dir_Acc/IC schema as the existing `data/processed/model_comparison.parquet`, kept as a separate file per this mission's scope (joining into `model_comparison.parquet` and running the DM/z-test comparison is deferred to Mission 07 — see `docs/research_bible/10_decision_log.md`).
