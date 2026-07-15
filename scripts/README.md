# scripts/

**Purpose:** Standalone helper scripts run outside Jupyter, typically for long or GPU-bound jobs where a notebook kernel would be inconvenient or prone to freezing.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README). **Updated 2026-07-14** for the Dataset v1.2 freeze.

## Contents

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_finbert.py` | Standalone FinBERT sentiment scorer — runs outside the notebook kernel, uses GPU (MPS on Apple Silicon) if available, falls back to CPU. Writes results to `data/processed/events_tagged.parquet`, which `03_event_detection.ipynb` then loads from cache. Predates the 2026-07-13 economic pre-filter — `run_finbert_economic.py` below is the version the current pipeline actually uses. | `python3 scripts/run_finbert.py` from the repository root, with the project virtual environment activated |
| `run_finbert_economic.py` | FinBERT scorer for the current, economic-pre-filtered APP subset (`app_presidential_documents_economic.parquet`, 916 documents) — uses `src/event_detector.py::EventDetector`'s frozen scoring contract (batch size 32, max sequence length 512, min. confidence 0.70). Writes `data/raw/app_finbert_sentiment_cache.parquet`, the primary cache `03_event_detection.ipynb` loads from. | `python3 scripts/run_finbert_economic.py` from the repository root |
| `build_master_dataset.py` | Sole authorised Dataset v1.2 freeze writer. Builds the 2,765 × 34 `master_dataset.parquet`, promotes Notebook 03's three direct category-occurrence counts, validates temporal/missing/leakage/count invariants, and writes the SHA-256-bound `master_dataset_validation.json`. | `python3 scripts/build_master_dataset.py` from the repository root |

## Dependencies

`config.yaml` (NLP parameters), `data/raw/app_presidential_documents_economic.parquet` (FinBERT scripts' input), `docs/research_bible/{dataset_contract.md, dataset_version.md}` (`build_master_dataset.py`'s governing contracts).
