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
- Only SPY, VIX, Federal Funds Rate, CPI, Unemployment, FOMC meetings, and presidential communications are treated as required datasets. QQQ, GLD, TLT are optional and are only kept if they demonstrably improve the analysis for RQ1–RQ3 (see `DATSCI7030_Repository_Audit_Report.ipynb` §8 for the current status of that decision). GDELT is integrated as a continuous daily confounder in `master_dataset.parquet` (full 2015–2025 history, 2026-07-13) but is not yet feature-engineered into `feature_matrix.parquet` — a deliberate scope boundary, not an oversight (see `docs/research_bible/feature_contract.md`).

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
│   │                            # data/feature dictionaries, SAP v1.0, FES v1.0, MCP v1.0, decision log,
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
| 03 | `03_event_detection.ipynb` | Rule-based event-type classification + FinBERT sentiment scoring (SEF v1.0) |
| 04 | `04_causal_analysis.ipynb` | Event study (CAR/CAAR) + DoWhy backdoor causal estimate |
| 05 | `05_feature_engineering.ipynb` | Builds `feature_matrix.parquet` — 95 features across 6 categories (FES v1.0) |
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
| GDELT Project | Global geopolitical event database | Full 2015–2025 daily history (4,018 days), integrated as a continuous confounder in `master_dataset.parquet` since 2026-07-13; not yet fed into `feature_matrix.parquet` or any RQ2/RQ3 model (`docs/research_bible/feature_contract.md` v1.0 scope boundary) | Free, public |

---

## Phase Progress

| Phase | Notebook | Status | Key Output |
|-------|----------|--------|------------|
| 1 | `01_data_collection.ipynb` | ✅ Complete — **GDELT full-history backfill added 2026-07-13** (4,018 days, 2015–2025, replacing the 5-day sample) | 5 raw parquets in `data/raw/`, incl. `gdelt_daily_summary.parquet` |
| 2 | `02_eda.ipynb` | ✅ Complete | EDA figures in `reports/figures/` |
| 3 | `03_event_detection.ipynb` | ✅ Complete — **rebuilt 2026-07-13**: economic pre-filter now scopes the APP catalogue to 916 documents (344 high-impact events); GDELT merged as a continuous confounder, not a catalogue event. Built as `03_event_detection_revised.ipynb` during the rebuild; the pre-rebuild file at this name was archived to `notebooks/archive/` and this one promoted to canonical 2026-07-14, closing the naming ambiguity flagged earlier this session. | 4 processed parquets, incl. `gdelt_daily_risk.parquet`, 4 figures |
| 4 | `04_causal_analysis.ipynb` | ✅ Complete — **re-run 2026-07-13** against the rebuilt pipeline; event-study significance test is now a null result, overall DoWhy estimate remains significant (see Phase 4 update above) | `car_results.parquet` (264 rows), `causal_estimates.parquet`, 4 figures |
| 5 | `05_feature_engineering.ipynb` | ✅ Complete — **rebuilt 2026-07-06 to reproduce FES v1.0 exactly** (Mission 05-07 Reproducibility Rebuild); **`master_dataset.parquet` re-frozen as v1.1 on 2026-07-13** after the GDELT/Notebook-03 rebuild (95-feature composition unchanged); legacy `model_features.parquet` output no longer produced by this notebook | `feature_matrix.parquet`, `feature_profile.json`, `feature_matrix_validation.json` |
| 6 | `06_model_training.ipynb` | ✅ Complete — **rebuilt 2026-07-06 to reproduce `Baseline_LASSO` exactly** (MCP v1.0) from `feature_matrix.parquet` only; **re-verified 2026-07-13** against the rebuilt feature matrix (RMSE/Dir_Acc closely track the frozen figures) | `models/baseline/baseline_lasso.joblib`, `baseline_model_metadata.json`, `reports/baseline/baseline_metrics.json`, `baseline_predictions.parquet` |
| 7 | `07_model_evaluation.ipynb` | ✅ Complete — **rebuilt 2026-07-06 to reproduce `Event_LASSO`/`XGBoost`/`LightGBM` and the RQ3 verdict exactly**; **re-verified 2026-07-13**, with a NaN-scaling bug fixed and SHAP/prediction outputs rebuilt — `Event_LASSO` now collapses to the same all-zero coefficients as the baseline on this data (DM statistic undefined) | `reports/model_comparison/model_comparison.parquet`, `statistical_tests.json`, `feature_importance.parquet` |
| 8 | `08_results_visualisation.ipynb` | ✅ Complete — **rebuilt 2026-07-06 (Results Visualisation Freeze v1.0)**: all four figures (08a-08d) now read exclusively from the canonical pipeline; no legacy dependency remains; **required zero code changes in the 2026-07-13 re-verification** | 4 publication figures (300 dpi) |

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

Two methods were evaluated:

