# 11 — Limitations

**Purpose:** A complete, honest inventory of the project's known weaknesses, scoped-out work, and methodological compromises — written so the dissertation's Limitations chapter is prepared in advance rather than assembled defensively after an examiner asks. Every entry states how it should be handled in the write-up.
**Owner:** Ibrahim Haroun.
**Dependencies:** All other Research Bible documents feed this one; cross-referenced throughout.
**Update Frequency:** Add an entry the moment a limitation is discovered — do not wait until the dissertation-writing phase to compile this list from memory.
**Relation to Dissertation:** Direct source for dissertation Chapter 5 (Discussion) §5.x (Limitations) and for pre-empting viva questions.

---

## Research-validity limitations (affect what can be claimed)

### L1 — No market-only baseline yet exists (blocks RQ3)
RQ3 cannot currently be answered because no model has been trained on price/technical features alone under the same protocol as the event-informed models. **This is the most consequential open limitation in the project.** See `07_model_plan.md` for the remediation plan and `01_research_questions.md` for why RQ3 must remain marked "not yet answered" until this closes.
**Handling in write-up:** If the dissertation is written before this closes, RQ3 must be explicitly framed as "approached but not concluded," with the baseline gap stated as future work — never implied as answered.

### L2 — Directional accuracy is close to chance
Best model (LASSO) test directional accuracy is 56.4% — a real but modest edge over a coin flip (50%). Even if RQ3's baseline comparison shows statistical significance, the *economic* significance of a ~6 percentage-point edge, before transaction costs, is small.
**Handling in write-up:** State both statistical and economic significance separately (per `04_statistics_plan.md`); do not conflate "statistically significant improvement" with "a viable trading edge."

### L3 — Event-type CAAR significance not yet multiple-comparison corrected
The per-event-type significance flags in `data/processed/car_results.parquet` are pre-correction. See `04_statistics_plan.md` and `09_results_log.md` — the "Geopolitical events are significant" finding should be re-verified after Benjamini-Hochberg correction before being stated unconditionally.
**Handling in write-up:** Report post-correction results; if correction changes the conclusion, report that transition explicitly rather than only the corrected number.

### L4 — Event clustering violates independence assumption
Presidential communications cluster in time (e.g. multiple statements during a single crisis week), violating the event-study t-test's independence assumption. Mitigated by testing on CAAR (event-type averages) rather than pooled raw CAR, but not eliminated.
**Handling in write-up:** State this as a standard, literature-acknowledged limitation of event-study methodology applied to unstructured/high-frequency communication events (as opposed to the sparser, naturally-independent FOMC calendar).

### L5 — Sentiment scored on titles only, not full text
Both FinBERT and the lexicon scorer operate on document *titles* (`app_presidential_documents.parquet: title`), not full transcripts (`text_snippet` is a snippet, not the full document). A title-level signal is a coarser proxy for the communication's actual content and tone.
**Handling in write-up:** State explicitly as a scope limitation; note that full-text scoring is a natural extension (see also L6, FinBERT domain mismatch, which full-text scoring might also partially address).

### L6 — FinBERT domain mismatch
FinBERT — the project's official primary sentiment engine (Sentiment Engine Freeze v1.0, 2026-07-06 — see `10_decision_log.md`) — is trained on financial-news headlines, not political/policy language, producing 95.3% neutral labels when applied to presidential communications. The lexicon scorer, retained only as a fallback/historical prototype, is itself a hand-curated (not independently validated) keyword list, and shows a more discriminative but unvalidated distribution (73.1% neutral).
**Handling in write-up:** Report both methods' distributions (already done in `09_results_log.md`), justify FinBERT as the adopted primary engine despite its neutral-heavy output (SEF v1.0 rationale: it matches what the pipeline actually runs and produces), and note that neither method has been validated against human-labelled ground truth for this domain — a genuine open validity question.

### L7 — GDELT limited to a 5-day sample against a 2015–2025 study period
`data/raw/gdelt_sample.parquet` and the derived `gdelt_daily_risk.parquet` cover only 5 days. Any geopolitical-risk feature derived from GDELT is not representative of the full study period.
**Handling in write-up:** Either exclude GDELT-derived features from any "final" reported model (recommended, and the current interim status per `10_decision_log.md`), or explicitly caveat any result touching them as based on a proof-of-concept sample only.

### L8 — QQQ/GLD/TLT collected but unused
Collected per `config.yaml` but not used in any downstream RQ1–RQ3 result as of 2026-07-04. Currently dead weight in the data dictionary with no defined analytical purpose.
**Handling in write-up:** Either scope and run the cross-asset generalisation check before submission (promotes this from limitation to a genuine RQ1 robustness section), or drop from the pipeline and note as "considered but out of scope" — see `10_decision_log.md`, decision must close before submission.

### L9 — XGBoost overfitting not yet root-caused
XGBoost's train R² (0.554) collapses to test R² (0.030). The comparison table currently reports this without deeper diagnosis (regularisation sensitivity, learning curve analysis).
**Handling in write-up:** Either investigate and report the cause (feature-count-to-sample-size ratio, insufficient regularisation, etc.) or explicitly flag XGBoost's result as unreliable/overfit in the RQ3 narrative rather than letting the test-set row stand unqualified.

### L10 — No claim of tradeable strategy performance
Figures such as `07d_strategy_performance.png` and the strategy panel in `08d_full_dashboard.png` show illustrative cumulative-return signal, not a backtested strategy net of transaction costs, slippage, or realistic position sizing.
**Handling in write-up:** Caption these figures explicitly as directional-signal illustrations; the dissertation must not claim or imply a profitable trading strategy has been demonstrated.

### L11 — Single-asset focus (SPY only for causal/predictive claims)
Despite collecting four tickers, all RQ1–RQ3 evidence is SPY-specific. Findings should not be generalised to other asset classes without the (currently unscoped) cross-asset analysis in L8.
**Handling in write-up:** State the single-asset scope explicitly in the Introduction/Methodology, not just implicitly through the figures used.

---

## Repository/engineering limitations (do not affect research validity, but affect professionalism and reproducibility)

### L12 — No version control history yet
Zero git commits exist as of 2026-07-04 despite a `.gitignore` and staged files being ready. See `DATSCI7030_Repository_Audit_Report.ipynb` §3 for the remediation steps (including removing a newly discovered nested git repository before the first commit).
**Handling in write-up:** Not a dissertation-content issue, but an examiner may ask for repository history as process evidence — resolve before submission, tracked in `13_validation_checklist.md`.

### L13 — Unrotated credentials
Live-looking API keys/tokens sit in `config.yaml` and `notebooks/.env`. Gitignored (won't be committed) but not rotated. See `DATSCI7030_Repository_Audit_Report.ipynb` §1.
**Handling in write-up:** Not dissertation content — pure hygiene, resolve before submission regardless of write-up status.

### L14 — Stale per-folder READMEs
`data/raw/README.md`, `data/processed/README.md`, `data/external/README.md` describe files that don't match what's on disk. `05_data_dictionary.md` in this folder is the current authoritative source until those are regenerated.
**Handling in write-up:** N/A to dissertation content directly, but affects the "well documented" repository-quality assessment criterion.

---

## Limitations explicitly NOT claimed as limitations (to avoid over-apologising in the write-up)

- The 8-notebook (vs. 10-phase) pipeline structure is a **documented design decision** (`10_decision_log.md`), not a limitation — do not apologise for it in the dissertation, just state the mapping.
- The flat `src/` module layout (six top-level files rather than nested subpackages) is an appropriately-scoped choice for a project of this size, not a shortfall.
