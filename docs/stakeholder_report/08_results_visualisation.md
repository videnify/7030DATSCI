# 8. Results Visualisation — Putting the Whole Story in One Place

**Status:** ✅ Written 2026-07-15 — verified via a live, clean-kernel execution the same day, not from a prior draft.
**Originally verified:** 2026-07-13 (initial figure generation).
**Last reviewed against current pipeline:** 2026-07-15 — the notebook was re-executed end-to-end from a clean kernel as part of the full traceability audit; all four figures were confirmed byte-for-byte identical to the pre-audit versions (zero drift).
**Technical detail:** `notebooks/08_results_visualisation.ipynb` · `reports/figures/results_visualisation_validation.json` · [`10_decision_log.md`](../research_bible/10_decision_log.md) (2026-07-15 entries)

---

## What this stage does

This is the final technical notebook in the pipeline. It doesn't compute anything new — it exclusively reads already-frozen, already-validated outputs from every earlier stage and turns them into four publication-style figures that tell the project's full story end to end: what events happened, what the causal evidence shows, how the predictive models performed, and how it all fits together.

## Why it matters

Because this stage only reads existing frozen artefacts, it acts as a final integrity check as much as a communication tool — if anything upstream had silently changed, these figures (and the validation file they produce) would be the place a discrepancy would most likely surface.

## Inputs

Every major artefact produced by Stages 1–7: the event catalogue, CAR results, per-event-type and pooled causal estimates (including the newly-added `causal_overall_estimate.json`), the feature matrix, and the full model comparison/SHAP results.

## Outputs

Four figures:

| Figure | What it shows |
|---|---|
| `08a_event_landscape.png` | The full 2015–2025 event timeline — types, sentiment, and high-impact flags |
| `08b_causal_evidence.png` | The event-study and causal-estimate results together (the null CAR result and the significant pooled causal estimate, shown side by side rather than merged into one number) |
| `08c_predictive_pipeline.png` | The RQ2 and RQ3 results — feature importance and the model comparison, including the null RQ3 verdict, stated directly |
| `08d_full_dashboard.png` | An integrated, full-period dashboard combining all of the above |

Plus `reports/figures/results_visualisation_validation.json`, a machine-readable record binding every figure's inputs (by SHA-256 hash) and confirming the reported statistics match what's in the frozen files.

## What was found

- **The pooled causal estimate is no longer a hardcoded number.** Earlier in the project, this notebook's causal-evidence figure contained a manually copied-in value for the pooled DoWhy estimate. As of 2026-07-15, this notebook reads the value directly from `data/processed/causal_overall_estimate.json` (a dedicated artefact Notebook 4 now produces), with built-in checks confirming the file's structure, that its confidence interval is correctly ordered, and that its values are finite before using them. The value itself is unchanged (+0.005601, 95% CI [+0.002295, +0.008907], p = 0.0009) — this was a traceability fix, not a result change.
- **Figures 08c/08d state the null findings directly**, rather than only implying them: the RQ2 top-decile check is shown as descriptive Random Forest/SHAP evidence, not a claim of statistical significance; XGBoost is presented as a diagnostic view (it has the highest defined "information coefficient" among the candidates) rather than as a winning model or a usable trading signal.
- **A live re-execution on 2026-07-15 confirmed zero drift.** The notebook was run end-to-end from a fresh kernel; all four figures came out byte-for-byte identical to the pre-existing versions, and every protected upstream artefact's hash (datasets, models, SHAP values, statistical test results) matched exactly before and after. This means the traceability fix above genuinely changed nothing about the reported results — it only changed *how* the pooled estimate gets into the figure.

## What was not found

No discrepancy between what these figures show and what the underlying frozen artefacts actually contain — the validation file's checks all passed.

## Limitations

This stage is a reporting layer only; any limitation in an upstream stage (title-only FinBERT sentiment, the observational nature of the causal estimate, the RQ3 null result) carries through unchanged into these figures. This notebook does not, and is not intended to, resolve any of those limitations — it visualises them honestly.

## How this connects to the next stage

These four figures, and the validated numbers behind them, are the direct source for the stakeholder report's headline claims and for the dissertation's Results and Discussion chapters — nothing in either of those documents should report a number that isn't traceable back to this notebook's validated output.

## Where to go for more detail

- The notebook itself: `notebooks/08_results_visualisation.ipynb`
- The machine-readable validation record: `reports/figures/results_visualisation_validation.json`
- The pooled-estimate traceability fix and live re-execution record: [`10_decision_log.md`](../research_bible/10_decision_log.md), 2026-07-15 entries
