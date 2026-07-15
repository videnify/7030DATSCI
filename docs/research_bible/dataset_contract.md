# Dataset Contract — `master_dataset.parquet` (SAP v1.0)

**Purpose:** The interface contract every downstream notebook must honour when reading `master_dataset.parquet` — distinct from `dataset_version.md`, which is the freeze/versioning *record* (what was built, when, and its validation report). This document is the *rulebook* for anyone (a future notebook, a future you, an examiner re-running the pipeline) consuming that frozen file. If `dataset_version.md` is the birth certificate, this is the terms of use.
**Owner:** Research Statistician sign-off (consumption rules), Senior Data Science Architect (schema authority).
**Dependencies:** `dataset_version.md` (schema and validation source of truth — this document does not repeat that schema table, it references it), `statistical_analysis_plan.md` Part A (missing-data, outlier, transformation, stationarity policies this contract enforces at the consumption boundary).
**Update Frequency:** Update only if the contract terms change (e.g. a new consumption rule is added) — a schema change belongs in `dataset_version.md` as a new dataset version, not here.
**Relation to Dissertation:** Supports the reproducibility appendix (Chapter 3 §3.6) — states precisely what "reproducible" means at the data-interface level.

---

## Why this document exists separately from `dataset_version.md`

`dataset_version.md` answers "what is `master_dataset.parquet`, and did it pass validation." This document answers a different question: "what am I allowed to do with it, and what must I never do with it." Collapsing the two would blur a versioning record with a set of ongoing behavioural rules — the same reasoning `10_decision_log.md` already gives for keeping `master_dataset.parquet` itself distinct from `model_features.parquet`.

---

## Contract terms

1. **Read-only.** No notebook may write to, overwrite, or hand-edit `master_dataset.parquet` directly. A schema or content change requires a new version (`v1.1`, `v2.0`) built by a dedicated freeze step and logged in `dataset_version.md` + `10_decision_log.md` — never an in-place edit.
2. **Single source for the merge.** `05_feature_engineering.ipynb` (and any future feature-matrix rebuild, Mission 05) must read `master_dataset.parquet` as its input and must not independently re-derive the raw price/VIX/macro/sentiment merge from `data/raw/*` — doing so would create two divergent "ground truths" for the same underlying data.
3. **No `NaN` back-filling.** The two structurally expected `NaN`s (`log_return` first row, `fwd_return_1d` last row) must be preserved as `NaN` through any downstream join — never filled with 0, a mean, or a forward-fill. Filling them would silently violate the leakage proof in `dataset_version.md`.
4. **Lag/rolling operations must be non-anticipative.** Any feature derived from this dataset via a rolling or lag operation must use `.shift(n)` with `n ≥ 0` relative to `date` — a centred or backward-looking window that reaches into `t+1` is prohibited outright, per `statistical_assumptions.md`'s "Temporal leakage" row. This is a hard gate: a pull request or notebook cell that violates it should not be merged/run, not merely flagged for later review.
5. **Split column is authoritative.** The `split` column (`"train"` / `"test"`) fixed in this dataset is the single source of truth for the chronological boundary (train 2015-01-02 → 2022-12-30, test 2023-01-03 → 2025-12-30). No notebook may redefine or re-derive a different split independently — doing so would silently break comparability between RQ2's feature-selection results and RQ3's model comparison, both of which must use the identical boundary.
6. **Optional cross-assets are absent; `gdelt_*` remains scope-limited.** QQQ/GLD/TLT are not present in the actual Dataset v1.2 schema because no approved raw source was available at freeze time; consumers must not assume otherwise. GDELT carries the full 2015–2025 history but remains outside FES v1.1. Its presence in the base dataset is not permission to introduce it into a reported model without a versioned FES amendment.
7. **Scaling happens downstream, not here.** `master_dataset.parquet` is unscaled by design (`StandardScaler` is fit at the feature-engineering stage on the training split only, per `statistical_analysis_plan.md` Part A) — a notebook must never assume this file's numeric columns are already standardised.
8. **Stationarity checks precede modelling use.** Before any macro **level** column in this dataset (`fed_funds_rate`, `cpi`, `treasury_10y`, etc.) is fed to a linear model, the stationarity check in `statistical_assumptions.md` Part H must be run; if it fails, the already-engineered first-differenced version (`cpi_mom`, `fed_rate_change`, `yield_spread_change` — built downstream in `model_features.parquet`, not present in this base dataset) must be used instead.
9. **Row-count reconciliation is expected, not a bug.** This dataset's row count (2,765) will always be 1–2 rows higher per split than any downstream feature matrix built from it, because lag/rolling-window warm-up rows are valid here and trimmed downstream — a notebook finding this discrepancy should not "fix" it by padding or interpolating the downstream file; see `dataset_version.md` and `05_data_dictionary.md`'s row-count sanity section.
10. **Version pinning.** Any notebook or script reading this file should state which version it was validated against (currently v1.2, 2026-07-14 — 2,765 rows × 34 columns, including three explicit occurrence counts) in its header/purpose cell. If `dataset_version.md` shows a newer version exists, re-validate outputs rather than assuming forward compatibility.
11. **Occurrence counts are authoritative for category presence.** For health, labour, and other, downstream event-day flags must use `n_<category>_catalogue_events > 0`; they must not infer occurrence from `health`, `labour`, or `other` sentiment being non-zero. The base dataset uses same-calendar-date alignment to the SPY trading calendar and does not move weekend/holiday events to the next session.

---

## Consumers of this contract (updated 2026-07-14)

| Consumer | Relationship |
|---|---|
| `05_feature_engineering.ipynb` | Primary consumer — completed FES v1.1 build reads Dataset v1.2 and uses term 11 for health/labour/other event-day flags |
| Mission 06 (Baseline Model) | Consumes the same feature matrix Mission 05 produces from this file — must inherit the identical `split` boundary (term 5) |
| Any future re-run of Phases 1–8 | Must re-validate against this contract before trusting outputs, per term 10 |

---

## Definition of Done — this document

- [x] Distinguishes this contract's role from `dataset_version.md`'s versioning-record role, explicitly
- [x] Read-only, no-backfill, non-anticipative-lag, and split-authority rules stated as hard gates, not guidelines
- [x] Actual absence of QQQ/GLD/TLT and the remaining GDELT scope boundary documented
- [x] Explicit occurrence counts made authoritative for health/labour/other event-day flags
- [x] Named consumers listed so the contract has a concrete enforcement point (Mission 05)
