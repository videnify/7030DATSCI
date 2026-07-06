# 08 — Figures Plan

**Purpose:** Inventory of every figure produced by the pipeline, which notebook generates it, and which research question it supports — so no figure ends up in the dissertation without a traceable purpose, and no notebook silently produces a figure nobody uses.
**Owner:** Ibrahim Haroun.
**Dependencies:** `15_traceability_matrix.md` (this document feeds that matrix's figure column); `03_methodology.md`.
**Update Frequency:** Update whenever a notebook adds, removes, or renames a figure.
**Relation to Dissertation:** Direct source for the dissertation's List of Figures and for deciding which figures earn a place in the main text vs. an appendix.

---

## Phase 2 — EDA (`02_eda.ipynb`) — 12 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `01_correlation_analysis.png` | RQ2 (context) | Cross-asset/macro correlation heatmap |
| `01_gdelt_distributions.png` | RQ1 (context) | GDELT sample distributions — caveat with the 5-day sample limitation when used |
| `01_price_history.png` | Context | SPY price history 2015–2025 |
| `01_vix.png` | RQ1/RQ2 (context) | VIX series |
| `02a_normalised_prices.png` | Context | SPY/QQQ/GLD/TLT normalised — only asset actually discussed downstream is SPY (see `11_limitations.md` re: QQQ/GLD/TLT) |
| `02b_return_distributions.png` | RQ3 (context) | Return distribution shape — informs model-family choice |
| `02c_rolling_volatility.png` | RQ2 | Motivates volatility-regime features |
| `02d_vix_series.png` | RQ1/RQ2 | VIX as confounder/feature |
| `02e_macro_indicators.png` | RQ2 | Macro feature time series |
| `02f_return_vix_corr.png` | RQ2 | Return–VIX correlation, motivates `vix_vs_ma` |
| `02g_app_doc_distribution.png` | RQ1 | Presidential document volume over time |
| `02h_app_by_president.png` | RQ1 (context) | Document counts by president |
| `02i_docs_vs_returns.png` | RQ1 | Visual motivation for the event study |
| `02j_fomc_distribution.png` | RQ1 | FOMC meeting frequency |
| `02k_fomc_event_window.png` | RQ1 | Example FOMC event window |
| `02l_combined_timeline.png` | RQ1 | Combined event/price timeline |

## Phase 2 — EDA, SAP v1.0 implementation (`02_eda.ipynb` §9, Mission 05A, added 2026-07-05) — 6 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `02m_descriptive_distributions.png` | Context (RQ1/RQ2) | Histogram+KDE for `log_return`, `vix`, `spy_close`, `overall_mean_sentiment` |
| `02n_qq_plots.png` | Context | QQ-plots vs. Normal for `log_return`, `vix` — visual normality check |
| `02o_boxplots.png` | Context | Boxplots for `log_return`, `vix`, `overall_mean_sentiment`, `total_events` — outliers retained per policy |
| `02p_rolling_stationarity.png` | RQ1/RQ2 | Rolling mean/std (21d/63d) for `log_return`, VIX rolling mean — also serves as the required time-series visualisation |
| `02q_acf_pacf.png` | RQ2 | ACF/PACF for `log_return`, 30 lags — motivates the existing lag feature set |
| `02r_correlation_heatmap.png` | RQ2 | Pearson vs. Spearman heatmap, full numeric column set |

## Phase 3 — Event Detection & NLP (`03_event_detection.ipynb`) — 4 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `03a_sentiment_distribution.png` | RQ1/RQ2 | Sentiment breakdown by event type and president |
| `03b_sentiment_timeline.png` | RQ1 | Sentiment vs. SPY price and event volume |
| `03c_high_impact_events.png` | RQ1 | High-impact event frequency and sentiment scatter |
| `03d_sentiment_by_event_type.png` | RQ2 | 90-day rolling sentiment per event type — motivates `sent_mean_*` features |

## Phase 4 — Causal Analysis (`04_causal_analysis.ipynb`) — 4 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `04a_car_by_event_type.png` | **RQ1 (primary evidence)** | CAR distribution/mean by event type |
| `04b_car_sentiment_scatter.png` | RQ1 | CAR timeline and sentiment-vs-CAR OLS |
| `04c_causal_estimates.png` | **RQ1 (primary evidence)** | DoWhy estimates with 95% CI |
| `04d_car_regime_sentiment.png` | RQ1 | CAR by VIX regime and sentiment direction |

## Phase 5 — Feature Engineering (`05_feature_engineering.ipynb`) — 3 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `05a_feature_importance.png` | **RQ2 (primary evidence)** | Top 25 features coloured by group |
| `05b_feature_correlation.png` | RQ2 | Feature-target correlation and pairwise heatmap |
| `05c_target_distribution.png` | RQ3 (context) | Target distribution + train/test timeline |

## Phase 6 — Model Training (`06_model_training.ipynb`) — 4 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `06a_model_comparison.png` | **RQ3 (primary evidence — currently incomplete, no baseline)** | Update once `07_model_plan.md` baseline is added |
| `06b_predicted_vs_actual.png` | RQ3 | Predicted vs. actual scatter, best model |
| `06c_shap_summary.png` | **RQ2 (primary evidence)** | Global SHAP summary |
| `06d_residual_analysis.png` | RQ3 | Residual diagnostics, ties to `models/residual_diagnostics.json` |

## Phase 7 — Model Evaluation (`07_model_evaluation.ipynb`) — 4 figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `07a_extended_metrics.png` | RQ3 | RMSE/MAE/R²/Dir.Acc/IC/Hit Rate by quintile |
| `07b_residual_analysis.png` | RQ3 | Deeper residual diagnostics |
| `07c_shap_deepdive.png` | RQ2 | SHAP force/dependence/interaction plots |
| `07d_strategy_performance.png` | RQ3 (illustrative only) | **Caveat required:** not a net-of-costs backtest; do not present as a trading-strategy claim (see `11_limitations.md`) |

## Phase 8 — Results Visualisation (`08_results_visualisation.ipynb`) — 4 integrated figures

| Figure | Supports | Notes |
|--------|----------|-------|
| `08a_event_landscape.png` | RQ1 | Event volume, type distribution, sentiment over time, president breakdown |
| `08b_causal_evidence.png` | **RQ1 (summary evidence)** | CAR distributions, DoWhy estimates with CI, sentiment–CAR scatter, regime interaction |
| `08c_predictive_pipeline.png` | **RQ2 + RQ3 (summary evidence)** | **Rebuilt 2026-07-06 (Results Visualisation Freeze v1.0)** — feature importance by category (FES v1.0, `feature_importance.parquet`), 4-model comparison including `Baseline_LASSO` (`model_comparison.parquet`), SHAP top drivers (`shap_values_event_lasso.parquet`), explicit RQ3 verdict annotation (H0₃ not rejected). No legacy input remains. |
| `08d_full_dashboard.png` | All three RQs | **Rebuilt 2026-07-06 (Results Visualisation Freeze v1.0)** — integrated timeline sourced from `feature_matrix.parquet` + `reports/model_comparison/event_model_predictions.parquet`; signal/strategy panels use `Event_LASSO` as the representative (not "best") event-enhanced model, explicitly captioned as illustrative only (same caveat as `07d`) with the RQ3 null result stated on the figure itself. |

## Architecture diagrams (`docs/architecture/`) — not data-driven, but part of the figure inventory

**Rebuilt 2026-07-06 (Architecture SVG Cleanup & Rebuild mission).** Canonical set (6 files, all support the dissertation Methodology chapter, not a specific RQ's evidence — see `docs/architecture/README.md` for the full use-in-dissertation mapping):

| File | Chapter use |
|------|-------------|
| `project_pipeline.svg` | Ch.3 pipeline overview |
| `data_lineage.svg` | Ch.3 §3.1 data sources / reproducibility appendix |
| `research_governance.svg` | Ch.3 governance/versioning figure |
| `rq_traceability.svg` | Ch.1 or Ch.4 opening figure — see `docs/architecture/README.md`'s note on the RQ1/RQ2 lane correction |
| `modelling_flow.svg` | Ch.3 §3.5 model specification / Ch.4 §4.4 model comparison |
| `car_formula.svg` | Ch.3 event-study equation reference (updated 2026-07-06 — ARIMA reference removed) |

11 diagrams describing a superseded ARIMA/intervention-analysis methodology (never implemented in the frozen pipeline) were archived to `docs/architecture/archive/`, and 2 files misattributed to a different project ("GOVFIN") were deleted. None of the archived/deleted diagrams should be cited in the dissertation.

---

## Figures requiring an update once the baseline model lands (`07_model_plan.md`)

**Resolved 2026-07-06 (Results Visualisation Freeze v1.0)** for `08c_predictive_pipeline.png` and `08d_full_dashboard.png` — both now show the full 4-model comparison including `Baseline_LASSO`, sourced from `reports/model_comparison/`. `06a_model_comparison.png` (produced by `06_model_training.ipynb`) was outside this mission's scope (Notebook 08 only, per its brief) — its status was not re-verified here and remains to be checked in a future pass if it is still cited anywhere.

## Figures requiring a caveat in the dissertation text

`07d_strategy_performance.png`, `08d_full_dashboard.png` — any cumulative-return/strategy-style panel must be captioned as illustrative directional-signal visualisation, not a claim of tradeable profit net of transaction costs and slippage (see `00_project_overview.md` "What this project explicitly does NOT attempt" and `11_limitations.md`). `08d`'s panel 5 now states this caveat directly on the figure itself, alongside the RQ3 null-result statement.
