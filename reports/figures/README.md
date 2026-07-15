# reports/figures/

**Purpose:** All charts and plots (300 dpi PNGs), one set per notebook. Gitignored — regenerate by re-running the corresponding numbered notebook, never hand-edited.
**Added:** 2026-07-13 (this folder previously had no README). **Updated 2026-07-14** after the validated FES v1.1 Notebook 08 rerun.

## Contents

Figures are prefixed `01`–`08` to match the notebook that produces them (for example, `02b_return_distribution.png` from `02_eda.ipynb`). The dissertation synthesis figures `08a`–`08d` are current visualisation v1.2 outputs. Their dimensions, SHA-256 hashes and upstream bindings are recorded in `results_visualisation_validation.json`, which reports `PASS`. Figure 08b now reports the completed RQ1 family result (0/5 BH-FDR rejections, minimum q=0.581, maximum |d|=0.239) and describes the separate DoWhy treatment as the combined APP + FOMC signal; the old “lexicon treatment” wording is historical. `docs/research_bible/08_figures_plan.md` remains the authoritative RQ mapping and caveat register.

## Dependencies

The notebook that produces each figure; `docs/research_bible/08_figures_plan.md`.
