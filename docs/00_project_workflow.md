# 00 — Official Project Workflow

**Project:** Causal Event-Driven Market Impact Modelling (DATSCI7030, MSc Data Science, LJMU)
**Status:** Living document — update the phase table below whenever a phase changes state.

---

## Governing rule

No notebook, figure, model, table, or statistical test should be included in this repository or the dissertation unless it directly supports one of the three research questions below. If a piece of work doesn't trace back to RQ1, RQ2, or RQ3, it should be cut or moved out of the main pipeline — depth over breadth.

## Research questions

| # | Question |
|---|----------|
| RQ1 | Do presidential communications and Federal Reserve announcements produce statistically significant abnormal returns in the S&P 500? |
| RQ2 | Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns? |
| RQ3 | Can machine learning models using event information outperform market-only baseline models? |

---

## Phases

### Phase 0 — Research Design
Define RQs, hypotheses, scope boundaries (required vs. optional datasets), and success criteria. Output: this document, `README.md`, and any research-log entries in `docs/research_notes/`.

### Phase 1 — Repository Cleanup
Establish reproducible project scaffolding: folder structure, `.gitignore`, secrets hygiene, canonical notebook naming, dependency pinning. No research output — pure engineering hygiene. Output: clean `git init`-ready repository, this workflow doc, an up-to-date `README.md`.

### Phase 2 — Data Collection
Pull SPY/VIX price data, Federal Funds Rate/CPI/Unemployment (macro), FOMC meeting dates, and presidential communications. Validate completeness and save immutable raw files. Notebook: `01_data_collection.ipynb`. Output: `data/raw/*`.

### Phase 3 — Data Cleaning
Handle missing values, align trading-day calendars, merge event and market data into a master dataframe. Notebook: `02_data_cleaning.ipynb`. Output: `data/interim/`, `data/processed/`.

### Phase 4 — EDA and Statistical Profiling
Descriptive statistics, distributions, market behaviour, and event-frequency profiling — establishes the empirical baseline the later phases will test against. Notebook: `03_exploratory_analysis.ipynb`.

### Phase 5 — Event Study
Abnormal returns (AR), cumulative abnormal returns (CAR), cumulative average abnormal returns (CAAR), and significance testing around event windows. This is the primary evidence for **RQ1**. Notebook: `04_event_study.ipynb`.

### Phase 6 — Sentiment Analysis
Text preprocessing and sentiment/event scoring of presidential communications and FOMC statements; merge sentiment back onto the event timeline. Feeds **RQ2**. Notebook: `05_sentiment_analysis.ipynb`.

### Phase 7 — Feature Engineering
Rolling returns, lag variables, volatility measures, technical indicators, event features, and macro features combined into the final ML dataset. Feeds **RQ2** and **RQ3**. Notebook: `06_feature_engineering.ipynb`.

### Phase 8 — Machine Learning
A market-only baseline (`Baseline_LASSO`) trained on price/technical features only, plus three event-enhanced candidates (Event_LASSO, XGBoost, LightGBM) trained on the full event-augmented feature set, all under an identical time-series cross-validation protocol. Random Forest is used only as an RQ2 feature-importance tool, not as an RQ3 predictive candidate. Directly answers **RQ3**. Notebooks: `06_model_training.ipynb` (baseline), `07_machine_learning.ipynb` (event-enhanced candidates + comparison).

### Phase 9 — Evaluation and Explainability
ROC, precision/recall, confusion matrix, feature importance, and SHAP values — quantifies *which* features matter (RQ2) and *whether* the event-augmented model actually wins (RQ3). Notebook: `08_model_evaluation.ipynb`.

### Phase 10 — Dissertation Writing
Assemble findings from Phases 4–9 into the dissertation narrative, aligned strictly to RQ1–RQ3. Output: `reports/dissertation/`.

---

## Phase-to-RQ traceability

| Phase | RQ1 | RQ2 | RQ3 |
|-------|:---:|:---:|:---:|
| 5 — Event Study | ✅ | | |
| 6 — Sentiment Analysis | | ✅ | |
| 7 — Feature Engineering | | ✅ | ✅ |
| 8 — Machine Learning | | | ✅ |
| 9 — Evaluation & Explainability | | ✅ | ✅ |

If a future notebook or figure can't be placed in this table against at least one RQ, it doesn't belong in the main pipeline.

## Notebook naming note

**Resolved 2026-07-06 (Project Governance Freeze).** The repository uses an 8-notebook pipeline (`01_data_collection.ipynb` … `08_results_visualisation.ipynb`), merging Phase 6 (Sentiment Analysis) into Phase 5's notebook (Event Detection) and Phase 9 (Evaluation & Explainability) into Phase 8's notebook (Machine Learning), rather than the 10-stage numbering shown above. This was an open decision as of the original repository audit (`DATSCI7030_Repository_Audit_Report.ipynb` §7); it is now closed — the 8-notebook layout is the official, frozen pipeline (`docs/research_bible/00_project_freeze.md` §5), not a placeholder pending renumbering. Treat the *phase names and RQ traceability* above as the authoritative research-design framing, and the notebook filenames actually in `notebooks/` as the frozen implementation of them — no further renumbering is planned.
