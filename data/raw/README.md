# data/raw/

**Purpose:** Untouched (or minimally normalised) source data, pulled directly from external APIs/exports. Gitignored — every file here must be reproducible by re-running `01_data_collection.ipynb`.
**Added:** 2026-07-13 (this folder previously had a README, per `DATSCI7030_Repository_Audit_Report.ipynb`, but it went stale and was subsequently lost — this version was written directly against the files actually on disk, not carried forward from memory).

## Contents (verified against disk and `01_data_collection.ipynb`'s own `save_table()` calls, 2026-07-13)

| File | Produced by | Notes |
|------|-------------|-------|
| `spy_ohlcv.parquet` | `01_data_collection.ipynb` (yfinance) | Full SPY OHLCV — used for event-study windows and `scripts/build_master_dataset.py`'s adjusted-price basis. Supersedes the older `prices.parquet` name still referenced in a few Research Bible documents (`05_data_dictionary.md`, `dataset_version.md`) — that file no longer exists on disk. |
| `spy_returns.parquet` | `01_data_collection.ipynb` (yfinance) | SPY daily returns, derived alongside OHLCV |
| `vix.parquet` | `01_data_collection.ipynb` (yfinance, `^VIX`) | `vix_close`/`vix_change`/`vix_high_regime` (schema corrected 2026-07-06, see `05_data_dictionary.md`) |
| `macro_indicators.parquet` | `01_data_collection.ipynb` (FRED API) | Fed funds rate, CPI, unemployment, treasury yields, `yield_spread` |
| `fomc_dates.parquet` | `01_data_collection.ipynb` (Federal Reserve, manual) | `rate_decision`/`is_emergency`/`event_importance` schema (corrected 2026-07-06) |
| `app_presidential_documents_raw.parquet` | `01_data_collection.ipynb` (American Presidency Project) | Full unfiltered APP scrape |
| `app_presidential_documents_economic.parquet` | `01_data_collection.ipynb` (economic pre-filter over the raw scrape) | **The file `03_event_detection.ipynb` actually reads** (916 documents) — not the plain `app_presidential_documents.parquet` name several Research Bible documents still use; that exact filename does not exist on disk. Also the input to `scripts/run_finbert_economic.py`. |
| `app_finbert_sentiment_cache.parquet` | `scripts/run_finbert_economic.py` | FinBERT sentiment scores for `app_presidential_documents_economic.parquet`'s document titles — the official primary sentiment cache (Sentiment Engine Freeze v1.0) |
| `gdelt_daily_summary.parquet` | `01_data_collection.ipynb` (GDELT 2.0, chunked bulk ingestion) | **Full 2015–2025 daily history (4,018 days) as of 2026-07-13**, replacing the earlier 5-day proof-of-concept sample (`gdelt_sample.parquet`, no longer on disk). Schema: `date, gdelt_event_count, gdelt_mean_goldstein, gdelt_mean_tone`. See `docs/research_bible/10_decision_log.md` (2026-07-13) for the integration design. |
| `daily_modelling_calendar_v1.parquet` | `01_data_collection.ipynb` | Canonical daily trading-calendar scaffold used to align the above sources onto one date index |
| `data_quality_report.parquet` | `01_data_collection.ipynb` | Notebook 01's own self-check output (row counts, null counts, date-range checks per source) |
| `app_csv/` (folder, ~120 files) | American Presidency Project scraper | Raw per-page scrape cache prior to consolidation into `app_presidential_documents_raw.parquet` — not a second copy of the same data |

**A naming-drift finding from this pass (2026-07-13, not fixed here):** `prices.parquet` and `app_presidential_documents.parquet` are referenced by name in several Research Bible documents (`05_data_dictionary.md`, `dataset_version.md`, and others) but neither file exists on disk under those names — the actual current files are `spy_ohlcv.parquet`/`spy_returns.parquet` and `app_presidential_documents_raw.parquet`/`app_presidential_documents_economic.parquet` respectively. This predates the 2026-07-13 rebuild (Notebook 01 was rewritten with these new names at some point) and is a separate, wider documentation sweep than this pass covers — flagged in `docs/research_bible/14_project_dashboard.md`'s 2026-07-13 update section.

## Dependencies

`config.yaml` (API keys, tickers), `src/data_collector.py` (`MarketDataCollector`, `APPCollector`, `GDELTCollector`).
