# src/

**Purpose:** Reusable Python modules imported by the numbered notebooks. Notebooks own the pipeline narrative (what runs, in what order, with what interpretation); modules here own the reusable logic so it isn't duplicated across notebooks.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README). **Updated 2026-07-13** (verified against actual current notebook imports, not assumed from the module list); **updated again 2026-07-14** (Notebook 3 naming resolved).

## Contents

| Module | Purpose | Used by |
|--------|---------|---------|
| `data_collector.py` | Market price (yfinance), presidential document (APP), macro (FRED), and — since the 2026-07-13 GDELT full-history backfill — global geopolitical event data (`GDELTCollector`, chunked bulk ingestion) collection helpers | `01_data_collection.ipynb` |
| `event_detector.py` | Event-type classification and sentiment scoring helpers (FinBERT — official primary engine, Sentiment Engine Freeze v1.0) | `03_event_detection.ipynb` — this is the file built as `03_event_detection_revised.ipynb` during the rebuild and promoted to canonical 2026-07-14, confirmed via import grep as the only Notebook 3 candidate this module actually feeds. See `docs/research_bible/10_decision_log.md`. |
| `causal_engine.py` | Event study (abnormal return / CAR) and DoWhy causal-graph estimation helpers | **Corrected 2026-07-13** — not actually imported by any current notebook. `04_causal_analysis.ipynb` implements its own inline `EventStudy` class rather than importing this module (confirmed via grep — no `from src.causal_engine import` anywhere in that notebook); the archived pre-rebuild Notebook 3 only mentioned the class in prose. Same "historically used, now inline in-notebook" pattern as `features.py`/`models.py`/`evaluation.py` below — this was previously mis-stated as an active dependency. |
| `features.py` | Feature engineering helpers | historically used by the pre-freeze feature pipeline; `05_feature_engineering.ipynb` now builds `feature_matrix.parquet` directly per `docs/research_bible/feature_contract.md` rather than calling this module — see that notebook for the current, authoritative feature-construction code |
| `models.py` | Model training/tuning/persistence helpers | historically used by the pre-freeze model pipeline; `06_model_training.ipynb`/`07_model_evaluation.ipynb` now train `Baseline_LASSO`/Event_LASSO/XGBoost/LightGBM directly per `docs/research_bible/model_contract.md` — see those notebooks for the current, authoritative training code |
| `evaluation.py` | Model evaluation, SHAP explainability, visualisation helpers | historically used by the pre-freeze evaluation pipeline; current SHAP/metric code lives directly in `07_model_evaluation.ipynb`/`08_results_visualisation.ipynb` |

**Note (2026-07-06):** `features.py`, `models.py`, and `evaluation.py`'s docstrings describe the module-level capability as originally designed; the frozen, contract-governed pipeline (FES v1.0, MCP v1.0) is implemented directly in the notebooks listed above, which are the authoritative source for any current RQ2/RQ3 result. This mirrors the same "notebook is authoritative, module docstring may predate the freeze" relationship already documented for `03_methodology.md` in `docs/research_bible/10_decision_log.md`. No source code was changed as part of this documentation pass — this note exists so a reader importing from `src/` doesn't assume module behaviour matches the frozen contracts without checking. **As of 2026-07-13, `causal_engine.py` belongs in this same category** — the table above previously implied otherwise.

## Dependencies

`config.yaml` (parameters), `docs/research_bible/` (governing contracts for any current use).