| Label | FinBERT | % | Lexicon | % |
|-------|---------|---|---------|---|
| Positive | 315 | 2.7% | 1,687 | 14.5% |
| Neutral | 11,077 | 95.3% | 8,512 | 73.1% |
| Negative | 237 | 2.0% | 1,430 | 12.3% |
| Mean score | +0.0067 | — | — | — |

> **Note (Sentiment Engine Freeze v1.0, 2026-07-06):** FinBERT is the project's official primary sentiment engine — used to construct `events_tagged.parquet`, `daily_sentiment.parquet`, and all downstream datasets. FinBERT was trained on financial news headlines, so the high neutral rate (95.3%) on formal presidential language reflects a known domain mismatch (see `docs/research_bible/11_limitations.md` L6). The curated lexicon scorer is retained only as a fallback mechanism (used when FinBERT is unavailable) and historical prototype — it is not the primary sentiment method for this project. See `docs/research_bible/10_decision_log.md` for the full decision.

### Outputs
**Processed data** (`data/processed/`):
- `events_tagged.parquet` — unified event catalogue (11,664 rows)
- `daily_sentiment.parquet` — daily sentiment time series (3,352 days × 15 cols)
- `high_impact_events.parquet` — high-impact events for causal event study (4,100 events)
- `gdelt_daily_risk.parquet` — GDELT daily geopolitical risk scores

**Figures** (`reports/figures/`):
- `03a_sentiment_distribution.png` — sentiment breakdown by event type and president
- `03b_sentiment_timeline.png` — sentiment timeline vs SPY price and event volume
- `03c_high_impact_events.png` — high-impact event frequency and sentiment scatter
- `03d_sentiment_by_event_type.png` — 90-day rolling sentiment per event type

### Key Findings
- Presidential communications are predominantly **neutral** in tone — consistent with formal policy language.
- **Monetary and geopolitical** events carry the strongest negative bias, consistent with the market-sensitivity hypothesis.
- FinBERT on document titles provides a first-pass signal; full-text scraping (Phase 3b) expected to sharpen discrimination.
- **GDELT historical data gap resolved (2026-07-13):** the full 2015–2025 daily series (4,018 days) has been backfilled and is now merged into `master_dataset.parquet` as a continuous confounder — see the Current Project Status section above. It is not yet used as a discrete high-impact event source: a direct check found the daily-averaged GDELT tone signal never reaches the existing high-impact threshold for any of the 4,018 days, so it was deliberately kept out of the event catalogue rather than force-fit (`docs/research_bible/10_decision_log.md`, 2026-07-13).

---

## Phase 4 — Causal Analysis (Complete; results below are a historical pre-SEF-v1.0 snapshot — see 2026-07-13 update)

### Method
Event study (AR/CAR, window −5 to +10 trading days) + DoWhy backdoor linear regression with confounders: VIX regime, prior-day return. Treatment (as computed for this already-frozen result, pre-SEF v1.0): lexicon sentiment. Robustness check: FinBERT sentiment. **Note:** Sentiment Engine Freeze v1.0 (2026-07-06) subsequently ratified FinBERT as the project's official primary sentiment engine going forward; this specific causal estimate is a historical result and has not been re-run.

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

> **2026-07-13 update — RQ1 evidence base has genuinely changed, not just been re-dated:** `04_causal_analysis.ipynb` was re-run end-to-end on the rebuilt, FinBERT-only pipeline (916 APP documents, 344 high-impact events, `car_results.parquet` now 264 rows). The event-study CAR significance test is now a **null result** — no event type reaches significance at even p<0.10 (geopolitical p=0.293, monetary closest at p=0.116), directly contradicting the "geopolitical is significant" finding above. The overall DoWhy causal estimate remains significant: **+0.005601, 95% CI [+0.002295, +0.008907], p=0.0009**. The `monetary` per-category causal estimate (+0.007094, CI [+0.002577, +0.010952]) closely replicates the original frozen figure despite the fully rebuilt upstream data — a genuine robustness signal. Two other per-category estimates (`geopolitical`, `energy`) rest on only `n_events=1` each and should not be treated as reliable. Whether the dissertation text should be updated to reflect this changed evidence base is an open decision for the Project Director — full analysis in `docs/research_bible/10_decision_log.md` (2026-07-13).

### Outputs
**Processed data** (`data/processed/`):
- `car_results.parquet` — 1,796 event CAR records
- `causal_estimates.parquet` — backdoor causal effect per event type

**Figures** (`reports/figures/`):
- `04a_car_by_event_type.png` — CAR distribution and mean by event type
- `04b_car_sentiment_scatter.png` — CAR timeline and sentiment vs CAR OLS
- `04c_causal_estimates.png` — DoWhy estimates with 95% CI
- `04d_car_regime_sentiment.png` — CAR by VIX regime and sentiment direction

---

## Phase 5 — Feature Engineering (Complete; superseded 2026-07-05 by Feature Matrix v1.0)

