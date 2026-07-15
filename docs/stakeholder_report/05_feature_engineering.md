# 5. Feature Engineering — Building the Table the Models Actually Learn From

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against `feature_profile.json` and `feature_matrix_validation.json` on disk, not copied from an earlier draft.
**Originally verified:** 2026-07-14 (FES v1.1 migration and freeze).
**Last reviewed against current pipeline:** 2026-07-15.
**Technical detail:** `notebooks/05_feature_engineering.ipynb` · [`feature_contract.md`](../research_bible/feature_contract.md) · [`06_feature_dictionary.md`](../research_bible/06_feature_dictionary.md)

---

## What this stage does

This stage assembles every input the predictive models will use into a single table: one row per trading day, one column per feature, split into a training period and a held-out test period that the models never see during training. This is the last stage before any model is actually fit — and it is deliberately the *only* stage allowed to create new predictor columns; everything before it collects and analyses, everything after it consumes what's built here.

## Why it matters

Building this table incorrectly (silently leaking future information, mixing train/test statistics, or double-counting a signal already captured another way) is one of the easiest ways for a modelling project to look successful for the wrong reasons. This project's feature contract exists specifically to prevent that, and this stage is where the contract is actually enforced.

## Inputs

Exactly two approved sources, per the project's feature contract — no others: `master_dataset.parquet` (v1.2, the frozen calendar of market/macro/sentiment data) and `car_results.parquet` (Stage 4's event-study output, 264 rows).

## Outputs

`data/processed/feature_matrix.parquet` — the current, frozen specification, **FES v1.1**:

| | Value |
|---|---|
| Total rows | 2,477 |
| Total columns | 95 (92 predictors + 1 target + 2 metadata: `date`, `split`) |
| Target | `fwd_return_1d` (next trading day's return) |
| Training rows | 1,727 |
| Test rows | 750 |
| Date range | 2016-02-24 to 2025-12-29 |

**Feature categories:** market 27, macro 16, sentiment 23, event 14, temporal 5, interaction 7.

A previous version, **FES v1.0** (95 predictors, 2,511 rows), is retained only as a historical/archived comparison point — it is not the current specification and should not be quoted as such.

## What was found

- **Three features were removed** between v1.0 and v1.1 because they carried exactly zero variance in the training split (`labour`, `energy`, `monetary_x_rate_cut`) — a feature that never varies cannot help any model, so keeping it would only add noise to feature-selection and importance results.
- **Three occurrence flags were redefined** (`health_event_day`, `labour_event_day`, `other_event_day`): previously these were inferred from non-zero sentiment, which meant a *neutral* event (common, since 94.9% of FinBERT scores are neutral) looked identical to *no event at all*. They now count direct catalogue occurrences instead, so a genuine but neutral-sentiment event is no longer invisible to the model.
- **No missing values, no constant columns, and no near-zero-variance columns** remain in the frozen matrix — the validation suite that checks for these passed cleanly.
- **Scaling is deliberately not baked into the stored file:** `feature_matrix.parquet` stores raw values; every model applies `(value − mean) / std` using parameters computed only from the training split and then persisted, so no information from the test period ever leaks into how features are scaled.
- **Some feature pairs are highly correlated** (e.g. `cum_return_21d`/`momentum_21d`, r = 0.997) — these are flagged as interpretability notes for later stages (they can distort which individual feature "gets credit" for an effect) but are not automatically deleted, since the project's plan treats this as a reporting caveat rather than an automatic exclusion rule.

## What was not found

No leakage between train and test splits, no duplicate feature columns, and no case where a feature computed from Stage 4's event data was found to violate the "no future information" rule.

## Limitations

Two feature pairs and a small number of macro/event interaction terms remain flagged for high correlation (|r| > 0.90) or elevated variance-inflation factors — this affects how individual coefficients should be interpreted (see Stage 7) but does not affect the overall predictive comparison, which evaluates whole models, not individual coefficients.

## How this connects to the next stage

Stage 6 trains a baseline model using only this table's 27 market-only columns (the only category a "market-only" comparison is allowed to see). Stage 7 trains the event-enhanced models using the full 92-feature table built here.

## Where to go for more detail

- The notebook itself: `notebooks/05_feature_engineering.ipynb`
- The formal feature contract (what's allowed, what isn't): [`feature_contract.md`](../research_bible/feature_contract.md)
- Column-by-column definitions: [`06_feature_dictionary.md`](../research_bible/06_feature_dictionary.md)
