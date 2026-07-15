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
| Abstract | `00_project_overview.md` + headline results from `09_results_log.md` | ✅ Synchronized to rebuilt RQ1, FES v1.1 RQ2/RQ3, and full-history GDELT on 2026-07-14 |
| Acknowledgements | — | ⬜ |
| List of Figures | `08_figures_plan.md` | ✅ Present; refresh Word fields on final open |
| List of Tables | `05_data_dictionary.md`, `06_feature_dictionary.md`, `09_results_log.md` | ✅ Present; refresh Word fields on final open |

## Chapter 1 — Introduction

| Section | Source | Status |
|---------|--------|--------|
| 1.1 Background & motivation | `00_project_overview.md` | ✅ Draft present |
| 1.2 Problem statement | `00_project_overview.md` | ✅ Draft present |
| 1.3 Research questions | `01_research_questions.md` | ✅ |
| 1.4 Scope & contribution | `00_project_overview.md` ("scope discipline," "does NOT attempt") | ✅ Draft present |
| 1.5 Dissertation structure | This document | ✅ Draft present |

## Chapter 2 — Literature Review

| Section | Source | Status |
|---------|--------|--------|
| 2.1 Event study methodology (classical) | `03_methodology.md` §1 (cite Fama, Fisher, Jensen & Roll 1969 tradition) | ✅ Draft present in prior-work positioning |
| 2.2 Causal inference in finance | `03_methodology.md` §2 (DoWhy framework literature) | ✅ Draft present in prior-work positioning |
| 2.3 NLP/sentiment for policy & financial text | `03_methodology.md` §3, `11_limitations.md` L5/L6 | ✅ Draft present in prior-work positioning |
| 2.4 ML for return prediction | `03_methodology.md` §5 | ✅ Draft present in prior-work positioning |
| 2.5 Gap this project addresses | `00_project_overview.md` "Why this project" | ✅ Draft present |

## Chapter 3 — Methodology

| Section | Source | Status |
|---------|--------|--------|
| 3.1 Data sources | `05_data_dictionary.md` | ✅ (content ready) |
| 3.2 Hypotheses | `02_hypotheses.md` | ✅ (content ready) |
| 3.3 Feature engineering | `06_feature_dictionary.md`, `03_methodology.md` §4 | ✅ (content ready) |
| 3.4 Statistical analysis plan | `statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`, `statistical_reporting_guidelines.md`, `04_statistics_plan.md` (per-notebook detail) | ✅ SAP v1.0 implemented; RQ1 BH-FDR/effect sizes and RQ3 paired tests complete. |
| 3.5 Model specification | `07_model_plan.md`, `model_contract.md`, `baseline_model_specification.md`, `03_methodology.md` §5 | ✅ Current FES v1.1 baseline, event suite, RF/SHAP, RQ3 tests, and Notebook 08 figures |
| 3.6 Reproducibility | `03_methodology.md` "Reproducibility notes," `dataset_contract.md`, root `README.md` | ✅ (content ready) |

## Chapter 4 — Results

| Section | RQ | Source | Status |
|---------|----|--------|--------|
| 4.1 Event study results | RQ1 | `09_results_log.md` (2026-07-15 RQ1-v1.0 entry), `event_type_statistics.parquet`, figures `04a`–`04d`, `08a`–`08b` | ✅ Five-type BH-FDR/95% CI/Cohen's d table complete; 0/5 rejected |
| 4.2 Causal estimates | RQ1 | `09_results_log.md`, `data/processed/causal_estimates.parquet`, `08b_causal_evidence.png` | ✅ Current pooled and sparse per-category estimates drafted with caveats |
| 4.3 Feature importance | RQ2 | `09_results_log.md`, `06_feature_dictionary.md`, `reports/model_comparison/feature_importance.parquet`, figure `08c` | ✅ Current FES v1.1 null finding drafted |
| 4.4 Model comparison | RQ3 | `09_results_log.md`, `baseline_evaluation.md`, `07_model_plan.md`, `reports/model_comparison/statistical_tests.json`, figures `08c`–`08d` | ✅ Current FES v1.1 comparison drafted; H0₃ not rejected |
| 4.5 Diagnostics & robustness | RQ1/RQ3 | `04_statistics_plan.md`, `reports/model_comparison/statistical_tests.json`, `11_limitations.md` L4/L9 | ✅ Current diagnostics drafted; XGBoost root-cause investigation remains a stated limitation |

## Chapter 5 — Discussion

| Section | Source | Status |
|---------|--------|--------|
| 5.1 Interpretation of RQ1 findings | `01_research_questions.md` (RQ1), `09_results_log.md` | ✅ Current mixed RQ1 interpretation drafted |
| 5.2 Interpretation of RQ2 findings | `01_research_questions.md` (RQ2) | ✅ Current null finding drafted |
| 5.3 Interpretation of RQ3 findings | `01_research_questions.md` (RQ3), `reports/model_comparison/statistical_tests.json` | ✅ Current null finding and base-rate caveat drafted |
| 5.4 Limitations | `11_limitations.md` in full | ✅ Current draft present |
| 5.5 Future work | `11_limitations.md` "Handling in write-up" notes across L1, L7, L8, L9 | ✅ Current draft present |

## Chapter 6 — Conclusion

| Section | Source | Status |
|---------|--------|--------|
| 6.1 Summary of contributions | `01_research_questions.md`, `09_results_log.md` | ✅ Current draft present |
| 6.2 Answers to RQ1–RQ3 | `01_research_questions.md` "Current status" fields | ✅ Current answers drafted |
| 6.3 Closing remarks | — | ✅ Draft present |

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

The full draft is synchronized to the current analytical boundary, including the completed RQ1 table. Work from `13_validation_checklist.md`: refresh Word fields and cross-references, verify every number against `09_results_log.md`, resolve the remaining scope/security gates, and perform the final proofreading pass.
