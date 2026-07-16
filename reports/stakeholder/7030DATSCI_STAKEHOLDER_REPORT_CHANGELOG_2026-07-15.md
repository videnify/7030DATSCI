# Stakeholder Report Changelog — 2026-07-15

## Source documents used

- **Primary narrative source:** `reports/dissertation/7030DATSCI_SUBMISSION_FINAL_2026-07-15.docx` (the current validated, QA'd dissertation).
- **Stage-by-stage stakeholder pages (read for reference, not overwritten):** `docs/stakeholder_report/{01_data_collection,02_eda,03_event_detection,04_causal_analysis,05_feature_engineering,06_model_training,07_model_evaluation,08_results_visualisation,final_summary}.md` and `docs/stakeholder_report/README.md`.
- **Supporting technical evidence:** `docs/architecture/` (pipeline diagrams), `docs/research_bible/` (methodology, decision log, limitations, validation checklist), root `README.md`, `reports/figures/` (existing validated figures, reviewed but not reused as-is — see below), and current validation/traceability artefacts (`feature_profile.json`, `causal_overall_estimate.json`, `event_type_statistics.parquet`, `statistical_tests.json`, `feature_importance.parquet`, `feature_matrix.parquet`, `events_tagged.parquet`, `high_impact_events.parquet`, `car_results.parquet`).

## Claim verification

A claim sheet was built before drafting (numeric claims, plain-language wording, technical source, dissertation location, permitted rounding, misinterpretation risk) and every number was re-queried directly from the live artefacts listed above — not drafted from memory. All values matched the dissertation's own reported figures exactly, including the Random Forest category-importance percentages (market 71.9% / macro 18.2% / event 3.9%) and the held-out test period (2023-01-03 to 2025-12-29).

## Report structure produced

A 15-page DOCX/PDF following the required structure: cover page; executive summary (kept to one page); the problem and three research questions; data used (one table); how the project works (simplified pipeline + event-study/causal/predictive distinction); RQ1 findings (event study and causal model, two subsections); RQ2 findings; RQ3 findings; what the findings mean; limitations; reproducibility/documentation/GitHub; glossary; final conclusion; and a compact technical evidence map appendix. This is within the requested 12-18 page range.

## Main narrative choices

- The executive summary uses language closely matching the brief's suggested central message, adapted to plain English and kept to one page.
- RQ1 is split into "A. Event study" (null result after BH-FDR correction) and "B. Causal model" (pooled estimate, positive and conditional) exactly as specified, so the two different questions are never merged into one claim.
- Every numeric finding is paired with an explicit callout distinguishing what it does and does not mean (e.g. "not experimental proof", "not about causal importance", "not from any genuine timing skill").
- The baseline's 57.47% directional accuracy is explicitly reframed as a base-rate/constant-prediction artefact wherever it appears, per the brief.
- The report never describes the project as a trading system and never states or implies that FinBERT was fine-tuned.
- The GDELT contextual/excluded framing and the FinBERT pretrained/title-only framing are stated identically to the dissertation and the earlier stakeholder-page audits in this project.

## Specialist terms simplified

Acronyms and technical terms are defined at first use in the body text (e.g. BH-FDR, VIX, RMSE, directional accuracy) and additionally collected in a one-page glossary (11 terms: BH-FDR, DAG, CAR, DoWhy, FinBERT, SHAP, LASSO, RMSE, directional accuracy, information coefficient, Bonferroni correction), matching the terms specified in the brief. No equation is used anywhere in the report; the event-study/CAR formula from the dissertation is described in words only.

## Figures and tables used

**No existing dissertation or `reports/figures/` PNG was reused as-is** — all of them are dense, multi-panel scientific figures built for a technical audience (e.g. `08a_event_landscape.png` has five sub-panels; `07_learning_outcome.png` mixes RMSE, directional accuracy, and a rolling-IC diagnostic). Per the brief's instruction to create simplified visuals where existing ones are too dense, five new, simple figures were generated directly from the same validated numbers (not by editing or cropping any existing figure file):

1. **Figure 1 — Simplified pipeline** (six-box flow diagram), adapted conceptually from `docs/architecture/project_pipeline.svg` for a non-technical reader.
2. **Figure 2 — RQ1 summary** (forest-plot style: five event-type estimates, all crossing zero, versus the pooled causal estimate, which does not), built from `event_type_statistics.parquet` and `causal_overall_estimate.json`.
3. **Figure 3 — RQ2 category importance** (horizontal bar chart), built from `feature_importance.parquet`.
4. **Figure 4 — RQ3 model comparison** (two-panel bar chart: RMSE and directional accuracy across all four models), built from `reports/model_comparison/statistical_tests.json`.
5. **Figure 5 — Evidence summary** (four-box conceptual diagram: association / abnormal return / causal estimate / predictive advantage), synthesised from the RQ1-RQ3 results.

Every figure has a plain-language caption, a source note pointing to the underlying artefact, and a one-sentence interpretation, as required. Three tables were also created (data sources; documentation map; technical evidence map) — all newly authored for this report, none copied from the dissertation's tables.

## GitHub and reproducibility statement

The reproducibility section uses wording closely matching the brief and explicitly states that large local datasets and trained model artefacts may not all be stored directly in GitHub, with their schemas/provenance/hashes documented in the repository instead — this avoids the prohibited claim that all raw data are hosted on GitHub. **The GitHub URL was left as the literal placeholder `[INSERT PUBLIC GITHUB URL]`**, as instructed — a `git remote` (`git@github.com:videnify/7030DATSCI.git`) exists locally, but the brief explicitly says not to invent the URL, and this local remote's existence does not confirm the intended public-facing URL or that the repository is public, so it was not substituted.

## Files created

- `reports/stakeholder/7030DATSCI_STAKEHOLDER_REPORT_2026-07-15.docx`
- `reports/stakeholder/7030DATSCI_STAKEHOLDER_REPORT_2026-07-15.pdf`
- `reports/stakeholder/7030DATSCI_STAKEHOLDER_REPORT_CHANGELOG_2026-07-15.md` (this file)

No file under `docs/stakeholder_report/` was created, edited, or overwritten — confirmed via `git status`, which shows no changes there.

## Validation performed

1. Every numeric claim re-verified against live artefacts (see Claim verification above) — all matched exactly.
2. RQ1-RQ3 conclusions confirmed to match the dissertation's own wording and verdicts exactly (qualified positive for RQ1's pooled estimate / null for RQ1's event-type tests; null for RQ2; null for RQ3).
3. No new scientific claim was introduced anywhere in the report — every sentence traces to an existing dissertation or artefact statement.
4. Every abbreviation used in the body (BH-FDR, DAG, CAR, VIX, RMSE, FOMC, APP, FRED, GDELT, SHAP, LASSO) is either defined at first use or in the glossary.
5. Glossary terms checked against their actual usage in the body text — consistent.
6. GitHub statement checked against the "do not claim all raw data are on GitHub" constraint — the wording explicitly flags that large artefacts may be excluded.
7. All internal folder/file references (docs/research_bible/, docs/architecture/, docs/stakeholder_report/, notebooks/, tests/, and the named technical documents/artefacts in the evidence map) were checked against the actual repository structure and exist.
8. DOCX structure validated with `scripts/office/validate.py` — **all validations passed** (230 paragraphs).
9. Exported to PDF via LibreOffice 26.2.4.2 headless (`soffice --headless --convert-to pdf`) — 15 pages, A4, no conversion errors.
10. All 15 PDF pages visually inspected individually (rendered via `pdftoppm -r 110`): no blank pages, no clipped text, no broken tables, no unreadable figures, no font substitution issues. Every figure and table renders crisply.
11. Confirmed no protected scientific artefact (data/processed/, models/, reports/model_comparison/, numbered dissertation figures) was changed — `git status` shows no modifications to any of these paths.
12. Confirmed the dissertation files (all versions) and every file under `docs/stakeholder_report/` remain untouched.

## Unresolved items (honest list)

1. **The Table of Contents field is a real Word field (`TableOfContents`, with the document's `updateFields` setting enabled) but renders blank in this environment's own PDF export.** LibreOffice's headless `--convert-to pdf` conversion does not compute TOC field content even with `w:updateFields` set (a known limitation of headless/batch conversion, distinct from interactively opening the file). This is the same situation already documented for the dissertation's own TOC in `reports/dissertation/SUBMISSION_QA_CHANGELOG_2026-07-15.md`. **Action required before distribution:** open the DOCX in Microsoft Word and press Ctrl+A then F9 (or right-click the TOC and choose "Update Field") to populate it — this does not affect any of the content already verified in this pass.
2. A separate List of Figures / List of Tables was intentionally **not** created, per the brief's own instruction to omit rather than create a stale or unreliable list — with only 5 figures and 3 tables, and the same field-reliability limitation noted above, a manually maintained list would risk going stale faster than it would help a reader.
3. The GitHub repository URL placeholder (`[INSERT PUBLIC GITHUB URL]`) still needs to be filled in by the author once the public repository location is confirmed.

## RQ1-RQ3 impact

**None.** This report introduces no new analysis, no new number, and no changed conclusion. It is a plain-language synthesis of already-validated dissertation and Research Bible content, produced without touching any notebook, dataset, model artefact, or existing figure.
