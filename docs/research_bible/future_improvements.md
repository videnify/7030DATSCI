# Future Improvements

**Purpose:** Non-critical improvements, technical debt, and refactoring ideas identified during repository maintenance sprints. Nothing here is to be implemented before dissertation submission — this is a parking lot, not a task list for the current work.
**Owner:** Ibrahim Haroun.
**Dependencies:** `10_decision_log.md` (promote an item here to a decision only when actually scheduled), `15_traceability_matrix.md`, `14_project_dashboard.md`.
**Update Frequency:** Append during any audit/maintenance sprint; do not reorder or delete past entries — mark them done in place instead.
**Relation to Dissertation:** None directly — this document exists precisely to keep post-submission ideas out of the dissertation-critical path.

---

## Repository governance

1. ~~**Track the Research Bible in git.**~~ **✅ Done (2026-07-06).** All files under `docs/research_bible/` are now tracked (confirmed committed as of commit `a9da995`, 2026-07-06). No further action needed.
2. ~~**Reconcile `14_project_dashboard.md`'s stated risks with current repo state.**~~ **✅ Done (2026-07-06, RCS v1.1).** The stale "zero git commits + nested git repository" risk was removed and replaced with an accurate note (4 commits, no nested `.git`).
3. ~~**Remove the stale `.git/index.lock`.**~~ **✅ Done (2026-07-06, RCS v1.1).** Verified no git process was running and removed the lock file. Note: this environment's git occasionally recreates and cannot fully clean up `index.lock` on its own read commands (observed during this sprint) — if `git add`/`commit` ever fails with "index.lock: File exists," re-check for a stale lock before assuming a real concurrency problem.
4. **Rotate credentials referenced in `config.yaml` / `notebooks/.env`.** Still outstanding — gitignored so no exposure via git, but rotation itself was out of scope for this cleanup sprint (not a file-organisation task).
5. ~~**Decide the fate of QQQ/GLD/TLT.**~~ **✅ Done (2026-07-06).** Logged as a supplementary/out-of-scope decision in `10_decision_log.md` (2026-07-06 entry) — columns retained in schema, explicitly not usable as RQ1–RQ3 evidence unless revisited.

## Documentation

6. ~~**Update `models/README.md`.**~~ **✅ Done (2026-07-06, RCS v1.1).** Rewritten to describe `models/baseline/`, `models/event/`, and the new `models/archive/`, plus an explicit legacy-model policy.
7. **Regenerate `data/raw/README.md` and `data/processed/README.md`.** Still outstanding — `05_data_dictionary.md` remains authoritative in the meantime. Deferred, not part of the approved cleanup scope.
8. **Add missing per-folder READMEs.** Still outstanding for `src/`, `tests/`, `scripts/`, `reports/` (root and subfolders), `models/baseline/`, `models/event/`, `models/archive/` (new), and `notebooks/archive/`.
9. ~~**Fix the `07_machine_learning.ipynb` cross-reference in the root `README.md`.**~~ **✅ Done (2026-07-06, RCS v1.1).**
10. ~~**Reconcile `notebooks/01_data_collection.ipynb`'s macro-indicator markdown with the frozen schema.**~~ **✅ Done (2026-07-06, RCS v1.1).** Markdown-only edit to cell 14; cell 15's executable `FRED_SERIES` dict was deliberately left unchanged (frozen architecture, cache guard already prevents re-collection) — see the new technical-debt item below.

## Architecture

11. **Add a `config/` folder, or explicitly document why a single `config.yaml` is sufficient.** Still outstanding — out of scope for this cleanup sprint.
12. ~~**Archive the legacy top-level model artefacts.**~~ **✅ Done (2026-07-06, RCS v1.1).** All 7 files moved into the newly created `models/archive/`; nothing deleted.
13. **Consider a numbered-prefix rename for `reports/08_05_2026_DATSCI7030_Data_Collection_Report.{pdf,docx}`.** Still outstanding — a rename touches `reports/`, which was not in this sprint's approved scope.

## Testing

14. **Expand `tests/` coverage.** Still outstanding; unchanged from the last audit.

## Newly identified (RCS v1.1, 2026-07-06)

15. **Notebook 01's `FRED_SERIES` dict (cell 15, code) still does not match the cached/frozen macro schema.** The markdown was corrected this sprint, but the executable dict still pulls only 5 series under `cpi_index`/`unemployment_rate` keys and does not derive `mfg_employment` or `yield_spread`. This is a latent reproducibility gap: if `data/raw/macro_indicators.parquet` is ever lost, rerunning this cell as currently written will not reproduce the existing schema. Fixing it is a real code change to a frozen-architecture notebook, correctly out of scope for a documentation-only cleanup sprint — tracked here for whenever Notebook 01 is next legitimately revisited (see `10_decision_log.md`, 2026-07-06 entry, "Reversible" clause).
16. **`data/fred_client.py` sits directly under `data/` rather than `src/`.** Every other collection/processing module lives in `src/` (`data_collector.py`, `event_detector.py`, etc.); a single script under `data/` is a minor structural inconsistency worth folding into `src/` in a future pass.
17. **No README yet for `models/archive/`** (created this sprint) — the legacy-model policy is documented in `models/README.md`, but a short standalone README in the folder itself would match the standard applied elsewhere once folder-level READMEs (item 8) are addressed.

