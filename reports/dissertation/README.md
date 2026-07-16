# reports/dissertation/

**Purpose:** Current dissertation-facing Word/PDF artefacts and their dated, non-destructive archives.
**Added:** 2026-07-13. **Updated:** 2026-07-16 — dissertation content accepted; repository finalisation pass.

## Accepted, current (2026-07-16)

| File | Notes |
|------|-------|
| `2026-07-16-7030DATSCI.docx` | **Authoritative dissertation source.** Accepted 2026-07-16. Not tracked by Git (`*.docx` is gitignored repository-wide); integrity is verified by the SHA-256 below instead. |
| `2026-07-16-7030DATSCI.pdf` | **Authoritative dissertation PDF.** Accepted 2026-07-16 as the current final research narrative. Re-exported natively from Word after a field refresh (Table of Contents / List of Figures / List of Appendix Figures and Tables / page numbers all current) — no manual field-refresh step remains outstanding. Not tracked by Git; see hash below. |
| `2026-07-16-7030DATSCI_Generative_AI_Statement.docx` | **Current AI-use declaration.** Revised 2026-07-16 to disclose the dissertation finalisation (equations/appendix) and repository cleanup/freeze passes, in addition to the prior work it already disclosed. |

**SHA-256 (recorded 2026-07-16, before this finalisation pass touched anything else):**
```
DOCX               a46c411da588a77a8293e4bacb2d16dc988c6d7ec8882e22eaf35a7e3b630747
PDF                4a8ce3cfc9eb49c400bc2ea8d08bb856d28bd36f33abd2c63214a86d231df1bf
AI Statement (rev) c5ca44f8a2762ef0ce28c955f7e8cf5625589ad7219abcd4b4148d6c4fe7fbdf
```
Full protected-artefact hash set: `reports/finalisation/PROTECTED_FILE_HASHES_2026-07-16.txt`.

**Latest changelogs:** `SUBMISSION_QA_CHANGELOG_2026-07-15.md` (citation/reference/protected-claims QA pass) and `FINAL_DISSERTATION_CHANGELOG_2026-07-15.md` (earlier 2026-07-15 QA pass). Both describe work on the *content* of the dissertation prior to 2026-07-16's appendix/equation finalisation pass; no separate changelog exists yet for the 2026-07-16 edit (event-study equations, duplicate-sentence removal, citation-grammar fix, LASSO-naming consistency, and new Appendix A7–A9/B2–B4 content) — the archived pre-edit backup below is that pass's audit trail.

## Archived

### `archive/superseded_2026-07-16/` (moved 2026-07-16, dissertation-acceptance cleanup)

Earlier 2026-07-15 dissertation versions, superseded by the accepted `2026-07-16-7030DATSCI.docx`: `7030DATSCI-15_07_2026.docx`, `7030DATSCI_FINAL_2026-07-15.docx`, `7030DATSCI_SUBMISSION_FINAL_2026-07-15.docx`, `7030DATSCI_SUBMISSION_FINAL_2026-07-15.pdf`, and `7030DATSCI-15_07_2026_Generative_AI_Statement.docx` (superseded by the revised `2026-07-16-7030DATSCI_Generative_AI_Statement.docx` above). Retained for audit trail only — do not cite or reopen; superseded by the 2026-07-16 accepted files above.

*(A LibreOffice-rendered preview PDF used only for the 2026-07-16 equation-rendering QA check, `2026-07-16-7030DATSCI_PREVIEW_LibreOffice_render.pdf`, was deleted rather than archived — it was explicitly a disposable verification artefact, never a dissertation version, and its content is fully superseded by the accepted native-Word PDF export above.)*

### `archive/2026-07-16-7030DATSCI_PREEDIT_BACKUP_20260716174628.docx`

Byte-identical pre-edit backup of `2026-07-16-7030DATSCI.docx`, taken immediately before the 2026-07-16 appendix/equation edit pass (verified via `cmp` and matching SHA-256 at the time). Retained as that pass's audit trail.

### `archive/pre_2026-07-14_cleanup/` and `archive/pre_fes_v1_1_doc_sync_2026-07-14/`

Earlier historical versions predating the FES v1.1 documentation sync (2026-07-14). See each folder's context in `10_decision_log.md`'s 2026-07-14 entries. Not to be used or cited.

## Dependencies

Sourced from `reports/figures/`, `reports/tables/`, `docs/research_bible/` and the persisted validation JSON/Parquet artefacts throughout. The separate `reports/08_05_2026_DATSCI7030_Data_Collection_Report.docx` remains a labelled legacy report and is intentionally not rewritten by any dissertation sync.

## Repository status

The repository (and this dissertation content) is **frozen pending assessment feedback** as of 2026-07-16. See `docs/research_bible/FINAL_PROJECT_FREEZE_2026-07-16.md` for the full freeze declaration and reopening conditions.
