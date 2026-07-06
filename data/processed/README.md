# data/processed/

**Updated 2026-07-06** — corrected to match what is actually on disk; the previous version of this file described `features.parquet`/`target.parquet`, filenames that were never produced by this pipeline.

Cleaned, merged, and feature-engineered data. Current (frozen) files are listed first; legacy files retained for historical reference are listed separately below.

## Current (frozen, canonical)

| File | Description | Notebook |
|------|-------------|----------|
| `events_tagged.parquet` | Unified event catalogue — rule-based event type + FinBERT sentiment (SEF v1.0) | `03_event_detection.ipynb` |
| `daily_sentiment.parquet` | Daily aggregated sentiment by event type | `03_event_detection.ipynb` |
| `high_impact_events.parquet` | High-impact event subset used in the event study | `03_event_detection.ipynb` |
| `gdelt_daily_risk.parquet` | GDELT daily geopolitical risk scores (5-day proof-of-concept sample only) | `03_event_detection.ipynb` |
| `car_results.parquet` | Event-level cumulative abnormal returns (CAR), event study | `04_causal_analysis.ipynb` |
| `causal_estimates.parquet` | DoWhy backdoor causal-effect estimates per event type | `04_causal_analysis.ipynb` |
| `master_dataset.parquet` | Dataset v1.0 — merged market/macro/sentiment daily table (`dataset_contract.md`) | upstream of `05_feature_engineering.ipynb` |
| `master_dataset_validation.json` | Validation report for `master_dataset.parquet` | — |
| `feature_matrix.parquet` | FES v1.0 — 95 engineered features across 6 categories, 2,511 rows (`feature_contract.md`) | `05_feature_engineering.ipynb` |
| `feature_profile.json` | Per-feature scaling parameters (train-split-only mean/std) and category membership for `feature_matrix.parquet` | `05_feature_engineering.ipynb` |
| `feature_matrix_validation.json` | Validation report (variance/correlation/VIF checks) for `feature_matrix.parquet` | `05_feature_engineering.ipynb` |

Baseline and event-enhanced model outputs (predictions, metrics, statistical tests) live under `reports/baseline/` and `reports/model_comparison/`, not here — see those folders' contents and `docs/research_bible/model_contract.md`.

## Legacy (superseded, retained for historical reference only — do not read in new work)

| File | Superseded by |
|------|---------------|
| `model_features.parquet` | `feature_matrix.parquet` (FES v1.0) |
| `feature_metadata.parquet` | `feature_profile.json` / `reports/model_comparison/feature_importance.parquet` |
| `model_comparison.parquet` | `reports/model_comparison/model_comparison.parquet` |
| `evaluation_summary.parquet` | `reports/model_comparison/statistical_tests.json` |
| `test_predictions.parquet` | `reports/baseline/baseline_predictions.parquet` / `reports/model_comparison/event_model_predictions.parquet` |
| `shap_values.parquet` | `reports/model_comparison/shap_values_*.parquet` |

See `docs/research_bible/10_decision_log.md` and `15_traceability_matrix.md` for when and why each legacy file was superseded.
