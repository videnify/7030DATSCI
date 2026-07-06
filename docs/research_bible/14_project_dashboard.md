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
| 07A — Event_LASSO (RQ3 Experiment 1) | Isolated re-run of Event_LASSO only vs. `Baseline_LASSO`, descriptive comparison, no DM/z-test | ✅ Complete (2026-07-06) — RMSE −1.74% vs. baseline, IC 0.166 (first defined), Dir. Acc. 0.564 (below baseline's mechanical 0.575); see `reports/statistics/07A_event_lasso_summary.md`. Corroborates the 2026-07-05 Mission 07 Event_LASSO numbers almost exactly. RQ3 not yet answered by this experiment alone. |
| 07B — XGBoost (RQ3 Experiment 2) | Isolated re-run of XGBoost only vs. `Baseline_LASSO`, descriptive comparison, no DM/z-test | ✅ Complete (2026-07-06) — RMSE +2.58% *worse* than baseline, Dir. Acc. 0.512 (worse), severe overfitting (train R² 0.597 → test R² −0.054); see `reports/statistics/07B_xgboost_summary.md`. Does not beat baseline on any metric. RQ3 not yet answered by this experiment alone. |
| 07C — LightGBM (RQ3 Experiment 3) | Isolated single-model re-run, same protocol as 07A/07B | ✅ Complete (2026-07-06) — RMSE −1.68% vs. baseline, R² 0.032, mild overfitting (train 0.119 → test 0.032), `mean_car` dominates gain importance at 36.9%; see `reports/statistics/07C_lightgbm_summary.md`. **07A/07B/07C sequence now complete** — all three models trained descriptively; formal significance testing on this sequence's own numbers still outstanding (existing 2026-07-05 Mission 07 DM/z-test result remains the authoritative tested verdict). |
| 03-PRECHECK — Event Detection Alignment | Audit/update `03_event_detection.ipynb` for consistency with EDA, Research Bible, SAP v1.0, Dataset/Feature Contracts before it is (re-)run | ✅ Complete (2026-07-06) — documentation-only pass; no executable cell logic changed. Two scope findings logged in `10_decision_log.md`: notebook must not consume `master_dataset.parquet` (circular dependency), and event-window construction correctly stays in `04_causal_analysis.ipynb` |
| 03 — Execute, Validate & Freeze (Event Detection) | Run `03_event_detection.ipynb` top-to-bottom, fix runtime errors, verify outputs, freeze | ✅ Complete (2026-07-06) — 2 upstream schema-drift bugs found and fixed (`fomc_dates.parquet` `decision`→`rate_decision`; cache-merge row-explosion); outputs verified on disk (11,664 events, 4,100 high-impact, 4 figures regenerated); 2 row-count corrections applied to `05_data_dictionary.md`; 1 methodology discrepancy flagged for founder decision (sentiment cache is 99.2% FinBERT-sourced, not lexicon as documented) — **resolved 2026-07-06 via Sentiment Engine Freeze v1.0**, see `10_decision_log.md` |
| SEF v1.0 — Sentiment Engine Freeze | Project Director decision: ratify FinBERT as the project's official primary sentiment engine; lexicon retained as fallback/historical prototype only | ✅ Complete (2026-07-06) — documentation-only update across Research Bible, README, Notebook 03, architecture docs; no datasets/models/statistics changed — see `10_decision_log.md` |
| Project Governance Freeze | Create `00_project_freeze.md` — master governance declaration: what is frozen, why, allowed vs. prohibited changes, Project Director sign-off | ✅ Complete (2026-07-06) — references Dataset v1.0, SAP v1.0, FES v1.0, MCP v1.0, SEF v1.0, canonical architecture set, and the full Research Bible; no methodology/datasets/models changed — see `10_decision_log.md` |
| Final Notebook Alignment | Style-align `04`–`08` to the Notebook 03 standard; fix minimal bugs; surface any research inconsistencies | ✅ Complete (2026-07-06) — fixed a `vix.parquet` schema-drift bug in 2 notebooks (same root cause as Notebook 03's fix); surfaced and documented a significant pre-existing gap: notebooks 05–07 implement the legacy pre-freeze pipeline and do not reproduce the frozen `Baseline_LASSO`/`Event_LASSO` result — see `10_decision_log.md`, `future_improvements.md` items 29–31 |
| 08 — Explainability | Deeper SHAP dependence/interaction analysis, PDP | ⬜ Waiting (depends on 07 ✅ — now unblocked; SHAP values already computed, Mission 08 extends the analysis) |
| 09 — Dissertation Synchronisation | Sync figures/tables/results/methods | ⬜ Waiting |

## Project status (as of 2026-07-06 — Project Governance Freeze)

| Field | Value |
|---|---|
| Project Status | **Methodology Frozen** |
| Governance | **Governance Frozen** |
| Documentation Phase | **Dissertation Phase Started** |

See `00_project_freeze.md` for the full governance declaration — what is frozen, why, and what changes remain allowed.

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

1. ~~**🟠 Sentiment cache is 99.2% FinBERT-sourced, contradicting the documented "lexicon is primary" methodology decision**~~ **✅ Resolved (2026-07-06, Sentiment Engine Freeze v1.0).** Project Director ratified FinBERT as the project's official primary sentiment engine, matching the actual pipeline output; documentation corrected across the Research Bible, README, and Notebook 03. No datasets, models, or statistical outputs changed — see `10_decision_log.md`.
2. **🟠 XGBoost overfitting remains uninvestigated at the root-cause level** — reproduced on the FES v1.0 retrain (train R² 0.267 → test R² 0.019), confirming it isn't a superseded-feature-set artefact (`11_limitations.md` L9, `07_model_plan.md`).
3. **🟡 Unrotated API credentials** in `config.yaml` / `notebooks/.env` — gitignored (no commit risk) but not yet rotated.

**Also tracked, not top-3:** QQQ/GLD/TLT scope decision (`10_decision_log.md`, 2026-07-06); GDELT's 5-day sample now confirmed to fall entirely outside the 2015-2025 study window (2026-05-02→05-06, Mission 03 execution) rather than being a historical sample, sharpening `11_limitations.md` L7.

**Resolved since the last update:** the repository is git-tracked (4 commits as of 2026-07-06, including the full `docs/research_bible/` governance layer) and no nested `.git` directory exists — the previous entry here ("zero git commits + a nested git repository") no longer reflects repository state and has been removed rather than carried forward inaccurately.

### What's genuinely solid right now

- Full pipeline (Phases 1–8) runs end-to-end and produces consistent, cross-checked outputs (`05_data_dictionary.md` row-count sanity checks all pass).
- RQ1 and RQ2 have real, defensible, well-documented evidence (`09_results_log.md`).
- Statistical methodology is planned in detail (`04_statistics_plan.md`), including the multiple-comparisons corrections not yet applied — the plan exists even where execution is pending.
- The Research Bible itself (this folder) is now complete as a documentation layer (2026-07-04).
- SAP v1.0's EDA-stage tests (ADF/KPSS, descriptive stats, Pearson/Spearman correlation, correlation-threshold flagging) are now actually implemented and run against the frozen `master_dataset.parquet`, not just specified (`09_results_log.md`, 2026-07-05).
- `feature_matrix.parquet` (FES v1.0) is frozen, validated (PASS), and fully documented — the market-only baseline's feature scope is now contractually enforced (`feature_contract.md`), removing the single largest remaining ambiguity blocking Mission 06.
- All three RQs now have a complete, evidence-based answer (2026-07-05) — RQ1 (provisional pending FDR correction), RQ2 (RF importance + SHAP re-run on FES v1.0), RQ3 (H0₃ not rejected, full DM/z-test comparison against a genuinely-tuned baseline). The project's core empirical work is done; remaining work is explainability depth (Mission 08), dissertation writing, and repository hygiene.

### Immediate next action

**Next decision point:** the 07A/07B/07C sequence is now complete (all three models trained and compared descriptively against `Baseline_LASSO`). Two options for what follows, neither yet actioned: (a) run a formal Diebold-Mariano/two-proportion z-test pass on this sequence's own predictions to see if it agrees with the existing 2026-07-05 Mission 07 verdict (H0₃ not rejected), or (b) proceed directly to **Mission 08 — Explainability**, treating the existing 2026-07-05 Mission 07 result as the authoritative tested RQ3 verdict and this sequence as a corroborating, descriptive cross-check. See `10_decision_log.md` (2026-07-06, "07A/07B/07C isolated experiment sequence complete") for the full reasoning.

**Mission 08 — Explainability:** extend the SHAP analysis already computed in Mission 07 (`reports/model_comparison/shap_values_*.parquet`) with dependence/interaction plots and partial dependence, per `docs/00_project_workflow.md`'s Phase 8 scope. All three RQs now have a complete, evidence-based answer — Mission 08 deepens the RQ2/RQ3 explainability narrative rather than closing a blocking gap.

**Mission 07C — LightGBM, RQ3 Experiment 3 (complete, 2026-07-06):** LightGBM retrained in isolation (all 95 features, identical split/seed/scaling to `Baseline_LASSO`), tuned via `RandomizedSearchCV` (25 iterations, `TimeSeriesSplit(5)`, full search space persisted), compared descriptively only. Test RMSE 0.009470 (−1.68%), R² 0.032 (vs. −0.002), Dir. Acc. 0.553 (vs. 0.575, worse for the same base-rate reason as 07A), IC 0.145, ROC-AUC 0.544 — pattern closely matches Event_LASSO (07A): modest improvement, mild (not severe) overfitting (train R² 0.119 → test R² 0.032). Standout finding: `mean_car` alone is 36.9% of gain importance, the clearest single-feature evidence of event-derived signal across all three experiments. No significance test run (by design). Full detail: `reports/statistics/07C_lightgbm_summary.md`, `10_decision_log.md`.

**Mission 07B — XGBoost, RQ3 Experiment 2 (complete, 2026-07-06):** XGBoost retrained in isolation (all 95 features, identical split/seed/scaling to `Baseline_LASSO`), tuned via `RandomizedSearchCV` (25 iterations, `TimeSeriesSplit(5)`), compared descriptively only. Test RMSE 0.009881 (+2.58% worse), R² −0.054 (vs. −0.002), Dir. Acc. 0.512 (vs. 0.575, worse), IC 0.073, ROC-AUC 0.517 — worse than `Baseline_LASSO` on every regression metric, with severe train/test overfitting (train R² 0.597 → test R² −0.054), reproducing this project's standing XGBoost-overfitting finding (`11_limitations.md` L9). Numbers do not exactly match the 2026-07-05 Mission 07 XGBoost run (different `RandomizedSearchCV` draw — the original run's exact search space was never persisted, only its winning point) but agree qualitatively. No significance test run (by design). Full detail: `reports/statistics/07B_xgboost_summary.md`, `10_decision_log.md`.

**Mission 07A — Event_LASSO, RQ3 Experiment 1 (complete, 2026-07-06):** `Event_LASSO` retrained in isolation (all 95 features, identical split/CV/seed/scaling to `Baseline_LASSO`), compared descriptively only. Test RMSE 0.009465 (−1.74%), R² 0.033 (vs. −0.002), IC 0.166 (first defined value in the RQ3 line), ROC-AUC 0.575 (vs. 0.500) — better than baseline on most legs; Dir. Acc. 0.564 is below baseline's 0.575 but this is not read as a deficiency given the baseline's mechanical base-rate behaviour. No significance test run (by design). Numbers corroborate, and do not contradict, the existing 2026-07-05 Mission 07 full comparison. Full detail: `reports/statistics/07A_event_lasso_summary.md`, `10_decision_log.md`.

**Mission 07 — Event-Enhanced Models (complete, 2026-07-05):** Event_LASSO, XGBoost, and LightGBM retrained on the full 95-feature `feature_matrix.parquet` (FES v1.0), identical split/`TimeSeriesSplit(5)`/seed 42/scaling to `Baseline_LASSO`. Compared via the frozen Diebold-Mariano + two-proportion z-test + Bonferroni protocol (`statistical_decision_matrix.md` Part K) — **none of the three clears the corrected threshold on either leg; H0₃ is not rejected.** RF importance and SHAP re-run on the new matrix, replacing all legacy `model_features.parquet`-derived values. Full detail: `reports/statistics/07_event_models_summary.md`, `10_decision_log.md`.

**Mission 06 — Baseline Model (complete, 2026-07-05):** `Baseline_LASSO` (27 Market-category features, `TimeSeriesSplit(5)`, seed 42) is trained and frozen — see `model_contract.md` (MCP v1.0), `baseline_model_specification.md`, `baseline_evaluation.md`. Headline result: at the cross-validated alpha, all 27 coefficients shrink to zero — the baseline reduces to a mean predictor, a legitimate null finding consistent with weak-form market efficiency. Not yet joined to `model_comparison.parquet` or compared against event-enhanced models — that is Mission 07.

**Mission 05B — Feature Matrix v1.0 (complete, 2026-07-05):** `feature_matrix.parquet` (95 features, 2,511 rows, validation PASS) is frozen and documented in `feature_contract.md`/`06_feature_dictionary.md`/`feature_profile.json`. Built from `master_dataset.parquet` + `car_results.parquet` (the latter approved as a second input, `10_decision_log.md`). RF-importance selection against this new matrix (re-running the 0.001-threshold pass that produced the legacy RQ2 result) and Mutual Information corroboration are not yet run — both remain open, non-blocking items tracked in `15_traceability_matrix.md`.

---

## Dashboard maintenance rule

If this document and any other Research Bible document disagree on status, the more granular document (e.g. `01_research_questions.md` for RQ status, `13_validation_checklist.md` for a specific checklist item) is authoritative — update this dashboard to match, not the other way around.
