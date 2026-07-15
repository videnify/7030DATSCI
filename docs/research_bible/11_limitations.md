# 11 — Limitations

**Purpose:** A complete, honest inventory of the project's known weaknesses, scoped-out work, and methodological compromises — written so the dissertation's Limitations chapter is prepared in advance rather than assembled defensively after an examiner asks. Every entry states how it should be handled in the write-up.
**Owner:** Ibrahim Haroun.
**Dependencies:** All other Research Bible documents feed this one; cross-referenced throughout.
**Update Frequency:** Add an entry the moment a limitation is discovered — do not wait until the dissertation-writing phase to compile this list from memory.
**Relation to Dissertation:** Direct source for dissertation Chapter 5 (Discussion) §5.x (Limitations) and for pre-empting viva questions.

---

## Research-validity limitations (affect what can be claimed)

### L1 — Market-only baseline gap (resolved 2026-07-14)
`Baseline_LASSO` v1.1 now provides the required 27-feature market-only comparator under the same split and validation discipline as the event-enhanced candidates. Notebook 07 applied the frozen two-leg, Bonferroni-corrected comparison: no candidate beats the baseline, so H0₃ is not rejected.
**Handling in write-up:** Report this as a resolved governance gap and a current null result, not as unfinished future work.

### L2 — Baseline directional accuracy is a base-rate artefact
`Baseline_LASSO` and Event_LASSO both predict the positive training mean on every test day and therefore obtain directional accuracy 57.47%, exactly the test period's up-day share. ROC-AUC is 0.500 and the prediction series has no rank information. XGBoost (48.93%) and LightGBM (44.27%) are lower.
**Handling in write-up:** Do not describe 57.47% as predictive skill or an edge over chance. State that it is produced mechanically by a constant-positive forecast and use the corrected model-comparison tests for RQ3.

### L3 — Event-type CAR family correction (resolved reporting gap)
**Resolved 2026-07-15.** Notebook 04 now reports five event-type mean-CAR 95% t intervals, Cohen's d and Benjamini–Hochberg FDR-adjusted q-values. No null is rejected (minimum q=0.5810), every interval crosses zero, and the largest |d| is 0.239. The earlier “geopolitical events are significant” result remains superseded.
**Handling in write-up:** Report the multiplicity-controlled null table from `event_type_statistics.parquet`. Do not treat the 15 individual-window flags as event-type evidence or revive the superseded result.

### L4 — Event clustering violates independence assumption (not currently mitigated)
Presidential communications cluster in time (e.g. multiple statements during a single crisis week), violating the event-study t-test's independence assumption. **Corrected 2026-07-07** (previously this entry claimed the violation was "mitigated by testing on CAAR (event-type averages) rather than pooled raw CAR" — verified false against `04_causal_analysis.ipynb` Cell 7 during the Chapter 3 Section 3.3 dissertation revision: the notebook tests pooled, event-level CAR directly, not event-type-averaged CAAR. See `04_statistics_plan.md` "Event Study Tests" and `10_decision_log.md`, 2026-07-07 entry.) The violation is therefore **not currently mitigated** in the implemented pipeline.
**Handling in write-up:** State this as a standard limitation of event-study methodology applied to clustered communications. BH-FDR controls multiplicity across types but does not repair within-type temporal dependence; no cluster-robust or date-clustered estimator is implemented.

### L5 — Sentiment scored on titles only, not full text
FinBERT operates on the economically filtered APP document *titles* (`app_presidential_documents_economic.parquet: title`), not full transcripts. A title-level signal is a coarser proxy for the communication's actual content and tone.
**Handling in write-up:** State explicitly as a scope limitation; note that full-text scoring is a natural extension (see also L6, FinBERT domain mismatch, which full-text scoring might also partially address).

### L6 — FinBERT domain mismatch
FinBERT — the project's official primary sentiment engine (Sentiment Engine Freeze v1.0, 2026-07-06 — see `10_decision_log.md`) — is trained on financial-news headlines, not political/policy language. In the current 1,005-event catalogue, 929 events (92.44%) are neutral, 43 (4.28%) positive, and 33 (3.28%) negative; 916 APP events are FinBERT-scored and 89 FOMC events use structured outcomes. The lexicon scorer is retained only as a fallback/historical prototype and is not a current event source.
**Handling in write-up:** Report both methods' distributions (already done in `09_results_log.md`), justify FinBERT as the adopted primary engine despite its neutral-heavy output (SEF v1.0 rationale: it matches what the pipeline actually runs and produces), and note that neither method has been validated against human-labelled ground truth for this domain — a genuine open validity question.

