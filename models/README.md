# models/

**Purpose:** Trained model binaries and their metadata. Gitignored — every file here is reproducible by re-running `06_model_training.ipynb` (baseline) and `07_model_evaluation.ipynb` (event-enhanced models).
**Added:** 2026-07-13 (this folder previously had a README, per `DATSCI7030_Repository_Audit_Report.ipynb`, but it went stale and was subsequently lost — this version was written directly against what's on disk).

## Contents

| Path | Produced by | Notes |
|------|-------------|-------|
| `baseline/baseline_lasso.joblib` | `06_model_training.ipynb` | Current `Baseline_LASSO` v1.1 — 27 Market features from FES v1.1, MCP v1.0; all coefficients zero at the CV-selected alpha. |
| `baseline/baseline_model_metadata.json` | `06_model_training.ipynb` | FES v1.1-bound hyperparameters and training metadata; current validation lives in `reports/baseline/baseline_model_validation.json`. |
| `archive/pre_fes_v1_1_notebook06_2026-07-14/` | Controlled Notebook 06 migration | Dated FES v1.0 baseline model and metadata retained before the canonical v1.1 paths were replaced. |
| `event/event_lasso.joblib` | `07_model_evaluation.ipynb` | Current FES v1.1 full-feature LASSO (92 features); 0 non-zero coefficients and predictions exactly equal to `Baseline_LASSO`. |
| `event/xgboost.joblib`, `event/lightgbm.joblib` | `07_model_evaluation.ipynb` | Current FES v1.1 event-enhanced tree models, refit from the frozen recorded hyperparameters; neither beats the baseline under MCP v1.0. |
| `event/random_forest_importance_tool.joblib` | `07_model_evaluation.ipynb` | Current fixed Random Forest (`n_estimators=500`, seed 42) used only for the reproducible RQ2 importance ranking. |
| `event/event_model_metadata.json` | `07_model_evaluation.ipynb` | Current FES v1.1 suite metadata, feature/hash bindings, model parameters, validation reference, and migration provenance. |
| `archive/pre_fes_v1_1_notebook07_2026-07-14/` | Controlled Notebook 07 migration | Dated FES v1.0 event models and metadata retained before canonical v1.1 paths were replaced. |
| `archive/pre_2026-07-13_pipeline_rebuild/` | Moved, not produced | Stale pre-rebuild `reports/` artefacts (baseline metrics, model comparisons, SHAP values, per-model statistics summaries) archived rather than deleted during the 2026-07-13 rebuild, since they had no current producer and risked being paired with freshly-trained models. |

## Dependencies

`data/processed/feature_matrix.parquet`, `docs/research_bible/{model_contract.md, feature_contract.md}`.
