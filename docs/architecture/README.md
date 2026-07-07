# Architecture Diagrams

**DATSCI7030 — Causal Event-Driven Market Impact Modelling** · Version 2.0 (2026-07-06)

**Purpose:** Minimal, accurate SVG diagrams of the current, frozen project architecture — pipeline order, data lineage, governance structure, RQ traceability, and the RQ3 modelling flow. These diagrams support the dissertation's Methodology chapter; they are reference material, not RQ1–RQ3 evidence figures (which live in `reports/figures/`, tracked in `docs/research_bible/08_figures_plan.md`).
**Last updated:** 2026-07-06 (Architecture SVG Cleanup & Rebuild mission) — the full diagram set was audited; 11 diagrams describing an earlier, superseded ARIMA/intervention-analysis methodology were archived, 2 broken/misattributed files were deleted, and the 5 canonical diagrams below were rebuilt from scratch against the current frozen pipeline.

---

## Canonical diagrams (current)

| File | What it shows | Use in dissertation |
|------|----------------|----------------------|
| `project_pipeline.svg` | Notebook execution order, 01 Data Collection → 08 Results Visualisation → Dissertation | Chapter 3 (Methodology) — pipeline overview figure |
| `data_lineage.svg` | Raw files → `events_tagged.parquet`/`daily_sentiment.parquet` → `master_dataset.parquet` → `car_results.parquet` → `feature_matrix.parquet` → models/reports | Chapter 3 §3.1 (Data Sources) / reproducibility appendix |
| `research_governance.svg` | Research Questions → Hypotheses → SAP v1.0 → Dataset Contract → FES v1.0 → MCP v1.0 → Results | Chapter 3 (Methodology) — governance/versioning figure |
| `rq_traceability.svg` | RQ1/RQ2/RQ3 → method chain → Results, for each research question | Chapter 1 (Introduction) or Chapter 4 (Results) opening figure |
| `modelling_flow.svg` | `feature_matrix.parquet` → Baseline → Event-enhanced models → Metrics → Statistical comparison → Explainability → RQ3 conclusion | Chapter 3 §3.5 (Model Specification) / Chapter 4 §4.4 (Model Comparison) |
| `car_formula.svg` | Annotated CAR formula reference (updated 2026-07-06 — ARIMA reference removed, event window corrected to config.yaml's −5/+10 days) | Chapter 3 (Methodology) — event study equation reference |

All six are plain SVG (no raster embeds), white background, dark grey/black text, a single muted steel-blue accent colour, Arial/Helvetica, and no local file paths — safe to open directly in a browser or embed in Word/LaTeX.

## A note on `rq_traceability.svg`

The mission brief that requested this diagram specified three separate lanes: RQ1→Event Study, RQ2→Causal Analysis, RQ3→Feature Matrix/Baseline. That does not match this project's frozen research questions (`docs/research_bible/01_research_questions.md`): **both** the Event Study and the DoWhy Causal Analysis answer **RQ1** (abnormal returns), while RQ2 is answered by feature importance/SHAP, not causal analysis. The diagram was built to match the frozen RQ definitions rather than the mission brief's lane assignment, with a caption on the figure itself noting the correction — see `docs/research_bible/10_decision_log.md` (2026-07-06) for the full reasoning.

---

## Archived diagrams (`archive/`)

11 diagrams from an earlier project iteration that used ARIMA/SARIMAX intervention analysis (since replaced by the market-model event study + DoWhy backdoor estimation actually implemented) or NewsAPI/ECB as a core data source (superseded by the American Presidency Project for 2015-2025). Kept for historical reference — none are accurate to the current frozen pipeline and none should be cited in the dissertation.

| File | Why archived |
|------|---------------|
| `arima_pipeline.svg` | ARIMA intervention methodology — not implemented |
| `causal_dag_dowhy.svg` | Superseded by the `_professional_clean` version; both depict GDELT as a core causal-model input, which it isn't |
| `causal_dag_dowhy_professional_clean.svg` / `.png` | Same GDELT-as-core-input issue; not part of the canonical 5 |
| `data_pipeline_architecture.svg` | References ARIMA and NewsAPI as core; superseded by `data_lineage.svg` |
| `datsci7030_project_structure.svg` | Directory tree predates `docs/research_bible/`, `master_dataset.parquet`, `feature_matrix.parquet`, `models/baseline`, `models/event` |
| `full_system_architecture.svg` | Old 13-phase broad-scope design (references NewsAPI/ECB); superseded by `project_pipeline.svg` |
| `hybrid_model.svg` | ARIMA + SARIMAX dual-layer model — never implemented |
| `intervention_equation.svg` | Intervention/transfer-function ARIMA equation — not the model actually used |
| `ml_project_map.svg` | Old 5-phase map, NewsAPI-centric; superseded by `project_pipeline.svg` |
| `phase5_validation_pipeline.svg` | Wrong train/test dates (2018-2022/2023-2024 vs. the actual frozen 2015-2022/2023-2025 split) and lists ARIMA as an applied model |

## Deleted (not archived)

Two files were deleted outright rather than archived, per the mission's DELETE criterion ("misleading, broken, or not useful"):

- `data_pipeline_architecture_rebuilt.svg` / `.png` — titled "GOVFIN Analytical Pipeline," referencing a different project entirely.
- `project_structure.svg` — already marked "Deprecated" in the prior version of this README and references a `govfin/` directory structure.

---

## Notes

- `.ipynb_checkpoints/` and `.DS_Store` in this folder are editor/OS artefacts, already gitignored — safe to ignore.
- All diagrams are SVG (scalable, no resolution loss in dissertation PDF export). To embed: `<img>` tag, or Word's Insert → Pictures.
- If a future diagram needs updating, edit the SVG directly (plain text/XML) — there is no separate source file or design tool dependency.
