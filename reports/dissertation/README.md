# reports/dissertation/

**Purpose:** Current dissertation-facing Word artefacts and their dated, non-destructive archives.
**Added:** 2026-07-13. **Updated:** 2026-07-14 after the executed Notebook 01–08 / FES v1.1 consistency pass.

## Contents (current, 2026-07-14)

| File | Notes |
|------|-------|
| `7030DATSCI-14_07_2026.docx` | Canonical dissertation working draft. Synchronized with the current 1,005-event catalogue, 264-row event study, combined APP + FOMC treatment, 92-feature FES v1.1, validated RQ2/RQ3 outputs and current figures. Rendered and visually checked after generation. |
| `7030DATSCI-14_07_2026_Generative_AI_Statement.docx` | Required AI-use declaration. It discloses both earlier Claude assistance and the final OpenAI Codex consistency/formatting pass; authorship and verification responsibility remain with the researcher. Rendered and visually checked. |

The companion `docs/Project_Summary.docx` is also synchronized to version 1.2 and visually checked. `scripts/sync_current_documents.py` makes these three current-document updates reproducible and preserves the first pre-sync copies under `archive/pre_fes_v1_1_doc_sync_2026-07-14/`.

The RQ1 statistical-reporting gate was completed on 2026-07-15: the dissertation now includes five event-type mean-CAR 95% intervals, raw p-values, BH-FDR q-values and Cohen's d. Remaining work is general citation, cross-reference and submission QA rather than an unresolved RQ result.

## Archived 2026-07-14 (`archive/pre_2026-07-14_cleanup/`, not deleted — no git history existed for this folder to fall back on)

Per author instruction: `7030DATSCI-00_07_2026.docx`, `7030DATSCI-11_07_2026.docx` (byte-identical to the kept draft's prior name), `7030DATSCI_Reference_Audit_2026-07-08.docx`, the original (pre-revision) `Generative AI Statement.docx`, and two harmless Word lock files (`~$30DATSCI-04_07_2026.docx`, `~$30DATSCI-09_07_2026.docx`).

## Dependencies

Sourced from `reports/figures/`, `reports/tables/`, `docs/research_bible/` and the persisted validation JSON/Parquet artefacts throughout. The separate `reports/08_05_2026_DATSCI7030_Data_Collection_Report.docx` remains a labelled legacy report and is intentionally not rewritten by the synchronization script.
