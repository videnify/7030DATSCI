# data/

**Purpose:** All data, at every pipeline stage. Gitignored in full (contents, not the folders themselves) — every file must be reproducible by re-running the numbered notebooks in order from `data/raw/` onward. See `docs/research_bible/dataset_contract.md` / `dataset_version.md` for the frozen `master_dataset.parquet` specifically.
**Added:** 2026-07-13 (this folder previously had no top-level README; its subfolders each have their own).

## Contents

| Subfolder | Purpose |
|-----------|---------|
| `raw/` | Untouched source data pulled directly from external APIs — see `raw/README.md` |
| `interim/` | Intermediate cleaning artefacts — see `interim/README.md` |
| `processed/` | Cleaned, merged, feature-engineered datasets — see `processed/README.md` |
| `external/` | Reference data (event calendars, macro indicators) — see `external/README.md` |
| `fred_client.py` | Standalone FRED API client helper, sits at this level rather than in `src/` |

## Dependencies

`config.yaml` (API keys), `01_data_collection.ipynb` onward.
