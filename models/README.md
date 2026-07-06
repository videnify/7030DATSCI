# models/

Trained model artefacts (LASSO, XGBoost, LightGBM, Random Forest) and their metadata/diagnostics.

Nothing in this directory is committed to git (binaries — see root `.gitignore`); every file here must be reproducible by re-running the notebook listed as its dependency below.

**Purpose:** persist fitted models so evaluation/explainability notebooks (07, 08) don't need to retrain from scratch.

## Layout

- **`models/baseline/`** — `Baseline_LASSO` (market-only, MCP v1.0), the RQ3 baseline. Contents: `baseline_lasso.joblib`, `baseline_model_metadata.json`. Trained on the Market-category columns of `feature_matrix.parquet` only, per `docs/research_bible/model_contract.md` and `docs/research_bible/feature_contract.md`'s Baseline Eligibility table. Consumed by `notebooks/07_model_evaluation.ipynb` and `notebooks/08_results_visualisation.ipynb`.
- **`models/event/`** — event-enhanced models trained on the full 95-feature `feature_matrix.parquet` (FES v1.0): `event_lasso.joblib`, `lightgbm.joblib`, `xgboost.joblib`, and `random_forest_importance_tool.joblib` (RQ2 importance-ranking tool, not an RQ3 predictive candidate — see `docs/research_bible/15_traceability_matrix.md`). Metadata in `event_model_metadata.json`. Consumed by `notebooks/07_model_evaluation.ipynb` and `notebooks/08_results_visualisation.ipynb`.
- **`models/archive/`** — legacy models trained on the superseded `model_features.parquet` (pre-FES-v1.0): `lasso.pkl`, `xgboost.json` / `xgboost_params.json`, `lightgbm.txt` / `lightgbm_params.json`, `model_metadata.json`, `residual_diagnostics.json`. Retained on disk for historical reference only (`docs/research_bible/09_results_log.md` 2026-07-04 entry) — **not** the ground truth for any current RQ2/RQ3 result. Do not read from this folder in new work; do not delete (kept for audit trail).

## Legacy model policy

A model moves to `models/archive/` when the feature matrix or dataset version it was trained on is superseded (per `docs/research_bible/10_decision_log.md`), never when it simply becomes "old." Archived models are never deleted — they document what produced the historical results still referenced in `09_results_log.md` and the dissertation's methodology narrative. New model artefacts belong in `models/baseline/` or `models/event/` depending on which feature scope produced them; only add a further subfolder (e.g. `models/legacy/` distinct from `archive/`) if a second, functionally different superseded generation appears — don't create one speculatively.

**Input:** `data/processed/feature_matrix.parquet` (current, `baseline/` + `event/`) or `data/processed/model_features.parquet` (legacy, `archive/` only).
**Output:** consumed by `notebooks/07_model_evaluation.ipynb` and `notebooks/08_results_visualisation.ipynb`.
**Dependencies:** `src/models.py`, `notebooks/06_model_training.ipynb`, `docs/research_bible/model_contract.md`, `docs/research_bible/feature_contract.md`.
