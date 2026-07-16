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

## Execution order and I/O summary

Notebooks must be read (and, if ever re-run, executed) strictly in numeric order — each stage's outputs are the next stage's inputs. See `docs/architecture/data_lineage.svg` for the full file-level lineage diagram.

| # | Notebook | Major inputs | Major outputs |
|---|---|---|---|
| 01 | Data collection | External APIs/downloads (yfinance, FRED, APP, FOMC, GDELT) | `data/raw/*.parquet` |
| 02 | EDA | `data/raw/*.parquet` | `reports/figures/02*.png`, `reports/tables/02_*.csv` |
| 03 | Event detection & sentiment | `data/raw/app_*`, FOMC dates | `data/processed/events_tagged.parquet`, `data/processed/daily_sentiment.parquet` |
| 04 | Causal analysis (event study + DoWhy) | `data/processed/master_dataset.parquet` | `data/processed/car_results.parquet`, `causal_estimates.parquet`, `causal_overall_estimate.json` |
| 05 | Feature engineering | `master_dataset.parquet`, `car_results.parquet` | `data/processed/feature_matrix.parquet` (FES v1.1) |
| 06 | Baseline model | `feature_matrix.parquet` | `models/baseline/baseline_lasso.joblib`, `reports/baseline/*` |
| 07 | Model evaluation | `feature_matrix.parquet`, baseline model | `models/event/*.joblib`, `reports/model_comparison/*` |
| 08 | Results visualisation | All prior validated outputs | `reports/figures/08a–08d_*.png` |

## Frozen-snapshot behaviour

All eight notebooks are **executed and frozen** — their saved cell outputs, execution counts, and metadata are the evidential record cited by the dissertation and must not be cleared, stripped, or re-run as part of routine maintenance. Re-running a notebook is a scientific action requiring a new dated `docs/research_bible/10_decision_log.md` entry, not a housekeeping step. See `docs/research_bible/00_project_freeze.md` and `docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md`.

## External-data warning

Notebook 01 fetches from live external APIs/services (yfinance, FRED, GDELT, etc.). Re-running it from scratch will hit those live services, may return different data than the frozen 2015–2025 snapshot (new trading days, revised macro releases, service changes/outages), and is **not required** to reproduce any reported result — every downstream notebook reads only the already-frozen `data/raw/` / `data/processed/` parquet files. Do not re-run Notebook 01 to "refresh" data as part of this repository's normal use.

## Expected environment

See `docs/research_bible/ENVIRONMENT_2026-07-16.md` for the full pinned environment, install command, and known-unsupported configurations. In short: Python (see that file for the exact validated version), dependencies from `requirements.txt`, `jupyter`/`nbclient` to open or (exceptionally) re-execute a notebook.

## Current validation status (as of 2026-07-16)

All eight notebooks executed cleanly (zero saved errors, monotonic execution counts) as of their last recorded run (see per-notebook dates above and `docs/research_bible/10_decision_log.md`'s 2026-07-14/2026-07-15 entries for the most recent live-execution verification). Downstream validation JSON files (`data/processed/*_validation.json`, `reports/*/​*_validation.json`) all report `PASS`. No notebook has been re-run since the repository was frozen on 2026-07-16 — see `docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md`.
