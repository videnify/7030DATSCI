# 12 — Dissertation Outline

**Purpose:** Chapter-by-chapter dissertation structure, with each section mapped to the Research Bible document(s) and repository artefact(s) that supply its content — so writing the dissertation is an assembly task from already-verified material, not a fresh research exercise.
**Owner:** Ibrahim Haroun.
**Dependencies:** Every other document in this folder; this is the integration point.
**Update Frequency:** Update as chapters are drafted — mark each section's status (⬜/🟡/✅) as writing progresses.
**Relation to Dissertation:** This *is* the dissertation's structural skeleton.

---

## Front matter

| Section | Source | Status |
|---------|--------|--------|
| Abstract | `00_project_overview.md` + headline results from `09_results_log.md` | ⬜ |
| Acknowledgements | — | ⬜ |
| List of Figures | `08_figures_plan.md` | ⬜ |
| List of Tables | `05_data_dictionary.md`, `06_feature_dictionary.md`, `09_results_log.md` | ⬜ |

## Chapter 1 — Introduction

| Section | Source | Status |
|---------|--------|--------|
| 1.1 Background & motivation | `00_project_overview.md` | 🟡 |
| 1.2 Problem statement | `00_project_overview.md` | 🟡 |
| 1.3 Research questions | `01_research_questions.md` | ✅ |
| 1.4 Scope & contribution | `00_project_overview.md` ("scope discipline," "does NOT attempt") | 🟡 |
| 1.5 Dissertation structure | This document | ⬜ |

## Chapter 2 — Literature Review

| Section | Source | Status |
|---------|--------|--------|
| 2.1 Event study methodology (classical) | `03_methodology.md` §1 (cite Fama, Fisher, Jensen & Roll 1969 tradition) | ⬜ |
| 2.2 Causal inference in finance | `03_methodology.md` §2 (DoWhy framework literature) | ⬜ |
| 2.3 NLP/sentiment for policy & financial text | `03_methodology.md` §3, `11_limitations.md` L5/L6 | ⬜ |
| 2.4 ML for return prediction | `03_methodology.md` §5 | ⬜ |
| 2.5 Gap this project addresses | `00_project_overview.md` "Why this project" | ⬜ |

## Chapter 3 — Methodology

| Section | Source | Status |
|---------|--------|--------|
| 3.1 Data sources | `05_data_dictionary.md` | ✅ (content ready) |
| 3.2 Hypotheses | `02_hypotheses.md` | ✅ (content ready) |
| 3.3 Feature engineering | `06_feature_dictionary.md`, `03_methodology.md` §4 | ✅ (content ready) |
| 3.4 Statistical analysis plan | `statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`, `statistical_reporting_guidelines.md`, `04_statistics_plan.md` (per-notebook detail) | ✅ Frozen v1.0 (2026-07-04) — RQ1/RQ2 methodology ratified as-run, RQ3 protocol frozen prospectively pending baseline (Mission 06) |
| 3.5 Model specification | `07_model_plan.md`, `model_contract.md`, `baseline_model_specification.md`, `03_methodology.md` §5 | 🟡 (baseline section content ready — `Baseline_LASSO` v1.0 trained 2026-07-05; event-enhanced model retraining on FES v1.0 still pending, Mission 07) |
| 3.6 Reproducibility | `03_methodology.md` "Reproducibility notes," `dataset_contract.md`, root `README.md` | ✅ (content ready) |

## Chapter 4 — Results

| Section | RQ | Source | Status |
|---------|----|--------|--------|
| 4.1 Event study results | RQ1 | `09_results_log.md` (2026-07-04 CAR entry), figures `04a`–`04d`, `08a`–`08b` | 🟡 (pending FDR correction — L3) |
| 4.2 Causal estimates | RQ1 | `09_results_log.md`, `data/processed/causal_estimates.parquet` | 🟡 |
| 4.3 Feature importance | RQ2 | `09_results_log.md`, `06_feature_dictionary.md`, figures `05a`, `06c`, `07c` | ✅ (content ready) |
| 4.4 Model comparison | RQ3 | `09_results_log.md`, `baseline_evaluation.md`, `07_model_plan.md`, `reports/statistics/07_event_models_summary.md` | ✅ (complete 2026-07-05 — H0₃ not rejected; full DM/z-test comparison, Bonferroni-corrected, against `Baseline_LASSO`) |
| 4.5 Diagnostics & robustness | RQ1/RQ3 | `04_statistics_plan.md` residual diagnostics, `11_limitations.md` L4/L9 | 🟡 |

## Chapter 5 — Discussion

| Section | Source | Status |
|---------|--------|--------|
| 5.1 Interpretation of RQ1 findings | `01_research_questions.md` (RQ1), `09_results_log.md` | ⬜ |
| 5.2 Interpretation of RQ2 findings | `01_research_questions.md` (RQ2) | ⬜ |
| 5.3 Interpretation of RQ3 findings | `01_research_questions.md` (RQ3), `reports/statistics/07_event_models_summary.md` | 🟡 (content ready — H0₃ not rejected; write-up must include the directional-accuracy base-rate caveat) |
| 5.4 Limitations | `11_limitations.md` in full | ✅ (content ready) |
| 5.5 Future work | `11_limitations.md` "Handling in write-up" notes across L1, L7, L8, L9 | 🟡 |

## Chapter 6 — Conclusion

| Section | Source | Status |
|---------|--------|--------|
| 6.1 Summary of contributions | `01_research_questions.md`, `09_results_log.md` | ⬜ |
| 6.2 Answers to RQ1–RQ3 | `01_research_questions.md` "Current status" fields | 🟡 (all three RQs answered; drafting pending) |
| 6.3 Closing remarks | — | ⬜ |

## Appendices

| Appendix | Source |
|----------|--------|
| A — Full data dictionary | `05_data_dictionary.md` |
| B — Full feature dictionary | `06_feature_dictionary.md` |
| C — Statistical test details | `04_statistics_plan.md` |
| D — Repository & reproducibility guide | Root `README.md`, `docs/00_project_workflow.md` |
| E — Decision log (methodology justifications) | `10_decision_log.md` |

---

## Writing-order recommendation

Given current status: draft Chapters 3 and the RQ1/RQ2 portions of Chapter 4 first (marked ✅/🟡, content is ready), while `07_model_plan.md`'s baseline model is being trained in parallel — do not block dissertation drafting on RQ3 closing, but do not write Chapter 4.4/5.3/6.2 until it does (marked 🔴 above). See `13_validation_checklist.md` before treating any chapter as final.
