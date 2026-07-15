# Research Bible — Index

**Purpose:** Single entry point to the project's Research Bible — the complete, versioned record of *why* every research decision was made, not just *what* the code does. Where `docs/00_project_workflow.md` defines the phase pipeline and `DATSCI7030_Repository_Audit_Report.ipynb` tracks repository hygiene, the Research Bible is the research-integrity layer: questions, hypotheses, methodology, statistics, data/feature definitions, results, decisions, limitations, and dissertation traceability, all in one place.
**Owner:** Ibrahim Haroun (project author).
**Dependencies:** `docs/00_project_workflow.md` (phase definitions), root `README.md` (repository-level status), `DATSCI7030_Repository_Audit_Report.ipynb` (hygiene/action tracking).
**Update Frequency:** Reviewed at the end of every phase (see `docs/00_project_workflow.md`); individual documents are updated more often — see each document's own header.
**Relation to Dissertation:** This folder is the primary source material for the dissertation's Introduction, Methodology, Results, Discussion, and Limitations chapters (see `12_dissertation_outline.md` for the exact chapter-to-document mapping). Nothing should appear in the dissertation that cannot be traced back to a document here.

---

## Companion: plain-language stakeholder report

[`docs/stakeholder_report/`](../stakeholder_report/README.md) translates this technical record into plain language, one pipeline stage at a time, for readers who want "what happened and can I trust it" without the methodology detail. It always links back to the specific document here that backs each claim — treat this Research Bible as the source of truth if the two ever disagree.

## Governing rule

Every document in this folder must justify its own existence against the three research questions (RQ1–RQ3, defined in `01_research_questions.md`). If a section of a document cannot be traced to at least one RQ via `15_traceability_matrix.md`, it should be cut or moved to `11_limitations.md` as an explicitly scoped-out item — silence is not an acceptable way to handle scope decisions in this project.

## Document index

**Start here:** [`00_project_freeze.md`](00_project_freeze.md) — the Project Governance Freeze (2026-07-06). States what is frozen, why, and what changes are still allowed before reading anything else in this folder. Sits alongside the numbered sequence below (like the SAP suite further down) rather than displacing `00_project_overview.md`'s number, to avoid disturbing the existing `12_dissertation_outline.md` chapter mapping.

| # | Document | One-line purpose |
|---|----------|-------------------|
| 00 | [`00_project_overview.md`](00_project_overview.md) | What the project is, why it exists, and current phase status at a glance |
| 01 | [`01_research_questions.md`](01_research_questions.md) | RQ1–RQ3 in full, with sub-questions and success criteria |
| 02 | [`02_hypotheses.md`](02_hypotheses.md) | Formal H0/H1 statements per RQ, mapped to statistical tests |
| 03 | [`03_methodology.md`](03_methodology.md) | Event study, causal inference, NLP, feature engineering, and ML methodology |
| 04 | [`04_statistics_plan.md`](04_statistics_plan.md) | Every statistical test used, why, its assumptions, and how violations are handled |
| 05 | [`05_data_dictionary.md`](05_data_dictionary.md) | Every raw and processed data file, column-by-column |
| 06 | [`06_feature_dictionary.md`](06_feature_dictionary.md) | Every engineered feature, its formula, and its group |
| 07 | [`07_model_plan.md`](07_model_plan.md) | Baseline and candidate models, hyperparameters, validation protocol |
| 08 | [`08_figures_plan.md`](08_figures_plan.md) | Every figure, which notebook produces it, and which RQ it supports |
| 09 | [`09_results_log.md`](09_results_log.md) | Dated log of headline results as the project progresses |
| 10 | [`10_decision_log.md`](10_decision_log.md) | Every non-trivial scope/design decision, with the reasoning and date |
| 11 | [`11_limitations.md`](11_limitations.md) | Known weaknesses, scoped-out work, and how each is handled in the write-up |
| 12 | [`12_dissertation_outline.md`](12_dissertation_outline.md) | Chapter-by-chapter dissertation structure mapped to phases and documents |
| 13 | [`13_validation_checklist.md`](13_validation_checklist.md) | Pre-submission checklist — reproducibility, statistical validity, hygiene |
| 14 | [`14_project_dashboard.md`](14_project_dashboard.md) | One-page current status snapshot across all phases and RQs |
| 15 | [`15_traceability_matrix.md`](15_traceability_matrix.md) | Matrix linking every notebook/figure/table/test to RQ1/RQ2/RQ3 |

