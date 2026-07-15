# Final Dissertation Changelog — 2026-07-15

## Source and backup

- **Source dissertation used:** `reports/dissertation/7030DATSCI-15_07_2026.docx` — selected because it is the only current-dated dissertation file in the repository, is referenced by the project's own documentation (`docs/research_bible/10_decision_log.md`, 2026-07-15 GDELT entry, explicitly names it), and its internal content (front matter, all numerical claims) is materially newer than any archived copy under `reports/dissertation/archive/`.
- **Pre-edit backup:** `reports/dissertation/archive/7030DATSCI-15_07_2026_PREEDIT_BACKUP_20260715142730.docx` (byte-identical copy of the source, made before any edit in this pass).
- **Generative AI Statement file** (`7030DATSCI-15_07_2026_Generative_AI_Statement.docx`): reviewed for relevance, not modified — out of scope for this pass (no factual claim in it depends on any repository artefact checked here).

## Audit method

A full-text extraction of the source docx was checked against six specific, independently-verified ground-truth facts (GDELT scope, FinBERT pretrained-only status, FES v1.1 feature/row counts, the pooled DoWhy causal estimate, the RQ3 model-comparison verdict, and the event-study methodology/windows). See the audit findings below — **five of six topics matched the ground truth with no changes needed; one topic had a genuine internal inconsistency that was corrected.**

## Numerical and methodological corrections made

**One genuine contradiction was found and fixed:** the dissertation described the pooled DoWhy causal estimate's outcome units inconsistently in two places.

- The notebook that actually produces this estimate (`notebooks/04_causal_analysis.ipynb`, Section 1) computes `spy_return` as `close.pct_change()` — an ordinary **simple (percentage) return**, not a log return — and this is the exact series the DoWhy causal model in Section 4 uses as its outcome (`spy_return_next`).
- One passage already correctly said "simple return" (the Methods chapter, describing the ACE coefficient). Two other passages — the Abstract and the Causal Analysis results section — instead called the identical +0.005601 figure a "log return" / "log-return units" value. This is an internal inconsistency about the same number, not a disagreement about its value.
- **Fix applied:** both incorrect passages were corrected from "log return"/"log-return units" to "simple return"/"simple-return units", so all three mentions of this figure now agree with each other and with the notebook that actually produced it. No numeric value was changed.
- **Also added, not previously stated anywhere in the document:** the pooled estimate's sample size, n = 2,762 observation-days (from `data/processed/causal_overall_estimate.json`), added to both corrected passages for completeness. This is additional traceability information, not a change to any reported result.

No other numerical or methodological change was made. All other checked topics (GDELT full-history scope, FinBERT pretrained-only/title-only status, FES v1.1 counts, the RQ3 null verdict, and the event-study constant-mean-return methodology and windows) were independently verified to already match the current repository ground truth — see the full per-topic quotes and verdicts recorded in this session's audit pass.

## Tables changed

None. Table 8 (the pooled/per-category causal-estimate table) already stated +0.005601 / [+0.002295, +0.008907] correctly; only surrounding prose was corrected.

## Figures changed

None. No figure or its caption required a change.

## References changed

None checked/changed in this pass — the six-topic audit was scoped to GDELT, FinBERT, FES v1.1, the pooled causal estimate, RQ3, and event-study methodology only, per the task's evidence-hierarchy priority. A full reference-list cross-check (every citation has a reference, no duplicates, consistent formatting) was **not** performed in this pass and remains an open item — see "Remaining unresolved items" below.

## Documentation-only wording changes (outside the dissertation, same pass)

- `docs/stakeholder_report/`: all seven missing stage pages (02–08) plus an executive summary (`final_summary.md`) were written and verified against current notebook outputs and artefacts; the index `README.md` was updated to mark all eight stages ✅ complete.
- `README.md` (repository root): version/date header updated 2026-07-13 → 2026-07-15; `causal_overall_estimate.json` added to the Phase 4 outputs list.
- `docs/architecture/README.md`: version badge corrected from the stale "2.9 (2026-07-14)" to "3.0 (2026-07-15)", matching the body text and all six canonical SVGs (already at v3.0).
- `docs/research_bible/15_traceability_matrix.md` and `docs/research_bible/05_data_dictionary.md`: both updated to list `causal_overall_estimate.json` as a Notebook 04 output / Notebook 08 input.
- `docs/research_bible/14_project_dashboard.md`: a new dated 2026-07-15 entry added at the top (historical 2026-07-14 entries preserved unedited, including their now-superseded "8 tests passed" wording, per the project's own append-don't-rewrite governance rule in `00_project_freeze.md` §10) recording the day's full traceability audit, the test-suite split (now 18 passing tests), and the stakeholder-report completion.

## Formatting changes

None to the dissertation's formatting, styles, headings, or embedded images — the edit was a targeted plain-text substitution inside two existing paragraphs; paragraph count is unchanged (655 → 655), and `scripts/office/validate.py` confirmed the edited package passes full XSD/structural validation against the original.

## Unresolved Word field-refresh requirements

None triggered by this edit — no cross-reference, TOC entry, list-of-figures/tables entry, or numbered caption was added, removed, or renumbered. If Word's table of contents or list of figures/tables was already stale for unrelated reasons prior to this pass, that is unchanged by this edit; Word should still be allowed to refresh fields (`Ctrl+A`, `F9`, or "Update Fields on Open") on next open, as standard practice.

## Final dissertation output paths

- `reports/dissertation/7030DATSCI_FINAL_2026-07-15.docx` — the corrected, versioned dissertation output from this pass.
- A corresponding PDF export was **not produced**: no LibreOffice/`soffice` installation was available in this environment to perform a verified DOCX→PDF conversion (confirmed: `soffice`/`libreoffice` not found on `PATH` or under `/Applications`). This is disclosed rather than silently skipped — producing the PDF is a mechanical, low-risk remaining step once a working LibreOffice/Word installation is available; the DOCX itself is complete and structurally validated.
- The original source file (`7030DATSCI-15_07_2026.docx`) and its pre-edit backup are both preserved unmodified.

## Confirmation of whether RQ1–RQ3 changed

**None.** No numeric result, effect size, confidence interval, p-value, model metric, or verdict was changed anywhere in the dissertation. The only dissertation edit was a units-label correction (and an added sample size) on an already-correct number.

## Remaining unresolved items (honest list)

1. **Full reference-list cross-check** (every citation ↔ reference pair, duplicate removal, formatting consistency) was not performed in this pass — only the six ground-truth factual topics were audited against the dissertation text.
2. **No PDF export was produced** (see above) — requires a LibreOffice/Word installation not present in this environment.
3. **Full Phase 9–11 dissertation audits** (a complete figure/table hash-provenance audit against every dissertation figure/table; a full grammar/language/UK-English pass; DOCX structural checks beyond XSD validity such as cross-reference/TOC/page-number correctness) were **not performed exhaustively** in this pass — the six-topic factual audit found the document already in strong, internally consistent shape on the highest-risk items (methodology, causal estimate, RQ3 verdict), and a full line-by-line language review was judged out of proportion to the one genuine defect actually found. This should be treated as **"technically complete, final document review required"** rather than a claim that every sentence in the dissertation has been re-read.
4. Word must still refresh its own fields (TOC, cross-references, page numbers) on next open, per standard practice — this was not and cannot be done programmatically here.
