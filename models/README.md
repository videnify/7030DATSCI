# models/

Trained model artefacts (LASSO, XGBoost, LightGBM) and their metadata/diagnostics.

Nothing in this directory is committed to git (binaries — see root `.gitignore`); every file here must be reproducible by re-running `notebooks/06_model_training.ipynb`.

**Purpose:** persist fitted models so evaluation/explainability notebooks (07, 08) don't need to retrain from scratch.
**Contents:** `lasso.pkl`, `xgboost.json`, `xgboost_params.json`, `lightgbm.txt`, `lightgbm_params.json`, `model_metadata.json`, `residual_diagnostics.json`.
**Input:** `data/processed/model_features.parquet`.
**Output:** consumed by `notebooks/07_model_evaluation.ipynb` and `notebooks/08_results_visualisation.ipynb`.
**Dependencies:** `src/models.py`, `notebooks/06_model_training.ipynb`.

Layout is intentionally flat (no `trained/`/`saved/` split) — three models is not enough to justify subfolders yet. Revisit if the model set grows.
