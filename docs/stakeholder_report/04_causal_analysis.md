# 4. Causal Analysis — Did These Events Actually Move the Market?

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against the current parquet/JSON artefacts, not copied from an earlier draft.
**Originally verified:** 2026-07-13 (live end-to-end execution); RQ1 multiplicity-corrected reporting frozen 2026-07-15; pooled-estimate persistence and live re-execution confirmed 2026-07-15.
**Last reviewed against current pipeline:** 2026-07-15.
**Technical detail:** `notebooks/04_causal_analysis.ipynb` · [`09_results_log.md`](../research_bible/09_results_log.md) · [`10_decision_log.md`](../research_bible/10_decision_log.md) (2026-07-15 entries) · `data/processed/causal_overall_estimate.json`

---

## What this stage does

This stage asks two related but genuinely different questions:

1. **Event study:** around each high-impact event, did the market move abnormally compared to what it would normally have done? (This is a description of what happened, not a causal claim.)
2. **Causal analysis:** once you account for other things that could explain the same market move (general market stress, the previous day's return), does the presidential/FOMC sentiment signal still show a genuine, independent relationship with next-day returns?

## Why it matters

These two questions are easy to conflate but answer different things — a statistically significant abnormal return around an event does not by itself prove the event *caused* the move, and a significant causal estimate under one set of assumptions is not the same as a reliable trading signal. Keeping these separate, and being honest about which is which, is central to how this project reports its findings.

## Inputs

The 344-event high-impact subset and the daily sentiment series produced in Stage 3, joined to daily SPY/VIX price data.

## Outputs

- `car_results.parquet` — 264 usable event-level cumulative abnormal return (CAR) records (monetary 45, geopolitical 60, energy 47, trade 62, regulatory 50)
- `event_type_statistics.parquet` — five multiplicity-corrected per-event-type significance tests
- `causal_estimates.parquet` — five per-event-type DoWhy causal estimates
- `data/processed/causal_overall_estimate.json` — the pooled/overall DoWhy causal estimate (new artefact, added 2026-07-15; Stage 8's figures now read this file directly rather than a hand-copied number)

## Method (in plain terms)

- **Event study:** for each event, the "normal" expected return is the stock's own average return over the year before the event (specifically, trading days −252 to −21 before it). The "abnormal" return on each day is the actual return minus that expectation. These are summed over a window from 5 trading days before the event to 10 trading days after it, giving one Cumulative Abnormal Return (CAR) per event.
- **Causal analysis:** a separate statistical technique (DoWhy's backdoor adjustment) estimates the relationship between daily sentiment and next-day return, while explicitly controlling for the VIX regime and the prior day's return — variables that could otherwise make sentiment look predictive by coincidence.

## What was found

- **Event study — a null result, honestly reported.** After correcting for testing five event types at once (Benjamini–Hochberg FDR correction), none of the five event-type mean-CAR tests are statistically significant. The strongest raw signal is monetary events (raw p = 0.116, Cohen's d = −0.239, a small effect), but its FDR-adjusted q-value is 0.581 — nowhere near the 0.05 threshold. All five confidence intervals cross zero. **In plain terms: once you correct for testing several event categories, there is no statistically reliable evidence that any single event type produces an abnormal market reaction on average.**
- **Pooled causal estimate — small but statistically distinguishable from zero.** The overall DoWhy backdoor estimate is **+0.005601** (95% CI [+0.002295, +0.008907], p = 0.0009, n = 2,762 observation-days). This confidence interval excludes zero, meaning that — under the model's stated assumptions (its adjustment set and no unmeasured confounding) — combined APP+FOMC sentiment shows a small but genuine independent association with next-day returns.
- **These two results are not a contradiction.** The event study asks "do CARs around specific *events* deviate from zero?" (no, once multiplicity-corrected); the causal estimate asks "does the daily sentiment *signal*, across the whole sample and adjusting for confounders, relate to next-day return?" (yes, weakly). They are different estimands answering different questions, and both are reported as found rather than reconciled into a single, tidier story.
- **Two of the five per-event-type causal estimates are not reliable and are flagged as such:** the geopolitical and energy per-category estimates are each computed from only a single non-neutral sentiment day, because FinBERT sentiment is 94.9% neutral (Stage 3). A confidence interval built from essentially one data point is narrow by mathematical construction, not because the underlying effect is well established — this is disclosed directly in the notebook rather than presented as a solid finding.

## What was not found

No evidence that any individual event type produces a reliable abnormal return once corrected for multiple testing. No claim that the pooled causal estimate implies a usable trading edge — it is a conditional, observational estimate, not a validated predictive signal (that question is addressed separately in Stages 6–7).

## Limitations

- **Observational, not experimental:** the causal estimate depends on the stated DAG (VIX regime and lagged return as confounders) being correctly specified and on no important confounder being left out — an assumption that cannot be fully tested from the data alone.
- **Event clustering:** events are not perfectly independent of each other in time, which can affect how confidently the event-study test statistics should be interpreted.
- **Small, non-degenerate effect size:** even where the causal CI excludes zero, the magnitude (+0.0056 in next-day return units) is small.

## How this connects to the next stage

The CAR values computed here (specifically `mean_car` and related event-derived measures) become the "event" feature category in Stage 5's feature matrix — the bridge between this stage's causal/event-study findings and the predictive modelling stages that follow.

## Where to go for more detail

- The notebook itself: `notebooks/04_causal_analysis.ipynb`
- The full BH-FDR reporting and reasoning: [`09_results_log.md`](../research_bible/09_results_log.md)
- The pooled-estimate persistence decision: [`10_decision_log.md`](../research_bible/10_decision_log.md), 2026-07-15 entries
