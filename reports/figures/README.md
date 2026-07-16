# reports/figures/

**Purpose:** All charts and plots (300 dpi PNGs), one set per notebook, plus a small set of dissertation-appendix-only figures. Gitignored — regenerate by re-running the corresponding numbered notebook (or the corresponding `scripts/generate_appendix_*.py` script for the appendix set), never hand-edited.
**Added:** 2026-07-13 (this folder previously had no README). **Updated 2026-07-16** to add the three new Appendix A7–A9 figures.

## Contents

Figures are prefixed `01`–`08` to match the notebook that produces them (for example, `02b_return_distribution.png` from `02_eda.ipynb`). The dissertation synthesis figures `08a`–`08d` are current visualisation v1.2 outputs. Their dimensions, SHA-256 hashes and upstream bindings are recorded in `results_visualisation_validation.json`, which reports `PASS`. Figure 08b now reports the completed RQ1 family result (0/5 BH-FDR rejections, minimum q=0.581, maximum |d|=0.239) and describes the separate DoWhy treatment as the combined APP + FOMC signal; the old “lexicon treatment” wording is historical. `docs/research_bible/08_figures_plan.md` remains the authoritative RQ mapping and caveat register.

### Dissertation Appendix figures (added 2026-07-16)

Not produced by a numbered notebook — each has its own standalone generation script in `scripts/`, since they support the dissertation appendix rather than an RQ analysis stage:

| Figure | File | Source |
|---|---|---|
| A7 — Causal DAG | `A7_causal_dag.png` (+ `.svg`) | `scripts/generate_appendix_a7_causal_dag.py`, built from Table 4's exact node/edge list |
| A8 — Residual diagnostics | `A8_residual_diagnostics.png` | `scripts/generate_appendix_a8_residual_diagnostics.py`, from `reports/model_comparison/event_model_predictions.parquet`'s 750-row test split |
| A9 — Research governance architecture | `A9_research_governance.png` | Rasterised via `rsvg-convert` from the existing canonical `docs/architecture/research_governance.svg` — no new source, reused as-is |

## Dependencies

The notebook (or `scripts/generate_appendix_*.py` script) that produces each figure; `docs/research_bible/08_figures_plan.md`.
