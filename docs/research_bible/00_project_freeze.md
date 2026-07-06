# 00 — Project Governance Freeze

**Purpose:** The master governance declaration for DATSCI7030. This is not a methodology document — it does not describe *how* anything was built (that is `03_methodology.md`'s job) or *what* is in any file (that is `05_data_dictionary.md`/`06_feature_dictionary.md`'s job). It states, in one place, what is frozen, when, why, what may still change, and what may not. Read this document first, before any other file in this repository.
**Owner:** Ibrahim Haroun, acting as Project Director.
**Dependencies:** This document references every other governance artefact below rather than duplicating their content — `dataset_version.md`, `dataset_contract.md`, `statistical_analysis_plan.md` (+ SAP suite), `feature_contract.md`, `model_contract.md`, `10_decision_log.md` (Sentiment Engine Freeze v1.0 entry), `docs/architecture/README.md`, and every numbered document 01–15.
**Update Frequency:** Frozen. A future update to this document itself constitutes a new governance milestone and requires a dated `10_decision_log.md` entry — it should not be silently edited.
**Relation to Dissertation:** Supports the reproducibility appendix and the framing of Chapter 3 (Methodology) as a description of a *completed, frozen* pipeline rather than work in progress.

---

## Section 1 — Project Governance Freeze

| Field | Value |
|---|---|
| Project | 7030DATSCI |
| Title | Causal Event-Driven Market Impact Modelling |
| Status | **Methodology Frozen** |
| Research Status | **Analysis Complete** |
| Documentation Phase | **Dissertation Phase** |
| Freeze Date | 2026-07-06 |

**What is frozen:** every dataset, contract, statistical plan, feature specification, model contract, and sentiment-engine decision listed in Section 3 below.
**When:** progressively between 2026-07-04 and 2026-07-06, culminating in this document.
**Why:** RQ1–RQ3 (`01_research_questions.md`) have each been answered at least once end-to-end (event study + causal estimate for RQ1, RF/SHAP importance for RQ2, baseline-vs-event-enhanced comparison for RQ3 — H0₃ not rejected). Continuing to change frozen artefacts after this point would invalidate already-reported, cross-referenced results and put the dissertation's internal consistency at risk. Freezing converts the project from an active research/engineering exercise into a fixed, citable body of work that the dissertation describes.
**What changes are still allowed:** Section 6. **What is prohibited:** Section 7.

---

## Section 2 — Governance Timeline

The freeze order, each link built on the one before it:

```
Dataset Version 1.0                    (2026-07-04 — master_dataset.parquet frozen)
        ↓
Dataset Contract                       (2026-07-04 — consumption rules for master_dataset.parquet)
        ↓
Statistical Analysis Plan (SAP v1.0)   (2026-07-04 — global statistical policy freeze)
        ↓
Feature Engineering Specification      (2026-07-05 — FES v1.0, feature_matrix.parquet frozen)
        ↓
Model Contract Protocol (MCP v1.0)     (2026-07-05 — approved models, promotion criteria)
        ↓
Sentiment Engine Freeze (SEF v1.0)     (2026-07-06 — FinBERT ratified as primary sentiment engine)
        ↓
Research Bible Complete                (2026-07-06 — all 16 numbered documents + SAP/FES/MCP suite current)
        ↓
Architecture Complete                  (2026-07-06 — canonical SVG set finalised)
        ↓
Project Governance Freeze              (2026-07-06 — this document)
```

Each stage is a dependency of the one below it — for example, SEF v1.0 could only be declared once the Dataset, SAP, FES, and MCP freezes had already fixed what "the pipeline" means, giving the Sentiment Engine decision something stable to be consistent with.

---

## Section 3 — Official Frozen Artefacts

| Category | Artefact(s) |
|---|---|
| **Dataset** | `data/processed/master_dataset.parquet`, `feature_matrix.parquet`, `car_results.parquet`, `events_tagged.parquet`, `daily_sentiment.parquet` — see `dataset_version.md`, `dataset_contract.md`, `feature_contract.md`, `05_data_dictionary.md` |
| **Statistical Plan** | SAP v1.0 — `statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`, `statistical_reporting_guidelines.md` |
| **Feature Engineering** | FES v1.0 — `feature_contract.md`, `06_feature_dictionary.md` |
| **Model Contract** | MCP v1.0 — `model_contract.md`, `07_model_plan.md`, `baseline_model_specification.md`, `baseline_evaluation.md` |
| **Sentiment Engine** | SEF v1.0 — FinBERT is the official primary sentiment engine; lexicon scorer is fallback/historical only. See `10_decision_log.md` (2026-07-06 entry) |
| **Architecture** | Canonical SVG set (6 files): `project_pipeline.svg`, `data_lineage.svg`, `research_governance.svg`, `rq_traceability.svg`, `modelling_flow.svg`, `car_formula.svg` — see `docs/architecture/README.md` |
| **Research Bible** | Current version, this folder in full (documents 00–15 + SAP/FES/MCP/SEF suite) |

