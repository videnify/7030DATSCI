# Repository Pre-Freeze Baseline — 2026-07-16

**Purpose:** Read-only snapshot of repository state, captured before any cleanup, archival, or documentation action in the 2026-07-16 finalisation pass. No file was created, moved, or deleted while gathering this snapshot (this report and the accompanying `PROTECTED_FILE_HASHES_2026-07-16.txt` are the only writes, and both are additive).

---

## 1. Repository root

`/Users/videnify/Devops/7030DATSCI-Data-Science-Project/7030DATSCI`

## 2. Current branch

`main`

## 3. Current remote URLs

```
origin  git@github.com:videnify/7030DATSCI.git (fetch)
origin  git@github.com:videnify/7030DATSCI.git (push)
```

## 4. Current HEAD commit

`ddc86cdca7bb349bce50c773ad17c304336103be` — 2026-07-15 14:37:27 +0100 — "Technically complete, final document review required"

## 5. Git status (at snapshot time)

Branch up to date with `origin/main`. Working tree has **no modified tracked files**, only untracked files (see §6).

## 6. Untracked files

```
data/Equation.png
reports/dissertation/2026-07-16-7030DATSCI.pdf
reports/dissertation/2026-07-16-7030DATSCI_PREVIEW_LibreOffice_render.pdf
reports/dissertation/7030DATSCI_SUBMISSION_FINAL_2026-07-15.pdf
reports/dissertation/SUBMISSION_QA_CHANGELOG_2026-07-15.md
reports/figures/A7_causal_dag.png
reports/figures/A8_residual_diagnostics.png
reports/figures/A9_research_governance.png
reports/stakeholder/
scripts/generate_appendix_a7_causal_dag.py
scripts/generate_appendix_a8_residual_diagnostics.py
```

Note: `reports/dissertation/2026-07-16-7030DATSCI.docx` does **not** appear above because `*.docx` is globally gitignored (see §13) — it is untracked-but-ignored, not untracked-and-visible. Its content is nonetheless the accepted, protected dissertation source for this task.

**Observation (not an issue):** the dissertation DOCX and PDF were both re-saved after my previous session ended (DOCX mtime 19:20:22, PDF mtime 19:20:13, both later than my last edit at 18:42). This is consistent with the user performing the Word field-refresh and native PDF re-export I recommended at the end of that session. The hashes recorded in `PROTECTED_FILE_HASHES_2026-07-16.txt` reflect this current, user-accepted state and are the baseline this freeze protects going forward.

## 7. Modified (tracked) files

None.

## 8. Ignored files

79 ignored paths at snapshot time (via `git status --ignored --short`), dominated by: all of `data/raw/`, `data/processed/` (parquet/JSON artefacts), `models/` (joblib + metadata), `reports/dissertation/*.docx`, `reports/**/archive/`, `reports/model_comparison/*.parquet`, `reports/tables/`, all `.ipynb_checkpoints/`, `.DS_Store`, `__pycache__/`, `.pytest_cache/`, `notebooks/.env`, `config.yaml`, `notebooks/archive/`. Full list available via `git status --ignored --short`.

## 9. Repository size

- Working tree (excl. `.git`): **262 MB**
- `.git` directory: **75 MB**

## 10. Largest 30 files (working tree)

| Size | Path |
|---|---|
| 75 MB | `models/event/random_forest_importance_tool.joblib` |
| 10.1 MB | `reports/dissertation/archive/2026-07-16-7030DATSCI_PREEDIT_BACKUP_20260716174628.docx` |
| 6.7 MB | `reports/dissertation/2026-07-16-7030DATSCI.pdf` |
| 5.1 MB | `reports/dissertation/2026-07-16-7030DATSCI.docx` |
| 4.3 MB | `reports/dissertation/archive/pre_2026-07-14_cleanup/7030DATSCI-00_07_2026.docx` |
| 4.3 MB | `reports/dissertation/archive/pre_fes_v1_1_doc_sync_2026-07-14/7030DATSCI-14_07_2026.docx` |
| 4.3 MB | `reports/dissertation/archive/pre_2026-07-14_cleanup/7030DATSCI-11_07_2026.docx` |
| 4.1 MB | `reports/dissertation/7030DATSCI_SUBMISSION_FINAL_2026-07-15.docx` |
| 3.9 MB | `reports/dissertation/archive/pre_2026-07-14_cleanup/7030DATSCI_Reference_Audit_2026-07-08.docx` |
| 3.7 MB | `reports/dissertation/archive/7030DATSCI_FINAL_2026-07-15_QA_PREEDIT_BACKUP_20260715144318.docx` |
| 3.7 MB | `reports/dissertation/archive/7030DATSCI-15_07_2026_PREEDIT_BACKUP_20260715142730.docx` |
| 3.7 MB | `reports/dissertation/7030DATSCI_FINAL_2026-07-15.docx` |
| 3.7 MB | `reports/dissertation/7030DATSCI-15_07_2026.docx` |
| 3.3 MB | `reports/08_05_2026_DATSCI7030_Data_Collection_Report.pdf` |
| 3.2 MB | `data/Equation.png` |
| 3.0 MB | `reports/dissertation/2026-07-16-7030DATSCI_PREVIEW_LibreOffice_render.pdf` |
| 3.0 MB | `notebooks/archive/02_eda.ipynb` |
| 2.5 MB | `reports/08_05_2026_DATSCI7030_Data_Collection_Report.docx` |
| 2.5 MB | `reports/dissertation/7030DATSCI_SUBMISSION_FINAL_2026-07-15.pdf` |
| 2.1 MB | `notebooks/08_results_visualisation.ipynb` |
| 2.0 MB | `notebooks/.ipynb_checkpoints/08_results_visualisation-checkpoint.ipynb` |
| 1.7 MB | `notebooks/02_eda.ipynb` |
| 1.0 MB | `reports/figures/08d_full_dashboard.png` |
| 0.9 MB | `notebooks/archive/__01_data_collection__.ipynb` |
| 0.9 MB | `notebooks/archive/.ipynb_checkpoints/__01_data_collection__-checkpoint.ipynb` |
| 0.85 MB | `notebooks/archive/__03_event_detection__.ipynb` |
| 0.8 MB | `notebooks/archive/03_event_detection.ipynb` |
| 0.8 MB | `reports/figures/archive/pre_fes_v1_1_notebook08_2026-07-14/08d_full_dashboard.png` |
| 0.8 MB | `notebooks/04_causal_analysis.ipynb` |
| 0.72 MB | `notebooks/.ipynb_checkpoints/04_causal_analysis-checkpoint.ipynb` |

