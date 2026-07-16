# 14 — Project Dashboard

**Purpose:** One-page, at-a-glance snapshot of current project status across phases, research questions, and open risks — the first document to read at the start of any session to re-orient quickly.
**Owner:** Ibrahim Haroun.
**Dependencies:** Synthesises `00_project_overview.md`, `01_research_questions.md`, `11_limitations.md`, `13_validation_checklist.md`, and `DATSCI7030_Repository_Audit_Report.ipynb`.
**Update Frequency:** Update at the end of every working session — this should never be more than one session stale.
**Relation to Dissertation:** Not directly quoted in the dissertation; it's the project-management layer that keeps the Research Bible internally consistent.

---

## 2026-07-16 current state — Dissertation accepted; repository cleaned, documented and frozen pending assessment feedback

**What changed (content, prior session):** the accepted dissertation (`reports/dissertation/2026-07-16-7030DATSCI.docx`/`.pdf`) had its two Section 3.3 event-study equations inserted as native OMML objects (they previously did not render), a duplicated Section 4.1 event-catalogue sentence removed, a citation-grammar defect fixed (Section 3.4's `(Sharma, et al., 2020)` → `(Sharma and Kiciman, 2020)`; `(Pearl, 2009) structural causal model` → `Pearl's (2009) structural causal model`), and reader-facing LASSO naming made consistent across nine paragraphs. Three new Appendix figures were added — A7 (causal DAG, newly created from Table 4's exact node/edge list), A8 (held-out residual diagnostics, newly created from the current test-split predictions), A9 (research-governance architecture, reusing the existing canonical `docs/architecture/research_governance.svg` unchanged) — plus new Appendix B2–B4 sections (repository/artefact map, environment/validation summary, GitHub availability statement). `Table A1` was renamed `Table B1`. No research question, dataset, model, numerical result, main-body figure, or RQ1–RQ3 conclusion was changed; all 15 pre-existing embedded images were confirmed byte-identical before/after. Full detail: `reports/dissertation/SUBMISSION_QA_CHANGELOG_2026-07-15.md` covers the immediately-prior QA pass; this appendix/equation pass itself is recorded by its pre-edit backup (`reports/dissertation/archive/2026-07-16-7030DATSCI_PREEDIT_BACKUP_20260716174628.docx`) rather than a separate changelog file.

**What changed (repository cleanup and freeze, this session):** a full inspection-first repository finalisation pass. (1) **Baseline recorded** before any change: `reports/finalisation/REPOSITORY_PRE_FREEZE_BASELINE_2026-07-16.md` and SHA-256 hashes for every protected artefact in `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`, re-verified identical after cleanup. (2) **Safe cleanup executed** (all untracked/gitignored, zero Git-history impact): removed 11 `.ipynb_checkpoints/` directories, 8 `.DS_Store` files, 2 `__pycache__/` directories, `.pytest_cache/`, and 2 stray Word lock files inside an existing archive folder. (3) **`reports/dissertation/` cleaned**: four superseded 2026-07-15 dissertation versions moved into a new dated `archive/superseded_2026-07-16/` subfolder (following the repository's existing archive convention, no new archive system introduced); a disposable LibreOffice preview PDF used only for this session's own equation-rendering QA was deleted (never a dissertation version); `reports/dissertation/README.md` rewritten to reflect the accepted 2026-07-16 files, their hashes, and the archive contents. (4) **Documentation currency pass**: `notebooks/README.md` extended with execution-order/I-O summary, frozen-snapshot behaviour, external-data warning, expected-environment pointer, and current validation status; `scripts/README.md` and `reports/figures/README.md` updated to document the two new appendix-figure scripts and three new appendix figures; `00_project_overview.md`'s phase-status table updated from "Dissertation Writing 🟡 In Progress" to "✅ Accepted 2026-07-16" (the only status-table entry that was genuinely stale — everything else inspected was already current). (5) **Validation re-run**: all eight notebooks confirmed valid JSON; all Python files in `src/`, `scripts/`, `tests/` compile cleanly; the full test suite (`/usr/local/bin/python3 -m pytest tests/`) passes 18/18, unchanged from the 2026-07-15 dashboard entry; all architecture SVGs and all processed/report JSON files confirmed well-formed.

**Findings flagged for owner decision, not silently resolved:**
- `reports/dissertation/7030DATSCI-15_07_2026_Generative_AI_Statement.docx` predates this session's AI-assisted appendix/equation edit and does not disclose it — left in place, not archived, pending a decision on whether it needs updating before submission.
- `data/Equation.png` (3.2 MB, untracked) — an equation-rendering verification screenshot, not project data, not referenced anywhere — left in place rather than unilaterally deleted, pending owner confirmation it is disposable.
- Five tracked notebooks (`02`, `03`, `04`, `05`, `06`) contain a printed local machine path (`/Users/videnify/...`) in an already-executed, protected cell output. Not fixed — doing so would mean re-running a frozen notebook, which is prohibited without a dated decision-log entry of its own. Flagged for a future, explicitly-approved documentation-only touch (clearing just that one printed line) if desired.
- No secrets, API keys, or tokens found in any Git-tracked file (checked via pattern scan). `config.yaml` and `notebooks/.env` remain correctly gitignored (this repeats the already-tracked, already-accepted 2026-07-06 risk item below — not a new finding).

**RQ1–RQ3 impact:** None, in either the dissertation content pass or the repository cleanup pass. See `docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md` for the full freeze declaration.

**Historical dates preserved:** all dates in `10_decision_log.md`, `09_results_log.md`, and every entry below this one in this file are untouched. The single content-date correction made was `00_project_overview.md`'s phase-status table header (`as of 2026-07-14` → `as of 2026-07-16`), which is a live status table, not a historical record.

---

## 2026-07-15 current state — Full eight-notebook traceability audit; documentation completed

**What changed (technical):** a full inspection-only traceability audit of all eight notebooks found and closed four findings: (1) a Notebook 01 GDELT branch-logic defect (a stale saved cell whose branch order tested one file but read another) was fixed with explicit `REFRESH_GDELT_RAW`/`REBUILD_GDELT_DAILY_SUMMARY` flags and a real error instead of a silent all-zero fallback; (2) the pooled/overall DoWhy causal estimate, previously only a hand-copied literal in `08_results_visualisation.ipynb`, is now persisted by Notebook 04 to a dedicated artefact, `data/processed/causal_overall_estimate.json` (effect +0.005601, 95% CI [+0.002295, +0.008907], p=0.0009, n=2,762), which Notebook 08 now reads directly; (3) the only event-study unit test was testing unused legacy code (`src/causal_engine.py::EventStudy`, an OLS market-model design) rather than the actual active constant-mean-return methodology — the old test file was renamed to `tests/test_legacy_causal_engine.py` (explicitly marked legacy) and a new `tests/test_event_study.py` (10 tests) was added against a new dependency-free reference module, `src/event_study_reference.py`, cross-validated against all 264 rows of `car_results.parquet`; (4) a Mission 05A EDA citation was corrected in `09_results_log.md` (Notebook 02 loads a Notebook 01 precursor file, not the later canonical `master_dataset.parquet`). **Test suite is now 18 passing tests** (`/usr/local/bin/python3 -m pytest tests/ -q`), not the 8 recorded in the entries below — those entries are preserved as-written since they were accurate for the test suite that existed on 2026-07-14, before today's legacy/active test split.

**Live re-execution:** both edited notebooks (04, 08) were executed end-to-end from clean kernels; all reported RQ1–RQ3 figures, all frozen `.parquet`/`.joblib` artefacts, and all four Notebook 08 figures were confirmed byte-identical before and after. **No RQ1–RQ3 result changed.**

**What changed (documentation):** the stakeholder report (`docs/stakeholder_report/`) is now complete — all eight stage pages plus an executive summary are written and verified, closing the "not yet written" gap that existed for stages 2–8 as of 2026-07-14. The root `README.md` and `docs/architecture/README.md` version/date headers were updated and both now reference `causal_overall_estimate.json`. `15_traceability_matrix.md` and `05_data_dictionary.md` were updated to list the new artefact. A new governance section (`00_project_freeze.md` §10) codifies the documentation-impact/date-maintenance discipline used throughout this pass.

**RQ1–RQ3 impact:** None. See `10_decision_log.md`'s 2026-07-15 entries for the full technical record.

## 2026-07-14 current state — FES v1.1 pipeline and publication figures complete

**What changed:** Notebooks 01–02 performed a genuine GDELT full-history backfill (`gdelt_daily_summary.parquet`, 4,018 days, 2015–2025, replacing the 5-day proof-of-concept sample); Notebook 03 now runs an economic pre-filter over the APP catalogue (916 documents, 344 high-impact events, down from tagging all 11,570); `master_dataset.parquet` was re-frozen as v1.1; Notebooks 04–08 were all fixed and re-verified end-to-end against this new data. Full detail: `10_decision_log.md` (2026-07-13 entries, GDELT backfill through the architecture-diagram/documentation-consistency pass).

**RQ status changes:**
- **RQ1 evidence base has genuinely changed, not just been re-verified:** the event-study CAR significance test is now a **null result** (no event type reaches p<0.10 on the current 264-row `car_results.parquet`; the original "geopolitical is significant" finding no longer holds against this data). The overall DoWhy causal estimate remains significant (+0.005601, 95% CI [+0.002295, +0.008907], p=0.0009), and the `monetary` per-category estimate closely replicates the original frozen figure — a genuine robustness signal despite the fully rebuilt pipeline. **Resolved 2026-07-14:** the dissertation has been updated to report this rebuilt evidence base.
- **RQ3:** answered on FES v1.1; no event-enhanced candidate beats the market-only baseline under the corrected two-leg rule, so H0₃ is not rejected.
- **RQ2:** answered on FES v1.1; the Random Forest top decile includes macro/VIX but no event feature, so H0 is not rejected under the frozen descriptive rule. LightGBM SHAP ranks `mean_car` fifth as model-specific corroborating evidence. GDELT remains deliberately outside the feature specification.

**Resolved since the last update:** GDELT's 5-day-sample limitation (`11_limitations.md` L7, tracked as a non-top-3 risk below) — full 2015–2025 history now integrated. Repository cleanup removed 25GB of raw GDELT dumps and stale pre-rebuild artefacts (archived, not deleted); repository size 25GB → 106MB.

**Resolved 2026-07-14:** the `03_event_detection.ipynb` vs. `03_event_detection_revised.ipynb` duplication flagged above is closed — the Project Director confirmed `src/event_detector.py` is imported only by `_revised`, so the pre-rebuild `03_event_detection.ipynb` was archived to `notebooks/archive/03_event_detection.ipynb` and `_revised` was renamed to the canonical `03_event_detection.ipynb`, matching the `01_data_collection.ipynb` resolution pattern. See `10_decision_log.md`.

## 2026-07-14 Founder update — Dissertation sync and Notebook 07 completion

- **Dissertation result sync:** the changed RQ1 finding, full-history GDELT integration, and rebuilt RQ3 results have been incorporated into the canonical dissertation draft. The broader pre-submission cross-reference and traceability pass remains part of Mission 09.
- **Notebook 07 execution state:** resolved. All 16 code cells in `07_model_evaluation.ipynb` now have execution counts, there are zero saved error outputs, and `reports/figures/07_learning_outcome.png` was regenerated by the completed run.
- **Notebook 07 result/validation:** ✅ FES v1.1 model suite complete and repeat-verified. Event_LASSO exactly matches the baseline; XGBoost and LightGBM are numerically worse; no candidate clears the Bonferroni-corrected DM and directional-accuracy legs. The RF/SHAP outputs are current, validation is `PASS`, and all 13 primary artefact hashes remain identical on repeat execution.
- **Feature-matrix validation state:** ✅ resolved structurally in FES v1.1. The 2,477-row, 92-feature matrix reports unconditional validation `PASS`; the superseded FES v1.0 `FAIL` and accepted exception are archived as historical evidence.
- **Dependency manifest:** ✅ resolved 2026-07-14 on Python 3.14.6. `requirements.txt` now contains direct pipeline dependencies, `requirements-dev.txt` adds testing/optional development dependencies, and `requirements-lock.txt` records the exact installed environment. The refreshed lock includes the full canonical pipeline (`scipy`, `statsmodels`, `scikit-learn`, `xgboost`, `seaborn`, `transformers`, `torch`, `tqdm`, and `lxml`) plus `pytest`/`newsapi-python`. SHAP is correctly guarded to Python <3.14 because its Numba dependency does not support Python 3.14; the canonical Notebook 07 uses native XGBoost/LightGBM contribution APIs instead. Verification result: **8 tests passed** (`python -m pytest -q`, 2026-07-14).

## 2026-07-14 controlled Dataset v1.2 / FES v1.1 migration

- **Notebook 03 — ✅ complete and verified.** `03_event_detection.ipynb` now aggregates explicit `n_health_catalogue_events`, `n_labour_catalogue_events`, and `n_other_catalogue_events` columns independently of sentiment polarity. All 17 code cells executed with zero saved errors. `daily_sentiment.parquet` is now 739 rows × 18 columns; occurrence totals 14/103/427 reconcile exactly to the 1,005-row catalogue, contain no nulls, and use integer dtype. The prior four Notebook 03 outputs were archived locally under `data/processed/archive/pre_dataset_v1_2_notebook03_2026-07-14/`. Eight repository tests pass.
- **Why this step matters:** FES v1.0 inferred health/labour/other event occurrence using `sentiment_category != 0.0`, which incorrectly maps a neutral event to “no event.” Direct counts separate occurrence from polarity and make `labour_event_day` observable even when every labour sentiment score is neutral.
- **Dataset v1.2 — ✅ frozen and verified.** `scripts/build_master_dataset.py` promoted the three occurrence counts and now writes `master_dataset_validation.json`. The frozen file is 2,765 × 34 with the unchanged 2,014/751 split. Only the intended three columns were added; every v1.1 column is value-for-value identical. Validation status is `PASS`, artefact SHA-256 is `142145722faff37156c6606801ae82d56843118b486942b050629b0472647819`, and eight repository tests pass.
- **Trading-calendar disclosure:** all-calendar occurrence totals are 14/103/427; the same-date SPY panel contains 12/96/395. The excluded 2/7/32 health/labour/other events occurred on non-trading dates and are recorded without next-session reassignment (`11_limitations.md` L17).
- **Notebook 05 / FES v1.1 — ✅ complete and verified.** The matrix has 92 features and 2,477 rows (1,727 train / 750 test). `energy`, `labour`, and `monetary_x_rate_cut` were removed under the <1e-8 training-variance rule; the three direct occurrence flags changed on 7/90/299 rows. Validation is `PASS`; matrix SHA-256 is `127a6dbe4b83e59c873dfdf7502060aab115037732bbb723f9d489c6b85dc383`.
- **Notebook 06 / `Baseline_LASSO` v1.1 — ✅ complete and verified.** All 10 code cells executed with zero saved errors. The model reads exactly 27 Market features, uses 1,727/750 train/test rows, selects alpha 0.0018533887501907256, and shrinks all coefficients to zero. Test RMSE is 0.009631 and directional accuracy is 0.5747. The full SAP metric suite is persisted, validation is `PASS`, all five artefacts reload successfully, and the comparison to the dated FES v1.0 archive is exact.
- **Notebook 07 / model evaluation v1.1 — ✅ complete and verified.** All 16 code cells executed with zero saved errors. Event models, RF/SHAP rankings, DM/z-tests, full SAP diagnostics, and 13 primary artefact hashes passed validation and a repeat-run idempotence check.
- **Notebook 08 / Visualisation v1.2 — ✅ complete and verified.** All code cells have execution counts and zero saved errors. Figures 08a–08d are regenerated from current validated inputs; Figure 08b displays BH q and Cohen's d from RQ1-v1.0. Figure hashes and upstream bindings are recorded in `results_visualisation_validation.json`, which reports `PASS`.
- **Current migration boundary:** the FES v1.1 notebook chain is closed. Remaining work is dissertation statistical-reporting, citation/cross-reference, security, and submission QA.

---

## Mission status (Mission Control v2.0)

| Mission | Objective | Status |
|---------|-----------|:---:|
| 01 — Repository Governance | Clean repo, gitignore, README, workflow, audit | ✅ Complete |
| 02 — Research Bible | 16-document Research Bible | ✅ Complete |
| 03 — Freeze Dataset v1.2 | `master_dataset.parquet` frozen, validated, documented | ✅ Complete (2026-07-14) — 2,765 × 34, validation `PASS`, SHA-256-bound report |
| 04 — Statistical Design Freeze | Freeze α, metrics, assumptions, test matrix | ✅ Complete (2026-07-04) — SAP v1.0 frozen across `statistical_analysis_plan.md` + 4 companion docs |
| 05A — Statistical Implementation (EDA) | Implement SAP v1.0 descriptive/time-series/correlation analysis on `master_dataset.parquet` | ✅ Complete (2026-07-05) — `notebooks/02_eda.ipynb` §9, `reports/tables/02_*.csv`, `reports/figures/02m`–`02r` |
| 05B — Feature Matrix v1.1 | Freeze `feature_matrix.parquet` from Dataset v1.2 + `car_results.parquet`; enforce variance/leakage/source validation | ✅ Complete (2026-07-14) — 92 features, 2,477 rows, validation `PASS`, exact migration delta and hashes persisted |
| 06 — Baseline Model | RQ3 market-only baseline (`Baseline_LASSO`) + MCP v1.0 | ✅ `Baseline_LASSO` v1.1 frozen 2026-07-14; FES/contract/output validation `PASS`; archived FES v1.0 reproduction exact |
| 07 — Event-Enhanced Models | Retrain LASSO/XGBoost/LightGBM; compare vs. Mission 06 baseline; regenerate RF/SHAP | ✅ FES v1.1 complete 2026-07-14; validation `PASS`; repeat-run hashes stable; H0₃ not rejected |
| 07A — Event_LASSO (RQ3 Experiment 1) | Isolated re-run of Event_LASSO only vs. `Baseline_LASSO`, descriptive comparison, no DM/z-test | ✅ Complete (2026-07-06) — RMSE −1.74% vs. baseline, IC 0.166 (first defined), Dir. Acc. 0.564 (below baseline's mechanical 0.575); see `reports/statistics/07A_event_lasso_summary.md`. Corroborates the 2026-07-05 Mission 07 Event_LASSO numbers almost exactly. RQ3 not yet answered by this experiment alone. |
| 07B — XGBoost (RQ3 Experiment 2) | Isolated re-run of XGBoost only vs. `Baseline_LASSO`, descriptive comparison, no DM/z-test | ✅ Complete (2026-07-06) — RMSE +2.58% *worse* than baseline, Dir. Acc. 0.512 (worse), severe overfitting (train R² 0.597 → test R² −0.054); see `reports/statistics/07B_xgboost_summary.md`. Does not beat baseline on any metric. RQ3 not yet answered by this experiment alone. |
| 07C — LightGBM (RQ3 Experiment 3) | Isolated single-model re-run, same protocol as 07A/07B | ✅ Complete (2026-07-06) — RMSE −1.68% vs. baseline, R² 0.032, mild overfitting (train 0.119 → test 0.032), `mean_car` dominates gain importance at 36.9%; see `reports/statistics/07C_lightgbm_summary.md`. **07A/07B/07C sequence now complete** — all three models trained descriptively; formal significance testing on this sequence's own numbers still outstanding (existing 2026-07-05 Mission 07 DM/z-test result remains the authoritative tested verdict). |
| 03-PRECHECK — Event Detection Alignment | Audit/update `03_event_detection.ipynb` for consistency with EDA, Research Bible, SAP v1.0, Dataset/Feature Contracts before it is (re-)run | ✅ Complete (2026-07-06) — documentation-only pass; no executable cell logic changed. Two scope findings logged in `10_decision_log.md`: notebook must not consume `master_dataset.parquet` (circular dependency), and event-window construction correctly stays in `04_causal_analysis.ipynb` |
| 03 — Execute, Validate & Freeze (Event Detection) | Run `03_event_detection.ipynb` top-to-bottom, fix runtime errors, verify outputs, freeze | ✅ Complete (2026-07-06) — 2 upstream schema-drift bugs found and fixed (`fomc_dates.parquet` `decision`→`rate_decision`; cache-merge row-explosion); outputs verified on disk (11,664 events, 4,100 high-impact, 4 figures regenerated); 2 row-count corrections applied to `05_data_dictionary.md`; 1 methodology discrepancy flagged for founder decision (sentiment cache is 99.2% FinBERT-sourced, not lexicon as documented) — **resolved 2026-07-06 via Sentiment Engine Freeze v1.0**, see `10_decision_log.md` |
| SEF v1.0 — Sentiment Engine Freeze | Project Director decision: ratify FinBERT as the project's official primary sentiment engine; lexicon retained as fallback/historical prototype only | ✅ Complete (2026-07-06) — documentation-only update across Research Bible, README, Notebook 03, architecture docs; no datasets/models/statistics changed — see `10_decision_log.md` |
| Project Governance Freeze | Create `00_project_freeze.md` — master governance declaration: what is frozen, why, allowed vs. prohibited changes, Project Director sign-off | ✅ Complete (2026-07-06) — references Dataset v1.0, SAP v1.0, FES v1.0, MCP v1.0, SEF v1.0, canonical architecture set, and the full Research Bible; no methodology/datasets/models changed — see `10_decision_log.md` |
| Final Notebook Alignment | Style-align `04`–`08` to the Notebook 03 standard; fix minimal bugs; surface any research inconsistencies | ✅ Complete (2026-07-06) — fixed a `vix.parquet` schema-drift bug in 2 notebooks (same root cause as Notebook 03's fix); surfaced and documented a significant pre-existing gap: notebooks 05–07 implement the legacy pre-freeze pipeline and do not reproduce the frozen `Baseline_LASSO`/`Event_LASSO` result — see `10_decision_log.md`, `future_improvements.md` items 29–31 |
| Mission 05-07 Reproducibility Rebuild | Rebuild `05`–`07` so they reproduce the frozen `feature_matrix.parquet`/`Baseline_LASSO`/`Event_LASSO`/`XGBoost`/`LightGBM` artefacts end-to-end from a clean checkout, closing item 29 above | ✅ Complete (2026-07-06) — all 3 notebooks rewritten (v3.0) and executed top-to-bottom with zero errors; `REPRODUCTION_EXACT = True` for feature values (1e-6) and `Baseline_LASSO` coefficients/metrics; Event_LASSO/XGBoost/LightGBM metrics and DM/z-test statistics match frozen values within 1e-6; RQ3 verdict (H0₃ not rejected) reproduces exactly. One substantive bug found and fixed during reconstruction (two-proportion z-test one-sided p-value formula was sign-conditional, not fixed-direction) — caught by the reproduction-check itself, never reached a saved output. No frozen dataset/model/RQ/SAP/FES/MCP content changed — see `10_decision_log.md` |
| Results Visualisation Freeze v1.0 | Rebuild `08_results_visualisation.ipynb`'s figures 08c/08d to read exclusively from the canonical MCP v1.0 pipeline, closing item 32 above — the last legacy dependency anywhere in the notebook chain | ✅ Complete (2026-07-06) — `load-data`, `fig-08c`, `fig-08d` rebuilt to read `feature_matrix.parquet`/`reports/model_comparison/`/`reports/baseline/` only; also fixed a previously-unnoticed legacy dependency inside `fig-08a` (Panel 5 silently used the old `load-data` cell's `feat_df`/`TRAIN_CUT`, now automatically canonical since the variable names were preserved). Both rebuilt figures state the RQ3 null result explicitly (no model beats `Baseline_LASSO`) rather than implying a "best model" winner. Notebook executed top-to-bottom with zero errors; a `base_value` SHAP-column bug introduced during the rebuild was caught by visual inspection and fixed before finalising. See `10_decision_log.md` |
| 08 — Results Visualisation | Regenerate synthesis figures from the validated FES v1.1 / MCP v1.0 boundary | ✅ Complete (2026-07-14) — figures 08a–08d regenerated, visually checked, and hash-bound; validation `PASS` |
| 09 — Dissertation Synchronisation | Sync figures/tables/results/methods | ✅ RQ1 BH-FDR/effect-size gate completed 2026-07-15; citation/cross-reference and submission QA remain |

## Project status (as of 2026-07-14)

| Field | Value |
|---|---|
| Project Status | **Methodology Frozen** |
| Governance | **Governance Frozen** |
| Documentation Phase | **Dissertation synchronisation in progress — core rebuilt results incorporated** |

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
| RQ1 — Abnormal returns | ✅ Final RQ1-v1.0 result: 0/5 BH-FDR rejections (min q=0.5810; max |d|=0.239); pooled DoWhy estimate remains positive | General citation/cross-reference QA only |
| RQ2 — Feature importance | ✅ Answered on FES v1.1 — macro/VIX but no event feature in RF top decile; H0 not rejected | Final dissertation citation/cross-reference QA |
| RQ3 — ML vs. baseline | ✅ Answered on FES v1.1 — no candidate clears both corrected legs; H0₃ not rejected | Final dissertation citation/cross-reference QA |

### Top 3 risks right now

1. ~~**🟠 Sentiment cache is 99.2% FinBERT-sourced, contradicting the documented "lexicon is primary" methodology decision**~~ **✅ Resolved (2026-07-06, Sentiment Engine Freeze v1.0).** Project Director ratified FinBERT as the project's official primary sentiment engine, matching the actual pipeline output; documentation corrected across the Research Bible, README, and Notebook 03. No datasets, models, or statistical outputs changed — see `10_decision_log.md`.
2. **🟠 XGBoost overfitting remains uninvestigated at the root-cause level** — reproduced on FES v1.1 (train R² 0.2225 → test R² −0.0067), confirming it is not a superseded-feature-set artefact (`11_limitations.md` L9, `07_model_plan.md`).
3. **🟡 Unrotated API credentials** in `config.yaml` / `notebooks/.env` — gitignored (no commit risk) but not yet rotated.

**Also tracked, not top-3:** QQQ/GLD/TLT scope decision (`10_decision_log.md`, 2026-07-06).

**Resolved since 2026-07-06:** GDELT's 5-day sample (previously confirmed to fall entirely outside the 2015-2025 study window, 2026-05-02→05-06) — full 2015–2025 history (4,018 days) backfilled and integrated 2026-07-13, see the update section at the top of this document and `11_limitations.md` L7.

**Resolved since the last update:** the repository is git-tracked (4 commits as of 2026-07-06, including the full `docs/research_bible/` governance layer) and no nested `.git` directory exists — the previous entry here ("zero git commits + a nested git repository") no longer reflects repository state and has been removed rather than carried forward inaccurately.

### What's genuinely solid right now

- Full pipeline (Phases 1–8) runs end-to-end and produces consistent, cross-checked outputs (`05_data_dictionary.md` row-count sanity checks all pass).
- RQ1 and RQ2 have real, defensible, well-documented evidence (`09_results_log.md`).
- Statistical methodology is planned in detail (`04_statistics_plan.md`); Notebook 07 now applies the frozen Bonferroni-corrected RQ3 comparison rule.
- The Research Bible itself (this folder) is now complete as a documentation layer (2026-07-04).
- SAP v1.0's EDA-stage tests (ADF/KPSS, descriptive stats, Pearson/Spearman correlation, correlation-threshold flagging) are now actually implemented and run against the frozen `master_dataset.parquet`, not just specified (`09_results_log.md`, 2026-07-05).
- `feature_matrix.parquet` is frozen as FES v1.1: 92 features, 2,477 rows, validation `PASS`, and the 27-feature market-only baseline boundary remains contractually enforced.
- RQ1–RQ3 and figures 08a–08d now have current, validated evidence. Final statistical-reporting, dissertation cross-reference, security, and submission QA are the active boundary.

### Immediate next action

**Mission 05-07 Reproducibility Rebuild (complete, 2026-07-06):** `notebooks/05_feature_engineering.ipynb`, `06_model_training.ipynb`, `07_model_evaluation.ipynb` rewritten from their governing contracts (`feature_contract.md`, `baseline_model_specification.md`, `model_contract.md`) rather than the legacy 2026-05-31 code, and executed end-to-end in a clean environment. All three reproduce the already-frozen artefacts exactly (feature values, `Baseline_LASSO` coefficients, and `Event_LASSO`/`XGBoost`/`LightGBM` metrics + DM/z-test statistics all within 1e-6; RQ3 verdict unchanged). This closes the reproducibility gap flagged in the Final Notebook Alignment mission (`future_improvements.md` item 29). `08_results_visualisation.ipynb`'s 08c/08d figures remain legacy (`future_improvements.md` item 32, deliberately out of scope for this mission). Full detail: `10_decision_log.md` (2026-07-06, "Mission 05-07 Reproducibility Rebuild").

**Next controlled action:** complete number-to-source traceability, the remaining scope/security decisions and final citation/cross-reference review. RQ1 BH-FDR/effect-size reporting is complete. Notebook 08 is current visualisation v1.2 and should not be rerun unless an upstream validated artefact changes.

**Mission 08 — Explainability:** extend the SHAP analysis already computed in Mission 07 (`reports/model_comparison/shap_values_*.parquet`) with dependence/interaction plots and partial dependence, per `docs/00_project_workflow.md`'s Phase 8 scope. All three RQs now have a complete, evidence-based answer — Mission 08 deepens the RQ2/RQ3 explainability narrative rather than closing a blocking gap.

**Mission 07C — LightGBM, RQ3 Experiment 3 (complete, 2026-07-06):** LightGBM retrained in isolation (all 95 features, identical split/seed/scaling to `Baseline_LASSO`), tuned via `RandomizedSearchCV` (25 iterations, `TimeSeriesSplit(5)`, full search space persisted), compared descriptively only. Test RMSE 0.009470 (−1.68%), R² 0.032 (vs. −0.002), Dir. Acc. 0.553 (vs. 0.575, worse for the same base-rate reason as 07A), IC 0.145, ROC-AUC 0.544 — pattern closely matches Event_LASSO (07A): modest improvement, mild (not severe) overfitting (train R² 0.119 → test R² 0.032). Standout finding: `mean_car` alone is 36.9% of gain importance, the clearest single-feature evidence of event-derived signal across all three experiments. No significance test run (by design). Full detail: `reports/statistics/07C_lightgbm_summary.md`, `10_decision_log.md`.

**Mission 07B — XGBoost, RQ3 Experiment 2 (complete, 2026-07-06):** XGBoost retrained in isolation (all 95 features, identical split/seed/scaling to `Baseline_LASSO`), tuned via `RandomizedSearchCV` (25 iterations, `TimeSeriesSplit(5)`), compared descriptively only. Test RMSE 0.009881 (+2.58% worse), R² −0.054 (vs. −0.002), Dir. Acc. 0.512 (vs. 0.575, worse), IC 0.073, ROC-AUC 0.517 — worse than `Baseline_LASSO` on every regression metric, with severe train/test overfitting (train R² 0.597 → test R² −0.054), reproducing this project's standing XGBoost-overfitting finding (`11_limitations.md` L9). Numbers do not exactly match the 2026-07-05 Mission 07 XGBoost run (different `RandomizedSearchCV` draw — the original run's exact search space was never persisted, only its winning point) but agree qualitatively. No significance test run (by design). Full detail: `reports/statistics/07B_xgboost_summary.md`, `10_decision_log.md`.

**Mission 07A — Event_LASSO, RQ3 Experiment 1 (complete, 2026-07-06):** `Event_LASSO` retrained in isolation (all 95 features, identical split/CV/seed/scaling to `Baseline_LASSO`), compared descriptively only. Test RMSE 0.009465 (−1.74%), R² 0.033 (vs. −0.002), IC 0.166 (first defined value in the RQ3 line), ROC-AUC 0.575 (vs. 0.500) — better than baseline on most legs; Dir. Acc. 0.564 is below baseline's 0.575 but this is not read as a deficiency given the baseline's mechanical base-rate behaviour. No significance test run (by design). Numbers corroborate, and do not contradict, the existing 2026-07-05 Mission 07 full comparison. Full detail: `reports/statistics/07A_event_lasso_summary.md`, `10_decision_log.md`.

**Mission 07 — Event-Enhanced Models (complete, 2026-07-05):** Event_LASSO, XGBoost, and LightGBM retrained on the full 95-feature `feature_matrix.parquet` (FES v1.0), identical split/`TimeSeriesSplit(5)`/seed 42/scaling to `Baseline_LASSO`. Compared via the frozen Diebold-Mariano + two-proportion z-test + Bonferroni protocol (`statistical_decision_matrix.md` Part K) — **none of the three clears the corrected threshold on either leg; H0₃ is not rejected.** RF importance and SHAP re-run on the new matrix, replacing all legacy `model_features.parquet`-derived values. Full detail: `reports/statistics/07_event_models_summary.md`, `10_decision_log.md`.

**Mission 06 — Baseline Model (complete, 2026-07-05):** `Baseline_LASSO` (27 Market-category features, `TimeSeriesSplit(5)`, seed 42) is trained and frozen — see `model_contract.md` (MCP v1.0), `baseline_model_specification.md`, `baseline_evaluation.md`. Headline result: at the cross-validated alpha, all 27 coefficients shrink to zero — the baseline reduces to a mean predictor, a legitimate null finding consistent with weak-form market efficiency. Not yet joined to `model_comparison.parquet` or compared against event-enhanced models — that is Mission 07.

**Mission 05B — Feature Matrix v1.0 (historical):** the original matrix and its later rebuilt `FAIL`/known-exception state are superseded and archived. Current status is FES v1.1: 92 features, 2,477 rows, validation `PASS`.

---

## Dashboard maintenance rule

If this document and any other Research Bible document disagree on status, the more granular document (e.g. `01_research_questions.md` for RQ status, `13_validation_checklist.md` for a specific checklist item) is authoritative — update this dashboard to match, not the other way around.
