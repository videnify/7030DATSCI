# 00 — Project Overview

**Purpose:** One-page orientation document — what this project is, why it exists, what it deliberately does not attempt, and where it currently stands. Read this before any other document in the Research Bible.
**Owner:** Ibrahim Haroun.
**Dependencies:** None (this is the root document); informs all others.
**Update Frequency:** Updated whenever project scope, title, or overall status changes — expect low churn after Phase 0.
**Relation to Dissertation:** Direct source for the dissertation Abstract and Chapter 1 (Introduction).

---

## Title

**Causal Event-Driven Market Impact Modelling**

## Programme context

MSc Data Science dissertation, Liverpool John Moores University (module DATSCI7030), 2025–2026 cohort. Author: Ibrahim Haroun.

## Main goal

Investigate whether major macroeconomic policy announcements and presidential communications influence the S&P 500, and whether information derived from those events improves short-term market prediction beyond what price history alone can achieve.

## Why this project (motivation)

Event-driven market reactions are a long-standing subject in empirical finance (classical event-study literature going back to Fama, Fisher, Jensen & Roll, 1969), but most academic and practitioner work treats "events" as scheduled, structured releases (earnings, FOMC decisions). This project extends that lens to **unstructured political communication** (presidential speeches, press conferences, executive orders) alongside the traditional macro calendar, and asks a second, distinct question: even if an event *causally* moves the market, does knowing about it *in advance or in real time* actually improve next-day return prediction relative to a model that only sees price history? The gap between "the event mattered" (causal inference) and "the event is useful for forecasting" (predictive ML) is the specific niche this project occupies.

## Scope discipline

This project deliberately narrows a much broader possible design (originally considered: multi-asset causal microstructure analysis) down to three research questions. **Depth is preferred over breadth.** Anything that does not trace to RQ1, RQ2, or RQ3 via `15_traceability_matrix.md` should be cut, not kept "for completeness." This is a repeated, explicit instruction from the project's own governing brief (`docs/00_project_workflow.md`) and is the single most important scope-control principle for this repository.

## The three research questions (summary — full detail in `01_research_questions.md`)

| # | Question | Answered by |
|---|----------|-------------|
| RQ1 | Do presidential communications and Federal Reserve announcements produce statistically significant abnormal returns in the S&P 500? | Event study + causal inference (Phase 4) |
| RQ2 | Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns? | Feature engineering + importance/SHAP (Phases 5, 7) |
| RQ3 | Can machine learning models using event information outperform market-only baseline models? | Model comparison (Phases 6–7) |

## Required vs. optional datasets

| Status | Dataset | Role |
|--------|---------|------|
| Required | SPY | Primary asset under study |
| Required | VIX | Volatility regime control / confounder |
| Required | Federal Funds Rate | Macro feature, monetary-policy proxy |
| Required | CPI | Macro feature, inflation proxy |
| Required | Unemployment | Macro feature, labour-market proxy |
| Required | FOMC meetings | Structured monetary-policy events |
| Required | Presidential communications (APP) | Unstructured political-event text |
| Optional | QQQ, GLD, TLT | Cross-asset generalisation check — not yet used in any downstream result; see `10_decision_log.md` and `11_limitations.md` |
| Optional | GDELT | Candidate geopolitical-risk control — full 2015–2025 daily history (4,018 days) integrated into the master dataset; excluded from the frozen DoWhy DAG and FES v1.1; see `11_limitations.md` |

## Pipeline (as implemented)

The governing brief specifies a 10-phase pipeline; the implemented repository currently runs an 8-notebook version that merges sentiment analysis into event detection and explainability into evaluation. This divergence is tracked as an open decision in `docs/00_project_workflow.md` and `10_decision_log.md` — treat the phase *names and RQ traceability* below as authoritative, and the notebook filenames as the current implementation.

| Phase | Notebook | Status (as of 2026-07-16) |
|-------|----------|------|
| 1 — Data Collection | `01_data_collection.ipynb` | ✅ Complete |
| 2 — EDA | `02_eda.ipynb` | ✅ Complete |
| 3 — Event Detection & NLP | `03_event_detection.ipynb` | ✅ Complete |
| 4 — Causal Analysis (Event Study) | `04_causal_analysis.ipynb` | ✅ Complete |
| 5 — Feature Engineering | `05_feature_engineering.ipynb` | ✅ FES v1.1 complete (92 features, validation PASS) |
| 6 — Model Training | `06_model_training.ipynb` | ✅ `Baseline_LASSO` v1.1 complete; validation PASS |
| 7 — Model Evaluation | `07_model_evaluation.ipynb` | ✅ FES v1.1 event suite, RF/SHAP and corrected tests complete; validation PASS |
| 8 — Results Visualisation | `08_results_visualisation.ipynb` | ✅ Visualisation v1.2 complete; figures 08a–08d include the completed RQ1 BH-FDR/effect-size reporting and validation is `PASS` |
| — Dissertation Writing | `reports/dissertation/` | ✅ **Accepted 2026-07-16** — `2026-07-16-7030DATSCI.docx`/`.pdf`. Repository frozen pending assessment feedback; see `FINAL_PROJECT_FREEZE_2026-07-16.md`. |

See `14_project_dashboard.md` for the live, more granular status view (including open repository-hygiene risks).

## What this project explicitly does NOT attempt

- No high-frequency / intraday microstructure analysis — daily closes only.
- No multi-asset causal claims — QQQ/GLD/TLT are exploratory only unless promoted via a logged decision (`10_decision_log.md`).
- No claim of tradeable alpha — RQ3 is about *statistical* predictive improvement, not a backtested trading strategy; any Sharpe-ratio-style figures produced (e.g. `07d_strategy_performance.png`) are illustrative, not a claim of profitability net of costs (see `11_limitations.md`).
- No full-text NLP on presidential communications in the current scope — sentiment is scored on document titles, not full transcripts (see `11_limitations.md`).

## Key documents outside this folder

- `docs/00_project_workflow.md` — phase-to-RQ traceability rule (governing document for scope decisions).
- `DATSCI7030_Repository_Audit_Report.ipynb` — living repository hygiene and action-plan tracker.
- Root `README.md` — repository-level setup, structure, and reproducibility instructions.
