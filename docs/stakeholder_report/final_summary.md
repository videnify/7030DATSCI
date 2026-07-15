# Executive Summary — What This Project Found

**Status:** ✅ Written 2026-07-15, after all eight pipeline stages were verified and this folder was completed.
**Audience:** Anyone who wants the headline answer without reading all eight stage pages.
**Technical detail:** see the stage-by-stage pages linked throughout, and the full technical record in [`docs/research_bible/`](../research_bible/README.md).

---

## What this project set out to do

Test whether presidential communications, Federal Reserve decisions, and global geopolitical signals have a measurable relationship with U.S. stock market (S&P 500) behaviour — and, separately, whether that relationship can be turned into a better next-day return prediction than a plain market-only model. The project asks three distinct research questions and answers each on its own terms, rather than blending them into one convenient story.

## The three questions, answered honestly

**RQ1 — Do specific event types produce abnormal market reactions?** No, not once you correct for testing five event categories at once (Benjamini–Hochberg FDR correction). The strongest single category (monetary events) has a small effect size and a corrected p-value nowhere near significance. See [Stage 4](04_causal_analysis.md).

**Separately — does a pooled causal estimate show sentiment relates to next-day returns?** A small but genuine one: +0.0056 in next-day return units, with a 95% confidence interval that excludes zero (p = 0.0009), once VIX regime and the prior day's return are statistically controlled for. This is a different statistical question from RQ1 above — an event-study null result and a significant pooled causal association can both be true at once, and both are reported. See [Stage 4](04_causal_analysis.md).

**RQ2 — Which features matter most to a predictive model?** Ordinary market/technical features (recent returns, VIX) dominate the feature-importance ranking — not the event or sentiment features. This does not contradict the causal finding above; feature importance for prediction and causal relevance are genuinely different questions, and this project keeps them separate rather than conflating "important to the model" with "causally important." See [Stage 7](07_model_evaluation.md).

**RQ3 — Do event-enhanced models beat a market-only baseline at prediction?** No. Under a strict, pre-registered, Bonferroni-corrected statistical promotion rule, none of the three event-enhanced candidates (a LASSO regression, XGBoost, LightGBM) statistically beats the market-only baseline on both required legs (prediction error and directional accuracy). One candidate (`Event_LASSO`) collapses to the exact same constant prediction as the baseline; the two tree-based models are measurably worse. See [Stages 6](06_model_training.md) and [7](07_model_evaluation.md).

## Why these results are still valuable

A null predictive result, honestly reported with a rigorous pre-registered test, is a real scientific finding — it tells you that a plausible, intuitively appealing hypothesis (political/geopolitical sentiment should help predict stock returns) does not hold up once you demand out-of-sample, statistically corrected evidence. This project treats that null result as worth reporting clearly, not as something to work around or downplay.

## What this system is, and is not

This is a decision-support research project, not a trading system. No result in this repository should be read as investment advice, and no model here is claimed to produce a profitable trading strategy. The distinction between association, abnormal return, causal estimate, and predictive advantage is deliberately kept sharp throughout this report and the underlying dissertation, because collapsing these into one another is the most common way this kind of finding gets overstated.

## Where the evidence lives

Every number in this summary traces back to a specific stage page (linked above), which in turn points to the exact notebook, artefact, and validation file behind it. If a number here and a number in the underlying data ever disagree, the data is correct and this page is stale.

## Read the stages in order

1. [Data Collection](01_data_collection.md)
2. [Exploratory Data Analysis](02_eda.md)
3. [Event Detection & Sentiment](03_event_detection.md)
4. [Causal Analysis](04_causal_analysis.md)
5. [Feature Engineering](05_feature_engineering.md)
6. [Model Training](06_model_training.md)
7. [Model Evaluation](07_model_evaluation.md)
8. [Results Visualisation](08_results_visualisation.md)
