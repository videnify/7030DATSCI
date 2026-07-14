# notebooks/

**Purpose:** The numbered pipeline notebooks — each stage reads only what the previous stage wrote. See root `README.md`'s "Notebooks" table for a one-line summary of each, and `docs/00_project_workflow.md` for the full Phase 0–10 mapping.
**Added:** 2026-07-13 (this folder previously had no README). **Updated 2026-07-14** — the Notebook 3 naming question below is resolved.

## Contents

| Notebook | Status |
|----------|--------|
| `01_data_collection.ipynb` | Canonical. Rewritten 2026-07-13 to perform the GDELT full-history backfill. |
| `02_eda.ipynb` | Canonical |
| `03_event_detection.ipynb` | Canonical. **Resolved 2026-07-14:** this is the file built as `03_event_detection_revised.ipynb` during the rebuild — confirmed as the one `src/event_detector.py` is actually imported by, and the one carrying this session's GDELT-integration/interpretation-cell work. The pre-rebuild file previously at this name was archived (below). |
| `04_causal_analysis.ipynb` | Canonical |
| `05_feature_engineering.ipynb` | Canonical |
| `06_model_training.ipynb` | Canonical |
| `07_model_evaluation.ipynb` | Canonical |
| `08_results_visualisation.ipynb` | Canonical |
| `archive/` | Superseded/duplicate notebooks, gitignored, kept locally for reference only — includes `__01_data_collection__.ipynb` (the original Phase-1 duplicate, archived 2026-07-04), `__03_event_detection__.ipynb` (an earlier Notebook 3 variant, archived 2026-07-13), and `03_event_detection.ipynb` (the pre-rebuild Notebook 3, archived 2026-07-14 when `03_event_detection_revised.ipynb` was promoted to canonical — see `docs/research_bible/10_decision_log.md`). |

## Dependencies

`src/` (reusable helpers, see `src/README.md` for which notebook imports which module), `docs/research_bible/` (governing contracts), `config.yaml`.
