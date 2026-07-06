# Future Improvements

**Purpose:** Non-critical improvements, technical debt, and refactoring ideas identified during repository maintenance sprints. Nothing here is to be implemented before dissertation submission — this is a parking lot, not a task list for the current work.
**Owner:** Ibrahim Haroun.
**Dependencies:** `10_decision_log.md` (promote an item here to a decision only when actually scheduled), `15_traceability_matrix.md`, `14_project_dashboard.md`.
**Update Frequency:** Append during any audit/maintenance sprint; do not reorder or delete past entries — mark them done in place instead.
**Relation to Dissertation:** None directly — this document exists precisely to keep post-submission ideas out of the dissertation-critical path.

---

## Repository governance

1. **Track the Research Bible in git.** As of this sprint, all 32 files under `docs/research_bible/` (including `dataset_contract.md`, `feature_contract.md`, `10_decision_log.md`, `15_traceability_matrix.md`) are untracked — 0 of 32 committed. This is the project's entire governance layer sitting outside version control. Commit it once the current uncommitted notebook changes are reviewed.
2. **Reconcile `14_project_dashboard.md`'s stated risks with current repo state.** The dashboard lists "zero git commits + a nested git repository" as an open risk, but the repo has 3 commits and no nested `.git` was found on this sprint's inspection. Either the risk was already resolved and the dashboard wasn't updated, or it refers to a state that no longer reproduces — needs a one-line reconciliation.
3. **Remove the stale `.git/index.lock`.** A zero-byte `index.lock` exists in `.git/` dated to this session. If no git process is actually running, delete it — otherwise any `git add`/`commit` will fail with "Unable to create index.lock: File exists."
4. **Rotate credentials referenced in `config.yaml` / `notebooks/.env`.** Already flagged as a known risk in the dashboard; gitignored so no exposure via git, but rotation is still outstanding.
5. **Decide the fate of QQQ/GLD/TLT.** `15_traceability_matrix.md` already flags these as orphaned (collected, never used in any RQ1–RQ3 result). Either scope them into an analysis or drop them from `master_dataset.parquet`'s next version — do not carry them forward silently into the dissertation write-up.

## Documentation

6. **Update `models/README.md`.** It still describes the pre-Mission-06/07 flat layout (`lasso.pkl`, `xgboost.json`, `lightgbm.txt` at `models/` root) and says "layout is intentionally flat" — but `models/baseline/` and `models/event/` subfolders now exist with the current artefacts. The README was not updated when the split happened.
7. **Regenerate `data/raw/README.md` and `data/processed/README.md`.** `05_data_dictionary.md` already documents that these describe files that don't exist on disk (`fred_macro.parquet`, `gdelt_events.parquet`, `features.parquet`, `target.parquet`). Low priority since `05_data_dictionary.md` is authoritative in the meantime, but the drift should eventually be closed so the folder READMEs aren't misleading on their own.
8. **Add missing per-folder READMEs.** `src/`, `tests/`, `scripts/`, `reports/` (root), `reports/baseline/`, `reports/model_comparison/`, `reports/dissertation/`, `models/baseline/`, `models/event/`, and `notebooks/archive/` have no `README.md`, unlike the rest of the tree. Not urgent, but inconsistent with the documentation standard applied elsewhere.
9. **Fix the `07_machine_learning.ipynb` cross-reference in the root `README.md`** (line 44) — the actual notebook is `07_model_evaluation.ipynb`; the reference to the 10-phase spec's original name is explained in context but reads as a broken link on a skim.
10. **Reconcile `notebooks/01_data_collection.ipynb`'s macro-indicator markdown/code with the frozen schema.** Cell 14/15 still describe `cpi_index`, `unemployment_rate`, `cpi_yoy`, and a "10Y–2Y spread" — none of which match the actual cached/frozen column names (`cpi`, `unemployment`, `yield_spread`, and no `cpi_yoy` anywhere in the pipeline). Documented in detail in the Mission 03 data-provenance audit; carried here as the actionable follow-up.

## Architecture

11. **Add a `config/` folder, or explicitly document why a single `config.yaml` is sufficient.** The agreed architecture (both the project brief and repository-maintenance instructions) lists a `config/` directory; the repo currently has one root-level `config.yaml` only. Probably fine for a project this size — just note the deliberate deviation somewhere so it doesn't look like an oversight.
12. **Archive the legacy top-level model artefacts.** `models/lasso.pkl`, `models/xgboost.json`, `models/xgboost_params.json`, `models/lightgbm.txt`, `models/lightgbm_params.json`, `models/model_metadata.json`, `models/residual_diagnostics.json` predate the `models/baseline/` / `models/event/` split and are superseded per `15_traceability_matrix.md`. Move to `models/archive/` (not delete) once confirmed nothing still reads them directly.
13. **Consider a numbered-prefix rename for `reports/08_05_2026_DATSCI7030_Data_Collection_Report.{pdf,docx}`.** Every other report/figure/table in `reports/` follows a `NN_description` numbering convention; this pair uses a `DD_MM_YYYY_...` convention instead, which stands out.

## Testing

14. **Expand `tests/` coverage.** Only `test_event_study.py` and `test_features.py` exist; `src/causal_engine.py`, `src/evaluation.py`, `src/models.py`, and `src/data_collector.py` have no dedicated test module. Not blocking for a dissertation, but worth a pass if time allows post-submission.

---

## Explicitly deferred (do not action before submission)

- Any change to `master_dataset.parquet`, `feature_matrix.parquet`, SAP v1.0, FES v1.0, or MCP v1.0.
- Renaming or moving any file under `data/raw/` or `data/processed/`.
- Rerunning, retraining, or re-deriving any frozen/versioned artefact.
- QQQ/GLD/TLT scoping decision (item 5) — requires a `10_decision_log.md` entry and Project Director sign-off before it touches the frozen dataset.
