# 7. Model Evaluation — Do Events and Sentiment Actually Improve Prediction?

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against `statistical_tests.json` and `model_comparison.parquet` on disk, not copied from an earlier draft.
**Originally verified:** 2026-07-14 (FES v1.1 event-model retrain and comparison).
**Last reviewed against current pipeline:** 2026-07-15.
**Technical detail:** `notebooks/07_model_evaluation.ipynb` · [`model_contract.md`](../research_bible/model_contract.md) · [`statistical_decision_matrix.md`](../research_bible/statistical_decision_matrix.md)

---

## What this stage does

This is the central predictive test of the whole project: does giving a model access to event and sentiment features (on top of ordinary market data) actually improve next-day return prediction, in a way that's statistically distinguishable from chance? It trains three "event-enhanced" candidate models on the full 92-feature matrix, statistically compares each against Stage 6's market-only baseline, and separately produces feature-importance evidence for a related but distinct question (RQ2: which features matter most, regardless of prediction accuracy).

## Why it matters

This is where RQ3 — the project's core predictive research question — gets its answer. It is also where it would be easiest to overstate a marginal or coincidental result as a genuine improvement; the project instead pre-registered a strict two-legged statistical promotion rule specifically to prevent that.

## Inputs

The full 92-feature FES v1.1 matrix (Stage 5) and the frozen `Baseline_LASSO` model (Stage 6).

## Outputs

Three trained candidate models (`Event_LASSO`, `XGBoost`, `LightGBM`), their test-set predictions and SHAP explanation values, a Random Forest feature-importance ranking (for RQ2 only), and the statistical comparison results.

## What was found

**Test-set performance, side by side with the baseline:**

| Model | Test RMSE | Test directional accuracy |
|---|---|---|
| Baseline_LASSO (market-only) | 0.009631 | 57.47% |
| Event_LASSO (92 features) | 0.009631 | 57.47% |
| XGBoost (92 features) | 0.009656 | 48.93% |
| LightGBM (92 features) | 0.009700 | 44.27% |

- **`Event_LASSO` collapses to the exact same constant prediction as the baseline** — with 92 features available, LASSO's own regularisation still shrinks every coefficient to zero. Giving a linear model more features to choose from did not help it find a real linear signal.
- **XGBoost and LightGBM are both worse than the baseline**, not better, on both metrics. XGBoost shows a large train/test gap (train R² 0.222 vs. test R² −0.007) — a classic overfitting signature — and its directional accuracy (48.9%) is below both the baseline and a coin flip.
- **Formal statistical test result: no candidate clears the promotion bar.** Using the pre-registered two-legged rule (a Diebold-Mariano test for RMSE, a two-proportion z-test for directional accuracy, both Bonferroni-corrected for testing three candidates at once, α = 0.0167), **none of the three event-enhanced models significantly beats the baseline on either leg.** The formal verdict is: **H0(3) NOT REJECTED** — the null hypothesis that event-enhanced models do not improve on the market-only baseline is not rejected.
- **RQ2 (feature importance) is a separate question, and its answer complicates a simple "events don't matter" reading.** A Random Forest fit on the full 92-feature matrix ranks features by importance for RQ2 purposes — but the top-ranked features are dominated by ordinary market/technical features (e.g. `log_return_hi`, `return_lag1d`, `vix`, `cum_return_5d`), not event or sentiment features. This does not mean events are causally irrelevant (Stage 4 found a small but genuine causal association) — it means that, for the specific task of *out-of-sample next-day prediction*, feature importance and causal relevance are not the same thing, and neither guarantees the other.

## What was not found

No event-enhanced model beat the market-only baseline under the project's own pre-registered promotion criteria. No evidence that adding more features (92 vs. 27) by itself improves prediction — if anything, the two tree-based models did worse than the simpler baseline.

## Limitations

- **Non-constant model diagnostics only:** XGBoost's overfitting pattern (large train/test gap) is a known limitation of tree-based models on this modest dataset size (1,727 training rows) and this task's low signal-to-noise ratio; it is disclosed rather than tuned away.
- **A single Random Forest importance ranking is descriptive, not a p-value** — it tells you what the model leaned on, not whether that reliance is statistically or causally justified.
- **Feature importance ≠ causal importance:** this stage's RQ2 evidence and Stage 4's causal evidence answer genuinely different questions and should not be merged into one narrative.

## Do not overstate this result

No model here demonstrates a validated predictive edge, and this project does not claim, and should not be read as claiming, a profitable trading strategy. The honest, reported finding is a null result on the specific, pre-registered predictive comparison — which is itself a meaningful and reportable scientific outcome, not a failure of the project.

## How this connects to the next stage

Stage 8 visualises exactly these results — honestly, including the null RQ3 verdict and the RQ2 feature-importance caveats — rather than reframing them as a success.

## Where to go for more detail

- The notebook itself: `notebooks/07_model_evaluation.ipynb`
- The formal two-legged promotion rule: [`model_contract.md`](../research_bible/model_contract.md)
- The statistical decision framework behind the Bonferroni correction: [`statistical_decision_matrix.md`](../research_bible/statistical_decision_matrix.md)
