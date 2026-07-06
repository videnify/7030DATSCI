# scripts/

**Purpose:** Standalone helper scripts run outside Jupyter, typically for long or GPU-bound jobs where a notebook kernel would be inconvenient or prone to freezing.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README).

## Contents

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_finbert.py` | Standalone FinBERT sentiment scorer — runs outside the notebook kernel, uses GPU (MPS on Apple Silicon) if available, falls back to CPU. Writes results to `data/processed/events_tagged.parquet`, which `03_event_detection.ipynb` then loads from cache. | `python3 scripts/run_finbert.py` from the repository root, with the project virtual environment activated |

## Dependencies

`config.yaml` (NLP parameters), `data/raw/app_presidential_documents_economic.parquet` (input), writes to `data/processed/events_tagged.parquet` (consumed by `03_event_detection.ipynb`).
