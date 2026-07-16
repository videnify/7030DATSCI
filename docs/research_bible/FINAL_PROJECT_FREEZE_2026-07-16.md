# Final Project Freeze — 2026-07-16

**Purpose:** The submission-state freeze declaration. This is a different, later freeze than `00_project_freeze.md` (the 2026-07-06 **methodology** governance freeze, amended 2026-07-15). That document freezes the *scientific methodology* — datasets, contracts, models, statistics — and remains the authoritative reference for what those artefacts are and why they are frozen. This document freezes the **submitted repository state as a whole**, now that the dissertation itself has been accepted, for the period while assessment feedback is awaited. It does not restate or supersede `00_project_freeze.md`; it depends on it.

**Owner:** Ibrahim Haroun, acting as Project Director.

---

> "This repository is frozen as the submitted MSc Data Science project state. No analytical, methodological or evidential changes should be made until assessment feedback is received. Any post-feedback change must begin with a new dated decision-log entry, a new version identifier and a documented impact assessment."

---

## 1. Freeze date

**2026-07-16**

## 2. Authoritative dissertation files

| File | Role | SHA-256 |
|---|---|---|
| `reports/dissertation/2026-07-16-7030DATSCI.docx` | Accepted dissertation source | `a46c411da588a77a8293e4bacb2d16dc988c6d7ec8882e22eaf35a7e3b630747` |
| `reports/dissertation/2026-07-16-7030DATSCI.pdf` | Accepted dissertation PDF (native Word export, fields refreshed) | `4a8ce3cfc9eb49c400bc2ea8d08bb856d28bd36f33abd2c63214a86d231df1bf` |
| `reports/dissertation/2026-07-16-7030DATSCI_Generative_AI_Statement.docx` | Current AI-use declaration, revised 2026-07-16 to disclose this pass | `c5ca44f8a2762ef0ce28c955f7e8cf5625589ad7219abcd4b4148d6c4fe7fbdf` |

None of these files are Git-tracked (`*.docx`/`reports/**/*.pdf` are gitignored repository-wide); these hashes are the integrity record. Full hash list, including every earlier archived version: `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`.

**Resolved by owner instruction, 2026-07-16 (after this freeze document was first drafted):** the Generative AI Statement has been revised to disclose the dissertation finalisation and repository-freeze passes and re-dated to match the accepted dissertation (superseded copy archived); `data/Equation.png` is retained and tracked at the owner's explicit instruction as a supplementary equation-reference image, not pipeline data (see `data/README.md`).

## 3. Authoritative notebook set

The eight canonical, executed notebooks — `notebooks/01_data_collection.ipynb` through `notebooks/08_results_visualisation.ipynb`. Hashes recorded in `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`. All eight re-confirmed valid JSON on 2026-07-16. See `notebooks/README.md` for frozen-snapshot behaviour and the external-data warning.

## 4. Authoritative dataset contract

`docs/research_bible/dataset_contract.md` + `dataset_version.md` (Dataset v1.2, `data/processed/master_dataset.parquet`, 2,765 × 34, SHA-256 `142145722faff37156c6606801ae82d56843118b486942b050629b0472647819`).

## 5. Authoritative feature contract

`docs/research_bible/feature_contract.md` (FES v1.1, `data/processed/feature_matrix.parquet`, 92 features / 2,477 rows / 1,727 train / 750 test, SHA-256 `127a6dbe4b83e59c873dfdf7502060aab115037732bbb723f9d489c6b85dc383`).

## 6. Authoritative model contract

`docs/research_bible/model_contract.md` (MCP v1.0): market-only `Baseline_LASSO` (27 market features) vs. event-enhanced `Event_LASSO`/XGBoost/LightGBM (92 features), Bonferroni-corrected two-leg promotion protocol (α = 0.05/3 ≈ 0.0167).

## 7. Authoritative results

`reports/model_comparison/model_comparison.parquet` and `statistical_tests.json`; `data/processed/car_results.parquet`, `causal_estimates.parquet`, `causal_overall_estimate.json`, `event_type_statistics.parquet`. All hash-recorded in `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`.

