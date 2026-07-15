# 15 — Traceability Matrix

**Purpose:** The enforcement mechanism for the project's governing rule — "no notebook, figure, model, or statistical test should exist unless it directly supports RQ1, RQ2, or RQ3." Every pipeline artefact is listed here against the RQ(s) it supports; anything that can't be placed is flagged as orphaned and must be justified in `10_decision_log.md` or removed.
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `08_figures_plan.md`, `05_data_dictionary.md`, `06_feature_dictionary.md`, `07_model_plan.md`.
**Update Frequency:** Update whenever a notebook, figure, table, model, or test is added, removed, or repurposed.
**Relation to Dissertation:** The final check before submission — run through `13_validation_checklist.md`'s traceability gate against this matrix.
**2026-07-14 note:** The mappings and current FES v1.1 numbers below have been synchronized after the full rerun. `Event_LASSO` collapses to 0/92 nonzero coefficients and exactly matches `Baseline_LASSO`; XGBoost and LightGBM are worse on held-out RMSE and directional accuracy. Historical FES v1.0 rows are explicitly labelled legacy.

**2026-07-14 FES v1.1 gate:** Notebooks 05–08 freeze and validate the 92-feature matrix, `Baseline_LASSO`, event-model suite, Random Forest/SHAP outputs, corrected model comparisons, and all four synthesis figures. `results_visualisation_validation.json` binds the figures to the same current matrix and model-evaluation validations.

**2026-07-15 addition:** `data/processed/causal_overall_estimate.json` (the pooled/overall DoWhy backdoor estimate) is added below as a Notebook 04 output, read directly by Notebook 08. This closes a traceability gap: the pooled estimate previously existed only as printed notebook output and a hand-copied literal in `08_results_visualisation.ipynb`. No RQ1–RQ3 value changed as a result — see `10_decision_log.md`, 2026-07-15 entries.

---

## Notebooks

| Notebook | RQ1 | RQ2 | RQ3 |
|----------|:---:|:---:|:---:|
| `01_data_collection.ipynb` | ✅ (raw inputs) | ✅ (raw inputs) | ✅ (raw inputs) |
| `02_eda.ipynb` | ✅ | ✅ | — |
| `03_event_detection.ipynb` | ✅ | ✅ | — |
| `04_causal_analysis.ipynb` | ✅ (primary) | ✅ (mean_car feature) | — |
| `05_feature_engineering.ipynb` | — | ✅ Current FES v1.1 source (92 features, validation `PASS`) | ✅ Current feature source |
| `06_model_training.ipynb` | — | — | ✅ Current `Baseline_LASSO` v1.1; validation `PASS`; archived FES v1.0 reproduction exact |
| `07_model_evaluation.ipynb` | — | ✅ Current FES v1.1 RF/SHAP; validation `PASS` | ✅ Current event models/tests; validation `PASS` |
| `08_results_visualisation.ipynb` | ✅ Current RQ1 event-study/DoWhy synthesis | ✅ Current FES v1.1 RF/SHAP synthesis; H0 not rejected | ✅ Current four-model comparison/dashboard; H0₃ not rejected |

## Figures (see `08_figures_plan.md` for the full per-figure table)

All 26 PNG figures currently under `reports/figures/` trace to at least one RQ per `08_figures_plan.md`. Figures 08a–08d are additionally hash-bound by `results_visualisation_validation.json`; no orphaned figure is known as of 2026-07-14.

## Processed data tables

| File | RQ1 | RQ2 | RQ3 |
|------|:---:|:---:|:---:|
| `car_results.parquet` | ✅ | — | — |
| `causal_estimates.parquet` | ✅ | — | — |
| `causal_overall_estimate.json` | ✅ (pooled DoWhy estimate; added 2026-07-15) | — | — |
| `events_tagged.parquet` / `high_impact_events.parquet` | ✅ | ✅ (source) | — |
| `daily_sentiment.parquet` | ✅ | ✅ | — |
| `gdelt_daily_risk.parquet` | 🟡 (full 2015–2025 history since 2026-07-13, but not yet feature-engineered — see `11_limitations.md` L7) | 🟡 | — |
| `master_dataset.parquet` / `master_dataset_validation.json` | ✅ (base signals) | ✅ (Dataset v1.2 source boundary) | ✅ (source for current FES v1.1 matrix) |
| `model_features.parquet` / `feature_metadata.parquet` | — | ✅ (legacy — superseded, see `10_decision_log.md` 2026-07-05) | ✅ (legacy) |
| `feature_matrix.parquet` / `feature_matrix_validation.json` / `feature_profile.json` | — | ✅ Current FES v1.1: 92 features, validation `PASS`, hash-bound | ✅ Current feature boundary; baseline and event suite complete |
| `model_comparison.parquet` / `evaluation_summary.parquet` (legacy) | — | — | 🟡 Superseded — pre-FES-v1.0 record only, no baseline row; see `reports/model_comparison/` for the current comparison |
| `reports/baseline/baseline_metrics.json` / `baseline_predictions.parquet` / `baseline_model_validation.json` / `models/baseline/*` | — | — | ✅ Current `Baseline_LASSO` v1.1; hash-bound validation `PASS` |
| `reports/model_comparison/model_comparison.parquet` / `statistical_tests.json` / `event_model_predictions.parquet` / `feature_importance.parquet` / `shap_values_*.parquet` / `shap_importance_summary.parquet` / `model_evaluation_validation.json` | — | ✅ Current FES v1.1 RF/SHAP evidence | ✅ Current FES v1.1 comparison, tests, predictions and validation |
| `shap_values.parquet` (legacy) / `test_predictions.parquet` (legacy) | — | ✅ (superseded) | ✅ (superseded) |