## Newly identified (Mission 07B, 2026-07-06)

18. **Persist full `RandomizedSearchCV` `param_distributions` for every tree-model tuning pass, not just the winning `best_params`.** The original 2026-07-05 Mission 07 XGBoost/LightGBM runs only recorded their winning hyperparameters in `event_model_metadata.json`, not the search space they were drawn from — this meant Mission 07B could not reproduce that run's exact result and had to reconstruct a new (documented) search space instead, producing a qualitatively similar but numerically different overfitting result. `models/event/xgboost_07b_metadata.json` now persists both `param_distributions` and `best_params` — apply the same practice retroactively to the original Mission 07 XGBoost/LightGBM metadata if those runs are ever revisited, and to Mission 07C (LightGBM) going forward.
19. **XGBoost's overfitting severity appears sensitive to the hyperparameter search space itself** (07B's reconstructed grid produced a worse train/test collapse — train R² 0.597→test R² −0.054 — than the original run's 0.267→0.019). This is consistent with, but does not newly resolve, the standing root-cause investigation already tracked in `11_limitations.md` L9; worth revisiting once (or if) that investigation happens, since it suggests the overfitting is at least partly a search-space/regularisation-strength artefact rather than purely a fixed property of the feature set.

## Newly identified (Mission 03-PRECHECK, 2026-07-06)

20. **`events_tagged.parquet` has no dedicated unique event-ID column.** The alignment pass's new duplicate-check cell (`validation-checks`) proxies on the natural key `(date, title, doc_type)` instead. A real surrogate ID (e.g. a hash of the natural key, or a simple integer index assigned at catalogue-build time) would make future de-duplication and cross-notebook joins more robust — not actioned now, as it would touch the frozen `events_tagged.parquet` schema.
21. **High-impact event flagging does not condition on VIX regime.** `02_eda.ipynb` §9.5 (Mission 05A) confirms volatility clustering matters (2020/2022 regimes clearly visible in rolling statistics); `03_event_detection.ipynb`'s `HIGH_IMPACT_TYPES`/`CONFIDENCE_THRESHOLD` criteria currently ignore VIX level entirely. A VIX-regime-aware high-impact definition is a plausible v1.1 enhancement to the event catalogue, not a correctness issue with the current one.
22. **A mission brief can suggest inputs/outputs that don't match the actual pipeline dependency graph.** The Mission 03-PRECHECK brief listed `master_dataset.parquet` as a "preferred input" for `03_event_detection.ipynb` and suggested `detected_events.parquet`/`event_windows.parquet`/`event_calendar.parquet` as expected outputs — neither holds up against the real dependency order (`10_decision_log.md`, 2026-07-06). Worth remembering for any future mission brief that references this notebook: verify suggested file relationships against `dataset_contract.md`'s consumer list before applying them mechanically.

## Newly identified (Mission 03 execution, 2026-07-06)

23. ~~**Sentiment methodology documentation vs. actual cached data disagree.**~~ **✅ Resolved (2026-07-06, Sentiment Engine Freeze v1.0).** Project Director ratified FinBERT as the project's official primary sentiment engine (matching the actual 99.2% FinBERT-sourced cache); the lexicon scorer is now documented as a fallback/historical prototype only. Documentation updated across `03_methodology.md`, `11_limitations.md`, `06_feature_dictionary.md`, `dataset_version.md`, `04_statistics_plan.md`, root `README.md`, Notebook 03, and `14_project_dashboard.md`. No datasets, models, or statistical outputs were changed — see `10_decision_log.md`.
24. **`data/raw/fomc_dates.parquet` and `data/raw/vix.parquet` schemas have drifted from what several Research Bible documents describe** (`decision`→`rate_decision`, `is_surprise`→`is_emergency`+`event_importance`; `vix`→`vix_close`/`vix_change`/`vix_high_regime`). Fixed at the point of use in `03_event_detection.ipynb`; worth a full sweep of `05_data_dictionary.md`/other notebooks (01, 02, 04+) for the same drift, since only Notebook 03 was in scope this session.
25. **124 duplicate `(date, title, doc_type)` rows in `events_tagged.parquet`**, surfaced by the new validation cell — plausibly genuine (recurring generic titles like repeated press-briefing or proclamation names on different underlying documents), not yet root-caused. Combine with item 20 (no unique event-ID column) as a joint future data-quality pass.
26. **GDELT's "5-day sample" is a recent live pull (2026-05-02→05-06), not a historical sample from within 2015–2025.** Confirmed by the new date-range validation check. Strengthens the case in `11_limitations.md` L7 to exclude GDELT-derived features from any "final" result until a genuine historical backfill exists — not actioned here.

