# 15 — Traceability Matrix

**Purpose:** The enforcement mechanism for the project's governing rule — "no notebook, figure, model, or statistical test should exist unless it directly supports RQ1, RQ2, or RQ3." Every pipeline artefact is listed here against the RQ(s) it supports; anything that can't be placed is flagged as orphaned and must be justified in `10_decision_log.md` or removed.
**Owner:** Ibrahim Haroun.
**Dependencies:** `01_research_questions.md`, `08_figures_plan.md`, `05_data_dictionary.md`, `06_feature_dictionary.md`, `07_model_plan.md`.
**Update Frequency:** Update whenever a notebook, figure, table, model, or test is added, removed, or repurposed.
**Relation to Dissertation:** The final check before submission — run through `13_validation_checklist.md`'s traceability gate against this matrix.

---

## Notebooks

| Notebook | RQ1 | RQ2 | RQ3 |
|----------|:---:|:---:|:---:|
| `01_data_collection.ipynb` | ✅ (raw inputs) | ✅ (raw inputs) | ✅ (raw inputs) |
| `02_eda.ipynb` | ✅ | ✅ | — |
| `03_event_detection.ipynb` | ✅ | ✅ | — |
| `04_causal_analysis.ipynb` | ✅ (primary) | ✅ (mean_car feature) | — |
| `05_feature_engineering.ipynb` | — | ✅ (legacy pipeline — superseded by `feature_matrix.parquet`/FES v1.0, produced out-of-band; see `10_decision_log.md` 2026-07-06) | ✅ (legacy) |
| `06_model_training.ipynb` | — | ✅ (legacy — importance/SHAP on legacy feature set) | ✅ (legacy — no baseline split; frozen RQ3 verdict comes from `model_contract.md`/Mission 07, not this notebook) |
| `07_model_evaluation.ipynb` | — | ✅ (legacy — SHAP deep-dive on legacy model) | ✅ (legacy — extended metrics only, no RQ3 verdict stated) |
| `08_results_visualisation.ipynb` | ✅ (08a/08b current) | ✅ (08c legacy) | ✅ (08c/08d legacy — pending regeneration, see `08_figures_plan.md`) |

## Figures (see `08_figures_plan.md` for the full per-figure table)

All 46 figures under `reports/figures/` (40 original + 6 added 2026-07-05 by Mission 05A) trace to at least one RQ per `08_figures_plan.md` — no orphaned figures identified as of 2026-07-05.

## Processed data tables

| File | RQ1 | RQ2 | RQ3 |
|------|:---:|:---:|:---:|
| `car_results.parquet` | ✅ | — | — |
| `causal_estimates.parquet` | ✅ | — | — |
| `events_tagged.parquet` / `high_impact_events.parquet` | ✅ | ✅ (source) | — |
| `daily_sentiment.parquet` | ✅ | ✅ | — |
| `gdelt_daily_risk.parquet` | 🟡 (5-day sample — see `11_limitations.md` L7) | 🟡 | — |
| `model_features.parquet` / `feature_metadata.parquet` | — | ✅ (legacy — superseded, see `10_decision_log.md` 2026-07-05) | ✅ (legacy) |
| `feature_matrix.parquet` / `feature_matrix_validation.json` / `feature_profile.json` | — | ✅ (current — FES v1.0, Mission 05B) | ✅ (current) |
| `model_comparison.parquet` / `evaluation_summary.parquet` (legacy) | — | — | 🟡 Superseded — pre-FES-v1.0 record only, no baseline row; see `reports/model_comparison/` for the current comparison |
| `reports/baseline/baseline_metrics.json` / `baseline_predictions.parquet` / `models/baseline/baseline_lasso.joblib` | — | — | ✅ (current — `Baseline_LASSO` v1.0, Mission 06) |
| `reports/model_comparison/model_comparison.parquet` / `statistical_tests.json` / `feature_importance.parquet` / `shap_values_*.parquet` | — | ✅ | ✅ (current — Mission 07, FES v1.0, RQ3 comparison complete) |
| `shap_values.parquet` (legacy) / `test_predictions.parquet` (legacy) | — | ✅ (superseded) | ✅ (superseded) |

*Row counts for `events_tagged.parquet`/`high_impact_events.parquet` were corrected 2026-07-06 (11,664/4,100) after a live re-execution of `03_event_detection.ipynb` — see `05_data_dictionary.md`, `10_decision_log.md`.*

## Models

