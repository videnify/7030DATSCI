# DATSCI7030 — Causal Event-Driven Market Impact Modelling

> **Module:** 7030DATSCI — Data Science Project
> **Author:** Ibrahim Haroun
> **Institution:** Liverpool John Moores University
> **Year:** 2025–2026
> **Version:** 3.0 — Dissertation Accepted, Repository Frozen (2026-07-16)

---

## Project status: Frozen pending assessment feedback
**Freeze date:** 2026-07-16

The dissertation is accepted and this repository is frozen as the submitted MSc Data Science project state. No analytical, methodological, or evidential change should be made until assessment feedback is received. See [`docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md`](docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md) for the full freeze declaration, protected-artefact hashes, and reopening conditions.

---

## Research summary

This project investigates the **causal impact of real-world events** — presidential communications and Federal Reserve (FOMC) announcements — on the S&P 500 (via SPY), combined with a **predictive layer** testing whether event-derived information improves next-day return prediction over a market-only baseline. The methodology combines an event study (cumulative abnormal returns), DoWhy backdoor causal inference, rule-based event classification with FinBERT sentiment scoring, and a regularised/tree-based predictive model comparison with SHAP explainability.

## Research questions

| # | Question |
|---|----------|
| RQ1 | Do presidential communications and Federal Reserve announcements produce statistically significant abnormal returns in the S&P 500? |
| RQ2 | Which event-derived and macroeconomic features contribute most to predicting next-day S&P 500 returns? |
| RQ3 | Do event-enhanced models (LASSO, XGBoost, LightGBM) improve next-day S&P 500 return prediction relative to a market-only LASSO baseline, under a pre-registered Bonferroni-corrected promotion protocol? |

## Findings (honest, as reported in the dissertation)