### L7 — GDELT backfilled to full history (2026-07-13) but not yet feature-engineered into any RQ2/RQ3 model
**Updated 2026-07-14:** the full 4,018-day GDELT series remains present in `master_dataset.parquet` v1.2. The remaining limitation is narrower: `feature_matrix.parquet` (FES v1.1) does not engineer any feature from it, so no RQ2/RQ3 result uses a GDELT-derived predictor. A direct check also found that daily-averaged GDELT tone never reaches the existing high-impact threshold, so GDELT is not a discrete event source.
**Handling in write-up:** State that the full GDELT series is now available in the base dataset as a candidate control, but that the frozen DoWhy DAG and FES v1.1 exclude it. No reported RQ1–RQ3 result uses a GDELT-derived feature; adding one would require a new causal/feature specification rather than merely relabelling the current analysis.

### L8 — QQQ/GLD/TLT collected but unused
Collected per `config.yaml` but not used in any downstream RQ1–RQ3 result as of 2026-07-04. Currently dead weight in the data dictionary with no defined analytical purpose.
**Handling in write-up:** Either scope and run the cross-asset generalisation check before submission (promotes this from limitation to a genuine RQ1 robustness section), or drop from the pipeline and note as "considered but out of scope" — see `10_decision_log.md`, decision must close before submission.

### L9 — XGBoost overfitting not yet root-caused
On FES v1.1, XGBoost's train R² is 0.2225 and its test R² is −0.0067; directional accuracy falls from 65.55% to 48.93%. The comparison documents this generalisation gap, but no dedicated regularisation-sensitivity or learning-curve investigation has isolated its cause.
**Handling in write-up:** Either investigate and report the cause (feature-count-to-sample-size ratio, insufficient regularisation, etc.) or explicitly flag XGBoost's result as unreliable/overfit in the RQ3 narrative rather than letting the test-set row stand unqualified.

### L10 — No claim of tradeable strategy performance
Figures such as `07d_strategy_performance.png` and the strategy panel in `08d_full_dashboard.png` show illustrative cumulative-return signal, not a backtested strategy net of transaction costs, slippage, or realistic position sizing.
**Handling in write-up:** Caption these figures explicitly as directional-signal illustrations; the dissertation must not claim or imply a profitable trading strategy has been demonstrated.

### L11 — Single-asset focus (SPY only for causal/predictive claims)
Despite collecting four tickers, all RQ1–RQ3 evidence is SPY-specific. Findings should not be generalised to other asset classes without the (currently unscoped) cross-asset analysis in L8.
**Handling in write-up:** State the single-asset scope explicitly in the Introduction/Methodology, not just implicitly through the figures used.

---

### L15 — Random Forest feature-importance reproducibility gap (resolved 2026-07-14)

Notebook 07 now contains and executes the approved fixed Random Forest step (`RandomForestRegressor`, 500 trees, seed 42, all 92 FES v1.1 features). It persists both the trained tool and the complete ranked table, and both are hash-bound by `model_evaluation_validation.json`. The earlier FES v1.0 artefact remains archived.
**Handling in write-up:** Describe Random Forest as a reproducible descriptive RQ2 ranking tool, not an RQ3 candidate or a classical significance test. Report that the frozen joint top-decile rule is not met even though LightGBM SHAP gives `mean_car` a high model-specific rank.

---

### L16 — Historical FES v1.0 zero-variance exception (resolved in FES v1.1)

**Resolved by FES v1.1 on 2026-07-14.** The FES v1.0 rebuild correctly failed because `labour` and `labour_event_day` were constant zero, and its narrowly approved `ACCEPTED_WITH_KNOWN_EXCEPTION` disposition is retained in the local pre-FES-v1.1 archive as historical governance evidence. FES v1.1 fixes the cause rather than carrying the exception: `labour_event_day` now derives from `n_labour_catalogue_events > 0`, while `labour`, `energy`, and `monetary_x_rate_cut` are removed because their training-split variance is below 1e-8. The resulting 92-feature matrix passes validation with no constant or near-zero-variance columns. Notebooks 06–08 and their baseline, model-comparison, and figure validation artefacts are current.

**Handling in write-up:** Describe the old exception only as the trigger for the corrective migration. Report that FES v1.1 uses direct occurrence, removes all three zero-training-variance features, and passes validation. Label archived pre-migration RQ2/RQ3 numbers as FES v1.0.

---

### L17 — Same-date trading-calendar alignment excludes weekend and market-holiday event dates

Dataset v1.2 aligns catalogue occurrences to the SPY trading calendar using the same calendar date and does not move events to the next open session. Consequently, 2 health, 7 labour, and 32 other catalogue events fall outside the trading-day panel; included totals are 12/96/395 rather than the all-calendar totals 14/103/427. This is explicit in `master_dataset_validation.json`, not a missing-data accident. The policy avoids silently choosing a causal timing convention, but it may understate first-session-after-event effects.

**Handling in write-up:** State the same-date alignment rule and the excluded counts. Treat next-session reassignment as a sensitivity analysis/future extension unless it is formally added through a new dataset/SAP amendment.

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
