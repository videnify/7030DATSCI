# 14 — Project Dashboard

**Purpose:** One-page, at-a-glance snapshot of current project status across phases, research questions, and open risks — the first document to read at the start of any session to re-orient quickly.
**Owner:** Ibrahim Haroun.
**Dependencies:** Synthesises `00_project_overview.md`, `01_research_questions.md`, `11_limitations.md`, `13_validation_checklist.md`, and `DATSCI7030_Repository_Audit_Report.ipynb`.
**Update Frequency:** Update at the end of every working session — this should never be more than one session stale.
**Relation to Dissertation:** Not directly quoted in the dissertation; it's the project-management layer that keeps the Research Bible internally consistent.

---

## Mission status (Mission Control v2.0)

| Mission | Objective | Status |
|---------|-----------|:---:|
| 01 — Repository Governance | Clean repo, gitignore, README, workflow, audit | ✅ Complete |
| 02 — Research Bible | 16-document Research Bible | ✅ Complete |
| 03 — Freeze Dataset v1.0 | `master_dataset.parquet` frozen, validated, documented | ✅ Complete — 🟡 pending Project Director approval |
| 04 — Statistical Design Freeze | Freeze α, metrics, assumptions, test matrix | ✅ Complete (2026-07-04) — SAP v1.0 frozen across `statistical_analysis_plan.md` + 4 companion docs |
| 05A — Statistical Implementation (EDA) | Implement SAP v1.0 descriptive/time-series/correlation analysis on `master_dataset.parquet` | ✅ Complete (2026-07-05) — `notebooks/02_eda.ipynb` §9, `reports/tables/02_*.csv`, `reports/figures/02m`–`02r` |
| 05B — Feature Matrix v1.0 | Freeze `feature_matrix.parquet` (FES v1.0) from `master_dataset.parquet` + `car_results.parquet` under `feature_contract.md`, applying variance/correlation/VIF thresholds ahead of RF selection | ✅ Complete (2026-07-05) — 95 features, 2,511 rows, validation PASS; see `feature_contract.md`, `06_feature_dictionary.md` |
| 06 — Baseline Model | RQ3 market-only baseline (`Baseline_LASSO`) + Model Contract Protocol (MCP v1.0) | ✅ Complete (2026-07-05) — all 27 Market coefficients shrink to zero (null finding); see `model_contract.md`, `baseline_evaluation.md` |
| 07 — Event-Enhanced Models | Retrain LASSO/XGBoost/LightGBM on `feature_matrix.parquet` (FES v1.0); compare vs. Mission 06 baseline via DM/two-proportion z-test | ✅ Complete (2026-07-05) — H0₃ not rejected; see `reports/statistics/07_event_models_summary.md`, `10_decision_log.md` |
| 08 — Explainability | Deeper SHAP dependence/interaction analysis, PDP | ⬜ Waiting (depends on 07 ✅ — now unblocked; SHAP values already computed, Mission 08 extends the analysis) |
| 09 — Dissertation Synchronisation | Sync figures/tables/results/methods | ⬜ Waiting |

## Snapshot as of 2026-07-04

### Phase status

| Phase | Status |
|-------|:---:|
| 1 — Data Collection | ✅ |
| 2 — EDA | ✅ |
| 3 — Event Detection & NLP | ✅ |
| 4 — Causal Analysis (Event Study) | ✅ |
| 5 — Feature Engineering | ✅ |
| 6 — Model Training | ✅ |
| 7 — Model Evaluation | ✅ |
| 8 — Results Visualisation | ✅ |
| Dissertation Writing | 🟡 In progress |

### Research question status

| RQ | Status | Blocking item |
|----|:---:|----------------|
| RQ1 — Abnormal returns | ✅ Answered (provisional — pending FDR correction, `11_limitations.md` L3) | None blocking; correction is a quick statistical follow-up |
| RQ2 — Feature importance | ✅ Answered — RF importance re-run on `feature_matrix.parquet` (FES v1.0, Mission 07), replacing legacy values | Mutual Information corroboration still not run — non-blocking |
| RQ3 — ML vs. baseline | ✅ Answered — **H0₃ not rejected** (2026-07-05, Mission 07) | None blocking; see `07_model_plan.md`, `reports/statistics/07_event_models_summary.md` |

### Top 3 risks right now

