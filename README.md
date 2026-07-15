# DATSCI7030 — Causal Event-Driven Market Impact Modelling

> **Module:** 7030DATSCI — Data Science Project  
> **Author:** Ibrahim Haroun  
> **Institution:** Liverpool John Moores University  
> **Year:** 2025–2026  
> **Version:** 2.1 — Pipeline Rebuilt, GDELT Integrated as Continuous Confounder (2026-07-13)  
> **Last updated:** 2026-07-13

---

## Project Overview

This project investigates the **causal impact of real-world events** — presidential communications and Federal Reserve (FOMC) announcements — on the S&P 500 (via SPY), combined with a **predictive layer** that tests whether event-derived information improves next-day return prediction over a market-only baseline.

The methodology combines:
- **Event Study Analysis** — cumulative abnormal return (CAR) measurement around event windows
- **Causal Inference** — DoWhy backdoor-adjusted structural causal model to isolate causation from correlation
- **NLP Event Detection** — rule-based keyword event-type classification plus FinBERT sentiment scoring of presidential-document titles (FinBERT is the official primary sentiment engine — Sentiment Engine Freeze v1.0)
- **Predictive Modelling** — a market-only `Baseline_LASSO` compared against event-enhanced Event_LASSO/XGBoost/LightGBM candidates, with SHAP explainability

---

## Research Questions

| # | Question |
|---|----------|
| RQ1 | Do presidential communications and Federal Reserve announcements produce statistically significant abnormal returns in the S&P 500? |
| RQ2 | Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns? |
| RQ3 | Can machine learning models using event information outperform market-only baseline models? |

Depth is preferred over breadth — no notebook, figure, model, or statistical test is included unless it supports one of these three questions (see `docs/00_project_workflow.md`).

**Project status:** Methodology frozen, pipeline rebuilt and re-verified 2026-07-13 (GDELT full-history integration), dissertation phase — see the Research Bible's governance freeze: [`docs/research_bible/00_project_freeze.md`](docs/research_bible/00_project_freeze.md) and the [decision log](docs/research_bible/10_decision_log.md) for the rebuild's full detail.

## Hypotheses

| # | Hypothesis | Tests against |
|---|------------|----------------|
| H1 | Major presidential communications and FOMC announcements are associated with statistically significant non-zero cumulative abnormal returns (CAR) in the S&P 500 around the event window (H0: mean CAR = 0). | RQ1 |
| H2 | Event-derived features (sentiment, event-type indicators) and macroeconomic features (VIX, Fed Funds Rate) rank among the most important predictors of next-day S&P 500 returns — i.e. they contribute more than price-lag-only features. | RQ2 |
| H3 | An ML model trained on the full feature set (market + macro + sentiment + event + interaction) achieves significantly lower RMSE **and** significantly higher directional accuracy than `Baseline_LASSO`, a market-only model trained on price/technical features alone (H0: no significant improvement on either leg). Tested candidates: Event_LASSO, XGBoost, LightGBM (`config.yaml: model.random_seed = 42`, Bonferroni-corrected α = 0.0167 across the three). Random Forest is used only as an RQ2 feature-importance tool, not as an RQ3 predictive candidate. | RQ3 |

## Data Policy

