# Feature Contract — `feature_matrix.parquet` (FES v1.0)

**Purpose:** The interface contract every downstream notebook (Baseline, XGBoost, LightGBM, Explainability — Missions 06–08) must honour when reading `feature_matrix.parquet`. Distinct from `06_feature_dictionary.md` (what each feature *means*) the same way `dataset_contract.md` is distinct from `dataset_version.md` — this document is the rulebook for *consuming* the frozen file, not a description of its contents.
**Owner:** Research Statistician sign-off (consumption rules), Senior Data Science Architect (schema authority).
**Dependencies:** `dataset_contract.md` (the upstream contract this one extends), `statistical_analysis_plan.md` Part A (scaling/missing-data/transformation policy this contract enforces), `06_feature_dictionary.md` (per-feature detail), `feature_matrix_validation.json` / `feature_profile.json` (the machine-checkable evidence backing this contract).
**Update Frequency:** Update only if a contract *term* changes. A feature added/removed/redefined is a new Feature Matrix version (`v1.1`, `v2.0`) with a `10_decision_log.md` entry — never an in-place edit of `feature_matrix.parquet`.
**Relation to Dissertation:** Supports the reproducibility appendix (Chapter 3 §3.6) and Chapter 3 §3.3 (Feature Engineering) — states precisely what every RQ2/RQ3 model is permitted to consume.

---

## Feature Matrix Version

**FES v1.0 — frozen 2026-07-05.** No feature may be added, removed, or redefined without a `10_decision_log.md` entry and a new numbered version.

## Permitted consumers

| Consumer | Relationship |
|---|---|
| Mission 06 — Baseline Model (`Baseline_LASSO`) | Must read **only** the Market-category columns (see Baseline Eligibility below) — reading any other category into the baseline is a protocol violation of `statistical_decision_matrix.md` Part K |
| Mission 06/07 — Event-enhanced models (LASSO, XGBoost, LightGBM) | May read the full 95-feature set |
| Mission 08 — Explainability (SHAP, PDP) | Reads whichever feature set the model it explains was trained on — must not silently mix baseline and full-feature SHAP values |
| Any future re-run of Missions 06–08 | Must re-validate against this contract before trusting outputs (see Validation Requirements below) |

**No notebook may bypass this contract** by re-deriving features independently from `master_dataset.parquet` or `car_results.parquet` — `feature_matrix.parquet` is the single source of engineered features from this point forward.

## Notebook dependencies

`feature_matrix.parquet` is built by the feature-engineering step of the pipeline (repo notebook: `05_feature_engineering.ipynb`, to be updated to read from this contract rather than re-deriving features in-memory — see `10_decision_log.md`). It depends on exactly two upstream artefacts:

1. `data/processed/master_dataset.parquet` (v1.0, frozen 2026-07-04) — market, macro, and daily sentiment aggregates.
2. `data/processed/car_results.parquet` (Phase-4 event-study output) — event-study daily aggregates (`mean_car`, significance flag, per-category event-day indicators). Approved as a second input specifically for this freeze — see the 2026-07-05 decision log entry. No other processed artefact (`events_tagged.parquet`, `high_impact_events.parquet`, `gdelt_daily_risk.parquet`) feeds this version; their absence is a deliberate v1.0 scope boundary, not an oversight (see `06_feature_dictionary.md` "Explicitly out of scope for v1.0").

## Target variable

`fwd_return_1d` — forward 1-day SPY log return, carried through unchanged from `master_dataset.parquet`. This is the **sole** frozen target for FES v1.0. `fwd_return_5d`/`fwd_return_10d` are explicitly **not** engineered in this version — RQ3's primary comparison uses only `fwd_return_1d` (`statistical_analysis_plan.md` Part B), and adding unused secondary targets would be scope creep without a stated purpose.

## Prediction horizon

1 trading day ahead, matching the target definition above and `dataset_version.md`'s `fwd_return_1d` construction (`log(close_{t+1}/close_t)`).

## Scaling rules

`feature_matrix.parquet` stores **raw, unscaled** engineered values — mirroring `dataset_contract.md` term 7's principle that scaling happens downstream, not at the artefact-freeze stage. `feature_profile.json`'s `scaling.parameters` block records the per-feature mean/std **fitted on the training split only** (rows where `split == "train"`). Any notebook training a model must:

1. Apply `(x - mean) / std` using exactly these persisted parameters — never refit a scaler on the full matrix (train+test), which would leak test-split distributional information into the scaling step.
2. Apply scaling uniformly to every engineered feature, including binary flags, per `statistical_analysis_plan.md` Part A's explicit policy (keeps the input matrix identical in shape/treatment across LASSO/XGBoost/LightGBM so model architecture is the only varying factor).

## Encoding rules

No one-hot or label encoding is required anywhere in this matrix. The only calendar/periodic variables (`dow_sin`/`dow_cos`/`month_sin`/`month_cos`) are cyclically encoded at build time; `quarter_num` is left as a small ordinal integer (1–4) since a 4-level ordinal does not warrant cyclical or one-hot treatment. No other engineered feature is categorical.

## Baseline eligibility (enforces `statistical_decision_matrix.md` Part K)

| Category | Allowed in Market-Only Baseline (`Baseline_LASSO`) | Allowed in Event-Enhanced Models |
|---|:---:|:---:|
| Market (27 features) | ✅ Yes | ✅ Yes |
| Macro & VIX (16) | ❌ No | ✅ Yes |
| Sentiment (25) | ❌ No | ✅ Yes |
| Event (14) | ❌ No | ✅ Yes |
| Temporal (5) | ❌ No | ✅ Yes |
| Interaction (8) | ❌ No | ✅ Yes |

**Rule (per the 2026-07-05 decision log entry):** the market-only baseline may use Market-category columns only. Every Macro/Sentiment/Event/Temporal/Interaction column is event-enhanced-only — this is the hard gate that prevents accidental leakage of event information into the baseline `statistical_decision_matrix.md` Part K depends on. All 8 interaction features mix an event/macro/sentiment term with a market term by construction, so none qualify for baseline use even partially.

## Validation requirements

Before any notebook trains on this file, it must confirm `feature_matrix_validation.json` shows `"validation_status": "PASS"` for the version it is reading. A `FAIL` status (e.g. a re-run introduces a constant column or a leakage mismatch) blocks all downstream use until resolved and re-validated — never trained around silently.

## Versioning rules

1. Any change to a feature's formula, a new feature, a removed feature, or a changed threshold (variance/correlation/VIF) requires: (a) a `10_decision_log.md` entry stating what changed and why, (b) a new version number here and in `feature_profile.json`, (c) re-running the full validation suite (`feature_matrix_validation.json`) before the new version is used by Mission 06+.
2. `feature_matrix.parquet` is **read-only** once frozen — identical discipline to `dataset_contract.md` term 1 for `master_dataset.parquet`.
3. A version bump does not require re-litigating already-closed decisions (e.g. the FinBERT-vs-lexicon sentiment choice) — only the specific term that changed.

---

## Definition of Done — this document

- [x] Feature Matrix Version, permitted consumers, and notebook dependencies stated unambiguously
- [x] Target variable and prediction horizon frozen (single target, no scope creep to secondary horizons)
- [x] Scaling and encoding rules stated as hard requirements, not guidelines
- [x] Baseline-eligibility table enforces the market-only vs. event-enhanced boundary at the contract level, not left to per-notebook discretion
- [x] Validation-gate and versioning rules stated so no notebook can silently train on an unvalidated or superseded matrix
