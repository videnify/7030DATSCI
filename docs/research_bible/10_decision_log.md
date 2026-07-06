# 10 — Decision Log

**Purpose:** Every non-trivial scope, design, or methodology decision made during the project, with the reasoning behind it and the date — so choices are defensible to an examiner as deliberate rather than accidental, and so future-you can recall *why* something was done a particular way.
**Owner:** Ibrahim Haroun.
**Dependencies:** Referenced by nearly every other document in this folder; this is the "why" companion to `09_results_log.md`'s "what."
**Update Frequency:** **Every time a real decision is made** — a decision is anything where a reasonable alternative existed and was rejected. Append-only, chronological.
**Relation to Dissertation:** Direct source for dissertation Chapter 3's methodology justifications ("we chose X over Y because...") and for pre-empting examiner questions in the Discussion/Limitations chapters.

---

## How to log a decision

```
### YYYY-MM-DD — <decision title>
**Decision:** <what was decided>
**Alternatives considered:** <what else was on the table>
**Reasoning:** <why this option won>
**Reversible:** Yes/No — under what condition would this be revisited
```

---

### 2026-05-XX — Narrow project scope from broad causal/microstructure design to three RQs

**Decision:** Adopt the three-RQ structure (RQ1 abnormal returns, RQ2 feature importance, RQ3 ML vs. baseline) as the fixed scope, replacing an earlier, broader design (per `01_data_collection.ipynb`'s "v2.0 narrowed scope" title cell).
**Alternatives considered:** Multi-asset causal microstructure analysis; broader macro-event universe beyond presidential communications and FOMC.
**Reasoning:** The brief's own principle — "depth is preferred over breadth" — combined with MSc-dissertation scope constraints (a single semester of implementation time).
**Reversible:** No, without supervisor re-approval — this is the frozen Phase 0 scope referenced throughout `01_research_questions.md`.

---

### 2026-07-XX — Use lexicon sentiment as primary signal, FinBERT as robustness check only

**Decision:** The curated financial/political lexicon scorer is the primary sentiment signal feeding the causal model and feature set; FinBERT is retained only as a secondary/robustness check.
**Alternatives considered:** FinBERT as primary (originally planned, given it's a purpose-built financial-sentiment transformer); an ensemble of both.
**Reasoning:** FinBERT was trained on financial-news headlines and, applied to formal presidential/policy language, produces 95.3% neutral labels — too little discriminative signal for downstream causal/feature use. The lexicon method (73.1% neutral) retains materially more usable variation. See `09_results_log.md` (2026-07-04 entry) for the numbers.
**Reversible:** Yes — if full-text (not title-only) scoring is added in a future iteration, FinBERT's domain mismatch may reduce and this decision should be re-tested, not assumed to still hold.

---

### 2026-07-XX — Rule-based (not ML) event-type classification

**Decision:** Classify APP documents into event categories (monetary, geopolitical, regulatory, trade, energy, health, labour, other) via rule-based keyword matching rather than a trained classifier.
**Alternatives considered:** Supervised ML classifier (would require a labelled training set); unsupervised topic modelling (LDA/BERTopic).
**Reasoning:** No labelled training set exists for this domain-specific category scheme, and rule-based matching is fully inspectable/auditable — an examiner can verify the classification logic directly rather than trusting an opaque model.
**Reversible:** Yes — if mislabelling is found to materially affect RQ1/RQ2 results, revisit with either a small hand-labelled validation set (to measure the rule-based method's precision/recall) or a topic-modelling alternative.

---

### 2026-07-04 — Keep the 8-notebook pipeline rather than splitting to match the 10-phase governing spec

**Decision:** Retain the current 8-notebook structure (sentiment folded into `03_event_detection.ipynb`, explainability folded into `07_model_evaluation.ipynb`) rather than splitting into the full 10-notebook layout described in `docs/00_project_workflow.md`.
**Alternatives considered:** Split `03_event_detection.ipynb` into separate event-detection and sentiment-analysis notebooks; split `07_model_evaluation.ipynb` into separate evaluation and explainability notebooks.
**Reasoning:** Phases 1–8 (as currently structured) are already complete; splitting at this stage adds file-management churn without changing any result, and the brief itself instructs "avoid unnecessary complexity." Phase-to-RQ traceability is preserved regardless of notebook boundaries (`docs/00_project_workflow.md`).
**Reversible:** Yes, low-cost if a supervisor specifically wants the dissertation methodology chapter structured around exactly 10 phases — the underlying code doesn't need to change, only file boundaries. **Status: this decision is proposed here but not yet formally closed** — `docs/00_project_workflow.md` still lists it as an open decision as of 2026-07-04; treat this entry as the recommended resolution, not yet a ratified one.

---

### 2026-07-04 — QQQ / GLD / TLT collected but not yet used downstream

**Decision (interim, not yet finalised):** Continue collecting QQQ, GLD, TLT prices per `config.yaml`, but do not include them in any Phase 3–8 result until a specific, scoped use case is defined.
**Alternatives considered:** Drop them entirely now; use them immediately in a cross-asset generalisation check.
**Reasoning:** Collection cost is low and the data is already in `data/raw/prices.parquet`; but including them without a defined analysis would violate "only include optional datasets if they improve the analysis." No such analysis has been scoped yet.
**Reversible:** Yes — either scope a cross-asset comparison (promote to active use, log a follow-up decision) or drop from `config.yaml`/`data/raw/` and document the exclusion in `05_data_dictionary.md` and `11_limitations.md`. **This decision must be closed one way or the other before submission** — see `13_validation_checklist.md`.

---

### 2026-07-04 — GDELT limited to 5-day proof-of-concept sample

**Decision (interim, not yet finalised):** Keep GDELT wired through the pipeline (`gdelt_daily_risk.parquet` exists and is merged into `daily_sentiment.parquet`) but do not treat any GDELT-derived feature as evidentially final given only a 5-day sample currently exists against a 2015–2025 study period.
**Alternatives considered:** Backfill the full historical GDELT series now; drop GDELT entirely.
**Reasoning:** Backfilling the full series is a non-trivial data-engineering task (GDELT's full historical export is large); dropping entirely would lose a genuinely relevant geopolitical-risk confounder. Interim compromise: keep the plumbing, exclude the feature from any "final" claim until resolved.
**Reversible:** Yes — this is explicitly flagged as needing resolution before Phase 6/7 results are treated as final. See `11_limitations.md` and `13_validation_checklist.md`.

---

### 2026-07-04 — Materialise `master_dataset.parquet` as a new, distinct artefact rather than reusing `model_features.parquet`

**Decision:** Build and freeze `data/processed/master_dataset.parquet` (clean/merged base data, no engineered features) as a new file, rather than treating the existing `model_features.parquet` (91 engineered features) as if it already served this role.
**Alternatives considered:** Rename/repurpose `model_features.parquet` as the "master dataset"; skip a dedicated freeze step entirely and keep letting `05_feature_engineering.ipynb` re-derive the merge in-memory each run.
**Reasoning:** `model_features.parquet` is already a downstream, feature-engineered product (lags, rolling windows, technical indicators) — collapsing it with the upstream "clean, merged" concept would blur the Phase 2/Phase 5 boundary and make it harder to audit each stage independently (e.g. this freeze's look-ahead-bias check is only meaningful at the pre-feature-engineering stage, before rolling windows introduce their own boundary effects). Re-deriving the merge in-memory each run (the prior status quo) meant there was no single frozen, versioned, independently-validated base dataset to point to — a reproducibility and auditability gap. Creating one new, clearly-scoped file closes that gap without duplicating `model_features.parquet`'s content (different column set: 34 raw/merged columns vs. 95 engineered columns).
**Reversible:** Low-cost to reverse if this proves redundant in practice — but not expected to be, since it directly satisfies the original 10-phase spec's "Create master dataframe" step (`docs/00_project_workflow.md` Phase 3), which the 8-notebook implementation had otherwise dropped.

---

### 2026-07-04 — Statistical Analysis Plan v1.0 frozen (Mission 04)

**Decision:** Freeze the complete Statistical Analysis Plan across five new documents (`statistical_analysis_plan.md`, `statistical_decision_matrix.md`, `statistical_assumptions.md`, `statistical_reporting_guidelines.md`, `dataset_contract.md`) plus an expanded `04_statistics_plan.md`, covering: α/CI/one-sided-vs-two-sided policy, multiple-comparison corrections, missing-data/outlier/transformation/scaling/stationarity policy, the full assumption matrix, the master test matrix (run and frozen-not-yet-run), and the exact RQ3 model-comparison protocol.
**Alternatives considered:** (a) Treat this SAP as a strict pre-registration written before any analysis — not honest, since Phases 1–8 already ran; (b) skip the freeze and let each remaining notebook (Missions 05–08) choose its own statistical methods ad hoc.
**Reasoning:** Option (a) would misrepresent the project's actual sequencing to an examiner. Option (b) risks exactly the kind of undocumented methodological drift the Research Bible exists to prevent. The adopted approach — ratify already-used RQ1/RQ2 methodology as-is (no numbers changed), freeze RQ3's remaining protocol prospectively before the baseline is trained — is stated explicitly in `statistical_analysis_plan.md`'s "Status of this freeze" section so the partial-retrospective nature is disclosed, not hidden.
**Additional judgment calls made and logged here for traceability:**
- **One-sided testing adopted for RQ3 only** (model-vs-baseline "outperforms" comparisons), two-sided remains the default everywhere else — directional test matches the already-existing directional wording of H3 in `02_hypotheses.md`, not introduced to inflate significance.
- **No outlier removal/winsorisation policy** — extreme return days are treated as signal, not noise, in an event-driven study; removing them would bias RQ1 toward smaller, "safer" effects.
- **VIF (>10), correlation (>0.90), and variance (<1e-8) thresholds** frozen for Mission 05, prospectively — previously undocumented.
- **Random Forest is not added as a fourth RQ3 predictive model**, despite the mission brief's Part K wording naming it alongside LASSO/XGBoost/LightGBM — RF stays an RQ2 importance tool only, per the existing `07_model_plan.md` candidate set. Flagged as an open scope question in `statistical_decision_matrix.md`, not silently resolved either way; revisiting it requires a Version 2 SAP amendment.
**Reversible:** Yes, via a numbered Version 2+ SAP amendment logged here — this entry establishes that governance rule going forward (no untracked statistical-method changes after v1.0).

---

### 2026-07-04 — Market-only baseline model not yet added (RQ3 gap) — ✅ resolved 2026-07-05, see below

**Decision:** Defer training the market-only baseline model until a dedicated session, rather than rushing a poorly-tuned baseline into the pipeline.
**Alternatives considered:** Add a quick untuned baseline immediately to "have a number."
**Reasoning:** An untuned baseline would bias the comparison in favour of the full-feature models (they were tuned; the baseline wouldn't be), producing a misleading RQ3 answer that looks resolved but isn't methodologically sound. Better to log the gap explicitly (`07_model_plan.md`) than to close it superficially.
**Reversible:** N/A — this is a sequencing decision, not a permanent one; see `07_model_plan.md` for the full specification of what needs to happen next.
**Resolution:** Closed 2026-07-05 (Mission 06) — see the "Market-only baseline (`Baseline_LASSO` v1.0) trained" entry below.

---

### 2026-07-05 — Feature Matrix v1.0 (FES v1.0) frozen; `car_results.parquet` approved as a second Mission 05B input

**Decision:** Freeze `data/processed/feature_matrix.parquet` (95 engineered features, 2,511 rows) built from exactly two inputs: `master_dataset.parquet` (v1.0, frozen) and `data/processed/car_results.parquet` (Phase-4 event-study output). `car_results.parquet` was **not** in Mission 05B's originally stated input list — this entry formally approves it as a second, explicit input, subject to a hard restriction: CAR/event-derived features built from it may be used only in event-enhanced models, never in the market-only baseline.
**Alternatives considered:** (a) Strict `master_dataset.parquet`-only scope, dropping `mean_car` and all CAR-derived event counts from the new canonical feature matrix entirely, since `master_dataset.parquet` alone cannot reconstruct them; (b) the adopted option, joining `car_results.parquet`'s daily aggregates as a second, explicitly-documented input.
**Reasoning:** `mean_car` is the single highest-ranked feature in the pre-freeze RQ2 result (`09_results_log.md`, 16.1% RF importance) and is required to test RQ2 and RQ3 meaningfully — dropping it would silently weaken the project's strongest existing finding for the sake of a stricter reading of Mission 05B's input list. `car_results.parquet` is itself an already-frozen, versioned Phase-4 artefact (not a "raw" source), so joining it does not violate `dataset_contract.md` term 2 (that term restricts re-deriving the *raw* price/VIX/macro/sentiment merge from `data/raw/*`, not incorporating another already-processed artefact). The restriction — CAR/event/sentiment features excluded from the market-only baseline, permitted only in event-enhanced models — is enforced structurally in `feature_contract.md`'s Baseline Eligibility table, not left as a convention a notebook could forget.
**Additional judgment calls made and logged here for traceability:**
- **`events_tagged.parquet`/`high_impact_events.parquet` remain out of scope.** `n_high_impact_events`, `days_since_hi_event`, and `high_impact_day` (present in the legacy `model_features.parquet`) require `is_high_impact`, which lives only in those two files — not approved as inputs here. Replaced by `sig_event_x_momentum` (uses the in-scope `n_sig_events` flag) where an equivalent interaction was needed. Re-adding them is a defined v1.1 candidate.
- **Warm-up/boundary rows are trimmed strictly**, per SAP v1.0's "trim, never back-fill" policy — 254 rows dropped (vs. `model_features.parquet`'s 2, which pre-dates the SAP freeze and did not trim as strictly). Train split shrinks from 2,014 to 1,761 usable rows; test split is unaffected (750, unchanged) since the longest warm-up window (200 days) falls entirely within 2015–2016.
- **Two documentation gaps fixed during the rebuild:** `momentum_21d` and `monetary_x_rate_cut` existed as real columns in the legacy `model_features.parquet` but were missing from the pre-freeze `06_feature_dictionary.md` tables. Both are included and documented in FES v1.0, correcting the Market category count to 27 (not 26) and the Interaction category to 8 (not 7) — `statistical_decision_matrix.md`'s "26 features (price + technical only)" baseline description should be read as 27 until that document is itself updated at Mission 06.
- **Variance/correlation/VIF thresholds applied for flagging, not automatic feature removal**, per `04_statistics_plan.md`/`statistical_assumptions.md` — 0 near-zero-variance features (after fixing a build bug where `car_event_day` was initially computed as a constant 1.0 for all rows — caught by the validation script, not shipped), 6 correlation pairs flagged (\|r\|>0.90), 10 features flagged VIF>10, all structurally expected (overlapping rolling windows, an interaction term correlated with its own parent, momentum vs. cumulative-return near-identity) and documented per-feature in `06_feature_dictionary.md` rather than silently dropped.
- **RF-importance selection is explicitly out of scope for this freeze** — Mission 05B produces the full, validated 95-feature candidate matrix; selecting a subset by RF importance (0.001 threshold, already-frozen from Phase 5) is a separate, later step, consistent with `14_project_dashboard.md`'s framing of Mission 05B as running "ahead of the existing RF-importance selection step."
- **Scaling parameters (train-split-only mean/std) are persisted in `feature_profile.json`, not baked into `feature_matrix.parquet`.** The frozen file stores raw engineered values — mirrors `dataset_contract.md` term 7's "scaling happens downstream" principle exactly, applied one layer further down the pipeline.
**Reversible:** Yes, via a new numbered Feature Matrix version (`v1.1`, `v2.0`) and a corresponding decision-log entry — e.g. re-adding `events_tagged.parquet`/`high_impact_events.parquet` as a third approved input, or revisiting the momentum/cumulative-return near-duplication once RF-selection results are in.

---

### 2026-07-05 — Market-only baseline (`Baseline_LASSO` v1.0) trained; Model Contract Protocol (MCP v1.0) frozen (Mission 06)

**Decision:** Train and freeze `Baseline_LASSO` (LassoCV, 27 Market-category features from `feature_matrix.parquet`, `TimeSeriesSplit(5)`, seed 42) as the project's official RQ3 benchmark, and freeze `model_contract.md` (MCP v1.0) governing which models are approved, how they're evaluated, and what "beats the baseline" means. Keep the baseline's outputs in dedicated `reports/baseline/`/`models/baseline/` files rather than joining `data/processed/model_comparison.parquet` or running the DM/two-proportion z-test comparison in this mission.
**Alternatives considered:** (a) Join `Baseline_LASSO` into `model_comparison.parquet` and run the full comparison against the existing full-feature LASSO/XGBoost/LightGBM immediately, closing RQ3 in one mission; (b) the adopted option — train and document the baseline only, deferring the comparison to Mission 07.
**Reasoning:** Mission 06's brief explicitly restricts comparing against event-enhanced models ("do NOT compare against event models yet") and the existing full-feature models were trained on the now-superseded `model_features.parquet`, not on `feature_matrix.parquet` (FES v1.0) — a same-feature-matrix comparison is not yet possible without retraining them, which is explicitly Mission 07's job, not Mission 06's. Keeping "baseline exists" and "baseline has been compared" as two separable steps also makes each step independently auditable.
**Additional judgment calls made and logged here for traceability:**
- **A single model family (LASSO) is used for the baseline, not a tree-based alternative.** Keeps model architecture constant across the RQ3 comparison (only feature scope varies) — already the reasoning frozen in `07_model_plan.md` prior to this mission, ratified again here.
- **Legacy `TimeSeriesSplit`-vs-`KFold` bug fixed.** `src/models.py: _lasso_baseline()` passed `LassoCV(cv=5, ...)`, which defaults to a shuffled `KFold`, silently violating `statistical_analysis_plan.md`'s "TimeSeriesSplit, never a random/shuffled split" policy. `Baseline_LASSO`'s build passes an explicit `TimeSeriesSplit(n_splits=5)` object instead — a correction, not a new methodological choice.
- **All 27 Market coefficients shrunk to zero at the CV-selected alpha — reported exactly as obtained, not re-tuned or adjusted.** This makes `Baseline_LASSO` numerically identical to a trivial mean predictor on every metric. This was verified deliberately (coefficient vector inspected directly, confirmed reproducible across two independent re-runs) rather than assumed to be a fitting error. See `09_results_log.md` (2026-07-05 entry) and `baseline_evaluation.md` Part G for the full interpretation.
- **Random Guess and Persistence comparators computed for context only**, per Mission 06 Part D — neither is a candidate RQ3 model; both exist solely so `Baseline_LASSO`'s numbers are read against a floor, not in isolation.
- **Scaling reused from `feature_profile.json`'s persisted train-split parameters, not refit.** Keeps `Baseline_LASSO` and any future Mission-07 model numerically consistent on the same 27 columns, and satisfies the "no undocumented preprocessing" QA requirement.
**Reversible:** Yes, via a new Baseline model version (`Baseline_LASSO v1.1`) if, e.g., a supervisor requests a market-only tree-based baseline in addition, or if a future Feature Matrix version changes the Market category's column set — each such change requires a `10_decision_log.md` entry and a version bump, per `model_contract.md`'s Versioning section.

---

### 2026-07-05 — Event-enhanced models retrained on FES v1.0; RQ3 comparison complete (Mission 07)

**Decision:** Retrain Event_LASSO, XGBoost, and LightGBM on `feature_matrix.parquet` (FES v1.0, 95 features) — the legacy versions of these models (trained on the superseded `model_features.parquet`) are not valid comparators against `Baseline_LASSO` (Mission 06), since a fair RQ3 comparison requires every model to read the identical frozen feature matrix. Run the frozen Diebold-Mariano + two-proportion z-test + Bonferroni protocol (`statistical_decision_matrix.md` Part K) against `Baseline_LASSO`, and re-run Random Forest importance + SHAP on the new matrix, replacing all legacy `model_features.parquet`-derived importance values.
**Alternatives considered:** (a) Compare the legacy full-feature models (trained on `model_features.parquet`) directly against `Baseline_LASSO` (trained on `feature_matrix.parquet`) without retraining — rejected, since the two model sets would differ in both feature set *and* feature matrix provenance, confounding the comparison; (b) the adopted option — retrain all three on the identical frozen matrix first.
**Reasoning:** MCP v1.0's fairness requirement ("every model MUST use the identical frozen feature_matrix.parquet") is not satisfiable by reusing legacy model objects. Retraining is a mechanical, reproducible step (documented hyperparameters/tuning/seed in `models/event/event_model_metadata.json`) and does not constitute a dataset, feature-engineering, or statistical-methodology change — it is applying the already-frozen protocols to the already-frozen matrix, exactly as Mission 07's restrictions require.
**Additional judgment calls made and logged here for traceability:**
- **Result: H0₃ is not rejected.** None of the three event-enhanced models clears the Bonferroni-corrected threshold (α = 0.0167) on either the RMSE (Diebold-Mariano) or directional-accuracy (two-proportion z-test) leg against `Baseline_LASSO`. Reported plainly as a null finding, per `02_hypotheses.md`'s explicit discipline that a null result is a valid, reportable outcome — not reframed or downplayed.
- **XGBoost/LightGBM tuned via `RandomizedSearchCV` with `TimeSeriesSplit(5)` (n_iter=25, seed 42) — genuine, documented tuning**, not left at `config.yaml`'s fixed defaults, to satisfy MCP v1.0's "no model wins purely on unequal tuning effort" fairness rule. `n_jobs=1` set on the base estimator (with `n_jobs=-1` on the search) to avoid nested-parallelism slowdown — a performance fix, not a methodological choice.
- **Comparison table and statistical tests kept in `reports/model_comparison/`, not overwriting `data/processed/model_comparison.parquet`.** Same "new canonical artefact, old one stays as a legacy record" pattern already used for `master_dataset.parquet`→no successor-needed and `model_features.parquet`→`feature_matrix.parquet` — keeps the FES v1.0-based comparison auditable as a distinct, complete artefact rather than silently mutating a pre-existing file with mixed provenance.
- **BH-FDR correction confirmed not applicable to this mission** — it governs RQ1's event-type family only (`statistical_analysis_plan.md` Part A); RQ3's frozen correction is Bonferroni, applied as specified. Stated explicitly in `reports/model_comparison/statistical_tests.json` so a future reader does not mistake its absence for an oversight.
- **SHAP computed via each library's native contribution API (`xgboost`'s `pred_contribs=True`, `lightgbm`'s `pred_contrib=True`) and the closed-form exact linear-SHAP identity for Event_LASSO — no external `shap`/`numba` package used.** These give mathematically exact TreeSHAP/linear-SHAP values (verified: every model's SHAP values sum exactly to its own prediction), not an approximation — chosen after the `shap` package's `numba` dependency proved impractical to install in the working environment; this is a tooling substitution with an equivalent (in fact exact, not sampled) result, not a methodological compromise.
- **Random Forest confirmed, again, as an importance-only tool** — fit once with fixed hyperparameters (not tuned via CV, since it is not a predictive candidate), consistent with `statistical_decision_matrix.md` Part K's "Open scope question" resolution and `model_contract.md`'s Approved Models table.
- **Directional-accuracy comparison caveat logged:** `Baseline_LASSO`'s test Dir. Acc. (0.575) is a degenerate artefact of its constant-positive prediction matching the test period's base rate — the two-proportion z-test against it is run exactly as the frozen SAP protocol specifies, but its interpretive weight is lower than the RMSE leg for this specific baseline version. Logged here so a future baseline version's comparison is read correctly relative to this one.
**Reversible:** Yes — a future Feature Matrix version, Baseline version, or model retuning requires a new decision-log entry and version bump (`model_contract.md` Versioning), and the RQ3 verdict above must be re-tested, not assumed to still hold.