| Model | RQ | Notes |
|-------|:---:|-------|
| Event_LASSO (full-feature) | RQ3 | **✅ Retrained 2026-07-05 (Mission 07)** on `feature_matrix.parquet` (FES v1.0) — `LassoCV`, `TimeSeriesSplit(5)`, 11/95 nonzero coefficients. Does not beat `Baseline_LASSO` at Bonferroni-corrected α (DM p=0.056, z-test p=0.662) |
| XGBoost | RQ3 | **✅ Retrained 2026-07-05 (Mission 07)** via `RandomizedSearchCV`/`TimeSeriesSplit(5)` — overfitting reproduces on FES v1.0 (train R² 0.267 → test R² 0.019, `11_limitations.md` L9). Does not beat `Baseline_LASSO` (DM p=0.163, z-test p=0.767) |
| LightGBM | RQ3 | **✅ Retrained 2026-07-05 (Mission 07)** via `RandomizedSearchCV`/`TimeSeriesSplit(5)`. Does not beat `Baseline_LASSO` (DM p=0.161, z-test p=0.839) |
| **`Baseline_LASSO` (market-only)** | RQ3 | **✅ Trained 2026-07-05 (Mission 06)** — `model_contract.md`, `baseline_model_specification.md`, `baseline_evaluation.md`. All 27 Market coefficients shrink to zero at the CV-selected alpha (null finding). Compared against all three event-enhanced models above (Mission 07) — **H0₃ not rejected**. |
| LASSO/XGBoost/LightGBM (legacy, superseded) | RQ3 | Trained on the superseded `model_features.parquet` — retained on disk for historical reference (`09_results_log.md` 2026-07-04 entry) only, no longer the ground truth for RQ3 |
| Random Forest | RQ2 only | Importance-ranking tool, not a trained RQ3 predictive candidate — see `statistical_decision_matrix.md` Part K "Open scope question" and `model_contract.md` "Approved models" (ratified again); **re-run 2026-07-05 on `feature_matrix.parquet`** (Mission 07), replacing legacy `feature_metadata.parquet` values |

## Statistical tests

**Master source of truth as of SAP v1.0 (2026-07-04):** `statistical_decision_matrix.md` — the table below is a status summary only; if it and the decision matrix disagree, the decision matrix is authoritative (per this document's own maintenance rule).

| Test | RQ | Status |
|------|:---:|--------|
| Event-study t-test (per-event CAR) | RQ1 | ✅ Run — `car_results.parquet` |
| CAAR cross-sectional significance | RQ1 | ✅ Run, 🟡 not yet FDR-corrected |
| DoWhy backdoor estimate + refutation tests | RQ1 | ✅ Run |
| ADF / KPSS stationarity checks | RQ1/RQ2 | ✅ Run (2026-07-05, `notebooks/02_eda.ipynb` §9.3, `reports/tables/02_stationarity_tests.csv`) — Mission 05A |
| Correlation threshold check (\|r\|>0.90) | RQ2 | ✅ Run (2026-07-05, `02_eda.ipynb` §9.4) — Mission 05A; 23 pairs flagged, not yet acted on |
| Variance / correlation / VIF threshold checks | RQ2 | ✅ Run (2026-07-05, Mission 05B) — `feature_matrix_validation.json`: 0 near-zero-variance features (train split), 6 pairs flagged \|r\|>0.90, 10 features flagged VIF>10, all reviewed and documented in `06_feature_dictionary.md`, none auto-dropped |
| Random Forest importance ranking | RQ2 | 🟡 Run on legacy `model_features.parquet` (`09_results_log.md`, 2026-07-04) — **not yet re-run on the new `feature_matrix.parquet` (FES v1.0)**; the qualitative finding is expected to replicate but the exact percentages must not be cited against the new file until re-derived |
| Mutual Information corroboration | RQ2 | ⬜ Frozen, not yet run — deferred to the RF-selection pass above |
| SHAP corroboration | RQ2 | ✅ Run |
| Diebold–Mariano / two-proportion z-test (model vs. baseline) | RQ3 | ✅ Run (2026-07-05, Mission 07) — `reports/model_comparison/statistical_tests.json`; none of the three event-enhanced models significant at the corrected threshold |
| Bonferroni correction (3 models vs. baseline) | RQ3 | ✅ Run (2026-07-05, Mission 07) — α = 0.0167; H0₃ not rejected for any of the three models |
| Empirical prediction intervals | RQ3 | ✅ Run (2026-07-05, Mission 07) — 90%/95% PIs for Event_LASSO/XGBoost/LightGBM in `reports/model_comparison/statistical_tests.json` |

## Optional datasets — explicit orphan check

| Dataset | Currently traces to | Status |
|---------|---------------------|--------|
| QQQ, GLD, TLT | **None** — collected, not used in any RQ1–RQ3 result | 🔴 Orphaned as of 2026-07-04 — must be scoped into an analysis or dropped per `10_decision_log.md` / `13_validation_checklist.md` |
| GDELT (full history) | RQ1 (partially, via `gdelt_daily_risk.parquet`) | 🟡 Present but limited to 5-day sample — not a full orphan, but not evidentially final either |

**Governing consequence:** per the project's own rule, QQQ/GLD/TLT should not remain in the repository indefinitely without a defined use — this is the matrix's job to surface, and it is surfaced. Resolve via `10_decision_log.md` before submission.

---

## How to use this matrix

Before adding any new notebook, figure, table, model, or test to the repository, add a row here first (or extend an existing one) and confirm it maps to at least one RQ. If it doesn't, don't build it — or if there's a good reason to build it anyway (e.g. a robustness check that might not pan out), log that reasoning as a decision in `10_decision_log.md` before starting, not after.
