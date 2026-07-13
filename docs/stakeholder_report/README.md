# Stakeholder Report — Index

**Purpose:** A plain-language walkthrough of this project for readers who don't need (or want) the technical detail — what was built, why it matters, what the results actually mean, and how confident we are in each part. Every section links back to the technical record for anyone who does want to check the detail.
**Audience:** Non-technical stakeholders (e.g. examiners skimming for substance, a supervisor's quick check-in, anyone who wants "what happened and can I trust it" without reading code).
**Owner:** Ibrahim Haroun.
**Relationship to the technical documentation:** This folder is a *companion* to [`docs/research_bible/`](../research_bible/README.md), not a replacement. The Research Bible is the complete, auditable technical record (methodology, statistics, decisions, limitations). This folder translates that record into plain language, one pipeline stage at a time, and always points back to the source document behind each claim.
**Status:** In progress — built incrementally, stage by stage, as each stage of the pipeline is verified. See the table below for what's covered so far.
**Update Frequency:** A section is only written (or rewritten) once the underlying notebook/data has been run and its output has been checked against the numbers reported here — not from memory or from an earlier draft. If a number in this folder and a number in the notebook ever disagree, the notebook is correct and this folder is stale and needs updating.

---

## What's covered so far

| # | Stage | Plain-language section | Status | Technical source |
|---|---|---|---|---|
| 1 | Data Collection | [`01_data_collection.md`](01_data_collection.md) | ✅ Written, numbers verified against files on disk (2026-07-13) | `notebooks/01_data_collection.ipynb`, [`dataset_contract.md`](../research_bible/dataset_contract.md), [`05_data_dictionary.md`](../research_bible/05_data_dictionary.md) |
| 2 | Exploratory Data Analysis | *not yet written* | — | `notebooks/02_eda.ipynb` |
| 3 | Event Detection & Sentiment | *not yet written* | — | `notebooks/03_event_detection.ipynb` (currently being revised — see [`10_decision_log.md`](../research_bible/10_decision_log.md), 2026-07-13 entries) |
| 4 | Causal Analysis | *not yet written* | — | `notebooks/04_causal_analysis.ipynb` |
| 5 | Feature Engineering | *not yet written* | — | `notebooks/05_feature_engineering.ipynb` |
| 6 | Model Training | *not yet written* | — | `notebooks/06_model_training.ipynb` |
| 7 | Model Evaluation | *not yet written* | — | `notebooks/07_model_evaluation.ipynb` |
| 8 | Results Visualisation | *not yet written* | — | `notebooks/08_results_visualisation.ipynb` |

## How to read this folder

1. **Want the headline story?** Read the numbered sections in order — each one builds on the last, the same way the actual pipeline does.
2. **Want to check a specific claim?** Every section has a "Technical detail" line pointing to the exact notebook and document it's drawn from.
3. **Something looks off, or out of date?** The project is still under active revision as of this writing (see [`10_decision_log.md`](../research_bible/10_decision_log.md) for the current state) — a "Status" tag at the top of each section says whether it reflects a verified, current run or an earlier one.

## A note on honesty

This project's own technical documentation is built around reporting things — including problems and null results — accurately rather than favourably (see the Research Bible's [governing rule](../research_bible/README.md)). This folder follows the same principle in plain language: if something is uncertain, still being checked, or didn't work as originally planned, that will be said plainly rather than smoothed over.
