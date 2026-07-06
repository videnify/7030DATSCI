# 13 — Validation Checklist

**Purpose:** The pre-submission checklist across three dimensions — research validity, reproducibility, and repository hygiene — consolidated from every other document in this folder plus the repository audit, so nothing gets missed by relying on memory at submission time.
**Owner:** Ibrahim Haroun.
**Dependencies:** All Research Bible documents; `DATSCI7030_Repository_Audit_Report.ipynb`.
**Update Frequency:** Check off items as they close; re-run the full list before any submission milestone (draft handover, final submission).
**Relation to Dissertation:** Gatekeeper document — nothing should be submitted with unchecked 🔴 items below.

---

## 🔴 Research-validity gates (must close before RQ3 can be reported as answered)

- [ ] Market-only baseline model trained under the identical protocol (`07_model_plan.md`).
- [ ] Baseline added as a row to `data/processed/model_comparison.parquet`.
- [ ] Diebold–Mariano test (RMSE) and two-proportion z-test (directional accuracy) run between each event-informed model and the baseline, Bonferroni-corrected (`04_statistics_plan.md`).
- [ ] `09_results_log.md` updated with the completed RQ3 entry.
- [ ] `01_research_questions.md` RQ3 status field updated from 🔴 to ✅/❌ based on the outcome.
- [ ] XGBoost train/test overfitting gap investigated and root cause documented (`11_limitations.md` L9).

## 🟠 Statistical rigour checks

- [ ] Benjamini-Hochberg FDR correction applied to the 5-event-type CAAR t-tests before reporting any as "significant" (`04_statistics_plan.md`, `11_limitations.md` L3).
- [ ] Effect sizes reported alongside every p-value in Chapter 4.
- [ ] Non-normality of LASSO residuals (Jarque-Bera p≈0.0) explicitly acknowledged wherever LASSO's significance is discussed.
- [ ] Every number quoted in the dissertation traces to a `09_results_log.md` entry with a named source file.

## 🟠 Scope decisions that must close one way or the other

- [ ] QQQ/GLD/TLT: either scoped into a cross-asset analysis or formally dropped and documented (`10_decision_log.md`, `11_limitations.md` L8).
- [ ] GDELT: either full 2015–2025 series backfilled, or GDELT-derived features formally excluded from any "final" result (`11_limitations.md` L7).
- [ ] 8-notebook vs. 10-phase pipeline naming decision formally ratified in `docs/00_project_workflow.md` (currently proposed in `10_decision_log.md` but not closed).

## 🟡 Documentation completeness (repository quality, not research validity)

- [ ] `data/raw/README.md`, `data/processed/README.md`, `data/external/README.md` regenerated to match `05_data_dictionary.md`.
- [ ] Missing `README.md` added to: `notebooks/`, `src/`, `scripts/`, `tests/`, `reports/`, `reports/figures/`, `reports/dissertation/`, `data/` (top-level), `docs/` (top-level).
- [ ] `src/*.py` docstring headers include Author, Version, and Dependencies (currently only Description + Usage).
- [ ] `data/raw/app_csv/` documented as scrape cache, not undocumented clutter.

## 🟡 Repository hygiene (from `DATSCI7030_Repository_Audit_Report.ipynb`)

- [ ] Nested git repository at `7030DATSCI/.git` removed before the first real commit.
- [ ] API keys/tokens rotated (`config.yaml`, `notebooks/.env`).
- [ ] Secrets stripped from `config.yaml` in favour of environment variables; `.env.example` added.
- [ ] Initial git commit made; remote configured; pushed off-machine.
- [ ] Four duplicate "Data Collection Report" `.docx` files in `reports/` consolidated to one (or folded into the README/dissertation).
- [ ] `.DS_Store` / `.ipynb_checkpoints` cleanup completed where filesystem permissions allow.

## ✅ Already verified (2026-07-04) — do not re-litigate unless something changes

- [x] `reports/dissertation/` holds a single canonical file.
- [x] `notebooks/01_data_collection.ipynb` is the single canonical Phase-1 notebook; the duplicate is archived (gitignored).
- [x] `.gitignore` correctly excludes all data/model/secret paths (verified via `git check-ignore -v`).

---

## Traceability gate (run last, before final submission)

- [ ] Every notebook, figure, table, and statistical test in the dissertation appears in `15_traceability_matrix.md` against at least one of RQ1/RQ2/RQ3.
- [ ] Nothing in `15_traceability_matrix.md` is marked "orphaned" (traceable to no RQ) without an explicit decision in `10_decision_log.md` explaining why it's retained anyway.
