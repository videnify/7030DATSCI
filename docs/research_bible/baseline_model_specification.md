# Baseline Model Specification — `Baseline_LASSO` v1.0

**Purpose:** The exact, reproducible specification of the market-only baseline (`model_contract.md`'s "Baseline" role) — every design choice stated so another researcher (or examiner) can retrain byte-for-byte the same model from `feature_matrix.parquet`.
**Owner:** Senior Data Science Architect / Research Statistician.
**Dependencies:** `model_contract.md` (governance), `feature_contract.md` (feature scope authority), `feature_profile.json` (scaling parameters), `statistical_analysis_plan.md` Part A.
**Update Frequency:** Update only alongside a new Baseline model version.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.5 "Baseline Model" subsection.

---

## Target

`fwd_return_1d` — forward 1-day SPY log return, read unchanged from `feature_matrix.parquet` (itself an unmodified passthrough of `master_dataset.parquet`'s target). Identical target to every event-enhanced model in Mission 07 — this is the one invariant that makes the RQ3 comparison valid.

## Prediction horizon

1 trading day ahead — matches the target definition, no horizon substitution.

## Training dataset

`feature_matrix.parquet`, rows where `split == "train"` (1,761 rows, 2016-01-05 → 2022-12-30 — the 2015 warm-up span was already trimmed at the FES v1.0 freeze, per `feature_matrix_validation.json`), restricted to the 27 **Market**-category columns (`feature_contract.md` Baseline Eligibility table). No Macro, Sentiment, Event, Temporal, or Interaction column is read.

## Testing dataset

`feature_matrix.parquet`, rows where `split == "test"` (750 rows, 2023-01-03 → 2025-12-29) — identical chronological boundary to every other model in this project, per `dataset_contract.md` term 5.

## TimeSeriesSplit

`sklearn.model_selection.TimeSeriesSplit(n_splits=5)`, applied both as the outer CV loop (fold-level RMSE/directional-accuracy diagnostics, reported below) and as the inner CV passed to `LassoCV` for alpha selection. No shuffling anywhere. This corrects a legacy gap: `src/models.py`'s `_lasso_baseline()` passed `LassoCV(cv=5, ...)`, which silently uses a shuffled `KFold` rather than a chronological split — logged as a QA fix in `10_decision_log.md`.

## Scaling

`StandardScaler`-equivalent transform, applied using the **persisted** train-split mean/std from `feature_profile.json.scaling.parameters` (one entry per Market feature) — not refit on this mission's train subset. This guarantees the baseline's scaling is numerically identical to what any Mission 07 model reads for the same 27 columns, so scaling cannot be a confound between the baseline and the event-enhanced models.

## Pipeline

1. Read `feature_matrix.parquet`, filter to the 27 Market columns + `date`/`split`/target.
2. Apply persisted per-feature `(x - mean) / std`.
3. Fit `sklearn.linear_model.LassoCV(cv=TimeSeriesSplit(n_splits=5), random_state=42, max_iter=50000, tol=1e-6, n_jobs=-1)` on the scaled training data.
4. Predict on the scaled test data with the fitted model (`.predict()`, alpha fixed at the CV-selected value — no further refitting on test data at any point).
5. Persist the fitted model object, metadata, predictions, and metrics (see `model_contract.md` "Outputs").

## Hyperparameters

| Hyperparameter | Value | Selection method |
|---|---|---|
| `alpha` (L1 regularisation strength) | **0.0018492955165777085** | `LassoCV`'s automatic coordinate-descent path search, minimising mean cross-validated squared error across a ~100-value alpha grid, evaluated via the `TimeSeriesSplit(5)` folds above |
| `max_iter` | 50,000 | Increased from the legacy default (5,000) to eliminate coordinate-descent convergence warnings — a numerical-stability fix, not a modelling choice |
| `tol` | 1e-6 | Paired with the `max_iter` increase above |
| `fit_intercept` | `True` (scikit-learn default) | Standard practice; the intercept absorbs the unconditional mean return |

## Random seed

`42` throughout — `config.yaml: model.random_seed`, passed to `LassoCV(random_state=42)` and every fold-level refit used for CV diagnostics. Identical seed to every other model in this project.

## Result of tuning — reported exactly as obtained, not adjusted

At the CV-selected `alpha = 0.00185`, **all 27 Market-feature coefficients shrink to exactly zero**; the fitted model reduces to its intercept alone (`0.0004334`, the scaled-training-mean return). This is not a bug — verified directly against the fitted `coef_` array (27/27 exactly `0.0`) — and is not adjusted, cherry-picked, or re-tuned to avoid it, per the no-HARKing discipline this Research Bible already applies elsewhere (`statistical_analysis_plan.md` "Status of this freeze"). See `baseline_evaluation.md` for the full interpretation of what this means for RQ3.