## Statistical Analysis Plan suite (frozen v1.0, 2026-07-04 — Mission 04)

These sit alongside `04_statistics_plan.md` (which they extend, not replace) rather than being renumbered into the 00–15 sequence, to avoid disturbing the existing dissertation-chapter mapping in `12_dissertation_outline.md`.

| Document | One-line purpose |
|---|---|
| [`statistical_analysis_plan.md`](statistical_analysis_plan.md) | Master SAP — global policy freeze, RQ→statistics mapping, hypothesis freeze summary |
| [`statistical_decision_matrix.md`](statistical_decision_matrix.md) | Master statistical test matrix + exact RQ3 model-comparison protocol |
| [`statistical_assumptions.md`](statistical_assumptions.md) | Full assumption matrix + time-series diagnostics specification |
| [`statistical_reporting_guidelines.md`](statistical_reporting_guidelines.md) | Numeric reporting, CI/effect-size, and figure-caption conventions |
| [`dataset_contract.md`](dataset_contract.md) | Consumption rules for `master_dataset.parquet` (distinct from `dataset_version.md`'s freeze record) |
| [`feature_contract.md`](feature_contract.md) | Consumption rules for `feature_matrix.parquet` (FES v1.1, 92 features, validation PASS) — baseline eligibility, scaling/encoding rules, versioning |
| [`model_contract.md`](model_contract.md) | Model Contract Protocol (MCP v1.0, Mission 06) — approved models, evaluation/hyperparameter/CV policy, promotion criteria |
| [`baseline_model_specification.md`](baseline_model_specification.md) | Exact, reproducible specification of current `Baseline_LASSO` v1.1 |
| [`baseline_evaluation.md`](baseline_evaluation.md) | Full evaluation, comparison-baseline context, and interpretation of current `Baseline_LASSO` v1.1 |

## How to use this folder

1. **Starting a new phase?** Read `00_project_overview.md` and `14_project_dashboard.md` first for current state, then the relevant methodology/statistics sections before writing code.
2. **Got a result?** Log it in `09_results_log.md` the same day, dated, with the source file/notebook that produced it — do not rely on memory or a notebook's saved output as the permanent record.
3. **Made a scope decision** (e.g. "drop GLD/TLT," "use lexicon sentiment over FinBERT")? Log it in `10_decision_log.md` with the reasoning, not just the outcome.
4. **Writing the dissertation?** Work from `12_dissertation_outline.md` outward — each chapter section links back to the document(s) that supply its content.
5. **Before submission:** work through `13_validation_checklist.md` in full and re-check `15_traceability_matrix.md` for orphaned work (anything not traceable to RQ1–RQ3).

## Conventions used across every document

- Dates are always absolute (`YYYY-MM-DD`), never relative ("today," "last week"), so entries remain interpretable after time passes.
- Every numeric result quoted anywhere in this folder must name its source file (e.g. `models/model_metadata.json`, `data/processed/causal_estimates.parquet`) so it can be re-verified by re-running the pipeline.
- Status markers used throughout: ✅ Done · 🟡 In Progress · ⬜ Not Started · 🔴 Blocked.
- No document in this folder replaces the code — it explains the code's intent and interprets its output. If a document and the code disagree, the code is provisionally correct and the document needs updating (raise it in `10_decision_log.md` if the disagreement reflects an undocumented decision).