> **Mission 05B update (2026-07-05):** the feature matrix described below (`model_features.parquet`, 91 engineered / 52 RF-selected) is now a **legacy artefact**. The canonical, frozen feature set is `data/processed/feature_matrix.parquet` (FES v1.0 — 95 features across Market (27)/Macro & VIX (16)/Sentiment (25)/Event (14)/Temporal (5)/Interaction (8) categories, built from `master_dataset.parquet` + `car_results.parquet` under `docs/research_bible/feature_contract.md`). See `docs/research_bible/06_feature_dictionary.md` and `docs/research_bible/10_decision_log.md` (2026-07-05 entry) for the full rebuild rationale. The historical narrative below is retained as the record of what Phase 5 originally produced, not as the current ground truth.
>
> **2026-07-13 update:** `master_dataset.parquet` was rebuilt as v1.1 (see decision log) after the GDELT full-history backfill and Notebook 03's economic pre-filter changed its upstream inputs — row/split counts came out identical to the frozen v1.0 figures (2,765 rows; 2,014 train / 751 test), since only the event/sentiment/GDELT *composition* changed, not the SPY trading calendar. `feature_matrix.parquet`'s 95-feature, 6-category composition is unchanged by this rebuild — GDELT columns are present in `master_dataset.parquet` but deliberately not yet feature-engineered (v1.0 scope boundary, see `feature_contract.md`).

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

- **2026-07-13 pipeline rebuild:** Notebooks 01–02 performed a genuine GDELT full-history backfill (`gdelt_daily_summary.parquet`, 4,018 days, 2015-01-01 to 2025-12-31, replacing the previous 5-day proof-of-concept sample), and Notebook 03's economic pre-filter now works from 916 APP documents (344 high-impact events) rather than the full 11,570-document catalogue. `master_dataset.parquet` (v1.1) and every downstream notebook (04–08) were rebuilt, fixed, and re-verified end-to-end against this new data — full detail and every individual fix in `docs/research_bible/10_decision_log.md` (2026-07-13 entries). GDELT is wired in as a continuous daily confounder (the same role VIX occupies), not a discrete catalogue event, and is **not yet** feature-engineered into `feature_matrix.parquet` (a deliberate v1.0 scope boundary, see `docs/research_bible/feature_contract.md`).
- **RQ1 evidence base has genuinely changed, not just been re-dated:** the event-study CAR significance test is now a null result (no event type reaches p<0.10 on the current 264-row `car_results.parquet`; the dissertation's original "geopolitical is significant" claim no longer holds against this data). The overall DoWhy causal estimate remains significant (+0.005601, 95% CI [0.002295, 0.008907], p=0.0009), and the `monetary` per-category estimate closely replicates the original frozen figure despite the fully rebuilt upstream pipeline. Whether the dissertation text should be updated to reflect this is an open decision for the Project Director — see the decision log entry for the full analysis.
- **RQ3 result:** `Baseline_LASSO` and `Event_LASSO` both collapse to all-zero coefficients on the current feature matrix, making them numerically identical and their Diebold-Mariano comparison undefined (`p=nan`) — a genuine model output, not a bug. See the decision log for the XGBoost/LightGBM comparison.
- **Repository cleanup (2026-07-13):** removed 25GB of raw pre-aggregation GDELT dumps (`gdelt_events.csv`/`.parquet`, superseded by the 220KB daily aggregate) plus editor/OS junk; archived all stale pre-rebuild model/report artefacts to `models/archive/pre_2026-07-13_pipeline_rebuild/` rather than deleting them. Repository size: 25GB → 106MB.
- **Version control:** repository is git-tracked; the `docs/research_bible/` governance layer and this rebuild's changes are committed.
- **Security:** a repo-wide secret scan previously found real-looking credentials in `config.yaml` (NewsAPI, FRED keys) and `notebooks/.env` (Hugging Face token + a plaintext username/password in a comment). All are gitignored and none have been committed, but the keys have not been rotated — treat them as compromised until rotated. Full detail in `DATSCI7030_Repository_Audit_Report.ipynb` §1.
- **Notebook 01:** `notebooks/01_data_collection.ipynb` is the single canonical version. A duplicate (`__01_data_collection__.ipynb`) has been moved to `notebooks/archive/` (gitignored, kept locally for reference only, not tracked).
- **Repository hygiene:** folder-level READMEs across `data/`, `models/`, `logs/`, `src/`, `scripts/`, `tests/`, and root `reports/` were audited and corrected 2026-07-06 to match what was then on disk; re-verified consistent against the 2026-07-13 rebuild during the same-day full-pipeline consistency scan (see decision log). One early "Data Collection Report" (`.docx`/`.pdf` pair, 2026-05-08) remains in `reports/` alongside the canonical dissertation draft in `reports/dissertation/` — superseded in scope by the Research Bible and not yet removed; tracked in `docs/research_bible/future_improvements.md`.

---

## License

Academic use only. Not for commercial deployment.
