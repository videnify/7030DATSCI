# Baseline Evaluation — `Baseline_LASSO` v1.0

**Purpose:** The complete evaluation record for the market-only baseline — every metric SAP v1.0 requires, the comparison-baseline context (Part D), reproducibility record (Part F), interpretation (Part G), QA checks (Part I), and Research Statistician sign-off (Part K). This is the evidence file `09_results_log.md`'s baseline entry cites.
**Owner:** Research Statistician sign-off.
**Dependencies:** `baseline_model_specification.md`, `model_contract.md`, `reports/baseline/baseline_metrics.json`, `reports/baseline/baseline_predictions.parquet`, `statistical_reporting_guidelines.md` (rounding/CI conventions applied throughout).
**Update Frequency:** Update only alongside a new Baseline model version.
**Relation to Dissertation:** Direct source for dissertation Chapter 4 §4.4's baseline row and the RQ3 framing in Chapter 3 §3.5.

---

## Part E — Model Evaluation (source: `reports/baseline/baseline_metrics.json`)

### Regression metrics

| Split | RMSE | MAE | R² | Dir. Acc | IC |
|---|---|---|---|---|---|
| Train (n=1,761) | 0.012035 | 0.007615 | 0.000 | 0.547 | not defined (constant prediction — see note) |
| Test (n=750) | 0.009632 | 0.006551 | −0.002 | 0.575 | not defined (constant prediction — see note) |

**IC note:** the Information Coefficient (Spearman rank correlation between prediction and actual) is undefined when the prediction series has zero variance — every `Baseline_LASSO` prediction is the same constant value (see "Result of tuning" in `baseline_model_specification.md`), so there is no rank information to correlate. This is reported as "not defined," not as `0`, to avoid implying a computed-and-null correlation where none exists.

### Classification-style metrics (direction-as-class framing, test split)

Framing: `actual > 0` → class 1 ("up"), same for the prediction. This is a derived reporting lens on the existing regression output, not a second model — required by Part E's "if classification" fields, computed without training anything beyond `Baseline_LASSO` itself.

One-sample framing on `fwd_return_1d` direction, n = 750: precision = 0.575, recall = 1.000, F1 = 0.730, accuracy = 0.575, ROC-AUC = 0.500.

**Confusion matrix (test, n=750):**

| | Predicted Up | Predicted Down |
|---|---|---|
| **Actual Up** | TP = 431 | FN = 0 |
| **Actual Down** | FP = 319 | TN = 0 |

Recall = 1.000 and TN/FN = 0 are mechanical consequences of a constant positive prediction (every row is called "up"), not evidence of skill — the model has no ability to call a "down" day, ever. ROC-AUC = 0.500 is the correct, expected value for a constant score (a constant has no rank-ordering power, so the ROC curve is the diagonal by construction) and is the single clearest piece of evidence that this "precision"/"recall" pair reflects the test period's base rate (431/750 = 57.5% up days), not predictive discrimination.

**Calibration:** Not applicable — `Baseline_LASSO` is a point-forecast linear regressor, not a probabilistic classifier; no calibration curve is defined for a single constant point prediction.

### Residual diagnostics (test split)

