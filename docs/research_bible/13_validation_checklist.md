# 13 — Validation Checklist

**Purpose:** The pre-submission checklist across three dimensions — research validity, reproducibility, and repository hygiene — consolidated from every other document in this folder plus the repository audit, so nothing gets missed by relying on memory at submission time.
**Owner:** Ibrahim Haroun.
**Dependencies:** All Research Bible documents; `DATSCI7030_Repository_Audit_Report.ipynb`.
**Update Frequency:** Check off items as they close; re-run the full list before any submission milestone (draft handover, final submission).
**Relation to Dissertation:** Gatekeeper document — nothing should be submitted with unchecked 🔴 items below.

---

## Research-validity gates

- [x] Market-only `Baseline_LASSO` v1.1 trained under the identical protocol and validated against FES v1.1 (`07_model_plan.md`, `baseline_model_validation.json`).
- [x] Baseline included in the canonical `reports/model_comparison/model_comparison.parquet`; the legacy `data/processed/model_comparison.parquet` is deliberately not overwritten.
- [x] Diebold–Mariano test (RMSE) and two-proportion z-test (directional accuracy) run between each event-informed model and the baseline, Bonferroni-corrected (`04_statistics_plan.md`).
- [x] `09_results_log.md` updated with the completed FES v1.1 RQ2/RQ3 entry.
- [x] `01_research_questions.md` RQ2/RQ3 statuses updated to the current null findings.
- [ ] XGBoost train/test overfitting gap investigated and root cause documented (`11_limitations.md` L9).

## 🟠 Statistical rigour checks

- [x] Benjamini-Hochberg FDR correction applied to the five event-type mean-CAR tests; `rq1_reporting_validation.json` reports `PASS`, with 0/5 rejected and minimum q=0.5810.
- [x] RQ1 event-type mean-CAR 95% intervals and Cohen's d values persisted and inserted into Chapter 4; remaining p-value/effect-size checks concern final proofreading, not a missing analysis.
- [ ] Non-normality of LASSO residuals (Jarque-Bera p≈0.0) explicitly acknowledged wherever LASSO's significance is discussed.
- [ ] Every number quoted in the dissertation traces to a `09_results_log.md` entry with a named source file.

## 🟠 Scope decisions that must close one way or the other

- [ ] QQQ/GLD/TLT: either scoped into a cross-asset analysis or formally dropped and documented (`10_decision_log.md`, `11_limitations.md` L8).
- [x] GDELT: full 2015–2025 series backfilled and formally disclosed as excluded from the frozen DoWhy DAG, FES v1.1, and all current RQ1–RQ3 results (`11_limitations.md` L7).
- [x] 8-notebook vs. 10-phase naming decision ratified in `docs/00_project_workflow.md`; the eight notebooks are the frozen implementation of the ten-phase conceptual workflow.

## 🟡 Documentation completeness (repository quality, not research validity)

- [x] `data/raw/README.md`, `data/processed/README.md`, `data/external/README.md` synchronized to the current files and `05_data_dictionary.md` on 2026-07-14.
- [x] Required folder-level README files are present across notebooks, source, scripts, tests, reports, figures, dissertation, data, and docs.
- [ ] `src/*.py` docstring headers include Author, Version, and Dependencies (currently only Description + Usage).
- [x] `data/raw/app_csv/` documented as the raw APP scrape cache feeding the canonical raw/economic parquet files.

## 🟡 Repository hygiene (from `DATSCI7030_Repository_Audit_Report.ipynb`)

- [x] No nested `7030DATSCI/.git` exists; the repository has one top-level Git boundary.
- [ ] API keys/tokens rotated (`config.yaml`, `notebooks/.env`).
- [ ] Secrets stripped from `config.yaml` in favour of environment variables; `.env.example` added.
- [x] Repository has commit history; `origin` is configured and `main` matches `origin/main` at the start of the 2026-07-14 documentation pass.
- [x] Duplicate Data Collection Report files consolidated; the one remaining early report is explicitly labelled legacy in `reports/README.md`.
- [ ] `.DS_Store` / `.ipynb_checkpoints` cleanup completed where filesystem permissions allow.

## ✅ Already verified (2026-07-04) — do not re-litigate unless something changes

- [x] `reports/dissertation/` holds a single canonical file.
- [x] `notebooks/01_data_collection.ipynb` is the single canonical Phase-1 notebook; the duplicate is archived (gitignored).
- [x] `.gitignore` correctly excludes all data/model/secret paths (verified via `git check-ignore -v`).
- [x] FES v1.0 `FAIL` and its SHA-256-bound `ACCEPTED_WITH_KNOWN_EXCEPTION` disposition preserved in the pre-FES-v1.1 archive as historical evidence.
- [x] FES v1.1 frozen 2026-07-14: 2,477 rows, 92 features, direct health/labour/other occurrence flags, no duplicate/missing/constant/near-zero-variance/leakage/source failures, validation `PASS`, matrix SHA-256 `127a6dbe4b83e59c873dfdf7502060aab115037732bbb723f9d489c6b85dc383`.
- [x] Notebooks 06–08 rerun in order; baseline, model, RQ2/RQ3, and figure artefacts are re-bound to FES v1.1 with validation `PASS`. The canonical dissertation draft was synchronized to these results on 2026-07-14; final statistical-reporting and cross-reference checks remain separately listed below.
- [x] Dataset v1.2 frozen 2026-07-14: 2,765 × 34, only three intended columns added, all v1.1 values preserved, validation `PASS`, SHA-256 bound, and non-trading-date occurrence counts disclosed (`master_dataset_validation.json`, `11_limitations.md` L17).

---

## Traceability gate (run last, before final submission)

- [ ] Every notebook, figure, table, and statistical test in the dissertation appears in `15_traceability_matrix.md` against at least one of RQ1/RQ2/RQ3.
- [ ] Nothing in `15_traceability_matrix.md` is marked "orphaned" (traceable to no RQ) without an explicit decision in `10_decision_log.md` explaining why it's retained anyway.