## 8. Final RQ1–RQ3 conclusions (frozen, unchanged by this or the prior dissertation-finalisation pass)

- **RQ1 — qualified:** 0/5 event-type mean-CAR nulls rejected after BH-FDR correction (minimum q = 0.5810; maximum |Cohen's d| = 0.239); the separate pooled DoWhy estimate is +0.005601 (95% CI [+0.002295, +0.008907], p = 0.0009, n = 2,762), conditional on the frozen DAG and no-unmeasured-confounding assumption.
- **RQ2 — null:** Random Forest importance is dominated by market/macro features; no event feature in the top ten.
- **RQ3 — null:** the market-only LASSO baseline and event-enhanced LASSO are identical constant predictors; XGBoost and LightGBM are worse on RMSE and directional accuracy; no candidate clears the Bonferroni-corrected two-leg promotion rule.

## 9. Protected artefacts and hashes

Full list (dissertation, core processed artefacts, model artefacts, predictions, SHAP outputs, model comparison/statistics, validation JSON, numbered dissertation figures, eight notebooks, Research Bible contracts, canonical architecture SVGs, tests): `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt` (computed before this cleanup pass) and `reports/finalisation/project_freeze_manifest_2026-07-16.json` (machine-readable, re-verified after cleanup — every hash identical, zero drift).

## 10. Validation commands and results

```bash
python -m pytest tests/ -v          # 18 passed, 0 failed (confirmed 2026-07-16, /usr/local/bin/python3)
python -m py_compile src/*.py scripts/*.py tests/*.py   # clean, no errors
```
All eight notebooks: valid JSON (confirmed 2026-07-16). All architecture SVGs and all processed/report JSON files: well-formed (confirmed 2026-07-16). Every protected-artefact SHA-256: identical before and after this cleanup pass (confirmed 2026-07-16).

## 11. Known limitations

Unchanged from the dissertation's own Limitations section: title-only APP sentiment (92.4% neutral label share), clustered events (BH-FDR controls the five-event-type family but not within-type temporal dependence), observational causal identification (no unmeasured-confounding cannot be proven), heavy-tailed residuals, a single asset (SPY) and a single chronological test period. See `docs/research_bible/11_limitations.md` for the full, itemised register.

## 12. Files excluded from GitHub

All raw/interim/processed data (`data/*`), trained model binaries (`models/*`, `*.joblib`), the dissertation and other Office binaries (`*.docx`, `*.pdf` under `reports/`), `reports/**/archive/`, `reports/tables/`, `notebooks/archive/`, and standard OS/editor/cache junk. Full policy: root `README.md`'s "Large-file exclusions" section and `.gitignore`.

## 13. Open future-improvement items

Tracked exclusively in `docs/research_bible/future_improvements.md` (not restated here) — includes cluster-aware event-study inference, full-text APP sentiment scoring, external asset/period validation, and the items already logged from the 2026-07-15 traceability audit (items 33–36). None of these are in scope until a formal reopening (§15 below).

## 14. Reopening conditions

This freeze is lifted only by:
1. Receipt of formal assessment feedback requiring a change, **or**
2. An explicit, dated Project Director decision to resume work for a distinct, non-assessment purpose (e.g. publication, portfolio use).

Either path must begin with a new dated `docs/research_bible/10_decision_log.md` entry stating what changed, why, and its impact on RQ1–RQ3 and every artefact hash in §9 above, following the discipline already codified in `00_project_freeze.md` §10 (Documentation Impact and Date Maintenance).

## 15. Assessment-feedback policy

Until feedback is received: no dataset, feature, model, statistic, or RQ1–RQ3 conclusion may change; documentation clarifications and typo fixes remain permitted (per `00_project_freeze.md` §6) but must not alter any reported number or claim. On receipt of feedback, changes should be scoped as narrowly as possible to what the feedback actually requires, with the existing frozen state (this document, §9's hashes) as the diff baseline.

---

*This document depends on, and does not restate, `00_project_freeze.md` (methodology freeze), `docs/research_bible/10_decision_log.md`'s 2026-07-16 entry (full technical record of this cleanup pass), and `reports/finalisation/project_freeze_manifest_2026-07-16.json` (machine-readable manifest).*
