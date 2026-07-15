# Model Contract Protocol — MCP v1.0

**Purpose:** The governance layer above `feature_contract.md` — freezes which models are approved to exist in this project's RQ3 comparison, what role each plays, and the promotion criteria a model must clear to be reported as "beating the baseline." Distinct from `07_model_plan.md` (which narrates *why* each model was chosen) the same way `dataset_contract.md` is distinct from `dataset_version.md` — this document is the rulebook, not the narrative.
**Owner:** Research Statistician sign-off (evaluation/promotion rules), Senior Data Science Architect (pipeline/versioning authority).
**Dependencies:** `feature_contract.md` (what each model is allowed to read), `statistical_analysis_plan.md` Part A (scaling/CV/model-selection policy), `statistical_decision_matrix.md` Part K (the exact RQ3 comparison procedure this contract enforces), `07_model_plan.md`, `10_decision_log.md`.
**Update Frequency:** Update only if a contract *term* changes (a new approved model, a changed promotion rule). Retraining an already-approved model with new data or hyperparameters is a new model version, not a contract change.
**Relation to Dissertation:** Direct source for dissertation Chapter 3 §3.5 (Model Specification) — states precisely which models exist, why, and what "wins" means.

---

## Approved models (frozen)

**FES v1.1 implementation status (2026-07-14):** the approved roster and promotion rule are unchanged. Notebook 06 freezes the 27-feature `Baseline_LASSO` v1.1; Notebook 07 freezes all 92-feature candidates, the RQ2 Random Forest/SHAP outputs, and the corrected comparisons. Both validation reports are `PASS`.

| Role | Model | Feature scope | Status this mission |
|---|---|---|---|
| **Baseline** | `Baseline_LASSO` | Market category only (27 features, `feature_contract.md`) | ✅ v1.1 frozen; validation `PASS`; exact historical reproduction |
| Event-enhanced candidate | LASSO | Full 92-feature set | ✅ v1.1 frozen; 0/92 non-zero; exactly matches baseline |
| Event-enhanced candidate | XGBoost | Full 92-feature set | ✅ v1.1 frozen; does not beat baseline |
| Event-enhanced candidate | LightGBM | Full 92-feature set | ✅ v1.1 frozen; does not beat baseline |
| Feature-importance tool (RQ2 only) | Random Forest | Full 92-feature set | ✅ v1.1 regenerated; 92-row ranking; not an RQ3 candidate |

**A note on naming:** `Baseline_LASSO` and the Mission-07 "LASSO" are the same *algorithm* (regularised linear regression) but two distinct, separately-trained model objects with different feature scopes and different purposes — one is the floor RQ3 must clear, the other is a full-feature candidate being tested against that floor. They must never be conflated or share a saved-model file.

## Purpose

Establish, once, the minimum performance bar (`Baseline_LASSO`) that every event-enhanced model trained in Mission 07 must exceed on **both** RMSE and directional accuracy to be reported as answering H3/RQ3 affirmatively. Mission 06 trains and freezes this bar; nothing in Mission 07 may retrain, retune, or otherwise change it.

## Inputs

`data/processed/feature_matrix.parquet` (FES v1.1, read-only), `data/processed/feature_profile.json` (persisted train-split scaling parameters — never refit), `docs/research_bible/feature_contract.md` (Baseline Eligibility table — the sole authority on which columns `Baseline_LASSO` may read).

## Outputs

Notebook 06 writes the baseline model, metadata, row predictions, full metrics, hash-bound validation, and learning figure. Notebook 07 writes the three event models, Random Forest importance tool, suite metadata, row predictions, model comparison, corrected tests, RF/SHAP tables, hash-bound validation, and its learning figure. Exact paths are indexed in `models/README.md` and `reports/README.md`.

## Evaluation

Every model under this contract is evaluated on the identical frozen metric set (`statistical_analysis_plan.md` Part A, `statistical_reporting_guidelines.md`): RMSE, MAE, R², directional accuracy, IC (Spearman rank correlation between prediction and actual), plus — for the direction-as-binary-class framing — precision/recall/F1/ROC-AUC/confusion matrix, residual diagnostics (Durbin-Watson, Jarque-Bera, heteroskedasticity correlation), empirical residual-quantile prediction intervals (90%/95%), a block-bootstrap 95% CI on test RMSE (block length 21 trading days), and a Wilson-score 95% CI on directional accuracy. No new metric is introduced beyond what SAP v1.0 already specifies.

## Hyperparameter policy

Every model is tuned independently, on the training split only, with the same tuning discipline applied to the baseline as to every event-enhanced candidate (`statistical_analysis_plan.md` Part A "Model selection policy" — no model may win purely because it received more tuning effort than another). For `Baseline_LASSO`: `LassoCV`'s automatic coordinate-descent alpha-path search (scikit-learn), which is the same tuning mechanism the legacy full-feature LASSO model used — functionally equivalent in spirit to the "RandomizedSearchCV" wording in `07_model_plan.md`/SAP for a single continuous hyperparameter (alpha). XGBoost/LightGBM's tuning (Mission 07) will follow `config.yaml`'s fixed hyperparameter grid unless a Mission 07 decision log entry states otherwise.

## Cross-validation policy

`TimeSeriesSplit`, 5 folds, `random_state`/`random_seed` = 42 (`config.yaml: model.random_seed`), **never** a shuffled/random K-fold split — restated here as a hard requirement because the legacy baseline code (`src/models.py: _lasso_baseline`) passed `LassoCV(cv=5, ...)`, which defaults to a shuffled `KFold`, silently violating this policy. `Baseline_LASSO` in this mission passes an explicit `TimeSeriesSplit` object instead — see `10_decision_log.md` for this QA fix.

## Promotion criteria (restates `statistical_decision_matrix.md` Part K — not altered)

A Mission-07 event-enhanced model is reported as "beats the baseline" / supports rejecting H0₃ only if, on the test split: (1) its RMSE is significantly lower than `Baseline_LASSO`'s via Diebold-Mariano (or block-bootstrap CI if the DM stationarity pre-check fails), **and** (2) its directional accuracy is significantly higher via a two-proportion z-test — both at the Bonferroni-corrected α = 0.0167. A model clearing only one leg is a mixed result, never rounded up. Notebook 07 applied this rule: none of the three candidates clears either required improvement leg, so H0₃ is not rejected.

## Versioning

`Baseline_LASSO` is versioned identically to `feature_matrix.parquet` — retraining after Feature Matrix v1.1 creates `Baseline_LASSO v1.1`. Before the canonical paths are replaced, the prior version is copied to a dated archive and the migration is recorded in `10_decision_log.md`; old results are never silently relabelled. Model comparison against event-enhanced models (updating a shared comparison table and running DM/z-tests) is explicitly deferred to Mission 07, keeping “the baseline exists” and “the baseline has been compared” as two separable, auditable steps.

## Dependencies

`feature_contract.md`, `feature_profile.json`, `statistical_analysis_plan.md`, `statistical_decision_matrix.md` Part K, `config.yaml` (`model.random_seed`, `model.cv_splits`), `10_decision_log.md`.

---

## Definition of Done — this document

- [x] Approved models and roles frozen, with the Baseline/event-enhanced-LASSO naming distinction stated explicitly
- [x] Purpose, inputs, outputs, evaluation metric set, hyperparameter/CV policy, promotion criteria, versioning, and dependencies all specified
- [x] Promotion criteria restate (not alter) the already-frozen `statistical_decision_matrix.md` Part K procedure
- [x] The legacy shuffled-KFold bug in `src/models.py` is named and the fix (explicit `TimeSeriesSplit`) is recorded as this mission's applied correction