One-sample residual analysis on `fwd_return_1d − prediction`, n = 750: mean = 0.000406, std = 0.009630, skewness = 0.601, excess kurtosis = 18.005, Durbin-Watson = 2.111 (no material autocorrelation), Jarque-Bera statistic = 10175.6, p < 0.001 (residuals strongly non-normal — expected for daily financial returns, consistent with the existing full-feature LASSO's residual diagnostics, kurtosis 17.26, `models/residual_diagnostics.json`), heteroskedasticity correlation ≈ 0 (4.2×10⁻¹⁶, i.e. exactly zero to numerical precision — mechanically expected, since a constant prediction cannot correlate its residual magnitude with anything it predicts).

### Prediction intervals (empirical residual-quantile method, frozen SAP v1.0)

90% PI: [−0.019071, +0.015582] around the point prediction. 95% PI: [−0.025885, +0.021391]. Computed from train-split residual quantiles only, per `04_statistics_plan.md`'s frozen method — not yet conditioned on any regime (the SAP explicitly defers a heteroskedasticity-aware interval as a future amendment).

### Confidence intervals

RMSE: block-bootstrap (block length 21 trading days, 2,000 resamples), 95% CI [0.007634, 0.012449] on test RMSE. Directional accuracy: Wilson score 95% CI [0.539, 0.610] on test Dir. Acc — the interval's lower bound (0.539) is still above 0.50, but see the Interpretation section below for why this should not be read as a real directional edge.

---

## Part D — Comparison baselines (context only, not official RQ3 contenders)

| Comparator | RMSE | MAE | R² | Dir. Acc | Justification for inclusion |
|---|---|---|---|---|---|
| Random Guess | 0.011443 | 0.008621 | −0.414 | 0.519 | Establishes the pure-chance floor — any model, including `Baseline_LASSO`, should be read against this before any "beats chance" claim |
| Persistence (predict = today's realised return) | 0.014003 | 0.009599 | −1.117 | 0.508 | The literature-standard weak-form-efficiency null; `Baseline_LASSO` clearing this is a minimal, expected bar, not a finding |
| Mean Predictor (train-mean, constant) | 0.009632 | 0.006551 | −0.002 | 0.575 | **Numerically identical to `Baseline_LASSO`** on every metric — see Interpretation below; included specifically because this identity is itself the headline finding of this mission |

---

## Part F — Reproducibility

| Item | Value |
|---|---|
| Python version | 3.10.12 (GCC 11.4.0) |
| scikit-learn version | 1.7.2 |
| Platform | Linux aarch64, glibc 2.35 |
| Random seed | 42 (`config.yaml: model.random_seed`) — passed to `LassoCV` and every CV-fold refit |
| Execution order | (1) Load `feature_matrix.parquet` + `feature_profile.json` → (2) filter to Market columns → (3) apply persisted scaling → (4) fit `LassoCV(cv=TimeSeriesSplit(5), random_state=42)` on train → (5) predict on train + test → (6) compute CV-fold diagnostics via `Lasso(alpha=alpha_)` refits per fold → (7) compute comparison baselines from the same test-split target → (8) persist model, metadata, predictions, metrics |
| Model version | `Baseline_LASSO v1.0` (MCP v1.0) |
| Hardware | Not load-bearing for reproducibility — no GPU, no hardware-dependent numerics used (CPU-only coordinate descent) |

Given identical inputs (`feature_matrix.parquet`, `feature_profile.json`), identical library versions, and the seed above, re-running the pipeline described in `baseline_model_specification.md` "Pipeline" reproduces `alpha_selected = 0.0018492955165777085` and the all-zero coefficient vector exactly — verified by re-running this build twice during this mission (see `10_decision_log.md`).

---

## Part G — Interpretation

**What the baseline represents:** `Baseline_LASSO` is the project's answer to "what can be predicted about tomorrow's SPY return using only today's price and technical-indicator history, with no knowledge of macro releases, political/monetary events, or sentiment." It is deliberately the same model *class* (regularised linear regression) already used for the full-feature LASSO, so that any future difference between it and the event-enhanced models in Mission 07 can be attributed to *information content*, not *model architecture*.

**What information it is allowed to use:** Exactly the 27 Market-category columns frozen in `feature_contract.md` — SPY price/return/volume history and technical indicators derived purely from SPY's own OHLCV series (returns, lags, cumulative returns, realised volatility, momentum, RSI, Bollinger Bands, moving-average trend flags). Nothing about VIX, Fed policy, CPI, unemployment, presidential communications, FOMC decisions, or sentiment reaches this model at any point in the pipeline (verified in Part I below).

**What it cannot use:** Every Macro, Sentiment, Event, Temporal, and Interaction feature in `feature_matrix.parquet` — 68 of the 95 frozen features are structurally invisible to this model.

**The headline finding — and why it is reported plainly, not smoothed over:** once genuinely tuned via cross-validated L1 regularisation (not left at a default alpha), `Baseline_LASSO` shrinks **all 27 Market coefficients to exactly zero** and reduces to predicting the training-split's unconditional mean return for every test-period day. Its RMSE, MAE, R², and directional accuracy are therefore numerically identical to the naive Mean Predictor comparator — this is not a coincidence or a bug, it is the same model. This is a legitimate, informative null result, consistent with `02_hypotheses.md`'s stated discipline that "a null result... is a valid dissertation finding and must be reported as such." It says: within a linear model, daily price/technical history alone does not contain exploitable signal for next-day SPY returns once the regularisation strength is chosen honestly by cross-validated error — a result entirely consistent with weak-form market efficiency and with this project's own already-reported observation that the full-feature LASSO's strongest signal came from `mean_car` (event) and `vix_vs_ma` (macro), not from price/technical features (`09_results_log.md`, 2026-07-04).

**Why the 57.5% directional accuracy is not a directional edge:** because the prediction is a positive constant, "directional accuracy" here collapses to "the fraction of test days SPY actually closed up" (431/750 = 57.5%). A model that always says "up" scores exactly this well regardless of any input data — this is mechanically confirmed by ROC-AUC = 0.500 (a constant score cannot rank-order anything). Any future model that reports directional accuracy without checking it against this baseline's mechanical floor risks mistaking test-period base rate for skill — a caveat that should carry into Mission 07/08's write-up explicitly.

**Why this is still the correct benchmark for RQ3:** RQ3 asks whether event information *adds* predictive value beyond market-only information. A baseline that itself contains no linear signal is not a weak or unfair comparator — it is the honest, undistorted answer to "what does market-only information alone achieve here," and it sets a genuinely low, non-arbitrary bar: an event-enhanced model claiming to "beat the baseline" must beat *this exact number* (RMSE 0.009632, Dir. Acc. 0.575 test), and given the Dir. Acc. figure is really just the test-period base rate, any claimed directional-accuracy improvement must be interpreted against that base rate explicitly, not against an assumed 50% chance line. This nuance is logged here precisely so Mission 07/08 do not have to rediscover it.

**No comparison against event-enhanced models is made in this document**, per this mission's Part G restriction — LASSO/XGBoost/LightGBM's full-feature numbers already exist in `09_results_log.md` (2026-07-04) but are not referenced against `Baseline_LASSO` here; that comparison, and the Diebold-Mariano/two-proportion z-test protocol, is Mission 07's task.

---

## Part I — Quality Assurance

| Check | Result |
|---|---|
| No event features used | ✅ Verified — `set(MARKET_FEATURES).isdisjoint(macro ∪ sentiment ∪ event ∪ temporal ∪ interaction)` asserted true at build time (0 overlap) |
| No sentiment leakage | ✅ Verified — same disjointness check; no sentiment-derived column name appears in the 27-feature list |
| No future leakage | ✅ Inherited from `feature_matrix_validation.json` (0 target-leakage mismatches, non-anticipative lag spot-check passed at the FES v1.0 freeze) — this mission adds no new engineered columns, so no new leakage surface was introduced |
| Correct train/test split | ✅ 1,761 train / 750 test, identical boundary to `feature_matrix.parquet`'s frozen `split` column — no independent re-split performed |
| Correct feature groups | ✅ Exactly the 27 names in `feature_contract.md`'s Market Baseline Eligibility list, cross-checked against `feature_profile.json.category_membership.market` |
| Correct random seed | ✅ `42` passed to `LassoCV` and every fold refit; confirmed reproducible across two independent re-runs this mission |
| Metrics reproducible | ✅ Identical `alpha_selected` and all-zero coefficient vector obtained on re-run |
| No undocumented preprocessing | ✅ The only preprocessing applied is the persisted `feature_profile.json` scaling transform — no additional imputation, winsorisation, or transformation introduced |

---

## Part K — Research Statistician Review

- **SAP compliance:** ✅ `TimeSeriesSplit` (not shuffled), seed 42, no outlier removal, no new statistical test introduced, scaling applied via the pre-frozen train-split parameters only.
- **FES compliance:** ✅ Reads `feature_matrix.parquet` unmodified; no feature redefinition; Market category taken exactly as frozen in `feature_contract.md`.
- **MCP compliance:** ✅ Matches `model_contract.md`'s Baseline role definition, hyperparameter/CV policy, and output locations exactly.
- **No prohibited features used:** ✅ Confirmed by the disjointness assertion in Part I.
- **All metrics follow SAP:** ✅ Rounding/reporting conventions applied per `statistical_reporting_guidelines.md` (RMSE/MAE to 6 d.p., R²/Dir.Acc to 3 d.p., p-values per convention).
- **No unsupported conclusions:** ✅ The all-zero-coefficient result is reported as a null finding about market-only linear predictability, not overstated as "the baseline is broken" or understated by silently re-tuning around it. The 57.5% directional accuracy is explicitly attributed to test-period base rate, not claimed as skill.

---

## Definition of Done — this document

- [x] Full SAP metric suite reported (RMSE/MAE/R²/Dir.Acc/IC, precision/recall/F1/ROC-AUC/confusion matrix, residual diagnostics, prediction intervals, CIs)
- [x] Comparison baselines (random/persistence/mean) reported with justification for each
- [x] Reproducibility fully documented (versions, seed, execution order)
- [x] Interpretation states what the baseline can/cannot use and why it is the correct RQ3 benchmark, without comparing to event-enhanced models
- [x] QA and Research Statistician review checklists both pass with no open items
