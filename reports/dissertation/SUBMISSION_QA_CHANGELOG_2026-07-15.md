# Submission QA Changelog — 2026-07-15

## Source and backup

- **Source DOCX:** `reports/dissertation/7030DATSCI_FINAL_2026-07-15.docx` (the version approved by the prior 2026-07-15 QA pass — see `FINAL_DISSERTATION_CHANGELOG_2026-07-15.md`).
- **Backup:** `reports/dissertation/archive/7030DATSCI_FINAL_2026-07-15_QA_PREEDIT_BACKUP_20260715144318.docx` — byte-identical copy confirmed via `cmp` before any edit in this pass.
- **Baseline stats recorded before editing:** 3,863,032 bytes; SHA-256 `04cea26e47c9946ad7e07a183592e3745b4021c978e829894df2349daf10af95`; 655 paragraphs; 12 tables; 1 section; 15 embedded media files (13 PNG + 2 SVG); cached page-count estimate 30 (Word's last-saved `docProps/app.xml` value, since superseded by the actual 31-page PDF render below).
- **Phase 1 stop condition checked and passed:** both prior corrections — the pooled causal outcome described as a simple percentage return (not log return), and the pooled estimate reporting n = 2,762 — were confirmed present in the source before any further edit began.

## Protected-claims checklist

A full checklist (research questions, dataset/event/FES counts, CAR table, pooled and per-category causal estimates, model metrics, RF importance table and category percentages, RQ1–RQ3 verdicts, held-out period) was built from the source text and cross-verified against live repository artefacts (`event_type_statistics.parquet`, `causal_estimates.parquet`, `causal_overall_estimate.json`, `feature_profile.json`, `statistical_tests.json`, `feature_importance.parquet`, `feature_matrix.parquet`). **Every numeric claim matched its source artefact exactly, including the Random Forest category-importance percentages (market 71.9% / macro 18.2% / event 3.9%, recomputed directly from `feature_importance.parquet`) and the held-out test period (2023-01-03 to 2025-12-29, confirmed against `feature_matrix.parquet`'s `split == 'test'` rows).** No numeric value anywhere in the dissertation was changed in this pass.

## Reference and citation corrections

**A. Malformed "et al." citations (7 instances across 5 references), all fixed to correct author-count convention:**

| Before | After | Reason |
|---|---|---|
| (Cutler, et al., 1989) | (Cutler et al., 1989) | 3-author work; "et al." is correct, but the comma before it was a formatting error |
| (Lucca, et al., 2015) ×2 | (Lucca and Moench, 2015) | 2-author work — "et al." is only correct for 3+ authors |
| (Sharma, et al., 2020) ×2 | (Sharma and Kiciman, 2020) | 2-author work |
| (Goyal, et al., 2008) | (Goyal and Welch, 2008) | 2-author work |
| (McLean, et al., 2016) | (McLean and Pontiff, 2016) | 2-author work |

**B. Six references existed in the reference list but were never cited in-text anywhere in the body — a genuine bidirectional-audit gap.** Each was added as an in-text citation at its natural, already-existing point of use (no new claim was introduced; the underlying sentence already named the method/tool):

- XGBoost → "(Chen and Guestrin, 2016)" added at its first substantive mention (Methods 3.6).
- LightGBM → "(Ke et al., 2017)" added at the same sentence.
- SHAP → "(Lundberg and Lee, 2017)" added where SHAP is first introduced (Methods 3.6).
- LASSO → "(Tibshirani, 1996)" added where the L1-regularised estimator is described (Methods 3.6).
- Market efficiency assumption → "(Fama, 1970)" added in Prior Work and Positioning (1.2), where the assumption is already stated.
- Hand-built sentiment lexicons → "(Loughran and McDonald, 2011)" added where the dissertation already contrasts FinBERT against "a hand-built keyword list" (Methods 3.2).

After these fixes, **all 19 references are cited at least once, and all in-text citations resolve to an existing reference** — confirmed by an exhaustive surname search across the full document text. No reference was deleted; none needed to be, since every one had a legitimate natural citation point already present in the prose.

**C. Not fixed, listed for manual confirmation (per instruction not to invent bibliographic details):** MacKinlay (1997) has no DOI/URL in the reference list. This may be intentional (no persistent DOI exists for this specific older JEL article scan) or may be a genuine gap — left for the author to confirm rather than guessed at.

## Language corrections

- Fixed one grammatical error: "the share of days **were** predicted and realised return shared sign" → "the share of days **where** predicted..." (Methods 3.6 / Results 4.5 metric definition).
- Standardised apostrophe typography: 8 straight apostrophes in "Cohen's d" (×4), "XGBoost's" (×3), and "baseline's" (×1) were converted to curly apostrophes (’) to match the curly apostrophes already used elsewhere in the document ("project's", "FinBERT's", "SPY's", "Welch's").
- No other grammar, spelling, tense, or terminology defects were found in a full paragraph-by-paragraph read of the extracted text. UK English spelling (modelling, behaviour, summarises, etc.) was already fully consistent throughout and required no changes.
- No scientific meaning, hedge, or certainty level was altered anywhere — every edit in this section is either a citation-format correction or a single-word grammar fix.

## Terminology review

Reviewed the full document for the terms listed in the QA brief (S&P 500/SPY, FinBERT, event type, CAR, DoWhy, model names, FES v1.1, train/test/held-out, GDELT, etc.). All were already used consistently throughout; no forced global replacements were made (e.g. "log return" is correctly used in market-return contexts and was left alone — only the two prior-session fixes already applied to the pooled-causal-outcome sentences use "simple return", which is correct and unrelated to the market log-return usage elsewhere).

## Structure and formatting changes

1. **Fixed a genuine heading-hierarchy defect:** Discussion subsections "5.2 Do These Signals Actually Help Predict Returns?", "5.3 Limitations" and "5.4 Where This Could Go Next" were bold Normal-style paragraphs with the section number typed as literal text — not real Word headings. This meant they were invisible to the Table of Contents, the Navigation Pane, and cross-referencing, unlike every other numbered subsection in the document (confirmed by inspecting the underlying XML: real headings use the `Heading2` style with auto-numbering and no literal number in the text run). Fixed by removing the literal "5.2 "/"5.3 "/"5.4 " prefix text and applying the same `Heading2` style used by every sibling subsection (e.g. "5.1 Interpretation of Causal Findings", "4.6 SHAP Explainability"). Verified in the rendered PDF (pages 25–26): both now render with correct, auto-generated sequential numbering ("5.2", "5.3", "5.4"), matching the surrounding headings exactly.
2. **Removed a stray formatting artefact:** the "4.5 Model Performance" heading's paragraph mark, and its cached Table-of-Contents entry, carried a leftover light-grey highlight (`w:highlight="lightGray"`) — a visible editing artefact, confirmed to be the only occurrence of this highlight anywhere in the 655-paragraph document (i.e. genuinely isolated, not a repeated style choice). Removed; verified in the rendered PDF (page 22) that the heading now renders identically to every other Heading2 in the document with no shading.
3. **No other structural defects found.** Heading hierarchy, chapter/subsection numbering (once the above was fixed), table numbering (1–11 + B1), figure numbering (1–6 + A1–A6), caption placement, section breaks, margins, headers/footers, and page numbering were all inspected directly in the rendered PDF and found correct and sequential.

## Figures and tables review

All 12 tables and 12 figures (6 body + 6 appendix) were checked against their captions and surrounding prose, and against the live artefacts they report:

- Every figure/table is referenced in the text; numbering is sequential; no obsolete FES v1.0 count, no "five-day GDELT" wording, and no hardcoded/inconsistent pooled-causal figure appears anywhere.
- Random Forest is consistently and correctly scoped as an RQ2 descriptive-importance tool only, never presented as an RQ3 predictive candidate.
- All 15 embedded images were confirmed **byte-identical** (SHA-256 match) between the pre-edit and post-edit package — no figure was regenerated or touched, since none needed to be.
- **One recurring low-severity issue found and disclosed, not fixed:** in the LibreOffice-rendered PDF, three tables show a narrow column causing an in-word line break — Table 6 ("Coun"/"t" for the "Count" header), Table 10 ("price_vs_ma20"/"0" and "momentum_63"/"d" in the Feature column), and Table 11 ("Baseline_LASS"/"O" in the Model column and "Promotio"/"n" in the header). This may be a LibreOffice-vs-Microsoft-Word column-autofit rendering difference rather than a genuine stored-width defect — Word's font metrics differ from LibreOffice's and may not reproduce this exact break point. **This was not edited blind**, since a table-width change risks a different, unverifiable layout change in the actual submission environment (Word). Recommend the author open the DOCX in Word, check these three tables, and widen the affected column slightly only if the same wrapping reproduces there.

## Abstract/Results/Discussion/Conclusion consistency

Cross-checked all four sections line by line: the same RQ1 (qualified — event-type null, pooled estimate positive), RQ2 (null — no event feature in RF top ten), and RQ3 (null — no candidate beats baseline) findings are stated identically in the Abstract, Results, Discussion, and Conclusions, with matching numbers throughout (RMSE/directional-accuracy/CI/p-values checked against Table 8/9/11 in each location they are restated). No claim appears in the Abstract that is absent from the Results; no major result appears in the Conclusion without supporting analysis earlier in the document.

## Word fields requiring user refresh

The Table of Contents, List of Figures, List of Tables, and List of Appendix Figures/Tables are live Word fields and were **not** regenerated by this pass (neither LibreOffice's conversion nor this QA process updates cached TOC field text). Because subsections 5.2–5.4 were newly promoted to real headings in this pass, **the cached Table of Contents does not yet list them** — this is expected and will resolve automatically once the field is refreshed.

**Action required before submission:** open `7030DATSCI_SUBMISSION_FINAL_2026-07-15.docx` in Microsoft Word, press **Ctrl+A** then **F9** (or right-click each TOC/list and choose "Update Field" → "Update entire table"), and confirm the Table of Contents now shows 5.2/5.3/5.4 under Discussion and that no error is reported. This does not affect any of the underlying content already verified in this pass — it only refreshes cached page numbers and entries.

## PDF export

- **Renderer:** LibreOffice 26.2.4.2 (AARCH64), installed via Homebrew (`brew install --cask libreoffice`) specifically for this task.
- **Command:** `soffice --headless --convert-to pdf --outdir . 7030DATSCI_SUBMISSION_FINAL_2026-07-15.docx`
- **Result:** 31 pages, A4 (595.304 × 841.89 pts), 2,593,398 bytes, SHA-256 `e6629feeff869f9cdd7bfb43aeaddbbf7743d9076c30a2e7e75c7e9a74bfc249`.
- No conversion errors or warnings other than a benign macOS sandbox notice ("Task policy set failed") that did not affect output.

## Page-by-page PDF inspection log

All 31 pages were rendered to JPEG (`pdftoppm -r 110`) and visually inspected individually.

| Page(s) | Section | Issue found | Severity | Action taken | Final status |
|---|---|---|---|---|---|
| 1 | Title page | None | — | — | OK |
| 2–4 | TOC / Lists of Figures & Tables | Cached TOC does not yet include 5.2–5.4 (expected — see Word-field note above) | Low (expected, disclosed) | Noted; requires Word F9 refresh | OK pending refresh |
| 5 | Abstract | None; confirmed "simple-return units" and "n = 2,762" render correctly | — | — | OK |
| 6–9 | Introduction, Data Sources | None; all corrected citations render naturally in context | — | — | OK |
| 10–14 | Methods 3.2–3.6 | None; new citations (Loughran & McDonald, Chen & Guestrin, Ke et al., Tibshirani, Lundberg & Lee) all render correctly in context | — | — | OK |
| 13–14 | Table 6 | "Count" header word-wraps as "Coun"/"t" | Low/cosmetic | Not edited (see Figures/Tables note) | Flagged for Word verification |
| 15–18 | Results 4.1–4.3, Figures 3–4 | None; all figures crisp and legible | — | — | OK |
| 19–20 | Table 9, Table 10 | Table 10: "price_vs_ma200"/"momentum_63d" word-wrap mid-token | Low/cosmetic | Not edited (see Figures/Tables note) | Flagged for Word verification |
| 21 | Figure 5 | None | — | — | OK |
| 22 | Table 11, "4.5 Model Performance" heading | Table 11: "Baseline_LASSO"/"Promotion" word-wrap; heading highlight artefact (fixed pre-render, confirmed absent) | Low/cosmetic (table only) | Highlight already fixed; table wrap flagged only | OK / flagged |
| 23 | Figure 6, SHAP section | None | — | — | OK |
| 24 | Residual Diagnostics | None | — | — | OK |
| 25–26 | Discussion 5.1–5.4 | Confirmed 5.2/5.3/5.4 now render as correctly numbered real headings | — (fix verified) | — | OK |
| 27 | Conclusions, Self-Evaluation | None | — | — | OK |
| 28 | References | None; all 19 references present, alphabetical, consistently formatted | — | — | OK |
| 29–31 | Appendix A & B | None; all 6 appendix figures and Table B1 crisp and correctly captioned | — | — | OK |

No blank pages, no clipped text, no broken characters, no displaced images, no missing captions, no split tables, no footer/header overlap, no incorrect page numbering, and no font substitution were found anywhere in the 31 pages.

## Unresolved items (honest list)

1. Three tables (6, 10, 11) show narrow-column word-wrapping in the LibreOffice-rendered PDF that may or may not reproduce in Microsoft Word — flagged, not edited blind (see Figures/Tables section above).
2. The Table of Contents and List of Figures/Tables/Appendix-Figures/Appendix-Tables fields must be refreshed in Word (Ctrl+A, F9) before submission, since the newly-promoted 5.2–5.4 headings are not yet reflected in the cached field text.
3. MacKinlay (1997) has no DOI/URL in the reference list — flagged for the author's manual confirmation rather than a fabricated DOI.
4. A full reference-list formatting audit beyond the specific authors named in the QA brief (e.g. re-verifying every DOI actually resolves to the correct paper) was not performed — this pass verified internal consistency (author/year/matching citation) but did not re-fetch every DOI externally.

## RQ1–RQ3 impact

**None.** No numeric result, effect size, confidence interval, p-value, model metric, or verdict was changed anywhere in this pass. Every edit was one of: a citation-formatting correction, a missing in-text citation addition, one grammar fix, an apostrophe-typography standardisation, or a heading-style/highlight structural fix. All protected claims in the pre-edit checklist were re-verified identical after editing.

## Final validation summary

1. DOCX package validated with `scripts/office/validate.py` against the pre-edit version — **all validations PASSED**, paragraph count unchanged (655 → 655).
2. DOCX confirmed to open and convert cleanly via LibreOffice with no errors.
3. All protected scientific claims re-verified unchanged against live artefacts after editing.
4. References and citations confirmed bidirectionally matched (19/19 references cited; every citation resolves).
5. Heading and numbering consistency confirmed via rendered PDF (5.2–5.4 fix verified correct).
6. All tables and figures confirmed referenced in text.
7. All 15 embedded images confirmed byte-identical (SHA-256) before/after.
8. Word fields (TOC/lists) confirmed structurally intact and refreshable; refresh required before submission (documented above).
9. PDF exported successfully (LibreOffice 26.2.4.2, 31 pages).
10. Every PDF page (31/31) visually inspected; log above.
11. No protected artefact (`data/processed/`, `models/`, `reports/model_comparison/`, numbered figures) changed — confirmed via `git status`.
12. No RQ1–RQ3 result changed anywhere.
13. Unresolved items listed honestly above (4 items, none blocking, all either cosmetic/rendering-engine-dependent or requiring a routine Word-side field refresh).