None of the above may be regenerated, retrained, or re-derived as part of routine repository maintenance — see Section 7.

---

## Section 4 — Research Questions

The project's official structure, frozen alongside the artefacts above. Full statements, sub-questions, success criteria, and current-status detail live in `01_research_questions.md` and `02_hypotheses.md` — not restated here.

| RQ | Evidence base |
|---|---|
| RQ1 | Event Study (CAR/CAAR) + Causal Analysis (DoWhy) |
| RQ2 | Feature Importance (RF / SHAP) |
| RQ3 | Baseline vs. Event-Enhanced Models |

See `rq_traceability.svg` for the visual method chain per RQ, and `docs/research_bible/10_decision_log.md` (Architecture cleanup entry, 2026-07-06) for why RQ1's evidence base is shown as a single combined lane rather than split across RQ1/RQ2.

---

## Section 5 — Official Pipeline

```
01 Data Collection
        ↓
02 Exploratory Data Analysis
        ↓
03 Event Detection & Sentiment Tagging
        ↓
04 Event Study & Causal Analysis
        ↓
05 Feature Engineering
        ↓
06 Baseline Model
        ↓
07 Model Evaluation
        ↓
08 Results Visualisation
        ↓
Dissertation
```

Full per-notebook purpose, inputs, and outputs: `project_pipeline.svg`, `08_figures_plan.md`, `docs/00_project_workflow.md`.

---

## Section 6 — Allowed Changes

Only the following categories of change are permitted from this point forward:

- Documentation (clarifications, corrections, new cross-references)
- Typo fixes
- Figure improvements (styling, labelling, legibility)
- SVG improvements (styling only — see `docs/architecture/README.md`'s canonical set)
- Notebook markdown (interpretation, headers, purpose/input/output statements)
- Dissertation writing
- Bug fixes that do **not** alter any output (e.g. a code path that was never executed, a display-only formatting fix)

Any change of this kind should still be logged in `10_decision_log.md` if it is non-trivial, and routine housekeeping items belong in `future_improvements.md`, not actioned directly.

---

## Section 7 — Prohibited Changes

The following are not permitted without a formal new version (e.g. SAP v2.0, FES v1.1, SEF v1.1) and a dedicated Project Director decision, logged in `10_decision_log.md`:

- New datasets
- New features
- New hypotheses
- New statistics
- New models
- New sentiment engines
- New preprocessing
- Changing any frozen output (`master_dataset.parquet`, `feature_matrix.parquet`, `car_results.parquet`, `events_tagged.parquet`, `daily_sentiment.parquet`, any model artefact, any evaluation metric)
- Changing the Research Questions
- Changing the SAP (`statistical_analysis_plan.md` + suite)
- Changing the FES (`feature_contract.md`)
- Changing the MCP (`model_contract.md`)
- Changing the SEF (`10_decision_log.md` SEF v1.0 entry)

---

## Section 8 — Reproducibility Statement

The frozen datasets, feature matrix, model contracts, statistical plan, sentiment engine, and governance documents listed in Section 3 collectively define the official, reproducible version of this dissertation. Any number quoted in the dissertation must trace back to one of these frozen artefacts (see `15_traceability_matrix.md`) — not to a re-run, a memory of a result, or an unlogged local change.

Future improvements, ideas, and technical debt belong exclusively in `future_improvements.md` and must not modify the frozen methodology described here. An idea recorded there is explicitly *not* part of the frozen dissertation scope until it is promoted through a new, dated decision in `10_decision_log.md`.

---

## Section 9 — Project Director Approval

| Field | Value |
|---|---|
| Project Director | Ibrahim Haroun |
| Project | 7030DATSCI |
| Status | **APPROVED** |
| Methodology Freeze | **APPROVED** |
| Ready for Dissertation | **YES** |

---

*This document is the first document any future contributor, examiner, or collaborator should read. `00_project_overview.md` remains the narrative "what is this project" companion; this document is the binding governance record.*
