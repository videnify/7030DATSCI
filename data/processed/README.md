# data/processed/

**Purpose:** Cleaned, merged, and feature-engineered datasets derived from `data/raw/`. Gitignored — every file here must be reproducible by re-running the numbered notebooks in order.
**Added:** 2026-07-13 (this folder previously had a README, per `DATSCI7030_Repository_Audit_Report.ipynb`, but it went stale and was subsequently lost — this version was written directly against the files actually on disk).

## Contents (verified against disk, 2026-07-13)

| File | Produced by | Notes |
|------|-------------|-------|
| `events_tagged.parquet` | `03_event_detection.ipynb` | Unified event catalogue (FOMC + economically-pre-filtered APP documents only — GDELT deliberately excluded, see `10_decision_log.md` 2026-07-13 Phase 0 decision) |
| `daily_sentiment.parquet` | `03_event_detection.ipynb` | Daily sentiment aggregation from `events_tagged.parquet`, plus a sparse (event-day-only) GDELT merge |
| `high_impact_events.parquet` | `03_event_detection.ipynb` | High-impact subset of `events_tagged.parquet` used for the event study |
| `gdelt_daily_risk.parquet` | `03_event_detection.ipynb` | Standardised GDELT daily signal — full 2015–2025 history (4,018 days) as of 2026-07-13, one row per calendar day (dense, unlike `daily_sentiment.parquet`'s sparse GDELT columns) |
| `car_results.parquet` | `04_causal_analysis.ipynb` | Event-study CAR/CAAR output (264 rows as of the 2026-07-13 rebuild — see `10_decision_log.md` for why this differs from the earlier frozen 1,796-row figure) |
| `causal_estimates.parquet` | `04_causal_analysis.ipynb` | DoWhy backdoor causal effect estimates, overall and per event-type |
| `master_dataset.parquet` | `scripts/build_master_dataset.py` | Frozen base dataset (v1.1, 2026-07-13) — one row per SPY trading day, merging price/VIX/macro/`daily_sentiment.parquet`/`gdelt_daily_risk.parquet`. **Not built by any notebook** — see `docs/research_bible/dataset_contract.md` term 2 for why `05_feature_engineering.ipynb` must not re-derive this merge itself. Governed by `docs/research_bible/dataset_version.md`/`dataset_contract.md`. |
| `feature_matrix.parquet` | `05_feature_engineering.ipynb` | Frozen engineered feature set (FES v1.0, 95 features across Market/Macro & VIX/Sentiment/Event/Temporal/Interaction) built from `master_dataset.parquet` + `car_results.parquet`. Governed by `docs/research_bible/feature_contract.md`. |
| `feature_matrix_validation.json` | `05_feature_engineering.ipynb` | Machine-checkable validation report backing `feature_contract.md` (constant/duplicate columns, variance/correlation/VIF checks) |
| `feature_profile.json` | `05_feature_engineering.ipynb` | Per-feature summary statistics for `feature_matrix.parquet` |

**Not currently in this folder** (documented as a known state, not an error): `model_features.parquet`, `feature_metadata.parquet`, `evaluation_summary.parquet`, `model_comparison.parquet`, `shap_values.parquet`, `test_predictions.parquet` — these were legacy pre-freeze artefacts described in the 2026-07-04 repository audit; the current pipeline's equivalents live under `reports/model_comparison/` and `models/`, not here (see `docs/research_bible/15_traceability_matrix.md`).

## Dependencies

`data/raw/*`, `docs/research_bible/{dataset_contract.md, dataset_version.md, feature_contract.md}` (governing contracts — read before writing to or consuming any file here).