## Newly identified (Architecture SVG Cleanup, 2026-07-06)

27. **A proper DoWhy causal DAG diagram is worth rebuilding once the GDELT scope question closes.** Both archived `causal_dag_dowhy*.svg` files depicted GDELT/Goldstein scale as a core input to the causal model, which it isn't (confounders are VIX regime and prior-day return, per `03_methodology.md` §2) — not rebuilt as one of the 5 canonical diagrams this session since it wasn't in the requested set and would need to wait on `11_limitations.md` L7/L8's resolution to avoid the same inaccuracy.
28. **`docs/architecture/archive/` has no folder-level README of its own** — the archival reasoning lives in the main `docs/architecture/README.md` instead. Fine for now given the folder's small size; revisit if the archive grows.

## Newly identified (Final Notebook Alignment, 2026-07-06)

29. ~~**No executable notebook reproduces the frozen MCP v1.0 model-comparison result.**~~ **✅ Resolved (2026-07-06, Mission 05-07 Reproducibility Rebuild).** `notebooks/05_feature_engineering.ipynb`, `06_model_training.ipynb`, and `07_model_evaluation.ipynb` were rebuilt to read `master_dataset.parquet`/`car_results.parquet` → `feature_matrix.parquet` → `Baseline_LASSO`/`Event_LASSO`/`XGBoost`/`LightGBM`, and validated to reproduce every frozen number (feature values, model coefficients, RMSE/MAE/R²/Dir_Acc/IC, Diebold-Mariano and two-proportion z-test statistics) to within 1e-6, executed end-to-end in-sandbox with zero errors. See `10_decision_log.md` (2026-07-06, Mission 05-07 Reproducibility Rebuild entry) for the full validation record, including one genuine bug the reproduction check itself caught and fixed (a sign-dependent one-sided p-value formula in the two-proportion z-test).
32. ~~**Notebook 08 still reads the legacy `model_features.parquet`/`model_comparison.parquet` for figures 08c/08d.**~~ **✅ Resolved (2026-07-06, Results Visualisation Freeze v1.0).** `08_results_visualisation.ipynb`'s `load-data` cell and figures 08c/08d were rebuilt to read exclusively from `feature_matrix.parquet`, `reports/model_comparison/`, and `reports/baseline/`. Both figures now show the full 4-model comparison (including `Baseline_LASSO`) and state the RQ3 null result directly on the figure. See `10_decision_log.md` (2026-07-06, Results Visualisation Freeze v1.0 entry) for the full audit, including a genuine SHAP `base_value` bug the rebuild introduced and then caught by visual inspection before finalising.

## Newly identified (Final Notebook Alignment, 2026-07-06, continued)

30. **`data/raw/vix.parquet`'s `vix`→`vix_close` schema drift affected three notebooks, not just Notebook 03.** `04_causal_analysis.ipynb` (two occurrences) and `05_feature_engineering.ipynb` (one occurrence at load) both hardcoded the old `vix` column name and would crash with `KeyError: "['vix'] not in index"` if re-run — fixed by aliasing `vix_close` → `vix` immediately after load in both notebooks (same pattern as the Notebook 03 `fomc_dates.parquet` fix). `06_model_training.ipynb`/`07_model_evaluation.ipynb`/`08_results_visualisation.ipynb` were not affected (they read the already-merged legacy `model_features.parquet`, not the raw file). Worth a proactive check of `01_data_collection.ipynb`/`02_eda.ipynb` for the same drift if either is next revisited, per item 24 above.
31. **Figures `08c_predictive_pipeline.png`/`08d_full_dashboard.png` are confirmed stale**, not just "pending" — they are generated from the legacy `model_features.parquet`/`model_comparison.parquet`, so they show the pre-baseline 3-model comparison referenced in item 29, not the frozen MCP v1.0 result. `08_figures_plan.md` already flagged these for regeneration; this entry confirms the root cause precisely (legacy notebook inputs, not a data-freshness issue that a simple re-run would fix).

---

## Explicitly deferred (do not action before submission)

- Any change to `master_dataset.parquet`, `feature_matrix.parquet`, SAP v1.0, FES v1.0, or MCP v1.0.
- Renaming or moving any file under `data/raw/` or `data/processed/`.
- Rerunning, retraining, or re-deriving any frozen/versioned artefact.
- Rebuilding Notebook 01's executable macro-collection logic (item 15) — documentation-only fix applied this sprint; code fix deferred.
- Credential rotation (item 4) — a security housekeeping task, not a repository-organisation task.
- Physically reordering `03_event_detection.ipynb`'s existing cells to match a suggested 13-section template (Mission 03-PRECHECK, 2026-07-06) — documentation added in place instead; a full reorder was judged unverifiable-without-execution risk for no functional benefit.
