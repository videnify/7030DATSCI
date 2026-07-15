# 2. Exploratory Data Analysis — What the Raw Data Actually Looks Like

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against the notebook's saved output and the underlying data files, not copied from an earlier draft.
**Originally verified:** 2026-07-14 (notebook execution and figure generation).
**Last reviewed against current pipeline:** 2026-07-15.
**Technical detail:** `notebooks/02_eda.ipynb` · [`05_data_dictionary.md`](../research_bible/05_data_dictionary.md) · [`09_results_log.md`](../research_bible/09_results_log.md) (2026-05/07 EDA entries and the 2026-07-15 scope clarification) · [`statistical_analysis_plan.md`](../research_bible/statistical_analysis_plan.md)

---

## What this stage does

Before building any model, it's worth simply looking at the data — plotting it, checking its statistical properties, and confirming it behaves the way eleven years of real financial and political data should. This stage is that look: it profiles the S&P 500 price series, the VIX "fear index," the macroeconomic indicators, and the volume of presidential communications, and runs a set of standard statistical diagnostic tests (stationarity, normality, autocorrelation, correlation) that later modelling choices depend on.

## Why it matters

Every later stage assumes certain things about the data — for example, that daily returns (not raw prices) are the right scale to model, or that price/technical features alone might not carry much predictive signal. This stage is where those assumptions are actually tested against the data rather than just asserted.

## Inputs

The datasets produced by Notebook 1: SPY prices, VIX, FRED macroeconomic series, FOMC decisions, and the presidential-documents corpus, joined onto a single daily calendar.

## Outputs

Ten diagnostic figures (price trajectory, return distribution, VIX/macro overlay, document-volume plots, correlation heatmap, Q-Q plots, rolling volatility, ACF/PACF) and five descriptive-statistics tables under `reports/tables/`. No modelling data is created at this stage — it is a read-only diagnostic pass.

## What was found

- **S&P 500 (SPY):** raw closing price is non-stationary (ADF p = 0.996), but the daily log return is stationary (ADF p < 0.0001) — confirming log return, not price level, is the correct scale for prediction.
- **Fat tails:** daily log returns show negative skew (−0.59) and heavy excess kurtosis (14.64) — large market moves are far more common than a normal distribution would predict, which is why the project favours robust, tree-based and non-linear models downstream rather than assuming Gaussian behaviour.
- **VIX regime behaviour:** the VIX crosses the "high stress" threshold (≥ 30) on 156 of 2,765 trading days (5.64%), concentrated in the 2020 COVID shock and the 2022 tightening cycle rather than spread evenly — this is why VIX is later used both as a continuous control and as a binary regime flag.
- **Macro series:** raw levels (Fed funds rate, CPI, 10-year Treasury yield) are non-stationary, as expected; their first differences are stationary, confirming the project's choice to feature-engineer differenced macro variables rather than raw levels.
- **Weak autocorrelation:** return autocorrelation decays to negligible levels within 2–3 lags — simple linear autoregressive features have limited value on their own, motivating the project's reliance on event/sentiment signals rather than lagged-return patterns alone.
- **Presidential-document volume vs. market moves — a genuine negative result:** weekly document volume and same-week absolute SPY return show essentially no correlation (r = 0.0469, p = 0.2641, not significant at 5%). In plain terms: a busier week for presidential communication is not, on average, a more volatile week. This result is one of the reasons the project moved toward scoring the *content* (sentiment, event type) of communications rather than counting them.
- **Document composition:** of the 916 economically-relevant presidential documents, spoken addresses (346, 37.8%) and formal statements (264, 28.8%) dominate; by administration, the corpus is heavily weighted toward the Biden term (507 documents, 55.4%), reflecting how much of the study window falls inside that term rather than any deliberate selection.
- **FOMC events:** 89 meetings, clustering into recognisable macro regimes (hikes concentrated in the 2022–2023 tightening cycle; emergency cuts around the 2020 shock).

## What was not found

No evidence that raw communication *volume* predicts market volatility. No evidence that price levels (as opposed to returns) are directly usable for modelling. No new statistical test was introduced beyond what the project's Statistical Analysis Plan pre-specified — this stage validates existing assumptions, it does not create new ones.

## Limitations

This notebook's own working dataframe is loaded from `data/raw/daily_modelling_calendar_v1.parquet` (2,743 rows), a Notebook 1 precursor checkpoint — not the later, canonical `master_dataset.parquet` (2,765 rows) used by every downstream notebook. The two files are closely related and the discrepancy does not change any of the statistical findings above (they were computed correctly on whichever file was actually loaded), but it means this notebook's exact row count should not be quoted as the project's canonical dataset size — see the dated scope clarification in [`09_results_log.md`](../research_bible/09_results_log.md) for the full correction record. This does not affect any RQ1–RQ3 result.

The narrowing of presidential documents from 10,892 collected to 916 "economically relevant" (discussed in the previous stage) has still not been independently re-derived from source rules in this pass — it remains an open verification item, not a defect.

## How this connects to the next stage

The negative "volume doesn't predict volatility" result, together with the fat-tailed, weakly-autocorrelated return series, is the empirical motivation for Notebook 3's shift to classifying *what kind* of event occurred and *how it was said* (sentiment), rather than simply counting events — which is exactly what the next stage builds.

## Where to go for more detail

- The notebook itself: `notebooks/02_eda.ipynb`
- Column definitions: [`05_data_dictionary.md`](../research_bible/05_data_dictionary.md)
- The full statistical results and the dataset-scope correction: [`09_results_log.md`](../research_bible/09_results_log.md)
- The pre-registered test plan these diagnostics follow: [`statistical_analysis_plan.md`](../research_bible/statistical_analysis_plan.md)
