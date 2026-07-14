# scripts/

**Purpose:** Standalone helper scripts run outside Jupyter, typically for long or GPU-bound jobs where a notebook kernel would be inconvenient or prone to freezing.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README). **Updated 2026-07-13** — two scripts added this session were missing from this table entirely.

## Contents

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_finbert.py` | Standalone FinBERT sentiment scorer — runs outside the notebook kernel, uses GPU (MPS on Apple Silicon) if available, falls back to CPU. Writes results to `data/processed/events_tagged.parquet`, which `03_event_detection.ipynb` then loads from cache. Predates the 2026-07-13 economic pre-filter — `run_finbert_economic.py` below is the version the current pipeline actually uses. | `python3 scripts/run_finbert.py` from the repository root, with the project virtual environment activated |
| `run_finbert_economic.py` | FinBERT scorer for the current, economic-pre-filtered APP subset (`app_presidential_documents_economic.parquet`, 916 documents) — uses `src/event_detector.py::EventDetector`'s frozen scoring contract (batch size 32, max sequence length 512, min. confidence 0.70). Writes `data/raw/app_finbert_sentiment_cache.parquet`, the primary cache `03_event_detection.ipynb` loads from. | `python3 scripts/run_finbert_economic.py` from the repository root |
| `build_master_dataset.py` | Rebuilds `data/processed/master_dataset.parquet` (frozen v1.1, 2026-07-13) from `data/raw/{spy_ohlcv,vix,macro_indicators}.parquet` + `data/processed/{daily_sentiment,gdelt_daily_risk}.parquet`. Exists as a dedicated script — not a notebook cell — because `docs/research_bible/dataset_contract.md` term 2 prohibits `05_feature_engineering.ipynb` from re-deriving this merge itself. See `docs/research_bible/10_decision_log.md` (2026-07-13) for why this became necessary (the file had no producer anywhere in the repository). | `python3 scripts/build_master_dataset.py` from the repository root |

## Dependencies

`config.yaml` (NLP parameters), `data/raw/app_presidential_documents_economic.parquet` (FinBERT scripts' input), `docs/research_bible/{dataset_contract.md, dataset_version.md}` (`build_master_dataset.py`'s governing contracts).
