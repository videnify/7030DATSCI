# data/external/

**Updated 2026-07-06** — this folder is currently **empty** (only `.gitkeep`) in the frozen pipeline. The previous version of this README described `sp500_constituents.csv`, `fomc_dates.csv`, `earnings_calendar.csv`, and `macro_events.csv` — none of these were ever actually collected; they were an early scaffolding placeholder from before the project's scope was narrowed to RQ1–RQ3 (`docs/research_bible/00_project_overview.md` "Scope discipline").

The project does not use single-company-constituent, earnings-calendar, or manually curated macro-event data anywhere in the frozen pipeline: FOMC dates are compiled directly in `01_data_collection.ipynb` and saved to `data/raw/fomc_dates.parquet`, and all macro series come from the FRED API (`data/raw/macro_indicators.parquet`). If a genuinely external, non-API reference file is needed in a future iteration, it belongs here — until then, this folder is reserved but unused.