1. **🟠 XGBoost overfitting remains uninvestigated at the root-cause level** — reproduced on the FES v1.0 retrain (train R² 0.267 → test R² 0.019), confirming it isn't a superseded-feature-set artefact (`11_limitations.md` L9, `07_model_plan.md`).
2. **🔴 Zero git commits + a nested git repository** discovered at `7030DATSCI/.git` — must be resolved before the first commit (`DATSCI7030_Repository_Audit_Report.ipynb` §3, §10b).
3. **🟠 Unrotated API credentials** in `config.yaml` / `notebooks/.env` — gitignored (no commit risk) but not yet rotated.

### What's genuinely solid right now

- Full pipeline (Phases 1–8) runs end-to-end and produces consistent, cross-checked outputs (`05_data_dictionary.md` row-count sanity checks all pass).
- RQ1 and RQ2 have real, defensible, well-documented evidence (`09_results_log.md`).
- Statistical methodology is planned in detail (`04_statistics_plan.md`), including the multiple-comparisons corrections not yet applied — the plan exists even where execution is pending.
- The Research Bible itself (this folder) is now complete as a documentation layer (2026-07-04).
- SAP v1.0's EDA-stage tests (ADF/KPSS, descriptive stats, Pearson/Spearman correlation, correlation-threshold flagging) are now actually implemented and run against the frozen `master_dataset.parquet`, not just specified (`09_results_log.md`, 2026-07-05).
- `feature_matrix.parquet` (FES v1.0) is frozen, validated (PASS), and fully documented — the market-only baseline's feature scope is now contractually enforced (`feature_contract.md`), removing the single largest remaining ambiguity blocking Mission 06.
- All three RQs now have a complete, evidence-based answer (2026-07-05) — RQ1 (provisional pending FDR correction), RQ2 (RF importance + SHAP re-run on FES v1.0), RQ3 (H0₃ not rejected, full DM/z-test comparison against a genuinely-tuned baseline). The project's core empirical work is done; remaining work is explainability depth (Mission 08), dissertation writing, and repository hygiene.

### Immediate next action

**Mission 08 — Explainability:** extend the SHAP analysis already computed in Mission 07 (`reports/model_comparison/shap_values_*.parquet`) with dependence/interaction plots and partial dependence, per `docs/00_project_workflow.md`'s Phase 8 scope. All three RQs now have a complete, evidence-based answer — Mission 08 deepens the RQ2/RQ3 explainability narrative rather than closing a blocking gap.

**Mission 07 — Event-Enhanced Models (complete, 2026-07-05):** Event_LASSO, XGBoost, and LightGBM retrained on the full 95-feature `feature_matrix.parquet` (FES v1.0), identical split/`TimeSeriesSplit(5)`/seed 42/scaling to `Baseline_LASSO`. Compared via the frozen Diebold-Mariano + two-proportion z-test + Bonferroni protocol (`statistical_decision_matrix.md` Part K) — **none of the three clears the corrected threshold on either leg; H0₃ is not rejected.** RF importance and SHAP re-run on the new matrix, replacing all legacy `model_features.parquet`-derived values. Full detail: `reports/statistics/07_event_models_summary.md`, `10_decision_log.md`.

**Mission 06 — Baseline Model (complete, 2026-07-05):** `Baseline_LASSO` (27 Market-category features, `TimeSeriesSplit(5)`, seed 42) is trained and frozen — see `model_contract.md` (MCP v1.0), `baseline_model_specification.md`, `baseline_evaluation.md`. Headline result: at the cross-validated alpha, all 27 coefficients shrink to zero — the baseline reduces to a mean predictor, a legitimate null finding consistent with weak-form market efficiency. Not yet joined to `model_comparison.parquet` or compared against event-enhanced models — that is Mission 07.

**Mission 05B — Feature Matrix v1.0 (complete, 2026-07-05):** `feature_matrix.parquet` (95 features, 2,511 rows, validation PASS) is frozen and documented in `feature_contract.md`/`06_feature_dictionary.md`/`feature_profile.json`. Built from `master_dataset.parquet` + `car_results.parquet` (the latter approved as a second input, `10_decision_log.md`). RF-importance selection against this new matrix (re-running the 0.001-threshold pass that produced the legacy RQ2 result) and Mutual Information corroboration are not yet run — both remain open, non-blocking items tracked in `15_traceability_matrix.md`.

---

## Dashboard maintenance rule

If this document and any other Research Bible document disagree on status, the more granular document (e.g. `01_research_questions.md` for RQ status, `13_validation_checklist.md` for a specific checklist item) is authoritative — update this dashboard to match, not the other way around.
