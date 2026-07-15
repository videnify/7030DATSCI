# notebooks/

**Purpose:** The numbered pipeline notebooks — each stage reads only what the previous stage wrote. See root `README.md`'s "Notebooks" table for a one-line summary of each, and `docs/00_project_workflow.md` for the full Phase 0–10 mapping.
**Added:** 2026-07-13 (this folder previously had no README). **Updated 2026-07-14** — the Notebook 3 naming question below is resolved.

## Contents

| Notebook | Status |
|----------|--------|
| `01_data_collection.ipynb` | Canonical. Rewritten 2026-07-13 to perform the GDELT full-history backfill. |
| `02_eda.ipynb` | Canonical |
| `03_event_detection.ipynb` | Canonical. **Dataset v1.2 preparation completed 2026-07-14:** the daily aggregation now persists explicit health/labour/other catalogue-occurrence counts, validates them against the 1,005-row catalogue, and saves a verified 739 × 18 `daily_sentiment.parquet`. The pre-rebuild file previously at this name remains archived (below). |
| `04_causal_analysis.ipynb` | Canonical |
| `05_feature_engineering.ipynb` | Canonical. Executed 2026-07-14 against Dataset v1.2; freezes FES v1.1 at 92 features with validation `PASS`. |
| `06_model_training.ipynb` | Canonical. Executed 2026-07-14; freezes `Baseline_LASSO` v1.1 from 27 Market features with full SAP metrics, validation `PASS`, and exact archived FES v1.0 reproduction. |
| `07_model_evaluation.ipynb` | Canonical. Executed and repeat-verified 2026-07-14; freezes the FES v1.1 event-model suite, 92-feature RF importance, held-out SHAP, SAP diagnostics, corrected DM/z comparisons, and hash-bound validation `PASS`. |
| `08_results_visualisation.ipynb` | Canonical. Executed 2026-07-14 against the validated FES v1.1 Notebook 07 boundary; all four publication figures are current, hash-bound, and covered by `reports/figures/results_visualisation_validation.json` (`PASS`). |
| `archive/` | Superseded/duplicate notebooks, gitignored, kept locally for reference only — includes `__01_data_collection__.ipynb` (the original Phase-1 duplicate, archived 2026-07-04), `__03_event_detection__.ipynb` (an earlier Notebook 3 variant, archived 2026-07-13), and `03_event_detection.ipynb` (the pre-rebuild Notebook 3, archived 2026-07-14 when `03_event_detection_revised.ipynb` was promoted to canonical — see `docs/research_bible/10_decision_log.md`). |

## Dependencies

`src/` (reusable helpers, see `src/README.md` for which notebook imports which module), `docs/research_bible/` (governing contracts), `config.yaml`.
