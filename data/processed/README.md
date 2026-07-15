# data/processed/

**Purpose:** Cleaned, merged, and feature-engineered datasets derived from `data/raw/`. Gitignored — every file here must be reproducible by re-running the numbered notebooks in order.
**Added:** 2026-07-13 (this folder previously had a README, per `DATSCI7030_Repository_Audit_Report.ipynb`, but it went stale and was subsequently lost — this version was written directly against the files actually on disk).

## Contents (Notebook 03 outputs re-verified against disk, 2026-07-14)

| File | Produced by | Notes |
|------|-------------|-------|
| `events_tagged.parquet` | `03_event_detection.ipynb` | Unified event catalogue (FOMC + economically-pre-filtered APP documents only — GDELT deliberately excluded, see `10_decision_log.md` 2026-07-13 Phase 0 decision) |
| `daily_sentiment.parquet` | `03_event_detection.ipynb` | 739 × 18 daily sentiment-and-occurrence table. Dataset v1.2 preparation adds `n_health_catalogue_events`, `n_labour_catalogue_events`, and `n_other_catalogue_events`; their verified totals (14/103/427) reconcile exactly to `events_tagged.parquet`. Also includes a sparse (event-day-only) GDELT merge. |
| `high_impact_events.parquet` | `03_event_detection.ipynb` | High-impact subset of `events_tagged.parquet` used for the event study |
| `gdelt_daily_risk.parquet` | `03_event_detection.ipynb` | Standardised GDELT daily signal — full 2015–2025 history (4,018 days) as of 2026-07-13, one row per calendar day (dense, unlike `daily_sentiment.parquet`'s sparse GDELT columns) |
| `car_results.parquet` | `04_causal_analysis.ipynb` | Event-study CAR/CAAR output (264 rows as of the 2026-07-13 rebuild — see `10_decision_log.md` for why this differs from the earlier frozen 1,796-row figure) |
| `event_type_statistics.parquet` | `04_causal_analysis.ipynb` | **RQ1-v1.0:** five event-type mean-CAR tests with 95% t intervals, raw p-values, BH-FDR q-values, Wilcoxon robustness p-values and Cohen's d. No BH rejection; minimum q=0.5810. |
| `rq1_reporting_validation.json` | `04_causal_analysis.ipynb` | Hash-bound `PASS` record for the five-test correction, confidence intervals and effect-size table; binds CAR, RQ1 statistics and causal-estimate artefacts. |
| `causal_estimates.parquet` | `04_causal_analysis.ipynb` | DoWhy backdoor causal effect estimates, overall and per event-type |
| `master_dataset.parquet` | `scripts/build_master_dataset.py` | **Dataset v1.2 frozen 2026-07-14:** 2,765 SPY trading days × 34 columns. Adds only the three explicit occurrence counts; every v1.1 column is unchanged value-for-value. **Not built by any notebook** — see `dataset_contract.md` term 2. |
| `master_dataset_validation.json` | `scripts/build_master_dataset.py` | Dataset v1.2 `PASS` report with schema, split/leakage/missing/count checks, source/output SHA-256 hashes, and explicit non-trading-date occurrence disclosure. |
| `feature_matrix.parquet` | `05_feature_engineering.ipynb` | **FES v1.1 frozen 2026-07-14:** 2,477 rows × 95 columns (date, split, 92 features, target). Category counts are Market 27 / Macro & VIX 16 / Sentiment 23 / Event 14 / Temporal 5 / Interaction 7. Built from Dataset v1.2 plus `car_results.parquet`; SHA-256 `127a6dbe4b83e59c873dfdf7502060aab115037732bbb723f9d489c6b85dc383`. |
| `feature_matrix_validation.json` | `05_feature_engineering.ipynb` | FES v1.1 machine-checkable `PASS`: no duplicate, missing, constant, near-zero-training-variance, leakage, or occurrence-source failures. Seven high-correlation pairs and 31 VIF>10 features remain documented, non-blocking interpretability flags. |
| `feature_profile.json` | `05_feature_engineering.ipynb` | FES v1.1 category membership, train-split scaling statistics, input hashes, and output hash for all 92 features. |

**Not currently in this folder** (documented as a known state, not an error): `model_features.parquet`, `feature_metadata.parquet`, `evaluation_summary.parquet`, `model_comparison.parquet`, `shap_values.parquet`, `test_predictions.parquet` — these were legacy pre-freeze artefacts described in the 2026-07-04 repository audit; the current pipeline's equivalents live under `reports/model_comparison/` and `models/`, not here (see `docs/research_bible/15_traceability_matrix.md`).

The former FES v1.0 `feature_matrix_validation_disposition.json` is no longer a current artefact. It and the exact superseded matrix/profile/validation files are retained under `archive/pre_fes_v1_1_2026-07-14/`; FES v1.1 requires and has an unconditional validation `PASS`.

## Dependencies

`data/raw/*`, `docs/research_bible/{dataset_contract.md, dataset_version.md, feature_contract.md}` (governing contracts — read before writing to or consuming any file here).