- **RQ1 — qualified:** no event-type mean-CAR null is rejected after Benjamini–Hochberg FDR correction across five event-type tests (minimum q = 0.581, maximum |Cohen's d| = 0.239), while the separate pooled DoWhy estimate remains positive and significant (+0.005601, 95% CI [+0.002295, +0.008907], p = 0.0009), conditional on the frozen DAG and no-unmeasured-confounding assumption.
- **RQ2 — null:** Random Forest importance is dominated by market and macroeconomic features; no event feature appears in the top ten.
- **RQ3 — null:** the market-only LASSO baseline and the event-enhanced LASSO are identical constant predictors on the held-out test set; XGBoost and LightGBM are worse on RMSE and directional accuracy; no candidate clears the Bonferroni-corrected two-leg promotion rule.

The project reports these null predictive results directly rather than overstating a weak signal — see the dissertation's Discussion and Conclusions for full interpretation.

## Eight-stage notebook workflow

Each stage reads only what the previous stage wrote — see [`notebooks/README.md`](notebooks/README.md) for inputs/outputs, frozen-snapshot behaviour, and the external-data warning before considering a re-run.

| # | Notebook | Purpose |
|---|----------|---------|
| 01 | `01_data_collection.ipynb` | Pull price data (yfinance), presidential documents (APP), macro indicators (FRED), FOMC dates, GDELT |
| 02 | `02_eda.ipynb` | Exploratory data analysis, distributions, stationarity, correlation |
| 03 | `03_event_detection.ipynb` | Rule-based event classification + FinBERT sentiment scoring |
| 04 | `04_causal_analysis.ipynb` | Event study (CAR/CAAR) + DoWhy backdoor causal estimate |
| 05 | `05_feature_engineering.ipynb` | Builds the frozen 92-feature FES v1.1 matrix |
| 06 | `06_model_training.ipynb` | Trains the market-only LASSO baseline (MCP v1.0) |
| 07 | `07_model_evaluation.ipynb` | Trains event-enhanced candidates; DM/two-proportion comparison; RQ3 verdict |
| 08 | `08_results_visualisation.ipynb` | Final publication-quality figures from the validated pipeline boundary |

## Repository structure

```
DATSCI7030/
├── data/                # raw/interim/processed/external — gitignored, reproducible via notebooks 01→
├── notebooks/           # eight canonical numbered notebooks + archive/ (superseded, local-only)
├── src/                 # reusable Python modules
├── models/               # trained model binaries — gitignored, reproducible via notebooks 06-07
├── scripts/              # standalone helper/build/figure-generation scripts
├── tests/                # unit tests for src/ modules
├── reports/
│   ├── figures/          # charts/plots — gitignored, regenerate from notebooks or scripts/generate_appendix_*.py
│   ├── dissertation/      # accepted dissertation DOCX/PDF (gitignored, hash-verified) + archive of earlier versions
│   ├── stakeholder/       # plain-language stakeholder report
│   └── finalisation/      # repository baseline/freeze/manifest records (this cleanup pass)
├── docs/
│   ├── research_bible/    # governing documentation — start at docs/research_bible/00_project_freeze.md
│   ├── stakeholder_report/  # per-stage plain-language stakeholder pages (source for reports/stakeholder/)
│   └── architecture/      # canonical pipeline/governance/model SVG diagrams
├── config.yaml            # project configuration incl. API keys — gitignored, never commit
├── requirements.txt        # pinned Python dependencies
└── .gitignore
```

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add real API keys to a local config.yaml / notebooks/.env (both gitignored — never commit real keys)

# 4. Open notebooks in numbered order — each stage reads only what the previous stage wrote
jupyter lab
```

See [`docs/research_bible/ENVIRONMENT_2026-07-16.md`](docs/research_bible/ENVIRONMENT_2026-07-16.md) for the exact validated Python version, package versions, and known-unsupported configurations.

## Data availability

Raw, interim, processed, and external data are **never committed to Git** (see `.gitignore`) — every file under `data/` is reproducible by re-running the numbered notebooks in order from `data/raw/` onward, using free/keyless sources for the required datasets (yfinance, APP, FOMC dates). FRED and NewsAPI keys are optional and only needed for the macro/legacy-news paths. Trained model binaries (`models/`) are likewise gitignored and reproducible via Notebooks 06–07. See `data/README.md` and each `data/*/README.md` for per-file schema, row counts, and provenance.

## Reproduction boundaries

The repository is **frozen** (see the status banner above): notebooks should not be re-run as part of normal use — their saved outputs are the evidential record cited by the dissertation. `model.random_seed: 42` in `config.yaml` and `TimeSeriesSplit` throughout make the pipeline deterministic if a genuinely new, approved re-run is ever needed (see the reopening conditions in the freeze document). GDELT is retained in `master_dataset.parquet` as a candidate contextual control but is deliberately excluded from the frozen causal DAG and FES v1.1 — no reported RQ1–RQ3 result depends on it.

## Tests and validation

```bash
python -m pytest tests/ -v
```
18 tests currently pass (10 active event-study reference tests, 4 legacy-reference tests, 4 feature-engineering tests). Every governed artefact (dataset, feature matrix, model set) is additionally checked against a stored SHA-256 hash and a machine-readable validation JSON file at build time — see `docs/research_bible/13_validation_checklist.md` and `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`.

## Architecture

Canonical pipeline/governance/model diagrams: [`docs/architecture/`](docs/architecture/README.md) (data lineage, modelling flow, research governance, RQ traceability, CAR formula reference).

## Research Bible

The full governing documentation set — research questions, hypotheses, methodology, statistical analysis plan, dataset/feature/model contracts, decision log, results log, limitations, and this project's freeze declarations. **Start at** [`docs/research_bible/00_project_freeze.md`](docs/research_bible/00_project_freeze.md) (methodology governance) and [`docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md`](docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md) (submission freeze). Live status: [`docs/research_bible/14_project_dashboard.md`](docs/research_bible/14_project_dashboard.md).

## Stakeholder report

A plain-language, non-technical summary for a non-specialist audience: [`reports/stakeholder/`](reports/stakeholder/) (source pages: [`docs/stakeholder_report/`](docs/stakeholder_report/)).

## Dissertation

Accepted 2026-07-16: `reports/dissertation/2026-07-16-7030DATSCI.docx` / `.pdf` (gitignored; SHA-256-verified — see [`reports/dissertation/README.md`](reports/dissertation/README.md) for hashes and the archive of earlier versions).

## Large-file exclusions

Not committed to GitHub, by design (see `.gitignore`): raw/interim/processed data (`data/*`), trained model binaries (`models/*`, `*.joblib`), the dissertation and other Office binaries (`*.docx`, `*.pdf` under `reports/`), generated report tables/figures exports, `notebooks/archive/` (superseded drafts), and all OS/editor/cache junk. Expected paths, schemas, and reproduction commands for every excluded artefact are documented in the relevant folder's `README.md`. Nothing excluded is required to read the code, notebooks (with their saved outputs), or documentation.

## Feedback / reopening policy

This repository is frozen pending assessment feedback (see the status banner above). Any post-feedback change must begin with a new dated `docs/research_bible/10_decision_log.md` entry, a new version identifier for whatever it touches, and a documented impact assessment — never a silent edit to a frozen artefact.

## Licence

MIT — see [`LICENSE`](LICENSE).

## Citation

If referencing this work, cite as: Haroun, I. (2026). *Causal Event-Driven Market Impact Modelling* (MSc Data Science dissertation). Liverpool John Moores University.
