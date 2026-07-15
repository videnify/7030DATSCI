# 6. Model Training — Setting an Honest Baseline

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against `model_comparison.parquet` and the model metadata on disk, not copied from an earlier draft.
**Originally verified:** 2026-07-14 (FES v1.1 baseline retrain).
**Last reviewed against current pipeline:** 2026-07-15.
**Technical detail:** `notebooks/06_model_training.ipynb` · [`model_contract.md`](../research_bible/model_contract.md) · [`baseline_model_specification.md`](../research_bible/baseline_model_specification.md) · [`baseline_evaluation.md`](../research_bible/baseline_evaluation.md)

---

## What this stage does

Before asking whether presidential/FOMC events and sentiment add any predictive value, the project first needs a fair comparison point: a model that only sees ordinary market data (price, volume, technical indicators) with none of the event or sentiment information. This stage trains and freezes that baseline, called `Baseline_LASSO`.

## Why it matters

Without a rigorous, honestly-reported baseline, it's easy to overstate what an "event-enhanced" model actually adds — a model that merely matches simple market patterns everyone already knows about isn't a meaningful improvement. This baseline is the yardstick every candidate model in the next stage must clear, on **both** accuracy and directional-accuracy criteria, to be reported as an improvement.

## Inputs

Only the 27 "market" category columns from Stage 5's feature matrix (price/return/technical-indicator features derived purely from SPY's own trading data) — by contract, this model is never shown any sentiment, event, or macro feature.

## Outputs

The trained `Baseline_LASSO` model (v1.1), its predictions on the held-out test period, and its performance metrics, all frozen for the next stage to compare against.

## What was found

**The baseline model shrinks to a constant.** Using cross-validated LASSO regression (with a chronological, not shuffled, validation split — future data is never used to tune a model that will predict the past), every one of the 27 market-only coefficients shrinks to exactly zero. In practice, this means the "model" reduces to predicting the training-period average return every single day, regardless of what the market actually did the day before.

Its test-period performance reflects that:

| Metric | Value | What it means |
|---|---|---|
| RMSE (test) | 0.009631 | Typical size of the prediction error |
| Directional accuracy (test) | 57.47% | How often it guesses the correct up/down direction |
| ROC-AUC | 0.500 | Exactly chance-level — no ranking skill at all |

The 57.47% directional accuracy sounds better than a coin flip, but it isn't — it comes entirely from the market going up more often than down over this period (a "mechanical always-up" result), not from the model detecting any real pattern.

## What was not found

No evidence that ordinary price/technical features alone carry a usable, cross-validated linear signal for next-day SPY returns. This is reported as the genuine result, not adjusted, re-tuned, or hidden to avoid an unflattering finding — the project's standing rule is to report null results exactly as obtained.

## Why this null result matters (rather than being a failure)

A baseline that reduces to "predict the average" is not a broken model — it is the correct, honest answer to "can simple market technicals alone predict next-day direction with a properly validated linear model?" Establishing this clearly and rigorously is what allows the next stage's comparison to mean something: if an event-enhanced model *did* clear this bar, that would be a real finding, not an artefact of a weak or badly-tuned baseline.

## Limitations

This baseline is specifically a linear (LASSO) market-only model — it does not test whether a more complex, non-linear model could find structure in market-only features that a linear model cannot. That question is out of scope for this baseline by design; the project's promotion criteria compare event-enhanced models against *this specific* baseline, not against every possible market-only model.

## How this connects to the next stage

Stage 7 trains three event-enhanced candidates (`Event_LASSO`, `XGBoost`, `LightGBM`) on the full 92-feature matrix and statistically compares each of them against this exact baseline, on both legs of the project's pre-registered promotion rule.

## Where to go for more detail

- The notebook itself: `notebooks/06_model_training.ipynb`
- The formal promotion rule any candidate must clear: [`model_contract.md`](../research_bible/model_contract.md)
- The full discussion of why this baseline design was chosen: [`baseline_evaluation.md`](../research_bible/baseline_evaluation.md)