None of these exceed GitHub's 100 MB hard limit or the 50 MB soft-warning limit **as tracked objects** — and in practice none of the largest files (models, dissertation binaries, notebook checkpoints) are tracked at all (see §13).

## 11. Total file count

465 files in the working tree (excluding `.git`); 143 tracked by Git.

## 12. Directory tree (depth 3)

```
.cache/yfinance
.claude/
.ipynb_checkpoints/
.pytest_cache/v/cache
data/{external,interim,processed/archive,raw/app_csv}/ (+ .ipynb_checkpoints in each)
docs/{architecture/archive,research_bible,stakeholder_report}/ (+ .ipynb_checkpoints)
logs/
models/{archive/{pre_2026-07-13_pipeline_rebuild,pre_fes_v1_1_notebook06_2026-07-14,pre_fes_v1_1_notebook07_2026-07-14},baseline,event}/
notebooks/{.ipynb_checkpoints,archive/.ipynb_checkpoints}/
reports/{baseline/archive,dissertation/archive,figures/{.ipynb_checkpoints,archive},model_comparison/archive,stakeholder,tables}/
scripts/
src/__pycache__/
tests/{.ipynb_checkpoints,__pycache__}/
```

## 13. `.gitignore` contents (summary)

Already thorough and repo-appropriate: ignores Python caches, `.ipynb_checkpoints/`, `.cache/`, all of `data/{raw,processed,interim,external}/*` (contents only — README/`.gitkeep` negated back in), a belt-and-braces blanket ignore on `*.csv|*.parquet|*.feather|*.h5|*.hdf5|*.pkl|*.pickle|*.xlsx|*.xls|*.docx|*.doc`, `models/*` (except README/`.gitkeep`), `*.joblib`, `notebooks/archive/`, secrets patterns (`.env`, `*.key`, `*.pem`, `*_secret*`, `*_private*`, `*credentials*`), OS files, Office lock files (`~$*`), IDE dirs, `reports/**/archive/`, and `reports/*.docx|*.pdf`. No changes identified as necessary in Phase 12.

## 14. Existing tags

None.

## 15. Existing release or freeze documents

- `docs/research_bible/00_project_freeze.md` — the existing **methodology governance freeze** (frozen 2026-07-06, RQ1 reporting boundary amended 2026-07-15). This is a different, earlier freeze than the one this task creates: it freezes the *scientific methodology* (datasets, contracts, models, statistics). This task's new `FINAL_PROJECT_FREEZE_2026-07-16.md` freezes the *submitted repository state* for the assessment-feedback waiting period, and explicitly defers to and cross-references this document rather than duplicating or superseding it.
- `docs/research_bible/14_project_dashboard.md` — actively maintained session-by-session status dashboard, last entry 2026-07-15.
- `docs/research_bible/10_decision_log.md` — append-only decision log, last entry 2026-07-15 (live execution/verification pass).

## 16. Existing backups and archives

Already-established archive locations (all pre-dating this task):
- `reports/dissertation/archive/` (+ two dated sub-folders: `pre_2026-07-14_cleanup/`, `pre_fes_v1_1_doc_sync_2026-07-14/`) — prior dissertation DOCX versions and pre-edit backups.
- `data/processed/archive/` — superseded processed artefacts.
- `models/archive/` (3 dated sub-folders) — superseded model artefacts.
- `notebooks/archive/` (+ its own `.ipynb_checkpoints/`) — superseded/duplicate notebook drafts, gitignored (local-reference-only by design).
- `reports/figures/archive/`, `reports/baseline/archive/`, `reports/model_comparison/archive/` — superseded figures/reports.
- `docs/architecture/archive/` — superseded architecture SVGs (11 files, already documented in `docs/architecture/README.md` as "none should be cited").

**This confirms a single, consistent, pre-existing archive convention (`<dir>/archive/[dated-subfolder]/`) is already in use throughout the repository.** Phase 4 of this task will reuse this convention exactly, not introduce a competing one.

## 17. Existing temporary, checkpoint and cache directories

`.ipynb_checkpoints/` (11 locations), `.DS_Store` (8 files), `__pycache__/` (2 locations: `src/`, `tests/`), `.pytest_cache/` (1, root), `.cache/yfinance/` (1). None of these are Git-tracked (confirmed via `git ls-files | grep`). All are safe, zero-risk deletion candidates addressed in Phase 3.