*Historical note: the 2026-07-06 prototype produced 11,664/4,100 rows. The current rebuilt APP + FOMC catalogue contains 1,005 events and 344 high-impact events; the current files and validation evidence supersede that prototype snapshot.*

## Models

| Model | RQ | Notes |
|-------|:---:|-------|
| Event_LASSO (full-feature) | RQ3 | ✅ FES v1.1; 0/92 non-zero; predictions exactly match baseline; does not beat baseline |
| XGBoost | RQ3 | ✅ FES v1.1; test RMSE 0.009656, directional accuracy 0.4893; does not beat baseline |
| LightGBM | RQ3 | ✅ FES v1.1; test RMSE 0.009700, directional accuracy 0.4427; does not beat baseline |
| **`Baseline_LASSO` (market-only)** | RQ3 | ✅ v1.1 frozen on the unchanged 27-feature Market scope; all-zero coefficients; test RMSE 0.009631; validation `PASS` |
| LASSO/XGBoost/LightGBM (legacy, superseded) | RQ3 | Trained on the superseded `model_features.parquet` — retained on disk for historical reference (`09_results_log.md` 2026-07-04 entry) only, no longer the ground truth for RQ3 |
| Random Forest | RQ2 only | ✅ FES v1.1 fixed 500-tree/seed-42 importance tool; complete 92-row ranking (55 >0.001); not an RQ3 candidate |

## Statistical tests

**Master source of truth as of SAP v1.0 (2026-07-04):** `statistical_decision_matrix.md` — the table below is a status summary only; if it and the decision matrix disagree, the decision matrix is authoritative (per this document's own maintenance rule).

| Test | RQ | Status |
|------|:---:|--------|
| Event-study t-test (per-event CAR) | RQ1 | ✅ Run — `car_results.parquet` |
| Event-type mean-CAR significance | RQ1 | ✅ Five tests with 95% CI, Cohen's d and BH-FDR; 0/5 rejected; validation `PASS` |
| DoWhy backdoor estimate + refutation tests | RQ1 | ✅ Run |
| ADF / KPSS stationarity checks | RQ1/RQ2 | ✅ Run (2026-07-05, `notebooks/02_eda.ipynb` §9.3, `reports/tables/02_stationarity_tests.csv`) — Mission 05A |
| Correlation threshold check (\|r\|>0.90) | RQ2 | ✅ Run (2026-07-05, `02_eda.ipynb` §9.4) — Mission 05A; 23 pairs flagged, not yet acted on |
| Variance / correlation / VIF threshold checks | RQ2 | ✅ FES v1.1 `PASS`: three <1e-8 training-variance features removed; 7 high-correlation pairs and 31 VIF>10 features retained as non-blocking flags |
| Random Forest importance ranking | RQ2 | ✅ Current FES v1.1 ranking: macro/VIX but no event feature in top 10; H0 not rejected under frozen descriptive rule |
| Mutual Information corroboration | RQ2 | ⬜ Optional/non-binding; not run. Current corroboration is held-out SHAP, so MI is not a dissertation-completion gate. |
| SHAP corroboration | RQ2 | ✅ Current FES v1.1 held-out output with exact prediction-reconstruction checks |
| Diebold–Mariano / two-proportion z-test (model vs. baseline) | RQ3 | ✅ Current FES v1.1 tests; no candidate clears either improvement leg |
| Bonferroni correction (3 models vs. baseline) | RQ3 | ✅ Applied at α = 0.0167; H0₃ not rejected |
| Empirical prediction intervals | RQ3 | ✅ Current 90%/95% PIs plus seeded block-bootstrap RMSE and Wilson directional-accuracy intervals |

## Optional datasets — explicit orphan check

| Dataset | Currently traces to | Status |
|---------|---------------------|--------|
| QQQ, GLD, TLT | **None** — collected, not used in any RQ1–RQ3 result | 🔴 Orphaned as of 2026-07-04 — must be scoped into an analysis or dropped per `10_decision_log.md` / `13_validation_checklist.md` |
| GDELT (full history) | Pipeline context only (`gdelt_daily_risk.parquet` in `master_dataset.parquet`) | 🟡 Full 2015–2025 history integrated as a candidate continuous control (2026-07-13), but excluded from the frozen DoWhy DAG and FES v1.1. It is not evidence for any current RQ and requires an explicit retention decision before submission. |

**Governing consequence:** per the project's own rule, QQQ/GLD/TLT should not remain in the repository indefinitely without a defined use — this is the matrix's job to surface, and it is surfaced. Resolve via `10_decision_log.md` before submission.

---

## How to use this matrix

Before adding any new notebook, figure, table, model, or test to the repository, add a row here first (or extend an existing one) and confirm it maps to at least one RQ. If it doesn't, don't build it — or if there's a good reason to build it anyway (e.g. a robustness check that might not pan out), log that reasoning as a decision in `10_decision_log.md` before starting, not after.
