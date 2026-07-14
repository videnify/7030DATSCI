# models/

**Purpose:** Trained model binaries and their metadata. Gitignored — every file here is reproducible by re-running `06_model_training.ipynb` (baseline) and `07_model_evaluation.ipynb` (event-enhanced models).
**Added:** 2026-07-13 (this folder previously had a README, per `DATSCI7030_Repository_Audit_Report.ipynb`, but it went stale and was subsequently lost — this version was written directly against what's on disk).

## Contents

| Path | Produced by | Notes |
|------|-------------|-------|
| `baseline/baseline_lasso.joblib` | `06_model_training.ipynb` | `Baseline_LASSO` — market-only (27 Market-category features), MCP v1.0. All coefficients shrink to zero at the CV-selected alpha (null finding). |
| `baseline/baseline_model_metadata.json` | `06_model_training.ipynb` | Hyperparameters and training metadata for the baseline |
| `event/event_lasso.joblib` | `07_model_evaluation.ipynb` | `Event_LASSO` — full 95-feature set. As of the 2026-07-13 rebuild, collapses to the same all-zero coefficients as the baseline (see `docs/research_bible/10_decision_log.md`). |
| `event/xgboost.joblib`, `event/lightgbm.joblib` | `07_model_evaluation.ipynb` | Event-enhanced tree models, refit from recorded hyperparameters |
| `event/event_model_metadata.json` | Reconstructed 2026-07-13 from the dissertation's Table 7 | The original file was lost from the repository entirely; XGBoost/LightGBM hyperparameters were reconstructed from the only surviving authoritative source rather than re-run via `RandomizedSearchCV` (which would produce different, non-reproducible values) — see `10_decision_log.md`. |
| `archive/pre_2026-07-13_pipeline_rebuild/` | Moved, not produced | Stale pre-rebuild `reports/` artefacts (baseline metrics, model comparisons, SHAP values, per-model statistics summaries) archived rather than deleted during the 2026-07-13 rebuild, since they had no current producer and risked being paired with freshly-trained models. |

## Dependencies

`data/processed/feature_matrix.parquet`, `docs/research_bible/{model_contract.md, feature_contract.md}`.