- Raw, interim, processed, and external data are **never committed to git** — see `.gitignore`. Every file under `data/` must be reproducible by re-running the numbered notebooks in order from `data/raw/` onward.
- Trained models (`models/`) are binaries and are also excluded from version control; the market-only baseline (`Baseline_LASSO`) is trained by `notebooks/06_model_training.ipynb`, and the event-enhanced candidates (Event_LASSO, XGBoost, LightGBM) are trained and statistically compared against it by `notebooks/07_model_evaluation.ipynb` (the original 10-phase spec's working name for this notebook, `07_machine_learning.ipynb`, was not the name used in the final 8-notebook implementation).
- API keys and tokens live only in `config.yaml` / `.env`, both gitignored. Never commit real credentials — use a local, untracked copy and rotate any key that is ever exposed on disk or in a notebook's saved output.
- Only SPY, VIX, Federal Funds Rate, CPI, Unemployment, FOMC meetings, and presidential communications are treated as required datasets. QQQ, GLD, TLT are optional and are only kept if they demonstrably improve the analysis for RQ1–RQ3 (see `DATSCI7030_Repository_Audit_Report.ipynb` §8 for the current status of that decision). GDELT's full 2015–2025 daily signal is integrated into `master_dataset.parquet` as a candidate geopolitical-risk control, but it is deliberately absent from the frozen DoWhy DAG and FES v1.1; no reported RQ1–RQ3 result uses a GDELT-derived feature.

---

## Repository Structure

```
DATSCI7030/
├── data/
│   ├── raw/            # Untouched source data (gitignored, README + .gitkeep tracked)
│   ├── interim/        # Intermediate cleaning artefacts (gitignored)
│   ├── processed/      # Cleaned, feature-engineered datasets (gitignored)
│   └── external/       # Reference data (event calendars, macro indicators; gitignored)
├── notebooks/          # Numbered Jupyter notebooks (one per phase)
│   └── archive/        # Superseded/duplicate notebooks — local reference only, gitignored
├── src/                # Reusable Python modules
├── models/             # Trained model binaries (gitignored, README + .gitkeep tracked)
├── logs/               # Runtime logs (gitignored, scaffolding for future scripts)
├── reports/
│   ├── figures/        # All charts and plots (gitignored — regenerate from notebooks)
│   └── dissertation/   # Final written report (tracked)
├── scripts/            # Standalone helper scripts (e.g. run_finbert.py)
├── tests/              # Unit tests for src/ modules
├── docs/
│   ├── 00_project_workflow.md   # Phase 0–10 pipeline and RQ traceability (historical numbering — see note in that file)
│   ├── research_bible/          # Governing documentation: research questions, hypotheses, methodology,
│   │                            # data/feature dictionaries, SAP v1.0, FES v1.1, MCP v1.0, decision log,
│   │                            # results log, dashboard, traceability matrix, project governance freeze
│   └── architecture/            # Canonical pipeline/governance/model diagrams (SVG)
├── DATSCI7030_Repository_Audit_Report.ipynb   # Living repo/dissertation audit log
├── config.yaml         # Project configuration incl. API keys — gitignored, never commit
├── requirements.txt    # Python dependencies
└── .gitignore
```

---

## Setup & Reproducibility

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add real API keys to a local config.yaml / .env (gitignored — never commit real keys)

# 4. Run notebooks in numbered order — each stage reads only what the previous stage wrote
jupyter lab
```

Reproducibility notes:
- `model.random_seed: 42` in `config.yaml` fixes all model randomness; `TimeSeriesSplit` is used everywhere to prevent look-ahead leakage.
- Every file under `data/`, `models/`, and `reports/figures/` is derived, not hand-edited — if it's missing, re-run the notebook listed in that folder's `README.md`.
- No secrets are required to reproduce the market-data pipeline (yfinance, APP, FOMC dates are all free/keyless); FRED and NewsAPI keys are optional and only needed for the macro/legacy-news paths.

---

## Notebooks

Short-form summary only — see the **Phase Progress** table below for current status and exact outputs per notebook.

| # | Notebook | Description |
|---|----------|-------------|
| 01 | `01_data_collection.ipynb` | Pull price data (yfinance), presidential docs (APP), macro (FRED), FOMC dates, GDELT sample |
| 02 | `02_eda.ipynb` | Exploratory data analysis, distributions, stationarity, missing data |
| 03 | `03_event_detection.ipynb` | Rule-based event classification + FinBERT sentiment (SEF v1.0), including explicit category-occurrence counts for Dataset v1.2/FES v1.1 |
| 04 | `04_causal_analysis.ipynb` | Event study (CAR/CAAR) + DoWhy backdoor causal estimate |
| 05 | `05_feature_engineering.ipynb` | Builds `feature_matrix.parquet` — 92 features across 6 categories (FES v1.1, validation PASS) |
| 06 | `06_model_training.ipynb` | Trains `Baseline_LASSO`, the market-only RQ3 baseline (MCP v1.0) |
| 07 | `07_model_evaluation.ipynb` | Trains Event_LASSO/XGBoost/LightGBM; runs the DM/z-test comparison against the baseline; RQ3 verdict |
| 08 | `08_results_visualisation.ipynb` | Final publication-quality figures (300 dpi) sourced from the canonical pipeline |

---

## Key Methods

- **Causal Inference:** DoWhy (Microsoft Research) — backdoor-adjusted structural causal model
- **Event Detection:** rule-based keyword classification (event type); FinBERT (ProsusAI) for sentiment — official primary sentiment engine, Sentiment Engine Freeze v1.0
- **Predictive Models:** `Baseline_LASSO` (market-only), Event_LASSO, XGBoost, LightGBM (all event-enhanced candidates compared against the baseline); Random Forest used only as an RQ2 feature-importance tool
- **Time-Series CV:** `TimeSeriesSplit` (5 folds, seed 42, no data leakage) — identical protocol for the baseline and every candidate
- **Explainability:** SHAP values (linear decomposition for LASSO variants, `TreeExplainer` for XGBoost/LightGBM)

---

## Data Sources

| Source | Type | Status | Access |
|--------|------|--------|--------|
| Yahoo Finance (`yfinance`) | SPY (required) / VIX (required) OHLCV; QQQ, GLD, TLT (optional, exploratory only) | Required (SPY, VIX) | Free, no key needed |
| American Presidency Project (APP) | Presidential speeches, executive orders, press conferences | Required | Free, no key needed |
| FOMC Calendar (Federal Reserve) | Rate decision dates | Required | Free, public |
| FRED (Federal Reserve) | Macro indicators (Fed Funds Rate, CPI, Unemployment, Treasury yields) | Required | Free (API key optional) |
| GDELT Project | Global geopolitical event database | Full 2015–2025 daily history (4,018 days), integrated into `master_dataset.parquet` as a candidate geopolitical-risk control; deliberately outside the current DoWhy DAG and FES v1.1 | Free, public |

---

## Phase Progress

| Phase | Notebook | Status | Key Output |
|-------|----------|--------|------------|
| 1 | `01_data_collection.ipynb` | ✅ Complete — **GDELT full-history backfill added 2026-07-13** (4,018 days, 2015–2025, replacing the 5-day sample) | 5 raw parquets in `data/raw/`, incl. `gdelt_daily_summary.parquet` |
| 2 | `02_eda.ipynb` | ✅ Complete | EDA figures in `reports/figures/` |
| 3 | `03_event_detection.ipynb` | ✅ Dataset v1.2 preparation complete (2026-07-14) — 1,005-event catalogue, 344 high-impact events, full-history GDELT, and a 739 × 18 daily table with explicit health/labour/other occurrence counts. The counts reconcile exactly to the catalogue (14/103/427), so neutral sentiment is no longer confused with no event. | 4 processed parquets, incl. `daily_sentiment.parquet` and `gdelt_daily_risk.parquet`, 4 figures |
| 4 | `04_causal_analysis.ipynb` | ✅ Complete — **re-run 2026-07-13** against the rebuilt pipeline; event-study significance test is now a null result, overall DoWhy estimate remains significant (see Phase 4 update above) | `car_results.parquet` (264 rows), `causal_estimates.parquet`, 4 figures |
| 5 | `05_feature_engineering.ipynb` | ✅ **FES v1.1 frozen and validated 2026-07-14:** 2,477 rows, 92 features, direct health/labour/other occurrence flags, validation `PASS`. The superseded FES v1.0 exception is archived. | `feature_matrix.parquet`, `feature_profile.json`, `feature_matrix_validation.json` |
| 6 | `06_model_training.ipynb` | ✅ **`Baseline_LASSO` v1.1 frozen and validated 2026-07-14:** 27 Market features, full SAP metric suite, validation `PASS`, exact archived FES v1.0 reproduction. | Model, metadata, predictions, metrics, validation, learning figure |
| 7 | `07_model_evaluation.ipynb` | ✅ **FES v1.1 model suite frozen and validated 2026-07-14:** Event_LASSO/XGBoost/LightGBM, Random Forest importance, held-out SHAP, full SAP diagnostics, and corrected DM/z tests; validation `PASS`. H0 is not rejected for RQ2 or RQ3 under the frozen rules. | Models, predictions, comparison/tests, RF/SHAP tables, validation, learning figure |
| 8 | `08_results_visualisation.ipynb` | ✅ **Visualisation v1.2 complete and validated 2026-07-15:** all four publication figures read the current FES v1.1 / MCP v1.0 outputs; validation `PASS`. Figure 08b reports the completed RQ1 BH-FDR/effect-size gate and explicitly labels the combined APP + FOMC treatment. | `08a`–`08d` PNGs plus `results_visualisation_validation.json` |

---

## Phase 3 — Event Detection & NLP (Complete; input counts below are a historical 2026-07-06 snapshot, superseded 2026-07-13)

> **2026-07-13 update:** Notebook 03 now runs an economic pre-filter over the APP catalogue (916 documents, 344 high-impact events) rather than tagging all 11,570 documents, and GDELT is now the full 2015–2025 daily series (4,018 days) rather than a 5-day sample. The tables below describe the original Phase 3 run and are kept for historical record — see `docs/research_bible/10_decision_log.md` (2026-07-13 entries) for the current, verified figures.

### Inputs (2026-07-06 snapshot)
| Source | Documents |
|--------|-----------|
| APP presidential documents (core 4 presidents) | 11,570 |
| FOMC meeting decisions (2015–2025) | 89 |
| GDELT daily events (5-day sample — since backfilled to full 2015–2025 history, 4,018 days) | 5 |

### Event Classification (rule-based keyword matching)
| Category | Count |
|----------|-------|
| Monetary | 204 |
| Geopolitical | 1,628 |
| Regulatory | 2,246 |
| Trade | 277 |
| Energy | 159 |
| Health | 449 |
| Labour | 243 |
| Other | 6,423 |

### Sentiment Scoring

The current event catalogue combines 916 FinBERT-scored APP records with 89
structured FOMC records. The resulting 1,005-event label distribution is:

| Label | Count | Share |
|-------|------:|------:|
| Positive | 43 | 4.3% |
| Neutral | 929 | 92.4% |
| Negative | 33 | 3.3% |

> **Note (Sentiment Engine Freeze v1.0, 2026-07-06):** FinBERT is the official APP sentiment engine and the structured FOMC signal is retained for scheduled monetary-policy events. The curated lexicon scorer is a fallback and historical prototype only. The persisted `sentiment_method` value `lexicon` in the causal output is a legacy field label; it does not describe the current combined APP + FOMC treatment. See `docs/research_bible/10_decision_log.md` for the decision trail.

### Outputs
**Processed data** (`data/processed/`):
- `events_tagged.parquet` — unified APP + FOMC event catalogue (1,005 rows)
- `daily_sentiment.parquet` — daily event/sentiment series (739 rows × 18 columns)
- `high_impact_events.parquet` — high-impact event subset (344 rows)
- `gdelt_daily_risk.parquet` — 4,018-day candidate geopolitical-risk control; excluded from the frozen causal DAG and FES v1.1

**Figures** (`reports/figures/`):
- `03a_sentiment_distribution.png` — sentiment breakdown by event type and president
- `03b_sentiment_timeline.png` — sentiment timeline vs SPY price and event volume
- `03c_high_impact_events.png` — high-impact event frequency and sentiment scatter
- `03d_sentiment_by_event_type.png` — 90-day rolling sentiment per event type

### Key Findings
- Presidential communications are predominantly **neutral** in tone — consistent with formal policy language.
- **Monetary and geopolitical** events carry the strongest negative bias, consistent with the market-sensitivity hypothesis.
- FinBERT on APP document titles provides a first-pass signal; full-text scoring remains a documented future improvement.
- **GDELT historical data gap resolved (2026-07-13):** the full 2015–2025 daily series (4,018 days) has been backfilled and merged into `master_dataset.parquet` as a candidate continuous geopolitical-risk control. It is not part of the frozen DoWhy DAG, FES v1.1, or any reported RQ1–RQ3 result. It is also not used as a discrete high-impact event source because the daily aggregate is conceptually a continuous signal rather than a document-level event (`docs/research_bible/10_decision_log.md`, 2026-07-13).

---

## Phase 4 — Causal Analysis (Complete; results below are a historical pre-SEF-v1.0 snapshot — see 2026-07-13 update)

### Method
Event study (AR/CAR, window −5 to +10 trading days) + DoWhy backdoor linear regression with confounders: VIX regime and prior-day return. **Historical note:** the 2026-07-06 snapshot below used a pre-SEF lexicon-era treatment and is retained only as change history. The current 2026-07-13 rerun uses the combined same-day APP FinBERT signal plus structured FOMC sentiment; the persisted `sentiment_method="lexicon"` value is a legacy field label, not the method used by the current run.

### Results (2026-07-06 snapshot — lexicon-based, pre-SEF v1.0)
| Event Type | Mean CAR | Significant |
|------------|----------|-------------|
| Geopolitical | +0.0032 | ✅ p<0.05 |
| Energy | +0.0012 | — |
| Regulatory | +0.0007 | — |
| Trade | −0.0002 | — |
| Monetary | −0.0043 | — |

- **DoWhy causal effect (lexicon — pre-SEF v1.0 treatment definition):** +0.005046 per unit sentiment, 95% CI [+0.0014, +0.0087]
- Only 4.7% of events produce statistically significant price reactions — consistent with market efficiency
- Refutation tests (random common cause, placebo, data subset) passed

> **2026-07-15 current result — RQ1 reporting gate complete:** `04_causal_analysis.ipynb` reports five two-sided event-type mean-CAR tests on 264 observations with 95% t intervals, Cohen's d and Benjamini–Hochberg FDR correction. No interval excludes zero and no null is rejected: minimum raw p=0.1162, minimum BH q=0.5810, and maximum |d|=0.239 (monetary, small). The pooled DoWhy estimate remains **+0.005601, 95% CI [+0.002295, +0.008907], p=0.0009** under the frozen adjustment set. The current conclusion is therefore qualified but final: event-type abnormal-return evidence is null, while the pooled conditional estimate is positive. Event clustering and observational-identification assumptions remain limitations.

### Outputs
**Processed data** (`data/processed/`):
- `car_results.parquet` — 264 current event-study CAR records
- `event_type_statistics.parquet` — five event-type mean-CAR rows with 95% CI, raw p, BH q and Cohen's d
- `rq1_reporting_validation.json` — hash-bound RQ1 statistical-reporting validation (`PASS`)
- `causal_estimates.parquet` — pooled and category backdoor estimates under the combined APP + FOMC treatment

**Figures** (`reports/figures/`):
- `04a_car_by_event_type.png` — CAR distribution and mean by event type
- `04b_car_sentiment_scatter.png` — CAR timeline and sentiment vs CAR OLS
- `04c_causal_estimates.png` — DoWhy estimates with 95% CI
- `04d_car_regime_sentiment.png` — CAR by VIX regime and sentiment direction

---

## Phase 5 — Feature Engineering (Complete; current Feature Matrix FES v1.1)

> **Mission 05B update (2026-07-05):** the feature matrix described below (`model_features.parquet`, 91 engineered / 52 RF-selected) is now a **legacy artefact**. The canonical, frozen feature set is `data/processed/feature_matrix.parquet` (FES v1.0 — 95 features across Market (27)/Macro & VIX (16)/Sentiment (25)/Event (14)/Temporal (5)/Interaction (8) categories, built from `master_dataset.parquet` + `car_results.parquet` under `docs/research_bible/feature_contract.md`). See `docs/research_bible/06_feature_dictionary.md` and `docs/research_bible/10_decision_log.md` (2026-07-05 entry) for the full rebuild rationale. The historical narrative below is retained as the record of what Phase 5 originally produced, not as the current ground truth.
>
> **2026-07-14 Dataset v1.2 checkpoint (historical migration state):** `master_dataset.parquet` became Dataset v1.2 (2,765 × 34; 2,014 train / 751 test), adding three direct occurrence counts. At that checkpoint `feature_matrix.parquet` still remained FES v1.0; the next paragraph records completion of the subsequent Notebook 05 boundary.
>
> **2026-07-14 FES v1.1 freeze:** Notebook 05 completed the controlled rebuild. The canonical matrix contains 92 features (27/16/23/14/5/7 by category), 2,477 rows, and passes validation. `energy`, `labour`, and `monetary_x_rate_cut` were removed because their training-split variance was below the frozen 1e-8 threshold; health/labour/other event-day flags now use direct catalogue-occurrence counts. The FES v1.0 matrix and exception disposition are archived. Notebooks 06–08 have subsequently regenerated and validated the baseline, event-model suite, RQ2/RQ3 evidence, and all publication figures against FES v1.1.

### Feature Matrix (legacy — see note above)
| Group | Features |
|-------|----------|
| Price & returns | 13 |
| Technical indicators | 14 |
| Sentiment | 25 |
| Event indicators | 14 |
| Macro & VIX | 16 |
| Interactions | 8 |
| **Total engineered** | **91** |
| **Selected (RF importance > 0.001)** | **52** |

### Top 10 Features by Importance
| Feature | Importance | Group |
|---------|-----------|-------|
| `mean_car` | 15.9% | Event |
| `return_lag1d` | 10.2% | Price |
| `vix_vs_ma` | 9.6% | Macro |
| `log_return_hi` | 5.4% | Price |
| `vix_change_5d` | 5.4% | Macro |
| `bb_width` | 4.7% | Technical |
| `cum_return_5d` | 4.6% | Price |
| `return_lag3d` | 4.3% | Price |
| `log_return` | 3.2% | Price |
| `momentum_63d` | 2.9% | Technical |

### Train / Test Split
- **Train:** 2015-01-05 → 2022-12-31 (2,013 days, 73%)
- **Test:** 2023-01-01 → 2025-12-29 (750 days, 27%)
- Time-series aware split — no shuffling, no leakage

### Outputs
**Processed data** (`data/processed/`):
- `model_features.parquet` — full feature matrix (2,763 rows × 95 cols)
- `feature_metadata.parquet` — feature importance rankings and group labels
- `scaler.pkl` — StandardScaler fitted on train set only

**Figures** (`reports/figures/`):
- `05a_feature_importance.png` — top 25 features coloured by group
- `05b_feature_correlation.png` — correlation with target and pairwise heatmap
- `05c_target_distribution.png` — target distribution and train/test timeline

---

## Current Project Status

**Pipeline Rebuilt — GDELT Integrated — Analysis Re-verified — Dissertation Phase** (2026-07-13). This is a live status; the authoritative, continuously updated view is `docs/research_bible/14_project_dashboard.md` — this section is a snapshot pointer, not a duplicate source of truth, so it will not be repeated in full here.

- **2026-07-14 FES v1.1 migration complete:** Notebooks 03–08 are complete through the hash-bound visualisation boundary. Notebook 07 regenerated all three event candidates, the 92-feature Random Forest ranking, held-out SHAP, SAP diagnostics, predictions, and corrected comparison tests; a repeat execution reproduced all 13 primary artefact hashes. Notebook 08 then regenerated figures 08a–08d exclusively from validated current inputs and wrote `reports/figures/results_visualisation_validation.json` with status `PASS`.
- **2026-07-13 pipeline rebuild:** Notebooks 01–02 performed a genuine GDELT full-history backfill (`gdelt_daily_summary.parquet`, 4,018 days, 2015-01-01 to 2025-12-31, replacing the previous 5-day proof-of-concept sample), and Notebook 03's economic pre-filter now works from 916 APP documents (344 high-impact events) rather than the full 11,570-document catalogue. `master_dataset.parquet` and every downstream notebook (04–08) were rebuilt, fixed, and re-verified end-to-end. GDELT is retained in the master dataset as a candidate continuous control but is deliberately excluded from the frozen DoWhy DAG and FES v1.1; the dissertation therefore does not claim that GDELT contributes to the reported RQ1–RQ3 estimates.
- **RQ1 evidence base has genuinely changed, not just been re-dated:** the event-study CAR significance test is now a null result (no event type reaches p<0.10 on the current 264-row `car_results.parquet`; the dissertation's original "geopolitical is significant" claim no longer holds against this data). The overall DoWhy causal estimate remains significant (+0.005601, 95% CI [0.002295, 0.008907], p=0.0009), and the `monetary` per-category estimate closely replicates the original frozen figure despite the fully rebuilt upstream pipeline. Whether the dissertation text should be updated to reflect this is an open decision for the Project Director — see the decision log entry for the full analysis.
- **RQ2/RQ3 status:** the current FES v1.1 Random Forest top decile contains macro/VIX features but no event feature (`mean_car` ranks 20th), so the frozen descriptive H2 rule is not met. `Event_LASSO` exactly matches the all-zero baseline; XGBoost and LightGBM are numerically worse on test RMSE and directional accuracy, and no candidate clears either corrected significance leg. H0 is therefore not rejected for RQ3. LightGBM held-out SHAP nevertheless ranks `mean_car` fifth, which is reported as model-specific event signal rather than evidence that H2's joint rule passed.
- **Repository cleanup (2026-07-13):** removed 25GB of raw pre-aggregation GDELT dumps (`gdelt_events.csv`/`.parquet`, superseded by the 220KB daily aggregate) plus editor/OS junk; archived all stale pre-rebuild model/report artefacts to `models/archive/pre_2026-07-13_pipeline_rebuild/` rather than deleting them. Repository size: 25GB → 106MB.
- **Version control:** the repository is git-tracked. The Research Bible is source documentation and is now exposed to Git for the next reviewed commit/push; no blanket ignore rule remains.
- **Security:** a repo-wide secret scan previously found real-looking credentials in `config.yaml` (NewsAPI, FRED keys) and `notebooks/.env` (Hugging Face token + a plaintext username/password in a comment). All are gitignored and none have been committed, but the keys have not been rotated — treat them as compromised until rotated. Full detail in `DATSCI7030_Repository_Audit_Report.ipynb` §1.
- **Notebook 01:** `notebooks/01_data_collection.ipynb` is the single canonical version. A duplicate (`__01_data_collection__.ipynb`) has been moved to `notebooks/archive/` (gitignored, kept locally for reference only, not tracked).
- **Repository hygiene:** folder-level READMEs across `data/`, `models/`, `logs/`, `src/`, `scripts/`, `tests/`, and root `reports/` were audited and corrected 2026-07-06 to match what was then on disk; re-verified consistent against the 2026-07-13 rebuild during the same-day full-pipeline consistency scan (see decision log). One early "Data Collection Report" (`.docx`/`.pdf` pair, 2026-05-08) remains in `reports/` alongside the canonical dissertation draft in `reports/dissertation/` — superseded in scope by the Research Bible and not yet removed; tracked in `docs/research_bible/future_improvements.md`.

---

## License

Academic use only. Not for commercial deployment.
